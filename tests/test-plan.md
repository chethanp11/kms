# Test Plan

## Purpose
Define how the current scope will be validated and which test layers are responsible for proving it.

## Planning rules
- Plan tests from intent-derived design, not from implementation convenience.
- Add a `TEST-*` row for each meaningful validation item.
- Link each `TEST-*` to the relevant `REQ-*`, design area, and architecture/design constraints.
- Use only `REQ-*`, `DEV-*`, and `TEST-*` as active traceability ID prefixes.
- If the behavior cannot be proven well with ordinary tests, state the manual or hybrid review method in the plan.

## Validation inventory
| ID | Layer | Purpose | Linked IDs | Artifact or location | Owner |
| --- | --- | --- | --- | --- | --- |
| `TEST-001` | `unit` | Validate maintenance run normalization, source bundle discovery, proposal metadata creation, and source-note generation. | `REQ-001`, `REQ-003`, `REQ-005` | `tests/unit/test_maintenance_run.py` | Knowledge Manager or platform engineer |
| `TEST-002` | `integration` | Verify contradiction routing, review-state transitions, publication gating, and blocked-finalization behavior. | `REQ-002`, `REQ-007` | `tests/integration/` | Knowledge Manager or platform engineer |
| `TEST-003` | `e2e` | Confirm the supported browse flow from finalized wiki content into Infopedia and ensure it is read-only. | `REQ-004` | `tests/e2e/` | Knowledge Manager or platform engineer |
| `TEST-004` | `regression` | Guard against audit, traceability, and failure-handling regressions after approval, rejection, escalation, or dependency failure. | `REQ-006` | `tests/regression/` | Knowledge Manager or platform engineer |
| `TEST-005` | `unit` | Validate knowledge-model schema, page typing, folder placement, and required frontmatter/body sections. | `REQ-005` | `tests/unit/test_kms_contracts.py` | Knowledge Manager or platform engineer |
| `TEST-006` | `static` | Verify the AppFlow 11-step lifecycle, retired ID-prefix absence, retired path removal, and reusable `.codex` consistency. | `REQ-001`, `DEV-013` | `.codex/tools/validate_codex_contract.py` | Platform engineer |
| `TEST-014` | `unit/static` | Validate current scaffold alignment: no stale tests or exports reference absent component-family modules; existing contracts, execution, governance, app, context, agent, observability, and orchestrator tests pass. | `REQ-014`, `DEV-014` | `tests/unit/test_kms_contracts.py`, `tests/unit/test_maintenance_run.py`, `tests/unit/test_scaffold_boundaries.py`, unit discovery | Platform engineer |
| `TEST-018` | `unit/static` | Validate corrected `src/`-only runtime scaffold files and absence of rejected scaffold roots such as `apps/`, `packages/`, top-level `scripts/`, and `src/components/`. | `REQ-018`, `DEV-018` | `tests/unit/test_src_runtime_scaffold.py`, unit discovery, Python compile | Platform engineer |
| `TEST-019` | `unit/static` | Validate complete core KMS domain contracts, state enums, identity relationships, projection flags, and backwards-compatible scaffold imports. | `REQ-019`, `DEV-019` | `tests/unit/test_domain_contracts.py`, `tests/unit/test_kms_contracts.py`, unit discovery, Python compile | Platform engineer |
| `TEST-020` | `unit/static` | Validate the working stdlib KMS runtime slice from raw source discovery through parsing, draft creation, QA, approval-gated publish, `/wiki` readback, search, Infopedia projection, API route functions, and fail-closed publishing. | `REQ-020`, `DEV-020` | `tests/unit/test_working_kms_runtime.py`, unit discovery, Python compile | Platform engineer |
| `TEST-021` | `unit/static` | Validate governed AI-assisted knowledge understanding candidates, relevance filtering, confidence scoring, non-publishable candidate drafts, review artifacts, and no direct `/wiki` mutation by candidate drafts. | `REQ-021`, `DEV-021` | `tests/unit/test_knowledge_understanding.py`, `tests/unit/test_working_kms_runtime.py`, unit discovery, Python compile | Platform engineer |

## Coverage checks
- Does each requirement have at least one proving artifact?
- Are failure paths tested as well as happy paths?
- Is at least one regression artifact added for each resolved major defect?
- Are manual-review behaviors clearly marked so they are not mistaken for unit-test coverage?
