# Step 02 Prompt: Create Plan

## Use This Prompt When

Use this prompt after reading intent and before changing context, design, tests, code, or logs.

## Objective

Translate current intent into explicit, traceable, iteration-scoped plan items across design, code, and tests.

## Required Inputs

Read and compare:

1. The outputs from step `01`
2. `plan/design-update.md`
3. `plan/code-update.md`
4. `plan/test-update.md`
5. Relevant `design/*`
6. Relevant `src/*`
7. Relevant `tests/*`
8. Active `dev_log/*`

## Instructions

1. Compare the latest intent against the current high-level context, design, tests, code, and logs.
2. Split needed work into:
   - `REQ-*` items for design changes
   - `DEV-*` items for implementation and execution work
   - `TEST-*` items for validation and proving work
3. Keep the current iteration explicit. Separate required work, known drift, blockers, and deferrals.
4. Preserve all important constraints, edge cases, and distinctions from intent.
5. Carry unresolved ambiguity into the plan instead of choosing a direction silently.
6. Put each item in the right plan file:
   - `plan/design-update.md`
   - `plan/code-update.md`
   - `plan/test-update.md`
7. Note when no work is required for a given layer.
8. Flag work that is out of scope as deferred or backlog rather than pulling it into the current pass.
9. If a problem is discovered during planning, classify it using only the allowed categories:
   - `design defect`
   - `implementation defect`
   - `test defect`
   - `eval gap`
   - `environment issue`
   - `backlog enhancement`

## Produce

Update the three plan files so they clearly state:

- current intent signal
- required changes
- existing drift or deviation
- open questions or blockers
- linked `REQ-*`, `DEV-*`, and `TEST-*` IDs

## Guardrails

- Do not change design, tests, or code in this step unless the contract requires an immediate workflow/context update first.
- Do not hide uncertainty.
- Do not create plan items that have no linkage to intent or detected gaps.
- Do not collapse multiple distinct workstreams into vague combined bullets.

## Exit Criteria

- The next design, test, and code steps know exactly what to do.
- The plan is traceable, scoped, and explicit about drift, blockers, and deferrals.
- No downstream implementation work depends on hidden assumptions.
