# 02 Iteration Scope

## Purpose
Define the exact work for the next iteration by interpreting intent and dev logs into updated design scope and proof requirements.

## Read first
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`
- `intent/feedback-intent.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `design/build-scope.md`
- `design/acceptance-criteria.md`
- relevant files from `design/`
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `dev_log/backlog.md`
- `dev_log/feedback-log.md`

## Update
- `design/build-scope.md`
- `design/acceptance-criteria.md` if acceptance is changing
- relevant files in `design/` that need to reflect current intent
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `src/README.md` if the project README needs to reflect current scope
- `src/docs/README.md`, `src/docs/purpose.md`, and `src/docs/functionalities.md` if the copied app documentation needs to reflect current scope
- `design/open-questions.md` if ambiguities remain
- `dev_log/change-log.md` if interpreting intent changes current scope

## Checklist
1. Interpret human intent into actionable design and implementation scope.
2. Interpret `dev_log/*` signals into design improvements, refinements, or backlog items.
3. Decide whether the copied project README or app docs need updates from the current intent.
4. Declare the exact in-scope IDs.
5. Declare what is explicitly out of scope.
6. Make sure each `ACC-*` has a proving path through `TEST-*`, `EVAL-*`, or manual review.
7. Identify dependencies, reviewers, environments, or data needed to validate the scope.
8. Reduce scope if validation is not realistic for the current iteration.

## Stop conditions
- Intent is too vague to translate safely into design
- Scope depends on undefined AI behavior
- Acceptance cannot be validated with available test or eval methods
- Critical open question remains unresolved

## Done when
- Scope is explicit, bounded, and testable
- Intent has been translated into current design artifacts
- Relevant dev log findings have been reflected into the design update plan
- Required `src/README.md` and `src/docs/` updates are identified when applicable
- Every in-scope acceptance item is mapped
- Out-of-scope work is visible instead of implicit
