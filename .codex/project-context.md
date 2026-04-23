# Codex Project Context

Compact high-level design context for this repository. `AGENTS.md` is the authoritative contract; this file is the primary design summary above `design/*`.

## Role
- Use this file to orient quickly before work.
- Keep it in sync with `AGENTS.md` for active repo shape, high-level design, and task-start guidance.
- Do not repeat the full policy text from `AGENTS.md`.
- Always read this file and `AGENTS.md` before starting any task.
- Treat this file as the compact high-level design summary, not the full contract.
- Folder-by-folder acceptability rules live in `AGENTS.md`; this file keeps the operating model and current design map.
- The numbered folder contracts in `AGENTS.md` define what belongs where, how files are created, and what is not allowed.

## Current repo shape
1. `intent/` is the starting point of requirements and contains `product-intent.md`, `feedback-intent.md`, and `gaps.md`.
2. `plan/` is the temporary iteration workspace and contains `design-update.md`, `code-update.md`, and `test-update.md`.
3. `design/` is the detailed design layer and contains `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
4. `src/` is the implementation layer and currently contains backend-oriented scaffold packages in `src/app`, `src/agents`, `src/context`, `src/contracts`, `src/execution`, `src/governance`, `src/observability`, `src/orchestrator`, and `src/shared`.
5. `tests/` is the validation layer and contains traceability, test plans, and test assets.
6. `dev_log/` is the permanent archive and contains `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
7. `dev_workflow/` contains the prompts that update design, code, tests, and logs in order.
8. `skills/` is used only when the task matches a skill’s scope.
9. `.codex/` holds local context, command references, and the local implementation stack note in `.codex/tech-stack.md`.
10. Source of truth order: `intent/*` -> `plan/*` -> `.codex/project-context.md` -> `design/*` -> `tests/*` -> `src/*`.
11. Plan entries and log entries use prefix IDs; design, `src/`, and `tests/` stay human-readable and do not use prefix IDs as primary numbering.

## `intent/`
1. Read first; do not edit unless explicitly asked.
2. `product-intent.md` and `feedback-intent.md` are the only human-edited operational inputs.
3. `gaps.md` is system-edited from validation and `dev_log/*`.
4. Preserve full detail when translating to `plan/`.

## `plan/`
1. Keep scope explicit, carry open questions forward, and split work into design, code, and test updates.
2. Number plan entries with prefix IDs so the current iteration is traceable.

## Active design map
- `.codex/project-context.md` defines the high-level product identity, operating model, and precedence over detailed design.
- `design/system-design.md` defines the detailed product identity, scope, users, and operating model.
- `design/architecture.md` defines the detailed layered system architecture and major services.
- `design/ux-flows.md` defines the detailed KMI and Infopedia interaction model and user flows.
- `design/acceptance-criteria.md` defines the detailed governance, validation gates, and policy enforcement.

## `design/`
1. Keep the four files complementary and aligned to their owned concerns.
2. Keep them as plain markdown without prefix-numbered IDs in the content.
3. Keep them aligned to `.codex/project-context.md`.
4. If any of the four canonical design files are missing on a new project or first pass, create them before broadening the design layer.

## `src/`
1. Implement from approved `plan/*` and `design/*`.
2. Scaffold from design if `src/` is empty on the first implementation pass; the current scaffold is placeholder-only and backend-oriented.
3. Use `.codex/tech-stack.md` as the local reference for the intended backend, frontend, and test stack when updating `src/`.

## `tests/`
1. Prove acceptance criteria and cover happy paths, edge cases, and failures.
2. Scaffold from design if `tests/` is empty on the first test pass.

## `dev_log/`
1. Record real changes and validation evidence through the workflow prompts.
2. Keep entries numbered with prefix IDs.

## `dev_workflow/`
1. Use these prompts to make design, code, test, and log updates in order.
2. Treat the prompts as the controlled iteration sequence.
3. The default iteration sequence is 10 steps: read intent, create plan, update design, update tests, implement code, run validation, fix failures, update logs, detect gaps, and review the iteration.
4. Validation and failure-fix steps may loop until failures are resolved or explicitly deferred.
5. `README.md` documents the loop, and numbered prompt files `01-read-intent.md` through `10-iteration-review.md` provide the reusable step instructions.
6. The prompt set is intended to be execution-complete: an agent should be able to move from intent to validated iteration closeout by following the numbered prompts and current repo artifacts alone.

## `skills/`
1. Open `SKILL.md` first and use the minimal matching skill.
2. Only use a skill when the task clearly matches its scope.

## Working loop
1. Read `intent/` first.
2. Reconcile into `plan/`.
3. Update `.codex/project-context.md` before detailed design when high-level behavior changes.
4. Update `design/` before `src/` when detailed behavior changes.
5. Update `tests/` from acceptance criteria before code when behavior changes.
6. Implement in `src/`.
7. Validate explicitly, then loop on failure fixes until pass or explicit deferral.
8. Record what changed in `dev_log/`.
9. Surface follow-on gaps into `intent/gaps.md` when validation or review exposes them.
10. Review iteration completeness and only start the next loop when intent or feedback changes.
11. Keep edits inside the scoped files unless a dependency is required in the same pass.
12. Code changes follow the approved plan and design; they do not implicitly require `src/docs/` or `README.md` updates.

## Conflict rule
- If this file and `AGENTS.md` disagree, follow `AGENTS.md`.
