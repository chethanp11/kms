# Codex Agent Catalog

This catalog defines bounded agent roles for repository-visible orchestration. These are role contracts, not autonomous permissions.

## Invocation Model

- Use one role when the task maps clearly to that responsibility.
- Combine roles through `.codex/orchestration/implementation-review-validation.md` for larger work.
- Agents must read `.devmode/mode.yaml`, the selected `.devmode/*` entry point, `.codex/project-context.md`, `.codex/tech-stack.md` when validation or stack matters, and the relevant workflow file before acting.
- Agents may recommend changes outside their role, but should not silently implement them.

## Roles

| Agent | Primary responsibility | AppFlow step fit | Must not do |
| --- | --- | --- | --- |
| Planner | Convert intent into phased, traceable execution plans | `02-create-plan` | Implement before plan readiness |
| Architecture | Review boundaries, data flow, service ownership, and extensibility | `03-update-design` | Approve code that contradicts design |
| Implementer | Make bounded code/docs changes from approved plan/design | `05-implement-code` | Invent product requirements |
| Reviewer | Check diff quality, maintainability, scope, and contract fit | `10-iteration-review` | Rewrite broad areas opportunistically |
| Validator | Select and run targeted validation, classify failures | `04-update-tests`, `06-run-validation` | Claim pass without evidence |
| Debugger | Reproduce and isolate failures, propose minimal fixes | `07-fix-failures` | Apply blind repeated fixes |
| Governance | Review policy, traceability, auditability, and safety | `01-read-intent`, `09-detect-gaps` | Bypass human-owned decisions |
| Documentation | Update repo-visible docs and project context | `03-update-design`, `08-update-logs` | Create empty or promotional docs |

## Handoff Contract

Every agent handoff should include:

1. scope and non-goals
2. source artifacts read
3. files changed or recommended
4. validation performed or required
5. risks, blockers, and deferrals
