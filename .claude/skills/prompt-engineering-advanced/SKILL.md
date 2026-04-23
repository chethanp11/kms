---
name: prompt-engineering-advanced
description: Design small, deterministic prompts with tight context, modular composition, and explicit output contracts.
---

## Purpose
Write prompts that do one thing well and produce predictable outputs.

## When to use
- When creating or updating workflow prompts.
- When a prompt needs clearer boundaries or less ambiguity.
- When context must be scoped tightly.

## Do
1. Give each prompt one job.
2. Pass only the context needed for that job.
3. State output shape and failure conditions explicitly.
4. Prefer reusable prompt modules over monoliths.

