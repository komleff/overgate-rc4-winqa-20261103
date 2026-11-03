# Verification Contract — OverGate 4.0.0-rc.4 literal fresh install (Windows, simple path, auto)

Date: 2026-11-04 (Asia/Novosibirsk). Role: installer agent (Claude Code, auto). Phase A only: plan + Draft PR; apply is not performed until independent PLAN_READY.

## Target
- Repo: https://github.com/komleff/overgate-rc4-e2e-simple-20261104
- Local checkout: C:/work/overgate-e2e-auto (ASCII path, no spaces)
- main SHA (GitHub auto_init, README only): 2bbca9cdde3ccf0649bc55756f6a12f85aa9b64f
- Work branch: qa/install-e2e-auto. Agent never pushes main, never merges/finalizes.
- Product authority: оператор (AGENTS.md absent → template default). Preserved: operator authority, project check commands, custom hooks (none exist in fresh target).

## Source
- Trusted clean Git checkout: D:/CodexArtifacts/overgate-rc4-winqa-20261103/source
- Exact SHA: 403f95b8a7fae50957a99c16a211a8ef7217cb22 (v4.0.0-rc.3-18-g403f95b)
- git status --porcelain: empty (only ignored .claude/hooks/__pycache__/). Source is read-only for this install.

## Environment (recorded, not asserted as PASS)
- Windows 11 Pro 10.0.26200; Git 2.51.2.windows.1; Git Bash 5.2.37 (msys, native, not WSL)
- Native Python: py -3 / python = 3.14.0 (C:/Python314)
- bd 1.2.2 (6c124203e) on PATH; gh 2.85.0 (logged in komleff, https); jq 1.8.2; node v24.11.0
- Claude Code: session launched explicitly with `claude --permission-mode auto`, portable 2.1.317 (operator-stated); PATH `claude --version` reports 2.1.139 (global, not used by this session).
- Mode: auto (fresh default; no --mode flag). Beads: enabled (no --no-beads).

## Installer procedure under contract
1. `install-overgate.py plan --source <source> --source-sha 403f95b8… --target C:/work/overgate-e2e-auto --contract <this file> --target-pr <Draft PR URL> --output D:/CodexArtifacts/overgate-rc4-winqa-20261103/evidence/e2e-simple-auto-plan.json`
2. Plan SHA256 and conflicts published in the Draft PR. Independent reviewer (separate session) issues PLAN_READY; PM stores approval JSON bound to plan bytes. Installer does not self-approve.
3. Only after approval: `apply --plan … --approval …`; then strictly `bash scripts/og-init-memory-bank.sh`, `bash scripts/bd-bootstrap.sh`, `bash scripts/og-protect-main.sh`.
4. Fill `.agents/project/verify.sh` with real project checks (below); run `python3 scripts/check-reference.py` and `bash .agents/project/verify.sh`.

## Acceptance criteria (checked after apply; all NOT RUN in Phase A)
- AC1 Plan: source_sha == 403f95b8…; conflicts == []; operations order guards/helpers → dispatcher → settings; no writes to target during plan (git status clean after plan).
- AC2 Apply: backup journal created at `.overgate-backups/<id>/rollback.json` before first write; `.overgate/install-state.json` has source_sha, mode=auto, beads=true, no absolute machine paths.
- AC3 Managed files byte-equal to source for fresh install (rc.4 fresh claim); `.claude/settings.json` has exactly one managed PreToolUse entry calling `.claude/hooks/pre-bash.sh`, timeout 600, no backslashes.
- AC4 `.gitignore` == managed fragment bytes exactly (target had no .gitignore). README.md unchanged.
- AC5 Helpers: Memory Bank 6 files created; bd-bootstrap: bd 1.2.2 accepted, embedded DB, `beads-backup` branch pushed (first export); og-protect-main: exit 0 with readback, or code 2/3/4/5 recorded as R8 in PR and Memory Bank; code 6 = stop.
- AC6 verify.sh: minimal real project verification of README.md — file exists, non-empty, first line is `# overgate-rc4-e2e-simple-20261104`, contains "OverGate"; exit 0. Unfilled template must exit 2 (checked before fill).
- AC7 `python3 scripts/check-reference.py` exit 0 in target.
- AC8 Repeat `plan` after apply → all operations before == after.
- AC9 Live hooks: fresh auto session in target root shows pre-bash guard active (e.g. blocked `git push origin main`). Recorded as receipt, not inferred from file bytes.
- AC10 Known: QA WB-01 mode-only no-op mismatch on Windows is a known warning; requirements and source/managed code are not modified by this install.

## Out of scope / forbidden
- bypass, --no-beads, --force; editing source; reading secrets/.env; bypassing hooks/permissions; merge, release, finalize, push main.
