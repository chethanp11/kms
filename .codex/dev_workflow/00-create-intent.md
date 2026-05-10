# Step 00 Prompt: Create Intent

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts.

## Use This Prompt When

Use this prompt at the start of every AppFlow turn. This step converts the user's raw prompt into a structured intent brief before repository context is interpreted.

## Workflow Position

- Input step: user prompt
- Output step: structured current-turn intent brief and prompt intake artifact for step `01`

## Objective

Capture what the user asked for, what must change, and what must not be assumed so the rest of AppFlow starts from explicit intent instead of chat memory. Also classify the prompt into the correct transient intake file so downstream workflow steps consume prompt intent, human feedback, and prior gaps through artifacts instead of chat state.

## Required Read Order

Read these in order:

1. The current user prompt
2. selected `.devmode/*` entry point
3. `.codex/project-context.md`
4. `.codex/tech-stack.md` when stack or validation may matter

## Allowed Writes

- `.codex/state/current-intent.md`
- `intent/product-intent.md` for product, design, test, code, documentation, or behavior-change prompts
- `intent/feedback-intent.md` for manual feedback, review observations, complaints, corrections, or user-reported issues
- `.codex/state/appflow-current.json` through `.codex/tools/appflow_run.py` for substantial file-changing app-mode work

Do not write both `intent/product-intent.md` and `intent/feedback-intent.md` for the same prompt unless the user explicitly provides both a change request and separate feedback. Do not edit `intent/gaps.md` in this step.

## Required Outputs

Create a current-turn intent brief that states:

- selected intake channel: `product-intent` or `feedback-intent`
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
2. Classify the prompt:
   - write `intent/product-intent.md` when the prompt asks to create, change, design, test, implement, document, or validate product behavior
   - write `intent/feedback-intent.md` when the prompt reports feedback, a review observation, confusion, dissatisfaction, a correction, or an issue to triage
3. Preserve user wording where it affects scope, constraints, or priority.
4. Separate explicit requirements from inferred implementation ideas.
5. Identify whether the work affects workflow, product behavior, tests, runtime code, docs, or validation.
6. Identify the smallest safe AppFlow path for the prompt.
7. Write the structured brief to `.codex/state/current-intent.md` when files will change.
8. Write the selected intake file using a transient current-cycle format with summary, explicit requirements or observations, constraints, affected areas, and validation expectations.
9. For substantial file-changing work, initialize or update AppFlow state with `.codex/tools/appflow_run.py` and mark step `00-create-intent` with evidence.
10. Continue to step `01-read-intent` so current-turn intent, selected intake, and existing gaps can be reconciled with project context and repository state.

## Guardrails

- Do not silently rewrite the user's prompt into a different objective.
- Do not leave prompt intent only in chat; write the selected intake artifact when files will change.
- Do not edit `intent/gaps.md`; old gaps are consumed later and new gaps are produced only at step `09`.
- Do not skip step `01`; current-turn intent still needs to be reconciled with existing project artifacts.
- Do not start implementation from this step.

## Exit Criteria

- Current-turn intent is explicit and reviewable.
- Exactly one selected prompt intake artifact is populated unless the user explicitly supplied both product intent and feedback.
- The next step has a clear intent brief plus intake artifacts to read.
- Ambiguities and boundaries are visible before planning begins.
