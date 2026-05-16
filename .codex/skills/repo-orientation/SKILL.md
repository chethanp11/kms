---
name: repo-orientation
description: Map the repository structure, runtime entrypoints, contracts, and validation path before making changes.
---

# Repo Orientation

## Purpose
Identify the smallest relevant part of the repository before editing.

## Read
- `AGENTS.md`
- project grounding file, usually `.codex/project-context.md`
- relevant design docs
- relevant tests or validation output
- entrypoint files, manifests, and top-level tree as needed

## Do
1. Identify the likely runtime, control-plane, or documentation surface.
2. Locate the smallest relevant file set.
3. Separate source of truth from derived artifacts.
4. Note contracts, dependencies, and likely failure points.
5. Decide what should be inspected next before editing.

## Outputs
- Short repo map for the task.
- Relevant files and why they matter.
- Risks, assumptions, and validation candidates.

## Rules
- Do not bulk-load the repository.
- Do not start editing before the relevant boundary is understood.
