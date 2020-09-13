.DEFAULT_GOAL := help

pytest_test_only="pytest --new-first --capture=sys"
pytest_reports="pytest --cov=. --cov-branch --cov-config=./setup.cfg --cov-report xml:./reports/coverage.xml --junitxml=./reports/tests.xml --cov-report html:reports/coverage_html_report"
pytest_func_cov="pytest --func_cov=pre_commit_hook"
pytest_debug="pytest --failed-first --pdb"
pytest_test_fail_fast="pytest --new-first --capture=sys --failed-first --showlocals"
pytest_10_slower="pytest --durations=10"
pytest_benchmark="pytest --benchmark-enable"
pytest_coverage="pytest --cov=. --cov-branch --cov-config=./setup.cfg"
pytest_coverage_html_report="pytest --cov=. --cov-branch --cov-config=./setup.cfg --cov-report html:reports/coverage_html_report"
documentation="sphinx-apidoc --follow-links --separate --module-first --ext-autodoc --ext-doctest --ext-intersphinx --ext-todo --ext-coverage --ext-mathjax --ext-viewcode --output-dir ./docs/source ./pre_commit_hook \
	&& sphinx-build --color -a -b html -j auto -c ./docs -d ./docs ./docs ./docs/build/html \
	&& sphinx-build --color -a -b changes -j auto -c ./docs -d ./docs ./docs ./docs/build/changes \
	&& sphinx-build --color -a -b coverage -j auto -c ./docs -d ./docs ./docs ./docs/build/coverage"
pylint="pylint --rcfile=./setup.cfg ./pre_commit_hook"
pylint_reports="pylint --rcfile=./setup.cfg --exit-zero --score=no --reports=no --msg-template=\"{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}\" ./pre_commit_hook | tee reports/pylint.txt"
flake8="flake8 --config=./setup.cfg ./pre_commit_hook"
mypy="mypy --config-file=./setup.cfg"

.PHONY: benchmark build clean coverage coverage-html-report documentation deploy down flake8 help install mypy pre-commit pylint pypi pypi-test quality tests tests-fail-fast tests-10-slower tests-debug tests-func-cov tests-reports

benchmark: ## Profile unit test
	@docker-compose run --rm pytest bash -c ${pytest_benchmark}
build: clean
	$(info Make: Build service ${service_name})
	@docker-compose build --compress --force-rm ${service_name}
clean:
	@docker-compose rm --force -v  ${service_name}
	@rm -rf *.egg-info build/ dist/ reports/ docs/{environment.pickle,build,source/**/*.doctree}  .mypy_cache .flake8.log
	@pyclean .
compile: build
	@docker-compose run --rm pytest bash -c "python setup.py bdist"
coverage: ## Run coverage => make coverage
	@docker-compose run --rm pytest bash -c ${pytest_coverage}
coverage-html-report: ## Run coverage html report => make coverage-html-report
	@docker-compose run --rm pytest bash -c ${pytest_coverage_html_report}
documentation: ## Build documentation => make documentation
	@docker-compose run --rm documentation bash -c ${documentation}
deploy: clean documentation build pypi pypi-test
	git push
down: ## Down project containers => make down
	$(info Make: Down)
	@docker-compose down
flake8: ## run flake8 => make flake8
	@docker-compose run --rm quality bash -c ${flake8}
generate_changelog: ## generate changelog
	@docker-compose run --rm generate_changelog bash -c generate-changelog
help: ## This help dialog. => make help
	@echo "Hello to the generate changelog Makefile\n"
	@IFS=$$'\n' ; \
	printf "%-30s %s\n" "target" "help" ; \
	printf "%-30s %s\n" "------" "----" ; \
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
mypy: ## Run mypy on code => make mypy
	@docker-compose run --rm quality bash -c ${mypy}
pre-commit: clean ## run localy precommit
	$(info Make: run pre-commit)
	@pip install --quiet pre-commit
	@pre-commit install-hooks
	@pre-commit autoupdate --bleeding-edge
	@pre-commit run --all-files --verbose
pylint: ## Run pylint on code => make pylint
	@docker-compose run --rm quality bash -c ${pylint}
pypi: build
	python3 -m twine upload dist/*
pypi-test: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
quality: ## run pylint, flake8, mypy, and tests => make quality
	@make -S pylint
	@make -S flake8
	@make -S mypy
	@make -S tests
tests:
	@docker-compose run --rm pytest bash -c ${pytes}
tests-fail-fast: ## Run tests and stop on first fail => make tests-fail-fast
	@docker-compose run --rm pytest bash -c ${pytest_test_fail_fast}
tests-10-slower: ## Run tests and display 10 slowers => make tests-10-slower
	@docker-compose run --rm pytest bash -c ${pytest_10_slower}
tests-debug: ## Run tests and launch pdb on first failed => make tests-debug
	@docker-compose run --rm pytest bash -c ${pytest_debug}
tests-func-cov: ## Run tests and display function cov => make tests-func-cov
	@docker-compose run --rm pytest bash -c ${pytest_func_cov}
tests-reports: ## Run tests and generate reports => make tests-reports
	@docker-compose run --rm pytest bash -c ${pytest_reports}
