import json,subprocess
from pathlib import Path
from prepare import B,E,S,run
cs=json.loads((E/'e2e-targets.json').read_text(encoding='utf-8'));result=[]
for c in cs:
 t=Path(c['target']);n=c['name'];r={**c,'source_sha':'403f95b8a7fae50957a99c16a211a8ef7217cb22'}
 for label,args in [('head',['git','rev-parse','HEAD']),('branch',['git','branch','--show-current']),('status',['git','status','--short']),('index',['git','diff','--cached','--name-status']),('remote',['git','remote','-v']),('remote_refs',['git','ls-remote','--heads','origin'])]:
  p=run(args,t,label=n+'-resume-'+label,ok=False);r[label]={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 r['git_locks']=[str(p.relative_to(t)) for p in (t/'.git').rglob('*.lock')]
 r['beads_metadata_present']=(t/'.beads/metadata.json').exists()
 if r['beads_metadata_present']:r['beads_metadata']=json.loads((t/'.beads/metadata.json').read_bytes())
 r['beads_lock_paths']=[str(p.relative_to(t)) for p in (t/'.beads').rglob('*.lock')] if (t/'.beads').exists() else []
 r['install_state_present']=(t/'.overgate/install-state.json').exists()
 if r['install_state_present']:
  state=json.loads((t/'.overgate/install-state.json').read_bytes());r['install_state_binding']={k:state.get(k) for k in ['format','source_sha','mode','beads']}
 r['memory_files']=[p.name for p in (t/'.memory-bank').glob('*.md')]
 r['project_verify_exists']=(t/'.agents/project/verify.sh').exists()
 if r['project_verify_exists']:r['project_verify_text']=(t/'.agents/project/verify.sh').read_text(encoding='utf-8')
 p=run(['gh','api','repos/'+c['repo']+'/branches/main/protection'],t,label=n+'-resume-protection',ok=False)
 try:r['protection']=json.loads(p.stdout)
 except ValueError:r['protection']={'exit_code':p.returncode}
 result.append(r)
(E/'resume-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{k:r.get(k) for k in ['name','head','branch','status','git_locks','beads_lock_paths','install_state_binding','memory_files','project_verify_text']} for r in result],ensure_ascii=True,indent=2))
