---
name: feedback-synthesis
description: Convert feedback from users, reviewers, or tools into concrete actions, risks, and follow-ups.
---

# Feedback Synthesis

## Purpose
Turn scattered feedback into a reviewable plan instead of losing signal.

## Read
- `AGENTS.md`
- project grounding file
- relevant feedback source
- relevant design, implementation, tests, or validation output

## Do
1. Classify each feedback item.
2. Separate blocking issues from follow-up work.
3. Map each item to the right artifact or layer.
4. Preserve traceability to the source feedback.
5. Recommend the smallest corrective action.

## Outputs
- Feedback summary
- Blocking vs non-blocking list
- Recommended artifact updates

## Rules
- Do not flatten every comment into a bug.
- Do not lose the original meaning of the feedback.
