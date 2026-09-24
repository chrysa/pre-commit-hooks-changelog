---
name: pre-commit-hook-authoring
description: "Author or change this repo's `.pre-commit-hooks.yaml` entry, its Python entry point, or its versioning for consumers. Not for generic Python/testing work — use `check`/`testing-pytest` for that."
when_to_use: "editing .pre-commit-hooks.yaml, changing the generate-changelog entry point/args, adding a new hook id, testing a hook change before release, bumping the tag consumers pin to"
metadata:
  version: "1.0.0"
---

# Pre-commit hook authoring

This repo IS a pre-commit hook, not a library imported by consumers. Every consumer
repo's `.pre-commit-config.yaml` pins a `rev:` (git tag) of this repo and references
the hook `id:` from `.pre-commit-hooks.yaml`. Changes here are a wire contract, not
an internal implementation detail.

## The contract: `.pre-commit-hooks.yaml`

```yaml
-   id: generate-changelog
    name: generate changelog from folder
    entry: generate-changelog
    language: python
    minimum_pre_commit_version: '3.7.1'
    language_version: python3
    files: ^(changelog|changelogs)/.*\.(yml|yaml)$
    types: [yaml]
    stages: [commit, push, manual]
```

Every field here is consumer-visible:

- `entry` — must match the console script in `setup.cfg`
  (`[options.entry_points] console_scripts`). Renaming the entry point without
  updating both breaks every consumer silently — `pre-commit` will only fail
  loudly on the consumer's next run, far from this repo.
- `files` / `types` — the trigger glob. Narrowing it is a breaking change for
  any consumer relying on the broader match; widening it can cause the hook
  to fire (and potentially fail) on files it never touched before.
- `stages` — which git hook stages (`commit`, `push`, `manual`) invoke it.
  Removing a stage is breaking for consumers who rely on it running there.
- `language` / `language_version` / `additional_dependencies` — the runtime
  pre-commit provisions. Changing these can shift startup time or break
  consumers pinned to an incompatible Python.

## Before changing the entry point or its args

1. Grep `setup.cfg` for `console_scripts` to confirm the entry point name is
   still consistent with `.pre-commit-hooks.yaml` → `entry`.
2. Check `pre_commit_hook/generate_changelog.py::main` — argument parsing
   changes are consumer-facing (any documented flag, default, or exit code).
3. Run the changelog-schema-reviewer subagent
   (`.claude/agents/changelog-schema-reviewer.md`) if the change touches
   entry parsing/formatting output, not just the CLI surface.

## Testing a hook change end-to-end

Unit tests (`tests/formatter_test.py`, `tests/collect_test.py`) exercise the
Python internals. They do **not** exercise the thing consumers actually run:
`pre-commit` invoking this repo as a hook. Before merging a change to
`pre_commit_hook/` or `.pre-commit-hooks.yaml`, run it the way a consumer
would:

```bash
# From this repo's root — runs the hook against this repo's own tree
pre-commit try-repo . generate-changelog --all-files

# From a separate consumer repo, to test against a real target
pre-commit try-repo /path/to/this/repo generate-changelog --files changelog/some-entry.yml
```

`try-repo` runs the hook exactly as `.pre-commit-hooks.yaml` declares it —
same `entry`, `language`, `files` filter — without needing a published tag.
A non-zero exit or unexpected diff here is the same failure a consumer would
hit on their next commit.

The `.claude/hooks/pre-commit-self-test.cjs` hook runs this automatically
before any `git commit` that touches `pre_commit_hook/**` or
`.pre-commit-hooks.yaml`, when `pre-commit` is installed locally.

## Versioning for consumers

- Consumers pin `rev: <tag>` in their `.pre-commit-config.yaml`. A breaking
  change to the contract above requires a major version bump; document it as
  its own changelog entry (this repo eats its own dog food — see
  `changelog/` folder format).
- Never silently change `entry`, `files`, or `stages` in a patch release —
  consumers won't re-check the diff, only the version number.

## Common pitfalls

- Renaming the console script without updating `.pre-commit-hooks.yaml` →
  `entry` in the same commit.
- Narrowing `files`/`types` and assuming it's "just a bugfix" — it silently
  stops the hook from running on files it used to cover.
- Testing only with `pytest`, never `pre-commit try-repo` — unit tests can't
  catch an entry-point or schema drift because they call the Python function
  directly, bypassing pre-commit's own invocation path entirely.
