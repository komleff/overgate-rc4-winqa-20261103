## WINDOWS QA → PM / FRESH B PROGRESS 1 — Windows-QA

Exact source2343df83a3a26ae83bc66d4009dd67a913eeea4e.

- simple/auto остаётся **FAIL WB-02**, остановлен без retry после actual hook denial на составную cp+hash команду; [предыдущий FAIL](https://github.com/komleff/overgate/pull/12#issuecomment-6612948384) не переписываю.
- simple/--no-beads — **PASS**: literal first apply сразу B, actual Claude auto, helpers Memory/protection (BD skipped), checker/projectverify/noop65equal, noBeads payload/db/backup, runtime binding, finaltree/indexclean. Target HEAD/remote/DraftPR1 `e9c1080592dc9f391ecb5e9b7a9f0d6de07be0db`; [final audit](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/e7104fa0dcdcd121e66af860a14612262c5b0166/receipts/literal-b-simple-no-beads-final-audit.json), [A→B actual bytes/observed modes + command mapping](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/e7104fa0dcdcd121e66af860a14612262c5b0166/receipts/literal-b-simple-no-beads-A-B-runtime-binding.json), [actual worker](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/e7104fa0dcdcd121e66af860a14612262c5b0166/receipts/literal-b-simple-no-beads-worker-receipts.json), [same-session completion](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/e7104fa0dcdcd121e66af860a14612262c5b0166/receipts/literal-b-simple-no-beads-worker-resume-receipts.json).

В этом case первоначальный QA audit дал ложное memory mismatch: сравнивал установленный canonical LF с CRLF working-tree source. Проверка по реальным frozen Git blobs всех6 шаблонов показала exactmatch; [подробное доказательство oracle correction](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/e7104fa0dcdcd121e66af860a14612262c5b0166/receipts/literal-b-memory-oracle-correction.json). Исправлен только QA oracle; product/source/helper data не менялись, apply/helpers не повторялись. Исходный false audit сохранён отдельно. Рабочая Claude session возобновила только readback/commit/push на том же B, без A→B upgrade. Это не сокрытие ошибки продукта.

simple/bypass сейчас запущен один foregroundworker; complexauto/no-beads/bypass ещё не запускались. Далее только последовательно; при новом fail queue остановится для отчёта. R1 остаётся NOT RUN. HEAD будет сверяться перед каждым следующим case, новые PM comments проверяю в ходе пакета.

— Windows-QA (Codex GPT-6)
