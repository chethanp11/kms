# 07 Design Audit

## Purpose
Confirm the finished work still matches design intent and that no undocumented behavior slipped in.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `design/ux-flows.md`
- `design/acceptance-criteria.md`
- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `design/` artifacts for the current iteration
- `src/` implementation summary
- `tests/design-traceability.md`

## Audit for
- intent/plan/design mismatch
- design improvement opportunities from plan or logs
- UX flow completeness
- acceptance criteria completeness
- undocumented behavior
- source documentation drift
- stale acceptance or test mappings
- prompt contract drift
- missing validation hooks

## Checklist
1. Compare final behavior to the current plan, active requirements, and acceptance criteria.
2. Confirm architecture constraints are still respected.
3. Confirm validation evidence supports the claimed outcome.
4. Record deviations and recommended follow-up actions.
5. Record design updates that should be made before the next iteration if the audit found weak structure.
6. Confirm `src/README.md` and `src/docs/` still match current plan and design.

## Done when
- Design alignment is explicitly stated
- Intent alignment is explicitly stated
- Deviations are captured
- The iteration is either approved for closeout or sent back to the fix loop
