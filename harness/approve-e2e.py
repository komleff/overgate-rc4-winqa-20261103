import sys,json,hashlib,shutil
from pathlib import Path
from prepare import B,E,S,run
R=B/'evidence-repo'
for n in ['e2e-simple-auto','e2e-complex-auto']:
 for ext in ['plan.json','contract.md']:
  p=E/(n+'-'+ext);shutil.copyfile(p,R/'plans'/p.name)
run(['git','add','plans'],R);run(['git','commit','-q','-m','docs: publish exact literal E2E plans before apply'],R);run(['git','push','origin','qa/evidence'],R)
sha=run(['git','rev-parse','HEAD'],R).stdout.strip()
for n in ['e2e-simple-auto','e2e-complex-auto']:
 p=E/(n+'-plan.json');v=json.loads(p.read_bytes());h=hashlib.sha256(p.read_bytes()).hexdigest();url=v['target_pr'];t=Path(v['target'])
 body='## Exact plan and PLAN_REVIEW before apply\n\n[Exact inventory](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+sha+'/plans/'+n+'-plan.json). SHA256 `'+h+'`.\n\nIndependent Reviewer / Codex GPT-6 (exact preset unavailable), same target Reviewer session: **PLAN_READY**, 0 new BLOCKER,0 ADVISORY for this test installation; not source acceptance. Source clean exact403f95b8a7fae50957a99c16a211a8ef7217cb22. Checked new test repo/origin/path/branch/DraftPR/HEAD/contract, 78ops all before null, all after hash+mode independently match frozen Git blobs, default auto/Beads true, closure order; no source fixes.\n\nWB-01 remains FAIL/BLOCKER under source PR12 PM decision6610864301; calling it a warning does not waive AC04. This approval permits testing other components on frozen403. Actual helpers/runtime/export are not certified by this Plan Review. Installer does not self-approve.\n\n— Independent target Reviewer (Codex GPT-6), published by Windows-QA (Codex GPT-6)\n'
 out=run([sys.executable,S/'.claude/tools/publish-pr-comment.py','1','-'],t,label=n+'-review-publish',input=body).stdout.strip();assert out.startswith(url+'#')
 (E/(n+'-approval.json')).write_text(json.dumps({'verdict':'PLAN_READY','plan_sha256':h,'evidence':out},indent=2),encoding='utf-8')
 prompt=B/(n+'-phase-b-prompt.txt');prompt.write_text((B/'e2e-phase-b.txt').read_text(encoding='utf-8').replace('E2E-NAME',n),encoding='utf-8')
 print(n,out,flush=True)
