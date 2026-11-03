import sys,json,hashlib
from pathlib import Path
from prepare import B,E,run
FIX='2343df83a3a26ae83bc66d4009dd67a913eeea4e';SOURCE=B/'source-2343df8'
def current(p):
 return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':p.stat().st_mode&0o777} if p.is_file() else None
def makeplan(c,label):
 output=E/(c['name']+'-'+label+'-plan.json')
 p=run([sys.executable,SOURCE/'scripts/install-overgate.py','plan','--source',SOURCE,'--source-sha',FIX,'--target',c['target'],'--contract',c['contract'],'--target-pr',c['pr'],'--output',output],label=c['name']+'-'+label,ok=False)
 return p,json.loads(output.read_bytes()) if output.exists() else None
def main():
 for c in json.loads((E/'fix-targets.json').read_text(encoding='utf-8')):
  if len(sys.argv)>1 and c['name'] not in sys.argv[1:]:continue
  n=c['name'];t=Path(c['target']);plan=json.loads(Path(c['plan']).read_bytes());approval=E/(n+'-approval.json');assert approval.exists()
  tracked=[x['target'] for x in plan['operations']]+['.overgate/install-state.json']
  def snapshot():return {p:current(t/p) for p in tracked}
  before=snapshot();old_backups=set((t/'.overgate-backups').glob('*/rollback.json'));r={'name':n,'source_sha':FIX,'target':str(t),'target_pr':c['pr'],'target_before_head':run(['git','rev-parse','HEAD'],t).stdout.strip(),'kind':c['kind']}
  p=run([sys.executable,SOURCE/'scripts/install-overgate.py','apply','--plan',c['plan'],'--approval',approval],label=n+'-apply',ok=False);r['apply_rc']=p.returncode
  if p.returncode:raise RuntimeError(n+' apply failed')
  new_backups=set((t/'.overgate-backups').glob('*/rollback.json'))-old_backups;assert len(new_backups)==1
  r['applied_operations_exact']=all(current(t/op['target'])==op['after'] for op in plan['operations'])
  p,replan=makeplan(c,'immediate-replan');r['noop_rc']=p.returncode;r['noop_conflicts']=replan['conflicts'];r['noop_operation_count']=len(replan['operations']);r['noop_mismatches']=[x['target'] for x in replan['operations'] if x['before']!=x['after']];r['noop_pass']=p.returncode==0 and not replan['conflicts'] and not r['noop_mismatches']
  state=json.loads((t/'.overgate/install-state.json').read_bytes());r['install_state']={k:state.get(k) for k in ['format','source_sha','mode','beads']}
  if c['kind']=='fresh':
   stable=snapshot();backup_count=len(list((t/'.overgate-backups').glob('*/rollback.json')))
   p=run([sys.executable,SOURCE/'scripts/install-overgate.py','apply','--plan',c['plan'],'--approval',approval],label=n+'-stale-apply',ok=False)
   r['stale_plan_rejected']=p.returncode!=0;r['stale_apply_rc']=p.returncode;r['stale_no_target_writes']=snapshot()==stable and backup_count==len(list((t/'.overgate-backups').glob('*/rollback.json')))
   controlled=t/'.agents/PIPELINE_ADR.md';saved=controlled.read_bytes();controlled.write_bytes(saved+b'\nQA controlled changed-byte conflict probe\n')
   changed=snapshot();p,changed_plan=makeplan(c,'changed-bytes');r['controlled_managed_path']='.agents/PIPELINE_ADR.md';r['changed_byte_plan_rc']=p.returncode;r['changed_byte_conflicts']=changed_plan['conflicts'] if changed_plan else [];r['changed_bytes_rejected']=changed_plan is not None and any('.agents/PIPELINE_ADR.md' in str(x) for x in r['changed_byte_conflicts']);r['conflict_no_target_writes']=snapshot()==changed
   controlled.write_bytes(saved)
   r['controlled_file_restored']=snapshot()==stable
   p=run([sys.executable,SOURCE/'scripts/install-overgate.py','rollback','--target',t,'--backup',next(iter(new_backups))],label=n+'-rollback',ok=False);r['rollback_rc']=p.returncode;r['rollback_exact_before_bytes_modes']=snapshot()==before
  else:
   r['checker_rc']=run([sys.executable,SOURCE/'scripts/check-reference.py','--root',t],label=n+'-checker',ok=False).returncode
   r['db_helpers_replayed']=False
  r['target_after_head']=run(['git','rev-parse','HEAD'],t).stdout.strip()
  run(['git','status','--short'],t,label=n+'-status')
  (E/(n+'-results.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps({k:v for k,v in r.items() if k not in ['changed_byte_conflicts']},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
