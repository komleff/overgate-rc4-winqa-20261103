import sys, json, hashlib, subprocess
from pathlib import Path
from prepare import B,E,run
c=json.loads((E/'wb02-fix-simple-auto-target.json').read_text())
s=Path(c['source']); t=Path(c['target'])
template=E/'literal-b-simple-auto-project-verify-template.sh'
historical=template.read_bytes()
published=subprocess.run(['git','cat-file','-e','66c8d88a467cf3a3f958b424d8c644ee1c00e8ec:receipts/'+template.name],cwd=B/'evidence-repo',capture_output=True).returncode==0
hook='.claude/hooks/commit_command_classifier.py'
blob=subprocess.run(['git','show',c['source_sha']+':'+hook],cwd=s,capture_output=True,check=True).stdout
versions={}
for name,args in {'git':['git','--version'],'bash':['C:/Program Files/Git/bin/bash.exe','--version'],'python':[sys.executable,'--version'],'bd':['bd','--version'],'claude':[str(B/'tools/claude-runtime/node_modules/.bin/claude.cmd'),'--version']}.items():
    p=run(args,label='wb02-version-'+name); versions[name]=p.stdout.strip().splitlines()[0]
result={'source_sha':c['source_sha'],'source_clean':not run(['git','status','--porcelain'],s).stdout,'target_sha':run(['git','rev-parse','HEAD'],t).stdout.strip(),'target_clean':not run(['git','status','--porcelain'],t).stdout,'managed_state_absent':not(t/'.overgate/install-state.json').exists(),'template_sha256':hashlib.sha256(historical).hexdigest(),'template_in_prior_bundle':published,'template_old_sha_assertion':next(x for x in historical.decode().splitlines() if 'source_sha' in x),'source_hook_git_blob':run(['git','rev-parse',c['source_sha']+':'+hook],s).stdout.strip(),'source_hook_sha256':hashlib.sha256(blob).hexdigest(),'versions':versions,'execution_status':'NOT RUN: awaiting PM template assertion clarification; independent inventory review pending'}
(E/'wb02-preflight.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
