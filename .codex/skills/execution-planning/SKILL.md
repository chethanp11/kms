---
name: execution-planning
description: Turn a task into a short, bounded, validation-backed execution plan with explicit stop conditions.
---

# Execution Planning

## Purpose
Convert a request into the smallest safe sequence of steps.

## Read
- `AGENTS.md`
- project grounding file
- relevant implementation, tests, and design docs

## Do
1. Restate the task in one sentence.
2. Identify the critical path and non-blocking side work.
3. Break the work into small validated steps.
4. Name the validation for each step.
5. Capture assumptions, dependencies, and stop conditions.

## Outputs
- A short step plan.
- Validation per step.
- Risks and explicit stop condition.

## Rules
- Prefer the minimum reversible change.
- Do not plan speculative refactors.
- Do not skip validation.
