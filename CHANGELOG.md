# Changelog

## Unreleased

- Both skills: add GOST R 2.105-2019 wording guidance for Russian passages
  only, on top of the STE baseline. Project terminology and chat register
  keep their defined scope.

## 1.0.1 — 2026-10-16

- `doc_lint.py`: a table cell with an ID and other words now needs a gloss.
  Only IDs and the words "then", "and", "or" (also "затем", "потом", "и",
  "или") are exempt.
- `doc_lint.py`: empty parentheses after an ID are not a gloss.
- `doc_lint.py`: fences of four or more backticks and tilde fences keep their
  language, so `--pair` compares their commands. A shorter fence inside a
  longer fence does not close it.
- README: names of the skills after a manual copy.

## 1.0.0 — 2026-10-16

- `plain-talk`: rewrite, explain or audit text in plain technical style.
- `tech-doc`: write or audit runbooks, READMEs and how-to guides with
  verified commands.
- `doc_lint.py`: checks sentence length, semicolons, word lists, references
  without a gloss and EN/RU pair parity.
- Plugin manifests for Claude Code and Codex.
