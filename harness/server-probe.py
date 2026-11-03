import json
from prepare import B,E,REPO,run
R=B/'server-probe'
run(['gh','api','repos/'+REPO+'/branches/main/protection'],label='server-protection-readback')
initial=run(['gh','api','repos/'+REPO+'/git/ref/heads/main'],label='server-main-before')
before=json.loads(initial.stdout)['object']['sha']
run(['git','clone','https://github.com/'+REPO+'.git',R],label='server-probe-clone')
run(['git','switch','-c','qa/server-rejection-probe'],R,label='server-probe-branch')
(R/'server-rejection-probe.txt').write_text('Disposable test repo only. This new commit must be rejected as a direct main update.\n',encoding='utf-8',newline='\n')
run(['git','add','server-rejection-probe.txt'],R)
run(['git','commit','-m','test: distinct commit for server main rejection'],R,label='server-probe-commit')
candidate=run(['git','rev-parse','HEAD'],R).stdout.strip();assert candidate!=before
run(['git','push','-u','origin','qa/server-rejection-probe'],R,label='server-probe-branch-push')
# Separate native terminal Git process: untouched initial README checkout, no installed local hooks.
# No --no-verify, hooksPath override, force, protection changes, or credentials overrides.
p=run(['git','push','origin','HEAD:refs/heads/main'],R,label='server-main-rejected-push',ok=False)
final=run(['gh','api','repos/'+REPO+'/git/ref/heads/main'],label='server-main-after')
after=json.loads(final.stdout)['object']['sha']
protection=json.loads(run(['gh','api','repos/'+REPO+'/branches/main/protection'],label='server-protection-after').stdout)
data={'repository':REPO,'local_checkout':str(R),'source_branch':'qa/server-rejection-probe','attempted_refspec':'HEAD:refs/heads/main','candidate_sha':candidate,'main_before_sha':before,'main_after_sha':after,'exit_code':p.returncode,'enforce_admins':protection['enforce_admins']['enabled'],'rejected_by_server':p.returncode!=0 and ('GH006' in p.stderr or 'GH013' in p.stderr) and before==after,'no_protection_or_hook_override':True}
(E/'server-rejection-results.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print(json.dumps(data,indent=2));print(p.stdout+p.stderr)
