# Workflow Improvement

## Purpose
Describe how to improve the template or workflow itself without corrupting an active project iteration.

## When to use
- When the template itself needs refinement.
- When a recurring process gap is identified.
- When multiple iterations reveal the same confusion or missing artifact.

## Improvement loop
1. Identify improvement candidates in `intent/feedback-intent.md`, `dev_log/feedback-log.md`, or `dev_log/deviations-log.md`.
2. Confirm the issue is about the workflow or template, not just the current project implementation.
3. Decide whether the fix belongs in design guidance, test guidance, logs, workflow prompts, skills, folder structure, or intent templates.
4. Apply the smallest reusable change that solves the repeated problem.
5. Record the improvement in `dev_log/change-log.md` with a `DEV-*` reference.

## Outputs
- A proposed template improvement summary.
- Updated workflow or template files with clear change rationale.
- A note in `dev_log/change-log.md` linking the improvement to the relevant `DEV-*`.

## Rules and cautions
- Do not let template improvements delay active product work.
- Do not change iteration exit criteria mid-flight without explicit approval.
- Keep improvements practical, reusable, and implementation-oriented.
