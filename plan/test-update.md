# Test Update Plan

## Current scope
- `TEST-022`: Validate GPT-4o configuration, API client payload handling, mocked extraction mapping, and deterministic fallback.

## Validation
- Add/extend unit tests using fake API clients only; no live API calls.
- Run `python3 -m unittest discover -s tests/unit -p 'test_*.py'`.
- Run `python3 -m compileall -q src`.
- Run `git diff --check`.
- Run `python3 .codex/tools/validate_codex_contract.py`.
