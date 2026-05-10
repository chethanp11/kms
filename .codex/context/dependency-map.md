# Dependency Map Template

Use this template to document project-specific stack and dependency boundaries in `.codex/tech-stack.md`.

## Capture

- language/runtime versions
- package managers
- build commands
- test/lint/typecheck commands
- runtime services
- databases and storage
- external APIs
- model providers and tools
- generated code boundaries

## Rules

- Do not add dependencies without a concrete implementation need.
- Prefer deterministic local tooling for validation.
- Keep dependency ownership clear.
- Record why major dependencies exist.
- Keep AI/model/tool integrations behind explicit interfaces.
