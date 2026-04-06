# Issue Log

## Purpose
Track defects, blockers, and gaps discovered during implementation, testing, evaluation, or review.

## Intent linkage
- Note when an issue is really an intent interpretation problem rather than a pure implementation defect.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Summary: `[what failed or what is blocked]`
- Classification: `[design defect / implementation defect / test defect / eval gap / environment issue / backlog enhancement]`
- Severity: `critical / major / minor`
- Status: `open / in progress / resolved`
- Source: `[implementation, test run, eval run, feedback review, design audit]`
- Linked artifacts: `[REQ-xxx, ACC-xxx, TEST-xxx, EVAL-xxx, FB-xxx]`
- Intent sources: `[INT-PROD-xxx, INT-FB-xxx, INT-CON-xxx, INT-ITER-xxx]`

## Entries
- `DEV-003` | `2026-04-06` | Template lacked a dedicated validation evidence record, making the closed loop harder to audit. | `design defect` | `major` | `resolved` | `design audit` | `REQ-004`, `EVAL-005`
- `DEV-020` | `2026-04-06` | The KMS design baseline still depends on unresolved implementation-surface and source-convention questions for the first KMI release. | `design defect` | `major` | `open` | `design audit` | `REQ-001`, `API-001`, `DATA-001`, `TEST-001`, `EVAL-001`, `DEV-011`, `DEV-012`
- `DEV-025` | `2026-04-06` | The next iteration cannot be scoped exactly because `intent/iteration-intent.md` still contains placeholders instead of concrete direction. | `design defect` | `major` | `open` | `design audit` | `REQ-001`, `ACC-001`, `TEST-001`, `EVAL-001`, `DEV-021`
- `DEV-028` | `2026-04-06` | Implementation could not begin because the iteration scope remains undefined while `intent/iteration-intent.md` still contains placeholders. | `design defect` | `major` | `open` | `implementation planning` | `REQ-001`, `ACC-001`, `TEST-001`, `EVAL-001`, `DEV-025`
