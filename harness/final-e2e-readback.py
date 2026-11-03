import sys,json,hashlib,re
from pathlib import Path
from prepare import B,E,run
FIX='2343df83a3a26ae83bc66d4009dd67a913eeea4e';S=B/'source-2343df8'
def main():
 out=[]
 for c in json.loads((E/'e2e-targets.json').read_text(encoding='utf-8')):
  n=c['name'];t=Path(c['target']);kind='simple' if 'simple' in n else 'complex';contract=E/('fix-'+kind+'-upgrade-contract.md');pr='https://github.com/'+c['repo']+'/pull/1';r={'source_sha':FIX,'target':str(t),'repo':c['repo'],'pr':pr}
  r['head']=run(['git','rev-parse','HEAD'],t,label=n+'-final-head').stdout.strip();r['branch']=run(['git','branch','--show-current'],t).stdout.strip();status=run(['git','status','--porcelain'],t,label=n+'-final-status');r['clean']=status.returncode==0 and not status.stdout
  index=run(['git','diff','--cached','--name-status'],t,label=n+'-final-index');r['index_empty']=index.returncode==0 and not index.stdout
  refs=run(['git','ls-remote','--heads','origin'],t,label=n+'-final-remote-refs').stdout;refs={line.split()[1]:line.split()[0] for line in refs.splitlines()};r['remote_head']=refs.get('refs/heads/'+r['branch']);r['branch_published']=r['remote_head']==r['head'];r['backup_sha']=refs.get('refs/heads/beads-backup')
  state=json.loads((t/'.overgate/install-state.json').read_bytes());r['state']={k:state.get(k) for k in ['format','source_sha','mode','beads']};r['strict_state_pass']=state.get('source_sha')==FIX and state.get('mode')=='auto' and state.get('beads') is True
  r['memory_six']=len(list((t/'.memory-bank').glob('*.md')))==6
  r['project_verify_rc']=run(['C:/Program Files/Git/bin/bash.exe','.agents/project/verify.sh'],t,label=n+'-final-project-verify',ok=False).returncode
  r['checker_rc']=run([sys.executable,S/'scripts/check-reference.py','--root',t],label=n+'-final-checker',ok=False).returncode
  plan=E/(n+'-final-noop-plan.json');p=run([sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',FIX,'--target',t,'--contract',contract,'--target-pr',pr,'--output',plan],label=n+'-final-noop',ok=False);v=json.loads(plan.read_bytes()) if p.returncode==0 else None;r['final_noop_pass']=v is not None and not v['conflicts'] and all(x['before']==x['after'] for x in v['operations']);r['noop_operations']=len(v['operations']) if v else None
  prot=json.loads(run(['gh','api','repos/'+c['repo']+'/branches/main/protection'],t,label=n+'-final-protection').stdout);r['protection_pass']=prot['enforce_admins']['enabled'] is True and prot.get('required_pull_request_reviews') is not None and prot['allow_force_pushes']['enabled'] is False and prot['allow_deletions']['enabled'] is False
  doc=json.loads(run(['gh','pr','view','1','--json','url,state,isDraft,headRefOid'],t,label=n+'-final-pr').stdout);r['draft_pr']=doc;r['draft_pr_binding']=doc['isDraft'] is True and doc['headRefOid']==r['head']
  r['result']='PASS' if all([r['clean'],r['index_empty'],r['branch_published'],bool(r['backup_sha']),r['strict_state_pass'],r['memory_six'],r['project_verify_rc']==0,r['checker_rc']==0,r['final_noop_pass'],r['protection_pass'],r['draft_pr_binding']]) else 'FAIL'
  out.append(r);print(json.dumps(r,ensure_ascii=True),flush=True)
 (E/'final-e2e-readback.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
