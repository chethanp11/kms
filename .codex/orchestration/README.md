# Orchestration

This folder defines reusable staged execution patterns for long-horizon autonomous development.

## Files

- `implementation-review-validation.md`: default loop for bounded work spanning implementation, review, validation, and repair.
- `hitl-checkpoints.md`: when to stop for human approval.
- `resumable-state.md`: how to leave restartable progress notes.

## AppFlow Usage

- Use single-agent execution for narrow steps with one clear owner.
- Use `implementation-review-validation.md` when a change crosses planning, implementation, validation, and repair.
- Use `hitl-checkpoints.md` whenever a decision changes authority, safety, dependencies, broad architecture, or mode boundaries.
- Use `resumable-state.md` for interrupted long-running work; pair it with `appflow_run.py status` or `preflight` before resuming.

## Governance

Orchestration files define process only. They do not grant authority to bypass the selected `.devmode/*` entry point, product design, validation, or human-owned decisions.
