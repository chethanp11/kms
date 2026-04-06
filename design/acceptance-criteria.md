# Acceptance Criteria

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Define what must be true for a scoped version or iteration to be considered acceptable.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`
- `intent/feedback-intent.md` when feedback changes acceptance expectations

## Rules
- Every `ACC-*` must map to at least one `REQ-*`.
- Every `ACC-*` must have a validation path through `TEST-*`, `EVAL-*`, or both.
- If acceptance depends on manual review, state the reviewer and pass condition explicitly.
- Acceptance criteria should describe observable behavior, not implementation preferences.

## Acceptance criteria
| ID | Requirement | Criterion | Validation path | Notes |
| --- | --- | --- | --- | --- |
| `ACC-001` | `REQ-001` | A maintenance run started from KMI over a local source path produces proposed markdown updates for affected wiki pages, with source references and change summaries visible in the run output. | `TEST-001`, `EVAL-001` | The run may remain unfinalized until review if the source set is incomplete or ambiguous. |
| `ACC-002` | `REQ-002` | When the system detects contradictions, low-confidence claims, or policy conflicts, it does not finalize knowledge automatically and instead requires the Knowledge Manager to approve, reject, or escalate the proposal. | `TEST-002`, `EVAL-002` | Manual review is part of the acceptance path. |
| `ACC-003` | `REQ-003` | Infopedia exposes finalized wiki content as read-only browse, search, and page-navigation surfaces, and does not provide a consumer path that can edit or publish knowledge. | `TEST-003`, `EVAL-003` | This criterion covers the separation between consumption and maintenance. |
| `ACC-004` | `REQ-004` | Every maintenance run leaves an audit trail that identifies the source path, proposal set, review decision or exception state, and the evidence needed to explain what changed or why nothing changed. | `TEST-004`, `EVAL-005` | Auditability must survive rejected, escalated, and failed runs. |

## Acceptance quality checks
- Is the criterion observable from outside the implementation?
- Does it describe success and not merely effort?
- Is the validation method realistic for this version?
- Does it avoid bundling unrelated behaviors into one line?

## Update rule
Keep the authoritative cross-reference in `tests/design-traceability.md`. This file should focus on the criteria themselves, not become the full audit log.
