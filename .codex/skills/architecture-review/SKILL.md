---
name: architecture-review
description: Review application architecture for alignment with design, interfaces, provenance, observability, persistence boundaries, and operational constraints.
---

# Architecture Review

## Purpose
Ensure the architecture can support the intended behavior, interfaces, and operational constraints.

## Read
- `.codex/project-context.md`
- relevant design docs
- relevant `src/` modules
- relevant tests or validation output

## Do
1. Review the task context before architecture details.
2. Validate ownership boundaries between services, interfaces, tools, schemas, and observability.
3. Check that provenance, tracing, failure handling, and persistence boundaries have clear homes.
4. Compare current implementation shape to documented architecture when code exists.
5. Recommend architecture updates or implementation guardrails.

## Outputs
- Architecture findings with severity and issue classification.
- Required design updates or implementation guardrails.

## Rules
- Do not approve architecture that ignores grounding, provenance, or tool-use assumptions.
- Do not approve architecture that satisfies code but not documented behavior.
- Do not change architecture without updating the relevant design artifact.
