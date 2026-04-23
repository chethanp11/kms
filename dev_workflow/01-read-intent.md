# Step 01 Prompt: Read Intent

## Use This Prompt When

Use this prompt at the start of every task or iteration before planning, design, testing, coding, validation, or logging.

## Workflow Position

- Input step: external request plus current repo state
- Output step: a complete intent brief that step `02` can plan from

## Objective

Interpret current human intent and repo constraints precisely enough that the rest of the workflow can proceed without guessing.

## Required Read Order

Read these in order:

1. `AGENTS.md`
2. `.codex/project-context.md`
3. `intent/product-intent.md`
4. `intent/feedback-intent.md`
5. `intent/gaps.md` when present
6. Any user-referenced local artifacts that materially affect scope

## Allowed Writes

- Normally: none
- Exception: if the current request explicitly changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` immediately before ending this step

## Required Outputs

Produce an intent brief that states:

- the in-scope request
- explicit goals and required outcomes
- constraints and non-goals
- feedback or gap inputs that matter now
- scope exclusions and deferrals
- ambiguities, conflicts, or missing information
- whether the repo contract or high-level context had to be updated first

## Procedure

1. Read the contract and high-level context first so intent is interpreted inside the repo rules.
2. Read all active human input files before touching plan, design, tests, code, or logs.
3. Extract current goals, users, workflows, constraints, expected behavior, and explicit non-goals.
4. Capture feedback-driven changes, manual observations, and previously surfaced gaps that shape this iteration.
5. Distinguish human intent from system-detected gaps. Treat `intent/gaps.md` as evidence input, not as a human requirements rewrite.
6. Identify whether the request is workflow-only, design-only, test-only, code-only, or a multi-layer change.
7. Identify direct dependencies that must be touched in the same pass and out-of-scope work that must not be pulled in.
8. Check whether the new request changes workflow, precedence, ownership, or operating rules. If yes, update `AGENTS.md` and `.codex/project-context.md` now before any downstream work.
9. Record unresolved ambiguity explicitly. If the ambiguity is too risky to infer and cannot be resolved from the repo, ask the user a concise clarifying question. Otherwise carry it into plan.
10. Preserve detail. Do not compress away distinctions that will affect planning, design, testing, implementation, or validation.

## Guardrails

- Do not modify `intent/product-intent.md` or `intent/feedback-intent.md` unless explicitly asked by the user.
- Do not invent missing requirements.
- Do not plan from implementation convenience.
- Do not skip feedback or gaps because they look secondary.
- Do not start coding or editing downstream artifacts in this step.

## Exit Criteria

- Current intent is understood well enough to plan without guessing.
- Scope boundaries, constraints, and unresolved ambiguities are explicit.
- Any required contract or high-level context updates have already been applied.
