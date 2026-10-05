# SECURITY — pre-commit-hooks-changelog

> Documentation-only review. No code was modified. Findings are for the owner. Tags: FACT / INFERENCE.

## Secret scan (this pass)

- No hardcoded secrets, keys, tokens, or credentials found in source, config, or fixtures. (FACT — targeted grep over `pre_commit_hook/`, `scripts/`, `setup.cfg`, `pyproject.toml`.)
- The only "secret"-shaped strings are in `scripts/quality_gate.py`, which *invokes* `detect-secrets` as a quality gate — a security control, not a leak. (FACT.)
- Author email `greau.anthony@gmail.com` appears in `setup.cfg` (package metadata). This is the
  project owner's own published contact, standard for PyPI packaging — not a finding. (FACT.)

## Threat surface

- **Input:** untrusted YAML from the consuming repo's `changelog/` folder. Parsed with
  `ruamel.yaml.YAML(typ="safe")` — the safe loader, so arbitrary object construction / code
  execution via YAML tags is not enabled. (FACT — `generate_changelog.py`.) Positive control.
- **File writes:** the tool writes `changelog.md` and files under `changelog/archives/`, and
  `remove_archives`/`remove_home_changelog` unlink files. Paths derive from `--output-file` /
  `--changelog-folder` and YAML filenames. (INFERENCE) A hostile `--changelog-folder`/`--output-file`
  value could direct writes/deletes outside the intended folder; in the pre-commit context these
  args are set by the repo maintainer, so the trust boundary is the maintainer, not an external
  attacker. Severity: LOW (local, maintainer-controlled). No fix applied (docs-only).
- **No network, no auth, no deserialization of remote data, no DB.** (FACT.)

## HIGH / CRITICAL findings

- None identified. (FACT — for this documentation pass.)

## Security posture (context)

- `detect-secrets` runs as part of `scripts/quality_gate.py`. (FACT.)
- Security scanning is a pre-commit + CI gate per chrysa standards. (FACT — CLAUDE.md / STANDARDS.)
- The repo ships a `.pre-commit-config.yaml` (3.6K) and CI workflows including `pythonpackage.yml`. (FACT — inventory.)

## Recommendations (non-blocking, for owner)

1. Consider validating/normalising `--output-file` and `--changelog-folder` to stay within the
   repo root (defence-in-depth against path traversal). (INFERENCE — LOW.)
2. Keep the `ruamel.yaml` safe loader; never switch to an unsafe/round-trip loader on untrusted input. (FACT-based.)
