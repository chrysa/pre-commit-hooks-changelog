# Architecture

## Purpose

`pre-commit-hooks-changelog` generates a Markdown changelog from a folder of
per-version YAML files. It ships as a [pre-commit](https://pre-commit.com) hook
(`generate-changelog`) and as a standalone CLI installable from PyPI. Each YAML
file describes one version's entries grouped by category (added, fixed,
removed, etc.); the tool aggregates them into a `CHANGELOG.md`.

## Stack

- **Language:** Python (`python_requires >= 3.9`; classifiers list 3.9–3.14).
- **Runtime dependency:** `ruamel.yaml` (YAML parsing, `typ="safe"`).
- **Packaging:** setuptools. `setup.py` is a shim (`setup()`); metadata,
  entry points and tooling config live in `setup.cfg`. `pyproject.toml`
  holds only Ruff config.
- **Tooling:** Ruff (lint + format, line length 120), mypy, pytest +
  pytest-cov + pytest-mock, Sphinx (docs), twine/build (release).
- **Containers:** multi-stage `Dockerfile` (base → application → pytest /
  documentation / quality), orchestrated by `docker-compose.yml`.

> Note: `pyproject.toml` declares the isort first-party package as
> `pre_commit_hooks_changelog`, but the actual importable package is
> `pre_commit_hook` (per `setup.cfg` entry point and the source tree).

## Layout

- `pre_commit_hook/` — the Python package (source of truth).
  - `generate_changelog.py` — CLI entry point, argument parsing, YAML
    collection dataclass and validation.
  - `formatter.py` — renders collected data into Markdown.
  - `helper.py` — supporting utilities.
  - `__init__.py`
- `changelog/` — sample/live YAML changelog sources (`v*.yaml`) plus
  `archives/` rendered per-version Markdown.
- `tests/` — pytest suite with `dataset/yaml/` fixtures (valid/invalid samples).
- `scripts/` — helper scripts.
- `docs/` — Sphinx documentation sources.
- `.pre-commit-hooks.yaml` — hook definition consumed by pre-commit.
- `Makefile`, `Dockerfile`, `docker-compose.yml` — dev/build/CI entry points.
- `.github/` — CI workflows (`pythonpackage.yml`).
- Root also contains several loose helper scripts (`changelog.py`,
  `formater.py`, `generate_changelog.py`, `formatter.py` wrappers) and config
  files (`cliff.toml`, `GitVersion.yml`, `black.toml`, etc.).

## Entrypoints

- **Console script:** `generate-changelog` →
  `pre_commit_hook.generate_changelog:main` (declared in `setup.cfg`).
- **Pre-commit hook:** id `generate-changelog` (`.pre-commit-hooks.yaml`),
  `language: python`, runs on `changelog/` or `changelogs/` `*.yml`/`*.yaml`
  files, stages commit/push/manual, `minimum_pre_commit_version: 3.7.1`.
- **CLI options:** `--output-file`, `--changelog-folder`, `--rebuild`
  (`all` | `versions` | `latest` | `home`).

## Data / External deps

- **Input:** YAML files in the changelog folder (default `changelog`),
  keyed by supported entry categories: added, blocked, fixed, in progress,
  modified, removed, todo, upgraded, unreleased. Unsupported keys raise an
  error.
- **Output:** a generated Markdown changelog file.
- **External services:** PyPI / TestPyPI (release), SonarCloud + Codecov
  (CI quality/coverage badges). No network calls at runtime.

## Build & test

Real commands (from `Makefile` and `setup.cfg`):

```bash
make install        # install dev dependencies
make tests          # run unit tests (pytest)
make coverage       # run coverage (fail_under = 85)
make ruff           # lint + import sort + style
make ruff-format    # check formatting
make mypy           # type check
make quality        # all linters + tests
make generate-changelog   # generate changelog from changelog/ folder
make documentation  # build Sphinx docs
make build          # build Docker images (no cache)
make deploy         # build + publish to PyPI/TestPyPI
```

Direct pytest: `pytest` (config in `setup.cfg`, `testpaths = tests`,
markers `unit`/`functional`). Extras: `.[tests]`, `.[documentation]`,
`.[mypy]`, `.[ruff]`, `.[pre_commit]`, `.[pypi]`.

Containerized flows use `docker-compose.yml` targets (`application`,
`pytest`, `documentation`, `quality`) built from the multi-stage `Dockerfile`.
