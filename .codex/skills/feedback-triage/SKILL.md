---
name: feedback-triage
description: Triage application stakeholder, reviewer, or user feedback into intent, plan, design, implementation, tests, evals, or backlog using the repo's allowed issue classifications. Use when manual feedback affects scope, behavior, quality, or release readiness.
---

# Feedback Triage

## Purpose
Capture manual feedback and route it to the right artifact without flattening every finding into a bug.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `.codex/state/current-intent.md`
- Optional project-owned feedback or gap artifacts when `.codex/project-context.md` says they are active
- Relevant `plan/*`, `design/*`, `tests/*`, `src/`, and `dev_log/*` files

## Do
1. Compare the feedback to current-turn intent, project context, and current plan scope.
2. Identify the affected layer: intent, design, implementation, tests, eval, environment, or backlog.
3. Classify each item using exactly the repo's allowed issue classifications.
4. Decide whether it blocks the current iteration or should become follow-up work.
5. Recommend updates to `plan/*`, `design/*`, `tests/*`, or `dev_log/*`; edit only when the user asked for triage plus updates.

## Outputs
- Feedback classification summary.
- Blocking vs non-blocking follow-up list.
- Artifact update recommendations with traceability back to the current prompt or active feedback artifact.

## Rules
- Do not ignore actionable feedback.
- Do not treat design defects, test defects, eval gaps, or environment issues as implementation bugs.
- Do not edit project-owned intent or requirements artifacts unless the user explicitly asks.
