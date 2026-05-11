# Code Update Plan

## Current scope
- `DEV-020`: Replace placeholder modules under `src/` with a working KMS runtime slice.

## Implementation steps
1. Add settings/path helpers and deterministic runtime context.
2. Implement in-memory metadata and filesystem stores for raw sources, artifacts, search indexes, and wiki pages.
3. Implement bounded services for source discovery/parsing, source notes, analysis, drafting, policy validation, contradiction handling, approval, publishing, linting, projections, and orchestration.
4. Implement API route functions, optional FastAPI app wiring, worker jobs, agent facades, and script entrypoints.
5. Keep implementation dependency-free except optional FastAPI import detection.

## Risks
- Avoid letting metadata/search/projection stores become authoritative over `/wiki`.
- Fail closed on missing source traces, missing approval, or blocked QA.
