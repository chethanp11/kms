# Design Traceability

## Purpose
Map intent, requirements, design constraints, tests, feedback, and issues into one usable traceability view.

## Traceability matrix
| Intent sections | Flow area | Requirement ID | Design constraints | Test IDs | Feedback / issues | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Source intake and finalization | `REQ-001`, `REQ-003`, `REQ-005` | Raw-source immutability, governed maintenance, wiki publication boundary | `TEST-001`, `TEST-005` | `DEV-*` | Source intake, source notes, and governed finalization coverage; concrete unit coverage exists in `tests/unit/test_maintenance_run.py` and `tests/unit/test_kms_contracts.py` |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Contradiction handling and bounded automation | `REQ-002`, `REQ-007` | Policy gates, review states, and agent/service handoff controls | `TEST-002`, `TEST-006` | `DEV-*` | Contradiction handling, policy gating, and bounded automation coverage |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Browse-only navigation | `REQ-004` | Read-only Infopedia projection over finalized wiki content | `TEST-003` | `DEV-*` | Browse-only Infopedia and projection coverage |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Auditability and failure handling | `REQ-006` | Traceability, explicit failure handling, and preserved operational evidence | `TEST-004` | `DEV-*` | Auditability, failure handling, and manual review coverage |
| `intent/product-intent.md` | Current scaffold alignment | `REQ-014` | Current `src/` scaffold is limited to existing base modules; no new top-level component families unless future plan/design proves necessity | `TEST-014` | `DEV-014` | Corrects stale plan/test drift and removes references to absent scaffold modules |

## Guidelines
- Add a row for every new requirement.
- Keep `REQ-*`, `DEV-*`, and `TEST-*` references current.
- Use this document to find missing coverage before implementation is called complete.
- When a behavior is deliberately deferred, mark the gap instead of leaving the row incomplete.
