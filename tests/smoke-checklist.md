# Smoke Checklist

## Purpose
Provide the minimum release-readiness checklist for the active iteration.

## Smoke checks
- [ ] Relevant intent sections and UX flows are still reflected in current design and scope.
- [ ] Active scope in the latest `plan/design-update.md` matches the work being shipped.
- [ ] In-scope `ACC-*` items are mapped in `tests/design-traceability.md`.
- [ ] Required unit, integration, e2e, regression, and smoke checks have run or have an explicit waiver.
- [ ] Validation evidence is recorded in `dev_log/validation-results.md`.
- [ ] No unresolved critical or blocking items remain in the active `dev_log/` files.
- [ ] Manual-review findings are captured in the active `dev_log/` files.
- [ ] The active `dev_log/` files reflect the current state.

## Notes
- Keep this list lightweight.
- If smoke checks repeatedly catch the same omission, improve the workflow or template instead of normalizing the miss.
