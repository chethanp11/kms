---
name: ai-eval-review
description: Review AI evaluation evidence for grounding, hallucination risk, tool assumptions, and whether results actually support the claimed behavior.
---

# AI Eval Review

## Purpose
Decide whether evaluation evidence is strong enough to support the claimed AI behavior.

## Read
- `.codex/project-context.md`
- relevant design docs
- relevant tests and validation output
- the prompt or eval scenario under review

## Do
1. Compare eval results to the stated behavior and grounding.
2. Check hallucination risk, retrieval/tool assumptions, and prompt boundaries.
3. Confirm the eval exercises the behavior it claims to prove.
4. Identify gaps that automated scores may miss.
5. Recommend prompt, design, test, or validation updates as separate findings.

## Outputs
- Pass/fail/partial status per evaluation scenario.
- Notes on hallucination checks, grounding, and tool usage.
- Follow-up recommendations.

## Rules
- Do not approve plausible model output without grounding evidence.
- Do not conflate eval coverage with complete behavior validation.
- Do not change requirements while reviewing eval evidence.
