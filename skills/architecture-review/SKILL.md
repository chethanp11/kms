# Architecture Review Skill

## Purpose
Ensure the architecture can actually support the intended AI behavior, interfaces, and operational constraints.

## When to use
- When validating new design decisions.
- When changes affect system structure, integrations, or data flow.
- When implementation starts to hide system behavior that should be explicit in design.

## Read
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`
- `intent/feedback-intent.md` when feedback changes operating constraints
- `design/architecture.md`
- `design/system-design.md`
- `design/api-contracts.md`
- `design/data-models.md`
- `design/ai-behavior-spec.md`
- `dev_log/change-log.md`
- `dev_log/decision-log.md`
- `dev_log/deviations-log.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`

## Do
1. Review the relevant intent first, then the architecture diagrams, components, and integration points.
2. Validate ownership boundaries between orchestration, tools, services, and schemas.
3. Check that AI tool use, provenance, logging, and failure handling have clear homes.
4. Check that copied-project documentation in `src/README.md` and `src/docs/` still matches the current architecture and purpose.
5. Recommend architecture updates or mitigations.

## Outputs
- A summary of architecture findings.
- A list of required design updates or implementation guardrails.
- Traceability to requirement IDs and AI behavior expectations.

## Rules and cautions
- Do not approve architecture that ignores AI-specific tool use or grounding assumptions.
- Do not approve architecture that satisfies current code but not current intent.
- Do not neglect operational or safety constraints in design.
- Do not change architecture without updating `design/architecture.md` and relevant traceability.
