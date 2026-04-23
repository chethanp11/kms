# KMS Copilot Context

High-level context for KMS. `AGENTS.md` is the authoritative contract, and this file summarizes the operating model for `design/*`, `src/*`, and `tests/*`.

## System Purpose

KMS is a governed Knowledge Management System that turns immutable raw source material into finalized markdown knowledge under Knowledge Manager control. The system is not a chat interface, a document dump, or a generic search engine. It is a controlled knowledge maintenance and publication system with a separate read-only navigation layer.

## Core Boundaries

- KMI is the governed maintenance surface.
- `/wiki` is the canonical finalized knowledge substrate.
- Infopedia is the read-only browsing surface.
- Raw source inputs remain immutable upstream material.
- Metadata, orchestration, and search are supporting services, not alternate truth stores.

## Design Principles

- Curated knowledge over raw retrieval.
- Determinism over improvisation.
- One source of truth in `/wiki`.
- Separation of maintenance and consumption.
- Governance-first publication.
- Structured markdown over free-form sprawl.
- Human control over finalization.
- Extensibility toward future agentic AI use.

## Repo Expectations For Codex

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
