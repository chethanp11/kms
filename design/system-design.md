# System Design

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Define the KMS product at the highest behavioral level: what it does, who controls truth, what the user-visible layers are, and which constraints shape the system.

## Intent sources
- `intent/product-intent.md`
- `intent/feedback-intent.md` when behavior changes are driven by feedback

## Current baseline
- Project: `KMS`
- Target version: `v0.3`
- Primary user or operator: `Knowledge Manager`
- Primary interaction surface: `KMI` maintenance surface plus read-only `Infopedia`
- Authoritative sources: immutable raw source folders and finalized markdown in `/wiki`

## Design principles
- Finalized knowledge is the product; source material is only input.
- KMI owns maintenance and publication governance.
- Infopedia is read-only and derived from finalized wiki content.
- AI may propose, compare, summarize, and ground work, but it may not own truth.
- Deterministic state changes, publication gates, and audit records must stay deterministic.
- Human review points are part of the operating model, not an exception path.

## Problem statement
- Problem being solved: institutional knowledge is fragmented across raw source files, issue threads, notes, and partial repositories, which makes knowledge decay and rework inevitable.
- Why AI is needed: source classification, extraction, comparison, proposal drafting, contradiction detection, and structured markdown generation all benefit from AI assistance.
- What the system must not attempt in this version: generic chat, uncontrolled source mutation, unguided autonomous publication, or consumer-facing editing of finalized knowledge.

## System context
- Inputs: local source-folder paths, existing `/wiki` markdown, governance rules, review decisions, and freshness signals.
- Outputs: proposed wiki updates, approval or rejection decisions, finalized markdown pages, browse-only navigation views, and audit records.
- External dependencies: local filesystem access, markdown parsing and diffing, an LLM for proposal support, and whatever runtime persists wiki content.
- Human checkpoints: approval, correction, escalation, and explicit rejection when contradictions or uncertainty cannot be resolved safely.

## Core requirements
| ID | Requirement | Why it matters | Linked artifacts |
| --- | --- | --- | --- |
| `REQ-001` | KMS must convert immutable raw source material into proposed markdown knowledge updates for `/wiki` through KMI. | This is the core maintenance function and the only path from source to governed knowledge. | `ACC-001`, `ARCH-001`, `TEST-001`, `TEST-003` |
| `REQ-002` | KMS must prevent uncontrolled truth changes and surface contradictions, gaps, and uncertainty to the Knowledge Manager for approve, reject, or escalate decisions. | Governance is the operating model and protects knowledge quality. | `ACC-002`, `ARCH-003`, `TEST-002` |
| `REQ-003` | KMS must provide read-only Infopedia navigation over finalized wiki content without exposing editing or publication capability. | Consumers need stable browse and search access without becoming maintainers. | `ACC-003`, `ARCH-004`, `TEST-003` |
| `REQ-004` | KMS must record source trace, review decisions, freshness signals, and validation evidence for every maintenance run and publication outcome. | Auditability and repeatability are required for trust and future maintenance. | `ACC-004`, `ARCH-006`, `TEST-004` |

## End-to-end narrative
1. A Knowledge Manager supplies a local source-folder path to KMI.
2. The system discovers raw inputs, compares them with current `/wiki` content, and drafts proposed knowledge changes.
3. The system flags contradictions, gaps, low-confidence claims, or freshness issues and requests human review when needed.
4. The Knowledge Manager approves, rejects, revises, or escalates the proposal.
5. Approved changes are published as finalized markdown under `/wiki`.
6. Infopedia renders the finalized wiki as read-only browse/search/navigation content.
7. Downstream AI systems consume the finalized markdown as governed context, not as mutable truth.
8. The system records trace, decisions, and validation evidence so future runs can explain what changed and why.

## Cross-cutting constraints
- Allowed trust boundary: immutable source folders, finalized `/wiki` markdown, and explicitly configured governance rules.
- Latency target: interactive for KMI review and Infopedia browse actions; async for maintenance runs.
- Cost boundary: maintenance runs should stay bounded to local-source analysis and selected model calls, not open-ended autonomous exploration.
- Security or privacy constraints: no secrets in prompts, no uncontrolled publication path, and no consumer-edit surface for finalized truth.
- Change control rule: behavior changes that affect publication, review, or consumption must be reflected in the four design files and recorded in `dev_log/change-log.md`.
