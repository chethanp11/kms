# Test Plan

## Purpose
Define how the current scope will be validated and which test layers are responsible for proving it.

## Planning rules
- Plan tests from intent-derived design, not from implementation convenience.
- Add a `TEST-*` row for each meaningful validation item.
- Link each `TEST-*` to `ACC-*` and any relevant `AI-*`, `API-*`, or `DATA-*` constraints.
- If the behavior cannot be proven well with ordinary tests, map it to `EVAL-*` and state the manual or hybrid review method.

## Validation inventory
| ID | Layer | Purpose | Linked IDs | Artifact or location | Owner |
| --- | --- | --- | --- | --- | --- |
| `TEST-001` | `unit` | Validate maintenance run normalization, source bundle discovery, and proposal metadata creation against the AI and data contracts. | `ACC-001`, `AI-001`, `AI-003`, `DATA-001`, `DATA-003` | `tests/unit/` | Knowledge Manager or platform engineer |
| `TEST-002` | `integration` | Verify contradiction routing, review-state transitions, and publication gating across the governance path. | `ACC-002`, `ARCH-003`, `API-002`, `DATA-005` | `tests/integration/` | Knowledge Manager or platform engineer |
| `TEST-003` | `e2e` | Confirm the supported browse flow from finalized wiki content into Infopedia and ensure it is read-only. | `ACC-003`, `REQ-003`, `ARCH-004`, `ARCH-005`, `API-004`, `DATA-004` | `tests/e2e/` | Knowledge Manager or platform engineer |
| `TEST-004` | `regression` | Guard against audit, traceability, and failure-handling regressions after approval, rejection, escalation, or dependency failure. | `ACC-004`, `DEV-*`, `DATA-002`, `DATA-006` | `tests/regression/` | Knowledge Manager or platform engineer |

## Coverage checks
- Does each acceptance item have at least one proving artifact?
- Are failure paths tested as well as happy paths?
- Is at least one regression artifact added for each resolved major defect?
- Are eval-only behaviors clearly marked so they are not mistaken for unit-test coverage?
