# KMS

KMS is a governed Knowledge Management System.

It turns raw source material into finalized markdown knowledge under Knowledge Manager control, publishes that knowledge to `/wiki`, and exposes it through read-only Infopedia browsing.

## Repository Structure

- `AGENTS.md` — universal engineering instructions
- `.codex/project-context.md` — KMS-specific grounding
- `.codex/skills/` — optional reusable execution knowledge
- `.codex/agents/` — optional reusable capability guidance
- `.codex/memory/` — reusable conventions, decisions, and lessons
- `design/` — architecture and behavior contracts
- `src/` — implementation
- `tests/` — validation

Optional utility folders such as `scripts/`, `data/`, and `artifacts/` may exist when useful.

## Working Model

1. Read `AGENTS.md`.
2. Read `.codex/project-context.md`.
3. Pull in only the additional context that is relevant to the task.
4. Update design if behavior changes.
5. Update implementation and tests.
6. Validate the result.

## Product Boundaries

- Raw sources are evidence, not truth.
- `/wiki` is the canonical knowledge store.
- KMI is the governed maintenance surface.
- Infopedia is read-only.
- AI may propose and assist, but it must not bypass review or publish governance.
