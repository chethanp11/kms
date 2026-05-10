# Validation Policy

## Documentation and Workflow Changes

Run:

```bash
python .codex/tools/validate_codex_contract.py
git diff --check
```

## Product Design Changes

Validate by review against:

- `intent/*`
- `.codex/project-context.md`
- `design/*`
- `tests/design-traceability.md`
- `tests/test-plan.md`

## Code Changes

Run the targeted test layer first. Broaden only after local pass.

## Failure Classification

Use: `design defect`, `implementation defect`, `test defect`, `eval gap`, `environment issue`, or `backlog enhancement`.
