# Test Update Plan

## Current scope
- `TEST-020`: Validate the populated KMS runtime through deterministic unit tests and compile checks.

## Validation
- Add `tests/unit/test_working_kms_runtime.py` for end-to-end source intake through approval/publish/search/projection using temporary directories.
- Run `python3 -m unittest discover -s tests/unit -p 'test_*.py'`.
- Run `python3 -m compileall -q src`.
- Run `git diff --check`.
- Run `python3 .codex/tools/validate_codex_contract.py`.
