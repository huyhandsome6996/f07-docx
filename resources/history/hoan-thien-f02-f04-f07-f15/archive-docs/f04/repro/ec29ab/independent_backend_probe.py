import os, sys, unittest
from pathlib import Path
root=Path(os.environ.get('F04_AUDIT_DIR','/tmp/f04-audit'))
source=root/'source'
sys.path[:0]=[str(source/'tests/feature-lab'),str(source/'packages'),str(source),str(root)]
os.environ.update(DJANGO_SETTINGS_MODULE='harness.settings',DJANGO_ENV='test',FB_FEATURES='f01_identity,f04_ai,f05_inbox,f06_drafts,f15_privacy')
import django
django.setup()
from django.test import TransactionTestCase
from django.test.utils import get_runner
from fixtures.actors import make_student
from family_bridge_features.f04_ai.services import registry as ai_registry
from family_bridge_features.f04_ai.services.express import AiExpressService
from family_bridge_features.f04_ai.services.deletion import AiSuggestionDeletionHook
from family_bridge_features.f04_ai.models import AiSuggestion,AiRefineOperation
from family_bridge_features.f04_ai.tests.test_f04 import grant_ai_consent
from family_bridge_features.f15_privacy.services import registry as privacy_registry
from family_bridge_features.f15_privacy.services.deletion import DeletionService
from family_bridge_features.f06_drafts.services.drafts import DraftService
from family_bridge_core.errors import CooldownActive
from labgrants.f06_fixtures import ControlledClock

class IndependentTests(TransactionTestCase):
    def test_ai_deletion_during_provider_wait_must_not_recreate_deleted_content(self):
        user=make_student();grant_ai_consent(user)
        privacy_registry.register_deletion_hook('ai','family_bridge_features.f04_ai.services.deletion.AiSuggestionDeletionHook')
        outcomes=[]
        class Provider:
            def refine(self,**kwargs):
                service=DeletionService()
                request=service.request_deletion(user=user,categories=['ai'])
                service.verify_request(request_id=request['request_id'],verifier_ref='synthetic-local-verification')
                completed=service.process_request(request_id=request['request_id'])
                outcomes.append({'deletion_status':completed.status,'suggestions_at_deletion':AiSuggestion.objects.filter(author=user).count(),'claims_at_deletion':AiRefineOperation.objects.filter(author=user).count()})
                return {'suggested_text':'Synthetic private suggestion','provider_id':'independent-test','model_revision':'test','prompt_revision':'test'}
        ai_registry.register_ai_provider(Provider())
        try:
            AiExpressService().refine(author_id=str(user.pk),original_text='Synthetic private draft',purpose='refine_expression',idempotency_key='independent-deletion-0001',input_revision=1)
        except Exception as e:
            outcomes.append({'finalize_error_type':type(e).__name__})
        remaining=AiSuggestion.objects.filter(author=user).count()
        print('DELETION_INFLIGHT_EVIDENCE',outcomes,'suggestions_after_provider=',remaining,flush=True)
        self.assertEqual(remaining,0,'A completed AI deletion must fence off a result from a pre-deletion request')

    def test_editing_a_paused_draft_must_not_bypass_300_second_gate(self):
        user=make_student();clock=ControlledClock();service=DraftService(clock=clock)
        draft=service.create(author_id=str(user.pk),kind='text',body='Synthetic original',recipient_id=str(user.pk))
        draft=service.start_pause(author_id=str(user.pk),draft_id=str(draft.id))
        deadline=draft.pause_deadline_at
        draft=service.edit(author_id=str(user.pk),draft_id=str(draft.id),body='Synthetic revised',recipient_id=str(user.pk))
        print('PAUSE_EDIT_EVIDENCE',{'status':draft.status,'deadline_preserved':draft.pause_deadline_at==deadline,'seconds_remaining':(deadline-clock.now()).total_seconds()},flush=True)
        with self.assertRaises(CooldownActive,msg='Editing must not implicitly cancel an opted-in pause'):
            service.make_preview(author_id=str(user.pk),draft_id=str(draft.id))

if __name__=='__main__':
    failures=get_runner(django.conf.settings)(verbosity=2,interactive=False).run_tests(['__main__.IndependentTests'])
    raise SystemExit(bool(failures))
