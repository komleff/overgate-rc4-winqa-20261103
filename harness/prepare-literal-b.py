import sys,json,hashlib
from pathlib import Path
from prepare import B,E,run
SHA='2343df83a3a26ae83bc66d4009dd67a913eeea4e';S=B/'source-2343df8';cases=[]
def main():
 assert run(['git','rev-parse','HEAD'],S).stdout.strip()==SHA
 assert not run(['git','status','--porcelain'],S).stdout
 for pc in ['simple','complex']:
  for mode in ['auto','no-beads','bypass']:
   name='literal-b-'+pc+'-'+mode;repo='komleff/overgate-rc4-b-'+pc+'-'+mode+'-20261104';target=Path('C:/work/og-b-'+pc+'-'+mode) if pc=='simple' else Path('C:/Users/komle/Мои проекты/og B '+mode)
   if target.exists():raise RuntimeError('New target already exists: '+str(target))
   run(['gh','api','user/repos','--method','POST','--input','-'],label=name+'-repo-create',input=json.dumps({'name':repo.split('/')[1],'description':'Disposable exact2343 literal Windows fresh '+pc+' '+mode,'private':False,'auto_init':True}))
   run(['git','clone','https://github.com/'+repo+'.git',target],label=name+'-clone');run(['git','switch','-c','install/overgate-b'],target,label=name+'-branch')
   beads=mode!='no-beads';state_mode='bypass' if mode=='bypass' else 'auto';runtime='bypassPermissions' if mode=='bypass' else 'auto'
   contract=('Literal fresh Windows QUICKSTART install on exact B '+SHA+' from managed-empty README-only target.\n'
    'Case '+name+'; target '+str(target)+'; repository '+repo+'; branch install/overgate-b. Operator retains product authority; no existing AGENTS/settings/hooks/Memory/Beads/install-state.\n'
    'Requested installer flags '+('--no-beads' if not beads else '--mode bypass' if mode=='bypass' else '(none: default auto)')+'; actual Claude startup mode '+runtime+'. State mode '+state_mode+'; beads strict bool '+str(beads)+'.\n'
    'Coordinator creates DraftPR, VC, exact inventory and independent target PLAN_READY before any managed apply. Actual Claude receives literal QUICKSTART phrase and accepted pins, validates approval, executes first B apply and helpers; no native coordinator apply substitution.\n'
    'After apply strictly Memory helper -> '+('BD bootstrap first export to empty remote -> ' if beads else 'skip BD helper -> ')+'protection helper. Codes2/3/4/5 produce explicit R8; code6 STOP. Do not weaken protection or overwrite existing context.\n'
    'Require operation byte/mode identity, Memory six templates, '+('embedded bd1.2.2 ready/config and independent first beads-backup' if beads else 'no Beads component/files/database and no Beads AGENTS block')+', protection readback, native checker PASS, project verifier tests real README plus exact source/mode/strictBeads. Immediate plan must have conflicts0 and all before==after. Actual working-branch commit/push in same DraftPR; final tree/index clean and SHA==remote/PR.\n'
    'First B problem: FAIL and stop this variant, no product/source fix, no reapply/helper replay. Only new test roots/repos; sequential single foreground Claude/Beads job. No merge/release/finalizer.\n'
    'A runtime steps4/5/6 may be reused only after exact installed hook/tool/settings bytes+observed-mode comparison for corresponding path/mode and explicit command primitive mapping; no relabelling A as B. R1 unavailable-account is NOT RUN if only working-auto account available.\n')
   cp=E/(name+'-contract.md');cp.write_text(contract,encoding='utf-8',newline='\n');(target/'qa-install-plan.md').write_text(contract,encoding='utf-8',newline='\n')
   run(['git','add','qa-install-plan.md'],target);run(['git','commit','-m','docs: plan literal B Windows fresh '+pc+' '+mode],target,label=name+'-planning-commit');run(['git','push','-u','origin','install/overgate-b'],target,label=name+'-planning-push')
   body=E/(name+'-pr-body.md');body.write_text(contract+'\nRole/model: Windows QA coordinator / Codex GPT-6; actual installer will be Claude Code in explicit '+runtime+'.\n',encoding='utf-8')
   pr=run(['gh','pr','create','--draft','--base','main','--head','install/overgate-b','--title','Literal fresh B Windows '+pc+' '+mode,'--body-file',body],target,label=name+'-pr').stdout.strip()
   plan=E/(name+'-plan.json');args=[sys.executable,S/'scripts/install-overgate.py','plan','--source',S,'--source-sha',SHA,'--target',target,'--contract',cp,'--target-pr',pr,'--output',plan]
   if not beads:args+=['--no-beads']
   if mode=='bypass':args+=['--mode','bypass']
   run(args,label=name+'-plan');v=json.loads(plan.read_bytes());assert not v['conflicts'] and v['state_before'] is None and all(x['before'] is None for x in v['operations'])
   cases.append({'name':name,'path_class':pc,'mode':mode,'runtime_mode':runtime,'state_mode':state_mode,'beads':beads,'target':str(target),'repo':repo,'pr':pr,'source_sha':SHA,'source':str(S),'contract':str(cp),'plan':str(plan),'plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'before_head':run(['git','rev-parse','HEAD'],target).stdout.strip(),'operations':len(v['operations'])})
   (E/'literal-b-targets.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8');print(name,pr,len(v['operations']),flush=True)
if __name__=='__main__':main()
