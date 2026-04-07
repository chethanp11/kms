# 05 Validation

## Purpose
Run the checks that prove the scoped work and record the evidence.

## Read first
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
- `.codex/commands.md`
- `tests/test-plan.md`
- `tests/design-traceability.md`

## Update
- `dev_log/validation-results.md`
- `dev_log/design-update-log.md`, `dev_log/code-update-log.md`, or `dev_log/test-update-log.md` if validation changes the scoped work

## Checklist
1. Run required unit, integration, e2e, regression, and smoke commands for the active scope.
2. Validate that observed behavior still matches the interpreted plan, UX flows, and acceptance criteria, not only the current implementation.
3. Record what ran, what did not run, and why.
4. Classify every failure before changing code.
5. Treat review gaps as real release input.
6. Note any environment issues separately from product defects.
7. Record design improvements implied by validation failures or review gaps.
8. Record any documentation drift in `src/README.md` or `src/docs/` as a design or implementation gap.

## Done when
- Validation evidence is recorded
- Failures are classified and linked to artifacts
- The fix loop has a concrete target list
