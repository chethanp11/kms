# Step 09 Prompt: Detect Gaps

## Use This Prompt When

Use this prompt after logs and validation results are current and the system needs to surface evidence-backed follow-on gaps for future reconciliation.

## Workflow Position

- Input step: permanent logs plus final validation evidence
- Output step: updated system gap record for the next iteration

## Objective

Update the system-managed gap record from evidence in logs, validation outcomes, repeated failures, unresolved deferrals, or persistent repo misalignment.

## Required Read Order

Read and use:

1. `dev_log/design-update-log.md`
2. `dev_log/code-update-log.md`
3. `dev_log/test-update-log.md`
4. `dev_log/validation-results.md`
5. The current `intent/gaps.md`

## Allowed Writes

- `intent/gaps.md` only

## Required Outputs

Produce a gap record that tells the next planning step:

- what gap exists
- how important it is
- which evidence exposed it
- what kind of downstream action is likely needed

## Procedure

1. Review permanent log evidence and validation outcomes, not just the latest user prompt.
2. Identify system-detected gaps such as:
   - missing capability
   - design inconsistency
   - implementation drift
   - missing or weak validation
   - repeated failure pattern
   - blocked work caused by environment or dependencies
3. Distinguish real evidence-backed gaps from human preference or interpretation.
4. Update `intent/gaps.md` using the repo's current structure and tone.
5. Include priority, source evidence, and suggested next action when the gap record format expects them.
6. If no new gap is detected, keep the record truthful. Leave it unchanged or explicitly state that no new system-detected gap was exposed, following current repo conventions.
7. Keep the file system-generated in tone. It is not a manual feedback note and not a product-backlog wish list.

## Guardrails

- Do not modify human-authored intent or feedback in this step.
- Do not add speculative gaps without evidence.
- Do not hide repeated failures that should shape the next loop.
- Do not turn a known blocker into silent backlog drift.

## Exit Criteria

- `intent/gaps.md` reflects the actual system-detected gaps exposed by the iteration.
- The next planning step can consume the gap record directly.
