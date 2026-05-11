---
name: mode-boundary-review
description: Review app, framework, and override mode boundaries before or after mode-sensitive changes. Use when edits affect `.devmode/*`, AGENTS routing, workflow permissions, or files that could cross app/framework ownership.
---

# Mode Boundary Review

## Purpose
Ensure AppFlow mode boundaries are explicit, synchronized, and not bypassed.

## Read
- `.devmode/mode.yaml`
- `AGENTS.md`
- `.devmode/app.md`, `.devmode/framework.md`, and `.devmode/override.md`
- Relevant `.codex/dev_workflow/*` mode guards
- Current diff when reviewing completed changes

## Do
1. Identify the active mode and the selected first-class instruction file.
2. Check whether the requested or changed files are allowed in that mode.
3. Verify framework mode does not repair application artifacts and app mode does not modify control-plane files without explicit prompt scope.
4. Confirm override mode remains a permission mode, not an automatic workflow.
5. Flag any missing mode guard or contradictory routing statement.

## Outputs
- Boundary decision: allowed, blocked, or needs explicit mode/scope change.
- Specific files or paths that cross mode boundaries.
- Minimal wording or validator updates needed to restore consistency.

## Rules
- Never blend modes to justify edits.
- Do not use application validation failures to authorize framework-mode product changes.
- Keep `.devmode/*` generic and concise; put project facts in project extension files.
