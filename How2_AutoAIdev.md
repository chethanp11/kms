# How to Use AutoAI Dev

## What AutoAI Dev Is
AutoAI Dev is the operating system for this repository.

- `AGENTS.md` is the constitution for AutoAIdev itself.
- `.codex/project-context.md` is the constitution for the product being developed.
- Root `README.md` is the user-facing documentation for AutoAI Dev and how to work with it.

## Core Flow
AutoAI Dev works as a controlled loop:

1. Read the current product intent from `intent/product-intent.md` and `intent/feedback-intent.md`.
2. Translate the intent into a scoped plan in `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
3. Update design first when behavior or structure changes.
4. Implement the approved change in `src/`.
5. Add or update validation in `tests/`.
6. Record the actual change and validation evidence in `dev_log/`.
7. Feed unresolved gaps back into `intent/gaps.md` or `intent/feedback-intent.md` as appropriate.

## How To Use It For Product Development
Use AutoAI Dev as the path from product direction to validated implementation.

1. Start with product intent.
2. Keep the product constitution in `.codex/project-context.md` current.
3. Use `plan/` to turn intent into concrete design, code, and test work.
4. Keep `design/` as the source of truth for what the product should do.
5. Use `src/` only for implementation that matches the approved design.
6. Use `tests/` to prove the product behaves as designed.
7. Use `dev_log/` to preserve what changed, why it changed, and what was validated.

## Practical Rules
- Do not code directly from vague intent.
- Do not change implementation without a matching design or plan update when behavior changes.
- Do not treat logs as optional. They are part of the workflow record.
- Keep traceability explicit so another contributor can continue without guessing.

## Quick Reading Order
When starting work, read files in this order:

1. `AGENTS.md`
2. `.codex/project-context.md`
3. `README.md`
4. `intent/product-intent.md`
5. `intent/feedback-intent.md`
6. `plan/design-update.md`
7. `plan/code-update.md`
8. `plan/test-update.md`
9. `design/*`
10. `tests/*`
11. `dev_log/*`

## Outcome
If the loop is working, product intent becomes design, design becomes code and tests, and code and tests become validated history in `dev_log/`.
