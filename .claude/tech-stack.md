## KMS Source Stack

This file records the intended implementation stack for `src/`.

## Stack Summary

| Layer | Technology | Purpose | Notes |
| --- | --- | --- | --- |
| Frontend | React + TypeScript | Build KMI and Infopedia web applications | Frontend implementation should live under `src/` and follow approved `plan/*` and `design/*` |
| Frontend tooling | Vite | Frontend build tooling and local development entrypoint | Keep setup lightweight and aligned to the React + TypeScript stack |
| Backend | Python | Implement APIs, orchestration, domain logic, and background jobs | Backend implementation should follow approved `plan/*` and `design/*` |
| Backend API | Python HTTP service | Serve KMI and Infopedia backend capabilities | Current design allows a Python web framework such as FastAPI or Flask |
| Background work | Python workers/jobs | Handle orchestration and scheduled processing | Keep worker responsibilities separate from request/response handling |
| Backend testing | `pytest` | Unit and integration testing for Python backend behavior | Align tests to acceptance criteria and planned validation |
| Frontend testing | TypeScript-based React test stack | Component and browser-flow validation for frontend behavior | Choose the concrete test tools when implementation is scaffolded |
| Local guidance | `.claude/*` | Repo-local workflow and stack guidance for Claude | Support files are not part of the product runtime |

## File And Data Format Map

| Format | Where it is used | Purpose | Examples |
| --- | --- | --- | --- |
| Markdown (`.md`) | Canonical knowledge, repo workflow artifacts, templates, and human-readable design/validation docs | Primary human-readable and AI-usable knowledge format | `/wiki/*.md`, `design/*.md`, `plan/*.md`, `tests/*.md`, `dev_log/*.md`, `templates/*.md` |
| YAML (`.yaml`, `.yml`) | Governance rules, machine-readable policy files, frontmatter, and environment/config templates | Machine-readable rules and structured metadata | `/rules/*.yaml`, wiki page frontmatter, config templates |
| JSON (`.json`) | API payloads, UI-service contracts, structured artifacts, and runtime exchange formats | Structured application data exchange | REST/GraphQL responses, run artifacts, UI payloads |
| TOML (`.toml`) | Python project and tool configuration | Python dependency and tooling configuration | `pyproject.toml`, local tool config |
| Environment files / config manifests | Centralized runtime configuration | Environment-driven configuration and secret references | `/config/*`, env templates, runtime manifests |

## Storage And Persistence

| Storage layer | Technology / type | Purpose | Notes |
| --- | --- | --- | --- |
| Canonical knowledge store | Filesystem-based Markdown store | Persist finalized knowledge under `/wiki` | This is the authoritative knowledge substrate |
| Raw source store | Filesystem / mounted source folders | Hold immutable upstream source artifacts | Inputs remain outside canonical truth |
| Metadata database | SQL metadata DB | Store runs, approvals, contradictions, revisions, QA state, and lifecycle metadata | Operational authority only; not the knowledge source of truth |
| Optional artifact storage | File or object-style artifact storage | Retain parse outputs, diffs, extracted text, and review bundles | Supporting operational storage |
| Optional search/index layer | Derived index store | Support browse/search over finalized content and metadata | Derived support layer, not canonical truth |

## Service And Interface Contracts

| Area | Technology / style | Purpose | Notes |
| --- | --- | --- | --- |
| UI to backend contracts | JSON over REST or GraphQL | Governed application-facing service boundary | UI must not access the database directly |
| Backend domain logic | Python packages/modules | Shared domain behavior, validators, rules, and orchestration logic | Keep domain logic reusable across API and worker layers |
| Templates | Markdown templates with structured metadata | Generate governed wiki pages and related artifacts | Template ownership belongs in `/templates` |
| Rules engine inputs | YAML rule files | Enforce publish, traceability, freshness, and governance rules | Missing required fields should fail closed |

## Notes

- React + TypeScript is the intended frontend stack.
- Python is the intended backend stack.
- Markdown is the canonical knowledge format.
- YAML is used for rules and structured metadata where machine-readable policy is needed.
- JSON is used for application contracts and structured runtime data exchange.
- The metadata DB is operational support and must not replace `/wiki` as canonical truth.
- The repository is still at scaffold stage, so this stack is the target implementation direction rather than a fully installed runtime.
- Keep `src/` aligned to `design/architecture.md`, `design/system-design.md`, and the approved `plan/*` files.
