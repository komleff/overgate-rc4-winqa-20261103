#!/usr/bin/env bash
set -euo pipefail
py -3 -I - <<'PY'
import json
from pathlib import Path
p=Path("README.md")
assert p.is_file() and p.read_bytes().strip(), "README absent or empty"
s=json.loads(Path(".overgate/install-state.json").read_text(encoding="utf-8"))
assert s.get("source_sha")=="2343df83a3a26ae83bc66d4009dd67a913eeea4e", "source SHA"
assert s.get("mode")=="auto", "state mode"
assert s.get("beads") is True, "strict Beads bool"
print("PASS: README and exact B/mode/Beads")
PY
