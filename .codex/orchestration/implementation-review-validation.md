# Implementation Review Validation Loop

## Purpose
Provide a repeatable loop for autonomous-but-governed execution.

## Loop
1. **Plan**: define scope, files, risks, and proof.
2. **Implement**: make minimal patch-safe changes.
3. **Self-review**: inspect diff for scope, contracts, and unintended impacts.
4. **Validate**: run targeted checks.
5. **Repair**: if validation fails, classify root cause and fix the correct layer.
6. **Record**: update factual logs when the workflow requires it.
7. **Close**: summarize status, risks, and remaining work.

## Exit Criteria
- changed files are intentional
- validation evidence exists or deferral is explicit
- risks and follow-up are visible
- no hidden next scope is started
