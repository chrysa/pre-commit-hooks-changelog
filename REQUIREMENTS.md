# REQUIREMENTS — pre-commit-hooks-changelog

> Requirements with an implementation traceability matrix. A row is marked IMPLEMENTED only when
> verifiable in the repo. Tags: FACT / INFERENCE / UNKNOWN.

## Functional requirements

| ID | Requirement | Status | Evidence |
| -- | ----------- | ------ | -------- |
| REQ-FUN-001 | Aggregate `changelog/*.yaml` into a Markdown changelog | IMPLEMENTED | `Collect.collect_versions`, `Formatter.generate` |
| REQ-FUN-002 | Expose a `generate-changelog` console script | IMPLEMENTED | `setup.cfg` `console_scripts` |
| REQ-FUN-003 | Provide a pre-commit hook `id: generate-changelog` scoped to changelog YAML | IMPLEMENTED | `.pre-commit-hooks.yaml` |
| REQ-FUN-004 | Validate entry keys against an allow-list, error on unknown key | IMPLEMENTED | `Collect.validate_keys`, `CHANGELOG_ENTRY_AVAILABLE` |
| REQ-FUN-005 | Support nested (grouped) entries rendered as sub-headers | IMPLEMENTED | `Helper.gen_content`, `changelog/v0.2.0.yaml` |
| REQ-FUN-006 | Configurable output file via `--output-file` | IMPLEMENTED | argparse in `main` |
| REQ-FUN-007 | Configurable source folder via `--changelog-folder` | IMPLEMENTED | argparse in `main` |
| REQ-FUN-008 | Rebuild modes: `all`, `versions`, `latest`, `home` | IMPLEMENTED | `_REBUILD_STRATEGIES`, `AVAILABLE_REBUILD_OPTION` |
| REQ-FUN-009 | Write per-version archives under `changelog/archives/` | IMPLEMENTED | `generate_versions`, `changelog/archives/` |
| REQ-FUN-010 | Home changelog shows latest version + History links to archives | IMPLEMENTED | `generate_home_changelog`, `generate_history`, `changelog.md` |
| REQ-FUN-011 | Idempotent writes (skip unchanged files) | IMPLEMENTED | `save` / `compare_content` |
| REQ-FUN-012 | No-op (exit 0) when no content found | IMPLEMENTED | `main` early return |

## Non-functional requirements

| ID | Requirement | Status | Evidence |
| -- | ----------- | ------ | -------- |
| REQ-NFR-001 | Python >= 3.9 | IMPLEMENTED | `setup.cfg` `python_requires` |
| REQ-NFR-002 | Single runtime dependency (`ruamel.yaml`) | IMPLEMENTED | `setup.cfg` |
| REQ-NFR-003 | Lint clean (ruff, complexity <= 10) | INFERENCE | `pyproject.toml` ruff config; not run here |
| REQ-NFR-004 | Type-checked (mypy) | INFERENCE | `setup.cfg` mypy extra, Makefile `mypy` target |
| REQ-NFR-005 | Tested (pytest, coverage gate) | INFERENCE | `tests/`, `setup.cfg` tests extra, CI badges |
| REQ-NFR-006 | Runs fast on each commit | INFERENCE | pre-commit hook, filename-based versioning (no git walk) |

## Gaps / not implemented (observed)

- Git-tag-driven version bucketing — NOT IMPLEMENTED (noted as a future option). (FACT — reference doc.)
- Config-driven entry taxonomy (allow-list is hardcoded in `generate_changelog.py`). (FACT.)
- Non-Markdown output. (INFERENCE.)
