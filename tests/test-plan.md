# Test Plan

## Purpose
Define how the current scope will be validated and which test layers are responsible for proving it.

## Planning rules
- Plan tests from intent-derived design, not from implementation convenience.
- Add a `TEST-*` row for each meaningful validation item.
- Link each `TEST-*` to `ACC-*`, the relevant `UXF-*`, and any relevant `ARCH-*` constraints.
- If the behavior cannot be proven well with ordinary tests, state the manual or hybrid review method in the plan.

## Validation inventory
| ID | Layer | Purpose | Linked IDs | Artifact or location | Owner |
| --- | --- | --- | --- | --- | --- |
| `TEST-001` | `unit` | Validate maintenance run normalization, source bundle discovery, proposal metadata creation, and source-note generation. | `UXF-001`, `ACC-001`, `REQ-001`, `REQ-003`, `REQ-005`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005` | `tests/unit/` | Knowledge Manager or platform engineer |
| `TEST-002` | `integration` | Verify contradiction routing, review-state transitions, publication gating, and blocked-finalization behavior. | `UXF-002`, `ACC-002`, `REQ-002`, `REQ-007`, `ARCH-006`, `ARCH-007`, `ARCH-008` | `tests/integration/` | Knowledge Manager or platform engineer |
| `TEST-003` | `e2e` | Confirm the supported browse flow from finalized wiki content into Infopedia and ensure it is read-only. | `UXF-003`, `ACC-003`, `REQ-004`, `ARCH-010`, `ARCH-012` | `tests/e2e/` | Knowledge Manager or platform engineer |
| `TEST-004` | `regression` | Guard against audit, traceability, and failure-handling regressions after approval, rejection, escalation, or dependency failure. | `UXF-004`, `UXF-005`, `ACC-004`, `REQ-006`, `ARCH-011` | `tests/regression/` | Knowledge Manager or platform engineer |
| `TEST-005` | `unit` | Validate knowledge-model schema, page typing, folder placement, and required frontmatter/body sections. | `REQ-005`, `ACC-001`, `ARCH-004`, `ARCH-005` | `tests/unit/` | Knowledge Manager or platform engineer |
| `TEST-006` | `integration` | Verify the bounded agent and service handoff model does not allow any single worker to bypass governance. | `REQ-007`, `ACC-002`, `ARCH-002`, `ARCH-006`, `ARCH-007` | `tests/integration/` | Knowledge Manager or platform engineer |

## Coverage checks
- Does each acceptance item have at least one proving artifact?
- Are failure paths tested as well as happy paths?
- Is at least one regression artifact added for each resolved major defect?
- Are manual-review behaviors clearly marked so they are not mistaken for unit-test coverage?
