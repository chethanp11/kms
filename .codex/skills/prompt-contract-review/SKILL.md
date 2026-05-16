---
name: prompt-contract-review
description: Review prompt contracts for structured inputs, output expectations, tool policy, model boundaries, fallback behavior, and safety.
---

# Prompt Contract Review

## Purpose
Validate AI prompt contracts, including inputs, outputs, tool policy, and fallback behavior.

## Read
- `.codex/project-context.md`
- relevant design docs
- prompt files, tool definitions, schemas, and model-routing code when present
- relevant tests or validation output

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
