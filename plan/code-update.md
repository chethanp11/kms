# Code Update Plan

## Purpose
Capture implementation changes required by this cycle.

## Current intent signal
- Create empty/minimal KMS application code scaffolding inside `src/` only.

## Required changes
1. `DEV-018`: Delete `src/components/`.
2. `DEV-018`: Delete previously created scaffold folders outside `src/`: `apps/`, `packages/`, `config/`, `agents/`, `rules/`, `templates/`, `wiki/`, `raw/`, `docs/`, and top-level `scripts/`.
3. `DEV-018`: Create detailed blank/minimal scaffold files under `src/` for runtime API, worker, domain, services, storage, frontends, config, agents, rules, templates, observability, orchestration, and scripts.
4. `DEV-018`: Update `src/__init__.py` so it exposes only present scaffold modules.

## Existing drift or deviation
1. Outside-`src` scaffold folders exist and must be removed.
2. `src/components` exists and must be removed.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-018`
2. `DEV-018`
3. `TEST-018`
