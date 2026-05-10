# Step 00 Prompt: Create Intent

## Use This Prompt When

Use this prompt at the start of every AppFlow turn. This step converts the user's raw prompt into a structured intent brief before existing project intent files are read.

## Workflow Position

- Input step: user prompt
- Output step: structured current-turn intent brief for step `01`

## Objective

Capture what the user asked for, what must change, and what must not be assumed so the rest of AppFlow starts from explicit intent instead of chat memory.

## Required Read Order

Read these in order:

1. The current user prompt
2. `.codex/AGENTS.md`
3. root `AGENTS.md`
4. `.codex/project-context.md`
5. `.codex/tech-stack.md` when stack or validation may matter

## Allowed Writes

- `.codex/state/current-intent.md`
- `.codex/state/appflow-current.json` through `.codex/tools/appflow_run.py` when lifecycle evidence is being tracked

Do not edit human-owned project intent files in this step unless the user explicitly asks.

## Required Outputs

Create a current-turn intent brief that states:

- raw user prompt summary
- interpreted objective
- explicit deliverables
- constraints and non-goals
- likely impacted artifact layers
- validation expectations
- ambiguity or HITL checkpoints
- whether this is project-specific work or reusable AppFlow factory work

## Procedure

1. Treat the user prompt as the source of intent for this turn.
2. Preserve user wording where it affects scope, constraints, or priority.
3. Separate explicit requirements from inferred implementation ideas.
4. Identify whether the work affects workflow, product behavior, tests, runtime code, docs, or validation.
5. Identify the smallest safe AppFlow path for the prompt.
6. Write the structured brief to `.codex/state/current-intent.md` when files will change.
7. Initialize or update AppFlow state when lifecycle evidence is required.
8. Continue to step `01-read-intent` so current-turn intent can be reconciled with project intent and repository state.

## Guardrails

- Do not silently rewrite the user's prompt into a different objective.
- Do not edit `intent/product-intent.md` or `intent/feedback-intent.md` unless explicitly requested.
- Do not skip step `01`; current-turn intent still needs to be reconciled with existing project artifacts.
- Do not start implementation from this step.

## Exit Criteria

- Current-turn intent is explicit and reviewable.
- The next step has a clear intent brief to read.
- Ambiguities and boundaries are visible before planning begins.
