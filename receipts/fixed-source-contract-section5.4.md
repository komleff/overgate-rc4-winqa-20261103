### 5.4 Чек-лист живой проверки на Windows (оператор, og-9ic.4)

Окружение: основной Windows-ПК разработки оператора, Git for Windows (Git Bash), Python через
`py -3`, Claude Code, `bd`. Новые тестовые проекты в отдельных каталогах: `C:\work\demo` и путь с
пробелом и кириллицей `C:\Users\<user>\Мои проекты\demo app`; для защиты main — отдельный тестовый
репозиторий на GitHub. Рабочие checkout U2 и OverGate не затрагиваются. Проверка идёт на финальном
candidate SHA после Code Review.

| Шаг | Действие | Ожидание |
|---|---|---|
| 1 | `git clone` OverGate, checkout candidate SHA | чистое дерево |
| 2 | В режиме `auto` поручить агенту установку фразой из QUICKSTART | без вопросов к оператору; режим `auto`, conflicts 0; `check-reference` PASS; Memory Bank создан; Beads инициализирован, есть `beads-backup`; защита main включена или записано, почему нет; при коде 4 в `.memory-bank/` шесть файлов и строка R8 |
| 3 | Claude Code из корня проекта | подтверждение загрузки хуков |
| 4 | Попросить агента создать файл, закоммитить в рабочую ветку, запушить и открыть PR | всё без вопросов к оператору |
| 5 | `git push origin main`, `gh pr merge 1`, `gh pr comment 1 --body "ready to merge"` | все три заблокированы хуком; на GitHub прямой push в main отклонён защитой |
| 6 | `git commit` при красных тестах в `verify.sh` | блок |
| 7 | Повторить шаги 2, 4, 5 для `--no-beads` и `--mode bypass` | Beads-набора нет, Memory Bank есть; в bypass те же блокировки |
| 8 | Отдельный тестовый проект: `apply` без helpers и правок, затем `rollback` | managed-байты, settings и install-state как до установки |

Evidence в PR WI-1: таблица «шаг | ожидание | факт | лог или скриншот», версии Windows, Git,
Python, Claude Code и bd, путь проекта. Случаи восстановления og-7sr проверяются в плане WI-2.
