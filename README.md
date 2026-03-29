# pre-commit-hooks-changelog

[![CI](https://github.com/chrysa/pre-commit-hooks-changelog/actions/workflows/pythonpackage.yml/badge.svg?branch=master)](https://github.com/chrysa/pre-commit-hooks-changelog/actions/workflows/pythonpackage.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=chrysa_pre-commit-hooks-changelog&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=chrysa_pre-commit-hooks-changelog)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=chrysa_pre-commit-hooks-changelog&metric=coverage)](https://sonarcloud.io/summary/new_code?id=chrysa_pre-commit-hooks-changelog)
[![codecov](https://codecov.io/gh/chrysa/pre-commit-hooks-changelog/graph/badge.svg)](https://codecov.io/gh/chrysa/pre-commit-hooks-changelog)
[![PyPI version](https://img.shields.io/pypi/v/pre-commit-hooks-changelog.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pre-commit-hooks-changelog.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pre-commit-hooks-changelog.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)
[![GitHub release](https://img.shields.io/github/v/release/chrysa/pre-commit-hooks-changelog)](https://github.com/chrysa/pre-commit-hooks-changelog/releases/)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/chrysa/pre-commit-hooks-changelog/graphs/commit-activity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

[Changelog](changelog.md)

## Overview

Generate a markdown changelog from a folder of YAML files.

### Using pre-commit-hooks-changelog with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/chrysa/pre-commit-hooks-changelog
    rev: v0.2.0  # Use the ref you want to point at
    hooks:
    -   id: generate-changelog
```

### Options

| Option | Description |
| ------ | ----------- |
| `--output-file` | Define changelog output file path |
| `--changelog-folder` | Source folder containing changelog YAML files |
| `--rebuild` | Rebuild changelog (see rebuild options below) |

#### Rebuild options

| Value | Description |
| ----- | ----------- |
| `all` | Rebuild changelog from scratch |
| `versions` | Rebuild changelog for each version |
| `latest` | Rebuild latest changelog |
| `home` | Rebuild changelog file on repo root |

### Standalone

`pip install pre-commit-hooks-changelog`

<!-- START makefile-doc -->
```text
$ make help
pre-commit-hooks-changelog — Makefile help

target                         help
------                         ----
benchmark                      Profile unit tests (benchmark)
build                          Build Docker images (no cache)
clean                          Remove generated artifacts (build, dist, cache)
compile                        Compile Python package (bdist)
coverage                       Run code coverage
coverage-html-report           Generate HTML coverage report
deploy                         Build, publish to PyPI and TestPyPI
documentation                  Build Sphinx documentation
down                           Stop and remove Docker containers
generate-changelog             Generate changelog from changelog/ folder
help                           Show this help
install                        Install development dependencies
mypy                           Run mypy type check
pre-commit                     Install and run pre-commit on all files
pypi                           Publish to PyPI
pypi-test                      Publish to TestPyPI
quality                        Run all linters + tests
ruff                           Run ruff linter (lint + import sort + style)
ruff-format                    Check ruff formatting
tests                          Run unit tests
tests-10-slower                Tests — display the 10 slowest tests
tests-debug                    Tests — drop into pdb on first failure
tests-fail-fast                Tests — stop at first failure
tests-func-cov                 Tests — show per-function coverage
tests-reports                  Tests — generate XML / HTML reports
```
<!-- END makefile-doc -->
