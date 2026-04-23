# Step 02 Prompt: Create Plan

## Use This Prompt When

Use this prompt after step `01` and before changing detailed design, tests, implementation, or logs.

## Workflow Position

- Input step: interpreted intent
- Output step: traceable `REQ-*`, `DEV-*`, and `TEST-*` work in `plan/*`

## Objective

Translate current intent and current repo state into an explicit iteration plan that downstream steps can execute without guessing.

## Required Read Order

Read and compare:

1. Step `01` intent brief
2. `plan/design-update.md`
3. `plan/code-update.md`
4. `plan/test-update.md`
5. Relevant `design/*`
6. Relevant `src/*`
7. Relevant `tests/*`
8. Active `dev_log/*`

## Allowed Writes

- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`

Create any missing plan file using the canonical names above.

## Required Outputs

The plan set must state:

- current intent signal
- required changes
- existing drift or deviation
- open questions or blockers
- linked `REQ-*`, `DEV-*`, and `TEST-*` IDs
- explicit `none` or equivalent when a layer has no work

## Procedure

1. Compare current intent against the current high-level context, design, tests, code, and logs.
2. Break work into three streams:
   - `REQ-*` for design and requirement interpretation changes
   - `DEV-*` for implementation and workflow execution work
   - `TEST-*` for proving and validation work
3. Preserve important constraints, edge cases, and policy gates from intent.
4. Carry ambiguity into the plan instead of choosing a direction silently.
5. Capture drift explicitly when the current repo state no longer matches intent, design, tests, or prior assumptions.
6. Separate required work, blockers, deferrals, and out-of-scope items.
7. Use the correct plan file for each change stream and keep the entries understandable by the next agent.
8. If a problem is discovered during planning, classify it using only the allowed categories:
   - `design defect`
   - `implementation defect`
   - `test defect`
   - `eval gap`
   - `environment issue`
   - `backlog enhancement`
9. If a request exceeds current scope, mark it for deferment or backlog instead of smuggling it into the current iteration.

## Guardrails

- Do not change design, tests, code, or logs in this step.
- Do not hide uncertainty or convert it into fake clarity.
- Do not create plan items with no linkage to intent, detected gaps, or actual repo drift.
- Do not collapse unrelated workstreams into vague combined bullets.

## Exit Criteria

- The next design, test, and implementation steps know exactly what to do.
- The plan is scoped, traceable, and explicit about blockers and deferrals.
- No downstream step depends on hidden assumptions.
