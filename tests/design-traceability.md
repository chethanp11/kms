# Design Traceability

## Purpose
Map intent, requirements, architecture constraints, tests, feedback, and issues into one usable traceability view.

## Traceability matrix
| Intent sections | Requirement ID | Acceptance ID | Design constraints | Test IDs | Feedback / issues | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `INT-PROD-*`, `INT-FB-*` | `REQ-001` | `ACC-001` | `ARCH-001`, `ARCH-002` | `TEST-001`, `TEST-003` | `FB-*`, `DEV-*` | Source intake and proposal generation coverage |
| `INT-PROD-*`, `INT-FB-*` | `REQ-002` | `ACC-002` | `ARCH-003` | `TEST-002` | `FB-*`, `DEV-*` | Contradiction handling and review gating coverage |
| `INT-PROD-*`, `INT-FB-*` | `REQ-003` | `ACC-003` | `ARCH-004`, `ARCH-005` | `TEST-003` | `FB-*`, `DEV-*` | Browse-only Infopedia and finalized wiki coverage |
| `INT-PROD-*`, `INT-FB-*` | `REQ-004` | `ACC-004` | `ARCH-006` | `TEST-004` | `FB-*`, `DEV-*` | Auditability, failure handling, and manual review coverage |

## Guidelines
- Add a row for every new requirement and acceptance criterion.
- Keep `TEST-*`, `FB-*`, and `DEV-*` references current.
- Use this document to find missing coverage before implementation is called complete.
- When a behavior is deliberately deferred, mark the gap instead of leaving the row incomplete.
