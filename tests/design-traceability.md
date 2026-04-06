# Design Traceability

## Purpose
Map intent, requirements, architecture constraints, AI rules, tests, evals, and feedback into one usable traceability view.

## Traceability matrix
| Intent sections | Requirement ID | Acceptance ID | Design constraints | Test IDs | Eval IDs | Feedback / issues | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `INT-PROD-*`, `INT-ITER-*` | `REQ-001` | `ACC-001` | `ARCH-001`, `ARCH-002`, `AI-001`, `AI-003` | `TEST-001`, `TEST-003` | `EVAL-001` | `FB-*`, `DEV-*` | Source intake and proposal generation coverage |
| `INT-PROD-*`, `INT-CON-*` | `REQ-002` | `ACC-002` | `ARCH-003`, `AI-002`, `AI-004`, `AI-006` | `TEST-002` | `EVAL-002` | `FB-*`, `DEV-*` | Contradiction handling and review gating coverage |
| `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*` | `REQ-003` | `ACC-003` | `ARCH-004`, `ARCH-005`, `API-004`, `DATA-004` | `TEST-003` | `EVAL-003` | `FB-*`, `DEV-*` | Browse-only Infopedia and finalized wiki coverage |
| `INT-CON-*`, `INT-FB-*`, `INT-ITER-*` | `REQ-004` | `ACC-004` | `ARCH-006`, `DATA-001`, `DATA-002`, `DATA-005`, `DATA-006` | `TEST-004` | `EVAL-004`, `EVAL-005` | `FB-*`, `DEV-*` | Auditability, failure handling, and manual review coverage |

## Guidelines
- Add a row for every new requirement and acceptance criterion.
- Keep `TEST-*`, `EVAL-*`, `FB-*`, and `DEV-*` references current.
- Use this document to find missing coverage before implementation is called complete.
- When a behavior is deliberately deferred, mark the gap instead of leaving the row incomplete.
