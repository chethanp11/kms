# Step 05 Prompt: Implement Code

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts.

## Use This Prompt When

Use this prompt after plan, design, and tests are ready and `DEV-*` work remains to be implemented.

## Workflow Position

- Input step: approved design plus test-first proving plan
- Output step: implementation ready for explicit validation

## Objective

Implement approved `DEV-*` items in the correct implementation artifacts while staying aligned to intent, design, and planned tests.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/implementer.md`.
- Recommended skill support: architecture-review when implementation changes boundaries.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read and use:

1. Step `02` plan outputs
2. Step `03` design outputs
3. Step `04` test outputs
4. Relevant `src/*`
5. `.codex/tech-stack.md` when stack assumptions matter

## Allowed Writes

- relevant implementation files under `src/*`
- app scaffolding only when `src/` is empty or the plan/design explicitly states that initial scaffolding is still incomplete

## Required Outputs

Produce implementation changes that:

- satisfy the planned `DEV-*` work
- stay within existing scaffold/component families unless the plan and design explicitly justify a new one
- match approved design and correctness behavior
- are ready for explicit validation in step `06`

## Procedure

1. Implement only approved in-scope `DEV-*` work.
2. Keep implementation aligned to current plan, current design, and planned tests.
3. If `src/` is empty for a new project or first pass, scaffold it from design before broadening behavior.
4. Once initial scaffolding exists, do not add new component families, top-level modules, or architectural layers unless the current plan and design state why they are absolutely necessary. Prefer extending existing contracts, ports, stores, services, or tests.
5. Handle happy paths, edge cases, and failure paths required by design and tests.
6. Keep modules coherent. Minimize unnecessary duplication, hidden coupling, and scope creep.
7. If implementation reveals a design gap, missing acceptance rule, or test-design hole, update the correct upstream artifact before continuing blindly.
8. Leave explicit proof to step `06` and permanent logs to step `08`.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not invent behavior not represented in intent, plan, context, design, or correctness artifacts.
- Do not bypass tests or correctness criteria because the code path looks straightforward.
- Do not expand scope without reflecting it in upstream artifacts first.
- Do not continue adding scaffold-only components after the initial scaffold is present unless necessary and planned.
- Do not treat local implementation convenience as architecture.
- Do not record fake completion before validation has run.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- Implementation is complete for the approved `DEV-*` items.
- Behavior is aligned with plan, design, and planned validation.
- The changed artifacts are ready for targeted validation.
