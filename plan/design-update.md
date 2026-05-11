# Design Update Plan

## Current scope
- `REQ-020`: Populate the existing `src/`-only KMS runtime scaffold with concrete, stdlib-first behavior aligned to the current design.

## Design interpretation
- No design document changes are required: the existing architecture already defines the runtime service model, governance gates, `/wiki` authority boundary, KMI control surface, Infopedia read-only projection, metadata support role, and source intake flow.
- The current iteration translates those existing design contracts into implementation only.

## Boundaries
- Keep runtime code under `src/`.
- Do not add new top-level runtime roots or new framework/control-plane behavior.
- Preserve `/wiki` as the only finalized truth store; metadata, search, and Infopedia stay derived/supporting.
