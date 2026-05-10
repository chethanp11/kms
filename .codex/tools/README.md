# Codex Tools

Deterministic helper scripts for validating repository-visible Codex infrastructure.

## Available

- `validate_codex_contract.py`: checks required Codex-native support files, instruction references, and non-empty purpose docs.
- `bootstrap_appflow.py`: creates starter project-specific AppFlow artifacts when `.codex/` is copied into a new repository.
- `appflow_run.py`: records and validates per-turn AppFlow lifecycle evidence; `closeout-intake` clears consumed product/feedback intent after step `09` writes next-cycle gaps.

## Workflow use

- App mode uses `appflow_run.py` for substantial file-changing lifecycle evidence and intake closeout cleanup.
- Framework mode and control-plane changes use `validate_codex_contract.py` for deterministic structure validation.
- Bootstrap uses `bootstrap_appflow.py` only to create missing starter artifacts; it must not overwrite project-specific files.
