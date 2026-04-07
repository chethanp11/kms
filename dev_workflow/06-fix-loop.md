# 06 Fix Loop

## Purpose
Address defects and gaps identified during validation until the scoped work is either acceptable or explicitly deferred.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/*`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `dev_log/issue-log.md`
- `dev_log/deviations-log.md`
- `dev_log/validation-log.md`
- `tests/design-traceability.md`

## Checklist
1. Fix root causes in the correct layer: design, implementation, test, review process, or environment.
2. If the root cause is bad interpretation of intent or plan, correct the plan and design logs before code.
3. Update tests or manual-review coverage only when the classification justifies it.
4. Re-run the minimum required validation to confirm the fix.
5. Update `dev_log/validation-log.md`, `dev_log/issue-log.md`, and `dev_log/deviations-log.md`.
6. Move non-blocking deferred work to `dev_log/backlog.md`.
7. Capture any design improvement that the fix exposed.
8. Update `src/README.md` and `src/docs/` if the fix changes the application’s stated purpose or functionality.

## Done when
- Current-scope failures are resolved or explicitly deferred
- Revalidation evidence exists
- The design audit has a stable target
