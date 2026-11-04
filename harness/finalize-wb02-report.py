"""Publish QA evidence/report only. Never invoke OverGate finalize, merge or release."""
import sys,json,hashlib,shutil,re
from pathlib import Path
from prepare import B,E,run
R=B/'evidence-repo'; SHA='ac58c9689d921cc859661e4cb7eb37a5b67c5abe';N='wb02-fix-simple-auto'
def read(name):return json.loads((E/name).read_text(encoding='utf-8'))
def sanitize(name):
    raw=E/(name+'.jsonl');events=[];init=None;calls={};results={};hooks=[]
    for line in raw.read_text(encoding='utf-8').splitlines():
        x=json.loads(line)
        if x.get('type')=='system' and x.get('subtype')=='init':
            init={k:x.get(k) for k in ['type','subtype','cwd','session_id','model','permissionMode','claude_code_version']};events.append(init)
        elif x.get('type')=='system' and x.get('subtype') in {'hook_started','hook_response'}:
            events.append(x);hooks.append(x)
        elif x.get('type')=='assistant':
            for v in x.get('message',{}).get('content',[]):
                if v.get('type')=='tool_use':
                    item={'type':'tool_use','id':v.get('id'),'name':v.get('name'),'input':v.get('input')};events.append(item);calls[v['id']]=item
        elif x.get('type')=='user':
            for v in x.get('message',{}).get('content',[]):
                if isinstance(v,dict) and v.get('type')=='tool_result':
                    item=dict(v);item['permission_metadata']=x.get('tool_result_meta');events.append(item);results[v.get('tool_use_id')]=item
        elif x.get('type')=='result': events.append({k:x.get(k) for k in ['type','subtype','is_error','result','session_id','permission_denials']})
    out={'source_sha':SHA,'raw_local_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'notice':'Original local JSONL preserved. Only runtime init, raw tool inputs/outputs, hook events and final factual response retained; no internal reasoning/OAuth flow.','events':events}
    (E/(name+'-receipts.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    return init,calls,results,hooks

def main():
    c=read(N+'-target.json');audit=read(N+'-final-audit.json');server=read(N+'-server-rejection.json');dry=read(N+'-dry-controls.json')
    assert all(x['result']=='PASS' for x in [audit,server,dry])
    assert read(N+'-red-fixture-restored.json')['target_clean']
    first=sanitize('literal-b-wb02-fix-install')
    live=sanitize('literal-b-wb02-fix-continuation')
    negative=sanitize('wb02-fix-negatives')
    expected=['git push origin main','gh pr merge 1','gh pr comment 1 --body "ready to merge"','git commit -m "qa: red verification must block"']
    probes=[]
    for cmd in expected:
        matches=[(i,v) for i,v in negative[1].items() if v['name']=='Bash' and v['input'].get('command')==cmd]
        assert len(matches)==1
        i,v=matches[0];result=negative[2][i]
        ok=result.get('is_error') is True and 'PreToolUse:Bash hook error' in str(result.get('content'))
        probes.append({'command':cmd,'tool_use_id':i,'result':'PASS' if ok else 'FAIL','raw_output':result.get('content')})
    assert all(x['result']=='PASS' for x in probes)
    assert all(x[0]['permissionMode']=='auto' and x[0]['claude_code_version']=='2.1.317' for x in [live,negative])
    cp='cd C:/work/og-wb02-auto && cp D:/CodexArtifacts/overgate-rc4-winqa-20261103/evidence/literal-b-simple-auto-project-verify-template.sh .agents/project/verify.sh && sha256sum .agents/project/verify.sh D:/CodexArtifacts/overgate-rc4-winqa-20261103/evidence/literal-b-simple-auto-project-verify-template.sh'
    found=[i for i,v in live[1].items() if v['name']=='Bash' and v['input'].get('command')==cp]
    assert len(found)==1 and not live[2][found[0]].get('is_error')
    assert read(N+'-verifier-copy.json')['target_sha256']=='7d92606526ba81f81aa3acae9bd5a264e7a647084abd161848fb9a232e74b28c'
    summary={'source_sha':SHA,'target_head':audit['head'],'actual_runtime':live[0],'fresh_negative_runtime':negative[0],'exact_cp_tool_id':found[0],'exact_cp_result':'PASS','negative_probes':probes,'successful_hook_responses':sum(x.get('subtype')=='hook_response' and x.get('exit_code')==0 for x in live[3]),'negative_hook_responses':sum(x.get('subtype')=='hook_response' and x.get('exit_code')==2 for x in negative[3]),'historical_scope':'Five old2343 variant PASS remain historical; changed classifier prevents whole-case relabel on ac58. R1 NOT RUN.','result':'PASS: affected packet only'}
    assert summary['negative_hook_responses']==4
    (E/'wb02-final-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    source=Path(c['source'])
    assert run(['git','rev-parse','HEAD'],source).stdout.strip()==SHA and not run(['git','status','--porcelain'],source).stdout
    head=run(['gh','pr','view','12','-R','komleff/overgate','--json','headRefOid','--jq','.headRefOid']).stdout.strip();assert head==SHA,'HEAD moved: ask PM before report scope changes'
    versions=read('wb02-preflight.json')['versions']
    for key,args in {'gh':['gh','--version'],'node':['node','--version'],'jq':['jq','--version']}.items():versions[key]=run(args).stdout.splitlines()[0]
    win=run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber | ConvertTo-Json -Compress']).stdout.strip()
    (E/'wb02-final-environment.json').write_text(json.dumps({'windows':json.loads(win),'versions':versions,'runtime':live[0],'negative_runtime':negative[0]},indent=2),encoding='utf-8',newline='\n')
    report=f'''## WINDOWS QA → PM / FINAL AFFECTED QA — WB-02

**Result: PASS for the affected WB-02 packet only.** Overall WI-1 acceptance/readiness is not asserted. Historical WB-02 FAIL on2343 is retained.

Role/model: Windows QA / Codex GPT-6 (exact preset unavailable). Actual installer and fresh negative runtime: Claude Code `{live[0]['claude_code_version']}`, model `{live[0]['model']}`, explicit/effective `auto`. 2026-11-04, Asia/Novosibirsk. Source/PR HEAD `{SHA}`, separate clean clone `D:/CodexArtifacts/overgate-rc4-winqa-20261103/source-ac58c96`. Target `C:/work/og-wb02-auto`, branch `install/wb02-auto`, [Draft test PR1]({c['pr']}), final local=remote=PR HEAD `{audit['head']}`; tree/index clean.

Contract: [PM affected packet](https://github.com/komleff/overgate/pull/12#issuecomment-6622330220), [exact-command/dry-run clarification](https://github.com/komleff/overgate/pull/12#issuecomment-6622338482), [project-owned verifier SHA permission](https://github.com/komleff/overgate/pull/12#issuecomment-6628354758), [pre-apply continuation decision](https://github.com/komleff/overgate/pull/12#issuecomment-6628495952). Independent same-session target [PLAN_READY](https://github.com/komleff/overgate-rc4-wb02-auto-20261104/pull/1#issuecomment-6628414360) before first apply; inventory SHA256 `0522eb1a4826fcb9dd5162a9724f9305e1d367ee8c74168a3721a0689c2ee2dd`, 78 initial operations, all before null, conflicts0. [Inventory](plans/wb02-fix-simple-auto-plan.json).

| case | AC / §5.4 | method | PASS/FAIL/NOT RUN | evidence |
|---|---|---|---|---|
| Frozen source + fresh README-only target + independent install review | AC13 / 1 | Native Git + exact inventory review | PASS | [preflight](receipts/wb02-preflight.json), target PLAN_READY above |
| Literal QUICKSTART first apply in auto; helpers Memory → bd → main protection | AC05/06/08/13 / 2 | Actual Claude Bash; no coordinator apply or helper replay | PASS | [raw tools + hook events](receipts/literal-b-wb02-fix-continuation-receipts.json) |
| Memory6 exact, embedded bd1.2.2, first backup, protection, checker, project verifier | AC05/06/08/13 / 2 | Native real-state/remote checks | PASS | [installed audit](receipts/{N}-installed-audit.json), [environment](receipts/wb02-final-environment.json) |
| Exact formerly blocked cp; only target cd changed | AC05/AC13/R6 / 2 | Actual Claude Bash + raw PreToolUse success + copied hash | PASS | [copy receipt](receipts/{N}-verifier-copy.json), runtime tool ID `{found[0]}` |
| Only project-owned verifier source assertion rebound after cp | AC13 / 2 | Actual Claude Edit, byte comparison + diff | PASS | [before/after hashes and diff](receipts/{N}-verifier-bound.json) |
| Root hook activation on fresh installed runtime | AC05 / 3 | Fresh actual Claude auto: four PreToolUse hook exit2 refusals | PASS | [negative runtime](receipts/wb02-fix-negatives-receipts.json) |
| Create file, commit, push working branch, DraftPR HEAD readback | AC05/AC13 / 4 | Actual Claude Bash + Git/PR readback | PASS | [runtime](receipts/literal-b-wb02-fix-continuation-receipts.json), [final audit](receipts/{N}-final-audit.json) |
| Main push, merge, readiness-comment blocked | AC05/AC06 / 5 | Three distinct actual Claude Bash attempts, no execution | PASS | [exact inputs/refusals](receipts/wb02-final-summary.json) |
| Real server-side direct main update rejection | AC06 / 5 | Distinct unreferenced commit pushed to test main; GH006; readback | PASS | [server receipt](receipts/{N}-server-rejection.json) |
| Red project verifier blocks commit | AC05 / 6 | Stage empty README, actual Claude commit refused, restore original fixture | PASS | [negative runtime](receipts/wb02-fix-negatives-receipts.json), [restoration](receipts/{N}-red-fixture-restored.json) |
| cp protected-merge argument | AC05/R6 affected | Installed repository guard, JSON stdin only; carrier never executed | PASS | [dry controls](receipts/{N}-dry-controls.json) |
| Nested git commit in cp | AC05/R6 affected | Installed classifier=commit, canonical gate executes red verifier, exit2; carrier never executed | PASS | [dry controls](receipts/{N}-dry-controls.json) |
| Changed hook exact bytes/mode, final no-op/readback | AC05/13 affected | Git blob vs installed SHA256, observed mode0666, 73 no-op operations | PASS | [final audit](receipts/{N}-final-audit.json) |
| Other five path/mode variants and rollback | §5.4.7/8 | Not rerun by this affected packet | NOT RUN on ac58 | Historical source2343 receipts remain separately bound |
| Unavailable-auto account | R1 | No real unavailable-auto account | NOT RUN | No account-mode manipulation or OAuth substitution |
| Whole WI-1 acceptance / trusted finalization / merge / release | Outside Windows packet | PM/operator ownership | NOT RUN | No readiness or release claim |

Changed installed `.claude/hooks/commit_command_classifier.py`: source Git blob `3e54c2a2002c67185274f1f00cfc33a8e9c7f4ff`; source=installed SHA256 `5d2847e90ccc05cafdb4c0f342888687bf881a98c0ff1759e9312ad17b7c44ec`; observed Windows mode0666. PM source package fingerprint (46 paths +1812 contract bytes) `96b6c47b53a3ed42b4573928605cffd927e3e04fe59af1c4e98f5134b2d86593`; scoped three-path fingerprint `89addacf0e59fa89d0e59ec27cc07884e6e80043e1932092ce5b5ae6c075f8a8` supplied by PM/source Reviewer. Exact source SHA and installed hook binding independently checked here.

Historical external template unchanged SHA256 `7d92606526ba81f81aa3acae9bd5a264e7a647084abd161848fb9a232e74b28c`; actual copy matches. After PM-authorized single assertion substitution target verifier SHA256 `6d82963b262f512e7adda903728387b643b0499a51a4e97470d3e3dcaedfea62`. No source or managed hook edits. Server main stayed `{server['main_before']}` before/after rejection of distinct probe `{server['distinct_probe_sha']}`, enforce_admins=true; protection unchanged. Backup branch `{audit['refs']['refs/heads/beads-backup']}`.

Environment: Windows11 Pro build26200; Git {versions['git']}; Bash5.2.37; native Python3.14.0 via py-3; bd1.2.2 scoped (global old bd untouched); Claude2.1.317 scoped; {versions['gh']}; Node {versions['node']}; jq {versions['jq']}. Exact [version receipt](receipts/wb02-final-environment.json). CLI warning about ignored project allow entries in an untrusted workspace is retained in stderr; globals/trust settings unchanged. Required hooks demonstrably ran, including four actual negative refusals.

QA infrastructure history is preserved separately: initial worker used ls on intentionally absent directories and stopped before apply; PM allowed same clean target/first apply. [Initial raw tools](receipts/literal-b-wb02-fix-install-receipts.json), [pre-apply report](receipts/wb02-preapply-attempt-report.md). The first nested dry-run harness passed a Windows-backslash Bash script pathname and resolved the wrong launcher location; corrected only harness argv to canonical relative POSIX path, preserving [initial raw attempt](receipts/{N}-qa-windows-path-attempt1-dry-controls.json) and corrected raw stdout/stderr. No real nested commit/merge carrier ran. These are QA infrastructure failures, not product failures relabelled PASS.

The [five prior PASS / one WB-02 FAIL on2343](https://github.com/komleff/overgate/pull/12#issuecomment-6613785932) remain historical scoped evidence only. ac58 changes the installed classifier, so those five entire cases are not called new whole-case PASS. Source diff is exactly classifier + two tests; unchanged installer/helpers/settings surfaces may use historical evidence within that limit. R1 remains NOT RUN; this report does not accept that risk or close overall WI-1. No merge/release/finalize, working U2/OverGate checkouts unchanged, QA workers stopped.
'''
    (E/'wb02-final-report.md').write_text(report,encoding='utf-8',newline='\n')
    dirty=run(['git','status','--porcelain'],R).stdout.splitlines()
    assert all(line[3:].startswith(('receipts/wb02-','receipts/literal-b-wb02-','harness/')) or line[3:] in {'SHA256SUMS.json','WB02-WINDOWS-QA.md'} for line in dirty)
    for p in E.iterdir():
        if p.is_file() and (p.name.startswith(('wb02-','literal-b-wb02-'))) and p.suffix not in {'.jsonl','.bin'}:
            shutil.copyfile(p,R/'receipts'/p.name)
    for p in B.iterdir():
        if p.is_file() and ('wb02' in p.name) and p.suffix in {'.py','.txt'}:shutil.copyfile(p,R/'harness'/p.name)
    shutil.copyfile(E/'wb02-final-report.md',R/'WB02-WINDOWS-QA.md')
    index={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['plans','receipts','harness'] for p in (R/folder).rglob('*') if p.is_file()}
    index['WB02-WINDOWS-QA.md']=hashlib.sha256((R/'WB02-WINDOWS-QA.md').read_bytes()).hexdigest()
    (R/'SHA256SUMS.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
    run(['git','add','receipts','harness','SHA256SUMS.json','WB02-WINDOWS-QA.md'],R)
    # Server stdout/stderr receipts intentionally preserve raw trailing spaces.
    run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--','harness','WB02-WINDOWS-QA.md'],R)
    run(['git','commit','-m','docs: report affected WB-02 Windows runtime QA'],R)
    run(['git','push','origin','qa/evidence'],R)
    commit=run(['git','rev-parse','HEAD'],R).stdout.strip()
    (E/'wb02-final-evidence-sha.txt').write_text(commit,encoding='utf-8')
    root='https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+commit+'/'
    publication=re.sub(r'\]\(((?:receipts|plans)/[^)]+)\)',lambda m:']('+root+m.group(1)+')',report)
    publication+='\nImmutable evidence bundle: [WB02-WINDOWS-QA.md]('+root+'WB02-WINDOWS-QA.md), [SHA256 index]('+root+'SHA256SUMS.json).\n'
    (E/'wb02-final-pr-comment.md').write_text(publication,encoding='utf-8',newline='\n')
    print(json.dumps({'result':summary['result'],'target_head':audit['head'],'evidence_commit':commit,'files':len(index),'report_ready':str(E/'wb02-final-pr-comment.md')}))
if __name__=='__main__':main()
