# Plan Update

## Purpose
Interpret the latest human intent against the current design, code, tests, and operational evidence, then split the resulting work into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.

## Read first
- `intent/product-intent.md`
- the active feedback record in `intent/`
- `intent/gaps.md` when present
- `design/ux-flows.md`
- `design/acceptance-criteria.md`
- `design/` artifacts relevant to the current work
- `src/` implementation relevant to the current work
- `tests/` artifacts relevant to the current work
- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`

## Produce
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- Updated `dev_log/design-update-log.md` when the planning step changes the workflow or scope

## Planning rules
1. Treat the latest intent as the source of desired direction.
2. Compare that intent to the current UX flows, acceptance criteria, system design, architecture, code, and tests before deciding what belongs in each bucket.
3. Split the work by destination:
   - design changes that should be made next
   - code or configuration changes that should be made next
   - tests or validation updates that should be made next
4. Call out deviations explicitly when current design or code already conflicts with the latest intent.
5. Keep each plan file short, actionable, and traceable.
6. If a bucket has no change, record that explicitly instead of leaving it empty without explanation.
7. Do not edit `design/`, `src/`, or `tests/` directly from this step.

## Suggested structure for each plan file
- Current intent signal
- Required changes
- Existing drift or deviation
- Open questions or blockers
- Linked IDs or notes

## Done when
- The three plan files are written
- Deviations are visible
- Blocking questions are surfaced
- The next step can consume the plan without archaeology
