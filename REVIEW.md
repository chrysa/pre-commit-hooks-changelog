# REVIEW — documentation pass notes

> Meta-notes from the documentation-only pass on 2026-09-25. No source/tests/config/CI were changed.

## What was generated (root .md)

PRD, TRD, ARCHITECTURE, REQUIREMENTS, CONSTRAINTS, DECISIONS, TESTING, SECURITY, OBSERVABILITY,
ROADMAP, GLOSSARY, and this REVIEW.

## Docs skipped (with reason)

- None of the target set was skipped as empty — the repo had enough evidence for each. (FACT.)

## Existing docs preserved

- `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, `handover.md`, `ai-instructions.md`,
  `llms-full.txt`, `context-map.json`, `docs/reference/github-inspiration.md`, `docs/conf.py` — untouched.
- `handover.md`, `ai-instructions.md`, `llms-full.txt`, `context-map.json` are marked
  GENERATED (ADR D-0012, `scripts/gen_context_files.py`) — left alone; regenerate via
  `make gen-context-files`, do not hand-edit. (FACT.)

## Contradictions / inconsistencies found

1. **Default branch mismatch.** `CLAUDE.md` says "Default branch: `develop`", while the CI badge
   in `README.md` points at `?branch=master` and `CONTRIBUTING.md` branches from `main`. Three
   different branch names referenced. Owner should reconcile. (FACT.)
2. **CLAUDE.md is a template.** It still contains `[PROJECT_NAME]` / `[PLACEHOLDER]` markers and
   `@[claude-sonnet-4-6]`, i.e. the project-specific section was never filled in. (FACT.)
3. **Two changelog files at root.** `changelog.md` (generated output, shows `V0.1.5`) and
   `CHANGELOG.md` (contains a git-cliff `[Unreleased]` block). The repo ships both this tool's
   YAML pipeline *and* a `cliff.toml` — two changelog mechanisms coexist. Potentially confusing;
   owner should confirm which is canonical. (FACT.)
4. **Version drift.** `setup.cfg` version = `0.2.0`; generated `changelog.md` latest = `V0.1.5`;
   newest YAML = `v0.2.0.yaml`. The home changelog appears stale versus the version files. (FACT.)

## Documentation debt

- No written ADRs in-repo (`DECISIONS.md` here is reconstructed). (FACT.)
- Exact coverage threshold not documented in-repo. (UNKNOWN.)
- `CLAUDE.md` placeholders unresolved (owner action).

## Key UNKNOWNs

- Rationale behind the hardcoded taxonomy and YAML-per-version design (no ADR).
- Canonical changelog mechanism (this tool vs git-cliff).
- Repo profile / DDD level (handover.md says "not available").
