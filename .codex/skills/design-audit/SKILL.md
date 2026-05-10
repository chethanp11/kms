---
name: design-audit
description: Audit application artifacts for drift across intent, plan, project context, design, tests, implementation, and dev logs. Use after a development cycle, before closeout, or whenever behavior, design, or validation may have diverged.
---

# Design Audit

## Purpose
Validate whether implementation, tests, and logs remain aligned with the current plan, design, and target behavior.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `.codex/state/current-intent.md`
- Optional project-owned intent, feedback, or gap artifacts when `.codex/project-context.md` says they are active
- `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`
- `design/system-design.md`, `design/architecture.md`, `design/acceptance-criteria.md`, and `design/ux-flows.md`
- `tests/design-traceability.md` and `tests/test-plan.md`
- Relevant `src/` files
- `dev_log/design-update-log.md`, `dev_log/code-update-log.md`, `dev_log/test-update-log.md`, and `dev_log/validation-results.md`

## Do
1. Compare current intent and plan to project context, design, tests, code, and logs.
2. Identify undocumented behavior, missing validation, outdated traceability, or scope creep.
3. Classify each finding using the repo's allowed issue classifications.
4. Recommend the smallest artifact updates needed to restore alignment.
5. Do not implement fixes unless the user explicitly asks for remediation.

## Outputs
- Concise audit summary.
- Findings grouped by design drift, implementation defect, test defect, eval gap, environment issue, or backlog enhancement.
- Recommended next updates and validation checks.

## Rules
- Do not approve implementation based solely on passing tests.
- Do not silently resolve ambiguity with assumptions.
- Do not make unapproved behavior changes during the audit.
