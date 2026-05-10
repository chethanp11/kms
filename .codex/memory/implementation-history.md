# Implementation History

Concise project milestones. Permanent evidence remains in `dev_log/*`.

## Milestone: portable AppFlow factory scaffold

- Date: 2026-05-10
- Scope: Added `.devmode/app.md`, agent roles, skills, workflows, orchestration, memory templates, state, and tools.
- Files/modules: `AGENTS.md`, `.devmode/*`, `.codex/*`, project context, tech stack, plan/log artifacts.
- Outcome: `AGENTS.md` is a router; `.devmode/*` and reusable `.codex/*` are project-agnostic; `.codex/project-context.md` and `.codex/tech-stack.md` hold project-specific information.
- Validation: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.
- Follow-up: Keep reusable framework files project-agnostic.

## Milestone: canonical workflow moved into `.codex`

- Date: 2026-05-10
- Scope: Moved canonical 11-step workflow from root `dev_workflow/` to `.codex/dev_workflow/`.
- Files/modules: `.codex/dev_workflow/*`, `.devmode/app.md`, root `AGENTS.md` router, `README.md`.
- Outcome: AppFlow lifecycle prompts are control-plane infrastructure under `.codex`.
- Validation: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.
- Follow-up: Use `.codex/tools/appflow_run.py` for lifecycle evidence on substantial turns.

## Milestone: support folders streamlined

- Date: 2026-05-10
- Scope: Removed unused `.codex/prompts/` and `.codex/context/`; folded duplicate `.codex/rules/` guidance into `.devmode/app.md`, workflow docs, and project files.
- Outcome: Remaining `.codex` folders are directly referenced by workflow, agents, skills, tools, state, orchestration, or memory.
- Validation: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.

## Rule

This is a navigation aid, not the authoritative changelog.
