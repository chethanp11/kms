# Current-Turn Intent

## Raw prompt summary
Add a create-intent step before read-intent, remove retired criteria ID prefix as an ID prefix, remove redundant workflow structure, ensure legacy root guidance is captured, delete the legacy root guidance file, and fix holistic `.codex` inconsistencies.

## Interpreted objective
Refactor AppFlow into an 11-step lifecycle where the raw user prompt is first converted into current-turn intent, then reconciled with project artifacts before planning and implementation.

## Deliverables
- Add `.codex/dev_workflow/00-create-intent.md`.
- Update AppFlow docs, state tooling, validator, and closeout checklist for 11 steps.
- Remove `retired criteria ID prefix` ID usage and keep only `REQ-*`, `DEV-*`, and `TEST-*`.
- Remove the redundant workflow-pattern folder structure.
- Delete the legacy root guidance file after translated guidance is captured.
- Validate `.codex` consistency.

## Constraints
- Keep `.codex` reusable and project-agnostic except project context and tech stack.
- Do not add unnecessary new folders.
- Preserve project-specific guidance in root `AGENTS.md` and project docs.
