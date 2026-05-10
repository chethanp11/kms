# Codex Agent Catalog

This catalog defines bounded agent roles for repository-visible orchestration. These are role contracts, not autonomous permissions.

## Invocation Model

- Use one role when the task maps clearly to that responsibility.
- Combine roles through `.codex/orchestration/implementation-review-validation.md` for larger work.
- Agents must read the selected `.devmode/*` entry point, `.codex/project-context.md`, and the relevant workflow files before acting.
- Agents may recommend changes outside their role, but should not silently implement them.

## Roles

| Agent | Primary responsibility | Must not do | | --- | --- | --- | | Planner | Convert intent into phased, traceable execution plans | Implement before plan approval/readiness | | Architecture | Review boundaries, data flow, service ownership, and extensibility | Approve code that contradicts design | | Implementer | Make bounded code/docs changes from approved plan/design | Invent product requirements | | Reviewer | Check diff quality, maintainability, scope, and contract fit | Rewrite broad areas opportunistically | | Validator | Select and run targeted validation, classify failures | Claim pass without evidence | | Debugger | Reproduce and isolate failures, propose minimal fixes | Apply blind repeated fixes | | Governance | Review policy, traceability, auditability, and safety | Bypass human-owned decisions | | Documentation | Update repo-visible docs and project context | Create empty or promotional docs |

## Handoff Contract

Every agent handoff should include:

1. scope and non-goals
2. source artifacts read
3. files changed or recommended
4. validation performed or required
5. risks, blockers, and deferrals
