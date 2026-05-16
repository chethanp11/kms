---
name: large-codebase-analysis
description: Trace request flow, map unfamiliar modules, and identify the smallest file set needed to solve a task.
---

# Large Codebase Analysis

## Purpose
Move quickly from a vague task to a bounded, inspectable scope.

## Read
- `AGENTS.md`
- project grounding file
- relevant design docs
- relevant tests, entrypoints, and runtime wiring

## Do
1. Find the main entrypoint and downstream flow.
2. Locate contracts, boundaries, and shared utilities.
3. Identify the smallest edit surface that can solve the task.
4. Separate source-of-truth files from derived or supporting files.
5. Capture the key risks before editing.

## Outputs
- Flow map
- Minimal file set
- Boundary and dependency notes

## Rules
- Prefer evidence over guesswork.
- Do not inspect unrelated modules unless the task forces it.
