import sys,json
from prepare import E,S,run
cs=json.loads((E/'targets.json').read_text(encoding='utf-8'))
for c in cs:
 body=('## PLAN_REVIEW — independent target installation\n\nRole/model: independent Reviewer / Codex GPT-6; exact preset unavailable. Root publishes the returned verdict without changing meaning.\n\nVerdict: **PLAN_READY**. BLOCKER 0, ADVISORY 0.\nSource `'+c['source_sha']+'`; exact plan SHA256 `'+c['plan_sha256']+'`.\n\nReviewer checked all eight disposable plans: source/target/branch/PR/HEAD/contract bindings, no conflicts, all before states absent, state_before null, managed-path safety/order, every after SHA256 and Git mode against frozen blobs. 78 operations for auto/bypass/rollback; 69 for no-beads. Bypass differs only by defaultMode; no-beads excludes Beads payload and both AGENTS template blocks. Rollback is immediate before helpers/edits.\n\nFull immutable plan link was published above before this approval. Not tested by Reviewer: apply, helpers, runtime activation, guards, server rejection, rollback execution. Shared beads-backup later no-op is not a separate first export. This is target-install review, not another source Code Review PR12.\n\n— Independent Reviewer (Codex GPT-6), published by PM/QA (Codex GPT-6)\n')
 p=run([sys.executable,S/'.claude/tools/publish-pr-comment.py',c['pr'].rsplit('/',1)[1],'-'],c['target'],label=c['name']+'-review-publish',input=body)
 url=p.stdout.strip().splitlines()[-1]
 assert url.startswith(c['pr']+'#')
 (E/(c['name']+'-approval.json')).write_text(json.dumps({'verdict':'PLAN_READY','plan_sha256':c['plan_sha256'],'evidence':url},indent=2),encoding='utf-8')
 print(c['name'],url,flush=True)
