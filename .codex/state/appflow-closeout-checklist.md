# AppFlow Closeout Checklist

Use `.codex/tools/appflow_run.py` to record and validate lifecycle evidence for any substantial prompt-driven change.

## Required lifecycle evidence

1. `00-create-intent`
2. `01-read-intent`
3. `02-create-plan`
4. `03-update-design`
5. `04-update-tests`
6. `05-implement-code`
7. `06-run-validation`
8. `07-fix-failures`
9. `08-update-logs`
10. `09-detect-gaps`
11. `10-iteration-review`

Each step must be marked `completed`, `skipped`, or `blocked` with evidence before closeout.

## Commands

```bash
python .codex/tools/appflow_run.py init --objective "..."
python .codex/tools/appflow_run.py mark --step 00-create-intent --status completed --evidence "..."
python .codex/tools/appflow_run.py validation --command "..." --result pass
python .codex/tools/appflow_run.py validate --require-complete
```

## Rules

- Use `skipped` only when the user explicitly bounds the task or the step is not applicable.
- Use `blocked` when a HITL decision or external constraint prevents completion.
- Do not use this state file as permanent evidence; summarize final outcomes in project logs.
