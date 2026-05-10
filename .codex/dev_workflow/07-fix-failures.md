# Step 07 Prompt: Fix Failures

## Use This Prompt When

Use this prompt when step `06` returns `fail` or `partial`, or when validation exposes a blocker that must be resolved or explicitly deferred.

## Workflow Position

- Input step: failed or partial validation result
- Output step: corrected artifact state plus rerun-ready validation loop

## Objective

Fix validation failures at the correct layer, classify root cause precisely, and loop back into validation until the result passes or the remaining issue is explicitly deferred.

## Required Read Order

Read and use:

1. Step `06` validation findings
2. The artifacts implicated by the failure
3. Relevant plan, design, test, implementation, or contract context

## Allowed Writes

Only the layer actually responsible for the failure, for example:

- `plan/*` when the failure reveals missing scope or unresolved ambiguity
- `.codex/project-context.md` and `design/*` for design defects
- `tests/*` for test defects or eval gaps
- `src/*` and related app docs for implementation defects
- `AGENTS.md` and `.codex/project-context.md` when validation reveals a workflow or operating-rule problem

Do not update permanent logs in this step.

## Required Outputs

Produce a failure-resolution result that states:

- root-cause classification
- changes made to resolve the problem
- validation rerun status
- remaining blockers or explicit deferrals

## Procedure

1. Classify the failure using only the allowed categories:
   - `design defect`
   - `implementation defect`
   - `test defect`
   - `eval gap`
   - `environment issue`
   - `backlog enhancement`
2. Fix the failure at the correct layer rather than at the easiest layer.
3. If the failure reveals missing scope, ambiguous intent, or broken workflow rules, repair the correct upstream artifact before changing code blindly.
4. Keep fixes tightly scoped to the failure and its direct dependencies.
5. Re-run the relevant validation after each fix.
6. Continue looping until the result becomes `pass` or the unresolved remainder is explicitly deferred with rationale.
7. If a blocker cannot be resolved within the current scope, state it clearly and preserve evidence for logging and gap detection later.

## Guardrails

- Do not patch around a design problem with an implementation hack.
- Do not mark unresolved failures as fixed.
- Do not quietly expand scope to avoid hard decisions.
- Do not exit the validation loop without a clear pass or explicit deferral outcome.

## Exit Criteria

- Validation either passes or the remaining issue is explicitly deferred.
- The responsible layer has been corrected instead of merely suppressed.
- The iteration is ready for permanent logging in step `08`.
