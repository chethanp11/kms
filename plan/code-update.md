# Code Update Plan

This file is generated from the active agentic workflow. Do not edit directly outside the workflow.

## Purpose
Capture implementation and tooling changes required by the current iteration.

## Current intent signal
- Add deterministic repository tooling only where it supports portable AppFlow factory validation.

## Required changes
1. `DEV-007`: Add `.codex/tools/validate_codex_contract.py` using only the Python standard library.
2. `DEV-008`: Update `.codex/tools/validate_codex_contract.py` to validate the portable `.codex` factory instead of requiring project-specific KMS files.
3. `DEV-009`: Add `.codex/tools/bootstrap_appflow.py` as a conservative no-overwrite bootstrap helper for copied factory usage.
4. `DEV-010`: Update `.codex/tools/validate_codex_contract.py` generic uppercase allowlist so reusable AppFlow traceability IDs are not misclassified as project-specific terms.
5. `DEV-011`: Update `.codex/tools/validate_codex_contract.py` to require the canonical `.codex/dev_workflow/*` files.
6. `DEV-012`: Add `.codex/tools/appflow_run.py`, expand `.codex/tools/validate_codex_contract.py` semantic checks, and add minimal `src/contracts` and `src/execution` runtime modules.
7. `DEV-013`: Update AppFlow state tooling and contract validation for `00-create-intent`, retired ID prefixes, removed duplicate workflow-pattern paths, and retired legacy guidance files.

## Existing drift or deviation
1. No product runtime code exists yet.
2. There was no deterministic static validation entrypoint for Codex support artifacts.

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
