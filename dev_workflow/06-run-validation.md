# Step 06 Prompt: Run Validation

## Use This Prompt When

Use this prompt after implementation or any meaningful design, test, workflow, or documentation change that requires explicit proof.

## Objective

Run the right validation for the changed scope, collect real evidence, and determine whether the iteration passes, fails, or is only partially proven.

## Required Inputs

Read and use:

1. The changed artifacts from steps `03`, `04`, and `05`
2. `tests/test-plan.md`
3. Relevant validation assets and commands for the repo
4. Any acceptance criteria or design constraints needed to interpret results

## Instructions

1. Select validation that matches the changed layer:
   - design changes: structured manual review against intent and traceability
   - test changes: targeted execution or checklist review
   - code changes: targeted unit, integration, e2e, regression, or smoke checks
   - workflow or documentation changes: manual review and structural checks such as `git diff --check`
2. Prefer targeted, relevant validation over broad but low-signal runs.
3. Run enough checks to prove the changed scope, not just the easiest command available.
4. Capture the exact commands or review method used.
5. Record whether the outcome is `pass`, `fail`, or `partial`.
6. Summarize key findings, including what was proven and what remains unproven.
7. If validation cannot run because of tooling, environment, or dependency issues, classify that explicitly as an `environment issue`.
8. Do not update logs yet unless the repo requires temporary scratch notes outside the permanent log files.

## Produce

Produce a validation result summary that includes:

- validation activity type
- commands or method used
- result: `pass`, `fail`, or `partial`
- key findings
- failure classification when relevant
- follow-up needed for step `07`

## Guardrails

- Do not claim a pass without real evidence.
- Do not fabricate commands, outputs, or coverage.
- Do not skip validation because the change looks small.
- Do not log final validation evidence before the validation/fix loop is complete.

## Exit Criteria

- The iteration has a real validation result.
- The next action is explicit: proceed to logs, or enter the failure-fix loop.
- Evidence is specific enough to be recorded accurately in step `08`.
