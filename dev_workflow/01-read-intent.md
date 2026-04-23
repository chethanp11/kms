# Step 01 Prompt: Read Intent

## Use This Prompt When

Use this prompt at the start of a new task or iteration before planning, design, testing, coding, or validation.

## Objective

Establish the current human intent, scope boundary, constraints, feedback, and known gaps without changing downstream artifacts yet.

## Required Inputs

Read these in order:

1. `AGENTS.md`
2. `.codex/project-context.md`
3. `intent/product-intent.md`
4. `intent/feedback-intent.md`
5. `intent/gaps.md` when present

## Instructions

1. Read the contract and high-level context first.
2. Read all active intent inputs before touching plan, design, tests, code, or logs.
3. Extract the current product goals, explicit constraints, workflows, acceptance expectations, and non-goals.
4. Capture any feedback-driven changes, surprises, weak points, or manual observations that affect the next iteration.
5. Review `intent/gaps.md` only as system-detected evidence, not as human reinterpretation.
6. Identify the in-scope request, the out-of-scope items, and anything that must be deferred.
7. Note conflicts, ambiguity, or drift between intent and the apparent repo state, but do not resolve them in this step.
8. If the current request changes workflow, precedence, ownership, or operating rules, plan to update `AGENTS.md` and `.codex/project-context.md` before downstream work.
9. Preserve detail. Do not compress away distinctions that will affect behavior, planning, or validation.

## Produce

Produce a concise step result that includes:

- current scope
- explicit constraints
- required behavior or outcomes
- known feedback and gaps that matter now
- open questions or ambiguities
- whether contract/context updates are required before later steps

## Guardrails

- Do not modify `intent/*` unless explicitly asked, except for the system-managed gaps step later in the workflow.
- Do not invent missing requirements.
- Do not start planning from implementation convenience.
- Do not skip feedback or gaps because they seem secondary.

## Exit Criteria

- Current intent is understood well enough to plan without guessing.
- Scope boundaries and unresolved ambiguities are explicit.
- Any required contract or context updates are identified before downstream changes.
