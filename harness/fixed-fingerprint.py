import json,hashlib
from prepare import B,E,run
S=B/'source-2343df8';sha='2343df83a3a26ae83bc66d4009dd67a913eeea4e';manifest=json.loads((S/'.agents/distribution-manifest.json').read_bytes());paths=sorted(set(x['source'] for x in manifest['files'])|{'scripts/install-overgate.py','scripts/check-reference.py','docs/plans/2026-10-24-v4.0.0-rc.4.md','QUICKSTART.md','AGENTS.md'})
ls=run(['git','ls-tree','-r',sha],S).stdout;blobs={line.split('\t',1)[1]:line.split('\t',1)[0].split()[2] for line in ls.splitlines()};lines=''.join(p+' '+blobs[p]+'\n' for p in paths)
contract=run(['git','show',sha+':docs/plans/2026-10-24-v4.0.0-rc.4.md'],S).stdout;section='### 5.4'+contract.split('### 5.4',1)[1].split('\n## 6.',1)[0];fp=hashlib.sha256(lines.encode()+section.encode()).hexdigest()
(E/'fixed-tested-paths-and-blobs.txt').write_text(lines,encoding='utf-8',newline='\n');(E/'fixed-source-contract-section5.4.md').write_text(section,encoding='utf-8',newline='\n');(E/'fixed-content-fingerprint.txt').write_text(fp+'\n',encoding='utf-8');print(fp)
