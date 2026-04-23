---
name: orchestration-workflow-engineering
description: Sequence prompts, branching, retries, and loop-back behavior in a controlled workflow.
---

## Purpose
Design the order and control flow of the workflow layer.

## When to use
- When defining workflow stages or node order.
- When handling retries, branching, or loop-back.
- When a step needs orchestration metadata.

## Do
1. Make state transitions explicit.
2. Keep the next step deterministic.
3. Route failures to the correct repair path.
4. Preserve traceability across iterations.

