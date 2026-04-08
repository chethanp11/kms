# KMS

`KMS` is a governed knowledge maintenance and publishing system. It transforms immutable raw source material into finalized markdown knowledge under Knowledge Manager control, then exposes that knowledge through a separate read-only navigation layer.

## What KMS is for
- Preserving institutional knowledge in durable markdown form
- Maintaining a single finalized knowledge substrate under governance
- Keeping source intake, publication, and consumption separate
- Supporting human readers and downstream AI systems with stable, curated knowledge

## Repo structure
1. `intent/` is the starting point of requirements.
2. `plan/` is the temporary working area for the current iteration.
3. `design/` is the current source of design truth.
4. `src/` is the implementation layer.
5. `tests/` is the validation layer.
6. `dev_log/` is the permanent archive of what was actually updated and validated.
7. `dev_workflow/` holds the prompts that drive the closed loop.
8. `skills/` holds reusable scoped workflows.
9. `.codex/` holds local context and command references.

## Folder and file map
1. `intent/`
   1. `product-intent.md`
   2. `feedback.md`
   3. `gaps.md`
   4. `product-intent.md` is manually updated with the latest product goals, scope, user flows, constraints, and expected behavior.
   5. `feedback.md` is manually updated with new findings from manual review, testing, usage feedback, bug observations, or scope changes.
   6. `gaps.md` is updated by a prompt that reviews `dev_log/*` and records system-detected gaps.
   7. `product-intent.md` and `feedback.md` are the only human-edited operational inputs.
   8. `gaps.md` is the system-edited operational input.
2. `plan/`
   1. `design-update.md`
   2. `code-update.md`
   3. `test-update.md`
   4. `plan/` is the temporary working area for the current iteration only.
   5. All plan entries use prefix IDs such as `REQ-*`, `DEV-*`, and `TEST-*`.
   6. `design-update.md` captures pending design changes.
   7. `code-update.md` captures preliminary pending code changes.
   8. `test-update.md` captures preliminary pending test changes.
   9. Keep plan items scoped to the current iteration and keep open questions visible.
3. `design/`
   1. `system-design.md`
   2. `architecture.md`
   3. `acceptance-criteria.md`
   4. `ux-flows.md`
   5. `system-design.md` is the system-level behavior and operating model.
   6. `architecture.md` is the structural layout, services, interfaces, data flow, and boundaries.
   7. `ux-flows.md` is the user journey, steps, edge cases, and failure path view.
   8. `acceptance-criteria.md` is the deterministic definition of correct behavior.
   9. The four design files are plain human-readable markdown and do not use prefix IDs as in-document numbering.
   10. Keep the four files complementary rather than repetitive.
4. `src/`
   1. `README.md`
   2. `docs/`
   3. Application source code and supporting implementation files.
   4. If `src/` is empty on the first implementation pass, scaffold it from design first.
   5. Keep implementation aligned with the approved design.
   6. Do not keep design drafts or plan notes here.
5. `tests/`
   1. `design-traceability.md`
   2. `test-plan.md`
   3. Test suites and validation assets that prove the design.
   4. If `tests/` is empty on the first test pass, scaffold it from design first.
   5. Keep tests tied to acceptance criteria and expected behavior.
   6. Do not invent tests without design linkage.
6. `dev_log/`
   1. `design-update-log.md`
   2. `code-update-log.md`
   3. `test-update-log.md`
   4. `validation-results.md`
   5. `dev_log/` is the permanent execution record.
   6. Log entries use prefix IDs to show what was implemented and validated.
   7. Update logs through the workflow prompts after the corresponding work has actually occurred.
7. `dev_workflow/`
   1. Workflow prompts and runbooks that drive the closed loop.
   2. Use these prompts to update design, code, tests, and logs in the correct order.
   3. Do not bypass the workflow with ad hoc updates.
8. `skills/`
   1. Reusable scoped workflows for matched tasks.
   2. Open `SKILL.md` first and use the minimal matching skill.
   3. Do not use a skill outside its scope.
9. `.codex/`
   1. Repo-local context and command references.
   2. Keep this folder compact and operational.
   3. Do not replace the top-level contract here.

## Operating flow
1. Humans describe direction in `intent/product-intent.md` and `intent/feedback.md`.
2. A prompt reviews `dev_log/*` and updates `intent/gaps.md`.
3. `design/` remains the current source of design truth.
4. `plan/` captures the current iteration only.
5. `src/` contains the implementation.
6. `tests/` proves the acceptance criteria.
7. `dev_log/` preserves what actually changed and what was validated.
8. `dev_workflow/` sequences the iteration prompts.
9. Design files remain plain markdown and do not use prefix IDs as primary numbering.
10. Plan files and log entries use prefix IDs to show what was implemented where.
11. KMI governs source maintenance and publication into `/wiki`.
12. Infopedia provides read-only navigation over finalized knowledge.
13. Downstream AI systems consume finalized markdown as governed context.

## First-use checklist
1. Populate `intent/product-intent.md` and `intent/feedback.md`.
2. Let the plan workflow split the latest intent into design, code, and test updates.
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

Plan files and log entries use these prefixes. Design files, `src/` files, and `tests/` files stay human-readable and do not use prefix IDs as their primary numbering, although comments may carry traceability notes when needed.

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
- Human-edited by default: `intent/product-intent.md` and `intent/feedback.md`
- System-edited: `intent/gaps.md`
- Occasionally human-edited: `AGENTS.md`, `skills/*`
- System-managed through workflow: `plan/*`, `design/*`, `src/*`, `tests/*`, `dev_log/*`, `dev_workflow/*`, and usually `.codex/*`

## Intent-driven flow
`intent/` drives the rest of the repository in this order:

`intent/product-intent.md` and `intent/feedback.md` -> `intent/gaps.md` -> `ux-flows` -> `system-design` -> `acceptance-criteria` -> `plan` -> `src/tests` -> `validation` -> `dev_log` -> feedback routing -> intent update -> next iteration

That means:
- Human intent becomes structured design.
- Human intent is first expressed as UX flows, then system behavior, then acceptance criteria.
- Human intent is then bucketed into plan files for design, code, and test work.
- Design drives implementation and validation.
- Validation and review create logs and feedback.
- Feedback is summarized back into `intent/feedback.md`, and durable direction updates are reflected in `intent/product-intent.md` for the next loop.

## Closed-loop workflow
1. `plan-update.md` prompt: compare the latest intent with design, code, tests, and logs, then write `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
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
- `intent/product-intent.md` and `intent/feedback.md` are populated enough to interpret.
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
