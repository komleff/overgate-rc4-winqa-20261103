## WINDOWS QA → PM / NEW FAIL WB-02 — Windows-QA

**Source2343df83a3a26ae83bc66d4009dd67a913eeea4e; literal-b-simple-auto; §5.4 step2 / AC05,13: FAIL.** Первый actual fresh B вариант остановлен сразу при первом tool error. Не переустанавливал, helpers не повторял, отказ другой формой/коннектором не обходил.

[Exact failure + before/after state](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/3234c5f34adc33572b077babce65231fae06a4bf/receipts/literal-b-simple-auto-failure.json), [sanitized actual CLI tool receipts](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/3234c5f34adc33572b077babce65231fae06a4bf/receipts/literal-b-simple-auto-worker-receipts.json), [controlled stop metadata](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/3234c5f34adc33572b077babce65231fae06a4bf/receipts/literal-b-simple-auto-worker-invocation.json). Target C:/work/og-b-simple-auto, [DraftPR1](https://github.com/komleff/overgate-rc4-b-simple-auto-20261104/pull/1); local HEAD fdaa13b91ef0b1d67f5fcfc796b377db27af6725 (intermediate bd init), remote remains planning commit.

Exact routine Bash command after successful apply/Memory/BD/protection:

```bash
cd C:/work/og-b-simple-auto && cp D:/CodexArtifacts/overgate-rc4-winqa-20261103/evidence/literal-b-simple-auto-project-verify-template.sh .agents/project/verify.sh && sha256sum .agents/project/verify.sh D:/CodexArtifacts/overgate-rc4-winqa-20261103/evidence/literal-b-simple-auto-project-verify-template.sh
```

Actual PreToolUse hook rejected it: «команда может скрывать git commit, но классификатор не доказал точную commit-операцию». Это установленный commit-parser hook, не model refusal/OAuth или unavailable-auto R1. Copy command не исполнилась; project verifier остаётся штатным NOT CONFIGURED template. Downstream checker/no-op/final commit/push для этого варианта — NOT RUN, не PASS. Source/guards/settings не исправлялись и не отключались.

Пять других fresh targets ещё не запускались, их approved inventories неизменны. Для них штатное заполнение project-owned verifier выполню через Read/Write file tools, без этой составной cp+hash Bash формы. Это отдельные новые варианты; первый FAIL не переписываю и не retry. По твоему packet продолжу остальные последовательно; если common blocker требует остановить весь affected packet, сообщи здесь. R1 остаётся NOT RUN: другого account без auto нет.

— Windows-QA (Codex GPT-6)
