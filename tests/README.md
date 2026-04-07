# Test Strategy

## Purpose
Explain how validation is organized in a copied project and how it connects back to design.

## Test types
- `unit/`: isolated deterministic logic, schema validation, prompt builders, and adapters.
- `integration/`: interactions across modules, data sources, tools, or model wrappers.
- `e2e/`: user-visible flows from entrypoint to final output.
- `regression/`: protections for previously fixed defects or risky behavior.
- `fixtures/`: reusable inputs, golden outputs, and review samples.

## Working rules
- `tests/` is system-managed and should be updated through the intent -> design -> validation workflow.
- Every changed behavior should point to at least one `TEST-*` or documented manual review step.
- Use `tests/test-plan.md` to define validation intent.
- Use `tests/design-traceability.md` as the authoritative mapping from design to validation.
- Keep `tests/smoke-checklist.md` short enough to run before closeout.
