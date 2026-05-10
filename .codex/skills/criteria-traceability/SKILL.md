---
name: criteria-traceability
description: Ensure every application correctness criterion has a concrete traceability path from intent to design to tests and validation proof. Use when defining correctness criteria, updating tests, planning an iteration, or reviewing traceability gaps.
---

# Criteria Traceability

## Purpose
Ensure every correctness criterion has a usable path from human intent to proof.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `intent/product-intent.md`
- `intent/feedback-intent.md` when feedback affects correctness expectations
- `intent/gaps.md` when system-detected gaps exist
- `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`
- `design/acceptance-criteria.md`, `design/system-design.md`, `design/architecture.md`, and `design/ux-flows.md`
- `tests/test-plan.md` and `tests/design-traceability.md`
- `dev_log/validation-results.md` when existing proof matters

## Do
1. Extract the relevant intent, plan items, and correctness statements.
2. Map each correctness item to proving tests, evals, or explicit manual validation.
3. Identify missing `TEST-*`, unclear acceptance wording, or validation blockers.
4. Update `tests/design-traceability.md` only when mappings change.
5. Recommend updates to `design/acceptance-criteria.md` or `tests/test-plan.md` when coverage is incomplete.

## Outputs
- A traceability matrix connecting intent, correctness expectations, plan IDs, tests, and validation evidence.
- A prioritized list of coverage gaps.
- Suggested criteria or test updates.

## Rules
- Do not invent correctness criteria or validation evidence.
- Do not treat vague future coverage as a real mapping.
- Do not assume test coverage exists unless it is documented or verified.
