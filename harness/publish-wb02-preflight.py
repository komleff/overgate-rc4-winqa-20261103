import json, hashlib, shutil
from prepare import B,E,run
R=B/'evidence-repo'
allowed={'SHA256SUMS.json','receipts/wb02-preflight.json','receipts/literal-b-simple-auto-project-verify-template.sh','receipts/wb02-fix-simple-auto-target.json','receipts/wb02-fix-simple-auto-repo-create.txt','receipts/wb02-fix-simple-auto-created-readback.txt','harness/prepare-wb02.py','harness/publish-wb02-plan.py','harness/inspect-wb02.py','harness/publish-wb02-preflight.py'}
assert all(line[3:] in allowed for line in run(['git','status','--porcelain'],R).stdout.splitlines())
for filename in ['wb02-preflight.json','literal-b-simple-auto-project-verify-template.sh','wb02-fix-simple-auto-target.json','wb02-fix-simple-auto-repo-create.txt','wb02-fix-simple-auto-created-readback.txt']:
    shutil.copyfile(E/filename,R/'receipts'/filename)
for filename in ['prepare-wb02.py','publish-wb02-plan.py','inspect-wb02.py','publish-wb02-preflight.py']:
    shutil.copyfile(B/filename,R/'harness'/filename)
index={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['plans','receipts','harness'] for p in (R/folder).rglob('*') if p.is_file()}
(R/'SHA256SUMS.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
run(['git','add','plans','receipts','harness','SHA256SUMS.json'],R)
run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],R)
run(['git','commit','-m','docs: record WB-02 preflight and unchanged historical verifier'],R)
run(['git','push','origin','qa/evidence'],R)
sha=run(['git','rev-parse','HEAD'],R).stdout.strip()
(E/'wb02-preflight-evidence-sha.txt').write_text(sha,encoding='utf-8')
print(sha)
