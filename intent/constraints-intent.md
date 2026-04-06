# Constraints Intent

## Purpose
This is the human-edited source for non-functional expectations and delivery constraints that the system must respect.

## Human-editable rule
- This file is intended for direct human editing.
- Codex should treat it as the source for design constraints, validation thresholds, and tradeoff decisions.
- Codex must not modify it unless explicitly asked.

## Non-functional requirements
| Intent Section | Constraint type | Expectation | Priority | Notes |
| --- | --- | --- | --- | --- |
| `INT-CON-001` | `performance` | `[latency or throughput expectation]` | `[high / medium / low]` | `[notes]` |
| `INT-CON-002` | `security` | `[security or privacy expectation]` | `[high / medium / low]` | `[notes]` |
| `INT-CON-003` | `cost` | `[budget or efficiency expectation]` | `[high / medium / low]` | `[notes]` |
| `INT-CON-004` | `operability` | `[observability, auditability, or support expectation]` | `[high / medium / low]` | `[notes]` |

## Tech stack preferences
- Preferred languages or frameworks: `[if any]`
- Preferred model providers or runtime constraints: `[if any]`
- Disallowed technologies: `[if any]`

## Risk boundaries
- Sensitive data considerations: `[PII, secrets, regulated data, none]`
- Reliability floor: `[what failure level is unacceptable]`
- Cost or latency ceiling: `[what is too expensive or too slow]`

## Notes for Codex
- Convert these constraints into `ARCH-*`, `AI-*`, `TEST-*`, and `EVAL-*` artifacts.
- If implementation or validation cannot satisfy these constraints, log the mismatch explicitly.
