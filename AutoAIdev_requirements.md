
## Application Flow
1. `intent/` is the starting point of requirements.
2. `intent/` contains exactly these operational input files: `product-intent.md`, `feedback-intent.md`, and `gaps.md`.
3. Manually update `intent/product-intent.md` with the latest product goals, scope, user flows, constraints, and expected behavior.
4. Manually update `intent/feedback-intent.md` with new findings from manual review, testing, usage feedback, bug observations, or scope changes.
5. A prompt reviews `dev_log/*` and updates `intent/gaps.md`.
6. Treat `intent/product-intent.md` and `intent/feedback-intent.md` as the only human-edited operational inputs for the workflow.
7. Treat `intent/gaps.md` as a system-edited operational input for the workflow.
8. Keep `design/` as the current source of design truth, not `intent/` and not any temporary plan files.
9. Keep `plan/` as the temporary working area for the current iteration only.
10. Keep `dev_log/` as the permanent archive of what was actually updated and validated.
11. The current design is represented by exactly these files: `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md`.
12. If any of those four design files are missing on a new project or first pass, create them before broadening the design layer.
13. Design files are typical markdown files and remain human-readable.
14. Design files do not use prefix IDs as primary numbering.
15. Plan files and log file entries use prefix IDs to show what was planned, implemented, and validated where.
16. `design/`, `src/`, and `tests/` do not use prefix IDs as primary numbering, although comments may carry traceability notes when needed.
17. Ensure current implementation exists in `src/`; if not, scaffold it from design when the implementation prompt runs for the first time.
18. Ensure the current test suite exists in `tests/`; if not, scaffold it from design when the test prompt runs for the first time.
19. An iteration means running `dev_workflow` prompts in sequence, either manually or programmatically.
20. A new iteration starts only after `intent/` or `feedback-intent.md` is updated manually, or after validation identifies gaps that are captured back into `intent/`.

## Updating Plan
1. All activities are driven by a prompt or a series of prompts.
2. The objective is to update three files in `plan/`: `design-update.md`, `code-update.md`, and `test-update.md`.
3. Reconcile `intent/`, `design/`, `src/`, and `tests/`.
4. Read `intent/product-intent.md` fully.
5. Read `intent/feedback-intent.md` fully.
6. Read `intent/gaps.md` fully.
7. Read all relevant design files in `design/`.
8. Inspect the current source code in `src/`.
9. Inspect the current tests in `tests/`.
10. Identify gaps between product intent and current design.
11. Identify gaps between design and current code.
12. Identify gaps between code and current tests.
13. Identify whether any product-intent, feedback, or gaps item requires design changes, code changes, test changes, or some combination of them.
14. Classify all pending work into three buckets: `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
15. Write the pending design changes into `plan/design-update.md` with prefix `REQ-*`.
16. Write the preliminary pending code changes into `plan/code-update.md` with prefix `DEV-*`.
17. Write the preliminary pending test changes into `plan/test-update.md` with prefix `TEST-*`.
18. All `plan/*` files are numbered with prefix IDs.

## Numbering and Ordering Rules
1. Folder order for the repo is `intent/`, `plan/`, `design/`, `src/`, `tests/`, `dev_log/`, `dev_workflow/`, `skills/`, and `.codex/`.
2. File order within `intent/` is `product-intent.md`, `feedback-intent.md`, and `gaps.md`.
3. File order within `plan/` is `design-update.md`, `code-update.md`, and `test-update.md`.
4. File order within `design/` is `system-design.md`, `architecture.md`, `ux-flows.md`, and `acceptance-criteria.md`.
5. File order within `dev_log/` is `design-update-log.md`, `code-update-log.md`, `test-update-log.md`, and `validation-results.md`.
6. Design, `src/`, and `tests/` stay human-readable and do not use prefix IDs as primary numbering.
7. Plan files and log entries use prefix IDs.
