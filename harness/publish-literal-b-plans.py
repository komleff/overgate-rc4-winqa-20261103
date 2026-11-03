import json,shutil,hashlib,sys
from pathlib import Path
from prepare import B,E,run
S=B/'source-2343df8';R=B/'evidence-repo';cs=json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8'))
for c in cs:
 for key in ['plan','contract']:
  p=Path(c[key]);shutil.copyfile(p,R/'plans'/p.name)
run(['git','add','plans'],R);run(['git','commit','-q','-m','docs: publish six exact fresh B literal inventories'],R);run(['git','push','origin','qa/evidence'],R);sha=run(['git','rev-parse','HEAD'],R).stdout.strip();(E/'literal-b-plan-evidence-sha.txt').write_text(sha,encoding='utf-8')
for c in cs:
 assert hashlib.sha256(Path(c['plan']).read_bytes()).hexdigest()==c['plan_sha256']
 body='## Exact literal fresh B inventory before apply\n\nSource `'+c['source_sha']+'`; fresh '+c['path_class']+' / '+c['mode']+' target. [Exact plan](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+c['name']+'-plan.json), SHA256 `'+c['plan_sha256']+'`; [contract](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+c['name']+'-contract.md). '+str(c['operations'])+' operations, all before null, conflicts0, no install-state. Independent same-session target review before actual Claude apply; no native coordinator apply.\n\n— Windows-QA (Codex GPT-6)\n'
 print(c['name'],run([sys.executable,S/'.claude/tools/publish-pr-comment.py','1','-'],c['target'],label=c['name']+'-inventory-publish',input=body).stdout.strip(),flush=True)
