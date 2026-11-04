#!/usr/bin/env bash
set -euo pipefail
py -3 -I - <<'PY'
import json
from pathlib import Path
p=Path("README.md")
assert p.is_file() and p.read_bytes().strip(), "README absent or empty"
s=json.loads(Path(".overgate/install-state.json").read_text(encoding="utf-8"))
assert s.get("source_sha")=="ac58c9689d921cc859661e4cb7eb37a5b67c5abe", "source SHA"
assert s.get("mode")=="auto", "state mode"
assert s.get("beads") is True, "strict Beads bool"
print("PASS: README and exact B/mode/Beads")
PY
