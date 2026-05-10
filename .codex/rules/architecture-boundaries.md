# Architecture Boundary Rules

Every application should define project-specific architecture boundaries in root `AGENTS.md` and design docs.

Reusable boundary checks:

- Identify authoritative state.
- Identify derived/cache state.
- Keep write paths explicit.
- Keep public contracts stable unless intentionally changed.
- Keep orchestration separate from domain logic where practical.
- Keep AI/model/tool calls behind explicit interfaces.
- Require human approval for high-risk state mutation or governance changes.
