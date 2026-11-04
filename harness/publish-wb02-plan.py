import json, hashlib, shutil, sys
from prepare import B,E,run
from pathlib import Path

c=json.loads((E/'wb02-fix-simple-auto-target.json').read_text())
R=B/'evidence-repo'
assert not run(['git','status','--porcelain'],R).stdout
assert hashlib.sha256(Path(c['plan']).read_bytes()).hexdigest()==c['plan_sha256']
for key in ['plan','contract']:
    p=Path(c[key]); shutil.copyfile(p,R/'plans'/p.name)
run(['git','add','plans/wb02-fix-simple-auto-plan.json','plans/wb02-fix-simple-auto-contract.md'],R)
run(['git','diff','--cached','--check'],R)
run(['git','commit','-m','docs: publish exact WB-02 affected Windows inventory'],R)
run(['git','push','origin','qa/evidence'],R)
sha=run(['git','rev-parse','HEAD'],R).stdout.strip()
(E/'wb02-plan-evidence-sha.txt').write_text(sha,encoding='utf-8')
body='## Exact WB-02 affected inventory before apply\n\nSource `'+c['source_sha']+'`; new README-only simple/auto target; planning HEAD `'+c['before_head']+'`. [Exact inventory](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/wb02-fix-simple-auto-plan.json), SHA256 `'+c['plan_sha256']+'`; [contract](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/wb02-fix-simple-auto-contract.md). 78 operations; all before null, state_before null, conflicts0. No apply/helpers yet. Independent same-session install review follows. Historical verifier SHA clarification is pending [PM question](https://github.com/komleff/overgate/pull/12#issuecomment-6628325201); dependent execution waits for PM.\n\n— Windows QA / Codex GPT-6\n'
url=run([sys.executable,Path(c['source'])/'.claude/tools/publish-pr-comment.py','1','-'],c['target'],label='wb02-inventory-publish',input=body).stdout.strip()
(E/'wb02-inventory-url.txt').write_text(url,encoding='utf-8')
print(json.dumps({'evidence_sha':sha,'inventory_url':url}))
