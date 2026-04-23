# Step 07 Prompt: Fix Failures

## Use This Prompt When

Use this prompt when step `06` returns `fail` or `partial`, or when validation exposes a blocker that must be resolved or explicitly deferred.

## Objective

Fix validation failures at the correct layer, classify the root cause, and loop back into validation until the result passes or is explicitly deferred.

## Required Inputs

Read and use:

1. Step `06` validation findings
2. The artifacts implicated by the failure
3. Relevant plan, design, test, or implementation context

## Instructions

1. Classify the failure using only the allowed categories:
   - `design defect`
   - `implementation defect`
   - `test defect`
   - `eval gap`
   - `environment issue`
   - `backlog enhancement`
2. Fix the failure at the correct layer:
   - design problems in design artifacts
   - test problems in test artifacts
   - implementation problems in code
   - validation gaps in validation assets or methods
3. If the failure reveals missing scope or ambiguous intent, update the appropriate upstream artifact before changing code behavior blindly.
4. Keep fixes tightly scoped to the failure and its direct dependencies.
5. Re-run the relevant validation after each fix.
6. Continue looping until the result is `pass` or the remaining issue is explicitly deferred with rationale.
7. If a failure cannot be resolved in the current scope, state the blocker clearly and preserve evidence for later steps.

## Produce

Produce a failure-resolution result that states:

- root-cause classification
- changes made to resolve the problem
- validation rerun status
- remaining blockers or explicit deferrals

## Guardrails

- Do not patch around a design problem with an implementation hack.
- Do not mark unresolved failures as fixed.
- Do not quietly expand scope to avoid hard decisions.
- Do not leave the loop without a clear pass or explicit deferral outcome.

## Exit Criteria

- Validation either passes or the remaining issue is explicitly deferred.
- The responsible layer has been corrected instead of merely suppressed.
- The iteration is ready for permanent logging in step `08`.
