"""Reset only marker-owned synthetic R08 fixtures in development SQLite."""
import os,sys,uuid
from pathlib import Path
app=Path(sys.argv[1]).resolve()
if os.environ.get('DJANGO_ENV')!='development' or os.environ.get('DB_ENGINE')!='sqlite':raise SystemExit('Development SQLite only')
sys.path[:0]=[str(app/'backend'),str(app/'packages'),str(app)]
os.environ['DJANGO_SETTINGS_MODULE']='config.settings'
import django
django.setup()
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from family_bridge_features.f16_classroom.models import ClassAccount
from family_bridge_features.f07_mood.models import MoodEntry
from family_bridge_features.f01_identity.models import Connection
if settings.DATABASES['default']['ENGINE']!='django.db.backends.sqlite3':raise SystemExit('SQLite required')
with transaction.atomic():
 for code in ['HSR08M19','HSR08W19']:
  marker='review-r08:2026-10-19:'+code
  account=ClassAccount.objects.filter(external_ref=marker).first()
  if account is None:
   if ClassAccount.objects.filter(login_code=code).exists():raise SystemExit('Account collision')
   user=get_user_model().objects.create_user(username='r08-'+uuid.uuid4().hex,password='E2e-local-2026!',first_name='R08 synthetic')
   account=ClassAccount.objects.create(user=user,login_code=code,role='student',class_ref='F07-R08-20261019',external_ref=marker)
  if Connection.objects.filter(party_low_id=account.user_id).exists() or Connection.objects.filter(party_high_id=account.user_id).exists():raise SystemExit('Unexpected fixture connection')
  MoodEntry.objects.filter(owner_id=account.user_id).delete()
print('Two dedicated unconnected synthetic R08 actors ready; mood reset only for these markers.')
