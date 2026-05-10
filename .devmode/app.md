# App Mode

App mode uses AppFlow to create or change an application.

## Activation

Root `AGENTS.md` routes to this file after reading `.devmode/mode.yaml`. When it contains:

```yaml
mode: app
```

use this file as the active operating entry point.

## AppFlow Purpose

AppFlow is a portable, prompt-driven application-development workflow. It turns human intent into governed repository changes by moving work through explicit artifacts instead of relying on chat memory or ad hoc edits.

AppFlow exists to:

- convert every application-development prompt into a structured engineering workflow
- keep development aligned to intent, plan, project context, design, validation, implementation, and evidence
- make work reproducible across Codex CLI, VS Code Codex, Codex Desktop, and future agents
- support long-horizon application development without uncontrolled autonomy

## Project-Specific Files

For a new application, only these files should need project-specific updates:

1. `.codex/project-context.md` for product identity, domain rules, architecture boundaries, source-of-truth order, repository shape, and project-specific operating instructions.
2. `.codex/tech-stack.md` for implementation stack, runtime layout, commands, dependencies, storage choices, and validation commands.

Root `AGENTS.md`, `.devmode/app.md`, `.devmode/framework.md`, and reusable `.codex/*` workflow files should remain project-agnostic unless the AppFlow framework itself is being improved.

## Prompt Handling

Treat each user prompt as application intent. Convert the prompt into current-turn intent, then route work through the AppFlow lifecycle.

Every ordinary development prompt is an AppFlow trigger by default. The user should not need to say "run the workflow."

When a user says something like "Improve the UI", "Fix this bug", "Refactor this module", or "Add a feature", the agent must automatically:

1. classify the request
2. start at `.codex/dev_workflow/00-create-intent.md`
3. use `.codex/orchestration/*` only when long-horizon coordination is needed
4. run the 11-step AppFlow loop as far as the task can safely proceed
5. ask the user only for genuinely blocking ambiguity, approval, or HITL decisions
6. validate and close out without requiring the user to manually name workflow files

If the user explicitly asks for an answer-only response, planning-only response, or no file changes, do not force implementation steps; still apply AppFlow reasoning and stop at the requested boundary.

## AppFlow Lifecycle

1. Create current-turn intent from the user prompt.
2. Read intent, project context, and stack guidance.
3. Create or update a scoped plan.
4. Update architecture, design, or contracts when behavior or structure changes.
5. Update validation expectations.
6. Implement in small, reversible steps.
7. Run targeted validation.
8. Fix failures at the correct layer.
9. Record factual evidence.
10. Surface gaps or follow-up work.
11. Review iteration and stop when scope is complete, blocked, or explicitly bounded by the user.

## Portable Source-of-Truth Pattern

Adapt this generic order through `.codex/project-context.md`:

1. user prompt and current-turn intent
2. human intent and feedback
3. active plan or backlog item
4. project context
5. architecture, design, contracts, and correctness criteria
6. validation plan, tests, evals, and review checklists
7. implementation
8. logs, validation evidence, gaps, and decisions

Do not let generated code, chat memory, or hidden assumptions outrank explicit repository artifacts.

## Artifact-Driven Workflow Rules

- The user prompt is first converted into current-turn intent.
- Human intent and feedback are reconciled before planning.
- Plans translate intent into scoped work before implementation.
- Design and contracts define behavior before code where behavior changes.
- Validation expectations must be explicit before closeout.
- Evidence/logs record actual outcomes only after work and validation happen.
- Gaps are evidence-backed follow-up work, not hidden assumptions.
- Do not code directly from vague intent. Structure it into plan, design, validation, and implementation steps first.

## Prompt Operating Rules

Each AppFlow prompt should:

- state the lifecycle phase
- name required inputs
- define allowed writes
- preserve traceability between intent, design, validation, and implementation
- stop at phase exit criteria
- record real outcomes only after validation or explicit review

## Factory Structure

- `.codex/agents/`: bounded role contracts.
- `.codex/dev_workflow/`: canonical 11-step prompt-to-change AppFlow lifecycle.
- `.codex/skills/`: reusable task procedures.
- `.codex/orchestration/`: staged long-horizon execution and HITL checkpoints.
- `.codex/context/`: project-agnostic context templates and indexing guidance.
- `.codex/memory/`: project-agnostic memory structure and maintenance rules.
- `.codex/rules/`: reusable execution, validation, security, governance, and observability rules.
- `.codex/prompts/`: reusable prompt templates.
- `.codex/tools/`: deterministic validation helpers for the factory.
- `.codex/state/`: temporary resumable task state.

## Project Boundary Rules

Project-specific behavior belongs only in:

- `.codex/project-context.md`: product identity, architecture boundaries, source-of-truth order, repository map, and project-specific workflow instructions
- `.codex/tech-stack.md`: stack, runtime layout, dependencies, storage, commands, and validation instructions
- project artifacts such as `intent/`, `plan/`, `design/`, `tests/`, implementation source, and logs

Reusable framework files must not encode a specific application's domain, users, architecture, or stack unless the task is explicitly about making a generic framework capability.

## Copy/Drop Bootstrap Behavior

When AppFlow is copied into a new repository:

1. check whether `AGENTS.md`, `.devmode/mode.yaml`, `.devmode/app.md`, `.devmode/framework.md`, `.codex/project-context.md`, and `.codex/tech-stack.md` exist
2. rewrite only `.codex/project-context.md` and `.codex/tech-stack.md` for the new application unless changing the framework itself
3. if required files are missing, offer to create starter placeholders with `.codex/tools/bootstrap_appflow.py`
4. if the project has no planning, design, validation, or evidence folders, offer to scaffold the generic AppFlow artifact chain
5. do not force a project to use a specific framework or runtime stack
6. keep reusable `.devmode/*` and `.codex/*` files project-agnostic after bootstrap

## Agent Discipline

Agents are bounded roles, not autonomous authority grants. Every agent must:

- read the relevant project-specific context before acting
- keep scope explicit
- preserve contracts unless asked to change them
- validate changed behavior or state deferral clearly
- record evidence only after work is real

## Boundary Rules

1. If a request is ambiguous about scope, file targets, validation, or ownership, ask before editing unless a safe minimal assumption is clear.
2. Do not edit outside explicit task scope unless the change is a direct dependency and is called out.
3. Prefer the smallest set of files that fully completes the task.
4. Do not introduce project-specific examples into reusable framework files.
5. Do not let implementation behavior become the de facto design source.

## Validation Rules

Every non-trivial change must end with explicit validation:

- docs/factory changes: static checks and `git diff --check`
- design changes: review against intent, project context, architecture, and correctness criteria
- code changes: targeted tests first, broader tests only after local success
- eval/AI changes: grounding, prompt-boundary, tool-policy, and hallucination-risk review

Validation evidence should state method, result (`pass`, `fail`, or `partial`), findings, failure classification, and follow-up.

For factory-only changes:

- confirm required files exist
- confirm reusable files are project-agnostic
- run `python .codex/tools/validate_codex_contract.py`
- run `git diff --check`

For project behavior changes, use the project-specific validation commands in `.codex/tech-stack.md` and the project validation plan.

## Issue Classifications

Use these categories consistently:

- design defect
- implementation defect
- test defect
- eval gap
- environment issue
- backlog enhancement

## Traceability Discipline

- Intent defines what humans want.
- Plan defines active scope.
- Project context defines compact high-level design and operating model.
- Design/contracts define expected behavior and boundaries.
- Tests/evals/checklists define proof.
- Implementation follows approved intent, plan, design, and validation expectations.
- Logs/evidence record what actually happened.

Use only `REQ-*`, `DEV-*`, and `TEST-*` as AppFlow traceability ID prefixes.

## Testing and Review Discipline

For implemented behavior, cover happy paths, edge cases, and failure scenarios where practical.

For every iteration, review:

- requirement coverage
- architecture alignment
- code quality and modularity
- duplication and coupling
- failure handling
- performance risks
- security considerations
- test sufficiency

## Failure Handling

When blocked:

1. state the blocker explicitly
2. classify the root cause
3. propose concrete next steps
4. proceed only as far as safely possible with assumptions visible

If validation fails, fix the correct failing layer rather than hiding the problem with a downstream workaround.

## Workflow Anti-Patterns

- coding directly from the latest prompt without reconciling intent
- using code behavior as the design source
- writing tests only after code exists when behavior changed
- logging planned work as completed work
- editing human-owned intent to resolve ambiguity
- closing an iteration while validation, logs, or review are incomplete

## Definition of Done

A scoped iteration is done only when:

- relevant intent and context were read
- in-scope work is explicit
- implementation matches design and design matches intent
- tests or manual validation are present or explicitly deferred
- validation evidence exists
- residual risks and next actions are clear enough for another agent to continue

## Governance

Use repository-visible artifacts over hidden runtime memory. If a convention becomes durable, promote it to `.codex/project-context.md`, `.codex/tech-stack.md`, design docs, tests, or logs as appropriate.

## Behavior Expectations

- Be precise, not verbose.
- Challenge weak or incomplete design.
- Do not skip gates in the loop.
- Do not generate large code blindly.
- Prefer structured progress over speed.
- Surface assumptions explicitly.
- Maintain engineering discipline at all times.
