# PRD — pre-commit-hooks-changelog

> Product Requirements. Generated as documentation-only; tags: FACT (verified in repo), INFERENCE (reasoned from evidence), UNKNOWN (not determinable from repo). No source/tests/config were modified.

## Problem

Teams that maintain a shared `CHANGELOG.md` hit merge conflicts on every branch, because
every contributor edits the same file. (INFERENCE, corroborated by `docs/reference/github-inspiration.md`,
which frames conflict avoidance as the core value versus towncrier/scriv.)

## Solution

A [pre-commit](https://pre-commit.com) hook plus standalone CLI, `generate-changelog`, that
reads a folder of per-version YAML files (`changelog/vX.Y.Z.yaml`) and renders a Markdown
changelog. Each release is authored in its own YAML file, so contributors do not edit one
shared file. (FACT — `.pre-commit-hooks.yaml`, `setup.cfg` `console_scripts`,
`pre_commit_hook/generate_changelog.py`.)

## Users

- **Consuming repositories** that add the hook to their `.pre-commit-config.yaml`. (FACT — README.)
- **Maintainers** authoring `changelog/*.yaml` entries. (FACT.)
- Author: Anthony Greau. (FACT — `setup.cfg`.)

## Distribution

- Published on PyPI as `pre-commit-hooks-changelog` (`pip install pre-commit-hooks-changelog`). (FACT — README, PyPI badges.)
- Consumed via pre-commit `repo:`/`rev:` reference. (FACT — README.)

## Value proposition

| Benefit | Evidence |
| ------- | -------- |
| No merge conflicts on the changelog | INFERENCE — per-version YAML files, `docs/reference/github-inspiration.md` |
| Curated, human-authored intent (not commit scraping) | FACT — YAML is the source of truth; contrasted with git-cliff in reference doc |
| Runs on every commit as a fast pre-commit hook | FACT — `.pre-commit-hooks.yaml` stages `[commit, push, manual]` |
| Also usable standalone / in a Makefile / in CI | FACT — README "Standalone", Makefile `generate-changelog` target |

## Out of scope (observed)

- Git-history / tag-driven version bucketing (noted as a possible future borrow, not implemented). (FACT — `docs/reference/github-inspiration.md`.)
- Non-Markdown output formats (RST/HTML). (INFERENCE — only Markdown rendering exists.)

## Open questions

- Target ecosystem role beyond OSS pre-commit hook. (UNKNOWN.)
