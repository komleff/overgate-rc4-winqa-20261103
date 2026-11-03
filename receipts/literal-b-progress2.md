## WINDOWS QA → PM / FRESH B PROGRESS 2 — Windows-QA

Source/HEAD2343df83a3a26ae83bc66d4009dd67a913eeea4e. На текущем этапе: **4 PASS, 1 FAIL WB-02, 1 in progress**.

| Fresh case | Result | Exact target HEAD / evidence |
|---|---|---|
| simple auto | FAIL, stopped/no retry | [WB-02](https://github.com/komleff/overgate/pull/12#issuecomment-6612948384) |
| simple no-beads | PASS | e9c1080592dc9f391ecb5e9b7a9f0d6de07be0db; [audit](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/d4342a1d5e2699d536bbc79e6006f488db044146/receipts/literal-b-simple-no-beads-final-audit.json) |
| simple bypass | PASS | 187a377272efbc75c2c8ef99152a43a55ae52780; [audit](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/d4342a1d5e2699d536bbc79e6006f488db044146/receipts/literal-b-simple-bypass-final-audit.json) |
| complex auto | PASS | a216fae295810d1965a0004e6212d3f9818e5881; [audit](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/d4342a1d5e2699d536bbc79e6006f488db044146/receipts/literal-b-complex-auto-final-audit.json) |
| complex no-beads | PASS | 800a38ece4cac2c8ad5fbe3dc1e1961b0df003c9; [audit](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/d4342a1d5e2699d536bbc79e6006f488db044146/receipts/literal-b-complex-no-beads-final-audit.json) |
| complex bypass | NOT RUN until complete | единственный active foreground worker |

Все завершённые PASS имеют B с первого apply, корректные actual runtime flags, helpers/checker/noop65/73equal, Memory6, expected Beads/backup/protection, clean/indexempty/remote=PRhead. Native coordinator apply или A→B upgrade здесь не было. Для каждого PASS сохранён отдельный A-B-runtime-binding.json с exact bytes/observed modes, runtime init и actual-A command primitive mapping. A receipts остаются A.

Metadata correction: наш collector раньше ошибочно ставил constant A source_sha в синтетический envelope даже у фактических B phase-C/literal-B transcripts. Исправлен вывод header из exact independently reviewed case plan / actual upgrade result; raw tool calls/results, actual source/state/targetSHA не менялись. [Подробная correction note](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/d4342a1d5e2699d536bbc79e6006f488db044146/receipts/collector-source-envelope-correction.json). A-сессии НЕ переименованы; старые immutable bundles сохранены. Новый bundle содержит корректные envelopes B и неизменённые A.

R1 unavailable-account — NOT RUN; source/guards не исправлялись. После последнего case опубликую final affected report.

— Windows-QA (Codex GPT-6)
