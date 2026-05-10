# Workflow Memory

Reusable workflow lessons validated by project artifacts.

## Lesson: every development prompt enters AppFlow by default

- Trigger: Review found that workflow enforcement was mostly procedural.
- Better workflow: Treat each development prompt as an AppFlow trigger, then route through `.codex/dev_workflow/` unless the user explicitly asks for a bounded answer-only or planning-only response.
- Evidence: `.devmode/app.md` `Default Prompt Handling` and `Automatic Routing`, `.codex/dev_workflow/README.md` `Automatic Prompt Routing`.
- Applies to: Codex CLI, VS Code Codex, Codex Desktop, and future agent sessions.
- Should be promoted to: Already promoted to `.devmode/app.md`.

## Lesson: lifecycle evidence needs a state artifact

- Trigger: Review identified that future turns could claim AppFlow without proving which lifecycle steps ran.
- Better workflow: Use `.codex/tools/appflow_run.py` and `.codex/state/appflow-closeout-checklist.md` for per-turn lifecycle evidence.
- Evidence: `appflow_run.py validate --require-complete` checks the 11-step state when a current run state exists.
- Applies to: Substantial prompt-driven changes.
- Should be promoted to: Already promoted to `.codex/tools/README.md` and `.codex/state/appflow-closeout-checklist.md`.

## Template

```md
## Lesson
- Trigger:
- Better workflow:
- Evidence:
- Applies to:
- Should be promoted to:
```

## Reusable Defaults

- Plan before editing.
- Update design before code when behavior changes.
- Validate before closeout.
- Record outcomes only after evidence exists.
