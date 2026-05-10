# App Mode

App mode uses AppFlow to create or change the application.

## Activation

Root `AGENTS.md` routes to this file after reading `.devmode/mode.yaml`. When it contains:

```yaml
mode: app
```

use this file as the active operating entry point.

## Prompt Handling

Treat each user prompt as application intent. Convert the prompt into current-turn intent, then route the work through the AppFlow lifecycle.

## AppFlow Lifecycle

1. Create current-turn intent from the user prompt.
2. Read intent, project context, and stack guidance.
3. Create or update a scoped plan.
4. Update architecture, design, or contracts when behavior or structure changes.
5. Update validation expectations.
6. Implement in small, reversible steps.
7. Run targeted validation.
8. Fix failures at the correct layer.
9. Record factual evidence.
10. Surface gaps or follow-up work.
11. Review iteration and stop when scope is complete or blocked.

## Operating Rules

- Use `.codex/dev_workflow/*` as the workflow engine.
- Preserve the prompt → intent → plan → design → tests → implementation → validation → logs → gaps chain.
- Do not invent requirements beyond the prompt and repository source-of-truth artifacts.
- Ask only for genuinely blocking ambiguity, approval, or human-owned decisions.
- Validate changed behavior with the most targeted checks available.

---

# KMS Project Contract

This is the project-specific operating contract for KMS. The reusable AppFlow factory contract lives in `.codex/AGENTS.md`.

When adapting this repository pattern to a new application, `.devmode/app.md`, `.devmode/framework.md`, `.codex/project-context.md`, and `.codex/tech-stack.md` are the expected project-specific files to rewrite.

## Project Identity

KMS is a governed Knowledge Management System that turns immutable raw source material into finalized markdown knowledge under Knowledge Manager control.

The product publishes finalized knowledge to `/wiki` and exposes that knowledge through a separate read-only navigation layer.

## Instruction Precedence

1. System and developer instructions from the active Codex runtime.
2. `AGENTS.overrride.md` when present. If this exact file exists, do not use mode-selected `.devmode/*` or `.codex/*` instructions before executing the task.
3. `AGENTS.overrrideXX.md` when present. If this pattern exists, read the mode-selected `.devmode/*` entry point before executing the task.
4. `.codex/AGENTS.md` for reusable AppFlow factory behavior.
5. `.devmode/app.md` for KMS-specific application behavior.
6. `.codex/project-context.md` and `.codex/tech-stack.md`.
7. KMS artifacts in `intent/`, `plan/`, `design/`, `tests/`, `src/`, and `dev_log/`.

## KMS Source-of-Truth Chain

Use this order when KMS artifacts disagree:

1. User prompt and `.codex/state/current-intent.md` for the active turn.
2. `intent/*`
3. `plan/*`
4. `.codex/project-context.md`
5. `design/*`
6. `tests/*`
7. `src/*`
8. `dev_log/*`

Do not edit `intent/product-intent.md` or `intent/feedback-intent.md` unless explicitly asked. Use `intent/gaps.md` only for evidence-backed system-detected gaps.

## KMS Repository Map

- `intent/`: human-owned product intent, feedback, and system-detected gaps.
- `plan/`: current iteration workspace split into design, code, and test updates.
- `design/`: detailed KMS design layer.
- `src/`: implementation source and app scaffolding.
- `tests/`: validation plans, traceability, fixtures, and test suites.
- `dev_log/`: permanent execution and validation record.
- `.codex/dev_workflow/`: reusable AppFlow prompts and runbooks that execute the project loop.
- `.devmode/mode.yaml`: selects `app` or `framework` operating mode.
- `.devmode/app.md`: app-mode entry point; treats prompts as application intent and routes them through AppFlow.
- `.devmode/framework.md`: framework-mode entry point; treats prompts as-is and improves the framework directly.
- `.codex/`: reusable AppFlow factory plus KMS-specific `project-context.md` and `tech-stack.md`.

## KMS Folder Contracts

### `intent/`
- Human-owned inputs: `product-intent.md` and `feedback-intent.md`.
- System-managed gap record: `gaps.md`.
- Do not use this folder for implementation notes or silent reinterpretation.

### `plan/`
- Canonical files: `design-update.md`, `code-update.md`, and `test-update.md`.
- Use this folder to classify current iteration work into design, implementation, and validation.
- Keep plan entries traceable with project IDs such as `REQ-*`, `DEV-*`, and `TEST-*` when applicable.

### `design/`
- Canonical files: `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
- Keep design files complementary and aligned to `.codex/project-context.md`.
- Do not let code redefine behavior without an approved design update.

### `src/`
- Implement only behavior represented in intent, plan, project context, design, and validation expectations.
- Scaffold from design when implementation is empty or incomplete.
- Use `.codex/tech-stack.md` for stack and layout guidance.

### `tests/`
- Prove correctness criteria and changed behavior.
- Keep traceability in `tests/design-traceability.md`.
- Keep validation intent in `tests/test-plan.md`.

### `dev_log/`
- Canonical files: `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
- Record actual outcomes only after work and validation occur.
- Do not fabricate validation evidence.

### `.codex/dev_workflow/`
- Holds reusable AppFlow workflow prompts and runbooks.
- Preserve the intent → plan → design → tests → src → validation → logs → gaps loop.
- Do not use workflow prompts to bypass `.devmode/app.md` or `.codex/AGENTS.md`.

## Architecture Boundaries

- Raw source inputs are immutable upstream evidence, not finalized truth.
- KMI is the governed maintenance and approval surface.
- `/wiki` is the finalized markdown source of truth.
- Infopedia is read-only and must not mutate finalized knowledge.
- Metadata/runtime services support orchestration and auditability; they do not replace `/wiki`.
- AI agents may propose, compare, validate, and review, but they must not silently finalize truth.

## Product Development Rule

When working on KMS product behavior, follow:

user prompt → `.codex/state/current-intent.md` → `intent/*` → `plan/*` → `.codex/project-context.md` → `design/*` → `tests/*` → `src/*` → validation → `dev_log/*` → `intent/gaps.md`.

Implementation must follow approved plan/design/test artifacts. Code must not invent requirements.

## Required Read Order Before Substantial KMS Work

1. `.devmode/mode.yaml`, then `.devmode/app.md` or `.devmode/framework.md` as selected
2. `.codex/AGENTS.md`
3. `.codex/state/current-intent.md` when present
4. `.codex/project-context.md`
5. `.codex/tech-stack.md`
6. `intent/product-intent.md`
7. `intent/feedback-intent.md`
8. `intent/gaps.md` when present
9. current `plan/*`
10. relevant `design/*`
11. `tests/design-traceability.md` and `tests/test-plan.md`
12. relevant `dev_log/*`
13. relevant `.codex/dev_workflow/*` step file when using the AppFlow workflow

## Production Deployment Boundary

Only `src/` is intended to become production runtime code in this repository.

`intent/`, `plan/`, `design/`, `tests/`, `dev_log/`, and `.codex/` are engineering control-plane artifacts. They guide development, validation, traceability, and governance but are not production deployment artifacts.

## KMS Traceability Rules

- `intent/*` defines human intent and feedback.
- `plan/*` defines active iteration scope.
- `.codex/project-context.md` defines compact high-level KMS design and operating model.
- `design/ux-flows.md` defines user experience.
- `design/system-design.md` defines system behavior.
- `design/architecture.md` defines structure and boundaries.
- `design/acceptance-criteria.md` defines correctness.
- `tests/*` defines proof.
- `dev_log/*` records actual work and validation evidence.

## Repository Improvement Rule

When improving the reusable AppFlow factory, keep `.codex/` project-agnostic except:

- `.codex/project-context.md`
- `.codex/tech-stack.md`

Project-specific workflow guidance belongs in `.devmode/app.md`, not in reusable factory files.

## Validation

- For AppFlow factory changes: run `python .codex/tools/validate_codex_contract.py` and `git diff --check`.
- For KMS documentation/workflow changes: also review affected KMS artifacts for source-of-truth alignment.
- For KMS product implementation changes: run the targeted validation from `.codex/tech-stack.md` and `tests/test-plan.md`.

## Stop Conditions

Stop and surface the issue when:

- KMS source-of-truth artifacts conflict and cannot be safely reconciled
- validation fails and the root cause is not understood
- a change would bypass KMS governance or publication boundaries
- a human-owned intent decision is missing
- a requested action would make reusable `.codex` files project-specific
