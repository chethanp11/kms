# Repository Memory

Structured, reviewable memory for future Codex sessions.

## Files

- `architecture-memory.md`: stable architecture decisions and boundaries.
- `workflow-memory.md`: operating conventions and iteration lessons.
- `conventions.md`: repository naming, artifact, and validation conventions.
- `implementation-history.md`: concise implementation milestones.
- `debugging-learnings.md`: reusable failure patterns and fixes.

## Rules

- Memory must be factual and reviewable.
- Do not use memory to override source-of-truth artifacts.
- Promote durable outcomes to design or workflow docs when they become normative.

## AppFlow Usage

- Read memory only after current repo artifacts when prior lessons can reduce repeated mistakes.
- During step `10-iteration-review`, identify memory candidates only when a lesson is durable, factual, reusable, and not already promoted to docs/design.
- Prefer promoting normative rules to `.devmode/*`, `.codex/dev_workflow/*`, `.codex/tools/*`, or project design docs instead of leaving them only in memory.
- Memory must never override the user prompt, selected mode contract, project context, plan, design, tests, or validation evidence.
