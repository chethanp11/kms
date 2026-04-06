# Acceptance Traceability Skill

## Purpose
Ensure every acceptance criterion has a usable traceability path from requirement to proof.

## When to use
- When defining or refining acceptance criteria.
- When writing tests or evaluations.
- During iteration planning.
- When a review finds unclear or decorative traceability.

## Read
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`
- `intent/feedback-intent.md` when feedback affects acceptance expectations
- `dev_log/feedback-log.md` when review feedback changes scope or readiness
- `design/acceptance-criteria.md`
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `design/build-scope.md`
- `src/README.md` and `src/docs/` when copied-project documentation changes affect acceptance

## Do
1. Extract the relevant intent sections, requirement IDs, and acceptance statements.
2. Map each acceptance item to proving tests, evals, or explicit manual review.
3. Identify missing `TEST-*`, `EVAL-*`, or blocking open questions.
4. Update `tests/design-traceability.md` with concrete mappings.
5. If acceptance changes imply documentation changes, note the corresponding `src/README.md` or `src/docs/` updates.

## Outputs
- A traceability matrix connecting `REQ-*` to `ACC-*`, `TEST-*`, and `EVAL-*`.
- A prioritized list of coverage gaps.
- Suggested updates to tests or acceptance criteria.

## Rules and cautions
- Do not create acceptance criteria without an associated traceability path.
- Do not lose the link between acceptance and the human intent that motivated it.
- Do not treat vague future coverage as a real mapping.
- Do not assume test coverage exists unless explicitly documented.
