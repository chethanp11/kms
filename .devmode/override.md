# Override Mode

Override mode follows the user prompt directly. It is not AppFlow application workflow and it is not framework workflow.

## Activation

Root `AGENTS.md` routes here when `.devmode/mode.yaml` contains:

```yaml
mode: override
```

## Core Rule

Treat the current prompt as the first-class instruction for the turn. Inspect before editing, make minimal reversible changes, and validate when practical, but do not force the request through AppFlow lifecycle artifacts or framework-control-plane workflows.

## File Access

Override mode may modify any repository file when the prompt requires it, including application artifacts, framework/control-plane files, mode contracts, workflow files, design, tests, source, plans, logs, and project-specific `.codex` files.

This is a permission mode, not a workflow. It does not erase normal safety rules: avoid destructive operations unless explicitly requested, preserve secrets, keep changes reviewable, and do not touch unrelated files.

## Execution Behavior

1. Read `.devmode/mode.yaml`, `AGENTS.md`, and this file first.
2. Use the prompt to determine scope directly.
3. Inspect relevant files and dependencies before editing.
4. Make the smallest coherent change set.
5. Run targeted validation when available or explain why validation was not run.
6. Stop when the prompt scope is complete.
