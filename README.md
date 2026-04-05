# KMS

Knowledge Management System scaffold and design repository.

## Local Development

- `npm run dev:api` starts the Python API.
- `npm run dev:worker` starts the worker process.
- `npm run dev:kmi` starts the KMI frontend.
- `npm run dev:infopedia` starts the Infopedia frontend.
- `scripts/dev-api.sh` and `scripts/dev-worker.sh` provide shell wrappers with repo-local defaults.
- `scripts/health-check.sh` checks API readiness once the backend is running.

## Validation

- `pytest -q` runs the Python test suite from the repo root.
- `npm run test:frontend` runs the React component tests.
- `npm run validate` runs backend linting, tests, compile checks, and frontend builds.
