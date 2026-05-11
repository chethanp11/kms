# App Mode

App mode uses AppFlow to create or change an application from the user's prompt.

## Activation

Root `AGENTS.md` routes here when `.devmode/mode.yaml` contains:

```yaml
mode: app
```

## Core Rule

The current user prompt is the source of intent for the turn. Do not assume intent is pre-filled in repository files.

Repository artifacts provide context, constraints, design baselines, validation expectations, and evidence; they do not replace the prompt as the current-turn intent source.

## Project-Specific Files

For a new application, only these files should require project-specific edits:

1. `.codex/project-context.md` for product identity, source-of-truth order, architecture boundaries, repository shape, and project-specific operating instructions.
2. `.codex/tech-stack.md` for implementation stack, runtime layout, dependencies, commands, storage choices, and validation commands.

Root `AGENTS.md`, `.devmode/*`, and reusable `.codex/*` files must stay project-agnostic unless the AppFlow framework itself is being improved.


## Files App Mode Must Not Modify

App mode must not modify framework/control-plane files unless the current prompt explicitly changes AppFlow behavior, routing, validators, bootstrap, agents, skills, orchestration, mode behavior, or reusable workflow docs. Forbidden-by-default paths include:

- `AGENTS.md`
- `.devmode/*`
- `.codex/dev_workflow/*`
- `.codex/agents/*`
- `.codex/skills/*`
- `.codex/orchestration/*`
- `.codex/tools/*`
- `.codex/state/*` conventions and schemas, except current-turn run state written by documented tools
- reusable `.codex/README.md` and `.codex/memory/*` framework docs

If app work appears to require these files, stop and ask for an explicit framework or override-mode prompt.

## Strict Mode Boundaries

App mode is application-delivery mode. Do not change AppFlow framework/control-plane behavior unless the current prompt explicitly asks to change workflow, routing, validators, bootstrap, agents, skills, orchestration, or mode behavior.

If an application task exposes framework drift, record or report it and ask before crossing into framework changes.

## Prompt Handling

Every ordinary development prompt is an AppFlow trigger by default. The user should not need to say "run the workflow."

For each app-mode prompt:

1. classify the request
2. create current-turn intent from the prompt
3. reconcile that intent with project context and relevant repository artifacts
4. run the AppFlow lifecycle as far as the task can safely proceed
5. ask only for genuinely blocking ambiguity, approval, or HITL decisions
6. validate and close out with evidence

If the user explicitly asks for answer-only, planning-only, or no file changes, apply AppFlow reasoning and stop at that requested boundary.

## AppFlow Lifecycle

1. Create current-turn intent from the prompt.
2. Read project context, stack guidance, and relevant artifacts.
3. Create or update a scoped plan.
4. Update architecture, design, or contracts when behavior or structure changes.
5. Update validation expectations.
6. Implement in small, reversible steps.
7. Run targeted validation.
8. Fix failures at the correct layer.
9. Record factual evidence.
10. Surface evidence-backed gaps or follow-up work.
11. Review iteration completeness and stop.

## Source-of-Truth Pattern

Adapt this generic order through `.codex/project-context.md`:

1. user prompt and current-turn intent
2. project context and durable project constraints
3. active plan or backlog item
4. architecture, design, contracts, and correctness criteria
5. validation plan, tests, evals, and review checklists
6. implementation
7. logs, validation evidence, gaps, and decisions

Do not let generated code, chat memory, or hidden assumptions outrank explicit repository artifacts.

## Artifact Rules

- Prompt-derived intent is written to `.codex/state/current-intent.md` when files will change.
- At step `00`, also populate exactly one prompt intake file from the raw prompt:
  - `intent/product-intent.md` for product, design, test, code, documentation, or behavior-change prompts.
  - `intent/feedback-intent.md` for manual feedback, review observations, complaints, corrections, or user-reported issues.
- `intent/gaps.md` is system-managed input from the previous cycle. Read it with product intent and feedback intent during reconciliation; do not treat it as human-authored requirements.
- Steps `01` through `08` must progress all three intake channels (`product-intent`, `feedback-intent`, and `gaps`) into the normal plan, design, test, implementation, validation, and log artifacts as applicable.
- Step `09` writes only newly detected evidence-backed gaps for the next cycle.
- Step `10` clears consumed `intent/product-intent.md`, `intent/feedback-intent.md`, and old `intent/gaps.md` content after closeout; keep only the new gaps produced by step `09`.
- Step `02` must update `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md` on every file-changing app-mode cycle before design, tests, code, or logs change. Do not reuse stale plan files from prior cycles.
- Step `03` must update design artifacts when intent changes behavior, architecture, component boundaries, data contracts, UX, validation gates, or scaffold/component structure. If no design change is required, it must explicitly record why in the plan and AppFlow state.
- Plans translate current-turn intent into scoped work before implementation.
- Design and contracts define behavior before code when behavior changes.
- Validation expectations must be explicit before closeout.
- Evidence/logs record actual outcomes only after work and validation happen.
- Gaps are evidence-backed follow-up work, not hidden assumptions.

## State and Tool Use

For substantial app-mode changes that edit files, use `.codex/tools/appflow_run.py` and `.codex/state/appflow-current.json` to record lifecycle evidence:

1. run `python .codex/tools/appflow_run.py init --objective "..."` before or during step `00`
2. mark each lifecycle step as `completed`, `skipped`, or `blocked` with evidence; use canonical step IDs such as `02-create-plan` or numeric aliases such as `02` / `2`
3. record validation commands and results with `python .codex/tools/appflow_run.py validation ...`
4. run `python .codex/tools/appflow_run.py validate --require-complete` before closeout when a full lifecycle was expected

Use `.codex/state/current-intent.md`, `intent/product-intent.md`, and `intent/feedback-intent.md` only for the current prompt-derived cycle. Do not carry them across unrelated turns as pre-filled application intent. Use `python .codex/tools/appflow_run.py closeout-intake` at step `10` when the cycle is complete so consumed prompt intent and feedback are cleared while newly detected gaps remain available for the next cycle.

Use `.codex/tools/validate_codex_contract.py` for framework/control-plane validation and `.codex/tools/bootstrap_appflow.py` only when bootstrapping missing AppFlow files.

## Reusable AppFlow Structure

- `.codex/agents/`: bounded role contracts.
- `.codex/dev_workflow/`: canonical prompt-to-change lifecycle.
- `.codex/skills/`: reusable task procedures.
- `.codex/orchestration/`: staged execution and HITL checkpoints.
- `.codex/memory/`: factual, reviewable workflow memory.
- `.codex/tools/`: deterministic support scripts.
- `.codex/state/`: temporary current-turn state and closeout evidence.

## Boundary Rules

1. Keep project-specific information in `.codex/project-context.md` and `.codex/tech-stack.md`.
2. Keep reusable framework files project-agnostic.
3. Preserve public contracts unless intentionally changed.
4. Prefer the smallest file set that completes the task.
5. Ask before proceeding when ambiguity is blocking and cannot be resolved from repository context.
6. Do not let implementation behavior become the design source.
7. After initial scaffolding exists, do not add new top-level `src/` component families or foundational modules unless the current plan and design prove they are necessary. Prefer extending existing components and ports.

## Validation Rules

Every non-trivial change must end with explicit validation:

- framework/docs changes: `python .codex/tools/validate_codex_contract.py` and `git diff --check`
- design changes: review against current-turn intent, project context, design, and correctness criteria
- code changes: targeted tests first, broader tests after local success
- eval/AI changes: grounding, prompt-boundary, tool-policy, and hallucination-risk review

Validation evidence should state method, result (`pass`, `fail`, or `partial`), findings, failure classification, and follow-up.

## Issue Classifications

Use only these categories:

- design defect
- implementation defect
- test defect
- eval gap
- environment issue
- backlog enhancement

## Definition of Done

A scoped iteration is done only when:

- current-turn intent is explicit
- in-scope work and deferrals are clear
- implementation matches design and design matches intent
- validation evidence exists or deferral is explicit
- residual risks and next actions are visible

## Behavior Expectations

- Be precise, not verbose.
- Inspect before editing.
- Plan before implementation.
- Validate before closeout.
- Record outcomes only after evidence exists.
- Surface uncertainty clearly.
