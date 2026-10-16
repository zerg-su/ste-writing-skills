PYTHON ?= python3
LINT := $(PYTHON) skills/plain-talk/scripts/doc_lint.py

.PHONY: test lint-docs

test: lint-docs
	$(PYTHON) tests/test_doc_lint.py
	$(PYTHON) tests/test_skill_paths.py

lint-docs:
	$(LINT) README.md --pair README.ru.md
	$(LINT) README.ru.md --pair README.md
