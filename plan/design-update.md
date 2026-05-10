# Design Update Plan

This file is generated from the active AppFlow cycle. Do not edit directly outside the workflow.

## Purpose
Capture design updates or explicit no-change design decisions required by the current iteration.

## Current intent signal
- Create `src/` scaffolding for all KMS components listed in the design component matrix.

## Required changes
1. `REQ-016`: Update `design/architecture.md` to mark all-component `src/components/*` scaffolding as approved for this cycle and define it as metadata/contract scaffolding only.
2. `REQ-016`: Clarify that component scaffolds do not grant write authority and must preserve existing KMS authority boundaries.

## Existing drift or deviation
1. Earlier scaffold alignment deferred new component families; the current prompt explicitly asks for all component scaffolds and the design component matrix proves the component set.
2. `scripts/validate_scaffold.py` currently treats `src/components` as disallowed; it must be updated for this approved cycle.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-016`
2. `DEV-016`
3. `TEST-016`
