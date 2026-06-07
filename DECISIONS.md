# Decisions

## Modernize pre-commit + adopt chrysa canonical baseline

- **Date:** 2026-06-07
- **Status:** Accepted
- **Context:** Legacy pre-commit config was broken (dead/gitlab-auth hooks); repo drifted from chrysa standard (OPS-190).
- **Decision:** Replace with the §8 baseline + keep the repo-local hooks (clean_python, hadolint, generate-changelog).
