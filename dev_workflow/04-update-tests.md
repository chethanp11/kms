# Step 04 Prompt: Update Tests

## Use This Prompt When

Use this prompt after design updates and before implementation whenever acceptance criteria, workflows, contracts, or system behavior changed.

## Workflow Position

- Input step: current design baseline
- Output step: acceptance-driven proof strategy and test assets

## Objective

Create or revise the validation layer from design and acceptance criteria before code changes are implemented.

## Required Read Order

Read and use:

1. Step `02` plan outputs
2. Step `03` design outputs
3. `design/acceptance-criteria.md`
4. `design/ux-flows.md`
5. Relevant architecture constraints
6. `tests/design-traceability.md`
7. `tests/test-plan.md`
8. Existing test suites, checklists, and validation assets relevant to the scope

## Allowed Writes

- `tests/design-traceability.md`
- `tests/test-plan.md`
- relevant test suites
- relevant smoke checklists, validation notes, or coverage assets under `tests/`

Create missing test planning or traceability files if they are required by the repo and not yet present.

## Required Outputs

Produce test and validation artifacts that:

- prove intended behavior before code changes begin
- map back to `ACC-*`, `UXF-*`, `ARCH-*`, and `REQ-*` where applicable
- state how the changed behavior will be validated in step `06`

## Procedure

1. Derive tests from design intent, not from implementation convenience.
2. Update `tests/design-traceability.md` so requirements, acceptance criteria, flows, constraints, and tests remain linked.
3. Update `tests/test-plan.md` so each meaningful validation item has a `TEST-*` record with layer, purpose, linked IDs, and proving location.
4. Add or revise actual test suites, checklists, fixtures, or validation assets appropriate to the repo.
5. Cover:
   - happy paths
   - edge cases
   - failure scenarios
   - gating or approval behavior
   - regression risks introduced by the change
6. Clearly mark manual or hybrid validation when ordinary automated tests cannot prove the behavior well.
7. Flag unclear or untestable design areas instead of masking them.
8. If the tests folder is empty on a first pass, scaffold the required validation structure from the design before proceeding.

## Guardrails

- Do not invent tests with no design linkage.
- Do not skip failure-path coverage because the happy path is obvious.
- Do not mistake a manual note for a real validation plan.
- Do not let code shape the tests before the design does.

## Exit Criteria

- The validation layer is ready before implementation starts.
- Each changed acceptance area has a proving path or an explicit limitation.
- Step `05` knows exactly what behavior must satisfy which tests.
