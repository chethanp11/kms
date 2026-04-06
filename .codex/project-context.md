# Codex Project Context

AgentAIdev is a design-driven, closed-loop development system that converts approved intent and design documents into production-quality applications through structured, iterative execution using coding models.

## Always-update contract
- When a new user prompt changes workflow, precedence, ownership, or operating rules, update this file and `AGENTS.md` first.
- Treat these two files as the current top-level operating contract for the repository.
- Then propagate any resulting rule changes into design, tests, logs, or workflow files as needed.

## Core principle
- `intent/` is the highest-priority human input.
- `design/` is the structured source of truth for implementation.
- `src/`, `tests/`, and `dev_log/` are implementations, proofs, and records of design.
- The system continuously enforces alignment between intent, design, implementation, and validation.

## Operating model
Run work in this loop:
1. Design grounding
2. Iteration planning
3. Implementation
4. Test creation and execution
5. Review
6. Fix and refine
7. Logging and traceability
8. Alignment check across intent, design, code, and tests

Repeat the loop until the scoped feature or system is complete and stable.

## Repository contract
- `intent/` holds human-editable product direction, constraints, feedback, and iteration overrides.
- `design/` holds system-managed requirements, architecture, behavior, flows, contracts, and acceptance criteria.
- `src/README.md` is the copied project's README.
- `src/docs/` holds application purpose and functionality documentation.
- `src/` holds application code and implementation scaffolding.
- `tests/` holds unit, integration, e2e, regression, eval, and traceability artifacts.
- `dev_log/` holds logs, decisions, issues, validation evidence, deviations, feedback routing, and remaining work.
- `dev_workflow/` holds reusable prompts, runbooks, and execution templates that update `dev_log/` as part of the loop.
- `.codex/` holds repo-local context and command references.

## Precedence when artifacts disagree
1. `intent/*`
2. `design/build-scope.md`
3. `design/*`
4. `tests/*`
5. `src/*`
6. `dev_log/*`
7. `dev_workflow/*`

## Execution rules
1. Always start from `intent/` and translate it into design before coding.
2. Work in scoped iterations and avoid uncontrolled changes.
3. `src/` may start empty; create scaffolding from design first, then create or refactor components as design requires.
4. Put the copied project README in `src/README.md` and application-purpose documentation in `src/docs/`.
5. Maintain traceability from every implementation and test back to intent and design.
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
- Design changes produced by `dev_workflow/00-design-update.md` must be captured in `dev_log/*`, especially `dev_log/change-log.md` and `dev_log/decision-log.md`.

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
