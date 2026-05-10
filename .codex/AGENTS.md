# CHECK MODE

FIRST:
Check `.foundation/mode.yaml`

If:

```yaml
mode: framework
```

then enter FRAMEWORK MODE.

---

# FRAMEWORK MODE RULES

In framework mode:

- Treat the current user prompt as the primary source of truth.
- Prioritize direct framework evolution over workflow execution.
- Do NOT trigger AppFlow application lifecycle workflows.
- Do NOT execute implementation-review-validation orchestration automatically.
- Do NOT simulate application delivery workflows.
- Do NOT assume application context unless explicitly provided.
- Do NOT recursively apply AppFlow to evolve AppFlow itself.
- Do NOT force staged workflow execution unless explicitly requested.

Focus on:
- framework structure
- workflow design
- orchestration design
- prompt systems
- execution models
- contracts
- governance patterns
- reusable engineering systems
- repository organization
- AI-native development patterns

---

# EXECUTION BEHAVIOR

In framework mode:

- Prefer conceptual clarity over premature implementation.
- Prefer lightweight scaffolding over excessive generation.
- Prefer framework evolution over feature implementation.
- Challenge weak abstractions and unnecessary complexity.
- Improve framework consistency and scalability.
- Keep framework boundaries clean and explicit.

---

# CONTEXT BEHAVIOR

In framework mode:

- Do NOT automatically consume downstream workflow state.
- Do NOT continue prior application execution flows unless explicitly instructed.
- Ignore application lifecycle orchestration unless the prompt explicitly invokes it.
- Avoid hidden execution assumptions.
- Minimize recursive workflow behavior.

The current user prompt should drive execution priority.

---

# OUTPUT EXPECTATIONS

Framework mode outputs may include:
- framework updates
- orchestration improvements
- execution model changes
- workflow structures
- prompt systems
- architecture guidance
- governance structures
- repository patterns
- engineering operating models

Framework mode is META-ENGINEERING mode, not application delivery mode. Below is not applicable for framework mode.

# CHECK MODE

FIRST:
Check `.foundation/mode.yaml`

If:

```yaml
mode: app
```

then enter APP MODE.

---

# APP MODE RULES

# AppFlow Factory Operating Contract

This file is the portable, project-agnostic contract for Codex CLI, VS Code Codex, Codex Desktop, and other AI-assisted application-development work.

Copying `.codex/` into a new repository should provide an elite workflow foundation. For a new application, update only:

1. root `AGENTS.md` for project-specific rules and architecture boundaries
2. `.codex/project-context.md` for project-specific context
3. `.codex/tech-stack.md` for project-specific stack and validation commands

Everything else in `.codex/` should remain reusable unless the factory itself is being improved.

## Core Operating Model

AppFlow converts every prompt into a governed engineering workflow:

1. create current-turn intent from the user prompt
2. reconcile intent with repository context
3. plan before editing
4. update design/contracts before implementation when behavior changes
5. define validation before or alongside implementation
6. implement in small reversible steps
7. validate deterministically where possible
8. repair failures at the correct layer
9. record evidence and residual gaps
10. detect follow-up gaps
11. stop at scoped completion

## Default Prompt Handling

Every user prompt in Codex CLI, VS Code Codex, or Codex Desktop is an AppFlow trigger by default.

When a user says something like "Improve the UI", "Fix this bug", "Refactor this module", or "Add a feature", the agent must automatically:

1. classify the request
2. start at `.codex/dev_workflow/00-create-intent.md` and use `.codex/orchestration/*` only when long-horizon coordination is needed
3. run the full 11-step AppFlow loop as far as the task can safely proceed
4. ask the user only for genuinely blocking ambiguity, approval, or HITL decisions
5. validate and close out without requiring the user to manually name or run workflow files

If the user explicitly asks for an answer-only response, planning-only response, or no file changes, do not force implementation steps; still apply AppFlow reasoning and stop at the requested boundary.

## Always-Update Contract

When a user prompt changes workflow, precedence, ownership, or operating rules:

1. update root `AGENTS.md` and `.codex/project-context.md` first when the change is project-specific
2. update `.codex/AGENTS.md` first when the change is reusable AppFlow factory behavior
3. propagate resulting rule changes into design, validation, logs, workflow files, or project docs only as needed
4. keep durable policy in the relevant `AGENTS.md` file and current high-level project design in `.codex/project-context.md`

Always reread `.codex/AGENTS.md`, root `AGENTS.md`, `.codex/project-context.md`, and `.codex/tech-stack.md` at the start of substantial work.

## Source-of-Truth Pattern

Use the project-specific root `AGENTS.md` and `.codex/project-context.md` to adapt this generic order:

1. user prompt and current-turn intent
2. human intent and feedback
3. active plan
4. project context
5. architecture/design/contracts
6. validation plan/tests/evals
7. implementation
8. logs/evidence/gaps

Do not let generated code, chat memory, or hidden assumptions outrank explicit repository artifacts.

## Artifact-Driven Workflow Rules

- The user prompt is first converted into current-turn intent.
- Human intent and feedback are reconciled before planning.
- Plans translate intent into scoped work before implementation.
- Design and contracts define behavior before code where behavior changes.
- Validation expectations must be explicit before closeout.
- Evidence/logs record actual outcomes only after work and validation happen.
- Gaps are evidence-backed follow-up work, not hidden assumptions.

Do not code directly from vague intent. Structure it into plan, design, validation, and implementation steps first.

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

## Project-Specific Extension Points

- Root `AGENTS.md`: project identity, architecture boundaries, domain rules, source-of-truth paths, validation commands, and special constraints.
- `.codex/project-context.md`: compact project map and current design summary.
- `.codex/tech-stack.md`: technology stack, dependency boundaries, tool commands, and runtime conventions.

## Deployment Boundary

Only the project implementation/runtime tree should be deployable to production. In the default AppFlow scaffold this is `src/`.

All `.codex/`, planning, design, validation, log, and workflow artifacts are engineering control-plane assets. They support development and governance; they are not production runtime artifacts unless a project explicitly says otherwise.

## Copy/Drop Bootstrap Behavior

When `.codex/` is copied into a new repository:

1. Check whether root `AGENTS.md`, `.codex/project-context.md`, and `.codex/tech-stack.md` exist and describe the new application.
2. If any are missing, offer to create starter placeholders with `.codex/tools/bootstrap_appflow.py`.
3. If the project has no planning, design, validation, or evidence folders, offer to scaffold the generic AppFlow artifact chain.
4. Do not force a project to use a specific framework or runtime stack.
5. Keep all reusable `.codex` files project-agnostic after bootstrap.

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
4. Do not introduce project-specific examples into reusable factory files.
5. Do not let implementation behavior become the de facto design source.

## Validation Rules

Every non-trivial change must end with explicit validation:

- docs/factory changes: static checks and `git diff --check`
- design changes: review against intent, project context, architecture, and correctness criteria
- code changes: targeted tests first, broader tests only after local success
- eval/AI changes: grounding, prompt-boundary, tool-policy, and hallucination-risk review

Validation evidence should state method, result (`pass`, `fail`, or `partial`), findings, failure classification, and follow-up.

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

Use repository-visible artifacts over hidden runtime memory. If a convention becomes durable, promote it to root `AGENTS.md`, `.codex/project-context.md`, `.codex/tech-stack.md`, design docs, tests, or logs as appropriate.

## Behavior Expectations

- Be precise, not verbose.
- Challenge weak or incomplete design.
- Do not skip gates in the loop.
- Do not generate large code blindly.
- Prefer structured progress over speed.
- Surface assumptions explicitly.
- Maintain engineering discipline at all times.
