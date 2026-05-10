---
name: ai-eval-review
description: Review AI evaluation evidence for application behavior, including hallucination risk, retrieval/tool assumptions, prompt boundaries, and whether validation proof supports the claimed behavior. Use after evals, when AI behavior boundaries are questioned, or when automated checks pass but confidence is low.
---

# AI Eval Review

## Purpose
Decide whether evaluation evidence is strong enough to support the claimed AI behavior.

## Read
- `.codex/AGENTS.md`, root `AGENTS.md`, and `.codex/project-context.md`
- `intent/product-intent.md`
- `intent/feedback-intent.md` when feedback changes eval expectations
- `intent/gaps.md` when eval gaps are recorded
- Relevant `plan/*` files
- `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md`
- `tests/design-traceability.md` and `tests/test-plan.md`
- `dev_log/validation-results.md`

## Do
1. Compare eval results to the relevant intent, plan scope, and correctness expectations.
2. Check hallucination risk, grounding, tool-use assumptions, and prompt boundaries.
3. Confirm the eval exercises the behavior it claims to prove.
4. Identify hidden gaps that automated scores may not reveal.
5. Recommend design, prompt, test, or validation updates as separate findings.

## Outputs
- Pass/fail/partial status per evaluation scenario.
- Notes on hallucination checks, retrieval correctness, and tool usage.
- Follow-up recommendations with issue classification.

## Rules
- Do not approve plausible model output without grounding evidence.
- Do not conflate eval coverage with complete behavior validation.
- Do not change requirements while reviewing eval evidence.
