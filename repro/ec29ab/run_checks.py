from pathlib import Path
import subprocess,os,json,sys,time
root=Path(__file__).resolve().parent;source=root/'source';py=str(root/'venv/bin/python');ev=root/'evidence'
env=dict(os.environ,DJANGO_ENV='test',DB_ENGINE='sqlite',F04_AUDIT_DIR=str(root))
commands={
'backend': [('foundation',[py,'manage.py','test','--noinput'],source/'backend',{}),('backend-check',[py,'manage.py','check'],source/'backend',{}),('migration-drift',[py,'manage.py','makemigrations','--check','--dry-run'],source/'backend',{})],
'feature':[('feature-f04',[py,'manage.py','test','harness','labgrants','family_bridge_features.f04_ai','family_bridge_features.f05_inbox','family_bridge_features.f06_drafts','family_bridge_features.f15_privacy','--noinput'],source/'tests/feature-lab',dict(DJANGO_SETTINGS_MODULE='harness.settings',FB_FEATURES='f01_identity,f04_ai,f05_inbox,f06_drafts,f15_privacy'))],
'web':[('web-test',['npm','test'],source/'web',{}),('web-build',['npm','run','build'],source/'web',{})],
'mini':[('mini-test',['npm','test'],source/'zalo-mini-app',{}),('mini-build',['npm','run','build'],source/'zalo-mini-app',{})],
'shared':[('shared',['bash','-c','node --test packages/family_bridge_shared/tests/*.test.mjs packages/family_bridge_shared/tests/test_f04_contract_a5.mjs packages/family_bridge_mobile/f04_ai/tests/*.mjs tests/qa-f04/*.test.mjs'],source,{}),('boundaries',['node','scripts/check_import_boundaries.mjs'],source,{}),('docs',['python3','scripts/check_agent_docs.py'],source,{})],
'probes':[('regression',[py,str(root/'independent_backend_probe.py')],root,{}),('claim-reuse',[py,str(root/'probe_claim_reuse.py')],root,{})]
}
results=[]
for name,cmd,cwd,extra in commands[sys.argv[1]]:
 t=time.monotonic()
 with (ev/(name+'.log')).open('w') as log:
  p=subprocess.run(cmd,cwd=cwd,env=dict(env,**extra),stdout=log,stderr=subprocess.STDOUT)
 item=dict(name=name,command=cmd,cwd=str(cwd),exit_code=p.returncode,seconds=round(time.monotonic()-t,2));results.append(item)
 print(json.dumps(item),flush=True)
 print('\n'.join((ev/(name+'.log')).read_text().splitlines()[-8:]),flush=True)
(ev/('commands-'+sys.argv[1]+'.json')).write_text(json.dumps(results,indent=2))
