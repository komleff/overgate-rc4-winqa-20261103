import sys,json,re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from prepare import S,E,SHA,run
def check(c):
 n=c['name'];t=Path(c['target'])
 args=[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',t,'--contract',c['contract'],'--target-pr',c['pr'],'--output',E/(n+'-noop-plan.json')]
 p=run(args,label=n+'-noop',ok=False)
 data=json.loads((E/(n+'-noop-plan.json')).read_bytes()) if p.returncode==0 else None
 mismatches=[{'target':x['target'],'before':x['before'],'after':x['after']} for x in data['operations'] if x['before']!=x['after']] if data else []
 state=(t/'.overgate/install-state.json').read_text(encoding='utf-8')
 result={'name':n,'exit_code':p.returncode,'no_conflicts':data is not None and not data['conflicts'],'operations_equal':data is not None and not mismatches,'mismatches':mismatches,'portable_state_no_absolute_path':not re.search(r'(?i)(?:[A-Z]:[\\/]|"/(?:Users|home|tmp|work|private)/)',state),'target_head':run(['git','rev-parse','HEAD'],t).stdout.strip(),'target_branch':run(['git','branch','--show-current'],t).stdout.strip()}
 run(['git','status','--short'],t,label=n+'-final-status')
 run(['C:/Program Files/Git/bin/bash.exe','.agents/project/verify.sh'],t,label=n+'-final-verify',ok=False)
 (E/(n+'-noop-results.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='mismatches'}),flush=True)
 return result
if __name__=='__main__':
 names=set(sys.argv[1:]); cs=[c for c in json.loads((E/'targets.json').read_text(encoding='utf-8')) if c['name'] in names]
 with ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(check,cs))
