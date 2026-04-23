---
name: core-system-thinking
description: Break DevWorkflow into modules, states, and control surfaces; use for decomposition, bounded scope, and workflow system shape.
---

## Purpose
Turn a complex workflow into a small, governed system with clear parts and boundaries.

## When to use
- When reasoning about workflow shape, scope, or module boundaries.
- When a prompt or workflow step needs to be split into smaller units.
- When control-plane behavior must stay explicit.

## Do
1. Identify the smallest useful system boundaries.
2. Separate state, control, execution, and evidence concerns.
3. Prefer explicit transitions over hidden coupling.
4. Keep the design small enough to orchestrate.

