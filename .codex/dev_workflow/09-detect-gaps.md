# Step 09 Prompt: Detect Gaps

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after logs and validation results are current and the system needs to surface evidence-backed follow-on gaps for future reconciliation.

## Workflow Position

- Input step: permanent logs plus final validation evidence
- Output step: new system gap record for the next iteration

## Objective

Create the next-cycle system-managed gap record from evidence in logs, validation outcomes, repeated failures, unresolved deferrals, or persistent repo misalignment. Treat pre-existing gaps as already-consumed input unless the current cycle produced evidence that they remain unresolved.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/governance.md`.
- Recommended skill support: design-audit for drift; feedback-triage for unresolved feedback.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read and use:

1. `dev_log/design-update-log.md`
2. `dev_log/code-update-log.md`
3. `dev_log/test-update-log.md`
4. `dev_log/validation-results.md`
5. The current `intent/gaps.md` as old gap input consumed by this cycle

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
4. Replace `intent/gaps.md` with only next-cycle gaps produced by this cycle.
5. Do not carry old gaps forward by default; repeat an old gap only when this cycle produced evidence that it remains unresolved.
6. Include priority, source evidence, and suggested next action when a new gap exists.
7. If no new gap is detected, write an explicit empty-gaps record for the next cycle.
8. Keep the file system-generated in tone. It is not a manual feedback note and not a product-backlog wish list.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not modify human-authored intent or feedback in this step.
- Do not add speculative gaps without evidence.
- Do not hide repeated failures that should shape the next loop.
- Do not turn a known blocker into silent backlog drift.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- `intent/gaps.md` reflects only new or still-evidenced system-detected gaps exposed by the iteration.
- The next planning step can consume the gap record directly.
