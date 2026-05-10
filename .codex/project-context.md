# Codex Project Context

Compact high-level design context for this repository. `AGENTS.md` is the authoritative contract; this file is the primary design summary above `design/*`.

## Role
- Use this file to orient quickly before work.
- Keep it in sync with root `AGENTS.md` for active repo shape, high-level design, and task-start guidance.
- Do not repeat the full policy text from root `AGENTS.md` or `.codex/AGENTS.md`.
- Always read `.codex/AGENTS.md`, root `AGENTS.md`, this file, and `.codex/tech-stack.md` before substantial work.
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
7. `.codex/dev_workflow/` contains the canonical AppFlow prompts that automatically route development prompts through the 11-step loop.
8. `.codex/skills/` contains reusable scoped procedures used only when a task matches a skill’s scope.
9. `.codex/agents/` contains bounded role contracts for planner, architecture, implementer, reviewer, validator, debugger, governance, and documentation agents.
10. `.codex/orchestration/` contains reusable execution patterns and long-horizon implementation-review-validation loops that support the canonical `.codex/dev_workflow/` sequence.
11. `.codex/context/` and `.codex/memory/` provide compact repository maps and reviewable structured memory for future Codex sessions.
12. `.codex/rules/`, `.codex/prompts/`, `.codex/tools/`, and `.codex/state/` hold repository-visible governance rules, prompt templates, deterministic helper scripts, and temporary resumable task state.
13. Only `src/` is intended for production runtime deployment; `.codex/`, `intent/`, `plan/`, `design/`, `tests/`, and `dev_log/` are engineering control-plane artifacts.
14. Source of truth order: `intent/*` -> `plan/*` -> `.codex/project-context.md` -> `design/*` -> `tests/*` -> `src/*`.
15. Plan entries and log entries use prefix IDs; design, `src/`, and `tests/` stay human-readable and do not use prefix IDs as primary numbering.

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
1. Prove correctness criteria and cover happy paths, edge cases, and failures.
2. Scaffold from design if `tests/` is empty on the first test pass.

## `dev_log/`
1. Record real changes and validation evidence through the workflow prompts.
2. Keep entries numbered with prefix IDs.

## `.codex/dev_workflow/`
1. Use these AppFlow prompts to make design, code, test, and log updates in order.
2. Treat the prompts as the controlled iteration sequence.
3. The default iteration sequence is 11 steps: create intent, read intent, create plan, update design, update tests, implement code, run validation, fix failures, update logs, detect gaps, and review the iteration.
4. Validation and failure-fix steps may loop until failures are resolved or explicitly deferred.
5. `README.md` documents the loop, and numbered prompt files `00-create-intent.md` through `10-iteration-review.md` provide the reusable step instructions.
6. The prompt set is intended to be execution-complete: an agent should be able to move from intent to validated iteration closeout by following the numbered prompts and current repo artifacts alone.
7. The workflow is artifact-driven: each step reads upstream artifacts, updates only its allowed downstream artifacts, and must satisfy its gate before the next step proceeds.

## `.codex/AGENTS.md` and `.codex/appflow.md`
1. `.codex/AGENTS.md` defines the reusable project-agnostic AppFlow factory contract.
2. `.codex/appflow.md` defines the reusable prompt-driven development lifecycle.
3. Root `AGENTS.md`, this file, and `.codex/tech-stack.md` are the expected project-specific extension points.
4. Keep all other `.codex/*` files project-agnostic unless improving the factory itself.
5. Use these files when the task changes prompt workflow behavior, `.codex` setup, or agent operating rules.

## Codex-native support structure
1. Use `.codex/context/*` for compact repository intelligence that helps task startup.
2. Use `.codex/memory/*` for factual, reviewable memory; do not let memory override source-of-truth artifacts.
3. Use `.codex/rules/*` for repository-visible operational rules.
4. Use `.codex/agents/*` for bounded responsibilities; agent roles do not grant authority beyond `AGENTS.md`.
5. Use `.codex/orchestration/*` for reusable workflow composition and HITL checkpoints.
6. Use `.codex/tools/validate_codex_contract.py` for static validation of Codex support artifacts.

## `skills/`
1. Open `SKILL.md` first and use the minimal matching skill.
2. Only use a skill when the task clearly matches its scope.

## Working loop
1. Convert the user prompt into `.codex/state/current-intent.md`.
2. Read `intent/` and reconcile the current-turn intent with human-owned project intent.
3. Reconcile into `plan/`.
4. Update `.codex/project-context.md` before detailed design when high-level behavior changes.
5. Update `design/` before `src/` when detailed behavior changes.
6. Update `tests/` from correctness criteria before code when behavior changes.
7. Implement in `src/`.
8. Validate explicitly, then loop on failure fixes until pass or explicit deferral.
9. Record what changed in `dev_log/`.
10. Surface follow-on gaps into `intent/gaps.md` when validation or review exposes them.
11. Review iteration completeness and only start the next loop when intent or feedback changes.
12. Keep edits inside the scoped files unless a dependency is required in the same pass.
13. Code changes follow the approved plan and design; they do not implicitly require `src/docs/` or `README.md` updates.
14. Update `dev_log/*` only after actual outcomes are known, and update `intent/gaps.md` only for evidence-backed system-detected follow-on gaps.
15. For workflow/Codex-support changes, validate with `python .codex/tools/validate_codex_contract.py` and `git diff --check` when available.

## Conflict rule
- If this file and `AGENTS.md` disagree, follow `AGENTS.md`.
