# Project Agents Guide

## Purpose
Provide repo-level rules for Codex and other AI collaborators working in this template or in any project copied from it.

## Always-update contract
- When the user gives a new prompt that changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` first.
- Treat those two files as the always-current top-level contract for the repo.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Contract roles
1. `AGENTS.md` is the authoritative repo contract. It defines durable policy, precedence, file ownership, traceability rules, and the structure that every other artifact must follow.
2. `.codex/project-context.md` is the compact working context. It should stay shorter than `AGENTS.md` and only carry the current repo shape, the active design map, and task-start guidance.
3. If the two files overlap, keep the full rule in `AGENTS.md` and a short operational summary in `.codex/project-context.md`.
4. If the two files disagree, `AGENTS.md` wins.
5. Always read both files before starting any task.
6. Reread both files at the start of every new task, and also whenever a prompt changes workflow, precedence, ownership, or operating rules.

## Boundary rules
1. If a request is ambiguous about scope, file targets, validation, or ownership, stop and ask before editing.
2. Do not edit outside the explicit task scope unless the change is a direct dependency of that scope and is called out in the same pass.
3. Prefer the smallest set of files that fully completes the task.

## Workflow contract
1. `intent/` is the starting point of requirements.
2. `intent/product-intent.md` and `intent/feedback.md` are the only human-edited operational inputs for the workflow.
3. `intent/gaps.md` is a system-edited operational input that is updated by a prompt after reviewing `dev_log/*`.
4. `design/` is the current source of design truth.
5. `plan/` is the temporary working area for the current iteration only.
6. `dev_log/` is the permanent archive of what was actually updated and validated.
7. `src/` is the implementation space, and `tests/` is the validation space.
8. A new iteration starts only after `intent/` or `feedback.md` is updated manually, or after validation surfaces gaps that are recorded back into `intent/`.

## Folder contracts
### `intent/`
1. Files that belong here are `product-intent.md`, `feedback.md`, and `gaps.md`.
2. Create or revise `product-intent.md` manually when product goals, scope, user flows, constraints, or expected behavior change.
3. Create or revise `feedback.md` manually when manual review, testing, usage feedback, bug observations, or scope changes introduce new findings.
4. Update `gaps.md` through a prompt that reads `dev_log/*` and records system-detected gaps, not human-authored interpretation.
5. Do not place implementation code, ad hoc design rewrites, or silent reinterpretation here.

### `plan/`
1. Files that belong here are `design-update.md`, `code-update.md`, and `test-update.md`.
2. Create or revise these files at the start of an iteration after reading `intent/`, `design/`, `src/`, and `tests/`.
3. Use this folder to reconcile gaps and classify pending work into design, code, and test changes.
4. Number plan entries with prefixes such as `REQ-*`, `DEV-*`, and `TEST-*` so the current iteration is explicit.
5. Do not store final implementation, hidden assumptions, or direct code edits here.

### `design/`
1. Files that belong here are `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
2. Create or revise these files when approved intent or plan work changes system behavior, structure, user experience, or correctness rules.
3. Use this folder for the system truth layer. Keep each file focused on its owned concern and keep the set complementary.
4. These files are plain human-readable markdown and do not use prefix IDs as in-document numbering.
5. Do not add extra design files, prefixed in-document traceability labels, or repeated content that blurs file ownership.

### `src/`
1. Files that belong here are implementation source files, app scaffolding, and application documentation such as `README.md` and `src/docs/`.
2. Create or revise these files only after the design has defined the expected behavior and structure for the change.
3. If `src/` is empty on the first implementation pass, scaffold it from design before adding behavior.
4. These files are plain implementation artifacts and do not use prefix IDs as primary numbering.
5. Do not store design drafts, plan notes, or code that diverges from the current design without an approved update.

### `tests/`
1. Files that belong here are traceability notes, test plans, validation assets, and the test suites that prove the design.
2. Create or revise these files whenever acceptance criteria, workflows, or implemented behavior change.
3. If `tests/` is empty on the first test pass, scaffold it from the design before broadening coverage.
4. These files are plain validation artifacts and do not use prefix IDs as primary numbering.
5. Do not invent tests without design linkage or keep validation artifacts that do not map back to criteria.

### `dev_log/`
1. Files that belong here are `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
2. Create or revise these files through the workflow prompts after the corresponding design, code, test, or validation step has actually occurred.
3. Use prefix IDs in log entries to show what was implemented where, and keep the archive permanent and traceable.
4. Do not add extra log files, make manual edits outside the workflow, or fabricate validation evidence.

### `dev_workflow/`
1. Files that belong here are reusable prompts and runbooks that drive the closed loop from design to validation.
2. Create or revise these files when the repository workflow itself needs a new or better step, order, or guardrail.
3. Use this folder to orchestrate updates to design, code, tests, and logs in the correct order.
4. Do not place direct implementation content, hidden one off procedures, or workflow steps that bypass the contract.

### `skills/`
1. Files that belong here are skill definitions and supporting instructions for reusable scoped workflows.
2. Create or revise these files only when the task really needs a reusable skill that fits a defined scope.
3. Use this folder for tasks that match the skill description and benefit from a reusable workflow.
4. Do not use a skill outside its scope or bypass `AGENTS.md` and the active design.

### `.codex/`
1. Files that belong here are repo local context, command references, and other Codex support files.
2. Create or revise these files when local working guidance or command references need to change for the repository.
3. Use this folder for compact working context that helps Codex operate inside the contract.
4. Do not replace the top level contract here, store implementation state here, or duplicate the full repo policy.

## Validation rules
1. Every non-trivial change must end with an explicit validation step such as `git diff --check`, a targeted test, or another relevant check.
2. Document the validation command or check in the workflow or log artifact that records the iteration.
3. Keep validation aligned with the changed layer: design changes validate structure and content, code changes validate behavior, and test changes validate coverage.

## Required read order before substantial work
Read the latest relevant artifacts in this order before modifying more than one file:
1. `README.md`
2. `intent/product-intent.md`
3. `intent/feedback.md` or the current active feedback file during migration
4. `intent/gaps.md` when system-detected gaps exist
5. `plan/design-update.md`
6. `plan/code-update.md`
7. `plan/test-update.md`
8. Relevant files from `design/`
9. `tests/design-traceability.md` and `tests/test-plan.md`
10. The active `dev_log/` files
11. Relevant step file from `dev_workflow/`

## Required behavior for Codex
1. Always read `intent/` before starting a task.
2. Treat `intent/` as the starting point of every loop and the highest-priority human input.
3. Do not modify `intent/` unless the user explicitly asks for it.
4. Translate intent into `plan/*` before coding or rewriting design, code, or tests.
5. Preserve the detail in `intent/*` when translating into `plan/*`; do not compress away constraints, distinctions, or open questions that affect behavior.
6. Compare the latest intent against current design, code, and tests, then split the needed work into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
7. Carry unresolved ambiguities into `plan/*` and the relevant downstream artifact instead of silently choosing a direction.
8. Make the plan explicit about what changed, what was deferred, and which `REQ-*`, `ACC-*`, `ARCH-*`, `TEST-*`, `FB-*`, or `DEV-*` items were created or revised.
9. Update or add tests and eval mappings whenever behavior, contracts, or acceptance criteria change.
10. Stay inside the documented version and iteration boundary after intent has been interpreted into plan and design.
11. Do not invent behavior that is not represented in intent, plan, design, or acceptance artifacts.
12. Align implementation with both intent and plan-guided design.
13. Always reflect meaningful intent changes into `plan/*`, `design/*`, `tests/*`, and the active `dev_log/` files.
14. Update logs when the work changes reality:
   - `dev_log/design-update-log.md` for meaningful design updates
   - `dev_log/code-update-log.md` for meaningful code updates
   - `dev_log/test-update-log.md` for meaningful test updates
   - `dev_log/validation-results.md` for actual validation evidence
15. Keep all work traceable to `intent/*`, `plan/*`, and to `REQ-*`, `ACC-*`, `ARCH-*`, `TEST-*`, `FB-*`, or `DEV-*`.
16. If a requirement is unclear, log it as a plan or design issue or open question instead of implementing a guess.
17. Treat manual feedback as first-class input; route it through the active feedback record in `intent/` and the operational logs in `dev_log/` when it should influence future direction.

## Allowed issue classifications
Use exactly these categories when classifying issues or feedback:
- design defect
- implementation defect
- test defect
- eval gap
- environment issue
- backlog enhancement

## Traceability rules
1. `intent/*` defines what humans want.
2. `design/ux-flows.md` defines how users experience the system.
3. `design/system-design.md` defines how the system behaves.
4. `design/acceptance-criteria.md` defines what correct means.
5. `REQ-*` should describe what the system must do.
6. `ACC-*` should define how readiness is judged.
7. `TEST-*` should prove `ACC-*`.
8. `ARCH-*` should constrain implementation details.
9. `FB-*` should capture human feedback without losing source or action target.
10. `DEV-*` should identify operational records such as issues, decisions, deviations, validation runs, and improvements.

## Testing discipline
- Create tests for all implemented behavior.
- Cover happy paths, edge cases, and failure scenarios.
- Validate against design intent, not just code behavior.
- Flag untestable or unclear design areas.

## Review discipline
For every iteration, review:
- requirement coverage
- architectural alignment
- code quality and modularity
- duplication and coupling
- failure handling
- performance risks
- security considerations
- test sufficiency

## Instruction hierarchy
When artifacts disagree, use this precedence:
1. `intent/*`
2. `plan/*`
3. `design/*`
4. `tests/*`
5. `src/*`

If implementation deviates from intent, flag it and log it. Do not silently normalize the drift.

## Repository constraints
- Keep the repo reusable by avoiding hardcoded app-specific examples in workflow and contract text unless the active project intent requires them.
- Use bracketed placeholders such as `[Project Name]`, `[Version]`, and `[Primary Model]` where project-specific content belongs.
- Treat the copied project as a reusable baseline, not a finished application.

## Editing model
- Human edits by default: `intent/*`
- Human edits occasionally: `AGENTS.md`, `skills/*`
- System-managed through workflow: `plan/*`, `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Source tree rule
- `src/README.md` is the project README for the copied application.
- `src/docs/` holds application purpose and functionality documentation.
- `src/` may be empty at the beginning; scaffold it from design, then refactor or expand it as design requires.

## Log ownership rule
- The four `dev_log/` files are updated by `dev_workflow/*` prompts, not by ad hoc manual edits.
- Use workflow prompts to record changes and validation evidence.
- If a user wants a direct log update, translate it into the appropriate workflow step and then update the log through that step.
- Design changes produced by `dev_workflow/00-design-update.md` must be captured in `dev_log/design-update-log.md`.

## Practical decision rules
- If intent changes, translate it into design first, then update tests, logs, and only then implementation.
- If behavior changes, update code first, then update `src/docs/` to reflect the changed behavior, and update design, tests, and logs in the same pass.
- If only implementation changes and behavior does not, keep design stable and update tests or logs as needed.
- If validation fails, classify the failure before changing code.
- If a requested change exceeds the active scope, move it to backlog unless the design is updated first.
- Do not code directly from vague intent; structure it into design first.

## Logging and artifacts
- Every iteration must update the four `dev_log/` files with what was implemented and what was validated.
- Logs must allow continuation by another agent without loss of context.
- If implementation exposes a design gap, record it in the relevant plan or design artifact before normalizing the code path.

## Alignment enforcement
- Continuously verify intent to design alignment.
- Continuously verify design to code alignment.
- Continuously verify code to tests alignment.
- Continuously verify tests to expected behavior alignment.
- If misalignment occurs, classify it as a design gap, implementation defect, test gap, or architecture mismatch, then fix it at the correct layer.

## Failure handling
- State the blocker explicitly.
- Classify the root cause.
- Propose concrete next steps.
- Proceed as far as safely possible with assumptions clearly logged.

## Reusability requirement
- Keep workflows, prompts, and structures reusable across projects.
- Avoid hardcoding a specific domain.
- Separate generic workflow logic from project-specific intent and design.

## Definition of done for a scoped iteration
- Relevant intent sections were read and interpreted explicitly.
- In-scope IDs are explicit.
- Implementation matches design and design matches intent.
- Tests exist or are intentionally deferred with documented rationale, and any manual review requirement is explicit.
- Validation evidence is recorded.
- Next actions are clear enough to continue the iteration without archaeology.

## Behavior expectations
- Be precise, not verbose.
- Challenge weak or incomplete design.
- Do not skip steps in the loop.
- Do not generate large code blindly.
- Prefer structured progress over speed.
- Surface assumptions explicitly.
- Maintain engineering discipline at all times.
