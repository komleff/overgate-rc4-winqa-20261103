import json,hashlib,shutil
from prepare import B,E,run
R=B/'evidence-repo'; name='literal-b-wb02-fix-install'
raw=E/(name+'.jsonl'); events=[]
for line in raw.read_text(encoding='utf-8').splitlines():
    x=json.loads(line)
    if x.get('type')=='system' and x.get('subtype')=='init':
        events.append({k:x.get(k) for k in ['type','subtype','cwd','session_id','model','permissionMode','claude_code_version']})
    elif x.get('type')=='assistant':
        events.extend({'type':'tool_use','id':v.get('id'),'name':v.get('name'),'input':v.get('input')} for v in x.get('message',{}).get('content',[]) if v.get('type')=='tool_use')
    elif x.get('type')=='user':
        events.extend(v for v in x.get('message',{}).get('content',[]) if isinstance(v,dict) and v.get('type')=='tool_result')
out=E/(name+'-receipts.json')
out.write_text(json.dumps({'source_sha':'ac58c9689d921cc859661e4cb7eb37a5b67c5abe','raw_local_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'notice':'Exact runtime init and raw tool inputs/outputs only. Local original preserved; internal reasoning excluded. QA preflight command returned2 before apply; product candidate not exercised.','events':events},ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
report='''# WB-02 affected Windows QA: pre-apply attempt

Role/model: Windows QA / Codex GPT-6. Source: ac58c9689d921cc859661e4cb7eb37a5b67c5abe. Target planning HEAD:6645603156c47e9211e1a262862fcd09edb35633; C:/work/og-wb02-auto, test PR1. PM packet6622330220, command clarification6622338482, verifier permission6628354758.

| case | AC | method | result | evidence |
|---|---|---|---|---|
| Frozen clean source, new target and exact inventory | AC13 / section5.4.1 | Native readback + independent same-session review | PASS | wb02-preflight.json; plan, contract, target review6628414360 |
| QA worker preflight command | QA infrastructure | Actual Claude auto Bash lists intentionally absent directories; ls exits2; wrapper stops | FAIL | literal-b-wb02-fix-install-receipts.json; invocation exit1 |
| First apply / helpers / literal cp | AC05/AC13/R6 / section5.4.2 | Actual runtime | NOT RUN | No apply or helper tool call; no install-state; target clean |
| Hook startup and workflow/negative controls/no-op | section5.4.3–6 | Actual runtime and installed-hook input | NOT RUN | Dependent on first apply |
| unavailable-auto account | R1 | Actual unavailable account | NOT RUN | Account unavailable; this is not an OAuth/auto refusal |
| Other five historical variants | Historical source2343 only | No rerun authorized | NOT RUN on new SHA | Historical five PASS remain separately bound to2343 |

No new product FAIL or acceptance is inferred from the QA preflight failure. No source/managed files changed, no apply/helpers/retries, merge/release/finalize. QA wrapper stopped its own process tree. PM continuation question6628475422: allow same unchanged target/exact inventory and successful native existence assertion before first apply, or require another target. Initial failed attempt retained regardless of continuation.
'''
(E/'wb02-preapply-attempt-report.md').write_text(report,encoding='utf-8',newline='\n')
for p in [out,E/(name+'-invocation.json'),E/(name+'.stderr.txt'),E/'wb02-preapply-attempt-report.md',E/'wb02-fix-simple-auto-approval.json']:
    shutil.copyfile(p,R/'receipts'/p.name)
for filename in ['audit-wb02.py','wb02-install-prompt.txt','publish-wb02-attempt.py']:
    shutil.copyfile(B/filename,R/'harness'/filename)
index={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['plans','receipts','harness'] for p in (R/folder).rglob('*') if p.is_file()}
(R/'SHA256SUMS.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
run(['git','add','receipts','harness','SHA256SUMS.json'],R)
run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],R)
run(['git','commit','-m','docs: preserve stopped WB-02 pre-apply QA attempt'],R)
run(['git','push','origin','qa/evidence'],R)
sha=run(['git','rev-parse','HEAD'],R).stdout.strip()
(E/'wb02-preapply-evidence-sha.txt').write_text(sha,encoding='utf-8')
print(sha)
