# ARCHITECTURE — pre-commit-hooks-changelog

> Tags: FACT / INFERENCE / UNKNOWN. Documentation-only; no code changed.

## Overview

A small Python package with a three-class pipeline: **collect → format → render**.
Input is a folder of per-version YAML files; output is a home `changelog.md` plus per-version
Markdown archives. (FACT — `pre_commit_hook/*`.)

## Components (FACT)

| Component | File | Responsibility |
| --------- | ---- | -------------- |
| CLI / `main()` | `generate_changelog.py` | argparse, wire `Collect` → `Formatter`, exit code |
| `Collect` (dataclass) | `generate_changelog.py` | discover YAML files, load, validate keys, build `content` dict |
| `Formatter` (dataclass) | `formatter.py` | rebuild-strategy dispatch, write archives + home changelog, idempotent save |
| `Helper` (dataclass) | `helper.py` | Markdown primitives: titles, headers, unordered lists, internal links, recursive `gen_content` |

## Data flow (FACT)

```
changelog/*.yaml
   │  Collect.collect_versions()  (glob, sort by stem, ruamel.yaml load, validate_keys)
   ▼
content: { "vX.Y.Z.yaml": { entry_key: [items] | {nested} } }
   │  Formatter.generate(rebuild)  → strategy from _REBUILD_STRATEGIES
   ▼
   ├─ generate_versions() → changelog/archives/vX.Y.Z.md   (one file per version)
   └─ generate_home_changelog() → changelog.md             (latest version + History links)
```

## Key design choices (FACT)

- **Strategy pattern for rebuild modes.** `_REBUILD_STRATEGIES` maps `all/home/latest/versions`
  to methods; `generate()` looks the mode up (default = plain generate). Adding a mode = a new
  dict row (documented intent in an inline comment). This aligns with the chrysa standard
  "prefer a lookup table to a state machine". (FACT.)
- **Idempotent writes.** `Formatter.save()` / `compare_content()` compares rendered content to
  the on-disk file and prints `CREATED` / `UPDATED` / `SKIPPED`; unchanged files are not
  rewritten. (FACT — `formatter.py`.)
- **Filename-derived versions.** Version titles come from the YAML filename stem, sorted; there
  is no git dependency. The "latest" version is `list(content).keys()[-1]` after sort. (FACT.)
- **Recursive renderer with a depth cap.** `Helper.gen_content` recurses over nested dict/list
  structures; header level is capped at `MAX_HEADER_LEVEL = 6` and raises `ValueError` beyond. (FACT.)
- **One class per file** (chrysa standard). (FACT.)

## Consumers (FACT)

- pre-commit: hook id `generate-changelog`, triggered on files matching
  `^(changelog|changelogs)/.*\.(yml|yaml)$`, `types: [yaml]`, stages `[commit, push, manual]`.
- Standalone CLI via the `generate-changelog` console script.
- Makefile `generate-changelog` target.

## Diagram fidelity

INFERENCE: the two-output split (archives + home with a "History" links section) is confirmed
by `changelog.md` (contains a `## History` list linking `changelog/archives/v*.md`).
