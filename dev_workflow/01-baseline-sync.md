# 01 Baseline Sync

## Purpose
Align the collaborator with the real current state before any new scoped work begins.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `design/` artifacts
- `tests/design-traceability.md`
- `dev_log/iteration-log.md`
- `dev_log/change-log.md`
- `dev_log/validation-log.md`
- `dev_log/issue-log.md`
- `dev_log/backlog.md`

## Produce
- A baseline summary of the current version, active scope, open risks, and unresolved questions
- A summary of the current design state after the design-update step
- A summary of how `src/README.md` and `src/docs/` reflect the current design
- A list of missing or stale design, test, eval, or log artifacts
- A clear statement of whether the project is ready to enter scoping

## Checklist
1. Confirm which `REQ-*`, `ACC-*`, `ARCH-*`, and `TEST-*` items are already active.
2. Review unresolved `DEV-*` issues, deviations, validation failures, and open questions.
3. Identify missing links in `tests/design-traceability.md`.
4. Verify that `src/README.md` and `src/docs/` match the current design and the code/test plan buckets.
5. State what cannot safely proceed until clarified.

## Stop conditions
- Intent is missing, stale, or materially conflicts with current design
- Missing core design artifact for current scope
- Blocking open question with user-visible impact
- Validation evidence contradicts the claimed project status

## Done when
- Baseline summary is documented
- Open blockers are explicit
- The next iteration can be scoped without hidden assumptions
