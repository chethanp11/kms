# ABA Claude Project Memory

This is the compact project memory for Claude Code. It mirrors the high-level ABA system context that used to live only in GitHub Copilot instructions, but it is written for Claude's project-memory model.

## System Purpose

Agentic Business Analytics (ABA) is a controlled agentic system for end-to-end business analytics. It is an analytics execution system, not a chatbot or prompt-only workflow. The system turns ambiguous business problems into structured analytical outcomes through stage-driven orchestration, bounded reasoning, governed execution, and traceable validation.

## Core Architecture Principles

- Separate reasoning, control, execution, context, validation, and observability responsibilities.
- Model every run as a graph of explicit stages and transitions.
- Keep outputs structured and machine-readable.
- Support iterative, exploratory, and branchable analysis flows.
- Treat context as curated input, not an unbounded dump.
- Preserve evidence, contradictions, failures, and lineage.
- Make decisions auditable through state, checkpoints, and trace records.
- Enforce controlled execution with safe, sandboxed tool use.

## System Shape

- LangGraph owns orchestration, transitions, retries, checkpoints, and termination decisions.
- Agents are modular reasoning components with strict input and output contracts.
- Context is stage-aware, curated, versioned, and traceable.
- Execution is governed and sandboxed for SQL, Python, and SAS.
- Validation is mandatory at every major stage.
- Observability must capture structured traces, logs, artifacts, and lineage.

## Design Philosophy

- Agentic, not prompt-driven.
- Controlled, not free-form.
- Structured, not narrative-first.
- Governed, not autonomous.
- Traceable, not black-box.
- Repeatable when inputs, policies, and data conditions are equivalent.

## Repo Expectations

- Start from `intent/` and keep design aligned to it.
- Use design-first workflow before implementation.
- Respect stage boundaries, contracts, and control-flow ownership.
- Update the correct layer for the change: design before code, tests to prove acceptance, and logs when reality changes.
- Do not invent behavior that is not represented in intent or approved design.
