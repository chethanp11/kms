# KMS

KMS is a governed Knowledge Management System. The current application in `src/` turns local source files into reviewable knowledge candidates, lets a Knowledge Manager approve or reject them in KMI, publishes approved candidates as markdown pages under the configured wiki root, and exposes finalized wiki pages through read-only Infopedia search and browse APIs.

## Current Runtime Surfaces

- `src/api/main.py` — API entrypoint. Uses FastAPI when installed and falls back to a dependency-free ASGI app for smoke testing.
- `src/kmi/` — browser UI for the three-stage candidate workflow: create candidates, review/approve or reject, then publish approved candidates.
- `src/infopedia/` — read-only browser UI for wiki tree, search, and page rendering.
- `src/services/run_orchestration.py` — coordinates source discovery, parsing, candidate extraction, duplicate awareness, approval state, governed publishing, audit events, contradiction artifacts, lint, search indexing, and Infopedia projection refresh.
- `src/storage/` — local in-memory metadata/search stores plus filesystem artifact and wiki stores.
- `src/contracts/` — dataclass and enum contracts shared across services, routes, tests, and UI responses.

## Application Flow

1. KMI submits either a local `source_path` or browser-selected `source_files`.
2. The runtime discovers and parses sources, writes source and candidate artifacts, and creates proposal-only knowledge candidates.
3. KMI lists candidates, including confidence/relevance, source reference, duplicate rationale, review state, and optional reviewer modifications.
4. The Knowledge Manager approves, rejects, or approve-all reviews candidates.
5. Only approved candidates can be published. Publication creates validated wiki pages under `sources/*.md`, archives candidates, rebuilds search, and refreshes the Infopedia projection.
6. Infopedia reads finalized wiki pages only. Candidate search is available only through the API's explicit `include_candidates` option and does not make candidates canonical.

## API Endpoints Exposed by `create_app()`

- `GET /` and `GET /api/health`
- `POST /api/runs`
- `GET /api/runs/{run_id}`
- `GET /api/runs/{run_id}/artifacts`
- `POST /api/candidates`
- `GET /api/candidates/{run_id}`
- `POST /api/candidates/{run_id}/approve`
- `POST /api/candidates/{run_id}/publish`
- `GET /api/infopedia/tree`
- `GET /api/infopedia/search?q=...&include_candidates=false`
- `GET /api/wiki/pages/{slug}`
- `GET /api/reviews/{revision_id}/diff`
- `POST /api/approvals/{revision_id}`
- `GET /api/contradictions/{id}`
- `GET /api/health/findings`

## Configuration

`KMSSettings.from_env()` reads process environment first, then `.env` and `config/.env` defaults when present.

| Variable | Purpose | Default |
|---|---|---|
| `KMS_DATA_ROOT` | Base folder for local runtime data | `data-storage` |
| `KMS_RAW_ROOT` | Raw source root | `$KMS_DATA_ROOT/raw` |
| `KMS_WIKI_ROOT` | Finalized wiki root | `$KMS_DATA_ROOT/wiki` |
| `KMS_ARTIFACT_ROOT` | Run artifact root | `$KMS_DATA_ROOT/artifacts` |
| `KMS_METADATA_PATH` | Reserved metadata path | unset |
| `KMS_AI_ENABLED` | Enables OpenAI-backed candidate extraction | true when `OPEN_AI_KEY` is set, otherwise false |
| `KMS_AI_MODEL` | OpenAI model name for extraction | `gpt-4o` |
| `KMS_AI_TIMEOUT_SECONDS` | OpenAI request timeout | `30` |
| `OPEN_AI_KEY` | Server-side OpenAI API key | unset |
| `KMS_ALLOW_AUTO_APPROVE` | Allows dev/test full-run auto-approval | `false` |

When AI extraction is disabled, missing a key, fails, or returns invalid candidate data, the runtime falls back to deterministic extraction. `auto_approve` requests do not publish unless `KMS_ALLOW_AUTO_APPROVE=true` or the runtime setting is explicitly enabled for tests.

## Local Development

Start the API and static UIs:

```bash
bash src/scripts/start-dev.sh
```

The script starts:

- API on `http://127.0.0.1:8000` or the next available port
- KMI on `http://127.0.0.1:3000` or the next available port
- Infopedia on `http://127.0.0.1:3001` or the next available port

It also rewrites `src/kmi/config.js` and `src/infopedia/config.js` to point at the selected API port.

## Validation

Run targeted runtime validation:

```bash
python -m src.scripts.validate_project
python -m unittest discover -s tests/unit
```

## Repository Structure

- `AGENTS.md` — engineering instructions
- `.codex/project-context.md` — KMS-specific grounding
- `design/` — architecture, governance, UX, and acceptance docs
- `src/` — application implementation
- `tests/` — deterministic validation and source fixtures
