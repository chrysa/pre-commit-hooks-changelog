# OBSERVABILITY — pre-commit-hooks-changelog

> Tags: FACT / INFERENCE. Documentation-only.

## Runtime signals (FACT)

This is a short-lived CLI, not a service — observability is stdout + exit code.

- `Formatter` prints per-file status to stdout, colour-coded: `CREATED`, `UPDATED`, `SKIPPED`,
  `REMOVED`, `FAILED`. (FACT — `formatter.py` `write_file` / `save` / `remove_*`.)
- Exit code: `main()` returns 0 on success and on the empty no-op path; validation raises
  Python exceptions (`ValueError`, `NotADirectoryError`, `TypeError`) which surface as tracebacks
  with non-zero exit. (FACT.)

## Build / quality signals (FACT — README badges)

- CI: GitHub Actions `pythonpackage.yml`.
- SonarCloud quality gate + coverage (`chrysa_pre-commit-hooks-changelog`).
- Codecov coverage.
- PyPI version / supported Python versions / monthly downloads.

## CI workflows present (FACT — `.github/workflows/`)

`ci.yml`, `pythonpackage.yml`, `release.yml`, `action-check.yml`, `labeler.yml`,
`sync-labels.yml`, `auto-assign.yml`, `approved-label.yml`, `detect-conflicts.yml`,
`dependabot-auto-merge.yml`, `pr-dependencies.yml`, `pull-request-size.yml`,
`update-pr-body.yml`, `enforce-shortcut-link.yml`.

## Gaps

- No structured logging / metrics / tracing — appropriate for a CLI hook. (INFERENCE.)
- No runtime error-tracking (Sentry) — not applicable to a batch CLI. (INFERENCE.)
