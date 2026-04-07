# 03 Implementation

## Purpose
Implement only the already-designed scope and update every artifact that changes with it, including design refinements suggested by the plan and dev logs.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/*`
- `design/` artifacts relevant to the iteration.
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `dev_workflow/02-iteration-scope.md`
- `tests/test-plan.md`
- `tests/design-traceability.md`
- `AGENTS.md`

## Produce
- Code or configuration changes limited to the scoped behavior
- Initial scaffolding when `src/` is empty
- Refactors inside `src/` when components already exist and design requires changes
- Updates to `src/README.md` and `src/docs/` after code changes so documentation reflects the implementation that just changed
- Supporting test and eval artifacts required by the scope
- Updated logs if the implementation changes design reality or reveals plan/design mismatch
- Design updates when implementation or validation shows the current design should be improved

## Checklist
1. Implement deterministic rules in code, not hidden prompt text.
2. Keep prompt, tool, and fallback behavior aligned with the four design files.
3. Add or update the tests that prove the changed behavior.
4. Flag any mismatch between implementation needs and the latest plan or current design.
5. Update traceability if files, IDs, or proving artifacts changed.
6. Record meaningful changes in `dev_log/change-log.md`.
7. If implementation reveals a design weakness, update design before continuing.
8. After each code or configuration change, update `src/README.md` and `src/docs/` if the change affects documented behavior or purpose.
9. Keep `src/README.md` and `src/docs/` aligned with the current design and plan.

## Stop conditions
- The latest plan has not been translated into sufficient design detail
- Implementation requires behavior not described in design
- A fix changes user-visible behavior but acceptance criteria are stale
- A failing test is being changed without classification

## Done when
- Implementation matches scoped design
- Required validation artifacts are present
- No hidden assumptions remain unlogged
