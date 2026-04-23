# Step 10 Prompt: Iteration Review

## Use This Prompt When

Use this prompt after validation, logging, and gap detection are complete for the current pass.

## Objective

Confirm whether the iteration is complete, identify residual risks or follow-up work, and prepare the repo for the next loop without silently continuing into new scope.

## Required Inputs

Read and use:

1. The outputs from steps `01` through `09`
2. Relevant updated plan, design, tests, code, and logs
3. The current gap record and validation evidence

## Instructions

1. Review the full iteration for:
   - requirement coverage
   - architectural alignment
   - code quality and modularity
   - duplication and coupling
   - failure handling
   - performance risks
   - security considerations
   - test sufficiency
2. Confirm that the source-of-truth order still holds:
   - `intent/*`
   - `plan/*`
   - `.codex/project-context.md`
   - `design/*`
   - `tests/*`
   - `src/*`
3. Check that meaningful changes were captured in the correct artifacts and that validation evidence is recorded.
4. Decide whether the iteration outcome is:
   - complete
   - partial
   - blocked
5. State any explicit deferrals, residual risks, or follow-up actions needed.
6. Do not start another iteration automatically. The next loop begins only when intent, feedback, or validated gap input changes the work.

## Produce

Produce a closeout summary that includes:

- status: complete, partial, or blocked
- what was actually finished
- residual risks or deferrals
- readiness for the next iteration
- whether new human input is required before continuing

## Guardrails

- Do not claim completion if validation or logs are missing.
- Do not hide misalignment between intent, design, code, and tests.
- Do not silently carry unresolved scope into the next loop.
- Do not treat a blocked iteration as done.

## Exit Criteria

- The current iteration has an explicit closeout state.
- Remaining risks and next actions are visible.
- The repository is ready either for pause or for the next intent-driven loop.
