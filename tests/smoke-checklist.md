# Smoke Checklist

## Purpose
Provide the minimum release-readiness checklist for the active iteration.

## Smoke checks
- [ ] Relevant intent sections are still reflected in current design and scope.
- [ ] Active scope in `design/build-scope.md` matches the work being shipped.
- [ ] In-scope `ACC-*` items are mapped in `tests/design-traceability.md`.
- [ ] Required unit, integration, e2e, regression, and eval checks have run or have an explicit waiver.
- [ ] Validation evidence is recorded in `dev_log/validation-log.md`.
- [ ] No unresolved critical or blocking `DEV-*` items remain in `dev_log/issue-log.md` or `design/open-questions.md`.
- [ ] Manual-review findings are captured in `dev_log/feedback-log.md`.
- [ ] `dev_log/release-notes.md` and `dev_log/version-status.md` reflect the current state.

## Notes
- Keep this list lightweight.
- If smoke checks repeatedly catch the same omission, improve the workflow or template instead of normalizing the miss.
