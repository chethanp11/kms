# Codex Project Context

AgentAIdev is a design-driven, closed-loop development system that converts approved intent and design documents into production-quality applications through structured, iterative execution using coding models.

## Always-update contract
- When a new user prompt changes workflow, precedence, ownership, or operating rules, update this file and `AGENTS.md` first.
- Treat these two files as the current top-level operating contract for the repository.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Core principle
1. `intent/` is the highest-priority human input.
2. The canonical intent set is `intent/product-intent.md`, `intent/feedback.md`, and the system-generated `intent/gaps.md` view when present.
3. This repository currently keeps `intent/feedback-intent.md` as the active feedback file during migration, but new guidance should target the canonical file names above.
4. `plan/` is the interpreted action layer that splits the latest intent into design, code, and test work.
5. `design/` contains only `design/system-design.md`, `design/architecture.md`, `design/acceptance-criteria.md`, and `design/ux-flows.md`.
6. The four design files follow the combined master draft structure: numbered major sections, numbered subsections, and plain content headings.
7. `design/system-design.md` covers system behavior and operating model.
8. `design/architecture.md` covers structural layout, components, services, and boundaries.
9. `design/ux-flows.md` covers user journeys, preconditions, steps, edge cases, and failure paths.
10. `design/acceptance-criteria.md` covers deterministic correctness conditions.
11. Design files do not use `REQ-*`, `ACC-*`, `ARCH-*`, `TEST-*`, `FB-*`, or `DEV-*` labels as in-document numbering; those prefixes are reserved for traceability artifacts in plan, tests, and logs.
12. `src/`, `tests/`, and `dev_log/` are implementations, proofs, and records of design.
13. The system continuously enforces alignment between intent, design, implementation, and validation.

## Operating model
Run work in this loop:
1. Intent grounding
2. UX flow grounding
3. System design grounding
4. Acceptance criteria grounding
5. Plan generation
6. Implementation
7. Test creation and execution
8. Review
9. Fix and refine
10. Logging and traceability
11. Alignment check across intent, plan, design, code, and tests

Repeat the loop until the scoped feature or system is complete and stable.

## Repository contract
1. `intent/` holds human-editable product direction and feedback plus system-generated gap signals when present.
2. `plan/` holds the interpreted work buckets for design, code, and test changes derived from the latest intent and current repository state.
3. `design/` holds the four system-managed design files: system design, architecture, acceptance criteria, and user flows.
4. `src/README.md` is the copied project's README.
5. `src/docs/` holds application purpose and functionality documentation.
6. `src/` holds application code and implementation scaffolding.
7. `tests/` holds unit, integration, e2e, regression, eval, and traceability artifacts.
8. `dev_log/` holds `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
9. `dev_workflow/` holds reusable prompts, runbooks, and execution templates that update `dev_log/` as part of the loop.
10. `.codex/` holds repo-local context and command references.

## Precedence when artifacts disagree
1. `intent/*`
2. `plan/*`
3. `design/*`
4. `tests/*`
5. `src/*`
6. `dev_log/*`
7. `dev_workflow/*`

## Execution rules
1. Always start from `intent/` and translate it into `plan/`, then design, before coding.
2. Work in scoped iterations and avoid uncontrolled changes.
3. `src/` may start empty; create scaffolding from design first, then create or refactor components as design requires.
4. Put the copied project README in `src/README.md` and update `src/docs/` after code changes so the documentation reflects the implemented behavior.
5. Maintain traceability from every implementation and test back to intent, plan, and design.
6. Never assume correctness because code looks reasonable.
7. Treat design as evolving when implementation exposes gaps, but do not silently diverge from it.
8. Prefer modular, production-quality code with explicit contracts, error handling, and extensibility.

## Testing discipline
- Create tests for implemented behavior.
- Cover happy paths, edge cases, and failure scenarios.
- Validate against design intent, not just local code behavior.
- Flag untestable or unclear design areas instead of guessing.

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

## Logging and artifacts
- Update `dev_log/` every iteration with what changed, what was validated, what failed, what was fixed, and what remains.
- Make the logs sufficient for another agent to continue without context loss.
- Treat `dev_log/*` as workflow-managed artifacts produced by `dev_workflow/*` prompts.
- Design changes produced by `dev_workflow/00-design-update.md` must be captured in `dev_log/design-update-log.md`.

## Alignment enforcement
- Verify intent to design alignment.
- Verify design to code alignment.
- Verify code to tests alignment.
- Verify tests to expected behavior alignment.
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

## Definition of done
A feature or system is complete only when:
- implementation matches design or an approved updated design
- tests validate core and edge behavior
- review passes without major gaps
- logs capture decisions and changes
- no unresolved critical issues remain

## Behavior expectations
- Be precise, not verbose.
- Challenge weak or incomplete design.
- Do not skip steps in the loop.
- Do not generate large code blindly.
- Prefer structured progress over speed.
- Surface assumptions explicitly.
- Maintain engineering discipline at all times.

AgentAIdev is not a code generator.
It is a controlled development system that produces reliable, auditable, production-grade software through iterative refinement.
