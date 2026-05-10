# AppFlow Contract

AppFlow is a portable, prompt-driven application-development workflow. It turns human intent into governed repository changes by moving work through explicit artifacts instead of relying on chat memory or ad hoc edits.

## Purpose

- Convert every prompt into a structured engineering workflow.
- Keep development aligned to intent, plan, architecture/design, validation, implementation, and evidence.
- Make work reproducible for Codex CLI, VS Code Codex, Codex Desktop, and future agents.
- Support long-horizon autonomous development without uncontrolled autonomy.

## Automatic Routing

AppFlow is the default route for every development prompt. The user should not need to say "run the workflow."

For each prompt, the agent should:

1. infer the task type
2. enter `.codex/dev_workflow/00-create-intent.md`
3. proceed through the 11-step lifecycle until the requested scope is complete, blocked, or explicitly bounded by the user
4. use `.codex/agents/`, `.codex/skills/`, `.codex/orchestration/`, `.codex/rules/`, and `.codex/tools/` as supporting infrastructure
5. validate and report the closeout state

## Portable Source-of-Truth Order

Adapt this order through the project-specific root `AGENTS.md` and `.codex/project-context.md`:

1. User prompt and current-turn intent.
2. Human intent and feedback.
3. Active plan or backlog item.
4. Project context.
5. Architecture, design, contracts, and correctness criteria.
6. Validation plan, tests, evals, and review checklists.
7. Implementation.
8. Logs, validation evidence, gaps, and decisions.

## AppFlow Lifecycle

1. Create current-turn intent from the user prompt.
2. Read intent and project context.
3. Create or update a scoped plan.
4. Update architecture/design/contracts when behavior or structure changes.
5. Update validation expectations.
6. Implement in small, reversible steps.
7. Run targeted validation.
8. Fix failures at the correct layer.
9. Record factual evidence.
10. Surface gaps or follow-up work.
11. Review iteration and stop.

## Prompt Operating Rules

Each AppFlow prompt should:

- state the lifecycle phase
- name required inputs
- define allowed writes
- preserve traceability between intent, design, validation, and implementation
- stop at phase exit criteria
- record real outcomes only after validation or explicit review

## Project Boundary Rules

Project-specific behavior belongs outside the reusable factory:

- domain identity and architecture boundaries: root `AGENTS.md`
- compact project map: `.codex/project-context.md`
- stack and commands: `.codex/tech-stack.md`
- detailed product design: project `design/`, `docs/`, `architecture/`, or equivalent
- implementation: project source tree
- tests/evals: project validation tree
- evidence/logs: project logs or development records

## Minimum Portable Setup

- `.codex/AGENTS.md`: reusable factory operating contract
- `.codex/appflow.md`: lifecycle contract
- `.codex/dev_workflow/*`: canonical 11-step prompt-to-change workflow
- `.codex/project-context.md`: project-specific context extension
- `.codex/tech-stack.md`: project-specific stack extension
- `.codex/agents/*`: bounded role contracts
- `.codex/skills/*/SKILL.md`: reusable procedures
- `.codex/orchestration/*`: staged execution and HITL checkpoints
- `.codex/context/*`: context engineering templates
- `.codex/memory/*`: structured memory templates
- `.codex/rules/*`: reusable operational rules
- `.codex/prompts/*`: small prompt templates
- `.codex/tools/*`: deterministic support scripts

## Validation Expectations

For factory-only changes:

- confirm required files exist
- confirm reusable files are project-agnostic
- run `python .codex/tools/validate_codex_contract.py`
- run `git diff --check`

For project behavior changes, use the project-specific validation commands in `.codex/tech-stack.md` and the project validation plan.
