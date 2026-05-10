---
name: design-update
description: Translate active application plan items and validated findings into concrete updates for `.codex/project-context.md` and `design/*` before implementation. Use when intent, feedback, plan work, or logs require design changes.
---

# Design Update

## Purpose
Turn approved plan scope and evidence into design updates before implementation proceeds.

## Read
- `.devmode/app.md` and `.codex/project-context.md`
- `intent/product-intent.md`, `intent/feedback-intent.md`, and `intent/gaps.md`
- `plan/design-update.md`, `plan/code-update.md`, and `plan/test-update.md`
- Existing `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md`
- Relevant `dev_log/*` files when prior outcomes affect the design

## Do
1. Read the current plan and operational evidence together.
2. Decide whether high-level context, detailed design, or both must change.
3. Update `.codex/project-context.md` first when high-level behavior or operating model changes.
4. Update the relevant `design/*` files for detailed behavior, architecture, UX, or acceptance changes.
5. Leave implementation and validation work to the appropriate workflow steps unless explicitly asked.

## Outputs
- Design updates ready for downstream test and code work.
- A clear summary of what changed in intent-to-design translation.
- Follow-up notes for `dev_log/design-update-log.md` after validation or closeout.

## Rules
- Do not jump from intent to code.
- Do not hide design uncertainty inside implementation.
- Do not fabricate completed log entries before the outcome is known.
