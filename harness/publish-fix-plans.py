from pathlib import Path
import json,shutil,sys,hashlib
from prepare import B,E,S,run
R=B/'evidence-repo';cases=json.loads((E/'fix-targets.json').read_text(encoding='utf-8'))
for c in cases:
 for key in ['plan','contract']:
  p=Path(c[key]);shutil.copyfile(p,R/'plans'/p.name)
run(['git','add','plans'],R);run(['git','commit','-q','-m','docs: publish exact2343 affected install plans'],R);run(['git','push','origin','qa/evidence'],R);sha=run(['git','rev-parse','HEAD'],R).stdout.strip();(E/'fix-plan-evidence-sha.txt').write_text(sha,encoding='utf-8')
for c in cases:
 h=hashlib.sha256(Path(c['plan']).read_bytes()).hexdigest();body='## Affected WB-01 exact inventory before apply\n\nSource2343df83a3a26ae83bc66d4009dd67a913eeea4e, target '+c['target']+'. Kind '+c['kind']+'.\n\n[Exact plan JSON](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+c['name']+'-plan.json); SHA256 `'+h+'`. [Contract](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+c['name']+'-contract.md). Independent same-session target review pending; no apply yet.\n\n— Windows-QA (Codex GPT-6)\n'
 print(c['name'],run([sys.executable,S/'.claude/tools/publish-pr-comment.py',c['pr'].rsplit('/',1)[1],'-'],c['target'],label=c['name']+'-inventory-publish',input=body).stdout.strip(),flush=True)
