# KMS Scripts

Project-owned helper scripts for the KMS application scaffold.

## Boundary

- Scripts may validate scaffold shape, run local project checks, prepare fixtures, or support maintenance operations.
- Scripts must use deterministic behavior and should prefer the Python standard library until the project dependency stack is installed.
- Scripts must not become hidden runtime services.
- Scripts must not bypass KMI governance or write finalized `/wiki` content directly.
- AppFlow/control-plane tooling belongs in `.codex/tools/`, not here.

## Current scripts

- `validate_scaffold.py`: validates that the staged KMS application scaffold has the expected `src/`, `tests/`, `design/`, `plan/`, `dev_log/`, `intent/`, and `scripts/` files/directories.
