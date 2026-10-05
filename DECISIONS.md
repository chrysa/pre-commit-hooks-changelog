# DECISIONS — pre-commit-hooks-changelog

> ADR-style record reconstructed from repository evidence. Where rationale is not written down it
> is tagged UNKNOWN. These are descriptive, not new decisions.

## ADR-001 — YAML-per-version as the source of truth

- **Status:** Accepted (observed in code). (FACT.)
- **Context:** A single shared `CHANGELOG.md` causes merge conflicts. (INFERENCE — reference doc.)
- **Decision:** Each release is authored in its own `changelog/vX.Y.Z.yaml`; the tool renders Markdown from them. (FACT.)
- **Consequences:** No conflicts on the changelog; curated intent; version derived from filename, not git.
- **Rationale source:** UNKNOWN (no ADR file in repo; inferred from `docs/reference/github-inspiration.md`).

## ADR-002 — Hardcoded entry-key allow-list

- **Status:** Accepted (observed). (FACT — `CHANGELOG_ENTRY_AVAILABLE`.)
- **Decision:** Validate YAML keys against a fixed in-code list; reject unknown keys with a clear error.
- **Consequences:** Predictable output taxonomy; adding a category requires a code change (not config).
  The reference doc flags externalising this as the highest-value future borrow. (FACT.)
- **Rationale source:** UNKNOWN.

## ADR-003 — Rebuild modes via strategy lookup table

- **Status:** Accepted (observed). (FACT — `_REBUILD_STRATEGIES` + inline comment.)
- **Decision:** `all/home/latest/versions` map to methods in a dict; `generate()` dispatches by key.
- **Consequences:** New mode = new table row, no new branch — matches chrysa "lookup table over state machine".
- **Rationale source:** FACT (inline comment states the intent).

## ADR-004 — Dual delivery: pre-commit hook + standalone PyPI CLI

- **Status:** Accepted (observed). (FACT — `.pre-commit-hooks.yaml`, `console_scripts`, PyPI badges.)
- **Decision:** Ship both as a pre-commit hook and as an installable console script.
- **Consequences:** Usable inside pre-commit, standalone, in a Makefile, and in CI.
- **Rationale source:** UNKNOWN (no written ADR).

## ADR-005 — Container-only developer loop

- **Status:** Accepted (observed). (FACT — Makefile targets run via `docker compose run`.)
- **Decision:** Lint/type/test/changelog run in containers; host tooling is not used.
- **Consequences:** Reproducible; aligns with chrysa container standards.
- **Rationale source:** FACT (chrysa STANDARDS in CLAUDE.md).

> No `docs/adr/` or `DECISIONS`-style ADR directory exists in the repo. (FACT.)
