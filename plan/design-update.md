# Design Update Plan

This file is generated from the active agentic workflow. Do not edit directly outside the workflow.

## Purpose
Capture design and workflow-support changes required by the current iteration.

## Current intent signal
- Convert `.codex/` into a reusable, project-agnostic AppFlow factory that can be copied into new application repositories. Only root `AGENTS.md` router, `.codex/project-context.md`, and `.codex/tech-stack.md` should require project-specific changes.

## Required changes
1. `DEV-007`: Establish a complete repo-level Codex operating contract in `AGENTS.md`.
2. `DEV-007`: Add purposeful `.codex` support structures for agents, workflows, orchestration, memory, context, rules, prompts, tools, and state.
3. `DEV-007`: Add human-facing index folders for workflows, governance, observability, and knowledge only where they point to active execution artifacts.
4. `DEV-007`: Update `.codex/project-context.md`, `.devmode/app.md`, `.codex/dev_workflow/README.md`, and `README.md` so repository navigation reflects the Codex-native structure.
5. `DEV-008`: Add `.devmode/app.md` as the portable AppFlow factory contract.
6. `DEV-008`: Remove project-specific KMS coupling from reusable `.codex` files outside `.codex/project-context.md` and `.codex/tech-stack.md`.
7. `DEV-008`: Reframe root `AGENTS.md` router as the KMS project contract that extends the reusable `.codex` factory.
8. `DEV-009`: Add copy/drop bootstrap guidance so a copied `.codex` folder can initialize missing project-specific AppFlow artifacts without overwriting existing files.
9. `DEV-010`: Translate durable guidance from `kms.md` into root `AGENTS.md` router for KMS-specific repository contracts and `.devmode/app.md` for reusable AppFlow factory rules.
10. `DEV-011`: Make AppFlow automatic for every development prompt, move the canonical 11-step workflow from root `dev_workflow/` into `.codex/dev_workflow/`, remove unnecessary top-level index folders, and document that only `src/` is production runtime.
11. `DEV-012`: Add lifecycle evidence enforcement, deeper semantic contract validation, factual memory entries, and minimal concrete runtime/test coverage for review gaps.
12. `DEV-013`: Add `00-create-intent` before `01-read-intent`, keep user prompt as the source for current-turn intent, retire the redundant workflow-pattern directory, and align AppFlow traceability around `REQ-*`, `DEV-*`, and `TEST-*`.

## Existing drift or deviation
1. `AGENTS.md` was an override fragment rather than a complete operating contract.
2. Existing `.codex` support had useful skills and context, but lacked explicit agent roles, orchestration protocols, memory/rules/context maps, prompt templates, and deterministic Codex contract validation.
3. The repository had no human-facing index for workflow, governance, observability, or knowledge assets.
4. Initial `.codex` scaffold still contained KMS-specific wording in reusable factory files.

## Open questions or blockers
1. None for the scaffold phase.
2. Runtime framework setup remains intentionally deferred until product implementation requires it.

## Linked IDs
1. `DEV-007`
2. `DEV-008`
3. `DEV-009`
4. `DEV-010`
5. `DEV-011`
6. `DEV-012`
7. `DEV-013`
