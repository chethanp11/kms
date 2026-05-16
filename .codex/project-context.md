# KMS Project Context

This is the only project-specific grounding file for KMS.
Keep it concise and high-signal.

## Product Identity

KMS is a governed Knowledge Management System that turns immutable source material into finalized markdown knowledge.

## Core Surfaces

- **KMI**: the governed maintenance surface for source intake, candidate review, approval, and publication.
- **`/wiki`**: the canonical finalized knowledge store.
- **Infopedia**: the read-only browsing and search layer over finalized wiki content.

## Authority Boundaries

- Raw source inputs are evidence, not truth.
- `/wiki` is the source of truth.
- KMI may propose, review, approve, and publish, but it must not silently finalize truth.
- Infopedia is read-only and must never mutate canonical knowledge.
- AI-assisted extraction is proposal-only until it passes governed review and publish checks.

## Operating Model

The repository should stay lightweight and context-driven:

- root `AGENTS.md` carries the universal engineering instructions
- `.codex/project-context.md` carries KMS-specific grounding
- `.codex/skills/`, `.codex/agents/`, and `.codex/memory/` provide optional reusable support context

## Context Budget

- Start with `AGENTS.md` and this file.
- Load only the single most relevant support file next.
- Prefer one `.codex/skills/`, `.codex/agents/`, or `.codex/memory/` file at a time.
- Open additional support files only when the current evidence is insufficient.

## Design Expectations

- Preserve governed publication boundaries.
- Preserve deterministic review and validation.
- Preserve read-only consumption through Infopedia.
- Keep implementation and design aligned with the canonical wiki store.

## Runtime Expectations

- Local source folders remain immutable upstream evidence.
- Candidate extraction should stay reviewable and bounded.
- Publication must pass governed validation before `/wiki` changes are accepted.
