import json,sys,subprocess
from prepare import B,E,run
SHA='2343df83a3a26ae83bc66d4009dd67a913eeea4e';results=[]
for c in json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8'))[2:]:
 head=run(['gh','pr','view','12','-R','komleff/overgate','--json','headRefOid','--jq','.headRefOid']).stdout.strip()
 if head!=SHA:
  print('HEAD_MOVED',head,flush=True);sys.exit(42)
 print('CASE_START',c['name'],flush=True)
 p=subprocess.run([sys.executable,str(B/'run-claude.py'),c['name']+'-worker',c['target'],c['runtime_mode'],str(B/(c['name']+'-worker-prompt.txt'))])
 final=E/(c['name']+'-final-audit.json');audit=json.loads(final.read_text(encoding='utf-8')) if final.exists() else None
 status='PASS' if p.returncode==0 and audit is not None and audit['result']=='PASS' else 'FAIL'
 results.append({'case':c['name'],'source_sha':SHA,'exit_code':p.returncode,'result':status,'final_audit_exists':final.exists()});(E/'literal-b-remaining-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 print('CASE_DONE',c['name'],status,flush=True)
 if status!='PASS':sys.exit(1)
