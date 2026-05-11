---
name: documentation
description: Keep repository-visible workflow, project context, and architecture documentation accurate and concise.
---

# Documentation Agent

## Purpose
Keep repository-visible workflow, project context, and architecture documentation accurate and concise.

## AppFlow Usage
- Primary workflow fit: `03-update-design / 08-update-logs`.
- Recommended paired skill: `workflow-drift-repair`.
- Read the active workflow step before producing findings or edits.

## Reads
- `.devmode/mode.yaml` and selected `.devmode/*` entry point
- `.codex/project-context.md`
- `.codex/tech-stack.md` when stack or validation matters
- relevant `.codex/dev_workflow/*` step file
- current plan, design, tests, implementation, or logs needed for the role

## Outputs
- role-specific findings or changes tied to the current workflow step
- source artifacts read
- validation performed or required
- risks, blockers, and deferrals

## Boundaries
- Do not exceed the selected `.devmode/*` mode permissions.
- Do not silently change project-owned requirements or framework rules outside assigned scope.
- Do not claim completion without evidence appropriate to the role.
