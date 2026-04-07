# 00 Design Update

## Purpose
Translate `plan/design-update.md` and the active `dev_log/` files into concrete design updates before baseline sync or implementation work.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `design/ux-flows.md`
- `design/acceptance-criteria.md`
- `design/system-design.md`
- `design/architecture.md`
- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`

## Update
- `design/system-design.md`
- `design/architecture.md`
- `design/acceptance-criteria.md`
- `design/ux-flows.md`
- `src/README.md` and `src/docs/` only if the project description or functionality needs to be reflected there
- `dev_log/design-update-log.md` when design updates are made

## Required translation method
1. Read the latest plan and operational evidence.
2. Extract the active product shape, constraints, open questions, and feedback-driven changes.
3. Map each meaningful plan theme to one or more concrete design artifacts and IDs.
4. Retain behavioral nuance in the design layer.
5. Add or revise `UXF-*`, `REQ-*`, `ACC-*`, `ARCH-*`, and `TEST-*` items as needed so the design can be tested and audited.
6. Record the resulting design choice, tradeoff, or gap in `dev_log/design-update-log.md`.

## Checklist
1. Read the current plan and current operational evidence.
2. Identify what the design should become before baseline sync begins.
3. Convert plan and log signals into concrete design edits, not vague notes.
4. Preserve the meaningful detail from the plan in the resulting design.
5. Update design traceability implications if the design changes.
6. Record the resulting design change in `dev_log/design-update-log.md`.

## Stop conditions
- Intent is too vague to translate into design
- Log evidence contradicts the intended direction and cannot be resolved safely
- Required design changes would exceed the current iteration without approval

## Done when
- The design update plan is explicit
- Required design files are updated or queued
- The related design changes are recorded in `dev_log/design-update-log.md`
- Baseline sync can start against the updated design
