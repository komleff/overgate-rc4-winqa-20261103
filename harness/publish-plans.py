import sys,json
from prepare import E,S,run
for c in json.loads((E/'targets.json').read_text(encoding='utf-8')):
 body='## Exact inventory plan before apply\n\nSHA256 `'+c['plan_sha256']+'`\n\n```json\n'+__import__('pathlib').Path(c['plan']).read_text(encoding='utf-8')+'\n```\n\n— PM/QA (Codex GPT-6)\n'
 p=run([sys.executable,S/'.claude/tools/publish-pr-comment.py',c['pr'].rsplit('/',1)[1],'-'],c['target'],label=c['name']+'-full-plan-publish',input=body)
 print(c['name'],p.stdout.strip(),flush=True)
