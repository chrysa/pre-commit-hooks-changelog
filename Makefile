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

PYLINT_CMD := pylint --rcfile=./setup.cfg ./pre_commit_hook
PYLINT_REPORT_CMD := pylint --rcfile=./setup.cfg --exit-zero --score=no --reports=no \
	--msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" ./pre_commit_hook | tee reports/pylint.txt
FLAKE8_CMD := flake8 --config=./setup.cfg ./pre_commit_hook
MYPY_CMD   := mypy --config-file=./setup.cfg pre_commit_hook/

SPHINX_CMD := sphinx-apidoc --follow-links --separate --module-first \
	--ext-autodoc --ext-doctest --ext-intersphinx --ext-todo --ext-coverage \
	--ext-mathjax --ext-viewcode --output-dir ./docs/source ./pre_commit_hook \
	&& sphinx-build --color -a -b html -j auto -c ./docs -d ./docs ./docs ./docs/build/html \
	&& sphinx-build --color -a -b changes -j auto -c ./docs -d ./docs ./docs ./docs/build/changes \
	&& sphinx-build --color -a -b coverage -j auto -c ./docs -d ./docs ./docs ./docs/build/coverage

# ─── Phony targets ────────────────────────────────────────────────────────────

.PHONY: benchmark build clean compile coverage coverage-html-report \
	deploy deploy-test documentation down flake8 generate-changelog \
	help install mypy pre-commit pylint pypi pypi-test quality \
	tests tests-debug tests-fail-fast tests-func-cov tests-reports tests-10-slower

# ─── Help ─────────────────────────────────────────────────────────────────────

help: ## Afficher cette aide
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

clean: ## Supprimer les artefacts générés (build, dist, cache)
	@rm -rf *.egg-info build/ dist/ reports/ .mypy_cache .flake8.log .coverage coverage.xml
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

build: clean ## Builder les images Docker (sans cache)
	@docker compose build --no-cache

compile: build ## Compiler le package Python (bdist)
	@docker compose run --rm pytest bash -c "python -m build"

install: ## Installer les dépendances de développement
	@pip install -e ".[tests,flake8,mypy,pylint,pre_commit]"

down: ## Arrêter et supprimer les conteneurs Docker
	@docker compose down

# ─── Tests ────────────────────────────────────────────────────────────────────

tests: ## Lancer les tests unitaires
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_ONLY)"

tests-fail-fast: ## Tests — arrêter au premier échec
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_FF)"

tests-debug: ## Tests — lancer pdb au premier échec
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_DEBUG)"

tests-10-slower: ## Tests — afficher les 10 tests les plus lents
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_SLOW)"

tests-func-cov: ## Tests — afficher la couverture par fonction
	@docker compose run --rm pytest bash -c "$(PYTEST) --func_cov=pre_commit_hook"

tests-reports: ## Tests — générer les rapports XML / HTML
	@mkdir -p reports
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_REPORTS)"

benchmark: ## Profiler les tests unitaires (benchmark)
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_BENCH)"

# ─── Coverage ─────────────────────────────────────────────────────────────────

coverage: ## Lancer la couverture de code
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_COV)"

coverage-html-report: ## Générer le rapport de couverture HTML
	@mkdir -p reports
	@docker compose run --rm pytest bash -c "$(PYTEST) $(PYTEST_OPTS_COV_HTML)"

# ─── Qualité ──────────────────────────────────────────────────────────────────

flake8: ## Linter flake8
	@docker compose run --rm quality bash -c "$(FLAKE8_CMD)"

pylint: ## Linter pylint
	@docker compose run --rm quality bash -c "$(PYLINT_CMD)"

mypy: ## Vérification des types mypy
	@docker compose run --rm quality bash -c "$(MYPY_CMD)"

quality: flake8 pylint mypy tests ## Lancer tous les linters + tests

# ─── Documentation ────────────────────────────────────────────────────────────

documentation: ## Générer la documentation Sphinx
	@docker compose run --rm documentation bash -c "$(SPHINX_CMD)"

# ─── Changelog ────────────────────────────────────────────────────────────────

generate-changelog: ## Générer le changelog depuis le dossier changelog/
	@docker compose run --rm generate_changelog bash -c generate-changelog

# ─── Pre-commit ───────────────────────────────────────────────────────────────

pre-commit: ## Installer et exécuter pre-commit sur tous les fichiers
	@pip install --quiet pre-commit
	@pre-commit install
	@pre-commit autoupdate
	@pre-commit run --all-files --verbose

# ─── Publication PyPI ─────────────────────────────────────────────────────────

pypi: compile ## Publier sur PyPI
	@python3 -m twine upload dist/*

pypi-test: compile ## Publier sur TestPyPI
	@python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy: clean pypi pypi-test ## Builder, publier sur PyPI et TestPyPI
