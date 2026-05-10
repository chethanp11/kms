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
- Linked IDs: `[REQ-xxx, DEV-xxx, TEST-xxx]`
- Intent sources: `[user prompt, intent/*, intent/gaps.md]`

## Entries
- `DEV-001` | `2026-04-07` | `template` | Reworked the repo contract and workflow guidance to remove the out-of-scope iteration-status file, reduce `dev_log/` to the four approved files, and remove retired log filename references from active docs. | The user requested a reduced structure with only four log files and no iteration-status file. | `REQ-001`, `REQ-004`, `DEV-001` | `INT-PROD-*`, `INT-FB-*`
- `DEV-002` | `2026-04-07` | `design` | Reframed the design chain so `design/ux-flows.md` and `design/acceptance-criteria.md` are explicit first-class inputs, and updated the repo contract, plan files, and workflow prompts to reflect the tighter intent → UX flow → system design → correctness criteria chain. | The new operating model requires explicit flow structure and deterministic correctness criteria before tests and validation. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `TEST-001`, `TEST-002`, `TEST-003`, `TEST-004`, `DEV-002` | `INT-PROD-*`, `INT-FB-*`, `intent/gaps.md`
- `DEV-003` | `2026-04-07` | `template` | Numbered the folder and file inventories in `README.md`, `AGENTS.md`, and `.codex/project-context.md` so the repo structure reads as an ordered sequence. | The user requested that all folders and files be numbered in the right order. | `DEV-003` | `INT-PROD-*`, `INT-FB-*`
- `DEV-004` | `2026-04-07` | `design` | Split the combined design draft into the four canonical design files and separated the shared material by responsibility. | The user requested that the full combined draft be distributed across the design documents without repetition. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `ARCH-007`, `ARCH-008`, `ARCH-009`, `ARCH-010`, `ARCH-011`, `ARCH-012`, `DEV-004` | `INT-PROD-*`, `INT-FB-*`
- `DEV-005` | `2026-04-07` | `design` | Completed the translation pass by folding the remaining combined-draft sections for the knowledge model, source intake, agents, data/runtime services, and implementation plan into the canonical design documents, and aligned the repo contract to the no-prefix design structure. | The user asked to make sure all combined-draft content was translated into the design documents. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `ARCH-007`, `ARCH-008`, `ARCH-009`, `ARCH-010`, `ARCH-011`, `ARCH-012`, `DEV-005` | `INT-PROD-*`, `INT-FB-*`
- `DEV-012` | `2026-05-10` | `workflow` | Added AppFlow lifecycle state/checklist design, populated factual memory entries from validated iterations, and clarified unit test traceability for concrete runtime contracts. | Address review gaps around lifecycle evidence, memory usefulness, and concrete validation coverage without broad product implementation. | `DEV-012`, `TEST-001`, `TEST-005` | `review gaps`
- `DEV-013` | `2026-05-10` | `workflow` | Added AppFlow step `00-create-intent`, made current-turn intent the first lifecycle artifact, removed the redundant workflow-pattern directory, and aligned reusable factory docs around the 11-step loop. | The user requested prompt-derived intent before read-intent and holistic `.codex` consistency cleanup. | `REQ-001`, `DEV-013`, `TEST-006` | `user prompt`
- `DEV-014` | `2026-05-10` | Added current scaffold alignment guidance to `design/architecture.md`. | The current app state has a limited `src/` scaffold and should not grow new top-level component families without future plan/design proof. | `REQ-014`, `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added scripts scaffold alignment and boundary guidance to `design/architecture.md`. | The design requires `/scripts`; the current staged scaffold needed a project-owned scripts boundary distinct from `.codex/tools/`. | `REQ-015`, `DEV-015`, `TEST-015` | `user prompt`
