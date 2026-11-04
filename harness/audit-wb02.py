import sys,json,hashlib,subprocess,difflib
from pathlib import Path
from prepare import B,E,run
c=json.loads((E/'wb02-fix-simple-auto-target.json').read_text())
S=Path(c['source']); T=Path(c['target']); SHA=c['source_sha']; NAME=c['name']
old='2343df83a3a26ae83bc66d4009dd67a913eeea4e'
template=E/'literal-b-simple-auto-project-verify-template.sh'
def sha(data): return hashlib.sha256(data).hexdigest()
def capture(stage):
    data=(T/'.agents/project/verify.sh').read_bytes(); original=template.read_bytes()
    expected=original if stage=='copy' else original.replace(old.encode(),SHA.encode())
    assert data==expected
    (E/(NAME+'-verifier-'+stage+'.sh')).write_bytes(data)
    r={'source_sha':SHA,'stage':stage,'template_sha256':sha(original),'target_sha256':sha(data),'exact_expected_bytes':True,'target_file':str(T/'.agents/project/verify.sh'),'pm_permission':'https://github.com/komleff/overgate/pull/12#issuecomment-6628354758'}
    if stage=='bound':
        r['diff']=''.join(difflib.unified_diff(original.decode().splitlines(True),data.decode().splitlines(True),fromfile='historical-template',tofile='new-target-verifier'))
        r['reason']='PM-approved project-owned fixture source SHA binding after exact actual cp; original external template unchanged.'
    (E/(NAME+'-verifier-'+stage+'.json')).write_text(json.dumps(r,indent=2),encoding='utf-8',newline='\n')
    print(json.dumps(r));return 0
def audit(stage):
    checks={};r={'source_sha':SHA,'stage':stage,'target':str(T),'repo':c['repo']}
    state=json.loads((T/'.overgate/install-state.json').read_bytes())
    checks['exact_source_auto_beads']=state.get('source_sha')==SHA and state.get('mode')=='auto' and state.get('beads') is True
    checks['default_mode_auto']=json.loads((T/'.claude/settings.json').read_bytes())['permissions']['defaultMode']=='auto'
    checks['memory_six_exact']=len(list((T/'.memory-bank').glob('*.md')))==6 and all((T/'.memory-bank'/p.name).read_bytes()==p.read_bytes() for p in (T/'.agents/templates/memory-bank').glob('*.md'))
    checks['project_verify']=run(['C:/Program Files/Git/bin/bash.exe','.agents/project/verify.sh'],T,label=NAME+'-'+stage+'-verify',ok=False).returncode==0
    checks['checker']=run([sys.executable,S/'scripts/check-reference.py','--root',T],label=NAME+'-'+stage+'-checker',ok=False).returncode==0
    np=E/(NAME+'-'+stage+'-noop-plan.json')
    p=run([sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',T,'--contract',c['contract'],'--target-pr',c['pr'],'--output',np],label=NAME+'-'+stage+'-noop',ok=False)
    v=json.loads(np.read_bytes()) if p.returncode==0 else None
    checks['noop']=v is not None and not v['conflicts'] and all(x['before']==x['after'] for x in v['operations']);r['noop_operations']=len(v['operations']) if v else None
    hook='.claude/hooks/commit_command_classifier.py'
    blob=subprocess.run(['git','show',SHA+':'+hook],cwd=S,capture_output=True,check=True).stdout
    h=(T/hook);r['changed_hook']={'git_blob':run(['git','rev-parse',SHA+':'+hook],S).stdout.strip(),'source_sha256':sha(blob),'installed_sha256':sha(h.read_bytes()),'observed_mode':oct(h.stat().st_mode&0o777)}
    checks['installed_fix_hook']=h.read_bytes()==blob and h.stat().st_mode&0o777==0o666
    refs=run(['git','ls-remote','--heads','origin'],T,label=NAME+'-'+stage+'-refs').stdout
    refs={x.split()[1]:x.split()[0] for x in refs.splitlines()};r['refs']=refs
    ready=run(['bd','--sandbox','ready','--json'],T,label=NAME+'-'+stage+'-bd-ready',ok=False)
    checks['bd_ready']=ready.returncode==0 and isinstance(json.loads(ready.stdout),list)
    checks['embedded_db']=json.loads((T/'.beads/metadata.json').read_bytes()).get('dolt_mode')=='embedded'
    checks['beads_backup']=bool(refs.get('refs/heads/beads-backup'))
    prot=json.loads(run(['gh','api','repos/'+c['repo']+'/branches/main/protection'],T,label=NAME+'-'+stage+'-protection').stdout)
    checks['protection']=prot['enforce_admins']['enabled'] is True and prot.get('required_pull_request_reviews') is not None and prot['allow_force_pushes']['enabled'] is False and prot['allow_deletions']['enabled'] is False
    r['head']=run(['git','rev-parse','HEAD'],T).stdout.strip();r['branch']=run(['git','branch','--show-current'],T).stdout.strip();checks['working_branch']=r['branch']==c['branch']
    if stage=='final':
        checks['clean']=not run(['git','status','--porcelain'],T,label=NAME+'-final-status').stdout
        checks['index_empty']=not run(['git','diff','--cached','--name-status'],T,label=NAME+'-final-index').stdout
        checks['remote_head']=refs.get('refs/heads/'+c['branch'])==r['head']
        pr=json.loads(run(['gh','pr','view','1','--json','isDraft,state,headRefOid,url'],T,label=NAME+'-final-pr').stdout);r['pr']=pr
        checks['draft_pr_head']=pr['isDraft'] and pr['state']=='OPEN' and pr['headRefOid']==r['head']
    r['checks']=checks;r['result']='PASS' if all(checks.values()) else 'FAIL'
    (E/(NAME+'-'+stage+'-audit.json')).write_text(json.dumps(r,indent=2),encoding='utf-8',newline='\n')
    print(json.dumps(r));return 0 if r['result']=='PASS' else 1
if __name__=='__main__':
    stage=sys.argv[1]
    sys.exit(capture(stage) if stage in {'copy','bound'} else audit(stage))
