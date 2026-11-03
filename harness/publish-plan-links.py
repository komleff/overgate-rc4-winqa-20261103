import sys,json,shutil
from prepare import E,S,B,run
R=B/'evidence-repo'
(R/'plans').mkdir(exist_ok=True)
for c in json.loads((E/'targets.json').read_text(encoding='utf-8')):
 for key in ['plan','contract']:
  p=__import__('pathlib').Path(c[key]); shutil.copyfile(p,R/'plans'/p.name)
shutil.copyfile(E/'targets.json',R/'plans/targets.json')
run(['git','add','plans'],R)
run(['git','commit','-m','docs: publish exact Windows QA install plans before review approval'],R,label='evidence-plans-commit')
sha=run(['git','rev-parse','HEAD'],R).stdout.strip()
run(['git','push','-u','origin','qa/evidence'],R,label='evidence-plans-push')
(E/'plans-evidence-sha.txt').write_text(sha,encoding='utf-8')
for c in json.loads((E/'targets.json').read_text(encoding='utf-8')):
 url='https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+c['name']+'-plan.json'
 body='Exact inventory before apply: [plan JSON]('+url+').\n\nSHA256 `'+c['plan_sha256']+'`; source `'+c['source_sha']+'`; conflicts 0. Independent review follows.\n\n— PM/QA (Codex GPT-6)\n'
 p=run([sys.executable,S/'.claude/tools/publish-pr-comment.py',c['pr'].rsplit('/',1)[1],'-'],c['target'],label=c['name']+'-plan-link-publish',input=body)
 print(c['name'],p.stdout.strip(),flush=True)
