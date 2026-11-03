Windows E2E literal fresh auto install (e2e-complex-auto)
Source 403f95b8a7fae50957a99c16a211a8ef7217cb22 (clean trusted Git checkout D:/CodexArtifacts/overgate-rc4-winqa-20261103/source)
Target C:\Users\komle\Мои проекты\overgate e2e auto, repo komleff/overgate-rc4-e2e-complex-20261104, branch qa/install-e2e-auto, base main 6ae19d5712ec60c26a2ed50cae3dde2d3cf28578
Target PR https://github.com/komleff/overgate-rc4-e2e-complex-20261104/pull/1
Operator is product authority. Project consists of README only; no custom settings/hooks/AGENTS exist. Preserve README and project authority.
Install frozen source with Beads; mode auto (explicit claude --permission-mode auto); no bypass, no --no-beads.
Runtime: Git Bash (GNU bash 5.2.37 msys), native Python 3.14.0 via py -3, git 2.51.2.windows.1, gh 2.85.0, jq 1.8.2, node v24.11.0, bd 1.2.2 (6c124203e), Claude Code CLI 2.1.139 reported / portable 2.1.317 harness.
Expected plan: 0 conflicts, operations guards/helpers -> dispatcher -> settings, before==after only on re-plan after apply.
After apply strictly: bash scripts/og-init-memory-bank.sh (six Memory Bank files), bash scripts/bd-bootstrap.sh (embedded bd 1.2.2, beads-backup branch pushed), bash scripts/og-protect-main.sh (PR required, enforce_admins true, force/delete false; codes 2/3/4/5 recorded as R8, code 6 stop).
Project verification: .agents/project/verify.sh must check the real README.md (exists, nonempty, contains project title); unfilled template FAIL is expected before fill. python3 scripts/check-reference.py must PASS in target.
Hooks must deny main push, merge, readiness comments, and commit with red project verification.
Independent PLAN_READY from a separate reviewer before apply; installer never self-approves. Live auto activation evidence is separate; file bytes are not mode evidence.
Known WB-01 mode-only no-op mismatch on Windows: do not change requirements, source or managed code.
No source fixes, no working U2/OverGate checkout changes, no merge, no release, no finalize, no push to main.
