# 04 Self Review

## Purpose
Review the actual diff against scope before spending time on broader validation.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/design-update-log.md`
- `dev_log/code-update-log.md`
- `dev_log/test-update-log.md`
- `dev_log/validation-results.md`
- Implementation artifacts in `src/`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `tests/` created or updated for this iteration
- `design/acceptance-criteria.md`
- `tests/design-traceability.md`

## Review for
- plan drift
- design improvement opportunities from logs
- source tree documentation drift
- Scope creep
- Missing failure handling
- Missing tests or eval mappings
- Design drift
- Validation or audit gaps
- Overlap between deterministic code and prompt behavior

## Checklist
1. Compare changed files to the in-scope IDs.
2. Verify that every changed behavior still reflects the relevant plan sections.
3. Verify that every changed behavior has a proving artifact.
4. Verify that the AI path still matches the prompt contract, tool rules, and fallback rules from the current design files.
5. Verify that logs and traceability were updated where needed.
6. Convert findings into immediate fixes or updates to the relevant `dev_log/` file.
7. Identify design changes that should be made before validation if the current design is weak.
8. Verify that `src/README.md` and `src/docs/` match the current plan and scoped functionality.

## Done when
- Findings are documented or fixed
- No obvious drift remains
- The work is worth running through full validation
