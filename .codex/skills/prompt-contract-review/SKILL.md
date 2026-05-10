---
name: prompt-contract-review
description: Review application prompt contracts for structured inputs, output expectations, tool policy, model boundaries, fallback behavior, and safety. Use when prompt-driven behavior is designed, changed, validated, or suspected of exceeding authorized scope.
---

# Prompt Contract Review

## Purpose
Validate AI prompt contracts, including inputs, outputs, tool policy, and fallback behavior.

## Read
- `.codex/AGENTS.md`, root `AGENTS.md`, and `.codex/project-context.md`
- Relevant `intent/*` and `plan/*` files
- `design/system-design.md`, `design/architecture.md`, `design/acceptance-criteria.md`, and `design/ux-flows.md`
- Prompt files, tool definitions, schemas, and model-routing code when present
- `tests/design-traceability.md`, `tests/test-plan.md`, and `dev_log/validation-results.md`

## Do
1. Review the intended behavior and prompt boundary before judging prompt text.
2. Check structured inputs, output format, fallback paths, and refusal/error behavior.
3. Confirm tool-use rules are explicit and route through the architecture-approved executor.
4. Identify unsafe assumptions, vague instructions, or missing validation cases.
5. Recommend prompt, schema, design, or test updates as separate findings.

## Outputs
- Prompt contract review summary.
- Recommended prompt updates or guardrails.
- Suggested validation checks.

## Rules
- Do not accept vague prompt expectations.
- Do not rely on the model behaving well without explicit boundaries.
- Keep prompt design issues distinct from implementation defects.
