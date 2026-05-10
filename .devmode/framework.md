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

---

# Detailed Framework Mode Rules

In framework mode:

- Treat the current user prompt as the primary source of truth.
- Prioritize direct framework evolution over workflow execution.
- Do not trigger AppFlow application lifecycle workflows.
- Do not execute implementation-review-validation orchestration automatically.
- Do not simulate application delivery workflows.
- Do not assume application context unless explicitly provided.
- Do not recursively apply AppFlow to evolve AppFlow itself.
- Do not force staged workflow execution unless explicitly requested.

Focus on:
- framework structure
- workflow design
- orchestration design
- prompt systems
- execution models
- contracts
- governance patterns
- reusable engineering systems
- repository organization
- AI-native development patterns

---

# EXECUTION BEHAVIOR

In framework mode:

- Prefer conceptual clarity over premature implementation.
- Prefer lightweight scaffolding over excessive generation.
- Prefer framework evolution over feature implementation.
- Challenge weak abstractions and unnecessary complexity.
- Improve framework consistency and scalability.
- Keep framework boundaries clean and explicit.

---

# CONTEXT BEHAVIOR

In framework mode:

- Do not automatically consume downstream workflow state.
- Do not continue prior application execution flows unless explicitly instructed.
- Ignore application lifecycle orchestration unless the prompt explicitly invokes it.
- Avoid hidden execution assumptions.
- Minimize recursive workflow behavior.

The current user prompt should drive execution priority.

---

# OUTPUT EXPECTATIONS

Framework mode outputs may include:
- framework updates
- orchestration improvements
- execution model changes
- workflow structures
- prompt systems
- architecture guidance
- governance structures
- repository patterns
- engineering operating models

## AppFlow Lifecycle Stewardship

Framework mode may modify AppFlow itself. Treat lifecycle, workflow, prompt, orchestration, validation, and bootstrap changes as framework changes, not application delivery work. Do not execute the application lifecycle while improving the lifecycle.

When moving or changing AppFlow framework files:

- keep reusable files project-agnostic
- preserve the app-mode contract that only `.codex/project-context.md` and `.codex/tech-stack.md` need project-specific updates for a new application
- update deterministic validators and bootstrap helpers alongside structural changes
- validate with `python .codex/tools/validate_codex_contract.py` and `git diff --check` when available
