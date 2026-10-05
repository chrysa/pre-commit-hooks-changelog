# ROADMAP — pre-commit-hooks-changelog

> Derived from in-repo evidence (reference doc, `todo` changelog entries, README). Not a commitment.
> Tags: FACT (stated in repo) / INFERENCE / PROPOSAL (suggested by evidence, not adopted).

## Signalled in-repo

- [FACT] `todo` entries in `changelog/v0.2.0.yaml`: "add alphabetic order", "add date on top of
  version file (created/updated)".
- [FACT] Older `todo` in `changelog.md` output: "refacto", "add unit tests".

## Candidate borrows (from `docs/reference/github-inspiration.md`)

- [PROPOSAL] Externalise the entry-category taxonomy into `pyproject.toml` (towncrier/reno pattern)
  instead of the hardcoded `CHANGELOG_ENTRY_AVAILABLE`. Flagged as highest-value.
- [PROPOSAL] Add `security` / `deprecations` categories to match Keep-a-Changelog.
- [PROPOSAL] Template the renderer (Jinja2/Tera) instead of string-built Markdown.
- [PROPOSAL] Optional `--from-git` version bucketing via git tags (reno's scanner).
- [PROPOSAL] GitHub Release sync of the `latest` output (scriv's `github-release`).

## Notes

- Version-ordering is lexical on filename stems; a semver-aware sort would be a natural
  robustness improvement (relates to the "alphabetic order" todo). (INFERENCE.)
- All referenced OSS is permissively licensed (MIT / Apache-2.0); no copyleft blockers. (FACT — reference doc.)
