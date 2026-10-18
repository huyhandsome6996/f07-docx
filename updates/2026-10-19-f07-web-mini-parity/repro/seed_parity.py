"""Create isolated synthetic parity fixtures in a local SQLite checkout only."""
import datetime as dt
import os
from pathlib import Path
import sys
import uuid

app=Path(sys.argv[1]).resolve()
if os.environ.get('DJANGO_ENV')!='development' or os.environ.get('DB_ENGINE')!='sqlite':
    raise SystemExit('Local development SQLite required')
sys.path[:0]=[str(app/'backend'),str(app/'packages'),str(app)]
os.environ['DJANGO_SETTINGS_MODULE']='config.settings'
import django
django.setup()
from django.conf import settings
if settings.DATABASES['default']['ENGINE']!='django.db.backends.sqlite3':
    raise SystemExit('Refusing non-SQLite fixtures')
from django.contrib.auth import get_user_model
from django.db import transaction
from family_bridge_features.f01_identity.models import Connection
from family_bridge_features.f16_classroom.models import ClassAccount
from family_bridge_features.f07_mood.models import MoodEntry

User=get_user_model()
actors=[]
with transaction.atomic():
    for code,role in [('HSPAR19','student'),('PHPAR19','caregiver')]:
        marker=f'review-parity:2026-10-19:{role}'
        account=ClassAccount.objects.filter(external_ref=marker).first()
        if account is None:
            if ClassAccount.objects.filter(login_code=code).exists():
                raise SystemExit('Refusing an account-code collision')
            user=User.objects.create_user(username=f'parity-{uuid.uuid4()}',first_name=f'{role} synthetic parity',password='E2e-local-2026!')
            account=ClassAccount.objects.create(user=user,login_code=code,role=role,class_ref='F07-REVIEW-PARITY-20261019',external_ref=marker)
        actors.append(account.user)
    low,high=sorted(str(actor.pk) for actor in actors)
    active=Connection.objects.filter(party_low_id=low,party_high_id=high,status='active').exists()
    if not active:
        if Connection.objects.filter(party_low_id=low,party_high_id=high).exists():
            raise SystemExit('Refusing to revive a revoked fixture connection')
        Connection.objects.create(party_low_id=low,party_high_id=high,relationship_kind='primary',invite=None,source='admin_provisioned',source_admin='synthetic-local-parity-review',status='active',generation=1)
    MoodEntry.objects.get_or_create(owner=actors[0],entry_date=dt.datetime.now(dt.timezone(dt.timedelta(hours=7))).date(),defaults={'emotion':'vui','note':'Nội dung tổng hợp để kiểm thử hai giao diện; không có dữ liệu người tham gia thật.'})
print('Synthetic local parity fixtures ready; existing non-fixture accounts unchanged.')
