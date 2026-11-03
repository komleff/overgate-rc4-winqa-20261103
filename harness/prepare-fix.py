import sys,json
from pathlib import Path
from prepare import B,E,run
FIX='2343df83a3a26ae83bc66d4009dd67a913eeea4e';SOURCE=B/'source-2343df8'
def main():
 original=json.loads((E/'targets.json').read_text(encoding='utf-8'));e2e=json.loads((E/'e2e-targets.json').read_text(encoding='utf-8'));cases=[]
 for pathclass in ['simple','complex']:
  c=next(x for x in original if x['name']==pathclass+'-rollback');cases.append({'name':'fix-'+pathclass+'-fresh','target':c['target'],'pr':c['pr'],'kind':'fresh'})
  c=next(x for x in e2e if x['name']=='e2e-'+pathclass+'-auto');cases.append({'name':'fix-'+pathclass+'-upgrade','target':c['target'],'pr':'https://github.com/'+c['repo']+'/pull/1','kind':'upgrade'})
 for c in cases:
  t=Path(c['target']);c['source']=str(SOURCE);c['source_sha']=FIX;c['before_head']=run(['git','rev-parse','HEAD'],t).stdout.strip()
  vc=('Affected Windows WB-01 QA. Source '+FIX+' clean Git checkout. Target '+str(t)+' branch '+run(['git','branch','--show-current'],t).stdout.strip()+'.\n'
      'Operator retains product authority. Existing source403 FAIL is not erased. No merge/release/finalize or working checkout changes.\n'
      'Runtime/controller delta: Windows observable-mode normalization changes the managed scripts/install-overgate.py payload. Upgrade must replace that exact source file; remaining payload paths and guards are unaffected. No whole-payload equivalence is claimed across the fix.\n'
      'Require approved '+c['kind']+' apply, immediately re-plan => every operation.before==after, conflicts0, state source_sha exact2343, mode auto, beads is True; preserve bytes/conflict checks.\n'
      +('Fresh in previously rolled-back disposable fixture, no helpers/project edits. Negative changed-byte conflict must refuse without target writes; stale original plan apply must refuse before backup/write; restore any controlled bytes exactly, then immediate rollback must restore all before bytes and absent state.\n' if c['kind']=='fresh' else
        'Legitimate upgrade of interrupted403 E2E target with existing embedded Beads/Memory/backup/protection. No bd init, bootstrap, protection reset, backup overwrite or helper replay. Preserve existing database/context/custom project verifier and uncommitted payload. After approved upgrade, actual Claude auto completes exact source/mode/beads project verification, checks ready/remote/protection, commits/pushes branch in existing Draft PR.\n'))
  cp=E/(c['name']+'-contract.md');cp.write_text(vc,encoding='utf-8',newline='\n');c['contract']=str(cp);plan=E/(c['name']+'-plan.json');c['plan']=str(plan)
  p=run([sys.executable,SOURCE/'scripts/install-overgate.py','plan','--source',SOURCE,'--source-sha',FIX,'--target',t,'--contract',cp,'--target-pr',c['pr'],'--output',plan],label=c['name']+'-plan',ok=False)
  c['plan_exit']=p.returncode
  if p.returncode:raise RuntimeError('Plan failed: '+c['name'])
  v=json.loads(plan.read_bytes());assert not v['conflicts'];c['operation_count']=len(v['operations'])
  print(c['name'],len(v['operations']),'non-noop',sum(x['before']!=x['after'] for x in v['operations']),flush=True)
 (E/'fix-targets.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
