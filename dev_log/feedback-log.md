# Feedback Log

## Purpose
Capture structured human feedback and route it into design, implementation, tests, evals, or backlog without losing context.

## Relationship to intent
- `intent/feedback-intent.md` is the human-owned upstream record.
- This file is the system-managed operational routing layer for that feedback.
- When feedback should influence future direction, record that here and point back to `intent/feedback-intent.md`.

## Entry template
- Feedback ID: `FB-001`
- Source: `[stakeholder / reviewer / operator / user / internal]`
- Date: `[YYYY-MM-DD]`
- Affected area: `[design / implementation / test / eval / workflow]`
- Severity: `[high / medium / low]`
- Classification: `[design defect / implementation defect / test defect / eval gap / environment issue / backlog enhancement]`
- Action target: `[design / code / test / eval / backlog]`
- Linked IDs: `[REQ-xxx, ACC-xxx, AI-xxx, TEST-xxx, EVAL-xxx, DEV-xxx]`
- Intent source: `[INT-FB-xxx]`
- Status: `[open / in progress / resolved]`
- Notes: `[what was observed, why it matters, and next step]`

## Entries
- `FB-001` | `reviewer` | `2026-04-06` | `workflow` | `medium` | `design defect` | `design` | `REQ-004`, `EVAL-005`, `DEV-003` | `[intent feedback not yet formalized at that stage]` | `resolved` | Review noted that manual feedback and validation evidence were not strongly connected in the baseline template; guidance and logs were updated together.
