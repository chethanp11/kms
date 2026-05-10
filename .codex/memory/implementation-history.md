# Implementation History

Concise project milestones. Permanent evidence remains in `dev_log/*`.

## Milestone: portable AppFlow factory scaffold

- Date: 2026-05-10
- Scope: Added `.devmode/app.md`, agent roles, skills, workflows, orchestration, context templates, memory templates, rules, prompts, state, and tools.
- Files/modules: `.codex/*`, root `AGENTS.md` router, `README.md`, `plan/*`, `dev_log/validation-results.md`.
- Outcome: `.codex/` became a reusable AppFlow factory; root `AGENTS.md` router, `.codex/project-context.md`, and `.codex/tech-stack.md` remain project-specific.
- Validation: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.
- Follow-up: Keep reusable `.codex` files project-agnostic.

## Milestone: canonical workflow moved into `.codex`

- Date: 2026-05-10
- Scope: Moved canonical 11-step workflow from root `dev_workflow/` to `.codex/dev_workflow/`.
- Files/modules: `.codex/dev_workflow/*`, `.devmode/app.md`, root `AGENTS.md` router, `README.md`.
- Outcome: AppFlow is now control-plane infrastructure under `.codex`; root index folders were removed.
- Validation: `DEV-011` in `dev_log/validation-results.md`.
- Follow-up: Use `.codex/tools/appflow_run.py` for lifecycle evidence on substantial turns.

## Template

```md
## Milestone
- Date:
- Scope:
- Files/modules:
- Outcome:
- Validation:
- Follow-up:
```

## Rule

This is a navigation aid, not the authoritative changelog.
