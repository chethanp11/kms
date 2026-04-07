# Feedback Intent

## Purpose
This is the human-edited record of manual observations that should influence future design and iteration planning. Use it to capture what felt wrong, confusing, weak, surprising, or promising.

## Human-editable rule
- This file is intended for direct human editing.
- Codex should treat it as upstream input for design revisions, backlog decisions, and next-iteration scope.
- Codex must not modify it unless explicitly asked.

## Feedback entries
| Intent Section | Date | Area | Observation | Why it matters | Suggested direction | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| `INT-FB-001` | `[YYYY-MM-DD]` | `[UX / behavior / accuracy / workflow / other]` | `[what was observed]` | `[impact]` | `[what should likely change]` | `[high / medium / low]` |
| `INT-FB-002` | `[YYYY-MM-DD]` | `[UX / behavior / accuracy / workflow / other]` | `[unexpected output or gap]` | `[impact]` | `[what should likely change]` | `[high / medium / low]` |

## Common feedback types
- Manual testing observations
- UX feedback
- Behavior gaps
- Unexpected or low-trust outputs
- Improvement suggestions

## Notes for Codex
- Route operationally actionable items into `dev_log/feedback-log.md`.
- Reflect approved intent changes into `design/` and `tests/`.
- If feedback conflicts with current design, treat this file as the higher-priority human source for the feedback record.
