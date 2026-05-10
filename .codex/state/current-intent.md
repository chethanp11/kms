# Current Intent

Create an initial implementation scaffold under `src/` for KMS based on the current design artifacts.

Scope:
- restore `src/` as a Python package with bounded contracts, execution, governance, orchestration, API, app, observability, and context modules
- keep scaffold deterministic and testable with standard-library code
- preserve KMS authority boundaries: raw sources are inputs, `/wiki` is canonical, Infopedia is read-only, and publication is governed
- add targeted unit coverage for scaffold contracts and service inventory
