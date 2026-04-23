# KMS Claude Project Memory

This is the compact project memory for Claude Code. It mirrors the high-level KMS system context and stays aligned with `AGENTS.md`, `.codex/project-context.md`, and the design layer.

## System Purpose

KMS is a governed Knowledge Management System that turns immutable raw source material into finalized markdown knowledge under Knowledge Manager control. The system is not a chatbot, not a document dump, and not a generic search engine. It is a controlled knowledge maintenance and publication system with a separate read-only navigation layer.

## Core Architecture Principles

- Separate maintenance, consumption, orchestration, validation, and observability responsibilities.
- Treat `/wiki` as the canonical finalized knowledge store.
- Keep raw source inputs immutable.
- Keep Infopedia read-only.
- Preserve evidence, contradictions, failures, and lineage instead of flattening them.
- Make decisions auditable through run state, checkpoints, and trace records.
- Enforce governed execution and publication.

## Repo Expectations

- Start from `intent/` and keep design aligned to it.
- Treat `AGENTS.md` and `.codex/project-context.md` as the first-read contract for every task.
- Use `plan/*` before changing design, tests, or code.
- Update design before code when behavior changes.
- Update tests from acceptance criteria before implementation when behavior changes.
- Keep implementation aligned with the approved plan and design.
- Do not invent behavior that is not represented in intent, plan, context, design, or acceptance artifacts.
- Do not treat `src/docs/` or project `README.md` updates as part of the default code-implementation path.

## Drift Prevention Rules

- Keep `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md` aligned with intent and with each other.
- If a change affects behavior, update plan and design before implementation and keep tests aligned in the same pass.
- If a change would create product drift, stop and reconcile it against intent rather than normalizing the drift in code or design.
- Use the repository stack and workflow only to support the KMS operating model, not to redefine it.
