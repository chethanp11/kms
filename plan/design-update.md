# Design Update Plan

This file is generated from `dev_workflow/plan-update.md`. Do not edit directly.

## Purpose
Capture the design changes that should be made next after comparing the latest intent with the current design, code, tests, and logs.

## Current intent signal
- Reconcile the repo-wide contract and support docs so every top-level instruction file describes KMS, not the retired ABA/AutoAIdev variants.

## Required changes
1. Normalize `AGENTS.md`, `.codex/project-context.md`, and `README.md` so they all describe the same KMS operating model and file layout.
2. Remove or retire legacy conflicting support docs that describe AutoAIdev or ABA rather than KMS.
3. Bring the `src/` scaffold description in `.codex/project-context.md` into sync with the current placeholder package layout.

## Existing drift or deviation
1. Legacy docs in the repository root still contain retired framework names and conflict with the KMS contract.
2. The `src/` scaffold exists as placeholder packages but the compact context summary does not yet describe the actual package layout.
3. A conflicting override file (`AGENTS.overrideXX.md`) remains in the repository and should not coexist with the KMS contract.

## Open questions or blockers
1. None.

## Linked IDs
1. `DEV-005`
