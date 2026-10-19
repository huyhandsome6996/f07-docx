"""Additional QA on the named disposable local fixture, after http_qa/UI."""
import argparse
import json
import os
from pathlib import Path
import sys
import uuid
from urllib.error import HTTPError
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument("--app-root", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()
root = Path(args.app_root).resolve()
assert not (root / "backend" / ".env").exists()
os.environ.update(DJANGO_SETTINGS_MODULE="config.settings", DJANGO_ENV="development",
                  DB_ENGINE="sqlite", FB_ZALO_LOGIN_ENABLED="false")
sys.path.insert(0, str(root / "backend"))
import django
django.setup()
from django.conf import settings
assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
assert Path(settings.DATABASES["default"]["NAME"]).resolve() == root/"backend"/"db.sqlite3"
from django.contrib.auth import get_user_model
from family_bridge_features.f16_classroom.models import ClassAccount
from family_bridge_features.f16_classroom.services.admin_provision import apply_pairs
from family_bridge_features.admin_core.models import ContentItem
from family_bridge_features.admin_core.services.admin import ContentLifecycleService
from family_bridge_features.f09_activities.models import SharedActivityInvite
assert ClassAccount.objects.filter(class_ref="F02-QA-20261019").count() == 4

results = []
def check(name, passed, actual):
    results.append({"name": name, "pass": bool(passed), "actual": actual})
    print(("PASS " if passed else "FAIL ") + name)
def call(path, token=None, body=None):
    headers = {"Content-Type":"application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = Request("http://127.0.0.1:8004/api/v1" + path, headers=headers,
        data=None if body is None else json.dumps(body).encode())
    try:
        with urlopen(req, timeout=15) as response:
            return response.status, json.load(response)
    except HTTPError as err:
        return err.code, json.load(err)

key = "dong-hanh-bon-tuan"
activity = "f09-w1-tieng-long-chua-noi"
student = ClassAccount.objects.get(login_code="HS903")
sent = SharedActivityInvite.objects.filter(
    inviter=student.user, content_key=activity).order_by("-updated_at").first()
check("UI invitation uses latest published activity revision2",
      sent is not None and sent.content_revision == 2,
      None if sent is None else {"content_revision":sent.content_revision, "status":sent.status})
operator = get_user_model().objects.get(username="synthetic-f02-qa-operator")
created = apply_pairs(operator, class_ref="F02-QA-20261019",
    rows=[{"student_code":"HS905","caregiver_code":"PH905",
           "student_name":"Học sinh thử phiên bản","caregiver_name":"Phụ huynh thử phiên bản"}],
    batch_ref=str(uuid.uuid4()), initial_password=os.environ["F02_QA_PASSWORD"])
assert created["ok"]
tokens = []
for code in ("HS905", "PH905"):
    status, data = call("/auth/class-session",
        body={"code":code, "password":os.environ["F02_QA_PASSWORD"]})
    assert status == 200
    token = data["token"]
    tokens.append(token)
    status, data = call("/program/enroll", token, {"program_key":key,"program_revision":1})
    assert status == 201
status, proposal1 = call("/program/agreement/propose", tokens[0], {"program_key":key})
assert status == 201 and proposal1["status"] == "proposed"
source = ContentItem.objects.get(kind="f02_program", status="published", revision=1)
svc = ContentLifecycleService()
new = svc.clone_draft(actor_id="synthetic:qa-version", content_id=str(source.id))
body = json.loads(new.body)
body["weeks"][0]["student_guide"] += " [Nội dung hướng dẫn mới cho QA rev2]"
new.body = json.dumps(body, ensure_ascii=False)
new.save(update_fields=["body"])
svc.publish(actor_id="synthetic:qa-version", content_id=str(new.id),
            expected_revision=new.revision)
for token in tokens:
    status, data = call("/program/enroll", token, {"program_key":key,"program_revision":2})
    assert status == 201 and data["program_revision"] == 2
status, proposal2 = call("/program/agreement/propose", tokens[0], {"program_key":key})
check("new program revision with unchanged agreement template does not reuse wrong pin",
      status == 201 and proposal2.get("program_revision") == 2,
      {"status":status,"old_agreement_id":proposal1["agreement_id"],"proposal":proposal2})
status, data = call("/program/agreement/" + proposal2["agreement_id"] + "/confirm", tokens[0], {})
check("both repinned users can confirm a proposal on their new program revision",
      status == 200, {"status":status,"response":data})
activity_row = ContentItem.objects.filter(content_key=activity,status="published").order_by("-revision").first()
print("ACTIVITY BODY", activity_row.body)
Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
