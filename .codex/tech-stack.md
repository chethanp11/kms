## KMS Source Stack

This file records the intended implementation stack for `src/`.

### Backend
- Python backend service
- HTTP API service for KMI and Infopedia
- Worker/job runner for orchestration and scheduled tasks
- Domain logic and shared utilities in reusable Python packages

### Frontend
- React KMI application for governed maintenance workflows
- React Infopedia application for read-only knowledge browsing
- Vite-based frontend entrypoints

### Testing
- `pytest` for backend unit and integration tests
- React test stack for frontend component and browser-flow coverage

### Supporting tools
- Markdown-first product documentation in `src/docs/`
- Local development contracts and workflow guidance in `.codex/`

### Notes
- The repository is still at scaffold stage, so this stack is the target implementation direction rather than a fully installed runtime.
- Keep `src/` aligned to the architecture in `design/architecture.md` and the product boundaries in `design/system-design.md`.
