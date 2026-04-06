# Deviations Log

## Purpose
Capture deviations from intended design, scope, workflow, or validation expectations.

## Intent linkage
- Use this log to capture mismatches between intent, design, and implementation.
- If implementation deviates from intent, do not silently normalize it; log it here.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Deviation: `[what drifted]`
- Impact area: `[design / implementation / test / eval / workflow / schedule]`
- Classification: `[design defect / implementation defect / test defect / eval gap / environment issue / backlog enhancement]`
- Resolution: `[fixed, accepted temporarily, moved to backlog, blocked]`
- Linked IDs: `[REQ-xxx, ACC-xxx, TEST-xxx, EVAL-xxx, FB-xxx]`
- Intent sources: `[INT-PROD-xxx, INT-FB-xxx, INT-CON-xxx, INT-ITER-xxx]`
- Status: `open / resolved`

## Entries
- `DEV-002` | `2026-04-06` | Early template guidance used inconsistent operational IDs such as `ISS-*` and `Q-*`, which weakened traceability across logs and questions. | `workflow` | `design defect` | Fixed by standardizing operational tracking on `DEV-*`. | `REQ-004`, `DEV-001` | `resolved`
- `DEV-013` | `2026-04-06` | The design layer was still framed as a generic copied-project template even though the current intent describes KMS-specific maintenance, wiki publication, and browse behavior. | `design` | `design defect` | Resolved by rewriting the design artifacts, version briefs, and application docs around KMS governance and read-only consumption. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004` | `resolved`
