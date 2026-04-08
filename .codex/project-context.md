# Codex Project Context

Compact task-start context for this repository. `AGENTS.md` is the authoritative contract; this file stays shorter and operational.

## Role
- Use this file to orient quickly before work.
- Keep it in sync with `AGENTS.md` for active repo shape and current design-map guidance.
- Do not repeat the full policy text from `AGENTS.md`.
- Always read this file and `AGENTS.md` before starting any task.
- Treat this file as the compact task-start checklist, not the full contract.
- Folder-by-folder acceptability rules live in `AGENTS.md`; this file keeps only the quick orientation.
- The numbered folder contracts in `AGENTS.md` define what belongs where, how files are created, and what is not allowed.

## Current repo shape
1. `intent/` is the starting point of requirements and contains `product-intent.md`, `feedback.md`, and `gaps.md`.
2. `plan/` is the temporary iteration workspace and contains `design-update.md`, `code-update.md`, and `test-update.md`.
3. `design/` is the current source of design truth and contains `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
4. `src/` is the implementation layer and contains application code, `README.md`, and `src/docs/`.
5. `tests/` is the validation layer and contains traceability, test plans, and test assets.
6. `dev_log/` is the permanent archive and contains `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
7. `dev_workflow/` contains the prompts that update design, code, tests, and logs in order.
8. `skills/` is used only when the task matches a skill’s scope.
9. `.codex/` holds local context and command references only.
10. Source of truth order: `intent/*` -> `plan/*` -> `design/*` -> `tests/*` -> `src/*`.
11. Plan entries and log entries use prefix IDs; design, `src/`, and `tests/` stay human-readable and do not use prefix IDs as primary numbering.

## `intent/`
1. Read first; do not edit unless explicitly asked.
2. `product-intent.md` and `feedback.md` are the only human-edited operational inputs.
3. `gaps.md` is system-edited from validation and `dev_log/*`.
4. Preserve full detail when translating to `plan/`.

## `plan/`
1. Keep scope explicit, carry open questions forward, and split work into design, code, and test updates.
2. Number plan entries with prefix IDs so the current iteration is traceable.

## `design/`
1. Keep the four files complementary and aligned to their owned concerns.
2. Keep them as plain markdown without prefix-numbered IDs in the content.

## `src/`
1. Implement from design, then update `src/docs/` when behavior changes.
2. Scaffold from design if `src/` is empty on the first implementation pass.

## `tests/`
1. Prove acceptance criteria and cover happy paths, edge cases, and failures.
2. Scaffold from design if `tests/` is empty on the first test pass.

## `dev_log/`
1. Record real changes and validation evidence through the workflow prompts.
2. Keep entries numbered with prefix IDs.

## `dev_workflow/`
1. Use these prompts to make design, code, test, and log updates in order.
2. Treat the prompts as the controlled iteration sequence.

## `skills/`
1. Open `SKILL.md` first and use the minimal matching skill.
2. Only use a skill when the task clearly matches its scope.

## Working loop
1. Read `intent/` first.
2. Reconcile into `plan/`.
3. Update `design/` before `src/` when behavior changes.
4. Update `tests/` to match acceptance criteria.
5. Record what changed in `dev_log/`.
6. Check alignment across intent, plan, design, tests, and code.
7. Validate the change with an explicit check before finishing.
8. Keep edits inside the scoped files unless a dependency is required in the same pass.

## Conflict rule
- If this file and `AGENTS.md` disagree, follow `AGENTS.md`.
