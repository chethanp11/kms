# Project Agents Guide

## Purpose
Provide repo-level rules for Codex and other AI collaborators working in this template or in any project copied from it.

## Always-update contract
- When the user gives a new prompt that changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` first.
- Treat those two files as the always-current top-level contract for the repo.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Operating stance
- `intent/` is the highest-priority human source of truth.
- Design is the structured system-managed translation of intent.
- Code, tests, and artifacts are implementations of design and must stay aligned with both intent and design.
- `src/` may start empty; create scaffolding from design first, then create or refactor components inside `src/` as design requires.
- Acceptance criteria, tests, and evals are the release gate, not optional documentation.
- Logs capture what actually happened, including feedback, defects, deviations, and unresolved questions.
- Small, traceable changes are preferred over broad speculative edits.
- If intent or design is unclear, stop implementation and surface the ambiguity explicitly.

## Required read order before substantial work
Read the latest relevant artifacts in this order before modifying more than one file:
1. `README.md`
2. `intent/product-intent.md`
3. `intent/constraints-intent.md`
4. `intent/iteration-intent.md`
5. `intent/feedback-intent.md`
6. `design/build-scope.md`
7. `design/acceptance-criteria.md`
8. Relevant files from `design/`
9. `tests/design-traceability.md` and `tests/test-plan.md`
10. Latest entries in `dev_log/change-log.md`, `dev_log/issue-log.md`, and `dev_log/validation-log.md`
11. Relevant step file from `dev_workflow/`

## Required behavior for Codex
1. Always read `intent/` before starting a task.
2. Treat `intent/` as the starting point of every loop and the highest-priority human input.
3. Do not modify `intent/` unless the user explicitly asks for it.
4. Translate intent into structured design updates before coding.
5. Preserve the detail in `intent/*` when translating into `design/*`; do not compress away constraints, distinctions, or open questions that affect behavior.
6. Carry unresolved ambiguities into `design/open-questions.md` or the relevant design artifact instead of silently choosing a direction.
7. Make the design update explicit about what changed, what was deferred, and which `REQ-*`, `ACC-*`, `ARCH-*`, `API-*`, `DATA-*`, `AI-*`, `TEST-*`, or `EVAL-*` items were created or revised.
8. Update or add tests and eval mappings whenever behavior, contracts, or acceptance criteria change.
9. Stay inside the documented version and iteration boundary after intent has been interpreted into design.
10. Do not invent behavior that is not represented in intent, design, or acceptance artifacts.
11. Align implementation with both intent and design.
12. Always reflect meaningful intent changes into `design/*`, `tests/*`, and `dev_log/*`.
13. Update logs when the work changes reality:
   - `dev_log/change-log.md` for meaningful design, code, test, eval, or workflow updates
   - `dev_log/feedback-log.md` for routed human feedback and intent follow-up
   - `dev_log/deviations-log.md` for drift, exceptions, or temporary departures from intended design
   - `dev_log/issue-log.md` for discovered defects, gaps, or blockers
   - `dev_log/validation-log.md` for actual validation evidence
14. Keep all work traceable to `intent/*` sections and to `REQ-*`, `ACC-*`, `ARCH-*`, `API-*`, `DATA-*`, `AI-*`, `TEST-*`, `EVAL-*`, `FB-*`, or `DEV-*`.
15. If a requirement is unclear, log it as a design issue or open question instead of implementing a guess.
16. Treat manual feedback as first-class input; route it through `dev_log/feedback-log.md` and point back to `intent/feedback-intent.md` when it should influence future direction.

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
- `intent/*` defines what humans want.
- `REQ-*` should describe what the system must do.
- `ACC-*` should define how readiness is judged.
- `TEST-*` and `EVAL-*` should prove `ACC-*`.
- `ARCH-*`, `API-*`, `DATA-*`, and `AI-*` should constrain implementation details.
- `FB-*` should capture human feedback without losing source or action target.
- `DEV-*` should identify operational records such as issues, decisions, deviations, validation runs, and improvements.

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
2. `design/*`
3. `tests/*`
4. `src/*`

If implementation deviates from intent, flag it and log it. Do not silently normalize the drift.

## Template constraints
- Do not create product-specific business logic in this template repository.
- Keep this folder reusable by avoiding app-specific examples.
- Use bracketed placeholders such as `[Project Name]`, `[Version]`, and `[Primary Model]` where project-specific content belongs.
- Treat the copied project as a template baseline, not a finished application.

## Editing model
- Human edits by default: `intent/*`
- Human edits occasionally: `AGENTS.md`, `skills/*`
- System-managed through workflow: `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Source tree rule
- `src/README.md` is the project README for the copied application.
- `src/docs/` holds application purpose and functionality documentation.
- `src/` may be empty at the beginning; scaffold it from design, then refactor or expand it as design requires.

## Log ownership rule
- Every `dev_log/*` file is updated by `dev_workflow/*` prompts, not by ad hoc manual edits.
- Use workflow prompts to record changes, decisions, validations, deviations, issues, feedback routing, and closeout state.
- If a user wants a direct log update, translate it into the appropriate workflow step and then update the log through that step.
- Design changes produced by `dev_workflow/00-design-update.md` must be captured in `dev_log/*`, especially `dev_log/change-log.md` and `dev_log/decision-log.md`.

## Practical decision rules
- If intent changes, translate it into design first, then update tests, logs, and only then implementation.
- If behavior changes, update design, tests, and logs in the same pass.
- If only implementation changes and behavior does not, keep design stable and update tests or logs as needed.
- If validation fails, classify the failure before changing code.
- If a requested change exceeds the active scope, move it to backlog unless the design is updated first.
- Do not code directly from vague intent; structure it into design first.

## Logging and artifacts
- Every iteration must update `dev_log/` with what was implemented, what was validated, what was fixed, what gaps remain, and what should flow back into `intent/`.
- Logs must allow continuation by another agent without loss of context.
- If implementation exposes a design gap, record it before normalizing the code path.

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
- Tests and evals exist or are intentionally deferred with documented rationale.
- Validation evidence is recorded.
- Deviations, feedback, and next actions are logged, including what should be updated back in `intent/`.

## Behavior expectations
- Be precise, not verbose.
- Challenge weak or incomplete design.
- Do not skip steps in the loop.
- Do not generate large code blindly.
- Prefer structured progress over speed.
- Surface assumptions explicitly.
- Maintain engineering discipline at all times.
