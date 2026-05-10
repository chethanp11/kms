# AppFlow Framework

AppFlow is a portable AI-native engineering framework for turning ordinary development prompts into governed repository changes.

Instead of treating a prompt as a one-off instruction, AppFlow routes it through a repeatable lifecycle:

`user prompt → current-turn intent → plan → design/contracts → validation plan → implementation → validation run → repair → evidence/logs → gaps → closeout`

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

## Default Prompt Behavior

Every development prompt is treated as an AppFlow trigger by default.

For example, a prompt like:

```text
Improve the dashboard UI
```

should automatically enter `.codex/dev_workflow/00-create-intent.md` without requiring the user to say "run AppFlow."

The agent should:

1. read the factory and project contracts
2. create current-turn intent from the raw user prompt
3. classify the request
4. execute the 11-step lifecycle as far as safely possible
5. validate the result
6. close out with evidence, risks, and follow-up

If the user explicitly asks for answer-only, planning-only, or no file changes, AppFlow still guides reasoning but stops at that requested boundary.

## Core Files

| Path | Purpose |
| --- | --- |
| `.devmode/app.md` | Portable AppFlow operating, lifecycle, and routing contract |
| `.codex/dev_workflow/` | Canonical 11-step workflow prompts |
| `.codex/agents/` | Bounded agent role contracts |
| `.codex/skills/` | Reusable specialized procedures |
| `.codex/orchestration/` | Long-horizon execution, task patterns, and HITL checkpoints |
| `.codex/rules/` | Reusable validation, execution, security, and observability rules |
| `.codex/tools/` | Deterministic helper scripts |
| `.codex/state/` | Temporary run state and closeout evidence |
| `.codex/context/` | Context-engineering templates |
| `.codex/memory/` | Reviewable repository memory |
| `.codex/prompts/` | Small reusable prompt templates |

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
python .codex/tools/appflow_run.py init --objective "..."
python .codex/tools/appflow_run.py validate --require-complete
```

## Validation

Validate the AppFlow factory with:

```bash
python .codex/tools/validate_codex_contract.py
git diff --check
```

Project behavior changes should additionally run the project-specific commands from `.codex/tech-stack.md` and the project validation plan.

## Deployment Boundary

`.codex/` is engineering control-plane infrastructure. It supports development, validation, governance, and agent orchestration.

It is not production runtime code. In the default AppFlow scaffold, only the project runtime tree, usually `src/`, should be considered deployable.
