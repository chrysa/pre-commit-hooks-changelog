# pre-commit-hooks-changelog

generate a markdown changelog from folder of yaml files

## Using pre-commit-hooks-changelog with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/chrysa/pre-commit-hooks-changelog
        rev: v0.1.0  # Use the ref you want to point at
        hooks:
        -   id: generate-changelog
            files: 'changelog/.*(?<!\.yaml|.yml)$'

## Options

|   |   |
|---|---|
| `--output-file` | define changelog outpout |
| `--changelog-folder` | source folder of changelogs |
| `--rebuild` | rebuild changelog see below |

### Rebuild options

|   |   |
|---|---|
| `all` | rebuild changelog from scratch |
| `versions` | rebuild changelog for each version |
| `latest` | rebuild latest changelog |
| `home` | rebuild changelog file on repo root |

## Standalone

`pip install pre-commit-hooks-changelog`

## [Changelog](changelog.md)
