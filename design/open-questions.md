# Open Questions

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Track unresolved questions that block or materially affect design, implementation, testing, evaluation, or release readiness.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`
- `intent/feedback-intent.md`

## Rules
- Use `DEV-*` IDs so questions are traceable alongside other operational records.
- Mark blocking questions clearly.
- Link each question to the artifacts it could invalidate.
- Close the question only when the answer is reflected in design, tests, or logs.

## Question register
| ID | Area | Blocking | Question | Impact | Next step | Linked IDs | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DEV-011` | `design` | `yes` | What is the first implementation surface for KMI: CLI, API, or web UI? | It affects the interface contract, test shape, and how the Knowledge Manager starts runs. | Decide during implementation planning. | `REQ-001`, `API-001`, `TEST-001` | `open` |
| `DEV-012` | `design` | `yes` | Which source file types and folder conventions are guaranteed in v0.1? | It affects source discovery, parsing rules, and contradiction detection. | Define the supported source bundle shape before implementation. | `REQ-001`, `DATA-001`, `TEST-001`, `EVAL-001` | `open` |
| `DEV-013` | `design` | `no` | Is `/wiki` local filesystem only in the first version, or is a remote sync path also required? | It affects publication adapters and operational risk, but not the core truth model. | Resolve when deployment scope is fixed. | `REQ-001`, `REQ-003`, `API-003` | `open` |
| `DEV-014` | `design` | `no` | What minimum metadata must every finalized page expose for source trace and freshness? | It affects how rich the publication record and audit trail must be. | Confirm during traceability and validation planning. | `REQ-004`, `DATA-004`, `DATA-006` | `open` |

## Current-use note
If the question affects user-visible behavior, treat it as blocking until the design is updated or the scope is reduced.
