# Current Intent

Create foundational implementation components in `src/` based on the KMS design. These components should act as stable base primitives for future services, API handlers, stores, projections, governance, and orchestration components.

## Scope

- Add reusable component metadata and registry primitives.
- Add explicit port/protocol contracts for stores, validation, publishing, search, and projection boundaries.
- Add deterministic in-memory base stores for tests and future components.
- Preserve KMS authority boundaries: `/wiki` is canonical, metadata/indexes/projections are supporting, Infopedia is read-only, and publication is governed.
- Validate with targeted standard-library unit tests.
