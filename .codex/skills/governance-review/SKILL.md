---
name: governance-review
description: Review traceability, provenance, approval boundaries, safety, and human-in-the-loop controls.
---

# Governance Review

## Purpose
Check whether a change respects review, approval, and audit boundaries.

## Read
- `AGENTS.md`
- project grounding file
- relevant design docs
- relevant implementation, tests, and validation output

## Do
1. Check what authority is allowed to change truth or state.
2. Verify evidence, traceability, and provenance paths.
3. Confirm human approval or escalation points are explicit.
4. Check for bypass paths, hidden writes, and silent finalization.
5. Report any missing audit or validation coverage.

## Outputs
- Governance findings with severity.
- Missing approval or traceability gaps.
- Required guardrails or follow-up checks.

## Rules
- Do not approve hidden finalization paths.
- Do not merge evidence with authority.
- Keep review and publication boundaries explicit.
