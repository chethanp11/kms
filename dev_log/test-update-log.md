# Test Update Log

## Purpose
Record meaningful test changes that were actually applied.

## Intent linkage
- Capture the validation coverage that accompanies design and code changes.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Change: `[what test changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, DEV-xxx, TEST-xxx]`
- Intent sources: `[user prompt, intent/*, intent/gaps.md]`

## Entries
- `DEV-002` | `2026-04-07` | `test` | Updated the test planning guidance so every test traces back to a UX flow and correctness criteria, and adjusted the traceability expectations to surface flow-to-criteria-to-test coverage. | The new design chain requires tests to be derived from correctness criteria rather than invented independently. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`, `DEV-002` | `INT-PROD-*`, `INT-FB-*`, `intent/gaps.md`
- `DEV-012` | `2026-05-10` | `unit tests` | Added `tests/unit/test_maintenance_run.py` and `tests/unit/test_kms_contracts.py`; updated `tests/test-plan.md` and `tests/design-traceability.md` to point `TEST-001` and `TEST-005` to concrete files. | Replace placeholder-only validation with deterministic unit coverage tied to the existing test plan. | `DEV-012`, `TEST-001`, `TEST-005` | `review gaps`
- `DEV-013` | `2026-05-10` | `contract validation` | Updated validation planning and traceability to check the 11-step lifecycle, retired ID prefix absence, retired support path removal, and reusable `.codex` consistency. | Ensure the workflow cleanup is testable and repeatable. | `DEV-013`, `TEST-006` | `user prompt`
