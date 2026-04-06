# Build Scope

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Define the active version and iteration boundary. This file is the scope contract that prevents drift.

## Intent sources
- `intent/iteration-intent.md`
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/feedback-intent.md` when feedback reprioritizes scope

## Current target
- Project: `KMS`
- Version: `v0.3`
- Iteration: `design baseline translation`
- Goal: translate the KMS intent into a governed design baseline for source maintenance, wiki publication, and read-only consumption.
- Owner or primary collaborator: `Knowledge Manager` and `Codex`

## In scope
- `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`
- `ACC-001`, `ACC-002`, `ACC-003`, `ACC-004`
- `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`
- `AI-001`, `AI-002`, `AI-003`, `AI-004`, `AI-005`, `AI-006`
- `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`
- `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `EVAL-005`
- `design/versions/*` brief alignment for v0.1 through v0.3
- `src/README.md` and `src/docs/*` to reflect the KMS application description
- `tests/design-traceability.md` and `tests/test-plan.md`
- `dev_log/change-log.md`, `dev_log/decision-log.md`, `dev_log/deviations-log.md`, `dev_log/validation-log.md`

## Out of scope
- Implementation in `src/`
- Real source-connectors, remote sync, or production deployment wiring
- Autonomous publication without Knowledge Manager review
- Broad search-engine or chat-product behavior
- Performance optimization beyond bounded maintenance and browse paths

## Entry conditions
- Relevant design artifacts are present or explicitly marked incomplete.
- In-scope IDs exist or are being created in the same planning step.
- Tests and eval intent are known enough to define validation.

## Exit conditions
- Every in-scope requirement is linked to `ACC-*`.
- Validation work is defined for every acceptance item.
- Out-of-scope items are either deferred to backlog or called out in the next version brief.

## Dependencies and risks
- Required dependencies: a local source tree, markdown/wiki content, a Knowledge Manager reviewer, and an LLM-backed proposal workflow.
- Blocking open questions: whether KMI is CLI-first, API-first, or UI-first in the first implementation.
- Risk notes: stale wiki snapshots, source ambiguity, accidental write paths, and incomplete provenance capture.

## Change control
- Any scope change after implementation starts must be recorded in `dev_log/change-log.md`.
- If a new behavior appears during coding and is not already in scope, stop and decide whether it belongs in design or backlog.
