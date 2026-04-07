# Design Traceability

## Purpose
Map intent, requirements, architecture constraints, tests, feedback, and issues into one usable traceability view.

## Traceability matrix
| Intent sections | UX flow ID | Requirement ID | Acceptance ID | Design constraints | Test IDs | Feedback / issues | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `INT-PROD-*`, `INT-FB-*` | `UXF-001` | `REQ-001`, `REQ-003`, `REQ-005` | `ACC-001` | `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-008`, `ARCH-009` | `TEST-001`, `TEST-005` | `FB-*`, `DEV-*` | Source intake, source notes, and governed finalization coverage |
| `INT-PROD-*`, `INT-FB-*` | `UXF-002` | `REQ-002`, `REQ-007` | `ACC-002` | `ARCH-006`, `ARCH-007` | `TEST-002`, `TEST-006` | `FB-*`, `DEV-*` | Contradiction handling, policy gating, and bounded automation coverage |
| `INT-PROD-*`, `INT-FB-*` | `UXF-003` | `REQ-004` | `ACC-003` | `ARCH-010`, `ARCH-012` | `TEST-003` | `FB-*`, `DEV-*` | Browse-only Infopedia and projection coverage |
| `INT-PROD-*`, `INT-FB-*` | `UXF-004`, `UXF-005` | `REQ-006` | `ACC-004` | `ARCH-011` | `TEST-004` | `FB-*`, `DEV-*` | Auditability, failure handling, and manual review coverage |

## Guidelines
- Add a row for every new requirement and acceptance criterion.
- Keep `TEST-*`, `FB-*`, and `DEV-*` references current.
- Use this document to find missing coverage before implementation is called complete.
- When a behavior is deliberately deferred, mark the gap instead of leaving the row incomplete.
