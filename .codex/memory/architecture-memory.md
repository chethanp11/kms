# Architecture Memory

Durable architecture decisions validated by project artifacts.

## Decision: AppFlow factory is the engineering control plane

- Context: The repository was converted into a copy/drop AppFlow factory while preserving project-specific context.
- Chosen approach: Keep reusable agent, workflow, orchestration, skill, rule, prompt, tool, memory, and state assets under `.codex/`.
- Alternatives considered: Keep workflow folders at repository root or duplicate human-facing index folders.
- Consequences: Root stays product/project-facing; `.codex/` owns reusable AI-native engineering infrastructure.
- Source artifacts: `.codex/AGENTS.md`, `.codex/appflow.md`, root `AGENTS.md`, `.codex/project-context.md`.
- Validation evidence: `DEV-008`, `DEV-009`, `DEV-010`, and `DEV-011` in `dev_log/validation-results.md`.

## Decision: only project runtime code deploys to production

- Context: AppFlow artifacts are development control-plane assets and should not be treated as production runtime.
- Chosen approach: Root `AGENTS.md` and `README.md` define `src/` as the intended production runtime boundary.
- Alternatives considered: Let workflow or governance folders exist at root and risk deployment ambiguity.
- Consequences: Intent, plan, design, tests, logs, and `.codex/` support development but are not deployed runtime artifacts.
- Source artifacts: root `AGENTS.md`, `README.md`, `.codex/AGENTS.md`.
- Validation evidence: `DEV-011` in `dev_log/validation-results.md`.

## Template

```md
## Decision
- Context:
- Chosen approach:
- Alternatives considered:
- Consequences:
- Source artifacts:
- Validation evidence:
```

## Rules

- Do not use memory to bypass design docs.
- Promote durable architecture rules to root `AGENTS.md` or project design docs.
