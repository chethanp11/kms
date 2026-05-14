# Test Update Log

## Purpose
Record meaningful test changes that were actually applied.

## Intent linkage
- Capture the validation coverage that accompanies design and code changes.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Change: `[what test changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, DEV-xxx, TEST-xxx]`
- Intent sources: `[user prompt, intent/*, intent/gaps.md]`

## Entries
- `DEV-002` | `2026-04-07` | `test` | Updated the test planning guidance so every test traces back to a UX flow and correctness criteria, and adjusted the traceability expectations to surface flow-to-criteria-to-test coverage. | The new design chain requires tests to be derived from correctness criteria rather than invented independently. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`, `DEV-002` | `INT-PROD-*`, `INT-FB-*`, `intent/gaps.md`
- `DEV-012` | `2026-05-10` | `unit tests` | Added `tests/unit/test_maintenance_run.py` and `tests/unit/test_kms_contracts.py`; updated `tests/test-plan.md` and `tests/design-traceability.md` to point `TEST-001` and `TEST-005` to concrete files. | Replace placeholder-only validation with deterministic unit coverage tied to the existing test plan. | `DEV-012`, `TEST-001`, `TEST-005` | `review gaps`
- `DEV-013` | `2026-05-10` | `contract validation` | Updated validation planning and traceability to check the 11-step lifecycle, retired ID prefix absence, retired support path removal, and reusable `.codex` consistency. | Ensure the workflow cleanup is testable and repeatable. | `DEV-013`, `TEST-006` | `user prompt`
- `DEV-014` | `2026-05-10` | Added `tests/unit/test_scaffold_boundaries.py` for authority constants, representative API endpoints, policy gating, approval gating, and intake orchestration summary behavior. | Cover the new scaffold with deterministic unit tests before broader runtime dependencies are introduced. | `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added `tests/unit/test_foundational_components.py` for component registry behavior, dependency checks, port conformance, governed wiki writes, metadata persistence, and rebuildable projections. | Prove the new foundational components are deterministic and enforce KMS design boundaries. | `DEV-015`, `TEST-015` | `user prompt`
- `DEV-014` | `2026-05-10` | Updated test planning/traceability for current scaffold alignment and removed stale `tests/unit/test_foundational_components.py`. | Tests now reflect the current scaffold and no longer require absent component-family modules. | `REQ-014`, `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added `tests/unit/test_scripts_scaffold.py` for scripts scaffold validation. | Prove the new scripts scaffold boundary and validator are usable. | `REQ-015`, `DEV-015`, `TEST-015` | `user prompt`
- `DEV-016` | `2026-05-10` | Added `tests/unit/test_component_scaffolds.py` and updated script scaffold tests for all component packages. | Prove every design component has a scaffold and read-only/projection boundaries do not write `/wiki`. | `REQ-016`, `DEV-016`, `TEST-016` | `user prompt`
- `DEV-017` | `2026-05-10` | Updated scaffold validation and unit tests to require target-layout blank files and reject `src/components`. | Prove the corrected scaffold interpretation and prevent reverting to component metadata packages. | `REQ-017`, `DEV-017`, `TEST-017` | `user prompt`
- `DEV-018` | `2026-05-10` | Replaced stale component/script scaffold tests with `tests/unit/test_src_runtime_scaffold.py`. | Validate the corrected `src/`-only scaffold and absence of rejected scaffold roots. | `REQ-018`, `DEV-018`, `TEST-018` | `user prompt`
- `DEV-019` | `2026-05-11` | Added `tests/unit/test_domain_contracts.py` and updated `tests/test-plan.md` plus `tests/design-traceability.md` for `TEST-019`. | Prove contract identifiers, states, relationships, validation rules, projection flags, and backwards-compatible constructors. | `REQ-019`, `DEV-019`, `TEST-019` | `user prompt`, `intent/product-intent.md`
- `DEV-020` | `2026-05-11` | Added `tests/unit/test_working_kms_runtime.py` and updated test planning/traceability for `TEST-020`. | Prove source intake, approval-gated publish, wiki readback, API route behavior, search, Infopedia projection, and fail-closed publishing in deterministic unit coverage. | `REQ-020`, `DEV-020`, `TEST-020` | `user prompt`, `intent/product-intent.md`
- `DEV-021` | `2026-05-12` | Added `tests/unit/test_knowledge_understanding.py` and updated runtime artifact expectations for candidate artifacts. | Prove extraction categories, relevance filtering, confidence scoring, non-publishable candidate drafts, review artifacts, and no direct `/wiki` mutation by candidate drafts. | `REQ-021`, `DEV-021`, `TEST-021` | `user prompt`, `intent/product-intent.md`
- `DEV-022` | `2026-05-12` | Extended `tests/unit/test_knowledge_understanding.py` for `.env` settings loading, mocked GPT-4o extraction, invalid-response fallback, and API failure fallback. | Prove the OpenAI integration path without live network calls or real secrets. | `REQ-022`, `DEV-022`, `TEST-022` | `user prompt`, `intent/product-intent.md`
- `DEV-023` | `2026-05-12` | Extended runtime and frontend unit tests for create-candidates, approve-all, publish-approved-to-wiki, Infopedia tree/search visibility, and KMI three-stage controls. | Prove the new workflow and UI contract deterministically without live LLM calls. | `REQ-023`, `DEV-023`, `TEST-023` | `user prompt`, `intent/product-intent.md`
- `DEV-024` | `2026-05-14` | Extended runtime, knowledge-understanding, and frontend scaffold tests for semantic decomposition, duplicate auto-rejection awareness, reject/approve-with-mods decisions, `sources/` publication, no `candidates/` wiki folder, frontend copy constraints, and search confidence scores. | Prove the requested workflow and UI/API contracts deterministically without live network calls. | `REQ-024`, `REQ-025`, `REQ-026`, `REQ-027`, `DEV-024`, `TEST-024` | `user prompt`, `intent/product-intent.md`
