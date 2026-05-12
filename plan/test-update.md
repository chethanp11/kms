# Test Update Plan

## Current scope
- `TEST-021`: Validate governed AI-assisted knowledge understanding candidates and no direct publish behavior.

## Validation
- Add `tests/unit/test_knowledge_understanding.py` for extraction categories, relevance filtering, confidence scoring, draft support, and run artifact behavior.
- Run `python3 -m unittest discover -s tests/unit -p 'test_*.py'`.
- Run `python3 -m compileall -q src`.
- Run `git diff --check`.
- Run `python3 .codex/tools/validate_codex_contract.py`.
