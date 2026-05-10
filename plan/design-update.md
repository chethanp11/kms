# Design Update Plan

## Purpose
Capture design updates or explicit no-change decisions for this cycle.

## Current intent signal
- Correct scaffold interpretation: KMS runtime/application code scaffolds must live inside `src/` only, including scripts scaffolding. Remove target-layout folders outside `src/` and delete `src/components` metadata scaffolds.

## Required changes
1. `REQ-018`: Update `design/architecture.md` to define a detailed `src/`-only runtime scaffold layout for API, worker, domain, shared utilities, storage, services, KMI, Infopedia, config, agents, rules, templates, observability, orchestration, and scripts.
2. `REQ-018`: Mark top-level `apps/`, `packages/`, `config/`, `agents/`, `rules/`, `templates/`, `wiki/`, `raw/`, `docs/`, and `scripts/` scaffold files as incorrect for current implementation preparation.
3. `REQ-018`: Keep `src/components/` excluded; future implementation should populate concrete files under the detailed `src/` layout.

## Existing drift or deviation
1. Previous scaffold created files outside `src/`, contrary to current clarification.
2. Previous scaffold used `src/components` metadata packages, which the user explicitly rejected.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-018`
2. `DEV-018`
3. `TEST-018`
