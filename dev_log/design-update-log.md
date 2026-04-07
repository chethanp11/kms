# Design Update Log

## Purpose
Record meaningful design changes that were actually applied.

## Intent linkage
- Capture when intent was interpreted into downstream design changes.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Change: `[what design changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, ACC-xxx, ARCH-xxx, TEST-xxx, FB-xxx, DEV-xxx]`
- Intent sources: `[INT-PROD-xxx, INT-FB-xxx, intent/gaps.md]`

## Entries
- `DEV-001` | `2026-04-07` | `template` | Reworked the repo contract and workflow guidance to remove the out-of-scope iteration-status file, reduce `dev_log/` to the four approved files, and remove retired log filename references from active docs. | The user requested a reduced structure with only four log files and no iteration-status file. | `REQ-001`, `REQ-004`, `DEV-001` | `INT-PROD-*`, `INT-FB-*`
- `DEV-002` | `2026-04-07` | `design` | Reframed the design chain so `design/ux-flows.md` and `design/acceptance-criteria.md` are explicit first-class inputs, and updated the repo contract, plan files, and workflow prompts to reflect the tighter intent → UX flow → system design → acceptance criteria chain. | The new operating model requires explicit flow structure and deterministic acceptance criteria before tests and validation. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `ACC-001`, `ACC-002`, `ACC-003`, `ACC-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`, `DEV-002` | `INT-PROD-*`, `INT-FB-*`, `intent/gaps.md`
- `DEV-003` | `2026-04-07` | `template` | Numbered the folder and file inventories in `README.md`, `AGENTS.md`, and `.codex/project-context.md` so the repo structure reads as an ordered sequence. | The user requested that all folders and files be numbered in the right order. | `DEV-003` | `INT-PROD-*`, `INT-FB-*`
- `DEV-004` | `2026-04-07` | `design` | Split the combined design draft from `temp_all_in_1_design.md` into the four canonical design files and separated the shared material by responsibility. | The user requested that the full combined draft be distributed across the design documents without repetition. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `ACC-001`, `ACC-002`, `ACC-003`, `ACC-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `ARCH-007`, `ARCH-008`, `ARCH-009`, `ARCH-010`, `ARCH-011`, `ARCH-012`, `DEV-004` | `INT-PROD-*`, `INT-FB-*`, `temp_all_in_1_design.md`
- `DEV-005` | `2026-04-07` | `design` | Completed the translation pass by folding the remaining combined-draft sections for the knowledge model, source intake, agents, data/runtime services, and implementation plan into the canonical design documents, and aligned the repo contract to the no-prefix design structure. | The user asked to make sure all combined-draft content was translated into the design documents. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `ACC-001`, `ACC-002`, `ACC-003`, `ACC-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `ARCH-007`, `ARCH-008`, `ARCH-009`, `ARCH-010`, `ARCH-011`, `ARCH-012`, `DEV-005` | `INT-PROD-*`, `INT-FB-*`, `temp_all_in_1_design.md`
