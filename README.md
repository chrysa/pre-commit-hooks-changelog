pre-commit-hooks-changelog
================

generate a markdown changelog from folder of yaml files



### Using pre-commit-hooks-changelog with pre-commit

Add this to your `.pre-commit-config.yaml`

    -   repo: https://github.com/chrysa/pre-commit-hooks-changelog
        rev: v0.1.0  # Use the ref you want to point at
        hooks:
        -   id: generate-changelog
            files: 'changelog/.*(?<!\.yaml|.yml)$'


### Options

- `--rebuild` - rebuild changelog from scratch

### As a standalone package (SOON)

If you'd like to use these hooks, they're also available as a standalone
package.

Simply `pip install pre-commit-hooks-changelog`
