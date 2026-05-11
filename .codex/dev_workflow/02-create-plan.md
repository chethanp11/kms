# Step 02 Prompt: Create Plan

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after step `01` and before changing detailed design, tests, implementation, or logs.

## Workflow Position

- Input step: interpreted current-cycle product intent, feedback intent, and gaps
- Output step: refreshed traceable `REQ-*`, `DEV-*`, and `TEST-*` work in `plan/*`

## Objective

Translate prompt-derived current intent, feedback, gaps, and current repo state into an explicit iteration plan that downstream steps can execute without guessing. This step is mandatory for every file-changing app-mode cycle; stale plan files must be replaced or updated before downstream edits.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/planner.md`.
- Recommended skill support: criteria-traceability.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read and compare:

1. Step `01` intent brief
2. `.codex/state/current-intent.md`
3. `intent/product-intent.md`
4. `intent/feedback-intent.md`
5. `intent/gaps.md`
6. `plan/design-update.md`
7. `plan/code-update.md`
8. `plan/test-update.md`
9. Relevant `design/*`
10. Relevant `src/*`
11. Relevant `tests/*`
12. Active `dev_log/*`

## Allowed Writes

- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`

Create any missing plan file using the canonical names above.

## Required Outputs

The plan set must be refreshed for the current cycle and state:

- current intent signal, including product intent, feedback intent, and gap inputs
- required changes
- existing drift or deviation
- open questions or blockers
- linked `REQ-*`, `DEV-*`, and `TEST-*` IDs
- explicit `none` or equivalent when a layer has no work
- whether scaffolding is still initial scaffolding or whether new component/module creation requires explicit justification

## Procedure

1. Replace or update stale plan contents so all three plan files describe the current cycle, not prior iterations.
2. Compare current intent, product intent, feedback intent, and gaps against the current high-level context, design, tests, code, and logs.
3. Break work into three streams:
   - `REQ-*` for design and requirement interpretation changes
   - `DEV-*` for implementation and workflow execution work
   - `TEST-*` for proving and validation work
4. Preserve important constraints, edge cases, and policy gates from intent.
5. Carry ambiguity into the plan instead of choosing a direction silently.
6. Capture drift explicitly when the current repo state no longer matches intent, design, tests, or prior assumptions.
7. Identify whether design updates are required before tests/code; if not, state why design is unchanged.
8. For `src/` work after the initial scaffold exists, justify any new component family or module as absolutely necessary; otherwise plan changes inside existing components.
9. Separate required work, blockers, deferrals, and out-of-scope items.
10. Use the correct plan file for each change stream and keep the entries understandable by the next agent.
11. If a problem is discovered during planning, classify it using only the allowed categories:
   - `design defect`
   - `implementation defect`
   - `test defect`
   - `eval gap`
   - `environment issue`
   - `backlog enhancement`
12. If a request exceeds current scope, mark it for deferment or backlog instead of smuggling it into the current iteration.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not change design, tests, code, or logs in this step.
- Do not proceed to step `03`, `04`, or `05` with stale plan content.
- Do not hide uncertainty or convert it into fake clarity.
- Do not create plan items with no linkage to current-turn intent, detected gaps, or actual repo drift.
- Do not collapse unrelated workstreams into vague combined bullets.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- The next design, test, and implementation steps know exactly what to do.
- The plan is current-cycle scoped, traceable, and explicit about blockers and deferrals.
- No downstream step depends on hidden assumptions.
