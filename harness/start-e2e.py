import sys,json,subprocess
from pathlib import Path
from prepare import B,E,REPO,run
configs=[]
for name,t,repo in [('e2e-simple-auto',Path('C:/work/overgate-e2e-auto'),'komleff/overgate-rc4-e2e-simple-20261104'),('e2e-complex-auto',Path('C:/Users/komle/Мои проекты/overgate e2e auto'),'komleff/overgate-rc4-e2e-complex-20261104')]:
 assert not t.exists()
 run(['gh','api','user/repos','--method','POST','--input','-'],label=name+'-repo-create',input=json.dumps({'name':repo.split('/')[1],'description':'Disposable literal fresh Windows auto install for OverGate PR12 exact403f95b','private':False,'auto_init':True}))
 run(['git','clone','https://github.com/'+repo+'.git',t],label=name+'-clone')
 c={'name':name,'target':str(t),'repo':repo};configs.append(c)
 p=B/(name+'-phase-a-prompt.txt');p.write_text((B/'e2e-phase-a.txt').read_text(encoding='utf-8').replace('E2E-NAME',name),encoding='utf-8')
 c['prompt']=str(p)
(E/'e2e-targets.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(configs))
