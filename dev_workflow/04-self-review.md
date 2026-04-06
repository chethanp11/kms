# 04 Self Review

## Purpose
Review the actual diff against scope before spending time on broader validation.

## Read first
- `intent/*`
- `dev_log/*`
- Implementation artifacts in `src/`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`
- `tests/` created or updated for this iteration
- `design/acceptance-criteria.md`
- `tests/design-traceability.md`
- `design/ai-behavior-spec.md`

## Review for
- intent drift
- design improvement opportunities from logs
- source tree documentation drift
- Scope creep
- Missing failure handling
- Missing tests or eval mappings
- Design drift
- Logging or audit gaps
- Overlap between deterministic code and prompt behavior

## Checklist
1. Compare changed files to the in-scope IDs.
2. Verify that every changed behavior still reflects the relevant intent sections.
3. Verify that every changed behavior has a proving artifact.
4. Verify that the AI path still matches the prompt contract, tool rules, and fallback rules.
5. Verify that logs and traceability were updated where needed.
6. Convert findings into `DEV-*` issues or immediate fixes.
7. Identify design changes that should be made before validation if the current design is weak.
8. Verify that `src/README.md` and `src/docs/` match the current product intent and scoped functionality.

## Done when
- Findings are documented or fixed
- No obvious drift remains
- The work is worth running through full validation
