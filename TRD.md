# TRD — pre-commit-hooks-changelog

> Technical Requirements / design reference. Tags: FACT / INFERENCE / UNKNOWN. Documentation-only.

## Stack (FACT)

- Language: Python, `python_requires = >=3.9` (`setup.cfg`).
- Runtime dependency: `ruamel.yaml` (`setup.cfg` `install_requires`).
- Packaging: `setup.cfg` (declarative) + minimal `setup.py` (`setup()`); `name = pre_commit_hooks_changelog`, `version = 0.2.0`.
- Console entry point: `generate-changelog = pre_commit_hook.generate_changelog:main` (`setup.cfg` `[options.entry_points]`).
- Pre-commit contract: `.pre-commit-hooks.yaml`, `language: python`, `minimum_pre_commit_version: 3.7.1`.

## Package layout (FACT)

`pre_commit_hook/`
- `__init__.py` — exports `Collect`, `Formatter`.
- `generate_changelog.py` — CLI entry (`main`), argparse, `Collect` dataclass, validation.
- `formatter.py` — `Formatter` dataclass, Markdown rendering, rebuild strategy dispatch.
- `helper.py` — `Helper` Markdown primitives (headers, lists, max 6 header levels).

## Entry flow (FACT — `generate_changelog.py:main`)

1. Parse args: `filenames` (positional, from pre-commit), `--output-file` (default `changelog.md`),
   `--changelog-folder` (default `changelog`), `--rebuild` (choices: `all`, `versions`, `latest`, `home`).
2. Build `Collect(changelog_folder, changelog_entry_available=CHANGELOG_ENTRY_AVAILABLE, main_output_file)`.
3. `collect_versions()` — glob `<folder>/*.yaml`, sort by filename stem, load each with `ruamel.yaml`,
   validate keys against the allow-list, accumulate into `content`.
4. If `content` empty → return 0 (no-op). (FACT.)
5. `Formatter(...).generate(archives_path, changelog_path, content_dict, rebuild)`.
6. Return 0. (FACT — always exits 0 on success path; see CONSTRAINTS for the pre-commit implication.)

## Data model (FACT)

- **Source of truth:** one YAML file per version, named `vX.Y.Z.yaml` in `changelog/`.
  Version title is derived from the filename stem (`.yaml`/`.yml` stripped) — not from git. (FACT.)
- **Allowed top-level entry keys** (`CHANGELOG_ENTRY_AVAILABLE`, `generate_changelog.py`):
  `added`, `blocked`, `fixed`, `in progress`, `modified`, `removed`, `todo`, `upgraded`, `unreleased`. (FACT.)
- Values may be a flat list or a nested mapping (e.g. `upgraded: { dependencies: { pre-commit: [...] } }`)
  which renders as nested sub-headers. (FACT — `changelog/v0.2.0.yaml`, `helper.py` recursion, `MAX_HEADER_LEVEL=6`.)
- **Output:** `changelog.md` at repo root (home), plus per-version archives in `changelog/archives/*.md`. (FACT — `changelog/archives/`, formatter.)

## Configuration surface (FACT)

| Flag | Default | Effect |
| ---- | ------- | ------ |
| `--output-file` | `changelog.md` | home changelog output path |
| `--changelog-folder` | `changelog` | source folder of YAML files |
| `--rebuild` | `None` | one of `all` / `versions` / `latest` / `home` (strategy dispatch in `formatter.py`) |

Rebuild is a lookup-table (strategy dict) dispatch — a new mode is a new table row, not a new
branch (FACT — comment in `formatter.py`: "A new mode is a new row, never a new branch").

## Validation (FACT)

`Collect.validate_keys()` raises `ValueError` when a YAML file uses a key outside the allow-list,
with a message listing the supported keys. `changelog_folder_path` raises `NotADirectoryError`
if the folder is absent.

## Unknowns

- Exact archive filename/section layout beyond `v*.md` glob (partially trimmed in reading). (UNKNOWN — verify in `formatter.py`.)
- Whether nested depth beyond 6 is guarded everywhere vs. only in `Helper`. (INFERENCE: `helper.py` raises `ValueError` past level 6.)
