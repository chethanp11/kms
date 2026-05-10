# Design Update Plan

This file is generated from the active AppFlow cycle. Do not edit directly outside the workflow.

## Purpose
Capture design updates or explicit no-change design decisions required by the current iteration.

## Current intent signal
- Review current KMS scaffold against design requirements and update design/scaffold, including scripts scaffolding, without adding unnecessary `src/` component families.

## Required changes
1. `REQ-015`: Update `design/architecture.md` scaffold alignment to include the required top-level `scripts/` scaffold and clarify which early runtime modules are intentionally present in `src/`.
2. `REQ-015`: Clarify that scripts are operational/developer helpers and must not become alternate application runtime or bypass governed KMS services.

## Existing drift or deviation
1. `design/architecture.md` requires `/scripts` for build, validation, and maintenance scripts, but the repository currently has no top-level `scripts/` scaffold.
2. The current `src/` scaffold is intentionally smaller than the long-term target layout in `apps/` and `packages/`; design needs to name this as a staged scaffold rather than a contradiction.
3. Prior deleted `src/components`, `src/ports`, and `src/storage` files remain out of scope for restoration because the current design does not prove they are necessary for this review.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-015`
2. `DEV-015`
3. `TEST-015`
