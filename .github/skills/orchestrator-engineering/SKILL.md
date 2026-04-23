---
name: orchestrator-engineering
description: Design lightweight Python workflow control loops, state persistence, context passing, and LangGraph-ready extensibility.
---

## Purpose
Build the control layer that executes workflow nodes safely and predictably.

## When to use
- When defining Python orchestration around prompts.
- When state must persist across steps or runs.
- When preparing for migration to LangGraph or similar control systems.

## Do
1. Keep state explicit and durable.
2. Pass only the context the next node needs.
3. Make migration paths visible.
4. Treat orchestration as control, not business logic.

