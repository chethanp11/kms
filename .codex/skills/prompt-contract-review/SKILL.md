# Prompt Contract Review Skill

## Purpose
Validate the AI prompt contract, including structured inputs, output expectations, tool policy, and fallback behavior.

## When to use
- When defining or refining prompt-driven behavior.
- When verifying prompt safety and reliability.
- When the model appears to be doing work the design never explicitly authorized.

## Read
- `intent/product-intent.md`
- `intent/feedback-intent.md`
- `design/system-design.md`
- `design/architecture.md`
- `design/acceptance-criteria.md`
- `design/ux-flows.md`
- `dev_log/change-log.md`
- `dev_log/validation-log.md`
- prompt examples and tool definitions

## Do
1. Review the relevant intent, then the prompt contract and behavior expectations.
2. Check for undefined assumptions or unsafe prompt patterns.
3. Confirm that tool use rules and fallback behavior are explicit.
4. Identify opportunities to tighten prompt boundaries or error handling.
5. Note whether copied-project documentation in `src/README.md` or `src/docs/` needs updates because of prompt changes.

## Outputs
- A prompt contract review summary.
- Recommended prompt updates or guardrails.
- Suggested validation checks for prompt behavior.

## Rules and cautions
- Do not accept vague or open-ended prompt expectations.
- Do not assume the model will behave well without explicit fallback and grounding rules.
- Do not mix prompt design issues with implementation issues; keep them distinct.
