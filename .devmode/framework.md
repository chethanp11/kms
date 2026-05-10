# Framework Mode

Framework mode improves the AppFlow framework itself.

## Activation

Root `AGENTS.md` routes to this file after reading `.devmode/mode.yaml`. When it contains:

```yaml
mode: framework
```

use this file as the active operating entry point.

## Prompt Handling

Treat each user prompt as-is. Do not convert it into application intent and do not run the AppFlow application lifecycle unless explicitly requested.

## Operating Rules

- Improve the framework directly from the current prompt.
- Focus on framework structure, workflow design, orchestration, prompt systems, contracts, governance, repository organization, and reusable engineering systems.
- Keep reusable framework files project-agnostic.
- Do not execute `.codex/dev_workflow/*` as an application workflow.
- Do not use application artifacts as required inputs unless the prompt explicitly asks for application work.
- Prefer minimal, reviewable framework changes over broad rewrites.
- Validate framework changes with `python .codex/tools/validate_codex_contract.py` and `git diff --check` when applicable.
