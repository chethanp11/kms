# Architecture Memory

Durable architecture decisions validated by project artifacts.

## Decision: root AGENTS and project context carry the engineering guidance

- Context: The repository should use a single universal engineering instruction file plus a single project-specific grounding file.
- Chosen approach: Keep reusable support context under `.codex/`; keep project-specific KMS grounding in `.codex/project-context.md`; keep the rest of the support files optional and reusable.
- Alternatives considered: Hardcoded workflow choreography, planner systems, or project-specific support docs scattered across the repository.
- Consequences: Root instructions stay generic, project context stays KMS-specific, and reusable support files stay optional.
- Source artifacts: `AGENTS.md`, `.codex/project-context.md`, `.codex/agents/README.md`, `.codex/memory/README.md`.
- Validation evidence: `git diff --check`.

## Decision: only runtime source deploys

- Context: Development support files must not be treated as production runtime.
- Chosen approach: `src/` is the deployable implementation surface; design, tests, docs, and support files remain non-runtime.
- Alternatives considered: Treat support files or docs as runtime inputs.
- Consequences: Only source code and required runtime assets should ship.
- Source artifacts: `.codex/project-context.md`, `README.md`.
- Validation evidence: `git diff --check`.

## Rules

- Do not use memory to bypass design docs.
- Promote durable architecture rules to `.codex/project-context.md` or project design docs.
