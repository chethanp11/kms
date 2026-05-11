# Step 08 Prompt: Update Logs

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after the iteration has a final validation outcome for the current pass and the actual design, test, and code changes are known.

## Workflow Position

- Input step: final changed artifacts plus final validation outcome
- Output step: permanent execution record

## Objective

Record what actually changed and what was actually validated in the permanent `dev_log/*` artifacts.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/documentation.md`.
- Recommended skill support: plan-log-mapping.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read and use:

1. Final design, test, and code diffs for the iteration
2. Final validation evidence from steps `06` and `07`
3. Existing `dev_log/*` entries
4. Linked `REQ-*`, `DEV-*`, `TEST-*`, `ARCH-*`, and feedback IDs when relevant

## Allowed Writes

- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`

Create any missing canonical log file using the approved filenames above.

## Required Outputs

Produce factual log entries that state:

- what changed
- why it changed
- which IDs it links to
- which intent sources drove it
- what validation actually happened
- what follow-up remains, if any

## Procedure

1. Use the repo's existing log structure and next available entry numbering convention.
2. Update only the logs that correspond to real work that actually happened.
3. Record design, code, and test changes separately when they were genuinely distinct.
4. Record validation with the real method, commands, result, findings, failure classification, and follow-up.
5. Include enough traceability so another agent can continue without archaeology.
6. Link log entries back to the relevant IDs and intent sources.
7. If a layer did not change, do not force a meaningless log entry.
8. Keep the log factual. Describe what changed and what was proven, not what was intended earlier.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not fabricate validation evidence.
- Do not log planned work that was not executed.
- Do not merge unrelated change types into vague single entries.
- Do not leave the iteration without recording the real validation outcome.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- The permanent logs reflect the iteration accurately.
- Validation evidence is durable, traceable, and usable by the next agent.
- Step `09` can detect system gaps from reliable log data.
