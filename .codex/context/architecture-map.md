# Architecture Map Template

Use this template to build project-specific architecture context in `.codex/project-context.md` or project design docs.

## Recommended Sections

1. System purpose.
2. Runtime entrypoints.
3. Major layers or modules.
4. Dependency direction.
5. Data ownership and persistence boundaries.
6. External integrations.
7. AI/model/tool boundaries when applicable.
8. Observability and failure-handling surfaces.
9. Security and governance boundaries.

## Boundary Checklist

- What is authoritative state?
- What is derived or cached state?
- Which components are allowed to mutate state?
- Which interfaces are public contracts?
- Which workflows require human approval?
- Which layers must never depend on each other?
