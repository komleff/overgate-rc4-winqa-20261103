import os,sys,json,hashlib,re,base64
from pathlib import Path
from prepare import B,E,S,SHA,REPO,run
BASH='C:/Program Files/Git/bin/bash.exe'
def save(c,result):
 (E/(c['name']+'-native-results.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
def hook(t,name,command):
 payload=json.dumps({'tool_name':'Bash','tool_input':{'command':command},'cwd':str(t)},ensure_ascii=False)
 return run([BASH,'.claude/hooks/pre-bash.sh'],t,label=name,ok=False,input=payload)
def main():
 for c in json.loads((E/'targets.json').read_text(encoding='utf-8')):
  name=c['name']; t=Path(c['target']); plan=json.loads(Path(c['plan']).read_bytes())
  if not (E/(name+'-approval.json')).exists():raise RuntimeError('No independent approval: '+name)
  result={'source_sha':SHA,'name':name,'target':str(t),'branch':plan['branch'],'pr':c['pr'],'target_before_sha':c['target_before_sha']}
  before={op['target']:(t/op['target']).read_bytes() if (t/op['target']).is_file() else None for op in plan['operations']}
  before['.overgate/install-state.json']=(t/'.overgate/install-state.json').read_bytes() if (t/'.overgate/install-state.json').exists() else None
  p=run([sys.executable,S/'scripts/install-overgate.py','apply','--plan',c['plan'],'--approval',E/(name+'-approval.json')],label=name+'-apply',ok=False)
  result['apply_rc']=p.returncode
  if p.returncode:save(c,result);continue
  result['operation_bytes_match']=all(hashlib.sha256((t/op['target']).read_bytes()).hexdigest()==op['after']['sha256'] for op in plan['operations'])
  backups=list((t/'.overgate-backups').glob('*/rollback.json'));assert len(backups)==1
  state=json.loads((t/'.overgate/install-state.json').read_bytes());result['install_state']=state
  if c['mode']=='rollback':
   p=run([sys.executable,S/'scripts/install-overgate.py','rollback','--target',t,'--backup',backups[0]],label=name+'-rollback',ok=False)
   result['rollback_rc']=p.returncode
   result['restored_before_bytes']=all(((t/path).read_bytes() if (t/path).is_file() else None)==data for path,data in before.items())
   result['install_state_absent']=not (t/'.overgate/install-state.json').exists()
   result['target_after_sha']=run(['git','rev-parse','HEAD'],t).stdout.strip()
   run(['git','status','--short'],t,label=name+'-rollback-status')
   save(c,result);print(name,'rollback',result['restored_before_bytes'],flush=True);continue
  result['checker_rc']=run([sys.executable,S/'scripts/check-reference.py','--root',t],label=name+'-checker',ok=False).returncode
  result['memory_rc']=run([BASH,'scripts/og-init-memory-bank.sh'],t,label=name+'-memory',ok=False).returncode
  templates=list((t/'.agents/templates/memory-bank').glob('*.md'))
  result['memory_six_exact']=len(templates)==6 and all((t/'.memory-bank'/p.name).read_bytes()==p.read_bytes() for p in templates)
  if c['mode']=='no-beads':
   result['beads_rc']='SKIPPED --no-beads'
   manifest=json.loads((S/'.agents/distribution-manifest.json').read_bytes())
   result['beads_component_absent']=all(not (t/x['target']).exists() for x in manifest['files'] if x.get('component')=='beads')
   result['beads_db_absent']=not (t/'.beads').exists()
  else:
   result['beads_rc']=run([BASH,'scripts/bd-bootstrap.sh'],t,label=name+'-beads',ok=False).returncode
   if result['beads_rc']==0:
    run(['bd','--sandbox','ready','--json'],t,label=name+'-bd-ready')
    run(['git','ls-remote','--heads','origin','beads-backup'],t,label=name+'-beads-backup')
  if result['beads_rc'] in (0,'SKIPPED --no-beads'):
   result['protection_rc']=run([BASH,'scripts/og-protect-main.sh'],t,label=name+'-protection',ok=False).returncode
  else: result['protection_rc']='NOT RUN: prior Beads helper failed; installer sequence stops'
  # Project test of actual demo content, distinct from structural OverGate checks.
  verify=t/'.agents/project/verify.sh'
  verify.write_text('#!/usr/bin/env bash\nset -euo pipefail\npy -3 -c "from pathlib import Path; p=Path(\'README.md\'); assert p.is_file() and p.read_text(encoding=\'utf-8\').strip(); print(\'demo README check PASS\')"\n',encoding='utf-8',newline='\n')
  result['project_verify_rc']=run([BASH,'.agents/project/verify.sh'],t,label=name+'-project-verify',ok=False).returncode
  result['hook_results']={}
  for label,command in [('main-push','git push origin main'),('merge','gh pr merge 1'),('readiness','gh pr comment 1 --body "ready to merge"')]:
   p=hook(t,name+'-hook-'+label,command)
   result['hook_results'][label]=p.returncode
  good=verify.read_bytes();verify.write_text('#!/usr/bin/env bash\necho "QA intentional red verification" >&2\nexit 1\n',encoding='utf-8',newline='\n')
  result['red_project_verify_rc']=run([BASH,'.agents/project/verify.sh'],t,label=name+'-project-red',ok=False).returncode
  p=hook(t,name+'-hook-red-commit','git commit -m "qa red must be blocked"')
  result['hook_results']['red-commit']=p.returncode
  verify.write_bytes(good)
  # Explicitly run the complete installed hook before each native mutation receipt.
  (t/'qa-live-file.txt').write_text('Real Windows native QA '+name+'\n',encoding='utf-8',newline='\n')
  p=hook(t,name+'-hook-green-commit','git commit -m "test: record isolated Windows QA"')
  result['hook_results']['green-commit']=p.returncode
  if p.returncode==0:
   run(['git','add','.'],t,label=name+'-stage')
   result['native_commit_rc']=run(['git','commit','-m','test: record isolated Windows QA '+name],t,label=name+'-installed-commit',ok=False).returncode
   p=hook(t,name+'-hook-branch-push','git push origin '+plan['branch'])
   result['hook_results']['branch-push']=p.returncode
   if p.returncode==0:result['native_push_rc']=run(['git','push','origin',plan['branch']],t,label=name+'-installed-push',ok=False).returncode
  result['target_after_sha']=run(['git','rev-parse','HEAD'],t).stdout.strip()
  result['actual_mode']=json.loads((t/'.claude/settings.json').read_bytes())['permissions']['defaultMode']
  result['claude_live']='NOT RUN until successful authenticated actual CLI run; native component evidence only'
  run(['git','status','--short'],t,label=name+'-end-status')
  save(c,result)
  print(name,'apply',result['apply_rc'],'checker',result['checker_rc'],'beads',result['beads_rc'],'protect',result['protection_rc'],'hooks',result['hook_results'],flush=True)
if __name__=='__main__':main()
