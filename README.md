# STE Writing Skills

[Русская версия](README.ru.md)

Two agent skills for plain technical writing in Claude Code and Codex. The
target is about 80 % of ASD-STE100 Simplified Technical English.

| Skill | What it does |
|---|---|
| `plain-talk` | Rewrites, explains or audits text. Removes AI filler: banned words, empty phrases and 16 typical patterns |
| `tech-doc` | Writes or audits a runbook, README or how-to. Each command has a source or the mark `(unverified)` |

Both skills use one rule file and one linter. The linter needs Python 3.9 or
later and no packages.

## Install

### Claude Code

```bash
claude plugin marketplace add zerg-su/ste-writing-skills
claude plugin install ste-writing-skills@ste-writing-skills
```

Expected: `claude plugin list` shows `ste-writing-skills@ste-writing-skills`
with the status `enabled`. Start a new session to load the skills.

### Codex

```bash
codex plugin marketplace add zerg-su/ste-writing-skills
codex plugin add ste-writing-skills@ste-writing-skills
```

Expected: `codex plugin list` shows the plugin as `installed, enabled`. Start
a new thread to load the skills.

### Without a plugin

Copy both skill directories. `tech-doc` reads the rules and the linter from
`plain-talk`.

```bash
git clone https://github.com/zerg-su/ste-writing-skills.git
mkdir -p ~/.claude/skills
cp -R ste-writing-skills/skills/plain-talk ste-writing-skills/skills/tech-doc ~/.claude/skills/
```

## Use

| Task | Claude Code | Codex |
|---|---|---|
| Rewrite a text | `/ste-writing-skills:plain-talk rewrite <text>` | `$ste-writing-skills:plain-talk rewrite <text>` |
| Find AI filler, change nothing | `/ste-writing-skills:plain-talk audit <text>` | `$ste-writing-skills:plain-talk audit <text>` |
| Write a runbook | `/ste-writing-skills:tech-doc write <topic>` | `$ste-writing-skills:tech-doc write <topic>` |
| Check a README | `/ste-writing-skills:tech-doc audit README.md` | `$ste-writing-skills:tech-doc audit README.md` |

The table shows the names after a plugin install. After a copy without a
plugin, the Claude Code names are `/plain-talk` and `/tech-doc`.

The agent can also select a skill from the request text, for example
"explain this in plain words" or "write a runbook".

`plain-talk` has three modes: `explain`, `rewrite` and `audit`. After
`rewrite` it lists "What changed" in 5 items or fewer. `audit` gives findings
in the form quote → rule → fix.

`tech-doc` has two modes: `write` and `audit`. It selects one of three
document types: usage, operations manual or explanation. Each step that
changes state has "Expected:". A step where failure is realistic also has
"If not:". The final report lists the unverified facts and the lint result.

## Apply the style to every reply

The skills run on request. To apply the rules to every reply, copy
`skills/plain-talk/references/plain-style.md` to `docs/plain-style.md` in the
project. Then add this line to `CLAUDE.md` or `AGENTS.md`:

```markdown
- Reply style: follow docs/plain-style.md. Strict rewrite: /ste-writing-skills:plain-talk.
```

## Lint from the command line

```bash
python3 skills/plain-talk/scripts/doc_lint.py README.md
python3 skills/plain-talk/scripts/doc_lint.py README.md --pair README.ru.md
python3 skills/plain-talk/scripts/doc_lint.py README.md --json
```

| Exit code | Meaning |
|---|---|
| `0` | No errors |
| `1` | Errors found |
| `2` | Usage error, file error or style file error |

Options: `--max-words` (default 25, error), `--warn-words` (default 20,
warning), `--style <file>`. The linter cannot tell an instruction from a
description. A clean result does not prove that the text is clear.

## Change the rules

`plain-style.md` is the single source of the rules. The linter reads the word
lists from its `text lint:*` blocks. Edit a block, then run `make test`.

| File | Contents |
|---|---|
| `skills/plain-talk/references/plain-style.md` | Sentence and word rules, word lists, patterns |
| `skills/plain-talk/scripts/doc_lint.py` | Linter |
| `skills/tech-doc/references/doc-structure.md` | Document types, section order, procedure template |

## Development

```bash
make test
```

Expected: the output ends with `All skill path tests passed.`

## License

MIT, see `LICENSE`. Third-party notices are in `THIRD_PARTY_NOTICES.md`.
