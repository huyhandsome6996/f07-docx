"""Synthetic F02 QA fixture on a NEW checkout-local SQLite DB only."""
import argparse
import os
from pathlib import Path
import sys
import uuid

parser = argparse.ArgumentParser()
parser.add_argument("--app-root", required=True)
args = parser.parse_args()
root = Path(args.app_root).resolve()
db = root / "backend" / "db.sqlite3"
if db.exists() or (root / "backend" / ".env").exists():
    raise SystemExit("Use a fresh disposable checkout without a DB or backend/.env.")
password = os.environ.get("F02_QA_PASSWORD", "")
if len(password) < 12:
    raise SystemExit("Set F02_QA_PASSWORD to a synthetic value >=12 characters.")
os.environ.update(DJANGO_SETTINGS_MODULE="config.settings", DJANGO_ENV="development",
                  DB_ENGINE="sqlite", FB_ZALO_LOGIN_ENABLED="false")
sys.path.insert(0, str(root / "backend"))
import django
django.setup()
from django.conf import settings
assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
assert Path(settings.DATABASES["default"]["NAME"]).resolve() == db
from django.core.management import call_command
from django.contrib.auth import get_user_model
from family_bridge_features.admin_core.models import AdminCapabilityGrant, ContentItem
from family_bridge_features.admin_core.services.admin import ContentLifecycleService
from family_bridge_features.f16_classroom.services.admin_provision import apply_pairs
from family_bridge_features.f01_identity.models import Connection, ConsentRecord

call_command("migrate", verbosity=0)
operator = get_user_model().objects.create_user(username="synthetic-f02-qa-operator")
AdminCapabilityGrant.objects.create(
    user=operator, capability="classroom.provision", scope_type="school",
    scope_ref="F02-QA-20261019", granted_by="synthetic-fixture-bootstrap")
rows = [{"student_code": f"HS{i}", "caregiver_code": f"PH{i}",
         "student_name": f"Học sinh thử F02 {i}",
         "caregiver_name": f"Phụ huynh thử F02 {i}"} for i in (901, 903)]
result = apply_pairs(operator, class_ref="F02-QA-20261019", rows=rows,
                     batch_ref=str(uuid.uuid4()), initial_password=password)
assert result["ok"] and result["connected"] == 2, "Provisioning failed."
assert Connection.objects.filter(status="active", invite__isnull=True,
                                 source="admin_provisioned").count() == 2
assert ConsentRecord.objects.count() == 0, "Admin must not consent for participants."
call_command("seed_f02_draft_program", verbosity=0)
svc = ContentLifecycleService()
for item in ContentItem.objects.filter(status="draft",
        kind__in=("f02_program", "activity", "micro_lesson")):
    item.title = "[THỬ LOCAL] " + item.title
    item.save(update_fields=["title"])
    svc.publish(actor_id="synthetic:f02-qa-local", content_id=str(item.id),
                expected_revision=item.revision)
activity = ContentItem.objects.get(content_key="f09-w1-tieng-long-chua-noi",
                                    status="published")
new = svc.clone_draft(actor_id="synthetic:f02-qa-local", content_id=str(activity.id))
svc.publish(actor_id="synthetic:f02-qa-local", content_id=str(new.id),
            expected_revision=new.revision)
print("Created fresh LOCAL SQLite fixture: HS901/PH901, HS903/PH903.")
print("Admin pairs active, no consent on behalf; synthetic published content.")
print("Activity week1 has published revisions 1 and 2 for independent UI QA.")
