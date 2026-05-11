# Step 01 Prompt: Read Intent

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after step `00-create-intent` to reconcile the prompt-derived current-turn intent brief with project context and repository constraints before planning, design, testing, coding, validation, or logging.

## Workflow Position

- Input step: `.codex/state/current-intent.md`, `intent/product-intent.md`, `intent/feedback-intent.md`, `intent/gaps.md`, plus current repo state
- Output step: a reconciled intent brief that step `02` can plan from

## Objective

Reconcile current-turn intent, project context, and repo constraints precisely enough that the rest of the workflow can proceed without guessing.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/governance.md`.
- Recommended skill support: feedback-triage for feedback prompts; mode-boundary-review for mode-sensitive scope.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read these in order:

1. `.codex/state/current-intent.md`
2. `intent/product-intent.md`
3. `intent/feedback-intent.md`
4. `intent/gaps.md`
5. selected `.devmode/*` entry point
6. `.codex/project-context.md`
7. `.codex/tech-stack.md` when stack or validation may matter
8. Any user-referenced local artifacts that materially affect scope

## Allowed Writes

- Normally: none
- Exception: if the current request explicitly changes workflow, precedence, ownership, or operating rules, update the selected `.devmode/*` entry point and `.codex/project-context.md` immediately before ending this step

## Required Outputs

Produce an intent brief that states:

- the in-scope request
- explicit goals and required outcomes
- constraints and non-goals
- product-intent, feedback-intent, and gap inputs that matter now, including explicit note when any channel is empty
- scope exclusions and deferrals
- ambiguities, conflicts, or missing information
- whether the repo contract or high-level context had to be updated first

## Procedure

1. Read the contract and high-level context first so intent is interpreted inside the repo rules.
2. Read only the active context and user-referenced artifacts needed before touching plan, design, tests, code, or logs.
3. Extract current goals, workflows, constraints, expected behavior, and explicit non-goals from the prompt-derived intent and project context.
4. Capture the current product-intent channel, feedback-intent channel, and existing gap channel even when one or more are empty.
5. Progress all non-empty channels into reconciliation:
   - product intent becomes scoped work for planning
   - feedback intent becomes triaged work, design correction, test expectation, implementation repair, or logged deferral
   - existing gaps become evidence-backed inputs to plan/design/test/code decisions or explicit deferrals
6. Distinguish prompt-derived intent from project context and evidence-backed gaps. Treat gap artifacts as evidence input, not as a requirements rewrite.
7. Identify whether the request is workflow-only, design-only, test-only, code-only, or a multi-layer change.
8. Identify direct dependencies that must be touched in the same pass and out-of-scope work that must not be pulled in.
9. Check whether the new request changes workflow, precedence, ownership, or operating rules. If yes, update the selected `.devmode/*` entry point and `.codex/project-context.md` now before any downstream work.
10. Record unresolved ambiguity explicitly. If the ambiguity is too risky to infer and cannot be resolved from the repo, ask the user a concise clarifying question. Otherwise carry it into plan.
11. Preserve detail. Do not compress away distinctions that will affect planning, design, testing, implementation, or validation.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not modify intake artifacts in this step; step `00` populates product/feedback intent, step `09` writes new gaps, and step `10` clears consumed intake.
- Do not invent missing requirements.
- Do not plan from implementation convenience.
- Do not skip relevant feedback or gaps because they look secondary.
- Do not start coding or editing downstream artifacts in this step.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- Current-turn intent and project context are reconciled well enough to plan without guessing.
- Scope boundaries, constraints, and unresolved ambiguities are explicit.
- Any required contract or high-level context updates have already been applied.
