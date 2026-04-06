# Architecture

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Translate `design/system-design.md` into concrete components, interfaces, responsibilities, and operational boundaries for governed knowledge maintenance and browse-only consumption.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`

## Scope of this file
- What components exist
- What each component owns
- How data and control move between components
- Where validation, logging, and failure handling occur
- What is intentionally deferred

## Architecture summary
- Runtime shape: local maintenance service plus read-only navigation surface
- Primary execution path: source-folder intake, proposal generation, human review, wiki publication, Infopedia browse
- Deployment assumptions: local-first with optional service boundaries around the maintenance workflow
- Observability assumptions: logs, run traces, validation evidence, and review records

## Component inventory
| ID | Component | Responsibility | Inputs | Outputs | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| `ARCH-001` | `KMI Interface Layer` | Accept a source path or maintenance command, validate it, and create a normalized maintenance run request. | source path, run options, operator identity | normalized maintenance command | bad input, missing path, unauthorized operation |
| `ARCH-002` | `Maintenance Orchestrator` | Discover source material, compare it with current `/wiki` content, draft knowledge proposals, and detect contradictions or freshness gaps. | normalized run request, source bundle, wiki snapshot | proposal set, contradiction signals, run summary | source scan failure, invalid markdown, unsupported input |
| `ARCH-003` | `Governance Review Service` | Present proposed changes, capture approve/reject/escalate decisions, and gate publication. | proposal set, validation evidence, policy rules | review decision, publication eligibility, open questions | policy conflict, unresolved contradiction, stalled review |
| `ARCH-004` | `Wiki Publication Layer` | Write approved markdown into `/wiki` and keep publication separate from consumer navigation. | approved proposal, publication command | finalized wiki pages, publication audit trail | write failure, conflict with existing page, stale approval |
| `ARCH-005` | `Infopedia Navigation Layer` | Provide read-only tree, search, and page navigation over finalized wiki content. | browse query, page reference, wiki index | rendered page, navigation tree, search results | missing page, stale index, unauthorized write attempt |
| `ARCH-006` | `Observability and Audit Layer` | Record source trace, decisions, freshness state, validation outcomes, and error conditions for later review. | events from all layers | audit records, validation evidence, operational logs | missing telemetry, incomplete trace, retention failure |

## Data and control flow
1. The KMI interface validates the operator request and creates a maintenance run.
2. The orchestrator discovers raw source material, loads the current wiki snapshot, and drafts proposals.
3. The governance service checks contradictions, gaps, and policy requirements, then requests human review if needed.
4. Approved changes move to the wiki publication layer, which writes finalized markdown under `/wiki`.
5. Infopedia reads the finalized wiki index and serves browse-only navigation and page views.
6. The observability layer records trace, state, review outcomes, and validation evidence across the run.

## Interface boundaries
- External interfaces must be documented in `design/api-contracts.md`.
- Shared schemas must be documented in `design/data-models.md`.
- Prompt and tool policies must be documented in `design/ai-behavior-spec.md`.

## Operational constraints
- Retry policy: bounded retries for source discovery and publication writes only
- Timeout policy: per run and per publication action, not unbounded background polling
- State model: durable workflow state for maintenance runs, with read-only browse state for Infopedia
- Secrets handling: credentials and tokens stay out of prompts and source bundles
- Human override path: Knowledge Manager review queue in KMI with explicit approve/reject/escalate actions

## Architecture risks
- Prompt drift or uncontrolled tool use
- Weak source provenance or stale wiki snapshots
- Hidden publication logic inside prompts
- Missing audit or replay data
- Coupling between maintenance and browse layers that would permit accidental writes
