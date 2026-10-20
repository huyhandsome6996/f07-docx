"""Independent F07 review checks. Run through Django's test runner only.

Uses disposable Django test databases, synthetic users, real F01 reader and
real F07 services. A patch controls timing of two reads; it does not replace
authorization, persistence, edit, share or recipient reads.
"""
import datetime as dt
import threading
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import connection, connections
from django.test import TransactionTestCase
from rest_framework.test import APIClient

from family_bridge_core.errors import NotFound, PreviewStale
from family_bridge_features.f01_identity.models import Connection
from family_bridge_features.f07_mood.apps import wire_production_ports
from family_bridge_features.f07_mood.models import MoodEntry
from family_bridge_features.f07_mood.services import mood, registry


class IndependentReviewTests(TransactionTestCase):
    def setUp(self):
        registry.reset_registries()
        wire_production_ports()
        user = get_user_model()
        self.owner_a = user.objects.create_user(username='review-owner-a')
        self.owner_b = user.objects.create_user(username='review-owner-b')
        self.recipient = user.objects.create_user(username='review-recipient')
        for owner in (self.owner_a, self.owner_b):
            low, high = sorted([str(owner.pk), str(self.recipient.pk)])
            Connection.objects.create(party_low_id=low, party_high_id=high,
                                      relationship_kind='primary', invite=None,
                                      source='admin_provisioned', source_admin='synthetic-review',
                                      status='active', generation=1)

    def entry(self, owner):
        return mood.MoodEntryService().create(owner_id=str(owner.pk), entry_date=None,
                                             emotion='vui', note='synthetic review note')

    def test_R03_recipient_lists_grants_from_two_owners(self):
        shares = []
        for owner in (self.owner_a, self.owner_b):
            entry = self.entry(owner)
            shares.append(mood.MoodShareService().share(owner_id=str(owner.pk),
                entry_id=str(entry.pk), recipient_id=str(self.recipient.pk), expected_revision=1))
        for share in shares:
            self.assertEqual(mood.MoodShareService().read_shared(
                recipient_id=str(self.recipient.pk), share_id=str(share.pk))['entry']['revision'], 1)
        listed, cursor = mood.MoodShareService().list_shared_with_me(
            recipient_id=str(self.recipient.pk), page_size=20)
        print(f'REVIEW-R03: individually_readable=2 listed={len(listed)} expected=2')
        self.assertEqual({str(s.pk) for s in listed}, {str(s.pk) for s in shares})

    def test_R05_date_suffix_is_rejected_by_actual_view(self):
        api = APIClient()
        api.force_authenticate(user=self.owner_a)
        day = (dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).date()
               - dt.timedelta(days=10)).isoformat()
        response = api.post('/api/v1/mood/entries',
            {'entry_date': day + '-not-an-ISO-date', 'emotion': 'vui'}, format='json')
        print(f'REVIEW-R05: invalid_date_http={response.status_code} expected=400')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(MoodEntry.objects.filter(owner=self.owner_a).exists())

    def test_R02_concurrent_edits_cannot_reuse_shared_revision(self):
        if connection.vendor != 'mysql':
            self.skipTest('Requires real MySQL for concurrent committed writes')
        entry = self.entry(self.owner_a)
        owner_id, entry_id, recipient_id = map(str, (self.owner_a.pk, entry.pk, self.recipient.pk))
        first_read = threading.Event()
        second_read = threading.Event()
        release_first = threading.Event()
        first_done = threading.Event()
        grant_done = threading.Event()
        errors = []
        grants = []
        share_outcomes = []
        real_read = mood._require_own_entry

        def read_with_schedule(**kwargs):
            result = real_read(**kwargs)
            name = threading.current_thread().name
            if name == 'review-first-edit':
                first_read.set()
                if not release_first.wait(timeout=15):
                    raise TimeoutError('First edit was not released')
            elif name == 'review-second-edit':
                second_read.set()
                # If a corrected implementation holds a row lock here,
                # the share may legitimately wait for this edit to commit.
                # Bounded waiting allows that safe serialization to finish.
                grant_done.wait(timeout=2)
            return result

        def edit_worker(note, first):
            try:
                mood.MoodEntryService().edit(owner_id=owner_id, entry_id=entry_id,
                                             emotion=None, note=note)
            except Exception as exc:
                errors.append(type(exc).__name__)
            finally:
                connections.close_all()
                if first:
                    first_done.set()

        def share_worker():
            try:
                grants.append(mood.MoodShareService().share(owner_id=owner_id,
                    entry_id=entry_id, recipient_id=recipient_id, expected_revision=2))
                share_outcomes.append('shared')
            except PreviewStale:
                share_outcomes.append('preview_stale')
            except Exception as exc:
                errors.append(type(exc).__name__)
            finally:
                connections.close_all()
                grant_done.set()

        with patch.object(mood, '_require_own_entry', side_effect=read_with_schedule):
            first = threading.Thread(name='review-first-edit', target=edit_worker,
                args=('synthetic approved version', True))
            second = threading.Thread(name='review-second-edit', target=edit_worker,
                args=('synthetic unapproved version', False))
            first.start()
            self.assertTrue(first_read.wait(timeout=15), 'First edit did not read')
            second.start()
            # Old code reads revision 1 immediately; correct row locking
            # may block the second read until the first commit, which is safe.
            second_read.wait(timeout=1)
            release_first.set()
            self.assertTrue(first_done.wait(timeout=20), 'First edit did not finish')
            sharing = threading.Thread(name='review-share', target=share_worker)
            sharing.start()
            first.join(timeout=20)
            second.join(timeout=20)
            sharing.join(timeout=20)
            self.assertFalse(first.is_alive() or second.is_alive() or sharing.is_alive(), 'Worker timeout')
        self.assertEqual(errors, [])
        self.assertIn(share_outcomes, [['shared'], ['preview_stale']])
        entry.refresh_from_db()
        unapproved_readable = False
        if grants:
            try:
                data = mood.MoodShareService().read_shared(recipient_id=recipient_id, share_id=str(grants[0].pk))
            except NotFound:
                pass
            else:
                unapproved_readable = data['entry']['note'] == 'synthetic unapproved version'
        print(f'REVIEW-R02: final_revision={entry.revision} unapproved_readable={unapproved_readable}; expected monotonic revision and denied unapproved read')
        self.assertFalse(unapproved_readable, 'A grant approved for the first edit exposed the second edit')
        self.assertEqual(entry.revision, 3, 'Two committed edits reused one revision')
