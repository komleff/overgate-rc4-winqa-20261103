import json,hashlib
from prepare import B,E,S,SHA,REPO,run
manifest=json.loads((S/'.agents/distribution-manifest.json').read_bytes())
paths=sorted(set(x['source'] for x in manifest['files'])|{'scripts/install-overgate.py','scripts/check-reference.py','docs/plans/2026-10-24-v4.0.0-rc.4.md','QUICKSTART.md','AGENTS.md'})
lines=''.join(p+' '+run(['git','rev-parse',SHA+':'+p],S).stdout.strip()+'\n' for p in paths)
contract=run(['git','show',SHA+':docs/plans/2026-10-24-v4.0.0-rc.4.md'],S).stdout
# Scope contract: exact UTF-8 LF bytes of approved plan section5.4 up to section6.
section='### 5.4'+contract.split('### 5.4',1)[1].split('\n## 6.',1)[0]
(E/'tested-source-paths-and-blobs.txt').write_text(lines,encoding='utf-8',newline='\n')
(E/'source-contract-section5.4.md').write_text(section,encoding='utf-8',newline='\n')
fp=hashlib.sha256(lines.encode()+section.encode()).hexdigest()
(E/'content-fingerprint.txt').write_text(fp+'\n',encoding='utf-8')
run(['gh','api','repos/komleff/overgate/issues/comments/6610035146'],label='pm-packet')
run(['gh','pr','view','12','-R','komleff/overgate','--json','headRefOid,baseRefOid,state,isDraft,mergeable'],label='source-pr-freshness')
for name,args in [('windows',['powershell','-NoProfile','-Command','Get-CimInstance Win32_OperatingSystem | Format-List Caption,Version,BuildNumber']),('git',['git','--version']),('python',['py','-3','--version']),('bash',['C:/Program Files/Git/bin/bash.exe','--version']),('bd',['bd','--version']),('gh',['gh','--version']),('node',['node','--version']),('jq',['jq','--version']),('claude-qa',[str(B/'tools/claude-runtime/node_modules/.bin/claude.cmd'),'--version']),('claude-global',['C:/Users/komle/AppData/Roaming/npm/claude.cmd','--version']),('codex',['C:/Users/komle/AppData/Roaming/npm/codex.cmd','--version'])]:
 run(args,label='version-'+name)
print('fingerprint',fp,'source paths',len(paths))
