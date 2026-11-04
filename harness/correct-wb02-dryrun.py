import json,sys,shutil
from pathlib import Path
from prepare import B,E,run
c=json.loads((E/'wb02-fix-simple-auto-target.json').read_text());T=Path(c['target']);N=c['name']
old=json.loads((E/(N+'-dry-controls.json')).read_text(encoding='utf-8'))
assert old['checks'][0]['result']=='PASS' and old['checks'][1]['classification']=='commit'
assert not (T/'README.md').read_bytes()
assert run(['git','rev-parse','HEAD'],T).stdout.strip()==old['head_before']
for suffix in ['dry-controls.json','nested-commit-gate-dryrun.txt','nested-commit-gate-dryrun-input.json']:
    p=E/(N+'-'+suffix);shutil.copyfile(p,E/(N+'-qa-windows-path-attempt1-'+suffix))
command=old['checks'][1]['command'];payload=json.dumps({'tool_name':'Bash','tool_input':{'command':command},'cwd':str(T)})
p=run(['C:/Program Files/Git/bin/bash.exe','.claude/hooks/check-tests-before-commit.sh'],T,label=N+'-nested-commit-gate-canonical-dryrun',ok=False,input=payload)
r={'command':command,'hook':'.claude/hooks/check-tests-before-commit.sh','invocation':'bash .claude/hooks/check-tests-before-commit.sh (relative POSIX path, cwd target)','exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'carrier_executed':False,'classification':'commit','result':'PASS' if p.returncode==2 and 'README absent or empty' in p.stdout+p.stderr else 'FAIL'}
old['checks'][1]=r;old['qa_harness_correction']='Initial native Python passed a Windows backslash script pathname to bash; dirname of BASH_SOURCE resolved wrong launcher path. Corrected only harness argv to canonical relative POSIX hook path. Initial raw refusal preserved separately; installed payload unchanged and carrier never executed.'
old['result']='PASS' if all(x['result']=='PASS' for x in old['checks']) else 'FAIL'
(E/(N+'-dry-controls.json')).write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
print(json.dumps(old));sys.exit(0 if old['result']=='PASS' else 1)
