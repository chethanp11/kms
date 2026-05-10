# Test Update Plan

This file is generated from the active agentic workflow. Do not edit directly outside the workflow.

## Purpose
Capture validation changes required by the current iteration.

## Current intent signal
- Validate the portable AppFlow factory deterministically without introducing runtime dependencies.

## Required changes
1. `DEV-007`: Use `.codex/tools/validate_codex_contract.py` to check required support files, directories, skill frontmatter, required `AGENTS.md` references, and retired log references.
2. `DEV-007`: Use `git diff --check` for whitespace validation.
3. `DEV-008`: Verify reusable `.codex` files contain no KMS-specific coupling outside `.codex/project-context.md` and `.codex/tech-stack.md`.
4. `DEV-009`: Run `.codex/tools/bootstrap_appflow.py` in the current repo to verify it skips existing project files without overwriting them.
5. `DEV-010`: Validate that translated `kms.md` guidance keeps `.codex` project-agnostic and passes factory validation.
6. `DEV-011`: Validate that root `dev_workflow/`, `governance/`, `observability/`, the root workflow index, and `knowledge/` no longer exist; validate `.codex/dev_workflow/*` is present and project-agnostic.
7. `DEV-012`: Add concrete standard-library unit tests for `TEST-001` and `TEST-005`; run unit discovery, contract validation, and AppFlow state validation.
8. `DEV-013`: Validate the 11-step AppFlow contract, absence of retired ID prefixes, absence of duplicate workflow-pattern paths, and removal of the retired legacy guidance file.

## Existing drift or deviation
1. Documentation/workflow changes previously relied mostly on manual review.

## Open questions or blockers
1. None.

## Linked IDs
1. `DEV-007`
2. `DEV-008`
3. `DEV-009`
4. `DEV-010`
5. `DEV-011`
6. `DEV-012`
7. `DEV-013`
