# Step 10 Prompt: Iteration Review

## Use This Prompt When

Use this prompt after validation, logging, and gap detection are complete for the current pass.

## Workflow Position

- Input step: final artifact state for the iteration
- Output step: explicit closeout status and next-loop readiness

## Objective

Confirm whether the iteration is complete, partial, or blocked; identify residual risks or follow-up work; and prepare the repo for the next loop without silently continuing into new scope.

## Required Read Order

Read and use:

1. Outputs from steps `01` through `09`
2. Relevant updated plan, design, tests, code, and logs
3. Current gap record and validation evidence

## Allowed Writes

- `intent/product-intent.md` to clear consumed current-cycle product intent
- `intent/feedback-intent.md` to clear consumed current-cycle feedback intent
- `intent/gaps.md` only to preserve the new gap record created by step `09` and remove consumed old gap content if needed
- If the repo uses a specific closeout artifact in the future, update only that approved artifact

## Required Outputs

Produce a closeout summary that includes:

- status: `complete`, `partial`, or `blocked`
- what was actually finished
- residual risks or explicit deferrals
- readiness for the next iteration
- whether new human input is required before continuing

## Procedure

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
   - current-turn intent
   - `.codex/project-context.md` and `.codex/tech-stack.md`
   - `plan/*`
   - `design/*`
   - `tests/*`
   - implementation source
3. Check that meaningful changes were captured in the correct artifacts and that validation evidence is recorded.
4. Decide whether the current iteration is `complete`, `partial`, or `blocked`.
5. State explicit deferrals, residual risks, and follow-up actions needed.
6. Clear consumed intake artifacts after the cycle is complete:
   - empty `intent/product-intent.md` back to its current-cycle template
   - empty `intent/feedback-intent.md` back to its current-cycle template
   - preserve only the new next-cycle gap record in `intent/gaps.md`
7. Prefer `python .codex/tools/appflow_run.py closeout-intake` when available so clearing is deterministic.
8. Do not start another iteration automatically. The next loop begins only when a new prompt, new feedback, or a surfaced gap changes the work.

## Guardrails

- Do not claim completion if validation or logs are missing.
- Do not hide misalignment between current-turn intent, design, code, and tests.
- Do not silently carry consumed product intent, feedback intent, or old gaps into the next loop.
- Do not treat a blocked iteration as done.

## Exit Criteria

- The current iteration has an explicit closeout state.
- Remaining risks and next actions are visible.
- Consumed product intent and feedback intent are cleared, and only new gaps remain for the next loop.
- Another agent can tell whether to stop, wait for a new prompt, or begin a fresh loop.
