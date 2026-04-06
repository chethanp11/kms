# UX Flows

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Describe the main user and operator flows, including failure paths and manual intervention points.

## Intent sources
- `intent/product-intent.md`
- `intent/feedback-intent.md`
- `intent/iteration-intent.md`

## Rules
- Keep each flow tied to one primary user goal.
- Include at least one failure path where the AI cannot or should not continue.
- Link each flow to the relevant requirements and acceptance criteria.

## Flow catalog
| Flow | Primary actor | Trigger | Normal path | Failure or exception path | Human review point | Linked IDs |
| --- | --- | --- | --- | --- | --- | --- |
| KMI maintenance run | Knowledge Manager | A source folder is ready for curation | Manager submits a source path, KMI discovers raw inputs, the orchestrator drafts wiki updates, and approved changes are published to `/wiki` | Source scan fails, markdown is invalid, or the proposal is held pending review | Knowledge Manager approves, rejects, or escalates the proposal | `REQ-001`, `ACC-001`, `AI-001`, `AI-005` |
| Contradiction review | Knowledge Manager | The run detects ambiguity, conflicting facts, or low-confidence claims | The proposal is shown with source trace, contradiction flags, and a recommendation | The run halts before publication if the issue cannot be resolved safely | Knowledge Manager decides whether to revise, reject, or escalate | `REQ-002`, `ACC-002`, `AI-002`, `AI-004` |
| Infopedia browse | Knowledge Consumer | A published topic needs to be read | Consumer opens Infopedia, searches or browses the tree, and reads finalized markdown | Requested page is unpublished or missing, or a write attempt is blocked | None for normal browse; escalation only if content is missing or stale | `REQ-003`, `ACC-003`, `AI-006` |
| Audit review | Knowledge Manager or reviewer | A prior run needs explanation | Reviewer opens the run record, sees source trace, decision state, and validation evidence | Evidence is incomplete or missing, which blocks confident closeout | Reviewer flags the gap for follow-up | `REQ-004`, `ACC-004`, `AI-005` |
| Dependency failure | System | Source discovery, parsing, or publication breaks | The run reports the failed step and preserves state for retry or review | The system refuses to publish partial or untraceable knowledge | Knowledge Manager may inspect and decide next steps | `REQ-002`, `REQ-004`, `ACC-004`, `AI-004` |

## Notes
- Keep step detail high enough that a tester could turn the flow into `TEST-*` or `EVAL-*` coverage.
- If a flow changes user-visible behavior, update acceptance criteria and traceability in the same pass.
