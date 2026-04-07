# KMS

`KMS` is a governed knowledge maintenance and publishing system. It transforms immutable raw source material into finalized markdown knowledge under Knowledge Manager control, then exposes that knowledge through a separate read-only navigation layer.

## What KMS is for
- Preserving institutional knowledge in durable markdown form
- Maintaining a single finalized knowledge substrate under governance
- Keeping source intake, publication, and consumption separate
- Supporting human readers and downstream AI systems with stable, curated knowledge

## Repo structure
1. `intent/` is the human + system owned requirements layer for what and why.
2. `plan/` is the temporary iteration workspace for what needs to change right now.
3. `design/` is the system truth layer for how the product should work.
4. `src/` is the implementation layer for what actually exists in code.
5. `tests/` is the validation layer for how correctness is proven.
6. `dev_log/` is the permanent execution record for what actually happened.

## Canonical files
### `intent/`
1. `product-intent.md`: human-edited end-to-end product intent.
2. `feedback.md`: human-edited feedback input file.
3. `gaps.md`: system-generated gap intake derived from logs and validation.
4. Migration note: this repository currently keeps `feedback-intent.md` as the active feedback file until the new naming is fully rolled out.

### `plan/`
1. `design-update.md`: pending design deltas.
2. `code-update.md`: pending code deltas aligned to the current design.
3. `test-update.md`: pending test and validation deltas.

### `design/`
1. `system-design.md`
2. `architecture.md`
3. `acceptance-criteria.md`
4. `ux-flows.md`
5. The four design files follow the combined master draft structure: numbered major sections, numbered subsections, and plain headings for content blocks.
6. The design files do not use `REQ-*`, `ACC-*`, `ARCH-*`, `TEST-*`, `FB-*`, or `DEV-*` labels as in-document numbering.

### `dev_log/`
1. `design-update-log.md`
2. `code-update-log.md`
3. `test-update-log.md`
4. `validation-results.md`

## Operating model
1. Humans describe direction in `intent/`.
2. Codex reconciles the latest intent with `design/ux-flows.md`, `design/acceptance-criteria.md`, `design/system-design.md`, `design/architecture.md`, and the active logs.
3. Codex updates `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
4. Codex translates the plan into `design/`, `tests/`, `src/`, and `dev_log/` through the workflow prompts.
5. KMI governs source maintenance and publication into `/wiki`.
6. Infopedia provides read-only navigation over finalized knowledge.
7. Downstream AI systems consume finalized markdown as governed context.

## First-use checklist
1. Populate `intent/product-intent.md` and the active feedback record in `intent/`.
2. Let `plan-update.md` split the latest intent into design, code, and test updates.
3. Keep `design/ux-flows.md` aligned with the current user journeys.
4. Keep `design/acceptance-criteria.md` aligned with the current correctness expectations.
5. Keep `design/system-design.md` aligned with behavior and `design/architecture.md` aligned with structure.
6. Update `tests/design-traceability.md` and `tests/test-plan.md` whenever acceptance scope changes.
7. Record meaningful design, validation, and workflow changes in the four `dev_log/` files.
8. Update `src/README.md` and `src/docs/` when the application purpose or functionality changes.

## Required ID scheme
Use these IDs consistently across plan files, tests, logs, and reviews:

| Prefix | Meaning |
| --- | --- |
| `REQ-###` | Product or system requirement |
| `ACC-###` | Acceptance criterion |
| `ARCH-###` | Architecture decision or constraint |
| `TEST-###` | Test case or test suite identifier |
| `FB-###` | Manual feedback item |
| `DEV-###` | Operational log item, issue, decision, deviation, validation result, or improvement |

## Folder map
1. `intent/`: the human + system owned requirements layer. Product intent is human-edited; feedback and gap intake are routed here.
2. `plan/`: the temporary iteration workspace derived from the latest intent and current repository state.
3. `design/`: system-managed translation of intent into the four live design files.
4. `src/README.md`: the project README for the copied application.
5. `src/docs/`: application purpose and functionality docs for the copied application.
6. `src/`: system-managed implementation space for app entrypoints, agents, workflows, services, tools, schemas, config, and utilities.
7. `tests/`: system-managed validation plan, traceability matrix, smoke checklist, and test directories.
8. `dev_log/`: system-managed operational memory updated by `dev_workflow/*` prompts for design, code, test, and validation records.
9. `dev_workflow/`: system-managed closed-loop operating prompts that update `dev_log/*` as part of the iteration.
10. `.codex/`: repo-local context and command references for Codex.
11. `skills/`: reusable review and workflow skills that remain neutral after the template is copied.

## Human vs system editing
- Human-edited by default: `intent/*`
- Occasionally human-edited: `AGENTS.md`, `skills/*`
- System-managed through workflow: `plan/*`, `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Intent-driven flow
`intent/` drives the rest of the repository in this order:

`intent -> ux-flows -> system-design -> acceptance-criteria -> plan -> src/tests -> validation -> dev_log -> feedback routing -> intent update -> next iteration`

That means:
- Human intent becomes structured design.
- Human intent is first expressed as UX flows, then system behavior, then acceptance criteria.
- Human intent is then bucketed into plan files for design, code, and test work.
- Design drives implementation and validation.
- Validation and review create logs and feedback.
- Feedback is summarized back into the active feedback record in `intent/`, and durable direction updates are reflected in `intent/product-intent.md` for the next loop.

## Closed-loop workflow
1. `plan-update.md`: compare the latest intent with design, code, tests, and logs, then write `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
2. `00-design-update.md`: translate `plan/design-update.md` and the active `dev_log/` files into concrete design updates.
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
- Manual review feedback is captured operationally in `dev_log/` and then routed back into the active feedback record in `intent/`.
