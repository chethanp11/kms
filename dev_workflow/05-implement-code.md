# Step 05 Prompt: Implement Code

## Use This Prompt When

Use this prompt after planning, design, and tests are ready and `DEV-*` work remains to be implemented.

## Objective

Implement approved `DEV-*` items in the correct implementation artifacts while staying aligned to design and planned tests.

## Required Inputs

Read and use:

1. Step `02` plan outputs
2. Step `03` design outputs
3. Step `04` test outputs
4. Relevant `src/*`
5. `.codex/tech-stack.md` when stack assumptions matter

## Instructions

1. Implement only the approved in-scope `DEV-*` work.
2. Keep the code aligned to the current design and test expectations.
3. If `src/` is empty for a new project or first pass, scaffold it from design before broadening behavior.
4. Update `src/docs/` or the project README when implemented behavior changes and the repo expects application docs to stay current.
5. Keep modules coherent and avoid unnecessary coupling or duplication.
6. Handle happy paths, edge cases, and failure paths that the design and tests require.
7. If implementation exposes a design gap, update the correct upstream artifact instead of silently normalizing the code path.
8. If only implementation details change and behavior does not, keep design stable and avoid unnecessary design churn.
9. Leave validation evidence to step `06` and log recording to step `08`.

## Produce

Produce implementation changes that:

- satisfy the planned `DEV-*` work
- match the approved design
- are ready for the explicit validation step

## Guardrails

- Do not invent behavior not represented in intent, plan, context, design, or acceptance artifacts.
- Do not bypass tests or acceptance criteria because the code path seems straightforward.
- Do not expand scope without reflecting it in plan and design first.
- Do not record fake completion before validation has run.

## Exit Criteria

- Implementation is complete for the approved `DEV-*` items.
- Behavior is aligned with design and planned tests.
- The changed artifacts are ready for targeted validation.
