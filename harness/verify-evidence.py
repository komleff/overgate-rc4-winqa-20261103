from pathlib import Path
import json,hashlib,subprocess
from prepare import B,E,run
rows=json.loads((E/'completed-403-matrix.json').read_text(encoding='utf-8'))
for r in rows:
 probes=r.get('negative_probe_receipts',[])
 if probes:
  red=[x for x in probes if 'red verification must block' in x['command']]
  protected=[x for x in probes if 'red verification must block' not in x['command']]
  r['step5_live']='PASS' if len(protected)==3 and all(x['hook_intercept'] for x in protected) else 'NOT RUN'
  r['step6_live']='PASS' if len(red)==1 and red[0]['hook_intercept'] and ('QA intentional red' in red[0]['reason']) else 'NOT RUN'
(E/'completed-403-matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
# Verify the published byte checksums against Git objects; no test tools/databases started.
R=B/'evidence-repo';sums=json.loads((R/'SHA256SUMS.json').read_text(encoding='utf-8'));bad=[]
for path,want in sums.items():
 p=subprocess.run(['git','show','HEAD:'+path],cwd=R,capture_output=True)
 if p.returncode or hashlib.sha256(p.stdout).hexdigest()!=want:bad.append(path)
print(json.dumps({'published_file_count':len(sums),'sha256_mismatches':bad},ensure_ascii=True))
(E/'evidence-byte-verification.json').write_text(json.dumps({'published_file_count':len(sums),'sha256_mismatches':bad},indent=2),encoding='utf-8')
