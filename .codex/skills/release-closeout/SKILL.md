---
name: release-closeout
description: Close out an application iteration by checking scope completion, validation evidence, open risks, log readiness, and the next starting point. Use when an iteration reaches completion criteria or before stakeholder/release handoff.
---

# Release Closeout

## Purpose
Capture final iteration status, release readiness, and the next starting point.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `.codex/state/current-intent.md`
- Optional project-owned intent, feedback, or gap artifacts when `.codex/project-context.md` says they are active
- `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`
- `design/*` and `tests/*` summaries
- Relevant `src/` files
- `dev_log/design-update-log.md`, `dev_log/code-update-log.md`, `dev_log/test-update-log.md`, and `dev_log/validation-results.md`

## Do
1. Confirm scoped plan items are complete, deferred, or explicitly blocked.
2. Verify validation evidence exists for completed work.
3. Review unresolved defects, feedback, gaps, and risks.
4. Identify what should be carried into the next iteration.
5. Record factual closeout information only in allowed `dev_log/*` files when asked to update logs.

## Outputs
- Release or iteration closeout summary.
- Open risks and next-step list.
- Log update recommendations or completed updates in the four canonical `dev_log/*` files.

## Rules
- Do not sign off without validation evidence.
- Do not hide unresolved issues.
- Do not create non-canonical `dev_log/*` files unless the repo contract changes first.
- Do not change scope during closeout except by formal follow-up planning.
