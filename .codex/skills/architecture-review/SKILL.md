---
name: architecture-review
description: Review application architecture for alignment with intent, design, interfaces, orchestration, tools, provenance, observability, persistence boundaries, and operational constraints. Use when design decisions or implementation changes affect system structure, integrations, or data flow.
---

# Architecture Review

## Purpose
Ensure the architecture can support the intended AI behavior, interfaces, and operational constraints.

## Read
- `.codex/AGENTS.md`, root `AGENTS.md`, and `.codex/project-context.md`
- `intent/product-intent.md`
- `intent/feedback-intent.md` when feedback changes operating constraints
- Relevant `plan/*` files
- `design/architecture.md`, `design/system-design.md`, `design/acceptance-criteria.md`, and `design/ux-flows.md`
- Relevant `src/` modules when implementation exists
- `tests/design-traceability.md` and `tests/test-plan.md`
- Relevant `dev_log/*` entries, especially `design-update-log.md`, `code-update-log.md`, and `validation-results.md`

## Do
1. Review intent and plan before architecture details.
2. Validate ownership boundaries between orchestrator, agents, model routing, tools, memory, schemas, and observability.
3. Check that AI tool use, provenance, tracing, failure handling, and persistence boundaries have clear homes.
4. Compare current implementation shape to documented architecture when code exists.
5. Recommend architecture updates or implementation guardrails.

## Outputs
- Architecture findings with severity and issue classification.
- Required design updates or implementation guardrails.
- Traceability to relevant plan IDs and correctness expectations.

## Rules
- Do not approve architecture that ignores grounding, provenance, or tool-use assumptions.
- Do not approve architecture that satisfies current code but not current intent.
- Do not change architecture without updating the relevant design artifact.
