import sys, json, hashlib
from pathlib import Path
from prepare import B, E, run

SHA = 'ac58c9689d921cc859661e4cb7eb37a5b67c5abe'
S = B / 'source-ac58c96'
T = Path('C:/work/og-wb02-auto')
NAME = 'wb02-fix-simple-auto'
REPO = 'komleff/overgate-rc4-wb02-auto-20261104'
BRANCH = 'install/wb02-auto'

def main():
    assert run(['git','rev-parse','HEAD'],S).stdout.strip() == SHA
    assert not run(['git','status','--porcelain'],S).stdout
    assert not T.exists(), 'Target must be new'
    changes = run(['git','diff','--name-only','2343df83a3a26ae83bc66d4009dd67a913eeea4e',SHA],S,label=NAME+'-source-diff').stdout.splitlines()
    assert changes == ['.claude/hooks/commit_command_classifier.py','scripts/tests/commit-command-classifier.test.sh','scripts/tests/commit-gate.test.py']
    if '--resume-created' not in sys.argv:
        run(['gh','api','user/repos','--method','POST','--input','-'],label=NAME+'-repo-create',input=json.dumps({'name':REPO.split('/')[1],'description':'Disposable affected WB-02 Windows simple auto QA exact ac58c96','private':False,'auto_init':True}))
    else:
        # POST returned502 after creation; GET proved the new repository exists.
        entries=json.loads(run(['gh','api','repos/'+REPO+'/contents'],label=NAME+'-created-readback').stdout)
        assert [x['name'] for x in entries] == ['README.md']
    run(['git','clone','https://github.com/'+REPO+'.git',T],label=NAME+'-clone')
    run(['git','switch','-c',BRANCH],T,label=NAME+'-branch')
    contract = '''WB-02 affected Windows QA; source ac58c9689d921cc859661e4cb7eb37a5b67c5abe.
Authority: operator. PM packet PR12#6622330220, clarification #6622338482; AC-05/AC-13, R6, affected plan section5.4 only. No source fix by QA.
Target C:/work/og-wb02-auto; komleff/overgate-rc4-wb02-auto-20261104; branch install/wb02-auto. Fresh README-only repository, no managed state/settings/Memory/Beads. Planning document is the only preinstall addition.
Default auto (no mode flag), Beads enabled strict JSON true; actual Claude Code explicit auto. New Draft PR, exact inventory and independent same-session target PLAN_READY published before apply. Actual Claude executes first apply from this source, never coordinator replacement.
Read QUICKSTART phrase literally. Helpers sequentially: og-init-memory-bank, bd-bootstrap with scoped bd1.2.2 and initial remote backup, og-protect-main. No reapply/helper replay or repair on FAIL; stop first unexpected refusal and preserve raw input/output. Codes2/3/4/5 require explicit R8; code6 STOP.
Exact positive Bash command is PM #6622338482 with only cd changed to this target. Historical external verifier template remains immutable. Its source assertion binds old2343; dependent verifier setup waits for explicit PM clarification #6628325201. Never silently label this as product FAIL or waive it.
Require actual cp PreToolUse without permission question, copied bytes/hash identity, project verifier green under agreed source assertion, source checker, file/working-branch commit/push/PR, actual main-push/merge/ready-comment/red-test hook denials; real server-side main update rejected in disposable repository with main unchanged. Never merge/release/finalize.
Additional negative cp gh-pr-merge carrier and nested git-commit control: hook-input/classifier dry-run only, never execute carrier Bash command. Installed changed hook bytes/mode must match source Git blob; record exact target HEAD and final no-op/clean/index/remote/DraftPR readback.
Historical five PASS on2343 remain scoped historical evidence, not new whole-case PASS on this source. R1 unavailable-auto-account NOT RUN if unavailable. No rerun of unrelated modes/paths/rollback/full CI.
'''
    cp = E / (NAME+'-contract.md')
    cp.write_text(contract,encoding='utf-8',newline='\n')
    (T/'qa-install-plan.md').write_text(contract,encoding='utf-8',newline='\n')
    run(['git','add','qa-install-plan.md'],T)
    run(['git','commit','-m','docs: plan affected WB-02 Windows auto QA'],T,label=NAME+'-planning-commit')
    run(['git','push','-u','origin',BRANCH],T,label=NAME+'-planning-push')
    body=E/(NAME+'-pr-body.md')
    body.write_text(contract+'\nWindows QA coordinator: Codex GPT-6; actual installer Claude Code, explicit auto.\n',encoding='utf-8')
    pr=run(['gh','pr','create','--draft','--base','main','--head',BRANCH,'--title','Affected WB-02 Windows simple auto QA ac58c96','--body-file',body],T,label=NAME+'-pr').stdout.strip()
    plan=E/(NAME+'-plan.json')
    run([sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',T,'--contract',cp,'--target-pr',pr,'--output',plan],label=NAME+'-plan')
    v=json.loads(plan.read_bytes())
    assert not v['conflicts'] and v['state_before'] is None and all(x['before'] is None for x in v['operations'])
    c={'name':NAME,'source':str(S),'source_sha':SHA,'target':str(T),'repo':REPO,'branch':BRANCH,'pr':pr,'plan':str(plan),'contract':str(cp),'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'before_head':run(['git','rev-parse','HEAD'],T).stdout.strip(),'operations':len(v['operations'])}
    (E/(NAME+'-target.json')).write_text(json.dumps(c,indent=2),encoding='utf-8')
    print(json.dumps(c),flush=True)

if __name__=='__main__': main()
