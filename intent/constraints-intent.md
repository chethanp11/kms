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
| `INT-CON-001` | `performance` | Maintenance runs may be async, but KMI review actions and Infopedia browse/search should remain responsive enough for interactive use. | `high` | Favor bounded run times and predictable navigation over broad background analysis. |
| `INT-CON-002` | `security` | Finalized knowledge must not be editable through consumer surfaces, and secrets or private credentials must never be exposed in prompts, logs, or published markdown. | `high` | Preserve the boundary between immutable source inputs, governed publication, and read-only consumption. |
| `INT-CON-003` | `cost` | Source analysis and proposal generation should stay bounded to the current source bundle and current wiki context, without open-ended autonomous exploration. | `medium` | Prefer local and targeted analysis over large-scale or repeated unbounded model calls. |
| `INT-CON-004` | `operability` | Every maintenance run, review decision, and publication outcome must be traceable through logs, validation evidence, and source references. | `high` | Auditability is required so Knowledge Managers can explain what changed and why. |

## Tech stack preferences
- Preferred languages or frameworks: keep the stack unspecified until implementation scope is chosen.
- Preferred model providers or runtime constraints: use a grounded LLM workflow with explicit source trace and bounded tool use.
- Disallowed technologies: consumer-side write paths for finalized knowledge, uncontrolled autonomous publication, and hidden prompt-only business rules.

## Risk boundaries
- Sensitive data considerations: source files may contain private business knowledge; secrets must not be surfaced in outputs or logs.
- Reliability floor: it is unacceptable for consumer browsing to mutate truth or for publication to occur without a governed review path.
- Cost or latency ceiling: interactive KMI and browse actions should not feel sluggish; maintenance runs should remain bounded to the current source bundle and wiki snapshot.

## Notes for Codex
- Convert these constraints into `ARCH-*`, `AI-*`, `TEST-*`, and `EVAL-*` artifacts.
- If implementation or validation cannot satisfy these constraints, log the mismatch explicitly.
