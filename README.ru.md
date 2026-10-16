# STE Writing Skills

[English version](README.md)

Два скилла для простого технического текста в Claude Code и Codex. Цель —
около 80 % стандарта ASD-STE100 Simplified Technical English.

STE остаётся основой для обоих языков. Для русских фрагментов дополнительно
применяются требования к изложению из ГОСТ Р 2.105-2019, пункты 5.2.2–5.2.3.
Область применения и исключения для терминов указаны в
[общих правилах стиля](skills/plain-talk/references/plain-style.md#2-words).

| Скилл | Что делает |
|---|---|
| `plain-talk` | Переписывает, объясняет или проверяет текст. Убирает AI-слоп: запрещённые слова, пустые фразы и 16 типовых шаблонов |
| `tech-doc` | Пишет или проверяет runbook, README или how-to. У каждой команды есть источник или пометка `(unverified)` |

Оба скилла используют один файл правил и один линтер. Линтеру нужен Python
3.9 или новее, пакеты не нужны.

## Установка

### Claude Code

```bash
claude plugin marketplace add zerg-su/ste-writing-skills
claude plugin install ste-writing-skills@ste-writing-skills
```

Ожидаемо: `claude plugin list` показывает `ste-writing-skills@ste-writing-skills`
со статусом `enabled`. Открыть новую сессию, чтобы скиллы загрузились.

### Codex

```bash
codex plugin marketplace add zerg-su/ste-writing-skills
codex plugin add ste-writing-skills@ste-writing-skills
```

Ожидаемо: `codex plugin list` показывает плагин как `installed, enabled`.
Открыть новый тред, чтобы скиллы загрузились.

### Без плагина

Скопировать оба каталога скиллов. `tech-doc` берёт правила и линтер из
`plain-talk`.

```bash
git clone https://github.com/zerg-su/ste-writing-skills.git
mkdir -p ~/.claude/skills
cp -R ste-writing-skills/skills/plain-talk ste-writing-skills/skills/tech-doc ~/.claude/skills/
```

## Использование

| Задача | Claude Code | Codex |
|---|---|---|
| Переписать текст | `/ste-writing-skills:plain-talk rewrite <текст>` | `$ste-writing-skills:plain-talk rewrite <текст>` |
| Найти AI-слоп без правок | `/ste-writing-skills:plain-talk audit <текст>` | `$ste-writing-skills:plain-talk audit <текст>` |
| Написать runbook | `/ste-writing-skills:tech-doc write <тема>` | `$ste-writing-skills:tech-doc write <тема>` |
| Проверить README | `/ste-writing-skills:tech-doc audit README.md` | `$ste-writing-skills:tech-doc audit README.md` |

В таблице — имена после установки плагина. После копирования без плагина
имена в Claude Code — `/plain-talk` и `/tech-doc`.

Агент выбирает скилл и по тексту запроса, например «объясни проще» или
«напиши ранбук».

У `plain-talk` три режима: `explain`, `rewrite` и `audit`. После `rewrite`
скилл даёт список «Что изменилось», до 5 пунктов. `audit` выдаёт находки в
форме цитата → правило → исправление.

У `tech-doc` два режима: `write` и `audit`. Скилл выбирает один из трёх типов
документа: usage, operations manual или explanation. У каждого шага, который
меняет состояние, есть «Expected:». У шага с реальным риском отказа есть ещё
«If not:». В итоговом отчёте — непроверенные факты и результат линтера.

## Стиль для каждого ответа

Скиллы работают по запросу. Чтобы правила действовали в каждом ответе,
скопировать `skills/plain-talk/references/plain-style.md` в
`docs/plain-style.md` проекта. Затем добавить эту строку в `CLAUDE.md` или
`AGENTS.md`:

```markdown
- Reply style: follow docs/plain-style.md. Strict rewrite: /ste-writing-skills:plain-talk.
```

## Линтер из командной строки

```bash
python3 skills/plain-talk/scripts/doc_lint.py README.md
python3 skills/plain-talk/scripts/doc_lint.py README.md --pair README.ru.md
python3 skills/plain-talk/scripts/doc_lint.py README.md --json
```

| Код выхода | Значение |
|---|---|
| `0` | Ошибок нет |
| `1` | Есть ошибки |
| `2` | Ошибка аргументов, файла или файла правил |

Опции: `--max-words` (по умолчанию 25, ошибка), `--warn-words` (по умолчанию
20, предупреждение), `--style <file>`. Линтер не отличает инструкцию от
описания. Чистый результат не доказывает, что текст понятен.

## Изменение правил

`plain-style.md` — единственный источник правил. Линтер читает списки слов
из его блоков `text lint:*`. Изменить блок, затем запустить `make test`.

| Файл | Содержимое |
|---|---|
| `skills/plain-talk/references/plain-style.md` | Правила предложений и слов, списки слов, шаблоны |
| `skills/plain-talk/scripts/doc_lint.py` | Линтер |
| `skills/tech-doc/references/doc-structure.md` | Типы документов, порядок разделов, шаблон процедуры |

## Разработка

```bash
make test
```

Ожидаемо: вывод заканчивается строкой `All skill path tests passed.`

## Лицензия

MIT, см. `LICENSE`. Уведомления о сторонних работах — в
`THIRD_PARTY_NOTICES.md`.
