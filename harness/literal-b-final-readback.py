import json,sys
from prepare import B,E,run
cases=json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8'));out=[]
for c in cases:
 name=c['name'];p=E/(name+'-final-audit.json')
 if not p.exists():
  out.append({'case':name,'source_sha':c['source_sha'],'result':'FAIL' if (E/(name+'-failure.json')).exists() else 'NOT RUN','reason':'WB-02 hook deny, stopped; no retry' if (E/(name+'-failure.json')).exists() else 'no final audit','path':c['target'],'pr':c['pr']});continue
 code=run([sys.executable,B/'audit-literal-b.py',name,'final'],label=name+'-independent-final-readback',ok=False).returncode
 r=json.loads(p.read_text(encoding='utf-8'));out.append({'case':name,'source_sha':c['source_sha'],'result':r['result'],'path':c['target'],'pr':c['pr'],'head':r['head'],'backup_sha':r.get('backup_sha'),'runtime':r['runtime_init'],'checks':r['checks'],'independent_readback_exit':code});print(name,r['result'],r['head'],flush=True)
(E/'literal-b-final-matrix.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
