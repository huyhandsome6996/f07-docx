import csv, json, os, secrets, subprocess
from pathlib import Path
root=Path(os.environ.get('F04_AUDIT_DIR','/tmp/f04-audit'));source=root/'source';py=str(root/'venv/bin/python')
secret=root/'.synthetic-credentials.json'
if not secret.exists():
    secret.write_text(json.dumps({'password':secrets.token_urlsafe(22)}));secret.chmod(0o600)
password=json.loads(secret.read_text())['password']
accounts=root/'synthetic.csv'
with accounts.open('w') as f:
    w=csv.writer(f);w.writerow(['external_ref','login_code','role','class_ref','display_name'])
    for i in range(941,946):
        for prefix,role in [('HS','student'),('PH','caregiver')]:
            w.writerow([f'audit-f04-{prefix}{i}',f'{prefix}{i}',role,'F04-LOCAL-SYNTHETIC',f'Audit {prefix}{i}'])
env=dict(os.environ,DJANGO_ENV='development',DB_ENGINE='sqlite',FB_CLASS_INITIAL_PASSWORD=password)
with (root/'evidence/fixtures.log').open('w') as log:
    subprocess.run([py,'manage.py','provision_classroom','--csv',str(accounts),'--auto-pair-by-index','--json'],cwd=source/'backend',env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
print('Synthetic browser accounts prepared.')
