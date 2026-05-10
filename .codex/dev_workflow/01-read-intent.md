# Step 01 Prompt: Read Intent

## Use This Prompt When

Use this prompt after step `00-create-intent` to reconcile the prompt-derived current-turn intent brief with project context and repository constraints before planning, design, testing, coding, validation, or logging.

## Workflow Position

- Input step: `.codex/state/current-intent.md` plus current repo state
- Output step: a reconciled intent brief that step `02` can plan from

## Objective

Reconcile current-turn intent, project context, and repo constraints precisely enough that the rest of the workflow can proceed without guessing.

## Required Read Order

Read these in order:

1. `.codex/state/current-intent.md`
2. selected `.devmode/*` entry point
3. `.codex/project-context.md`
4. `.codex/tech-stack.md` when stack or validation may matter
5. Any user-referenced local artifacts that materially affect scope
6. Optional project-owned intent, feedback, requirements, or gap artifacts only when `.codex/project-context.md` says they are active for this application

## Allowed Writes

- Normally: none
- Exception: if the current request explicitly changes workflow, precedence, ownership, or operating rules, update the selected `.devmode/*` entry point and `.codex/project-context.md` immediately before ending this step

## Required Outputs

Produce an intent brief that states:

- the in-scope request
- explicit goals and required outcomes
- constraints and non-goals
- context, feedback, or gap inputs that matter now
- scope exclusions and deferrals
- ambiguities, conflicts, or missing information
- whether the repo contract or high-level context had to be updated first

## Procedure

1. Read the contract and high-level context first so intent is interpreted inside the repo rules.
2. Read only the active context and user-referenced artifacts needed before touching plan, design, tests, code, or logs.
3. Extract current goals, workflows, constraints, expected behavior, and explicit non-goals from the prompt-derived intent and project context.
4. Capture user-provided feedback, manual observations, and previously surfaced gaps that shape this iteration.
5. Distinguish prompt-derived intent from project context and evidence-backed gaps. Treat gap artifacts as evidence input, not as a requirements rewrite.
6. Identify whether the request is workflow-only, design-only, test-only, code-only, or a multi-layer change.
7. Identify direct dependencies that must be touched in the same pass and out-of-scope work that must not be pulled in.
8. Check whether the new request changes workflow, precedence, ownership, or operating rules. If yes, update the selected `.devmode/*` entry point and `.codex/project-context.md` now before any downstream work.
9. Record unresolved ambiguity explicitly. If the ambiguity is too risky to infer and cannot be resolved from the repo, ask the user a concise clarifying question. Otherwise carry it into plan.
10. Preserve detail. Do not compress away distinctions that will affect planning, design, testing, implementation, or validation.

## Guardrails

- Do not modify project-owned intent, feedback, or requirements artifacts unless explicitly asked by the user.
- Do not invent missing requirements.
- Do not plan from implementation convenience.
- Do not skip relevant feedback or gaps because they look secondary.
- Do not start coding or editing downstream artifacts in this step.

## Exit Criteria

- Current-turn intent and project context are reconciled well enough to plan without guessing.
- Scope boundaries, constraints, and unresolved ambiguities are explicit.
- Any required contract or high-level context updates have already been applied.
