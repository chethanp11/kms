# Code Update Log

## Purpose
Record meaningful code changes that were actually implemented.

## Intent linkage
- Capture implementation decisions that follow approved design.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Change: `[what code changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, DEV-xxx, TEST-xxx]`
- Intent sources: `[user prompt, intent/*, intent/gaps.md]`

## Entries
- `DEV-012` | `2026-05-10` | Added `.codex/tools/appflow_run.py`, expanded `.codex/tools/validate_codex_contract.py`, and introduced minimal KMS runtime modules in `src/contracts` and `src/execution`. | Provide executable lifecycle evidence checks, deeper semantic contract validation, and concrete runtime contracts for source discovery and knowledge-page validation. | `DEV-012`, `TEST-001`, `TEST-005` | `review gaps`
- `DEV-013` | `2026-05-10` | Updated `.codex/tools/appflow_run.py` and `.codex/tools/validate_codex_contract.py` to require `00-create-intent`, reject retired ID prefixes, and fail when retired support paths remain. | Make AppFlow lifecycle evidence and cleanup requirements deterministic instead of procedural only. | `DEV-013`, `TEST-006` | `user prompt`
- `DEV-014` | `2026-05-10` | Added initial standard-library KMS scaffold under `src/` with contracts, execution, governance, orchestration, API endpoint inventory, context boundaries, agent role names, and audit-event helpers. | Create a concrete implementation starting point aligned to the design while preserving governed `/wiki`, raw-source, KMI, and Infopedia boundaries. | `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added foundational component primitives in `src/components`, explicit ports in `src/ports`, deterministic in-memory stores in `src/storage`, and exported the base registry from `src`. | Provide stable base contracts for future KMS services, stores, projections, governance gates, and adapters while preserving `/wiki`, metadata, raw-source, and Infopedia authority boundaries. | `DEV-015`, `TEST-015` | `user prompt`
- `DEV-014` | `2026-05-10` | Corrected `src/__init__.py` to export only modules present in the current scaffold. | Remove stale references to absent component-family modules without adding unneeded new `src` components. | `REQ-014`, `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added top-level `scripts/` scaffold with `README.md`, `__init__.py`, and `validate_scaffold.py`. | Provide deterministic project scaffold validation without adding new `src` component families. | `REQ-015`, `DEV-015`, `TEST-015` | `user prompt`
- `DEV-016` | `2026-05-10` | Added `src/components/` with metadata-only scaffolds for every design component and updated scaffold validation to require them. | Provide component anchors for future implementation while preserving KMS authority boundaries. | `REQ-016`, `DEV-016`, `TEST-016` | `user prompt`
- `DEV-017` | `2026-05-10` | Deleted `src/components/` and added blank/minimal scaffold files under `apps/`, `packages/`, `config/`, `agents/`, `rules/`, `templates/`, `wiki/`, `raw/`, `docs/`, and `scripts/`. | Prepare target project folders for future prompts to populate concrete implementation. | `REQ-017`, `DEV-017`, `TEST-017` | `user prompt`
- `DEV-018` | `2026-05-10` | Removed `src/components/` and outside-`src` scaffold folders; added detailed `src/`-only runtime scaffold files for API, worker, domain, services, storage, KMI, Infopedia, config, agents, rules, templates, observability, orchestration, execution, governance, and scripts. | Prepare the actual KMS runtime code tree for future prompts to populate. | `REQ-018`, `DEV-018`, `TEST-018` | `user prompt`
- `DEV-019` | `2026-05-11` | Added `src/contracts/__init__.py` with stdlib dataclass contracts and enums for runs, sources, documents, wiki pages, revisions, approvals, contradictions, QA reports, lint findings, Infopedia nodes, and search documents; re-exported governance QA contracts and restored minimal `src/context.py` constants required by existing scaffold tests. | Complete the core domain contract layer without adding new component families or runtime dependencies. | `REQ-019`, `DEV-019`, `TEST-019` | `user prompt`, `intent/product-intent.md`
- `DEV-020` | `2026-05-11` | Populated placeholder modules under `src/` with a stdlib-first KMS runtime slice: settings, stores, services, orchestration, API routes, workers, agents, rules, scripts, audit/health helpers, and approval-gated publish flow. | Create a working KMS application implementation aligned to the design while preserving `/wiki` authority, metadata/search/projection support boundaries, and fail-closed governance. | `REQ-020`, `DEV-020`, `TEST-020` | `user prompt`, `intent/product-intent.md`
- `DEV-021` | `2026-05-12` | Added `KnowledgeCandidate` and `CandidateDraft` contracts, deterministic knowledge-understanding extraction, relevance/confidence scoring, candidate review/draft artifacts, metadata storage, an agent facade, and Run lifecycle artifact wiring. | Implement bounded AI-assisted understanding as inspectable proposal artifacts without granting direct publish authority. | `REQ-021`, `DEV-021`, `TEST-021` | `user prompt`, `intent/product-intent.md`
