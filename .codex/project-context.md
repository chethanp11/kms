# KMS Project Context

This file is the project-specific operating and design context for KMS. It must stay in sync with `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md`.

For AppFlow reuse in a new application, this file and `.codex/tech-stack.md` are the only files expected to require project-specific edits.

## Product Identity

KMS is a governed Knowledge Management System that turns immutable raw source material into finalized markdown knowledge under Knowledge Manager control.

The system publishes finalized knowledge to `/wiki` and exposes that knowledge through a separate read-only navigation layer called Infopedia. Raw source inputs are evidence, not finalized truth.

## Core Product Layers

1. **Raw source input layer**: immutable upstream evidence from local or mounted source folders.
2. **Knowledge Maintenance Layer / KMI**: governed maintenance UI and workflow surface for Knowledge Managers.
3. **Finalized Knowledge Layer / `/wiki`**: canonical markdown knowledge store and source of truth.
4. **Knowledge Navigation Layer / Infopedia**: read-only browse/search experience over finalized knowledge.
5. **Metadata and runtime services**: operational state for runs, approvals, contradictions, revisions, validation, search, and projections.

## Users and Authority

- **Knowledge Managers** own review, approval, contradiction resolution, and finalization decisions through KMI.
- **Knowledge Consumers** use Infopedia to browse and search finalized knowledge but cannot mutate `/wiki`.
- **Downstream AI systems** may consume governed knowledge through retrieval paths, but must not write finalized truth or bypass source trace and approval boundaries.

AI agents may propose, compare, validate, and review; they must not silently finalize truth.

## Source of Truth and Precedence

When KMS artifacts disagree, use this order:

1. user prompt and `.codex/state/current-intent.md` for the active turn
2. `.codex/project-context.md` and `.codex/tech-stack.md`
3. `plan/*`
4. `design/*`
5. `tests/*`
6. implementation source
7. `dev_log/*`
8. optional project-owned intent or feedback artifacts when explicitly maintained for the application

Current-turn intent is prompt-derived, not pre-filled. If project-owned intent or feedback artifacts exist, treat them as supporting context only; do not edit them unless explicitly asked. Use gap records only for evidence-backed system-detected follow-up.

## Repository Map

- `intent/`: optional project-owned intent, feedback, and evidence-backed gaps when the application maintains those artifacts.
- `plan/`: current iteration work split into design, code, and test updates.
- `design/`: detailed KMS design layer.
- `src/`: current implementation scaffold; future runtime code should align to the structure in `.codex/tech-stack.md`.
- `tests/`: validation plans, traceability, fixtures, and test suites.
- `dev_log/`: permanent execution and validation record.
- `.codex/dev_workflow/`: reusable AppFlow lifecycle prompts.
- `.codex/skills/`: scoped procedures used only when a task matches their scope.
- `.codex/agents/`: bounded role contracts.
- `.codex/orchestration/`, `.codex/tools/`, and `.codex/state/`: reusable AppFlow support infrastructure.

Only implementation/runtime source is intended for production deployment. AppFlow control-plane artifacts guide development, validation, traceability, and governance.

## Design Document Map

- `design/system-design.md`: product vision, roles, operating model, and core workflows.
- `design/architecture.md`: layered architecture, runtime services, metadata model, API surface, repository structure, and implementation phases.
- `design/ux-flows.md`: KMI and Infopedia information architecture, user journeys, UI boundaries, and backend interaction expectations.
- `design/acceptance-criteria.md`: governance model, validation gates, HITL approval, contradiction handling, audit, and policy enforcement.

Keep these files complementary. Do not let code redefine behavior without a corresponding design and validation update.

## KMS Architecture Boundaries

- Raw sources are immutable upstream evidence and never finalized truth.
- `/wiki` is the canonical finalized markdown knowledge substrate.
- KMI is the only governed maintenance and approval surface.
- Infopedia is read-only and must not mutate finalized knowledge.
- Metadata databases, indexes, projections, and artifacts are operational support and must not replace `/wiki`.
- All `/wiki` writes must go through governed services, validation gates, and required approval.
- Search and Infopedia projections are rebuildable derived views, not authoritative stores.
- UI clients must use API contracts; they must not access persistence directly.

## Runtime Service Model

KMS runtime behavior is organized around bounded services:

- API service
- run orchestration service
- source discovery and parsing services
- knowledge understanding service
- source analysis service
- wiki draft/refresh service
- policy validation service
- contradiction service
- approval service
- publisher service
- lint/health service
- search/index service
- Infopedia projection service

Service boundaries should preserve auditability, idempotency, explicit failure states, and governance checks.

## Workflow Expectations

For KMS product work, follow:

user prompt → current-turn intent → `.codex/project-context.md` / `.codex/tech-stack.md` → `plan/*` → `design/*` → `tests/*` → implementation → validation → `dev_log/*` → evidence-backed gaps when needed.

Implementation must follow approved plan, design, and validation artifacts. Code must not invent requirements.

## Validation and Governance Expectations

KMS validation must prove source-trace integrity, approval gating, contradiction handling, deterministic markdown output, read-only Infopedia behavior, and no direct mutation of finalized knowledge outside governed publish paths.

AI-assisted understanding outputs are governed intermediate artifacts only. Candidate entities, processes, metrics, decisions, concepts, contradictions, confidence scores, relevance scores, and candidate drafts may support review and draft preparation, but they are not finalized knowledge and cannot mutate `/wiki` without deterministic validation and Knowledge Manager approval.

Validation evidence belongs in `dev_log/validation-results.md` after checks are actually run. Do not fabricate validation evidence.

## Stop Conditions

Stop and surface the issue when:

- KMS source-of-truth artifacts conflict and cannot be safely reconciled
- validation fails and the root cause is not understood
- a change would bypass KMS governance or publication boundaries
- a human-owned intent decision is missing
- implementation would make supporting stores authoritative over `/wiki`
