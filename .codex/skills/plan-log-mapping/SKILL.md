---
name: plan-log-mapping
description: Translate `plan/*` entries into matching `dev_log/*` records for KMS iterations. Use when recording design, code, test, or validation updates after a plan has been executed, when maintaining REQ/DEV/TEST traceability, or when reconciling what changed with what was validated.
---

# Plan Log Mapping

## Purpose

Map completed plan items to permanent log entries without losing IDs, scope, or validation evidence.

## Use This Skill When

- Updating `dev_log/design-update-log.md`, `dev_log/code-update-log.md`, `dev_log/test-update-log.md`, or `dev_log/validation-results.md` from completed plan work.
- Translating `REQ-*`, `DEV-*`, and `TEST-*` items into concrete log entries.
- Recording what changed, why it changed, and how it was validated.
- Checking that log entries match the latest `plan/*` and the active design/test artifacts.

## Workflow

1. Read `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`.
2. Read the active `dev_log/*` files to preserve numbering and avoid duplicate entries.
3. Identify which completed plan items belong in which log file.
4. Write each log entry with the relevant prefix ID and a concise reason.
5. Carry over linked IDs and intent sources so another agent can trace the change.
6. Add validation evidence to `dev_log/validation-results.md` when a check actually ran.
7. Flag gaps, drift, or blockers instead of normalizing them away.

## Output Rules

- Keep log entries factual and specific.
- Use the same IDs that appear in the plan or linked design/test artifacts.
- Do not invent validation, implementation, or design changes that did not happen.
- Do not update `intent/*` from this skill.

## Checks

- Verify plan and log IDs line up.
- Verify validation entries include the command or method used.
- Verify the log file chosen matches the type of change.
