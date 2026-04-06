# AI Eval Review Skill

## Purpose
Review evaluation evidence and determine whether it is strong enough to support the claimed behavior.

## When to use
- After running evaluation scenarios.
- When a hallucination or retrieval gap is suspected.
- When AI behavior boundaries need verification.
- When automated checks pass but confidence is still low.

## Read
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/feedback-intent.md`
- `intent/iteration-intent.md`
- `dev_log/feedback-log.md` when review findings should change future evals
- `design/ai-behavior-spec.md`
- `design/eval-plan.md`
- `tests/design-traceability.md`
- `dev_log/validation-log.md`
- `src/README.md` and `src/docs/` when eval findings affect user-facing description or functionality

## Do
1. Compare eval results to the relevant intent, expected outcomes, and failure categories.
2. Validate that model behavior stayed within prompt boundaries.
3. Check whether tool use and retrieval assumptions are correctly exercised.
4. Identify hidden gaps that automated scores may not reveal.
5. Note any design or documentation changes implied by the eval findings.

## Outputs
- A review summary showing pass/fail per evaluation scenario.
- Notes on hallucination checks, retrieval correctness, and tool usage.
- Recommendations for design, prompt, or test updates.

## Rules and cautions
- Do not approve passing evals if the review reveals hidden drift.
- Do not assume the model is correct when it merely produced a plausible answer.
- Do not conflate evaluation coverage with complete behavior validation.
