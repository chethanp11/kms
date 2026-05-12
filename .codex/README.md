# AppFlow Framework

AppFlow is a portable AI-native engineering framework for turning ordinary development prompts into governed repository changes.

Instead of treating a prompt as a one-off instruction, AppFlow routes it through a repeatable lifecycle:

`user prompt → preflight → current-turn intent → plan → design/contracts → validation plan → implementation → validation run → repair → evidence/logs → gaps → closeout`

The goal is simple: every meaningful prompt becomes structured engineering work with context, traceability, validation, and a clear stopping point.

## What AppFlow Does

AppFlow helps Codex CLI, VS Code Codex, Codex Desktop, and future agents:

- reason at repository level instead of file level
- convert user prompts into current-turn intent
- inspect context before editing
- plan before implementation
- update design and validation expectations before code when behavior changes
- run targeted validation before closeout
- record evidence instead of relying on chat memory
- keep project-specific rules separate from reusable workflow infrastructure

## Devmode Enforcement

`AGENTS.md` routes every turn through `.devmode/mode.yaml`. AppFlow application workflow is active only in `mode: app`. In `mode: framework`, agents may edit framework/control-plane files but must not repair application code, product design, tests, plans, or logs unless the user explicitly changes mode or asks for app work. In `mode: override`, agents follow the prompt directly and may modify any file without treating AppFlow or framework docs as workflows. In `mode: fix`, agents run the application repair loop for existing behavior and must not modify framework/control-plane files or add new features.

## Default Prompt Behavior

Every development prompt is treated as an AppFlow trigger by default.

For example, a prompt like:

```text
Improve the dashboard UI
```

should automatically enter `.codex/dev_workflow/00-create-intent.md` without requiring the user to say "run AppFlow."

The agent should:

1. read the factory and project contracts
2. run AppFlow preflight to detect stale state or intake
3. create current-turn intent from the raw user prompt
4. classify the request
5. execute the 11-step lifecycle as far as safely possible
6. validate the result
7. close out with evidence, risks, and follow-up

If the user explicitly asks for answer-only, planning-only, or no file changes, AppFlow still guides reasoning but stops at that requested boundary.

## Core Files

| Path | Purpose |
| --- | --- |
| `.devmode/app.md` | Portable AppFlow operating, lifecycle, and routing contract |
| `.devmode/framework.md` | Framework/control-plane operating contract |
| `.devmode/override.md` | Direct prompt-driven override contract |
| `.devmode/fix.md` | Application test-and-repair operating contract |
| `.codex/dev_workflow/` | Canonical 11-step workflow prompts |
| `.codex/fix_workflow/` | Bounded application repair loop for fix mode |
| `.codex/agents/` | Bounded agent role contracts |
| `.codex/skills/` | Reusable specialized procedures |
| `.codex/orchestration/` | Long-horizon execution, task patterns, and HITL checkpoints |
| `.codex/tools/` | Deterministic helper scripts |
| `.codex/state/` | Temporary run state and closeout evidence |
| `.codex/memory/` | Reviewable repository memory |


## Role and Skill Routing

- Use `.codex/agents/` role contracts when a workflow step needs planning, architecture review, implementation, validation, debugging, governance review, documentation, or final review discipline.
- Use `.codex/skills/*/SKILL.md` only when the task matches the skill description; skills are recognized by their standard frontmatter.
- Do not invent ad hoc roles or prompt templates when an existing workflow step, agent role, or skill already covers the need.

## Project-Specific Files

When using AppFlow for a new application, only these files should normally need project-specific edits:

1. `.codex/project-context.md`
2. `.codex/tech-stack.md`

Root `AGENTS.md`, `.devmode/*`, and everything else in `.codex/` should remain reusable unless the AppFlow framework itself is being improved.

## The 11-Step Lifecycle

The canonical workflow lives in `.codex/dev_workflow/`:

1. create intent
2. read intent
3. create plan
4. update design
5. update tests
6. implement code
7. run validation
8. fix failures
9. update logs
10. detect gaps
11. review iteration

Steps may be marked complete, skipped, or blocked with evidence. Substantial work should use:

```bash
python .codex/tools/appflow_run.py preflight
python .codex/tools/appflow_run.py init --objective "..."
python .codex/tools/appflow_run.py mark 02 completed --evidence "Plan files refreshed"
python .codex/tools/appflow_run.py status
python .codex/tools/appflow_run.py validate --require-complete
python .codex/tools/appflow_run.py complete
```

## Validation

Validate the AppFlow factory with:

```bash
python .codex/tools/validate_codex_contract.py
git diff --check
```

Application behavior changes should additionally run the project-specific commands from `.codex/tech-stack.md` and the project validation plan.

## Deployment Boundary

`.codex/` is engineering control-plane infrastructure. It supports development, validation, governance, and agent orchestration.

It is not production runtime code. In the default AppFlow scaffold, only the project runtime tree, usually `src/`, should be considered deployable.

## Reliability Skills

Use these framework-focused skills for AppFlow reliability work:

- `appflow-framework-audit`: audit routing, workflow consistency, bootstrap drift, state conventions, and validator coverage.
- `mode-boundary-review`: review app/framework/override boundary compliance before or after mode-sensitive edits.
- `workflow-drift-repair`: repair stale framework references across mode docs, workflow docs, tools, state docs, bootstrap templates, and validators.
