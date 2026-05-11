# Step 04 Prompt: Update Tests

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after design updates and before implementation whenever correctness criteria, workflows, contracts, or system behavior changed.

## Workflow Position

- Input step: current design baseline
- Output step: criteria-driven proof strategy and test assets

## Objective

Create or revise the validation layer from design and correctness criteria before code changes are implemented.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/validator.md`.
- Recommended skill support: criteria-traceability; test-repair when validation assets are stale.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

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
- map back to ``UXF-*`, `ARCH-*`, and `REQ-*` where applicable
- state how the changed behavior will be validated in step `06`

## Procedure

1. Derive tests from design intent, not from implementation convenience.
2. Update `tests/design-traceability.md` so requirements, correctness criteria, flows, constraints, and tests remain linked.
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

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not invent tests with no design linkage.
- Do not skip failure-path coverage because the happy path is obvious.
- Do not mistake a manual note for a real validation plan.
- Do not let code shape the tests before the design does.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- The validation layer is ready before implementation starts.
- Each changed correctness area has a proving path or an explicit limitation.
- Step `05` knows exactly what behavior must satisfy which tests.
