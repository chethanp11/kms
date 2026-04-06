# Iteration Intent

## Purpose
This is the human-edited source for what should happen next. Use it to steer the next version or iteration without manually editing the downstream system-managed artifacts.

## Human-editable rule
- This file is intended for direct human editing.
- Codex should interpret it into design scope, tests, workflow actions, and logging updates.
- Codex must not modify it unless explicitly asked.

## Current direction
- Current target version: `v0.1`
- Next iteration goal: implement the first usable KMS delivery slice: local source intake, governed proposal generation, Knowledge Manager review gating, finalized wiki publication, Infopedia read-only navigation, and traceable audit output.
- Why now: the product intent defines a governed knowledge control plane, and the repository needs a concrete first implementation slice to prove the maintenance-to-publication loop end to end.

## Priority areas
| Intent Section | Priority | Area | Desired change | Notes |
| --- | --- | --- | --- | --- |
| `INT-ITER-001` | `high` | `implementation` | Build the first governed maintenance loop from source path intake through proposal output and review decision. | This should establish the minimum KMI behavior and the source-to-wiki boundary. |
| `INT-ITER-002` | `high` | `consumption` | Add the first read-only Infopedia browse/search/page flow over finalized wiki content. | This should prove consumption is separated from maintenance. |
| `INT-ITER-003` | `medium` | `observability` | Record source trace, review state, and publication outcome for each run. | This should support auditability and later validation. |

## Version direction
- `v0.1`: prove the core governed maintenance loop works end to end for one bounded source bundle.
- `v0.2`: improve contradiction handling, review tooling, and browse quality without losing governance.
- `v0.3`: mature into a repeatable, releaseable knowledge maintenance system with stable contracts and strong auditability.

## Overrides to current plan
- Exact implementation-surface choice for KMI is still unresolved and must be settled before coding.
- Source bundle conventions and file-type support must be defined before the first implementation slice is built.
- If review gating or publication cannot be validated cleanly, reduce scope rather than weakening governance.

## Notes for Codex
- Interpret this file into actionable changes in `design/build-scope.md`, acceptance criteria, tests, and workflow state before coding.
- If this file conflicts with the current system-managed plan, treat this file as authoritative human direction and update downstream artifacts accordingly.
