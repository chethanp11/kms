# Feedback Triage Skill

## Purpose
Capture manual feedback and route it to the right artifact without flattening everything into a bug.

## When to use
- When receiving stakeholder, reviewer, or user feedback.
- When feedback affects scope, behavior, or quality.
- When manual review uncovers issues that automated checks missed.

## Read
- `intent/feedback-intent.md`
- `intent/iteration-intent.md`
- `dev_log/feedback-log.md`
- `dev_log/deviations-log.md`
- `design/open-questions.md`
- `dev_log/issue-log.md`
- `dev_log/backlog.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md` when feedback changes app description or behavior

## Do
1. Review the human feedback in `intent/feedback-intent.md` and any operational feedback already logged.
2. Confirm the affected area: intent, design, implementation, tests, eval, or backlog.
3. Classify severity, action target, and whether it blocks the current iteration.
4. Route feedback to the appropriate artifact or ticket.
5. If feedback changes application description or functionality, flag the corresponding `src/docs/` update.

## Outputs
- Updated `dev_log/feedback-log.md` with structured entries.
- A list of follow-up actions in `dev_log/backlog.md`.
- A classification summary for the current iteration.

## Rules and cautions
- Do not ignore feedback that is actionable.
- Do not treat all feedback as implementation bugs; preserve design intent.
- Do not consume human feedback operationally without preserving the link back to `intent/feedback-intent.md`.
- Do not escalate without first verifying the impact and scope.
