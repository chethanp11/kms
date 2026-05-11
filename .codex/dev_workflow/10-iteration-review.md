# Step 10 Prompt: Iteration Review

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after validation, logging, and gap detection are complete for the current pass.

## Workflow Position

- Input step: final artifact state for the iteration
- Output step: explicit closeout status and next-loop readiness

## Objective

Confirm whether the iteration is complete, partial, or blocked; identify residual risks or follow-up work; and prepare the repo for the next loop without silently continuing into new scope.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/reviewer.md`.
- Recommended skill support: release-closeout; design-audit before final sign-off.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

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

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not claim completion if validation or logs are missing.
- Do not hide misalignment between current-turn intent, design, code, and tests.
- Do not silently carry consumed product intent, feedback intent, or old gaps into the next loop.
- Do not treat a blocked iteration as done.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- The current iteration has an explicit closeout state.
- Remaining risks and next actions are visible.
- Consumed product intent and feedback intent are cleared, and only new gaps remain for the next loop.
- Another agent can tell whether to stop, wait for a new prompt, or begin a fresh loop.
