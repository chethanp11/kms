# Step 09 Prompt: Detect Gaps

## Use This Prompt When

Use this prompt after logs and validation results are current and the system needs to surface follow-on gaps for future reconciliation.

## Objective

Update the system-managed gap record from evidence in logs, validation outcomes, repeated failures, and unresolved deferrals.

## Required Inputs

Read and use:

1. `dev_log/design-update-log.md`
2. `dev_log/code-update-log.md`
3. `dev_log/test-update-log.md`
4. `dev_log/validation-results.md`
5. The current `intent/gaps.md`

## Instructions

1. Review the permanent log evidence and validation outcomes, not just the latest user request.
2. Identify system-detected gaps such as:
   - missing capability
   - design inconsistency
   - implementation drift
   - missing or weak validation
   - repeated failure pattern
   - blocked work caused by environment or dependencies
3. Distinguish real evidence-backed gaps from human preference or interpretation.
4. Update `intent/gaps.md` using the repo's current structure and language.
5. Include priority, source evidence, and a suggested next action when the gap record format expects them.
6. If no new gap is detected, keep the record truthful. Either leave it unchanged or state explicitly that no additional system-detected gaps were found, following repo conventions.
7. Keep this file system-generated in tone. Do not rewrite it as a human feedback essay.

## Produce

Produce a gap record that tells the next planning step:

- what gap exists
- how important it is
- which evidence exposed it
- what kind of downstream action is likely needed

## Guardrails

- Do not modify human-authored intent or feedback in this step.
- Do not add speculative gaps without evidence.
- Do not hide repeated failures that should shape the next loop.
- Do not turn a known blocker into silent backlog drift.

## Exit Criteria

- `intent/gaps.md` reflects the actual system-detected gaps exposed by the iteration.
- The next planning step can consume the gap record directly.
