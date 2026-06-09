# pre-commit-hooks-changelog

|    GENERAL    |
|---|---|---|---|
|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/chrysa/pre-commit-hooks-changelog/graphs/commit-activity)|[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)|[![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/)|[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)|
|[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/chrysa/pre-commit-hooks-changelog/releases/)|[![PyPI download day](https://img.shields.io/pypi/dd/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.org/project/pre-commit-hooks-changelog/)|

|     CI STATUS    |
|------------------|
| master | develop |
|:------:|:-------:|
| ![.github/workflows/pythonpackage.yml](https://github.com/chrysa/pre-commit-hooks-changelog/workflows/.github/workflows/pythonpackage.yml/badge.svg?branch=master) | ![.github/workflows/pythonpackage.yml](https://github.com/chrysa/pre-commit-hooks-changelog/workflows/.github/workflows/pythonpackage.yml/badge.svg?branch=develop) |

Generate a Markdown `changelog.md` from a folder of small YAML files — one file per release.

## Why

Editing a single growing `CHANGELOG.md` by hand causes merge conflicts on every branch. Instead, each release gets its own tiny YAML file. This tool collects them, validates them, and renders a clean Markdown changelog automatically — ideal as a [pre-commit](https://pre-commit.com/) hook so the changelog stays in sync with your sources.

## Who it's for

Project maintainers who want a conflict-free, reviewable changelog workflow driven by per-version files committed alongside the code.

## Features

- **One file per version** — keep `changelog/v1.2.0.yaml` next to your work, no shared file to conflict on.
- **Validated entries** — only supported section keys are accepted; an unknown key fails the run with a clear error.
- **Automatic on commit** — runs as a pre-commit hook whenever a changelog YAML changes.
- **Rebuild modes** — regenerate everything, per-version, or just the latest from scratch.
- **Archives + history** — older versions are linked from the root changelog under a `History` section.

## Installation

Standalone via PyPI:

```bash
pip install pre-commit-hooks-changelog
```

This installs the `generate-changelog` console script.

## Usage

### 1. Write per-version YAML files

Put one file per release in a `changelog/` folder, e.g. `changelog/v0.2.0.yaml`:

```yaml
added:
    - markdown linter in pre-commit cycle
    - rebuild argument

fixed:
    - mypy error

todo:
    - add unit tests
```

Supported section keys (any other key fails validation):

`added`, `blocked`, `fixed`, `in progress`, `modified`, `removed`, `todo`, `upgraded`, `unreleased`

Files are ordered by filename, so name them so they sort chronologically (e.g. `v0.1.0.yaml`, `v0.2.0.yaml`).

### 2. Generate

```bash
generate-changelog
```

This reads `changelog/*.yaml` and writes `changelog.md` at the repo root, with older versions linked under a `History` section pointing to `changelog/archives/`.

### As a pre-commit hook

Add this to your `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/chrysa/pre-commit-hooks-changelog
    rev: v0.2.0  # use the tag you want to pin
    hooks:
    -   id: generate-changelog
```

The hook (id `generate-changelog`) runs on the `commit`, `push`, and `manual` stages whenever a staged file matches `changelog/**.yaml`.

## Options

| Flag | Default | Description |
|---|---|---|
| `--output-file` | `changelog.md` | Output changelog file |
| `--changelog-folder` | `changelog` | Source folder of changelog YAML files |
| `--rebuild` | _(none)_ | Rebuild mode — see below |

`--rebuild` accepts one of:

| Value | Effect |
|---|---|
| `all` | Rebuild the whole changelog from scratch |
| `versions` | Rebuild the per-version files |
| `latest` | Rebuild only the latest version |
| `home` | Rebuild the changelog file at the repo root |

Example:

```bash
generate-changelog --changelog-folder changelog --output-file changelog.md --rebuild all
```

## Documentation

- [Changelog](changelog.md)
- [Contributing](CONTRIBUTING.md)
- Sphinx docs config in [`docs/`](docs/)

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
