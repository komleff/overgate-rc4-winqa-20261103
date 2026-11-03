import sys,json
from datetime import datetime,timezone,timedelta
from prepare import B,E,run
S=B/'source-2343df8';A='403f95b8a7fae50957a99c16a211a8ef7217cb22';F='2343df83a3a26ae83bc66d4009dd67a913eeea4e';ART='cbf667d39eb71c0c212a17cd0233e8178f4868bc'
BASE='https://github.com/komleff/overgate-rc4-winqa-20261103/blob/'+ART+'/receipts/'
def link(file,label='receipt'):return '['+label+']('+BASE+file+')'
def main():
 readback=json.loads((E/'final-e2e-readback.json').read_text(encoding='utf-8'));assert len(readback)==2 and all(x['result']=='PASS' for x in readback)
 fp=(E/'fixed-content-fingerprint.txt').read_text().strip();oldfp=(E/'content-fingerprint.txt').read_text().strip()
 stamp=datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
 body=f'''## WINDOWS QA → PM / FINAL QA EXECUTION — Windows-QA

**Role/model:** Windows QA / Codex GPT-6, точный preset не предоставлен. Actual runtime: Claude Code **2.1.317**, init model **claude-fable-5-1**; effective `auto` / `bypassPermissions` взяты из runtime init, interactive UI показал auto. Время отчёта: {stamp}, Asia/Novosibirsk UTC+07:00.

**Итог:** WB-01 на новом source **PASS** для физического Windows fresh/upgrade/no-op и отрицательных controls. Выполненные live/scoped cases ниже — PASS. **Whole fresh literal установка целиком с final source2343 — NOT RUN**: фактическая история двух E2E targets — fresh403 → операторский STOP → independently approved upgrade2343 → actual auto completion. Не выдаю эту историю за непрерывный fresh2343 и не объявляю приёмку всех AC или release readiness.

**Source A:** `{A}` — первоначальный frozen packet6610035146; исторический WB-01 остаётся **FAIL**. **Source B:** `{F}` — опубликованный PM [Developer exact-SHA fix/Windows route](https://github.com/komleff/overgate/pull/12#issuecomment-6611272165), [source scoped review](https://github.com/komleff/overgate/pull/12#issuecomment-6611315986). STOP снят оператором; inventory выполнен до нового apply. [Binding A→de55285](https://github.com/komleff/overgate/pull/12#issuecomment-6610737247) не используется как whole-payload binding через B: между A/B изменён managed installer, остальные74 из75 manifest source paths mode/blob-identical — {link('fix-payload-binding.json','exact path binding')}. Последний read PR HEAD = B; старые запуски не переименованы.

**Окружение:** Windows11Pro 10.0.26200/build26200; Git2.51.2.windows.1; native Git Bash5.2.37 x86_64-msys; `py -3` Python3.14.0; gh2.85.0; jq1.8.2; Node24.11.0; portable bd1.2.2(6c124203e), официальный release checksum проверен. Начальный global bd0.62 не использовался для БД QA. Начальный Claude2.1.139 дал model400; отдельный QA install2.1.317 решил transport mismatch. До этого OAuth401 устранён нормальным CLI login оператором. Это prerequisites, не доказательство unavailable-auto behavior. Установленный Codex CLI0.154.0 — inventory, его native activation в этой QA не тестировалась.

Только новые disposable roots/репозитории. Рабочие U2 и `D:/GitHub/overgate` не изменялись; последний status рабочего OverGate совпадает с исходным (unborn main, untracked README/docs/overgate-docs). Источник B clean в `D:/CodexArtifacts/overgate-rc4-winqa-20261103/source-2343df8`. После снятия перегрузки — последовательное выполнение, без параллельных Claude/Beads jobs; сейчас task-path QA processes не осталось.

| §5.4 / ожидание | Source / Result | Наблюдаемый факт | Evidence |
|---|---|---|---|
| 1 — clone exact SHA, clean | A и B / PASS | отдельные clean detached source clones, exact40hex | {link('source-final-clean.txt','A cleanliness')}; B HEAD/clean проверен перед публикацией |
| 2 — fresh/default auto, helpers, checker, Memory/BD/protection | A→B / PASS **только для описанного маршрута** | два literal QUICKSTART actual-auto старта; независимые планы до apply; Memory→BD→protection реально выполнены на A; после STOP — approved B upgrade без helper replay; final checker0, project verifier0, state exact B/auto/`beads is True`, no-op73/73equal | {link('e2e-simple-phase-a-receipts.json','simple phaseA')}, {link('e2e-simple-phase-b-receipts.json','phaseB')}, {link('e2e-simple-phase-c-receipts.json','phaseC')}; {link('e2e-complex-phase-a-receipts.json','complex A')}, {link('e2e-complex-phase-b-receipts.json','B')}, {link('e2e-complex-phase-c-receipts.json','C')}; {link('final-e2e-readback.json','independent final readback')} |
| 2 — first export на сложном пути в независимый empty remote | A / PASS | новый complex test repo без backup до bootstrap; реальный первый export `4df707803cf9621d5244b646ed2591eb2b4ae504`; simple first export `1cd7342be843f3309cdeef93d274915b91125d45` | phaseB tool receipts + final readback выше |
| 2 — whole uninterrupted literal fresh непосредственно B | B / NOT RUN | current-source physical fresh-controller checks отдельно PASS; whole Claude install B from empty target не выполнялся | {link('fix-simple-fresh-results.json','B native fresh simple')}, {link('fix-complex-fresh-results.json','complex')} |
| 3 — actual root startup / normal trust / hooks | A и B scopes / PASS | normal interactive Yes trust на обоих типах пути, CLI2.1.317/auto indicator; actual PreToolUse denials подтверждают исполнение hooks, не только settings | {link('e2e-simple-interactive-trust-start.txt','simple prompt')}, {link('e2e-simple-interactive-trust-accepted.txt','accepted/auto')}; {link('e2e-complex-interactive-trust-start.txt','complex prompt')}, {link('e2e-complex-interactive-trust-accepted.txt','accepted/auto')}; six runtime receipts в matrix |
| 4 — файл/commit/branch push/Draft PR без вопросов | A six modes + B auto E2E / PASS | реальные tool calls, commits и remote ref/PR SHA; final trees/index clean | {link('completed-403-matrix.json','six-case matrix')}; {link('final-e2e-readback.json','B final refs')} |
| 5 — native hook rejects main push / PR merge / positive declaration | A six runtime combinations / PASS | все три intercepted PreToolUse до исполнения, не model refusal/sandbox error; B hooks unchanged — только component reuse, не новый six-case runB | matrix + sanitized runtime receipts |
| 5 — real GitHub server rejects distinct new main update | A / PASS | отдельный native terminal в disposable clone, no hook/protection overrides; GH006; main unchanged | {link('server-main-rejected-push.txt','full Git stderr')}, {link('server-rejection-results.json','ref/protection binding')} |
| 6 — commit при красном project verifier | A six runtime combinations / PASS | intentional red реально исполнялся test hook, commit blocked; затем exact verifier restored, green check и HEAD/index сохранены | matrix negative tool IDs + six live receipts |
| 7 — no-beads / bypass, обоих path classes | A / PASS **для native fresh + actual post-install4/5** | no-beads: компоненты/БД отсутствуют, Memory6; bypass actual init `bypassPermissions`; те же hook denials | matrix + each native-results/live-receipts |
| 7 — whole literal Claude fresh установщик для no-beads/bypass с B | B / NOT RUN | не заявляется по чтению config или старому A runtime | explicit limit |
| 8 — immediate apply/rollback до helpers | A и B / PASS | managed/settings/install-state before bytes восстановлены; B также observed modes, state absent; no database/context/protection rollback | {link('simple-rollback-native-results.json','A simple')}, {link('complex-rollback-native-results.json','A complex')}; B fresh receipts |
| WB-01 / AC04 — immediate second plan | A / FAIL; B / PASS | A:73(65 no-beads) mode-only mismatches,0 byte mismatches. B fresh+upgrade both paths:73equal, conflicts0 | {link('noop-minimal-results.json','A minimum repro')}; {link('fix-simple-fresh-results.json','B fresh')}, {link('fix-simple-upgrade-results.json','B upgrade')}, {link('fix-complex-fresh-results.json','complex fresh')}, {link('fix-complex-upgrade-results.json','upgrade')} |
| WB-01 safety controls | B / PASS | changed managed bytes produce addressed conflict/no writes; stale approved plan apply exits1 before backup/write; controlled bytes exact restored; immediate rollback exact | B fresh receipts + corresponding changed/stale command logs |

**Final B E2E target binding:**

| Target / path | Target HEAD = remote = Draft PR head | First backup SHA |
|---|---|---|
| [simple PR1](https://github.com/komleff/overgate-rc4-e2e-simple-20261104/pull/1), `C:/work/overgate-e2e-auto` | `5d58b5a8f573e56f2496982c75dcd2afe72d3678` | `1cd7342be843f3309cdeef93d274915b91125d45` |
| [complex PR1](https://github.com/komleff/overgate-rc4-e2e-complex-20261104/pull/1), `C:/Users/komle/Мои проекты/overgate e2e auto` | `95222cc9ecbb33fc4a96d9868b989ec033e242d7` | `4df707803cf9621d5244b646ed2591eb2b4ae504` |

Первоначальные `C:/work/demo` / `C:/Users/komle/Мои проекты/demo app` и variants — repo `komleff/overgate-rc4-winqa-20261103`, exact source A и полные target SHAs в {link('completed-403-matrix.json','matrix')}. Общий backup этого первого repo не выдан за независимый first export later targets; пробел закрыт двумя отдельными E2E remotes выше. B fresh rollback fixture HEADs: simple `529a6313d30d55bb2a6531a1a2e08cb8b9d3340d`, complex `c5601caf36fc6ddace4b51256971b94378958065`.

Server probe repo: `komleff/overgate-rc4-winqa-20261103`; local new clone `D:/CodexArtifacts/overgate-rc4-winqa-20261103/server-probe`; source branch `qa/server-rejection-probe`; candidate `e74242c0cc8b2aed37a51739df872c0d1af21e7b`; attempted refspec `HEAD:refs/heads/main`; actual remote GH006/exit1. Before/after main `bd7fda1576137a2adf0dbbd4b611c9b1be96c21f`; enforce_admins=true, PR required. Никаких force/no-verify/hooksPath или снятия protection.

**Limits / наблюдения:**

- Case history разделена по A/B, включая aborted phaseB. Raw subagent summary `head_before` иногда использовал planning/remote ancestor; authoritative before HEAD взят из resume inventory (`1f48658ddb88ae43fe91e40c7a0bdcd102642cfb` / `f5a7df7b0186f98182043a38d35205f7e009ebb2`), final — из независимого readback.
- Были incidental parser denials на `od|tail`, compound/quoted editing commands; installer agents затем применили простые разрешённые формы. Логи сохранены; не заявляю отсутствие любых routine denials. Явный deny `git checkout -- *` в source объясняет restoration permission denial; это не доказанный auto-classifier R6. Protective code/settings не отключались. Первые drafts project verifier имели quoting SyntaxError и были исправлены агентами до successful checks/commit; source code QA не менял.
- QA harness первоначально ошибочно требовал nonzero от `plan` при conflict. API намеренно возвращает0 и `conflicts=1`; проверка исправлена на addressed conflict/no writes и дополнительно подтверждена managed ADR probe. Audit annotations сохранены, это не product FAIL и не ослабление contract.
- NOT RUN этим Windows QA: whole uninterrupted fresh literal B (включая mode variants), forced unavailable-auto/fallback-account scenario, native Windows Codex activation, full reference suite/exact-HEAD CI, Unix mode enforcement. CI/source Review имеют отдельные receipts PM; не подменяю ими physical QA и наоборот. AC05/06/13 и overall acceptance остаются решением PM по точному coverage, не выводом из scoped PASS.

**Evidence integrity:** [immutable bundle](https://github.com/komleff/overgate-rc4-winqa-20261103/tree/{ART}); [SHA256 map](https://github.com/komleff/overgate-rc4-winqa-20261103/blob/{ART}/SHA256SUMS.json). Проверены587/587 published files против Git archive,0 mismatch/0missing. Только factual runtime init/tool calls/results/final report; raw thinking, OAuth flow и credentials не публиковались. Exact inventory/VC/verdict comments опубликованы перед каждым apply, same target Reviewer, без нового source-review launch.

**Tested source content binding:** explicit78-path set + exact §5.4 contract, не whole PR package. B Content-Fingerprint `{fp}` — {link('fixed-tested-paths-and-blobs.txt','paths/blobs')}, {link('fixed-source-contract-section5.4.md','contract input')}. Historical A fingerprint `{oldfp}` сохранён отдельно. Это binding исполненных компонентов, не утверждение semantic review всех78 paths.

Ни merge, ни release, ни finalization не выполнялись. Source/local result передан PM; дальнейший повтор только по новому определённому affected scope. Новых фоновых QA jobs нет.

— Windows-QA (Codex GPT-6)
'''
 (E/'final-qa-report.md').write_text(body,encoding='utf-8')
 p=run([sys.executable,S/'.claude/tools/publish-pr-comment.py','12','-'],S,label='source-final-qa-publish',input=body)
 print(p.stdout)
if __name__=='__main__':main()
