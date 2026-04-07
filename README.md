# KMS

`KMS` is a governed knowledge maintenance and publishing system. It transforms immutable raw source material into finalized markdown knowledge under Knowledge Manager control, then exposes that knowledge through a separate read-only navigation layer.

## What KMS is for
- Preserving institutional knowledge in durable markdown form
- Maintaining a single finalized knowledge substrate under governance
- Keeping source intake, publication, and consumption separate
- Supporting human readers and downstream AI systems with stable, curated knowledge

## Operating model
1. Humans describe direction in `intent/`.
2. Codex converts the latest intent into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
3. Codex translates the plan into `design/`, `tests/`, and `dev_log/`.
4. KMI governs source maintenance and publication into `/wiki`.
5. Infopedia provides read-only navigation over finalized knowledge.
6. Downstream AI systems consume finalized markdown as governed context.

## First-use checklist
1. Populate `intent/product-intent.md` and `intent/feedback-intent.md`.
2. Run the plan step to split the latest intent into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
3. Keep `design/` aligned with the current plan and iteration boundary.
4. Update `tests/design-traceability.md` and `tests/test-plan.md` whenever acceptance scope changes.
5. Record meaningful design, validation, and workflow changes in `dev_log/`.
6. Update `src/README.md` and `src/docs/` when the application purpose or functionality changes.

## Required ID scheme
Use these IDs consistently across design, tests, logs, and reviews:

| Prefix | Meaning |
| --- | --- |
| `REQ-###` | Product or system requirement |
| `ACC-###` | Acceptance criterion |
| `ARCH-###` | Architecture decision or constraint |
| `TEST-###` | Test case or test suite identifier |
| `FB-###` | Manual feedback item |
| `DEV-###` | Operational log item, issue, decision, deviation, or improvement |

## Folder map
- `intent/`: the single human-editable source of truth for product direction and feedback. There are no separate constraints or iteration intent files.
- `plan/`: the interpreted work queue derived from the latest intent, split into design, code, and test update buckets.
- `design/`: system-managed translation of intent into four files only: system design, architecture, acceptance criteria, and user flows.
- `src/README.md`: the project README for the copied application.
- `src/docs/`: application purpose and functionality docs for the copied application.
- `src/`: system-managed implementation space for app entrypoints, agents, workflows, services, tools, schemas, config, and utilities.
- `tests/`: system-managed validation plan, traceability matrix, smoke checklist, and test directories.
- `dev_log/`: system-managed operational memory updated by `dev_workflow/*` prompts for changes, issues, validation evidence, feedback routing, decisions, deviations, backlog, and release readiness.
- `dev_workflow/`: system-managed closed-loop operating prompts that update `dev_log/*` as part of the iteration.
- `.codex/`: repo-local context and command references for Codex.
- `skills/`: reusable review and workflow skills that remain neutral after the template is copied.

## Human vs system editing
- Human-edited by default: `intent/*`
- Occasionally human-edited: `AGENTS.md`, `skills/*`
- System-managed through workflow: `plan/*`, `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Intent-driven flow
`intent/` drives the rest of the repository in this order:

`intent -> plan -> design -> src/tests -> validation -> dev_log -> feedback -> intent update -> next iteration`

That means:
- Human intent becomes structured design.
- Human intent is first bucketed into plan files for design, code, and test work.
- Design drives implementation and validation.
- Validation and review create logs and feedback.
- Feedback is summarized back into `intent/feedback-intent.md`, and durable direction updates are reflected in `intent/product-intent.md` for the next loop.

## Closed-loop workflow
1. `plan-update.md`: compare the latest intent with design, code, and tests, then write `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
2. `00-design-update.md`: translate `plan/design-update.md` and `dev_log/` into concrete design updates.
3. `01-baseline-sync.md`: confirm the current design state, scope, and documentation alignment.
4. `02-iteration-scope.md`: interpret the plan and logs into exact in-scope IDs and the tests or manual reviews that will prove them.
5. `03-implementation.md`: implement only already-designed behavior and update impacted artifacts.
6. `04-self-review.md`: review the diff against scope, failure handling, and traceability before formal validation.
7. `05-validation.md`: run the required checks and record evidence, failures, and classifications.
8. `06-fix-loop.md`: fix root causes, re-run required checks, and update logs.
9. `07-design-audit.md`: confirm there is no undocumented behavior or silent drift from intent, plan, or design.
10. `08-closeout.md`: update status, release notes, next priorities, and recommended intent updates.

## Design-to-delivery rule
Do not start implementation in a copied project until these are true:
- The human intent files in `intent/` are populated enough to interpret.
- The latest intent has been bucketed into `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
- The four design files exist and are up to date.
- Acceptance criteria are mapped to tests or validations in `tests/design-traceability.md`.
- Real project commands exist in `.codex/commands.md`.

## `src/` startup rule
- `src/` may begin empty in a copied project.
- First create scaffolding from design.
- If components already exist, refactor inside `src/` as required by the current design.
- Put the copied project README in `src/README.md`.
- Put application purpose and functionality documentation in `src/docs/` after code changes so the docs stay synchronized with implementation.
- Keep `src/` aligned with the design layer, not with ad hoc implementation shortcuts.

## What a good copied project looks like
- A new contributor can tell what the human wants by reading `intent/` first.
- Codex can translate intent into plan and then design without inventing requirements.
- Every material behavior change is linked back to intent and plan, then to `REQ-*`, `ACC-*`, `TEST-*`, or documented manual review.
- Manual review feedback is captured operationally in `dev_log/feedback-log.md` and then routed back into `intent/feedback-intent.md`.
