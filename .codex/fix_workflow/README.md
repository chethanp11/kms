# Fix Workflow

Fix workflow is a bounded application repair loop used by `.devmode/fix.md`.

It is for testing and repairing existing application behavior only. It must not add new features or modify AppFlow framework/control-plane files.

## Trigger

Use this workflow when the active mode is `fix` and the user prompt is:

```text
fix mode start
```

## Loop

1. Inspect application run instructions, current diff, and available test fixtures.
2. Run the smallest terminal validation or local runtime smoke test.
3. Exercise the application as a human would, using visible/API workflows and configured test inputs.
4. Capture observed errors, regressions, or logical gaps in existing behavior.
5. Make the smallest application-only fix.
6. Re-run the failing check.
7. Repeat until validation is satisfactory or a blocker is explicit.

## Boundaries

Allowed writes are application source, application tests, and application fixtures. Forbidden writes are framework/control-plane paths such as `AGENTS.md`, `.devmode/*`, and reusable `.codex/*` files.

If the root cause is framework drift, stop and request framework or override mode instead of fixing it here.
