# Decision Log

## Purpose
Record material decisions and tradeoffs that change design, validation, or workflow direction.

## Intent linkage
- Record how intent was interpreted when the translation into design was not obvious.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Decision: `[what was decided]`
- Context: `[why it was needed]`
- Alternatives considered: `[other viable choices]`
- Linked IDs: `[REQ-xxx, ARCH-xxx, AI-xxx, TEST-xxx, EVAL-xxx]`
- Intent sources: `[INT-PROD-xxx, INT-FB-xxx, INT-CON-xxx, INT-ITER-xxx]`

## Entries
- `DEV-004` | `2026-04-06` | Added `dev_log/validation-log.md` as a first-class artifact in the template. | Validation evidence was implied by workflow prompts but had no durable home. | Reusing `iteration-log.md` or `release-notes.md` would have mixed planning with evidence. | `REQ-004`, `EVAL-005` | `[intent not yet formalized at that stage]`
- `DEV-008` | `2026-04-06` | Established `intent/*` as the highest-precedence human input and treated downstream folders as system-managed outputs of the workflow. | The template needed a clearer separation between what humans express and what Codex operationalizes. | Keeping humans editing both intent and design directly would have preserved ambiguity and drift. | `REQ-001`, `ARCH-001`, `AI-001` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`, `INT-FB-*`
- `DEV-016` | `2026-04-06` | Modeled KMS as three distinct layers: KMI for governed maintenance, `/wiki` for finalized knowledge, and Infopedia for read-only navigation. | The product intent explicitly separates maintenance from consumption, and the design needed to preserve that boundary. | A single blended interface or direct wiki editing path would have weakened governance and made consumer writes too easy. | `REQ-001`, `REQ-002`, `REQ-003`, `ARCH-001`, `ARCH-003`, `ARCH-004`, `ARCH-005` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`
- `DEV-022` | `2026-04-06` | Tightened the `00-design-update` prompt contract so the workflow explicitly preserves detail, records open questions, and preserves traceability during intent-to-design translation. | The old prompt described the steps, but it did not explicitly guard against losing distinctions when intent was converted into design. | A lighter rewrite, or relying on the workflow operator to remember the nuance, would have left the same failure mode in place. | `REQ-001`, `REQ-002`, `ARCH-001`, `AI-001`, `TEST-001`, `EVAL-001` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`
- `DEV-027` | `2026-04-06` | Treated placeholder-only `intent/iteration-intent.md` as a hard blocker for exact iteration scoping instead of inventing a next work package. | The iteration-scope workflow requires concrete human direction to set a safe scope boundary. | Guessing a scope would hide the missing intent and could create false readiness for implementation. | `REQ-001`, `REQ-004`, `DEV-025` | `INT-ITER-*`
