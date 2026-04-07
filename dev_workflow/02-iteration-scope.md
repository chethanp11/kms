# 02 Iteration Scope

## Purpose
Define the exact work for the next iteration by interpreting the latest plan and active logs into updated design scope and proof requirements.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `design/ux-flows.md`
- `design/acceptance-criteria.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `design/acceptance-criteria.md`
- relevant files from `design/`
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`

## Update
- `design/acceptance-criteria.md` if acceptance is changing
- relevant files in `design/` that need to reflect current plan
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `src/README.md` if the project README needs to reflect current scope
- `src/docs/README.md`, `src/docs/purpose.md`, and `src/docs/functionalities.md` if the copied app documentation needs to reflect current scope
- `dev_log/design-update-log.md` if interpreting plan changes current scope

## Checklist
1. Interpret the latest plan into actionable design and implementation scope.
2. Interpret the active `dev_log/` signals into design improvements or refinements.
3. Decide whether the copied project README or app docs need updates from the current plan.
4. Declare the exact in-scope IDs.
5. Declare what is explicitly out of scope.
6. Make sure each `UXF-*` has matching `REQ-*` and `ACC-*` coverage.
7. Make sure each `ACC-*` has a proving path through `TEST-*` or manual review.
8. Identify dependencies, reviewers, environments, or data needed to validate the scope.
9. Reduce scope if validation is not realistic for the current iteration.

## Stop conditions
- Intent is too vague to translate safely into design
- Scope depends on undefined AI behavior
- Acceptance cannot be validated with available test or eval methods
- Critical open question remains unresolved

## Done when
- Scope is explicit, bounded, and testable
- Intent has been translated into current design artifacts
- Relevant log findings have been reflected into the design update plan
- Required `src/README.md` and `src/docs/` updates are identified when applicable
- Every in-scope acceptance item is mapped
- Out-of-scope work is visible instead of implicit
