---
name: plan-log-mapping
description: Translate completed application `plan/*` entries into the four canonical `dev_log/*` records while preserving REQ/DEV/TEST IDs, scope, and validation evidence. Use after design, code, test, or validation work has actually been completed.
---

# Plan Log Mapping

## Purpose
Map completed plan items to permanent log entries without losing IDs, scope, or validation evidence.

## Read
- `.codex/AGENTS.md`, root `AGENTS.md`, and `.codex/project-context.md`
- `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`
- `dev_log/design-update-log.md`, `dev_log/code-update-log.md`, `dev_log/test-update-log.md`, and `dev_log/validation-results.md`
- Relevant `design/*`, `tests/*`, or `src/` files only as needed to verify what changed

## Do
1. Identify completed plan items and the artifact layer they affected.
2. Preserve existing numbering and avoid duplicate log entries.
3. Write design changes to `dev_log/design-update-log.md`.
4. Write implementation changes to `dev_log/code-update-log.md`.
5. Write test changes to `dev_log/test-update-log.md`.
6. Write actual validation evidence to `dev_log/validation-results.md`.
7. Flag gaps, drift, blockers, or missing validation instead of normalizing them away.

## Outputs
- Factual log entries tied to the relevant `REQ-*`, `DEV-*`, or `TEST-*` IDs.
- Validation entries containing the command or method, result, findings, and follow-up.
- A concise summary of any unmapped or blocked plan items.

## Rules
- Do not invent validation, implementation, or design changes.
- Do not update `intent/*` from this skill.
- Do not create non-canonical `dev_log/*` files unless the repo contract changes first.
