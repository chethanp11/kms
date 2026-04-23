# ABA Copilot Context

High-level design context for Agentic Business Analytics (ABA). `intent/product-intent.md` is the source of truth. This file summarizes the operating model for `design/*`, `src/*`, and `tests/*`.

## System Purpose

ABA is a controlled agentic system for end-to-end business analytics. It is an analytics execution system, not a chatbot or prompt-only workflow. The system turns ambiguous business problems into structured analytical outcomes through stage-driven orchestration, bounded reasoning, governed execution, and traceable validation.

## Core Architecture Principles

- Separate reasoning, control, execution, context, validation, and observability responsibilities.
- Model every run as a graph of explicit stages and transitions.
- Keep all outputs structured and machine-readable.
- Support iterative, exploratory, and branchable analysis flows.
- Treat context as curated input, not an unbounded dump.
- Preserve evidence, contradictions, failures, and lineage instead of flattening them.
- Make every decision auditable through state, checkpoints, and trace records.
- Enforce controlled execution with safe, sandboxed tool use.

## Key Components

### Orchestration

LangGraph is the control layer. It owns run state, stage transitions, branching, loop-back, retry logic, checkpointing, escalation, and termination decisions. The orchestrator is the control brain for the run.

### Agents

Agents are modular reasoning components with strict input and output contracts. They handle intake structuring, business context, data context, context curation, hypothesis generation, hypothesis prioritization, analysis planning, code generation, code review, execution interpretation, pattern or driver analysis, insight generation, recommendation, critic behavior, and insight validation.

Agents do not control flow and do not execute tools directly.

### Context and Memory

ABA uses a stage-aware context pack for each run. Context includes business context, data context, prior outputs, reusable memory, and versioned artifacts. The context layer supports selection, prioritization, reuse, and traceability while preventing context overload and noise propagation.

### Execution Layer

The execution layer handles SQL, Python, and SAS under governed, sandboxed runtime conditions. It exposes execution through structured requests and returns normalized results with logs, artifacts, and metadata. Tool selection is controlled by policy and runtime constraints.

### Validation and Governance

Validation is mandatory at every major stage. Governance applies runtime policy checkpoints, confidence checks, contradiction handling, escalation triggers, and human-in-the-loop gates. Failed validation must block progression, revise the path, retry within policy, or escalate.

### Observability and Traceability

ABA must capture run-level traces, agent-level logs, stage transitions, intermediate artifacts, decision rationale, retry and failure history, and lineage from intake to insight. Observability data must be structured and queryable so runs can be replayed and debugged.

## Design Philosophy

- Agentic, not prompt-driven.
- Controlled, not free-form.
- Structured, not narrative-first.
- Governed, not autonomous.
- Traceable, not black-box.
- Repeatable across runs when inputs, policies, and data conditions are equivalent.

## Development Expectations For Codex

- Start from `intent/` and keep design aligned to it.
- Use a design-first workflow before implementation.
- Respect stage boundaries, contracts, and control-flow ownership.
- Update the correct layer for the change: design before code, tests to prove acceptance, and logs when reality changes.
- Do not invent behavior that is not represented in intent or approved design.
- Keep implementation and validation aligned with the controlled ABA operating model.

## Drift Prevention Rules

- Treat `intent/product-intent.md` as the source of truth for product behavior.
- Do not introduce capabilities, stages, agents, outputs, or technologies that are not supported by intent or the approved design layers.
- Keep `design/system-design.md`, `design/architecture.md`, `design/ux-flows.md`, and `design/acceptance-criteria.md` aligned with intent and with each other.
- If a change affects behavior, update design before implementation and keep tests and documentation aligned in the same pass.
- If a change would create product drift, stop and reconcile it against intent rather than normalizing the drift in code or design.
- Use the repository stack and workflow only to support the ABA operating model, not to redefine it.
