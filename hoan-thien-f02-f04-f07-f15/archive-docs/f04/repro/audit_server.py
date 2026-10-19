import os, sys
from pathlib import Path
source=Path(os.environ.get('F04_AUDIT_DIR','/tmp/f04-audit'))/'source'
sys.path[:0]=[str(source/'backend'),str(source/'packages'),str(source)]
os.environ.update(DJANGO_SETTINGS_MODULE='config.settings',DJANGO_ENV='development',DB_ENGINE='sqlite',CORS_ALLOWED_ORIGINS='http://127.0.0.1:5144,http://127.0.0.1:3044')
import django
django.setup()
from family_bridge_features.f04_ai.services import registry
class AuditProvider:
    provider_id='LOCAL_SYNTHETIC_PROVIDER'
    def refine(self,**kwargs):
        if 'AUDIT_FORCE_OUTAGE' in kwargs['text']:
            class Outage(Exception):fb_provider_reason='provider_outage'
            raise Outage()
        return {'suggested_text':'AUDIT_FINAL_SUGGESTION — Tôi muốn được lắng nghe.','provider_id':self.provider_id,'model_revision':'synthetic','prompt_revision':'synthetic'}
registry.register_ai_provider(AuditProvider())
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py','runserver','127.0.0.1:8044','--noreload'])
