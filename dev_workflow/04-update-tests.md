# Step 04 Prompt: Update Tests

## Use This Prompt When

Use this prompt after design updates and before implementation when acceptance criteria, workflows, or system behavior changed.

## Objective

Create or revise the validation layer from design and acceptance criteria before code changes are implemented.

## Required Inputs

Read and use:

1. Step `02` plan outputs
2. Step `03` design outputs
3. `design/acceptance-criteria.md`
4. `design/ux-flows.md`
5. Relevant architecture constraints
6. `tests/design-traceability.md`
7. `tests/test-plan.md`

## Instructions

1. Derive tests from design intent, not from implementation convenience.
2. Update `tests/design-traceability.md` so requirements, acceptance criteria, flows, constraints, and tests remain linked.
3. Update `tests/test-plan.md` so each meaningful validation item has a `TEST-*` record with layer, purpose, linked IDs, and proving location.
4. Add or revise actual test suites, checklists, or validation assets as appropriate for the repo.
5. Cover:
   - happy paths
   - edge cases
   - failure scenarios
   - approval or gating behavior
   - regression risks introduced by the planned change
6. Clearly mark manual or hybrid validation when ordinary automated tests cannot prove the behavior well.
7. Flag unclear or untestable design areas instead of masking them.
8. Keep test artifacts aligned with acceptance criteria and current design structure.

## Produce

Produce test and validation artifacts that:

- prove the intended behavior before code changes begin
- map back to `ACC-*`, `UXF-*`, `ARCH-*`, and `REQ-*` where applicable
- make validation expectations explicit for the implementation and validation steps

## Guardrails

- Do not invent tests with no design linkage.
- Do not skip failure-path coverage because the happy path is obvious.
- Do not mistake a manual note for real validation planning.
- Do not let code shape the tests before the design does.

## Exit Criteria

- The validation layer is ready before implementation starts.
- Each changed acceptance area has a proving path or an explicit limitation.
- Traceability is updated enough to detect missing coverage later.
