# API Contracts

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Define external and internal interface contracts. Use this file for API, event, queue, tool adapter, or structured prompt I/O contracts that other components depend on.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`

## Rules
- Each contract gets an `API-*` ID.
- Shared payload schemas should reference `DATA-*` definitions from `design/data-models.md`.
- Contracts that influence prompting or tool calls should also link to `AI-*`.
- Version breaking changes belong in `design/change-history.md` and the active version brief.

## Contract catalog
| ID | Interface | Purpose | Caller | Response or output | Failure modes | Linked IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `API-001` | `StartMaintenanceRun` | Start a governed maintenance run from a local source path and current wiki snapshot. | KMI operator or workflow controller | `run_id`, source bundle summary, proposal summary, contradiction summary | invalid path, unsupported source type, unavailable source tree | `REQ-001`, `ACC-001`, `DATA-001`, `DATA-002`, `AI-001` |
| `API-002` | `ReviewKnowledgeProposal` | Capture a Knowledge Manager decision for a proposal set and determine whether publication is allowed. | Knowledge Manager | review decision, rationale, publication eligibility, escalation target | invalid state, missing evidence, stale proposal | `REQ-002`, `ACC-002`, `DATA-003`, `DATA-005`, `AI-002` |
| `API-003` | `PublishApprovedWikiPages` | Write approved markdown into `/wiki` as finalized knowledge. | Governance or publication service | finalized wiki page paths, publication audit record | write conflict, stale approval, filesystem failure | `REQ-001`, `REQ-004`, `ACC-001`, `ACC-004`, `DATA-004`, `DATA-006` |
| `API-004` | `BrowseInfopedia` | Return read-only tree, search, and page content for finalized wiki knowledge. | Knowledge Consumer or downstream AI reader | navigation tree, page markdown, search hits | missing page, unpublished content, unauthorized write attempt | `REQ-003`, `ACC-003`, `DATA-004`, `AI-005` |

## Per-contract checklist
- Input fields and required validation
- Output fields and confidence or provenance expectations
- Authentication or authorization rules if applicable
- Idempotency expectations if side effects are possible
- Retry safety and timeout behavior
- Logging or audit requirements

## AI-specific contract notes
- Keep prompt-facing inputs structured whenever possible.
- Separate user content, system context, and tool results.
- If the contract returns model output, specify whether it must be plain text, structured JSON, citations, or an action plan.
