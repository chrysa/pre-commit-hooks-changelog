#!make
ifneq (,$(findstring n,$(firstword -$(MAKEFLAGS))))
    DRY_RUN := 1
endif

.DEFAULT_GOAL := help

# ─── Variables ────────────────────────────────────────────────────────────────

PYTEST            := pytest
PYTEST_OPTS_ONLY  := --new-first --capture=sys
PYTEST_OPTS_FF    := --new-first --capture=sys --failed-first --showlocals
PYTEST_OPTS_DEBUG := --failed-first --pdb
PYTEST_OPTS_SLOW  := --durations=10
PYTEST_OPTS_BENCH := --benchmark-enable
PYTEST_OPTS_COV   := --cov=pre_commit_hook --cov-branch --cov-config=./setup.cfg
PYTEST_OPTS_COV_HTML := $(PYTEST_OPTS_COV) --cov-report html:reports/coverage_html_report
PYTEST_OPTS_REPORTS  := $(PYTEST_OPTS_COV) --cov-report xml:./reports/coverage.xml --junitxml=./reports/tests.xml --cov-report html:reports/coverage_html_report

RUFF_CMD        := ruff check ./pre_commit_hook
RUFF_FMT_CMD    := ruff format --check ./pre_commit_hook
MYPY_CMD        := mypy --config-file=./setup.cfg pre_commit_hook/

SPHINX_CMD := sphinx-apidoc --follow-links --separate --module-first \
	--ext-autodoc --ext-doctest --ext-intersphinx --ext-todo --ext-coverage \
	--ext-mathjax --ext-viewcode --output-dir ./docs/source ./pre_commit_hook \
	&& sphinx-build --color -a -b html -j auto -c ./docs -d ./docs ./docs ./docs/build/html \
	&& sphinx-build --color -a -b changes -j auto -c ./docs -d ./docs ./docs ./docs/build/changes \
	&& sphinx-build --color -a -b coverage -j auto -c ./docs -d ./docs ./docs ./docs/build/coverage

# ─── Phony targets ────────────────────────────────────────────────────────────

.PHONY: benchmark build clean compile coverage coverage-html-report \
	deploy deploy-test documentation down ruff ruff-format generate-changelog \
	help install mypy pre-commit pypi pypi-test quality \
	tests tests-debug tests-fail-fast tests-func-cov tests-reports tests-10-slower

# ─── Help ─────────────────────────────────────────────────────────────────────

help: ## Show this help
	@echo "==================================================================="
	@echo "            pre-commit-hooks-changelog — Makefile help"
	@echo "==================================================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "==================================================================="

# ─── Build & Clean ────────────────────────────────────────────────────────────

clean: ## Remove generated artifacts (build, dist, cache)
	@rm -rf *.egg-info build/ dist/ reports/ .mypy_cache .coverage coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean ## Build Docker images (no cache)
	@docker compose build --no-cache

compile: build ## Compile Python package (bdist)
	@docker compose run --rm pytest bash -c "python -m build"

install: ## Install development dependencies
	@pip install -e ".[tests,ruff,mypy,pre_commit]"

down: ## Stop and remove Docker containers
	@docker compose down

# ─── Tests ────────────────────────────────────────────────────────────────────

tests: ## Run unit tests
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_ONLY)"

tests-fail-fast: ## Tests — stop at first failure
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_FF)"

tests-debug: ## Tests — drop into pdb on first failure
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_DEBUG)"

tests-10-slower: ## Tests — display the 10 slowest tests
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_SLOW)"

tests-func-cov: ## Tests — show per-function coverage
	@docker compose run --rm pytest bash -c "$(PYTEST) --func_cov=pre_commit_hook"

tests-reports: ## Tests — generate XML / HTML reports
	@mkdir -p reports
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_REPORTS)"

benchmark: ## Profile unit tests (benchmark)
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_BENCH)"

# ─── Coverage ─────────────────────────────────────────────────────────────────

coverage: ## Run code coverage
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_COV)"

coverage-html-report: ## Generate HTML coverage report
	@mkdir -p reports
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_COV_HTML)"

# ─── Quality ──────────────────────────────────────────────────────────────

ruff: ## Run ruff linter (lint + import sort + style)
	@docker compose run --rm quality bash -c "$(RUFF_CMD)"

ruff-format: ## Check ruff formatting
	@docker compose run --rm quality bash -c "$(RUFF_FMT_CMD)"

mypy: ## Run mypy type check
	@docker compose run --rm quality bash -c "$(MYPY_CMD)"

quality: ruff ruff-format mypy tests ## Run all linters + tests

# ─── Documentation ────────────────────────────────────────────────────────────

documentation: ## Build Sphinx documentation
	@docker compose run --rm documentation bash -c "$(SPHINX_CMD)"

# ─── Changelog ────────────────────────────────────────────────────────────────

generate-changelog: ## Generate changelog from changelog/ folder
	@docker compose run --rm generate_changelog bash -c generate-changelog

# ─── Pre-commit ───────────────────────────────────────────────────────────────

pre-commit: ## Install and run pre-commit on all files
	@pip install --quiet pre-commit
	@pre-commit install
	@pre-commit run --all-files --verbose

# ─── PyPI publish ─────────────────────────────────────────────────────────

pypi: compile ## Publish to PyPI
	@python3 -m twine upload dist/*

pypi-test: compile ## Publish to TestPyPI
	@python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy: clean pypi pypi-test ## Build, publish to PyPI and TestPyPI
