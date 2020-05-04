# badges

|    GENERAL    |
|---|---|---|---|
|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/chrysa/pre-commit-hooks-changelog/graphs/commit-activity)|[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)|[![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/)|[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)|
|[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/chrysa/pre-commit-hooks-changelog/releases/)|[![PyPI download day](https://img.shields.io/pypi/dd/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|

|     CI STATUS    |
|------------------|
| master | develop |
|:------:|:-------:|
| ![.github/workflows/pythonpackage.yml](https://github.com/chrysa/pre-commit-hooks-changelog/workflows/.github/workflows/pythonpackage.yml/badge.svg?branch=master) | ![.github/workflows/pythonpackage.yml](https://github.com/chrysa/pre-commit-hooks-changelog/workflows/.github/workflows/pythonpackage.yml/badge.svg?branch=develop) |

[Changelog](changelog.md)

## pre-commit-hooks-changelog

generate a markdown changelog from folder of yaml files

### Using pre-commit-hooks-changelog with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/chrysa/pre-commit-hooks-changelog
        rev: v0.2.0  # Use the ref you want to point at
        hooks:
        -   id: generate-changelog

### Options

|   |   |
|---|---|
| `--output-file` | define changelog outpout |
| `--changelog-folder` | source folder of changelogs |
| `--rebuild` | rebuild changelog see below |

#### Rebuild options

|   |   |
|---|---|
| `all` | rebuild changelog from scratch |
| `versions` | rebuild changelog for each version |
| `latest` | rebuild latest changelog |
| `home` | rebuild changelog file on repo root |

### Standalone

`pip install pre-commit-hooks-changelog`

<!-- START makefile-doc -->
```
$ make help
Hello to the generate changelog Makefile

target                         help
------                         ----
benchmark                      Profile unit test
coverage-html-report           Run coverage html report => make coverage-html-report
coverage                       Run coverage => make coverage
documentation                  Build documentation => make documentation
down                           Down project containers => make down
generate_changelog             generate changelog
help                           This help dialog. => make help
mypy                           Run mypy on code => make mypy
pre-commit                     run localy precommit
pylint                         Run pylint on code => make pylint
quality                        run pylint, flake8, mypy, and tests => make quality
tests-debug                    Run tests and launch pdb on first failed => make tests-debug
tests-fail-fast                Run tests and stop on first fail => make tests-fail-fast
tests-func-cov                 Run tests and display function cov => make tests-func-cov
tests-reports                  Run tests and generate reports => make tests-reports
```
<!-- END makefile-doc -->
