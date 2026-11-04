# WB-02 affected Windows QA: pre-apply attempt

Role/model: Windows QA / Codex GPT-6. Source: ac58c9689d921cc859661e4cb7eb37a5b67c5abe. Target planning HEAD:6645603156c47e9211e1a262862fcd09edb35633; C:/work/og-wb02-auto, test PR1. PM packet6622330220, command clarification6622338482, verifier permission6628354758.

| case | AC | method | result | evidence |
|---|---|---|---|---|
| Frozen clean source, new target and exact inventory | AC13 / section5.4.1 | Native readback + independent same-session review | PASS | wb02-preflight.json; plan, contract, target review6628414360 |
| QA worker preflight command | QA infrastructure | Actual Claude auto Bash lists intentionally absent directories; ls exits2; wrapper stops | FAIL | literal-b-wb02-fix-install-receipts.json; invocation exit1 |
| First apply / helpers / literal cp | AC05/AC13/R6 / section5.4.2 | Actual runtime | NOT RUN | No apply or helper tool call; no install-state; target clean |
| Hook startup and workflow/negative controls/no-op | section5.4.3–6 | Actual runtime and installed-hook input | NOT RUN | Dependent on first apply |
| unavailable-auto account | R1 | Actual unavailable account | NOT RUN | Account unavailable; this is not an OAuth/auto refusal |
| Other five historical variants | Historical source2343 only | No rerun authorized | NOT RUN on new SHA | Historical five PASS remain separately bound to2343 |

No new product FAIL or acceptance is inferred from the QA preflight failure. No source/managed files changed, no apply/helpers/retries, merge/release/finalize. QA wrapper stopped its own process tree. PM continuation question6628475422: allow same unchanged target/exact inventory and successful native existence assertion before first apply, or require another target. Initial failed attempt retained regardless of continuation.
