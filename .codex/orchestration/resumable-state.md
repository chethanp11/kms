# Resumable State Protocol

Use `.codex/state/` only for active, lightweight task checkpoints that help another Codex session resume safely.

## AppFlow Usage

- Use `appflow_run.py preflight` before starting or resuming substantial app-mode work.
- Use `appflow_run.py status` to inspect incomplete steps, validation state, and stale intake warnings.
- Keep resumable notes aligned to the current AppFlow step and remove or supersede them after closeout.

## Checkpoint Template

```md
# Task Checkpoint

- Objective:
- Current AppFlow step:
- Files inspected:
- Files changed:
- Validation run:
- Known failures:
- Next safe step:
- Stop conditions:
```

## Rules

- Do not store secrets.
- Do not use state files as permanent logs.
- Move final outcomes into `dev_log/*` when the workflow closes.
- Delete or supersede stale state notes when they are no longer useful.
