# Code Update Log

## Purpose
Record meaningful code changes that were actually implemented.

## Intent linkage
- Capture implementation decisions that follow approved design.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Change: `[what code changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, DEV-xxx, TEST-xxx]`
- Intent sources: `[user prompt, intent/*, intent/gaps.md]`

## Entries
- `DEV-012` | `2026-05-10` | Added `.codex/tools/appflow_run.py`, expanded `.codex/tools/validate_codex_contract.py`, and introduced minimal KMS runtime modules in `src/contracts` and `src/execution`. | Provide executable lifecycle evidence checks, deeper semantic contract validation, and concrete runtime contracts for source discovery and knowledge-page validation. | `DEV-012`, `TEST-001`, `TEST-005` | `review gaps`
- `DEV-013` | `2026-05-10` | Updated `.codex/tools/appflow_run.py` and `.codex/tools/validate_codex_contract.py` to require `00-create-intent`, reject retired ID prefixes, and fail when retired support paths remain. | Make AppFlow lifecycle evidence and cleanup requirements deterministic instead of procedural only. | `DEV-013`, `TEST-006` | `user prompt`
