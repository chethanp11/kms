---
name: test-repair
description: Repair or improve application tests when failures are caused by stale validation artifacts, changed correctness criteria, missing regression coverage, or environment issues. Use when validation fails, correctness criteria change, or a bug fix needs preserved regression coverage.
---

# Test Repair

## Purpose
Repair or improve tests while preserving the requirements they are meant to validate.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `.codex/state/current-intent.md` and relevant `plan/*` files
- Failing test reports or validation output
- `design/acceptance-criteria.md` and other relevant `design/*` files
- `tests/design-traceability.md` and `tests/test-plan.md`
- `dev_log/validation-results.md`
- Relevant `src/` files only to understand behavior under test

## Do
1. Compare each failure to current-turn intent, plan scope, and correctness criteria.
2. Classify each failure as implementation defect, test defect, eval gap, environment issue, or backlog enhancement.
3. Repair tests only when the test is stale, incorrect, or insufficient.
4. Add regression coverage when fixing a real defect.
5. Update traceability when test IDs, coverage, or mappings change.

## Outputs
- Corrected tests or a clear finding that implementation must change instead.
- Short justification for each repair.
- Updated traceability recommendations or edits.

## Rules
- Do not weaken tests to make them pass.
- Do not mark an implementation defect fixed by changing tests.
- Preserve test intent and deterministic validation.
