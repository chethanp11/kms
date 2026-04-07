# Test Repair Skill

## Purpose
Repair or improve tests when failures are caused by stale, incorrect, or insufficient validation artifacts.

## When to use
- When tests fail for reasons unrelated to actual requirements.
- When acceptance criteria change.
- When known gaps are identified during validation.
- When a regression should be preserved after a bug fix.

## Read
- `intent/product-intent.md`
- `intent/feedback-intent.md` when tests are driven by observed behavior gaps
- `tests/` failing test reports
- `design/acceptance-criteria.md`
- `tests/design-traceability.md`
- `dev_log/validation-log.md`
- `dev_log/change-log.md`
- `src/README.md` and `src/docs/` when tests reveal documentation drift

## Do
1. Review failing test details and compare them with current intent and design requirements.
2. Classify each failure as implementation defect, test defect, or environment issue.
3. Update tests to accurately validate the intended behavior.
4. Keep regression and evaluation checks aligned with requirements.
5. Note any documentation updates needed for the copied project README or app docs.

## Outputs
- Corrected test cases.
- A short justification for each repair.
- Updated traceability entries if test IDs or mappings change.

## Rules and cautions
- Do not fix tests by altering requirements covertly.
- Do not mark an implementation defect as fixed if the test is invalid.
- Preserve test intent and clarity when repairing coverage.
