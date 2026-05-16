---
name: test-repair
description: Repair or improve tests when failures are caused by stale artifacts, changed behavior, missing regression coverage, or environment issues.
---

# Test Repair

## Purpose
Repair or improve tests while preserving the requirements they are meant to validate.

## Read
- `.codex/project-context.md`
- failing test reports or validation output
- relevant design docs
- relevant `src/` files only to understand behavior under test

## Do
1. Compare each failure to the documented behavior and expected results.
2. Classify each failure as implementation defect, test defect, eval gap, environment issue, or backlog enhancement.
3. Repair tests only when the test is stale, incorrect, or insufficient.
4. Add regression coverage when fixing a real defect.
5. Update traceability when coverage or behavior expectations change.

## Outputs
- Corrected tests or a clear finding that implementation must change instead.
- Short justification for each repair.
- Updated traceability recommendations or edits.

## Rules
- Do not weaken tests to make them pass.
- Do not mark an implementation defect fixed by changing tests.
- Preserve test intent and deterministic validation.
