# Implementation Review Validation Loop

## Purpose
Provide a repeatable loop for autonomous-but-governed execution inside AppFlow steps `02` through `10`.

## When to Use

- Use for multi-artifact changes that need implementation plus review and validation.
- Do not use to bypass the required AppFlow lifecycle; it operates inside the selected step boundaries.

## Loop
1. **Plan**: define scope, files, risks, and proof.
2. **Implement**: make minimal patch-safe changes.
3. **Self-review**: inspect diff for scope, contracts, and unintended impacts.
4. **Validate**: run targeted checks.
5. **Repair**: if validation fails, classify root cause and fix the correct layer.
6. **Record**: update factual logs when the workflow requires it.
7. **Close**: summarize status, risks, and remaining work.

## State Handoff

- Record AppFlow step evidence with `appflow_run.py mark`.
- Run `appflow_run.py status` before resuming after interruption.
- Use `.codex/state/` checkpoint notes only for temporary resumable context.

## Exit Criteria
- changed files are intentional
- validation evidence exists or deferral is explicit
- risks and follow-up are visible
- no hidden next scope is started
