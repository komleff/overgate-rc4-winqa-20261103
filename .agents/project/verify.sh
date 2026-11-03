#!/usr/bin/env bash
set -euo pipefail
py -3 -c "from pathlib import Path; p=Path('README.md'); assert p.is_file() and p.read_text(encoding='utf-8').strip(); print('demo README check PASS')"
