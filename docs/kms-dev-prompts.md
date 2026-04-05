# KMS Development Prompts

These prompts are derived from `docs/kms-system-design.md`, especially Section 10. Run them sequentially. Each prompt assumes prior prompts have already been executed and the repo has been updated accordingly. Each work order includes `Plan`, `Develop`, `Validate`, and `Fix` phases so Codex can execute in agentic mode without guessing scope or sequencing.

## Prompt 1 — Repository Scaffold and Shared Foundations

Purpose: establish the repo layout, shared conventions, and baseline tooling that every later phase will depend on.

Depends on: none.

```text
You are working in the KMS repository. Read Section 10 of docs/kms-system-design.md before making changes. Inspect the current repo state first and do not assume any code already exists beyond the design doc.

Use `docs/kms-system-design.md` as the source of truth.

Goal: create the initial repository scaffold and shared foundations required for all later KMS work. This is phase 1 from the design doc.

### Plan
- Inspect docs/kms-system-design.md, especially Section 10.1 through 10.5.
- Identify the minimum repo structure needed for /apps/api, /apps/worker, /apps/kmi, /apps/infopedia, /packages/domain, /packages/shared, /packages/config, /agents, /rules, /templates, /wiki, /raw, /tests, /docs, and /scripts.
- Confirm what package manager, language, and test tooling are already present, if any.
- Avoid implementing domain logic yet; this prompt is about scaffold and conventions.

### Develop
- Create or update the top-level directory structure that matches the system design.
- Add baseline shared configuration, linting, formatting, type-checking, and test harness files appropriate to the repo’s existing stack.
- Add starter package manifests, workspace configuration, environment examples, and developer scripts as needed.
- Create placeholder README or stub files only where they are needed to make the repo structure explicit.
- Establish shared naming conventions, status enum conventions, and module boundary expectations in reusable config or documentation files.

### Validate
- Verify the scaffold matches Section 10.2 and 10.5 of the design doc.
- Confirm imports, package resolution, and workspace configuration are internally consistent.
- Confirm /wiki remains treated as canonical content storage and /raw as immutable input.
- Confirm there are no build or lint regressions from the scaffold changes.

### Fix
- Resolve missing directories, broken workspace references, inconsistent naming, or tooling mismatches.
- Remove or adjust any scaffold artifacts that would confuse later phases.
- Leave the repo in a clean foundation state for database and domain modeling work.

Execute Prompt 1 now.
```

## Prompt 2 — Metadata Database, Core Models, and Migrations

Purpose: implement the authoritative operational data model that supports runs, revisions, approvals, contradictions, and projections without replacing `/wiki` as truth.

Depends on: Prompt 1.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 9 and 10 before making changes. Build only the metadata and domain model slice for phase 2.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the existing scaffold and shared conventions from Prompt 1.
- Map the core metadata entities from Section 9.3 and the phase 2 deliverables from Section 10.4.
- Identify the files needed for migrations, ORM/Pydantic/domain models, repositories, and seed data.
- Do not add ingestion, UI, or search logic in this prompt.

### Develop
- Implement the metadata database schema and migrations for Run, SourceFile, SourceDocument, WikiPage, WikiPageRevision, ImpactRecord, ContradictionRecord, QAReport, ApprovalRecord, LintFinding, InfopediaNode, and SearchDocument as needed.
- Add shared status enums and identifiers consistent with the design doc.
- Implement repository-layer contracts and basic service access patterns for creating and querying metadata.
- Add seed or fixture data only when needed to validate model shape and relationships.
- Keep `/wiki` content separate from metadata persistence.

### Validate
- Verify the model reflects Section 9.4, 9.5, and 9.6.
- Confirm migrations are reversible and entity relationships are coherent.
- Confirm metadata entities support operational control only and do not become a knowledge truth store.
- Run schema, type, and repository-level validation.

### Fix
- Resolve schema mismatches, missing foreign keys, enum inconsistencies, or migration issues.
- Adjust model boundaries if any entity starts duplicating canonical wiki content.
- Leave the repo ready for source discovery and ingestion work.

Execute Prompt 2 now.
```

## Prompt 3 — Source Intake, Discovery, Parsing, and Intake Artifacts

Purpose: build the raw source discovery and parsing pipeline that turns `/raw` inputs into structured operational artifacts.

Depends on: Prompts 1–2.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 5, 9, and 10 before making changes. Implement phase 3 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the metadata model and scaffold established by prior prompts.
- Identify the source discovery, parsing, and normalization modules that fit the repository structure.
- Confirm how raw filesystem inputs are mounted and treated as immutable.
- Avoid adding wiki writing, governance, or UI code in this prompt.

### Develop
- Implement source discovery over /raw and register discovered files in metadata.
- Add parsers/normalizers for supported source types and classify unsupported files explicitly.
- Persist parse outputs, source documents, source notes, and run-level intake artifacts.
- Add orchestration-ready service boundaries for discovery and parsing so later phases can consume them.
- Make the intake pipeline deterministic and auditable.

### Validate
- Verify source discovery and parsing align with Section 5 and Section 9.7.
- Confirm raw inputs are never modified in place.
- Confirm supported and unsupported file handling is explicit and testable.
- Run parser, discovery, and metadata integration tests.

### Fix
- Repair path handling, parse failures, artifact persistence issues, or missing metadata links.
- Normalize naming and status behavior if it diverges from earlier phases.
- Leave the repo ready for wiki draft generation and template work.

Execute Prompt 3 now.
```

## Prompt 4 — Wiki Schema, Templates, Markdown Services, and Canonical Page Handling

Purpose: implement the canonical page layer that writes finalized wiki content through governed services and structured templates.

Depends on: Prompts 1–3.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 4, 5, 9, and 10 before making changes. Implement phase 4 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the current source intake outputs and metadata entities.
- Determine the markdown templates and wiki page conventions required by the design doc.
- Identify the service boundaries for draft creation, revision writing, and canonical page handling.
- Do not implement policy approval logic yet except what is required to support draft and revision creation.

### Develop
- Add canonical markdown templates and page blueprints in /templates.
- Implement wiki draft generation and revision writing services that convert structured outputs into finalized page content.
- Add page path/slug conventions and canonical page handling logic.
- Create fixtures for representative canonical page types and output shapes.
- Ensure all wiki writes flow through governed services and write to /wiki only when allowed by later phases.

### Validate
- Verify templates and markdown output align with Section 4 and Section 10.4.
- Confirm page generation is deterministic and testable.
- Confirm no direct or ad hoc /wiki write path bypasses the service boundary.
- Run golden tests for markdown generation and page path handling.

### Fix
- Resolve markdown formatting issues, slug collisions, or template mismatches.
- Repair any coupling between draft generation and unsupported storage layers.
- Leave the repo ready for governance and validation gates.

Execute Prompt 4 now.
```

## Prompt 5 — Governance Engine, Validation Rules, and Approval Gates

Purpose: implement the policy enforcement spine that blocks invalid publication and surfaces review requirements.

Depends on: Prompts 1–4.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 7, 9, and 10 before making changes. Implement phase 5 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the wiki draft service and metadata entities from prior prompts.
- Map rule execution, validation stages, contradiction handling, and approval gates to concrete backend services.
- Identify the rule files under /rules that should be loaded by runtime validation.
- Do not build UI screens yet; this prompt is about backend governance.

### Develop
- Implement the rules loader for /rules/*.yaml and the policy validation service.
- Add source trace validation, contradiction gating, approval gating, and QA report generation.
- Add explicit failure states and block/escalate decisions that align with Section 7.
- Ensure no rule, service, or API path can bypass governance before finalization.

### Validate
- Verify behavior against Section 7.4 through 7.13 and Section 9.8.
- Confirm publish attempts are blocked when required validation fails.
- Confirm approval decisions are recorded as metadata, not inferred from UI state.
- Run rule engine tests, validation tests, and approval gate tests.

### Fix
- Repair rule parsing, severity handling, or blocked-state propagation.
- Remove any accidental bypass path to /wiki publication.
- Leave the repo ready for orchestration and agent integration.

Execute Prompt 5 now.
```

## Prompt 6 — Agents, Skills, Orchestration, and Run Lifecycle Integration

Purpose: wire the run lifecycle, bounded automation, and skill/agent integration through governed services.

Depends on: Prompts 1–5.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 6, 7, 9, and 10 before making changes. Implement phase 6 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the established backend services for discovery, drafting, and governance.
- Identify the run orchestration jobs and agent/skill boundaries required by the design doc.
- Confirm what state transitions and audit events need to be emitted.
- Avoid creating autonomous behavior outside governed services.

### Develop
- Implement run orchestration jobs and lifecycle state transitions.
- Add bounded agent execution wrappers and skill invocation boundaries.
- Connect orchestration to source discovery, parsing, draft generation, validation, contradiction handling, and approval readiness.
- Emit audit events and lifecycle records for each meaningful stage transition.
- Keep agent behavior constrained to service contracts and policy outcomes.

### Validate
- Verify orchestration matches Section 6 and Section 10.3/10.4.
- Confirm run lifecycle states are visible and consistent across metadata and API layers.
- Confirm agents cannot bypass governance or write directly to /wiki.
- Run orchestration, stage-transition, and integration tests.

### Fix
- Repair stage sequencing, event emission, or handoff contracts.
- Remove any direct coupling between agents and canonical storage.
- Leave the repo ready for KMI review workflows.

Execute Prompt 6 now.
```

## Prompt 7 — Knowledge Manager Interface (KMI) Core Screens and Review Workflows

Purpose: build the governed maintenance UI for the Knowledge Manager using the stable backend contracts.

Depends on: Prompts 1–6.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 8, 9, and 10 before making changes. Implement phase 7 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the backend APIs and state models established by prior prompts.
- Map KMI screens to the UX architecture and workflow states in the design doc.
- Determine the minimal route structure and component responsibilities needed for dashboard, run detail, diff review, contradictions, approvals, and health views.
- Do not implement Infopedia yet except where shared UI primitives are unavoidable.

### Develop
- Build the KMI dashboard, run detail, source review, diff review, contradictions/open questions, approvals/finalization, and maintenance health screens.
- Wire the screens to stable backend APIs and metadata state.
- Show rule violations, source trace indicators, and approval blockers explicitly.
- Keep all maintenance actions workflow-driven and bounded by governance.
- Ensure the UI reflects that /wiki is canonical and that KMI is the only sanctioned maintenance surface.

### Validate
- Verify route and screen behavior matches Section 8.4 through 8.12.
- Confirm the UI does not expose direct edit paths that bypass the workflow.
- Confirm state, review, and approval flows use backend contracts rather than local mock state.
- Run UI integration and workflow tests.

### Fix
- Repair broken bindings, route mismatches, missing loading states, and inconsistent status displays.
- Remove any accidental write surface outside governed actions.
- Leave the repo ready for Infopedia browse and read-only experience work.

Execute Prompt 7 now.
```

## Prompt 8 — Infopedia Navigation, Search, and Read-Only Page Experience

Purpose: build the browse-only consumer surface over finalized wiki content and derived projections.

Depends on: Prompts 1–7.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 8, 9, and 10 before making changes. Implement phase 8 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the finalized wiki content paths, page metadata, and Infopedia projection requirements.
- Determine the route structure and component responsibilities for tree navigation, search, page view, related pages, and filters.
- Confirm what data should be read-only and what should be derived from projections.
- Do not add maintenance actions or editing paths to Infopedia.

### Develop
- Build Infopedia tree navigation, search results, page view, related pages/backlinks, filters, and freshness/status indicators.
- Render finalized markdown from /wiki and surface derived metadata only.
- Use the projection data model for navigation while keeping it clearly separate from truth.
- Make the surface read-only and consumer-oriented.

### Validate
- Verify the browse flow matches Section 8.13 through 8.18 and Section 9.12.
- Confirm Infopedia cannot mutate finalized knowledge.
- Confirm page rendering and search behavior are backed by stable service contracts.
- Run browse, navigation, and read-only UI tests.

### Fix
- Repair navigation links, status display issues, and search result mismatches.
- Remove any hidden maintenance control from the consumer surface.
- Leave the repo ready for indexing and end-to-end workflow wiring.

Execute Prompt 8 now.
```

## Prompt 9 — Search/Index Projections, Integration Flows, and End-to-End Workflow Wiring

Purpose: connect the backend, UI, and projections into a coherent end-to-end KMS workflow.

Depends on: Prompts 1–8.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 9 and 10 before making changes. Implement phase 9 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the current metadata, wiki draft, governance, KMI, and Infopedia implementations.
- Map how search documents and navigation projections should be derived from /wiki and metadata.
- Identify integration gaps between run completion, publish, index refresh, and UI reflection.
- Avoid changing canonical content semantics; this prompt is about projection wiring.

### Develop
- Implement search/index document projection and Infopedia node projection refresh jobs.
- Wire publish completion to projection refresh and retrieval consistency checks.
- Add backend integration flows that connect run completion, approval, publish, and browse/search visibility.
- Ensure KMI operational search and Infopedia browse/search are backed by derived projections, not direct storage shortcuts.

### Validate
- Verify projection logic matches Section 9.11 and 9.12.
- Confirm index refresh does not alter /wiki truth.
- Confirm the UI and backend flow from run to publish to browse/search are internally consistent.
- Run projection, integration, and end-to-end workflow tests.

### Fix
- Repair stale index refresh, projection drift, or missing integration hooks.
- Remove any shortcut that treats search or projection stores as canonical.
- Leave the repo ready for final hardening, deployment, and validation sweep.

Execute Prompt 9 now.
```

## Prompt 10 — Testing, Hardening, Local Deployment, Validation Sweep, and Gap Fixing

Purpose: finish the implementation with serious test coverage, local deployment readiness, operational signals, and cleanup of any remaining gaps.

Depends on: Prompts 1–9.

```text
You are working in the KMS repository. Read docs/kms-system-design.md Sections 10 and the prior sections before making changes. Implement phase 10 only.

Use `docs/kms-system-design.md` as the source of truth.

### Plan
- Inspect the whole repo for missing tests, fixture gaps, deployment gaps, and authority-boundary violations.
- Compare the implementation against docs/kms-system-design.md end to end.
- Identify what must be hardened before the repository can be used as a buildable KMS baseline.
- Do not introduce new features; focus on verification, polish, and gap closure.

### Develop
- Add or expand unit, integration, end-to-end, golden, regression, and fixture-based tests.
- Add realistic fixtures for raw sources, wiki pages, contradictions, approval cases, and lint failures.
- Add local startup scripts, health checks, environment examples, and developer documentation as needed.
- Strengthen observability, structured logging, and validation surfaces where the implementation is incomplete.
- Close the last-mile gaps so the system behaves like a coherent KMS baseline.

### Validate
- Verify the implementation is consistent with docs/kms-system-design.md across Sections 1 through 10.
- Confirm /wiki remains canonical, governance remains enforced, and no UI or API bypass exists.
- Confirm local development can run the API, worker, metadata DB, KMI, and Infopedia together.
- Run the full test suite and any smoke checks relevant to the repo’s stack.

### Fix
- Repair broken imports, schema mismatches, missing configs, flaky tests, and inconsistent naming.
- Close any remaining integration, deployment, or observability gaps.
- Leave the repo in the cleanest possible state for ongoing development or code generation.

Execute Prompt 10 now.
```
