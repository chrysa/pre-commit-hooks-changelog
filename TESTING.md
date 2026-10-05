# TESTING — pre-commit-hooks-changelog

> Tags: FACT / INFERENCE. Documentation-only; commands transcribed from `Makefile` / `setup.cfg`,
> not executed by this pass.

## Test layout (FACT)

`tests/`
- `collect_test.py` — `Collect` behaviour (path generation defaults/custom, key validation), GIVEN/WHEN/THEN style, uses `tmp_path` + `mocker`.
- `formatter_test.py` — `Formatter` rendering / rebuild.
- `conftest.py`, `__init__.py`.
- `dataset/yaml/` — fixtures: `simple_valid.yaml`, `sublist_valid.yaml`, `sublist_invalid.yaml`.
- `dataset/markdown/` — expected outputs: `simple_valid.md`, `sublist_valid.md`.

Style follows the chrysa `testing-pytest` standard: pytest, `pytest-mock`, GIVEN/WHEN/THEN,
data-driven fixtures. (FACT — `setup.cfg` tests extra: `pytest`, `pytest-cov`, `pytest-mock`.)

## How to run (FACT — containerised, via Makefile)

The chrysa standard is container-only; do not call `pytest`/`ruff`/`mypy` on the host.

```bash
make install      # dev deps + pre-commit
make test         # unit tests (docker compose run --rm pytest)
make coverage     # tests with coverage  (alias: make test-cov)
make lint         # ruff  (alias of make ruff)
make ruff-format  # ruff format check
make mypy         # mypy  (alias: make typecheck)
make quality      # ruff + ruff-format + mypy + test
make pre-commit   # install + run pre-commit on all files
```

Other useful targets (FACT — `make help`): `tests-fail-fast`, `tests-debug`,
`tests-10-slower`, `tests-func-cov`, `tests-reports`, `benchmark`.

## Coverage gate (INFERENCE)

Coverage is reported to SonarCloud and Codecov (README badges). A numeric threshold is enforced
in CI (INFERENCE — CONTRIBUTING says "keep coverage at or above the project threshold");
the exact percentage is not stated in-repo. (UNKNOWN — exact number.)

## Verification commands (FACT — CONTRIBUTING)

```bash
pre-commit run --all-files
make test
```
