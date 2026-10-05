# CONSTRAINTS — pre-commit-hooks-changelog

> Each constraint is tagged HARD (enforced by code/config), SOFT (convention/standard), or
> INFERRED. Documentation-only.

## Platform & runtime

- [HARD] Python >= 3.9 (`setup.cfg` `python_requires`).
- [HARD] Single runtime dependency: `ruamel.yaml` (`setup.cfg`).
- [HARD] pre-commit >= 3.7.1 to consume the hook (`.pre-commit-hooks.yaml` `minimum_pre_commit_version`).

## Data / input

- [HARD] Source files must live in the changelog folder and match `^(changelog|changelogs)/.*\.(yml|yaml)$`. (`.pre-commit-hooks.yaml`.)
- [HARD] Entry keys are restricted to the allow-list `CHANGELOG_ENTRY_AVAILABLE`
  (`added, blocked, fixed, in progress, modified, removed, todo, upgraded, unreleased`);
  any other key raises `ValueError`. (`generate_changelog.py`.)
- [HARD] The changelog folder must exist or `changelog_folder_path` raises `NotADirectoryError`.
- [HARD] Nested entries render as headers capped at 6 levels; deeper nesting raises `ValueError`. (`helper.py`.)
- [INFERRED] Version ordering relies on lexical sort of filename stems, so `vX.Y.Z.yaml` naming
  is load-bearing (e.g. `v0.10.0` vs `v0.2.0` would sort lexically, not semver). (INFERENCE — `versions_files` sorts by `p.stem`.)

## Behavioural

- [HARD] `main()` returns 0 on the success path even after writing files. Because the hook
  rewrites tracked files but exits 0, a consuming repo needs its own policy to re-stage/verify
  generated output. (INFERENCE — no non-zero "files changed" exit like typical formatters.)
- [HARD] Writes are idempotent — unchanged targets are skipped. (`save`/`compare_content`.)

## chrysa standards (SOFT — from CLAUDE.md / CONTRIBUTING / STANDARDS.chrysa)

- [SOFT] English on disk (code, comments, docs, config).
- [SOFT] Conventional Commits; typed branch prefixes; direct commits to `main` blocked.
- [SOFT] Container-only dev loop (Makefile targets, no host `pytest`/`ruff`/`mypy`).
- [SOFT] Max function 50 lines, max file 500 lines, complexity <= 10, 0 lint warnings (CLAUDE.md Standards; ruff mccabe max-complexity=10 is HARD via `pyproject.toml`).
- [SOFT] One class per file (observed across `pre_commit_hook/`).

## Contradiction note

- CLAUDE.md declares "Default branch: `develop`", but README/CI badges and CONTRIBUTING reference
  `master`/`main` as the working branch. See REVIEW.md. (FACT.)
