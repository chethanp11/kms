---
name: repeatable-workflows
description: Capture repeated Codex work as a reusable skill, CLI, or scripted procedure.
---

# Repeatable Workflows

## Purpose
Turn recurring engineering work into a reusable, low-friction workflow.

## Read
- `AGENTS.md`
- project grounding file
- the task pattern to be repeated
- any existing scripts, skills, or docs that already encode the workflow

## Do
1. Identify the repeated task and its stable inputs.
2. Decide whether the reuse should live in a skill, script, or CLI.
3. Keep the reusable artifact narrow and deterministic.
4. Use a short invocation contract with explicit outputs.
5. Prefer reusable context over one-off prompt repetition.

## Outputs
- Reusable workflow shape
- Suggested skill or script boundary
- Inputs, outputs, and reuse notes

## Rules
- Do not hide a one-off task behind an overgeneralized workflow.
- Keep reusable artifacts small and specific.
