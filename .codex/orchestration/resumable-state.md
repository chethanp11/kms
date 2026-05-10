# Resumable State Protocol

Use `.codex/state/` only for active, lightweight task checkpoints that help another Codex session resume safely.

## Checkpoint Template

```md
# Task Checkpoint

- Objective:
- Current phase:
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
