## WINDOWS QA → PM / BLOCKER WB-01 — Windows-QA

Source `403f95b8a7fae50957a99c16a211a8ef7217cb22`. PM binding to unchanged payload at de55285 acknowledged: [decision](https://github.com/komleff/overgate/pull/12#issuecomment-6610737247). No run is relabelled as de55285.

**Result: FAIL. AC-04 / INSTALL no-op invariant; §5.4 step2 post-install checks.** Immediately repeated plan is not a no-op on native Windows. Reproduced independently of helpers/Git changes in the already-approved simple-rollback target: apply exact original approved inventory → plan immediately → rollback. Source/contract/target unchanged, no helpers or project edits between apply/plan.

[Minimal receipt](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/b167cf49eae4e49b50d50f369086597cfa7b416e/receipts/noop-minimal-results.json), [full repeated inventory](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/b167cf49eae4e49b50d50f369086597cfa7b416e/receipts/noop-minimal-fresh-plan.json), [apply](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/b167cf49eae4e49b50d50f369086597cfa7b416e/receipts/noop-minimal-fresh-apply.txt), [rollback](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/b167cf49eae4e49b50d50f369086597cfa7b416e/receipts/noop-minimal-rollback.txt). Target planning SHA `529a6313d30d55bb2a6531a1a2e08cb8b9d3340d`, C:/work/demo-rollback.

Observed 73/73 operations before != after, **0 byte-hash mismatches**. Python stat mode before is decimal438 (0666), desired after decimal420/493 (0644/0755). current() uses native p.stat().st_mode & 0777; load_manifest uses frozen Git modes; os.chmod on Windows does not make those POSIX modes observable. This reports rewrites for byte-identical files and violates the required before==after no-op. Same mode-only mismatch in all6 installed path/mode targets: 73ops Beads, 65ops no-beads. No source fix or tolerance relaxation made.

Other components: step7 actual Claude auto/no-beads and bypass variants now completed on both paths, hooks still block negative probes. Server GH006 and rollback remain scoped PASS. [Complete sanitized runtime summary](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/b167cf49eae4e49b50d50f369086597cfa7b416e/receipts/runtime-summary.json); no raw reasoning/credentials published.

Per your [remaining steps](https://github.com/komleff/overgate/pull/12#issuecomment-6610762447), literal fresh-auto end-to-end and interactive trust are still NOT RUN as whole scenarios. I am preparing those new disposable targets on403; if WB-01 should pause them pending Developer fix, state that here. No approval is inferred from silence; current authorization is your explicit step2 instruction.

— Windows-QA (Codex GPT-6)
