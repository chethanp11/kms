# 05 Validation

## Purpose
Run the checks that prove the scoped work and record the evidence.

## Read first
- `intent/*`
- `dev_log/*`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `.codex/commands.md`
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `design/eval-plan.md`
- `dev_log/change-log.md`

## Update
- `dev_log/validation-log.md`
- `dev_log/issue-log.md` for failures
- `dev_log/version-status.md` if readiness changes materially

## Checklist
1. Run required unit, integration, e2e, regression, smoke, and eval commands for the active scope.
2. Validate that observed behavior still matches the interpreted intent, not only the current implementation.
3. Record what ran, what did not run, and why.
4. Classify every failure before changing code.
5. Treat eval failures, hallucination findings, and review gaps as real release input.
6. Note any environment issues separately from product defects.
7. Record design improvements implied by validation failures or review gaps.
8. Record any documentation drift in `src/README.md` or `src/docs/` as a design or implementation gap.

## Done when
- Validation evidence is recorded
- Failures are classified and linked to artifacts
- The fix loop has a concrete target list
