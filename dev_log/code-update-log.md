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
- `DEV-014` | `2026-05-10` | Added initial standard-library KMS scaffold under `src/` with contracts, execution, governance, orchestration, API endpoint inventory, context boundaries, agent role names, and audit-event helpers. | Create a concrete implementation starting point aligned to the design while preserving governed `/wiki`, raw-source, KMI, and Infopedia boundaries. | `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added foundational component primitives in `src/components`, explicit ports in `src/ports`, deterministic in-memory stores in `src/storage`, and exported the base registry from `src`. | Provide stable base contracts for future KMS services, stores, projections, governance gates, and adapters while preserving `/wiki`, metadata, raw-source, and Infopedia authority boundaries. | `DEV-015`, `TEST-015` | `user prompt`
- `DEV-014` | `2026-05-10` | Corrected `src/__init__.py` to export only modules present in the current scaffold. | Remove stale references to absent component-family modules without adding unneeded new `src` components. | `REQ-014`, `DEV-014`, `TEST-014` | `user prompt`
- `DEV-015` | `2026-05-10` | Added top-level `scripts/` scaffold with `README.md`, `__init__.py`, and `validate_scaffold.py`. | Provide deterministic project scaffold validation without adding new `src` component families. | `REQ-015`, `DEV-015`, `TEST-015` | `user prompt`
