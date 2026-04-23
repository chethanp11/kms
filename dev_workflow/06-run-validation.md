# Step 06 Prompt: Run Validation

## Use This Prompt When

Use this prompt after implementation or after any meaningful design, test, workflow, or documentation change that requires explicit proof.

## Workflow Position

- Input step: changed artifacts are ready for proof
- Output step: real validation outcome for the current iteration state

## Objective

Run the right validation for the changed scope, collect real evidence, and determine whether the iteration currently passes, fails, or remains only partially proven.

## Required Read Order

Read and use:

1. The changed artifacts from steps `03`, `04`, and `05`
2. `tests/test-plan.md`
3. Relevant validation assets and commands for the repo
4. Any acceptance criteria or design constraints needed to interpret results

## Allowed Writes

- No permanent workflow artifacts are required to be updated in this step
- Temporary local reasoning notes are fine, but permanent logging belongs to step `08`

## Required Outputs

Produce a validation result summary that includes:

- validation activity type
- commands or method used
- result: `pass`, `fail`, or `partial`
- key findings
- failure classification when relevant
- follow-up needed for step `07`

## Procedure

1. Select validation that matches the changed layer:
   - design changes: structured manual review against intent, traceability, acceptance, and architecture
   - test changes: targeted execution or checklist review
   - code changes: targeted unit, integration, e2e, regression, or smoke checks
   - workflow or documentation changes: manual review plus structural checks such as `git diff --check`
2. Prefer targeted, relevant validation over broad but low-signal runs.
3. Run enough checks to prove the changed scope, not just the easiest available command.
4. Capture exact commands or exact manual-review method.
5. Record whether the current result is `pass`, `fail`, or `partial`.
6. Summarize what was proven, what failed, and what remains unproven.
7. If validation cannot run because of tooling, environment, or dependency issues, classify that explicitly as an `environment issue`.
8. If the result is `fail` or `partial`, hand off to step `07` instead of pretending the iteration is complete.

## Guardrails

- Do not claim a pass without real evidence.
- Do not fabricate commands, outputs, or coverage.
- Do not skip validation because the change looks small.
- Do not write permanent final validation logs before the validation-fix loop is resolved.

## Exit Criteria

- The iteration has a real current validation result.
- The next action is explicit: proceed to step `07` or continue to step `08`.
- Evidence is specific enough to be recorded accurately in logs later.
