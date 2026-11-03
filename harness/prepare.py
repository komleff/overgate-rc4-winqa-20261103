import os,sys,subprocess,json,hashlib,urllib.request,zipfile
from pathlib import Path
B=Path(__file__).parent; E=B/'evidence'; S=B/'source'
SHA='403f95b8a7fae50957a99c16a211a8ef7217cb22'; REPO='komleff/overgate-rc4-winqa-20261103'
os.environ['PATH']=str(B/'tools')+';C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+os.environ['PATH']
os.environ['CLAUDE_CODE_GIT_BASH_PATH']='C:/Program Files/Git/bin/bash.exe'
os.environ['PYTHONUTF8']='1'
def run(args,cwd=B,label=None,ok=True,input=None):
 p=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',input=input)
 if label:(E/(label+'.txt')).write_text(json.dumps({'command':[str(x) for x in args],'cwd':str(cwd),'exit_code':p.returncode},ensure_ascii=False)+'\nSTDOUT:\n'+p.stdout+'\nSTDERR:\n'+p.stderr,encoding='utf-8')
 if ok and p.returncode:raise RuntimeError(str(args)+'\n'+p.stdout+p.stderr)
 return p
def prepare():
 # Portable exact bd; leave operator's global 0.62 untouched.
 checks=run(['gh','release','download','v1.2.2','-R','gastownhall/beads','-p','beads_1.2.2_windows_amd64.zip','-p','checksums.txt','-D',B/'tools'],label='bd-download')
 archive=B/'tools/beads_1.2.2_windows_amd64.zip'
 actual=hashlib.sha256(archive.read_bytes()).hexdigest()
 expected=next(x.split()[0] for x in (B/'tools/checksums.txt').read_text().splitlines() if x.split()[-1]=='beads_1.2.2_windows_amd64.zip')
 assert expected==actual
 with zipfile.ZipFile(archive) as z:
  exe=next(x for x in z.namelist() if x.rsplit('/',1)[-1]=='bd.exe')
  (B/'tools/bd.exe').write_bytes(z.read(exe))
 (E/'bd-checksum.json').write_text(json.dumps({'release':'v1.2.2','sha256':actual,'checksum_match':True}),encoding='utf-8')
 run(['bd','--version'],label='bd-version')
 configs=[]
 for pathclass,stem in [('simple',Path('C:/work/demo')),('complex',Path('C:/Users/komle/Мои проекты/demo app'))]:
  for mode in ['auto','no-beads','bypass','rollback']:
   name=pathclass+'-'+mode; target=stem if mode=='auto' else Path(str(stem)+'-'+mode)
   if name!='simple-auto':
    if target.exists():raise RuntimeError('target already exists '+str(target))
    run(['git','clone','https://github.com/'+REPO+'.git',target],label=name+'-clone')
    run(['git','switch','-c','qa/'+name],target,label=name+'-branch')
   contract=('Windows live QA disposable install '+name+'\nSource '+SHA+'\nTarget '+str(target)+'\n'
    'Operator is product authority. No custom settings/hooks exist. Preserve README and project authority.\n'
    'Install frozen source with '+('no Beads' if mode=='no-beads' else 'Beads')+'; '+('explicit bypass' if mode=='bypass' else 'default auto')+'.\n'
    'Named risks AC05/06/08/09/12/13 and plan section5.4: canonical Git Bash + native Python, 0 conflicts, checker PASS, six Memory Bank templates, exact bd1.2.2/main embedded, backup, protected main enforce_admins, server rejects a distinct new commit.\n'
    'Hooks must deny main push, merge, readiness comments, and commit with red project verification. Demo verification reads nonempty README.\n'
    'Claude live execution is separate; OAuth401 is NOT RUN, never substitute fixtures/config for activation PASS.\n'
    +('Rollback immediately after apply before helpers: restore every before byte/mode and absent install-state. Do not run helpers in this target.\n' if mode=='rollback' else 'After apply: Memory helper, then Beads helper unless no-beads, then protection helper; project verify must be filled with minimal README test.\n')+
    'No source fixes, no working checkout changes, no merge, no release, no finalization; all findings returned PM.\n')
   (target/'qa-install-plan.md').write_text(contract,encoding='utf-8',newline='\n')
   run(['git','add','qa-install-plan.md'],target)
   run(['git','commit','-m','docs: plan isolated '+name+' Windows QA'],target,label=name+'-planning-commit')
   run(['git','push','-u','origin','qa/'+name],target,label=name+'-planning-push')
   body=E/(name+'-pr-body.md');body.write_text(contract+'\nIndependent PLAN_READY required before apply. QA receipts will follow.\nRole/model: PM + Windows QA / Codex GPT-6.\n',encoding='utf-8')
   url=run(['gh','pr','create','--draft','--base','main','--head','qa/'+name,'--title','Windows QA '+name+' exact403f95b','--body-file',body],target,label=name+'-pr').stdout.strip()
   cp=E/(name+'-contract.md');cp.write_text(contract,encoding='utf-8',newline='\n')
   plan=E/(name+'-plan.json')
   args=[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',target,'--contract',cp,'--target-pr',url,'--output',plan]
   if mode=='no-beads':args+=['--no-beads']
   if mode=='bypass':args+=['--mode','bypass']
   run(args,label=name+'-plan')
   value=json.loads(plan.read_bytes());assert not value['conflicts']
   digest=hashlib.sha256(plan.read_bytes()).hexdigest()
   targetsha=run(['git','rev-parse','HEAD'],target).stdout.strip()
   c={'name':name,'target':str(target),'mode':mode,'pr':url,'plan':str(plan),'contract':str(cp),'plan_sha256':digest,'target_before_sha':targetsha,'source_sha':SHA}
   configs.append(c)
   (E/'targets.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2),encoding='utf-8')
   comment=E/(name+'-inventory-comment.md');comment.write_text('Inventory generated, not applied. Source `'+SHA+'`; target `'+targetsha+'`.\nPlan SHA256 `'+digest+'`; conflicts 0; operations '+str(len(value['operations']))+'.\nFull plan is in the local QA evidence package '+str(plan)+'. Independent review follows before apply.\n— PM/QA (Codex GPT-6)\n',encoding='utf-8')
   run(['gh','pr','comment',url,'--body-file',comment],target,label=name+'-inventory-publish')
   print(name,url,digest,flush=True)
if __name__=='__main__':prepare()
