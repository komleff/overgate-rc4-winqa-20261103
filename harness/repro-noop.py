import sys,json
from pathlib import Path
from prepare import E,S,SHA,run
c=next(c for c in json.loads((E/'targets.json').read_text(encoding='utf-8')) if c['name']=='simple-rollback');t=Path(c['target'])
old=set((t/'.overgate-backups').glob('*/rollback.json'))
run([sys.executable,S/'scripts/install-overgate.py','apply','--plan',c['plan'],'--approval',E/'simple-rollback-approval.json'],label='noop-minimal-fresh-apply')
new=set((t/'.overgate-backups').glob('*/rollback.json'))-old;assert len(new)==1
run([sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',t,'--contract',c['contract'],'--target-pr',c['pr'],'--output',E/'noop-minimal-fresh-plan.json'],label='noop-minimal-fresh-plan')
x=json.loads((E/'noop-minimal-fresh-plan.json').read_bytes());m=[v for v in x['operations'] if v['before']!=v['after']]
r={'source_sha':SHA,'target':str(t),'target_sha':run(['git','rev-parse','HEAD'],t).stdout.strip(),'stage':'immediately after approved fresh apply; before helpers, Git stage/commit or project edits','conflicts':x['conflicts'],'operation_count':len(x['operations']),'mismatch_count':len(m),'hash_mismatches':sum(v['before']['sha256']!=v['after']['sha256'] for v in m),'mode_pairs':sorted({(v['before']['mode'],v['after']['mode']) for v in m}),'no_op_pass':not m}
run([sys.executable,S/'scripts/install-overgate.py','rollback','--target',t,'--backup',next(iter(new))],label='noop-minimal-rollback')
(E/'noop-minimal-results.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r))
