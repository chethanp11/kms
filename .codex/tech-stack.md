# KMS Tech Stack

This file is the project-specific technical reference for KMS. It must stay aligned with `design/architecture.md`, especially sections 9 and 10.

For AppFlow reuse in a new application, this file and `.codex/project-context.md` are the only files expected to require project-specific edits.

## Target Stack Summary

| Layer | Technology | Purpose | Notes |
| --- | --- | --- | --- |
| Backend language | Python | APIs, orchestration, parsing, validation, publishing, and jobs | Backend should be built before advanced UI depth. |
| Backend API | FastAPI or Flask-style Python HTTP service | JSON API for KMI and Infopedia | Keep API contracts stable and governed; UI must not access storage directly. |
| Worker runtime | Python worker/job runner | Run orchestration, source processing, validation, publishing, indexing | Separate background work from request/response handling. |
| Frontend | HTML + CSS + JavaScript | KMI and Infopedia web applications | KMI is governed maintenance; Infopedia is read-only consumption. |
| Frontend tooling | static web tooling | Local development and frontend build entrypoints | Applies to both KMI and Infopedia apps. |
| API contracts | JSON over REST or GraphQL | UI-to-backend and service-facing exchange | REST endpoints are the current representative design; GraphQL remains optional. |
| Backend tests | pytest or equivalent Python test runner | Unit, integration, golden, fixture, and regression validation | Current scaffold may still use `unittest` until pytest is installed. |
| Frontend tests | JavaScript browser/component test stack | Component and browser-flow validation | Choose concrete tools when frontend scaffold is added. |


## Storage and Persistence

| Store | Technology / type | Authority | Purpose |
| --- | --- | --- | --- |
| `/wiki` | Filesystem markdown store | Canonical truth | Finalized governed knowledge. |
| `/raw` | Filesystem or mounted source folders | Upstream evidence only | Immutable source inputs for maintenance runs. |
| Metadata database | SQL database | Operational support | Runs, approvals, contradictions, revisions, QA state, projections, audit events. |
| Artifact storage | File/object-style storage | Supporting evidence | Parse outputs, diffs, extracted text, review bundles. |
| Search/index store | Derived index | Rebuildable projection | Search and navigation acceleration for KMI and Infopedia. |

The metadata DB and indexes must not replace `/wiki` as the knowledge source of truth.

## Data and File Formats

| Format | Use |
| --- | --- |
| Markdown | Canonical wiki pages, templates, design docs, plans, logs, validation docs. |
| YAML | Wiki frontmatter, governance rules, machine-readable policy, config templates. |
| JSON | API payloads, service contracts, run artifacts, UI data exchange. |
| TOML | Python project and tooling configuration. |
| Environment/config manifests | Runtime configuration and secret references; never commit secret values. |

## AI Provider Configuration

OpenAI-backed AI activities are configured through server-side environment variables:

| Variable | Purpose | Default / behavior |
| --- | --- | --- |
| `OPENAI_API_KEY` | Secret key for OpenAI API calls. | Empty by default; load from local `.env` or process env only. |
| `KMS_AI_MODEL` | Model used for knowledge-understanding extraction. | `gpt-4o` |
| `KMS_AI_ENABLED` | Enables API-backed AI extraction when an API key exists. | Enabled when a key is present unless explicitly false. |
| `KMS_AI_TIMEOUT_SECONDS` | API request timeout for AI extraction. | `30` |

Local `.env` files are ignored and must not contain committed secrets. `.env.example` is the committed placeholder.

## Service and API Contracts

Representative API categories:

- run APIs
- source APIs
- knowledge candidate/review artifact APIs
- review/diff APIs
- approval APIs
- contradiction APIs
- health/lint APIs
- wiki read APIs
- Infopedia navigation/search APIs

Representative REST-style endpoints from design:

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/runs` | Create a governed maintenance run. |
| `GET` | `/api/runs/{run_id}` | Fetch run status and summary. |
| `GET` | `/api/runs/{run_id}/artifacts` | List run artifacts and outputs. |
| `GET` | `/api/reviews/{revision_id}/diff` | Fetch review diff and validation context. |
| `POST` | `/api/approvals/{revision_id}` | Submit approval or rejection. |
| `GET` | `/api/wiki/pages/{slug}` | Read finalized wiki page content. |
| `GET` | `/api/infopedia/tree` | Fetch navigation projection. |
| `GET` | `/api/infopedia/search` | Search finalized knowledge. |
| `GET` | `/api/contradictions/{id}` | Read contradiction detail. |
| `GET` | `/api/health/findings` | Read lint and maintenance issues. |

## Validation Commands

Current scaffold validation:

```bash
python -m unittest discover -s tests/unit -p 'test_*.py'
python .codex/tools/validate_codex_contract.py
git diff --check
```

Target validation as the stack is installed:

- Python format/lint/type checks through the chosen Python toolchain.
- Backend unit and integration tests through `pytest` or equivalent.
- Golden tests for deterministic markdown generation and diffs.
- Fixture-based tests for source folders, wiki outputs, lint failures, and contradictions.
- JavaScript component and browser-flow tests for KMI and Infopedia.
- End-to-end tests for run initiation, diff review, approval, publish, and read-only page browse.

## Engineering Constraints

- Backend domain logic belongs in Python services/packages, not only in frontend code.
- Status enums and API schemas should be shared consistently across backend and frontend contracts.
- All `/wiki` writes must go through governed backend services.
- Rules should fail closed when required fields or traceability are missing.
- Search/index and Infopedia projection layers must be rebuildable from `/wiki` plus metadata.
- Local development should run API, worker, metadata DB, `/raw`, and `/wiki` together so authority boundaries match production intent.
