## WINDOWS QA → PM / WB-01 FIX EXECUTION — Windows-QA

**Source `2343df83a3a26ae83bc66d4009dd67a913eeea4e`. Result: PASS for affected native WB-01 cases**, not overall PR acceptance. Role/model Windows QA / Codex GPT-6; Python3.14/Git Bash5.2.37 on physical Windows11. Four exact target plans independently approved/published before apply in the existing Reviewer session.

[Immutable evidence bundle](https://github.com/komleff/overgate-rc4-winqa-20261103/tree/8c18bd9daf035fed68faa764a7842c091dab83c4/receipts):

| Native case | Result | Evidence |
|---|---|---|
| Simple fresh apply → immediate plan | PASS:73ops, conflicts0, every before==after | [receipt](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/8c18bd9daf035fed68faa764a7842c091dab83c4/receipts/fix-simple-fresh-results.json) |
| Complex fresh apply → immediate plan | PASS:same73 equality | [receipt](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/8c18bd9daf035fed68faa764a7842c091dab83c4/receipts/fix-complex-fresh-results.json) |
| Simple403→2343 approved upgrade → plan/checker | PASS:73equal, checker0, no helper replay | [receipt](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/8c18bd9daf035fed68faa764a7842c091dab83c4/receipts/fix-simple-upgrade-results.json) |
| Complex403→2343 upgrade → plan/checker | PASS:same | [receipt](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/8c18bd9daf035fed68faa764a7842c091dab83c4/receipts/fix-complex-upgrade-results.json) |
| Changed managed bytes, both fresh paths | PASS:addressed conflict, no target writes; exact bytes restored | fresh receipts above |
| Stale original approved plan re-apply | PASS:exit1 before backup/target writes, both paths | fresh receipts above |
| Immediate rollback after controls | PASS:all before bytes/modes/state restored, both paths | fresh receipts above |

QA harness correction: plan intentionally returns exit0 while reporting conflicts. Initial assertion incorrectly expected nonzero; conflict itself was correctly detected. Corrected predicate checks conflict/address/no writes; additional managed ADR probe passed. Audit annotations retained; no invented product defect or waived check.

Installed E2E state now2343/auto/beads=true, upgraded only managed installer, existing Memory/BD/backup/protection retained. Fresh403 baseline FAIL stays historical. Continuing the already-authorized remaining §5.4 auto completion sequentially (project tests strict2343/mode/beads, actual commit/push and final readback). No further apply/helpers/DB init. Full latest-HEAD literal fresh2343 not claimed: actual history fresh403 → interruption → approved2343 upgrade.

— Windows-QA (Codex GPT-6)
