import json
from pathlib import Path
from prepare import B,E,run
n='literal-b-simple-auto';c=next(x for x in json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8')) if x['name']==n);t=Path(c['target']);calls={};completed=[];failed=[]
for line in (E/(n+'-worker.jsonl')).read_text(encoding='utf-8').splitlines():
 try:
  x=json.loads(line)
  if x.get('type')=='assistant':
   for a in x.get('message',{}).get('content',[]):
    if a.get('type')=='tool_use':calls[a['id']]=a
  if x.get('type')=='user':
   for a in x.get('message',{}).get('content',[]):
    if isinstance(a,dict) and a.get('type')=='tool_result':
     q=calls.get(a.get('tool_use_id'),{});v={'id':a.get('tool_use_id'),'tool':q.get('name'),'input':q.get('input'),'is_error':a.get('is_error',False),'output':a.get('content')};completed.append(v)
     if v['is_error']:failed.append(v)
 except ValueError:pass
r={'case':n,'source_sha':c['source_sha'],'result':'FAIL','step':'5.4 step2: fill project-owned verify.sh','failed':failed,'completed_apply_and_helper_receipts':[v for v in completed if v['tool']=='Bash' and any(z in v.get('input',{}).get('command','') for z in [' install-overgate.py apply ','/install-overgate.py apply ','og-init-memory-bank.sh','bd-bootstrap.sh','og-protect-main.sh'])],'no_retry_or_alternative_after_deny':True,'head':run(['git','rev-parse','HEAD'],t).stdout.strip(),'status':run(['git','status','--porcelain'],t).stdout,'install_state':{k:v for k,v in json.loads((t/'.overgate/install-state.json').read_bytes()).items() if k in ['source_sha','mode','beads','format']},'verifier_text':(t/'.agents/project/verify.sh').read_text(encoding='utf-8')}
(E/(n+'-failure.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'result':r['result'],'source':r['source_sha'],'head':r['head'],'errors':len(failed)}))
