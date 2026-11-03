import sys,json,subprocess
from pathlib import Path
from prepare import B,E
cs=json.loads((E/'targets.json').read_text(encoding='utf-8'))
for name in sys.argv[1:]:
 c=next(x for x in cs if x['name']==name)
 prompt=B/(name+'-live-prompt.txt');prompt.write_text((B/'live-prompt-template.txt').read_text(encoding='utf-8').replace('CASE',name),encoding='utf-8')
 p=subprocess.run([sys.executable,str(B/'run-claude.py'),name+'-live-2317',c['target'],'bypassPermissions' if c['mode']=='bypass' else 'auto',str(prompt)])
 print(name,'cli_exit',p.returncode,flush=True)
