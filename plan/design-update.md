# Design Update Plan

This file is generated from `dev_workflow/plan-update.md`. Do not edit directly.

## Purpose
Capture the design changes that should be made next after comparing the latest intent with the current design, code, tests, and logs.

## Current intent signal
- Keep the four canonical design files aligned with the master draft structure and keep design-layer content free of traceability prefixes.

## Required changes
1. Rebuild `design/system-design.md` with the core behavioral logic from sections 1 and 2 of the master draft.
2. Rebuild `design/architecture.md` with the structural content from sections 3, 4, 5, 6, 9, and 10 of the master draft.
3. Rebuild `design/ux-flows.md` with the user and operator journey content from section 8 of the master draft.
4. Rebuild `design/acceptance-criteria.md` with the governance and correctness content from section 7 of the master draft.

## Existing drift or deviation
1. The current design files are now populated but need a final completeness review against the full master draft.
2. Design-layer prefixes were removed from the design docs and should remain reserved for plan, tests, and logs.

## Open questions or blockers
1. None.

## Linked IDs
1. `DEV-005`
