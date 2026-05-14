# Design Traceability

## Purpose
Map intent, requirements, design constraints, tests, feedback, and issues into one usable traceability view.

## Traceability matrix
| Intent sections | Flow area | Requirement ID | Design constraints | Test IDs | Feedback / issues | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Source intake and finalization | `REQ-001`, `REQ-003`, `REQ-005` | Raw-source immutability, governed maintenance, wiki publication boundary | `TEST-001`, `TEST-005` | `DEV-*` | Source intake, source notes, and governed finalization coverage; concrete unit coverage exists in `tests/unit/test_maintenance_run.py` and `tests/unit/test_kms_contracts.py` |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Contradiction handling and bounded automation | `REQ-002`, `REQ-007` | Policy gates, review states, and agent/service handoff controls | `TEST-002`, `TEST-006` | `DEV-*` | Contradiction handling, policy gating, and bounded automation coverage |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Browse-only navigation | `REQ-004` | Read-only Infopedia projection over finalized wiki content | `TEST-003` | `DEV-*` | Browse-only Infopedia and projection coverage |
| `intent/product-intent.md`, `intent/feedback-intent.md` | Auditability and failure handling | `REQ-006` | Traceability, explicit failure handling, and preserved operational evidence | `TEST-004` | `DEV-*` | Auditability, failure handling, and manual review coverage |
| `intent/product-intent.md` | Current scaffold alignment | `REQ-014` | Current `src/` scaffold is limited to existing base modules; no new top-level component families unless future plan/design proves necessity | `TEST-014` | `DEV-014` | Corrects stale plan/test drift and removes references to absent scaffold modules |
| `intent/product-intent.md` | Corrected src-only runtime scaffold | `REQ-018` | All KMS runtime/application scaffold files live under `src/`; rejected external runtime roots and `src/components` are absent | `TEST-018` | `DEV-018` | Future prompts should populate the detailed `src/` tree |
| `intent/product-intent.md` | Core domain contracts | `REQ-019` | Architecture section 9 entity contracts are explicit; metadata entities are operational and Infopedia/search entities remain derived projections over `/wiki` | `TEST-019` | `DEV-019` | Complete contracts live in `src/contracts` with backwards-compatible scaffold constructors |
| `intent/product-intent.md` | Working KMS runtime | `REQ-020` | Existing `src/`-only runtime scaffold is populated with bounded services, governance gates, API route functions, worker jobs, supporting stores, and read-only Infopedia/search projections while preserving `/wiki` authority | `TEST-020` | `DEV-020` | Concrete runtime coverage lives in `tests/unit/test_working_kms_runtime.py` |
| `intent/product-intent.md` | AI-assisted knowledge understanding | `REQ-021` | Knowledge candidates and candidate drafts are proposal-only Run artifacts with source trace, relevance/confidence scoring, review visibility, and no direct authority to publish `/wiki` truth | `TEST-021` | `DEV-021` | Concrete candidate extraction and non-publishable draft coverage lives in `tests/unit/test_knowledge_understanding.py` |
| `intent/product-intent.md` | API-backed AI extraction configuration | `REQ-022` | OpenAI GPT-4o extraction uses server-side `OPEN_AI_KEY` config, validates responses into candidate contracts, falls back deterministically on missing key or API failure, and never exposes secrets or grants publish authority | `TEST-022` | `DEV-022` | Mocked API coverage lives in `tests/unit/test_knowledge_understanding.py`; local secrets are ignored through `.gitignore` |
| `intent/product-intent.md` | KMI candidate approval and Infopedia publication | `REQ-023` | KMI separates candidate creation, review/approve-all, and load-to-wiki stages; only approved candidates publish to `/wiki`, and Infopedia remains read-only over finalized pages | `TEST-023` | `DEV-023` | Runtime route coverage lives in `tests/unit/test_working_kms_runtime.py`; frontend contract coverage lives in `tests/unit/test_src_runtime_scaffold.py` |

| `intent/product-intent.md` | Semantic candidate review and Infopedia search | `REQ-024`, `REQ-025`, `REQ-026`, `REQ-027` | Semantic decomposition, duplicate auto-rejection, visible review decisions, source-path publication, and confidence-scored read-only search | `TEST-024` | `DEV-024` | Runtime and frontend coverage lives in `tests/unit/test_working_kms_runtime.py`, `tests/unit/test_knowledge_understanding.py`, and `tests/unit/test_src_runtime_scaffold.py` |

## Guidelines
- Add a row for every new requirement.
- Keep `REQ-*`, `DEV-*`, and `TEST-*` references current.
- Use this document to find missing coverage before implementation is called complete.
- When a behavior is deliberately deferred, mark the gap instead of leaving the row incomplete.
