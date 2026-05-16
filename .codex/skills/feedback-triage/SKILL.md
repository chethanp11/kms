---
name: feedback-triage
description: Triage stakeholder, reviewer, or user feedback into design, implementation, tests, evaluation, environment, or backlog updates.
---

# Feedback Triage

## Purpose
Capture manual feedback and route it to the right artifact without flattening every finding into a bug.

## Read
- `.codex/project-context.md`
- relevant `design/*`, `tests/*`, and `src/` files
- any feedback artifact the repository uses

## Do
1. Compare the feedback to project context and current repository state.
2. Identify the affected layer: design, implementation, tests, evaluation, environment, or backlog.
3. Classify each item using the repository's allowed issue classifications.
4. Decide whether it blocks the current work or should become follow-up work.
5. Recommend updates to the relevant artifact only when the user asked for updates.

## Outputs
- Feedback classification summary.
- Blocking vs non-blocking follow-up list.
- Artifact update recommendations with traceability back to the feedback source.

## Rules
- Do not ignore actionable feedback.
- Do not treat design defects, test defects, eval gaps, or environment issues as implementation bugs.
- Do not edit project-owned requirements artifacts unless the user explicitly asks.
