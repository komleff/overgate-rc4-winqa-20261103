import sys,json,hashlib,subprocess
from pathlib import Path
from prepare import B,E,run
c=json.loads((E/'wb02-fix-simple-auto-target.json').read_text());T=Path(c['target']);N=c['name']
def save(name,r): (E/(N+'-'+name+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
def hook(command,path,label):
    payload=json.dumps({'tool_name':'Bash','tool_input':{'command':command},'cwd':str(T)})
    (E/(N+'-'+label+'-input.json')).write_text(payload,encoding='utf-8',newline='\n')
    args=[sys.executable,T/path] if path.endswith('.py') else ['C:/Program Files/Git/bin/bash.exe',path]
    p=run(args,T,label=N+'-'+label,ok=False,input=payload)
    return {'command':command,'hook':path,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'carrier_executed':False}
def red():
    assert json.loads((E/(N+'-final-audit.json')).read_text())['result']=='PASS'
    assert not run(['git','status','--porcelain'],T).stdout
    head=run(['git','rev-parse','HEAD'],T).stdout.strip();data=(T/'README.md').read_bytes()
    assert data.strip();(E/(N+'-readme-before-red.bin')).write_bytes(data)
    (T/'README.md').write_bytes(b'');run(['git','add','README.md'],T)
    checks=[]
    r=hook("cp 'gh pr merge 1' d/",'.claude/hooks/check-repository-mutation.py','cp-protected-dryrun')
    r['result']='PASS' if r['exit_code']==2 else 'FAIL';checks.append(r)
    command='cp "$(git commit -m wb02-nested-probe)" d/'
    cl=run([sys.executable,T/'.claude/hooks/commit_command_classifier.py','classify'],T,label=N+'-nested-classifier',input=command)
    r=hook(command,'.claude/hooks/check-tests-before-commit.sh','nested-commit-gate-dryrun')
    r['classification']=cl.stdout.strip();r['result']='PASS' if cl.stdout.strip()=='commit' and r['exit_code']==2 and 'README absent or empty' in (r['stdout']+r['stderr']) else 'FAIL';checks.append(r)
    unchanged=run(['git','rev-parse','HEAD'],T).stdout.strip()==head
    result={'source_sha':c['source_sha'],'head_before':head,'head_after_unchanged':unchanged,'readme_original_sha256':hashlib.sha256(data).hexdigest(),'readme_now_empty':True,'checks':checks,'result':'PASS' if unchanged and all(x['result']=='PASS' for x in checks) else 'FAIL'}
    save('dry-controls',result);print(json.dumps(result));return 0 if result['result']=='PASS' else 1
def restore():
    data=(E/(N+'-readme-before-red.bin')).read_bytes();(T/'README.md').write_bytes(data)
    run(['git','restore','--staged','--','README.md'],T,label=N+'-restore-readme-index')
    result={'restored_original_sha256':hashlib.sha256(data).hexdigest(),'target_clean':not run(['git','status','--porcelain'],T).stdout}
    save('red-fixture-restored',result);print(json.dumps(result));return 0 if result['target_clean'] else 1
def server():
    before=run(['git','ls-remote','origin','refs/heads/main'],T,label=N+'-server-main-before').stdout.split()[0]
    tree=run(['git','rev-parse','origin/main^{tree}'],T).stdout.strip()
    probe=run(['git','commit-tree',tree,'-p',before],T,label=N+'-server-probe-object',input='QA: distinct unreferenced main-protection probe; no branch update\n').stdout.strip();assert probe!=before
    p=run(['git','push','origin',probe+':refs/heads/main'],T,label=N+'-server-direct-main-push',ok=False)
    after=run(['git','ls-remote','origin','refs/heads/main'],T,label=N+'-server-main-after').stdout.split()[0]
    prot=json.loads(run(['gh','api','repos/'+c['repo']+'/branches/main/protection'],T,label=N+'-server-protection').stdout)
    result={'source_sha':c['source_sha'],'remote':c['repo'],'main_before':before,'distinct_probe_sha':probe,'push_rc':p.returncode,'push_stdout':p.stdout,'push_stderr':p.stderr,'main_after':after,'enforce_admins':prot['enforce_admins']['enabled'],'local_head':run(['git','rev-parse','HEAD'],T).stdout.strip(),'protection_changed_by_probe':False}
    result['result']='PASS' if p.returncode!=0 and 'GH006' in p.stderr and before==after and prot['enforce_admins']['enabled'] is True else 'FAIL'
    save('server-rejection',result);print(json.dumps(result));return 0 if result['result']=='PASS' else 1
if __name__=='__main__': sys.exit({'red':red,'restore':restore,'server':server}[sys.argv[1]]())
