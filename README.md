# KMS

`KMS` is a governed knowledge maintenance and publishing system. It transforms immutable raw source material into finalized markdown knowledge under Knowledge Manager control, then exposes that knowledge through a separate read-only navigation layer.

## What KMS is for
- Preserving institutional knowledge in durable markdown form
- Maintaining a single finalized knowledge substrate under governance
- Keeping source intake, publication, and consumption separate
- Supporting human readers and downstream AI systems with stable, curated knowledge

## Operating model
1. Humans describe direction in `intent/`.
2. Codex translates intent into `design/`, `tests/`, and `dev_log/`.
3. KMI governs source maintenance and publication into `/wiki`.
4. Infopedia provides read-only navigation over finalized knowledge.
5. Downstream AI systems consume finalized markdown as governed context.

## First-use checklist
1. Populate `intent/product-intent.md`, `intent/constraints-intent.md`, `intent/iteration-intent.md`, and `intent/feedback-intent.md`.
2. Keep `design/` aligned with the current KMS intent and iteration boundary.
3. Update `tests/design-traceability.md` and `tests/test-plan.md` whenever acceptance scope changes.
4. Record meaningful design, validation, and workflow changes in `dev_log/`.
5. Update `src/README.md` and `src/docs/` when the application purpose or functionality changes.

## Required ID scheme
Use these IDs consistently across design, tests, logs, and reviews:

| Prefix | Meaning |
| --- | --- |
| `REQ-###` | Product or system requirement |
| `ACC-###` | Acceptance criterion |
| `ARCH-###` | Architecture decision or constraint |
| `API-###` | External or internal interface contract |
| `DATA-###` | Data model or schema definition |
| `AI-###` | AI behavior rule, prompt contract, or guardrail |
| `TEST-###` | Test case or test suite identifier |
| `EVAL-###` | Evaluation scenario or rubric item |
| `FB-###` | Manual feedback item |
| `DEV-###` | Operational log item, issue, decision, deviation, or improvement |

## Folder map
- `intent/`: the single human-editable source of truth for product idea, feedback, constraints, and next-iteration direction.
- `design/`: system-managed translation of intent into structured product and technical design.
- `design/versions/`: version briefs that define what each release stage is supposed to achieve.
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
- System-managed through workflow: `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Intent-driven flow
`intent/` drives the rest of the repository in this order:

`intent -> design -> src/tests -> validation -> dev_log -> feedback -> intent update -> next iteration`

That means:
- Human intent becomes structured design.
- Design drives implementation and validation.
- Validation and review create logs and feedback.
- Feedback is summarized back into `intent/feedback-intent.md` and `intent/iteration-intent.md` for the next loop.

## Closed-loop workflow
1. `00-design-update.md`: translate `intent/` and `dev_log/` into concrete design updates.
2. `01-baseline-sync.md`: confirm the current design state, scope, and documentation alignment.
3. `02-iteration-scope.md`: interpret intent and logs into exact in-scope IDs and the tests/evals that will prove them.
4. `03-implementation.md`: implement only already-designed behavior and update impacted artifacts.
5. `04-self-review.md`: review the diff against scope, failure handling, and traceability before formal validation.
6. `05-validation.md`: run the required checks and record evidence, failures, and classifications.
7. `06-fix-loop.md`: fix root causes, re-run required checks, and update logs.
8. `07-design-audit.md`: confirm there is no undocumented behavior or silent drift from intent or design.
9. `08-closeout.md`: update status, release notes, next priorities, and recommended intent updates.

## Design-to-delivery rule
Do not start implementation in a copied project until these are true:
- The human intent files in `intent/` are populated enough to interpret.
- The version target and iteration boundary are documented in `design/build-scope.md`.
- The AI behavior contract exists in `design/ai-behavior-spec.md`.
- Acceptance criteria are mapped to tests or evals in `tests/design-traceability.md`.
- Real project commands exist in `.codex/commands.md`.

## `src/` startup rule
- `src/` may begin empty in a copied project.
- First create scaffolding from design.
- If components already exist, refactor inside `src/` as required by the current design.
- Put the copied project README in `src/README.md`.
- Put application purpose and functionality documentation in `src/docs/`.
- Keep `src/` aligned with the design layer, not with ad hoc implementation shortcuts.

## What a good copied project looks like
- A new contributor can tell what the human wants by reading `intent/` first.
- Codex can translate intent into design without inventing requirements.
- Every material behavior change is linked back to intent, then to `REQ-*`, `ACC-*`, `TEST-*`, or `EVAL-*`.
- Manual review feedback is captured operationally in `dev_log/feedback-log.md` and then routed back into `intent/feedback-intent.md`.
