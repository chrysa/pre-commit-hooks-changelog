# GLOSSARY — pre-commit-hooks-changelog

> Tags: FACT unless noted.

- **generate-changelog** — the console script / pre-commit hook id; entry point
  `pre_commit_hook.generate_changelog:main`.
- **Collect** — dataclass that discovers, loads, and validates `changelog/*.yaml` into a `content` dict.
- **Formatter** — dataclass that renders the `content` dict to Markdown and writes archives + home changelog.
- **Helper** — dataclass of Markdown primitives (titles, headers, unordered lists, internal links); `MAX_HEADER_LEVEL = 6`.
- **Entry key** — a top-level YAML key describing a change type; must be in the allow-list
  `CHANGELOG_ENTRY_AVAILABLE` (`added, blocked, fixed, in progress, modified, removed, todo, upgraded, unreleased`).
- **Version file** — one YAML per release, `changelog/vX.Y.Z.yaml`; the version title is the filename stem.
- **Archive** — per-version rendered Markdown under `changelog/archives/vX.Y.Z.md`.
- **Home changelog** — the root output file (default `changelog.md`): latest version + a "History"
  list of links to archives.
- **Rebuild mode** — one of `all` / `versions` / `latest` / `home`, dispatched via `_REBUILD_STRATEGIES`.
- **Idempotent save** — `save()`/`compare_content()` skips writing when rendered content equals the file on disk.
- **Fragment/news-file pattern** (INFERENCE) — the OSS category (towncrier/scriv/reno) of building a
  changelog from many small files to avoid merge conflicts; this repo uses file-per-version YAML.
