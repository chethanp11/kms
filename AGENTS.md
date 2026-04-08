# Project Agents Guide

## Purpose
Provide repo-level rules for Codex and other AI collaborators working in this template or in any project copied from it.

## Always-update contract
- When the user gives a new prompt that changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` first.
- Treat those two files as the always-current top-level contract for the repo.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Contract roles
1. `AGENTS.md` is the authoritative repo contract. It defines durable policy, precedence, file ownership, traceability rules, and the structure that every other artifact must follow.
2. `.codex/project-context.md` is the compact high-level design source and working context.
3. If `AGENTS.md` and `.codex/project-context.md` overlap, keep the durable policy in `AGENTS.md` and the current high-level design summary in `.codex/project-context.md`.
4. If `.codex/project-context.md` and `design/*` disagree, `.codex/project-context.md` wins for high-level design intent until it is updated.
5. Always read both files before starting any task.
6. Reread both files at the start of every new task, and also whenever a prompt changes workflow, precedence, ownership, or operating rules.

## Repo Shape
- `intent/` holds requirements and feedback inputs.
- `plan/` is the current iteration workspace.
- `design/` is the live design source of truth.
- `src/` is the implementation layer.
- `tests/` is the validation layer.
- `dev_log/` is the permanent execution record.
- `dev_workflow/` contains the prompts and runbooks that drive the loop.
- `skills/` contains reusable scoped procedures.
- `.codex/` contains local context and command references only.

## Boundary rules
1. If a request is ambiguous about scope, file targets, validation, or ownership, stop and ask before editing.
2. Do not edit outside the explicit task scope unless the change is a direct dependency of that scope and is called out in the same pass.
3. Prefer the smallest set of files that fully completes the task.

## Workflow contract
1. `intent/` is the starting point of requirements.
2. `intent/product-intent.md` and `intent/feedback.md` are the only human-edited operational inputs for the workflow.
3. `intent/gaps.md` is a system-edited operational input that is updated by a prompt after reviewing `dev_log/*`.
4. `.codex/project-context.md` is the high-level design source of truth above `design/*`.
5. `design/` is the detailed design layer that must align to `.codex/project-context.md`.
6. `plan/` is the temporary working area for the current iteration only.
7. `dev_log/` is the permanent archive of what was actually updated and validated.
8. `src/` is the implementation space, and `tests/` is the validation space.
9. A new iteration starts only after `intent/` or `feedback.md` is updated manually, or after validation surfaces gaps that are recorded back into `intent/`.

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
2. Create or revise these files when approved intent, plan work, or `.codex/project-context.md` changes system behavior, structure, user experience, or correctness rules.
3. Use this folder for the detailed system layer. Keep each file focused on its owned concern and keep the set complementary.
4. These files are plain human-readable markdown and do not use prefix IDs as in-document numbering.
5. Do not add extra design files, prefixed in-document traceability labels, or repeated content that blurs file ownership.
6. `REQ-*`, `DEV-*`, and `TEST-*` are used in comments only

### `src/`
1. Files that belong here are implementation source files, app scaffolding, and application documentation such as `README.md` and `src/docs/`.
2. Create or revise these files only after the design has defined the expected behavior and structure for the change.
3. If `src/` is empty on the first implementation pass, scaffold it from design before adding behavior.
4. These files are plain implementation artifacts and do not use prefix IDs as primary numbering.
5. Do not store design drafts, plan notes, or code that diverges from the current design without an approved update.
6. `REQ-*`, `DEV-*`, and `TEST-*` are used in comments only

### `tests/`
1. Files that belong here are traceability notes, test plans, validation assets, and the test suites that prove the design.
2. Create or revise these files whenever acceptance criteria, workflows, or implemented behavior change.
3. If `tests/` is empty on the first test pass, scaffold it from the design before broadening coverage.
4. These files are plain validation artifacts and do not use prefix IDs as primary numbering.
5. Do not invent tests without design linkage or keep validation artifacts that do not map back to criteria.
6. `REQ-*`, `DEV-*`, and `TEST-*` are used in comments only

### `dev_log/`
1. Files that belong here are `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
2. Create or revise these files through the workflow prompts after the corresponding design, code, test, or validation step has actually occurred.
3. Number log entries with prefixes such as `REQ-*`, `DEV-*`, and `TEST-*` to show what was implemented where, and keep the archive permanent and traceable.
4. Do not add extra log files, make manual edits outside the workflow, or fabricate validation evidence.


### `dev_workflow/`
1. Files that belong here are reusable prompts and runbooks that drive the closed loop from design to validation.
2. Create or revise these files when the repository workflow itself needs a new or better step, order, or guardrail.
3. Use this folder to orchestrate updates to design, code, tests, and logs in the correct order.
4. Do not place direct implementation content, hidden one off procedures, or workflow steps that bypass the contract.
5. Read `AGENTS.md` and `.codex/project-context.md` first before running these prompts.

### `skills/`
1. Files that belong here are skill definitions and supporting instructions for reusable scoped workflows.
2. Create or revise these files only when the task really needs a reusable skill that fits a defined scope.
3. Use this folder for tasks that match the skill description and benefit from a reusable workflow.
4. use skills applicable along with `dev_workflow/*` prompts.
4. Do not use a skill outside its scope or bypass `AGENTS.md` and the active design.

### `.codex/`
1. Files that belong here are repo local context, command references, and other Codex support files.
2. Create or revise these files when local working guidance or command references need to change for the repository.
3. Use this folder for compact working context that helps Codex operate inside the contract.
4. Do not replace the top level contract here, store implementation state here, or duplicate the full repo policy.
5. `.codex/project-context.md` is the compact high-level design source and working context.

## Validation rules
1. Every non-trivial change must end with an explicit validation step such as `git diff --check`, a targeted test, or another relevant check.
2. Document the validation command or check in the workflow or log artifact that records the iteration.
3. Keep validation aligned with the changed layer: design changes validate structure and content, code changes validate behavior, and test changes validate coverage.

## Required read order before substantial work
Read the latest relevant artifacts in this order before modifying more than one file:
1. `AGENTS.md` and `.codex/project-context.md`
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
1. start any task by reading `AGENTS.md` and `.codex/project-context.md`
1. Always read `intent/` before starting a task.
2. Treat `intent/` as the starting point of every loop and the highest-priority human input.
3. Do not modify `intent/` unless the user explicitly asks for it.
4. Translate intent into `plan/*` before coding or rewriting `.codex/project-context.md`, design, code, or tests.
5. Preserve the detail in `intent/*` when translating into `plan/*`; do not compress away constraints, distinctions, or open questions that affect behavior.
6. Compare the latest intent against current high-level context, detailed design, code, and tests, then split the needed work into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
7. Carry unresolved ambiguities into `plan/*` and the relevant downstream artifact instead of silently choosing a direction.
8. Make the plan explicit about what changed, what was deferred, and which `REQ-*`, `TEST-*`, or `DEV-*` items were created or revised.
9. Update or add tests and eval mappings whenever behavior, contracts, or acceptance criteria change.
10. Stay inside the documented version and iteration boundary after intent has been interpreted into plan and context.
11. Do not invent behavior that is not represented in intent, plan, `.codex/project-context.md`, design, or acceptance artifacts.
12. Align implementation with both intent and plan-guided context and design.
13. Always reflect meaningful intent changes into `plan/*`, `.codex/project-context.md`, `design/*`, `tests/*`, and the active `dev_log/` files.
14. Update logs when the work changes reality:
   - `dev_log/design-update-log.md` for meaningful design updates
   - `dev_log/code-update-log.md` for meaningful code updates
   - `dev_log/test-update-log.md` for meaningful test updates
   - `dev_log/validation-results.md` for actual validation evidence
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
2. `.codex/project-context.md` defines the high-level design and operating model above the detailed design files.
3. `design/ux-flows.md` defines how users experience the system.
4. `design/system-design.md` defines how the system behaves.
5. `design/acceptance-criteria.md` defines what correct means.
6. `REQ-*` should describe design changes
11. `DEV-*` should describe code changes
8. `TEST-*` should describe tests
12. Only `plan/*` , `dev_log/*`  carry `REQ-*` , `DEV-*` `TEST-*` as ID.
13. `design/*`, `src/*`  and `tests/*` carry `REQ-*` , `DEV-*` `TEST-*` as comments only

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
3. `.codex/project-context.md`
4. `design/*`
5. `tests/*`
6. `src/*`

If implementation deviates from intent, flag it and log it. Do not silently normalize the drift.

## Repository constraints
- Keep the repo reusable by avoiding hardcoded app-specific examples in workflow and contract text unless the active project intent requires them.


## Editing model
- Human edits by default: `intent/product-intent.md`, `intent/feedback-intent.md`
- Human edits occasionally: `AGENTS.md`, `skills/*`
- System-managed through workflow: `intent/gaps.md`, `plan/*`, `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Source tree rule
- `README.md` is the project README for the copied application.
- `src/docs/` holds application purpose and functionality documentation.
- `src/` may be empty at the beginning; scaffold it from design, then refactor or expand it as design requires.

## Log ownership rule
- The four `dev_log/` files are updated by `dev_workflow/*` prompts, not by ad hoc manual edits.
- Use workflow prompts to record changes and validation evidence.

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

## Application Flow
1. `intent/` is the starting point of requirements.
2. `intent/` contains exactly these operational input files: `product-intent.md`, `feedback.md`, and `gaps.md`.
3. Manually update `intent/product-intent.md` with the latest product goals, scope, user flows, constraints, and expected behavior.
4. Manually update `intent/feedback.md` with new findings from manual review, testing, usage feedback, bug observations, or scope changes.
5. A prompt reviews `dev_log/*` and updates `intent/gaps.md`.
6. Treat `intent/product-intent.md` and `intent/feedback.md` as the only human-edited operational inputs for the workflow.
7. Treat `intent/gaps.md` as a system-edited operational input for the workflow.
8. Keep `design/` as the current source of design truth, not `intent/` and not any temporary plan files.
9. Keep `plan/` as the temporary working area for the current iteration only.
10. Keep `dev_log/` as the permanent archive of what was actually updated and validated.
11. The current design is represented by exactly these files: `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md`.
12. If any of those four design files are missing on a new project or first pass, create them before broadening the design layer.
13. Design files are typical markdown files and remain human-readable.
14. Design files do not use prefix IDs as primary numbering.
15. Plan files and log file entries use prefix IDs to show what was planned, implemented, and validated where.
16. `design/`, `src/`, and `tests/` do not use prefix IDs as primary numbering, although comments may carry traceability notes when needed.
17. Ensure current implementation exists in `src/`; if not, scaffold it from design when the implementation prompt runs for the first time.
18. Ensure the current test suite exists in `tests/`; if not, scaffold it from design when the test prompt runs for the first time.
19. An iteration means running `dev_workflow` prompts in sequence, either manually or programmatically.
20. A new iteration starts only after `intent/` or `feedback.md` is updated manually, or after validation identifies gaps that are captured back into `intent/`.

## Updating Plan
1. All activities are driven by a prompt or a series of prompts.
2. The objective is to update three files in `plan/`: `design-update.md`, `code-update.md`, and `test-update.md`.
3. Reconcile `intent/`, `design/`, `src/`, and `tests/`.
4. Read `intent/product-intent.md` fully.
5. Read `intent/feedback.md` fully.
6. Read `intent/gaps.md` fully.
7. Read all relevant design files in `design/`.
8. Inspect the current source code in `src/`.
9. Inspect the current tests in `tests/`.
10. Identify gaps between product intent and current design.
11. Identify gaps between design and current code.
12. Identify gaps between code and current tests.
13. Identify whether any product-intent, feedback, or gaps item requires design changes, code changes, test changes, or some combination of them.
14. Classify all pending work into three buckets: `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
15. Write the pending design changes into `plan/design-update.md` with prefix `REQ-*`.
16. Write the preliminary pending code changes into `plan/code-update.md` with prefix `DEV-*`.
17. Write the preliminary pending test changes into `plan/test-update.md` with prefix `TEST-*`.
18. All `plan/*` files are numbered with prefix IDs.

## Numbering and Ordering Rules
1. Folder order for the repo is `intent/`, `plan/`, `design/`, `src/`, `tests/`, `dev_log/`, `dev_workflow/`, `skills/`, and `.codex/`.
2. File order within `intent/` is `product-intent.md`, `feedback.md`, and `gaps.md`.
3. File order within `plan/` is `design-update.md`, `code-update.md`, and `test-update.md`.
4. File order within `design/` is `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
5. File order within `dev_log/` is `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
6. Design, `src/`, and `tests/` stay human-readable and do not use prefix IDs as primary numbering.
7. Plan files and log entries use prefix IDs.
