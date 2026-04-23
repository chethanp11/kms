# Step 05 Prompt: Implement Code

## Use This Prompt When

Use this prompt after plan, design, and tests are ready and `DEV-*` work remains to be implemented.

## Workflow Position

- Input step: approved design plus test-first proving plan
- Output step: implementation ready for explicit validation

## Objective

Implement approved `DEV-*` items in the correct implementation artifacts while staying aligned to intent, design, and planned tests.

## Required Read Order

Read and use:

1. Step `02` plan outputs
2. Step `03` design outputs
3. Step `04` test outputs
4. Relevant `src/*`
5. `.codex/tech-stack.md` when stack assumptions matter

## Allowed Writes

- relevant implementation files under `src/*`
- app scaffolding when `src/` is empty on a first implementation pass

## Required Outputs

Produce implementation changes that:

- satisfy the planned `DEV-*` work
- match approved design and acceptance behavior
- are ready for explicit validation in step `06`

## Procedure

1. Implement only approved in-scope `DEV-*` work.
2. Keep implementation aligned to current plan, current design, and planned tests.
3. If `src/` is empty for a new project or first pass, scaffold it from design before broadening behavior.
4. Handle happy paths, edge cases, and failure paths required by design and tests.
5. Keep modules coherent. Minimize unnecessary duplication, hidden coupling, and scope creep.
6. If implementation reveals a design gap, missing acceptance rule, or test-design hole, update the correct upstream artifact before continuing blindly.
7. Leave explicit proof to step `06` and permanent logs to step `08`.

## Guardrails

- Do not invent behavior not represented in intent, plan, context, design, or acceptance artifacts.
- Do not bypass tests or acceptance criteria because the code path looks straightforward.
- Do not expand scope without reflecting it in upstream artifacts first.
- Do not treat local implementation convenience as architecture.
- Do not record fake completion before validation has run.

## Exit Criteria

- Implementation is complete for the approved `DEV-*` items.
- Behavior is aligned with plan, design, and planned validation.
- The changed artifacts are ready for targeted validation.
