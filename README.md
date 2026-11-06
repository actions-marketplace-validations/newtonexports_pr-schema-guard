# PR Schema Guard

A lightweight, zero-configuration GitHub Action that validates incoming JSON contributions against your repository's JSON Schema.

## Usage

```yaml
- name: Validate PR Data
  uses: newtonexports/pr-schema-guard@v1
  with:
    schema-path: '.github/schema.json'
    target-dir: 'patterns/data'
