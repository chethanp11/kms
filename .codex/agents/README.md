# Codex Agent Catalog

This catalog describes optional capability guides for task-specific reasoning.
Agents are not orchestration layers and should not be treated as required helper steps.

## Usage

- Use an agent only when the task clearly benefits from that perspective.
- Prefer the smallest relevant set of contextual files.
- Start with one role file; load a second only if the task truly needs another viewpoint.
- Keep handoffs concrete, bounded, and reviewable.

## Available Roles

| Agent | Use when |
| --- | --- |
| Architecture | reviewing system boundaries, data flow, and interfaces |
| Implementer | making bounded code or doc changes |
| Reviewer | checking scope, maintainability, and unintended impact |
| Validator | selecting and running focused checks |
| Debugger | reproducing and isolating failures |
| Governance | reviewing policy, safety, and approval boundaries |
| Documentation | improving repo-visible docs and context files |

## Handoff Contract

When an agent is useful, include:

1. scope and non-goals
2. source artifacts read
3. files changed or recommended
4. validation performed or required
5. risks, blockers, and deferrals
