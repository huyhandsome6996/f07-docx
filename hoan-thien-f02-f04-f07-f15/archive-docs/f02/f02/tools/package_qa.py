"""Package sanitized F02 QA evidence with provenance; preserve F07 archives."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--app-root", required=True)
parser.add_argument("--run-log-dir", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
app = Path(args.app_root).resolve()
logs = Path(args.run_log_dir).resolve()
review = root / "f02" / "qa" / "2026-10-19-c29469b"
evidence = review / "evidence"
evidence.mkdir(parents=True, exist_ok=True)
sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=app, text=True).strip()
assert sha == "c29469b3d57f2c2cc53fe686fe7ec8f917f2dec6"
for name in ("backend.log","miniapp.log","shared-mobile.log","web.log",
             "miniapp-build.log","web-build.log","boundaries.log","http.log"):
    shutil.copyfile(logs/name, evidence/name)
ref = root / "f02" / "reference" / "c29469b"
paths = [
    "docs/features/f02/scope.md",
    "docs/product/four-week-flow.md",
    "docs/handover/f02-qa/06-RESUME-HANDOVER.md",
    "packages/family_bridge_features/f02_program/models.py",
    "packages/family_bridge_features/f02_program/services/program.py",
    "packages/family_bridge_features/f02_program/wiring.py",
    "packages/family_bridge_features/f09_activities/services/activities.py",
    "packages/family_bridge_features/f09_activities/wiring.py",
    "zalo-mini-app/src/pages/companion/index.js",
    "web/src/pages/companion/index.js",
]
for name in paths:
    target = ref / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(subprocess.check_output(["git", "show", sha+":"+name], cwd=app))
provenance = {
    "review_date":"2026-10-19", "timezone":"Asia/Ho_Chi_Minh",
    "application_repository":"https://github.com/huyhandsome6996/family-bridge",
    "application_branch":"tinh-nang/f02-dong-hanh-bon-tuan-us036-us044",
    "application_sha":sha,
    "application_main_sha":"ee1346a32bb5adaee7fdb7e842fceb7b9b8c32d0",
    "documents_repository":"https://github.com/huyhandsome6996/f07-docx",
    "documents_branch":"F02-docx",
    "documents_base_main_sha":"a4a4b0982db5ae5cd48892d0e8ebf85ba407fdd2",
    "application_tracked_changes":subprocess.check_output(["git","status","--short"],cwd=app,text=True),
    "database":"SQLite disposable local, production backend settings in development mode",
    "fixture_class":"F02-QA-20261019",
    "real_participant_data":False,"production_database_accessed":False,
    "mysql_tested":False,"zalo_device_tested":False,
    "application_committed_or_pushed":False,"deployed":False,
    "snapshot_paths":paths,
    "scope":"QA, local fixture and docs only; snapshots are read-only evidence.",
}
(review/"PROVENANCE.json").write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding="utf-8")
# Manifest is limited to F02 artifacts and F02 root entry points; inherited
# F07 catalogs and original bundles deliberately remain byte-identical.
files = sorted(p for p in (root/"f02").rglob("*") if p.is_file()
               and p.name != "SHA256SUMS" and "__pycache__" not in p.parts)
files += [root/"PROMPT-COPY-F02.md",root/"README.md",root/"AGENTS.md",root/".gitattributes"]
# Scoped .gitattributes specifies LF for these textual artifacts. Normalize
# before hashing so committed blobs and fresh Windows/Linux checkouts agree.
for p in files:
    if p.suffix.lower() not in {".jpg", ".png", ".zip"}:
        raw = p.read_bytes()
        p.write_bytes(raw.replace(b"\r\n", b"\n"))
rows = [hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(root).as_posix()
        for p in files]
(root/"f02"/"SHA256SUMS").write_text("\n".join(rows)+"\n",encoding="utf-8")
print(f"Packaged {len(files)} F02 files with SHA256 manifest.")
