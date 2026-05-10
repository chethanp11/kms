# Codex Tools

Deterministic helper scripts for validating repository-visible Codex infrastructure.

## Available

- `validate_codex_contract.py`: checks required Codex-native support files, instruction references, and non-empty purpose docs.
- `bootstrap_appflow.py`: creates starter project-specific AppFlow artifacts when `.codex/` is copied into a new repository.
- `appflow_run.py`: records and validates per-turn AppFlow lifecycle evidence.
