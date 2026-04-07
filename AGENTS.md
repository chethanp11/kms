# Project Agents Guide

## Purpose
Provide repo-level rules for Codex and other AI collaborators working in this template or in any project copied from it.

## Always-update contract
- When the user gives a new prompt that changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` first.
- Treat those two files as the always-current top-level contract for the repo.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Operating stance
1. `intent/` is the highest-priority human source of truth.
2. The canonical human-owned intent set is `intent/product-intent.md`, `intent/feedback.md`, and the system-generated `intent/gaps.md` view when present.
3. This repository currently keeps `intent/feedback-intent.md` as the active feedback file during migration, but new guidance should treat `intent/feedback.md` as the target shape.
4. `plan/` is the interpreted action layer that buckets the latest intent into design, code, and test work before downstream edits happen.
5. `design/` contains only `design/system-design.md`, `design/architecture.md`, `design/acceptance-criteria.md`, and `design/ux-flows.md`.
6. The four design files follow the combined master draft structure: numbered major sections, numbered subsections, and plain headings for content blocks.
7. `design/system-design.md` covers the system-level behavior and operating model.
8. `design/architecture.md` covers the structural layout, components, services, and boundaries.
9. `design/ux-flows.md` covers user journeys, preconditions, steps, edge cases, and failure paths.
10. `design/acceptance-criteria.md` covers deterministic, testable correctness conditions.
11. Design files do not use `REQ-*`, `ACC-*`, `ARCH-*`, `TEST-*`, `FB-*`, or `DEV-*` labels as in-document numbering. Those prefixes are reserved for traceability in plan, tests, and log artifacts.
12. Code, tests, and artifacts are implementations of design and must stay aligned with both intent and design.
13. `src/` may start empty; create scaffolding from design first, then create or refactor components inside `src/` as design requires.
14. Acceptance criteria, tests, and manual review are the release gate, not optional documentation.
15. `dev_log/` is limited to `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
16. Logs capture what actually happened, including feedback, defects, unresolved questions, and validation evidence.
17. Small, traceable changes are preferred over broad speculative edits.
18. If intent or design is unclear, stop implementation and surface the ambiguity explicitly.

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

## Skill usage during development
- Use a skill whenever the task clearly matches its purpose, especially for design update, traceability, architecture review, AI eval review, feedback triage, prompt contract review, release closeout, or test repair.
- Before using a skill, open its `SKILL.md` and follow only the workflow it defines.
- Treat skills as operational guidance, not background reading. Apply them in the current task when they match the work.
- If more than one skill applies, use the minimal set that covers the task. Do not stack overlapping skills unless the work really needs it.
- Do not use a skill outside its scope just because it seems related.
- If a skill conflicts with `intent/`, `AGENTS.md`, or the active design, stop and resolve the higher-priority artifact first.
- When a skill produces a result that changes design, tests, validation, or logs, update the affected artifacts in the same iteration.

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
