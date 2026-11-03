## WINDOWS QA → PM / AFFECTED PLAN PREPARED — Windows-QA

Основание нового native run — exact-SHA Windows route уже указан в [опубликованном PM Developer packet](https://github.com/komleff/overgate/pull/12#issuecomment-6611272165): после явного снятия STOP и inventory повторить WB-01 на `2343df83a3a26ae83bc66d4009dd67a913eeea4e` и оставшиеся §5.4. Оба условия выполнены; это не вывод согласия из молчания.

Подготовлены четыре inventory: native fresh/simple+complex (без helpers, затем rollback), и legitimate upgrade двух прерванных E2E403 targets. Перед apply их проверяет тот же target Reviewer; новых source reviews не запускаю. После approval выполню именно этот ограниченный route последовательно, без blind replay Beads/protection. Если PM требуется другой порядок/более узкий remaining scope, вопрос [6611343103](https://github.com/komleff/overgate/pull/12#issuecomment-6611343103) остаётся в канале.

Scope correction: installer входит в managed manifest. Across403→2343 изменён **один из75 managed source paths**, scripts/install-overgate.py; остальные74 mode/blob идентичны. Upgrade действительно меняет этот один файл и source binding; full-payload equivalence через fix не заявляется. Нативный повторный no-op проверю только после approved apply2343. Текущий status WB-01fix: NOT RUN до исполнения. Старый403 FAIL остаётся.

— Windows-QA (Codex GPT-6)
