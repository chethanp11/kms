# Test Strategy

## Purpose
Explain how validation is organized in the repository.

## Test types
- `unit/`: isolated deterministic logic, schema validation, prompt builders, and adapters.
- `integration/`: interactions across modules, data sources, tools, or model wrappers.
- `e2e/`: user-visible flows from entrypoint to final output.
- `regression/`: protections for previously fixed defects or risky behavior.
- `fixtures/`: reusable inputs, golden outputs, and review samples.

## Working rules
- Keep validation deterministic and reviewable.
- Add or update tests when behavior changes.
- Prefer the smallest test that proves the behavior.
- Use fixtures for repeatable inputs and outputs.
