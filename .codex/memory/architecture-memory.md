# Architecture Memory

Durable architecture decisions validated by project artifacts.

## Decision: AppFlow factory is the engineering control plane

- Context: The repository was converted into a copy/drop AppFlow factory while preserving project-specific context in two files.
- Chosen approach: Keep reusable agent, workflow, orchestration, skill, tool, memory, and state assets under `.codex/`; keep app/framework routing under `.devmode/`; keep project-specific information only in `.codex/project-context.md` and `.codex/tech-stack.md`.
- Alternatives considered: Keep workflow folders at repository root, keep separate prompt/context/rules template folders, or duplicate human-facing index folders.
- Consequences: Root `AGENTS.md` is only a router; `.devmode/*` and reusable `.codex/*` stay project-agnostic; project facts live in the two project files.
- Source artifacts: `AGENTS.md`, `.devmode/app.md`, `.devmode/framework.md`, `.codex/project-context.md`, `.codex/tech-stack.md`, `.codex/dev_workflow/README.md`.
- Validation evidence: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.

## Decision: only project runtime code deploys to production

- Context: AppFlow artifacts are development control-plane assets and should not be treated as production runtime.
- Chosen approach: `.codex/project-context.md` and `.codex/tech-stack.md` define the application deployment boundary; reusable AppFlow folders remain control-plane infrastructure.
- Alternatives considered: Let workflow or governance folders exist at root and risk deployment ambiguity.
- Consequences: AppFlow support files guide development but are not deployed runtime artifacts.
- Source artifacts: `.codex/project-context.md`, `.codex/tech-stack.md`, `.devmode/app.md`.
- Validation evidence: `python .codex/tools/validate_codex_contract.py`; `git diff --check`.

## Rules

- Do not use memory to bypass design docs.
- Promote durable architecture rules to `.codex/project-context.md`, `.codex/tech-stack.md`, or project design docs.
