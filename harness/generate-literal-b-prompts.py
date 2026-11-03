import json
from prepare import B,E
cases=json.loads((E/'literal-b-targets.json').read_text(encoding='utf-8'))
for c in cases:
 verifier='#!/usr/bin/env bash\nset -euo pipefail\npy -3 -I - <<\'PY\'\nimport json\nfrom pathlib import Path\np=Path("README.md")\nassert p.is_file() and p.read_bytes().strip(), "README absent or empty"\ns=json.loads(Path(".overgate/install-state.json").read_text(encoding="utf-8"))\nassert s.get("source_sha")=="'+c['source_sha']+'", "source SHA"\nassert s.get("mode")=="'+c['state_mode']+'", "state mode"\nassert s.get("beads") is '+str(c['beads'])+', "strict Beads bool"\nprint("PASS: README and exact B/mode/Beads")\nPY\n'
 (E/(c['name']+'-project-verify-template.sh')).write_text(verifier,encoding='utf-8',newline='\n')
 text=(B/'literal-b-worker-prompt.txt').read_text(encoding='utf-8');subs={'TARGET_PR':c['pr'],'TARGET':c['target'].replace('\\','/'),'SOURCE':c['source'].replace('\\','/'),'RUNTIME':c['runtime_mode'],'FLAGS':'--no-beads' if not c['beads'] else '--mode bypass' if c['mode']=='bypass' else '(none: default auto)','STATE_MODE':c['state_mode'],'BOOL':str(c['beads']),'MODE':c['mode'],'CASE':c['name'],'BEADS_STEP':'`bash scripts/bd-bootstrap.sh`' if c['beads'] else 'BD helper ПРОПУСТИТЬ: --no-beads, никаких bd init/bootstrap/ready и никакой .beads'}
 for k in sorted(subs,key=len,reverse=True):text=text.replace(k,subs[k])
 (B/(c['name']+'-worker-prompt.txt')).write_text(text,encoding='utf-8')
