# KMS

KMS is a governed Knowledge Management System for turning immutable raw source material into finalized markdown knowledge under Knowledge Manager control.

The product publishes its finalized knowledge to `/wiki` and exposes that knowledge through a separate read-only navigation layer.

## At a Glance

- Governed knowledge maintenance, not ad hoc note taking
- Finalized markdown as the unit of truth
- Controlled publication through the Knowledge Manager Interface
- Read-only consumption through Infopedia
- Stable knowledge for humans and downstream AI systems

## Why KMS Exists

KMS exists to preserve institutional knowledge in a durable, structured, and reviewable form.
It is designed for teams that need trusted knowledge for analytics, reporting, operational decisions, and AI-assisted work.

The product focuses on:

- turning scattered source material into curated markdown knowledge
- keeping truth controlled through a governed maintenance workflow
- separating knowledge maintenance from knowledge consumption
- providing stable knowledge for humans and downstream AI systems

## Core Product Surfaces

KMS provides three product surfaces:

### 1. Knowledge Manager Interface

The Knowledge Manager Interface, or KMI, is the governed maintenance surface. It is used to:

- start a knowledge maintenance run from a local source path
- inspect discovered sources and parsed content
- review proposed changes, diffs, contradictions, and rule violations
- approve, reject, defer, or escalate updates
- publish finalized knowledge to `/wiki`

KMI is the only sanctioned path for controlled knowledge publication.

### 2. Wiki Layer

The Wiki Layer is the finalized knowledge store. It contains the authoritative markdown pages that represent current truth.

The wiki layer is:

- human-readable
- structured for reuse by AI systems
- stable across maintenance cycles
- protected from uncontrolled edits outside the governed workflow

### 3. Infopedia

Infopedia is the read-only knowledge browsing layer. It helps people explore finalized knowledge through:

- tree-based navigation
- hyperlink traversal
- search and browse flows
- page-level reading and discovery

Infopedia never edits truth. It only presents finalized wiki content.

## How KMS Works

1. Raw source material is placed in a local source folder.
2. KMI starts a maintenance run against that source path.
3. KMS discovers, parses, and analyzes the source material.
4. KMS proposes updates, identifies contradictions, and applies validation rules.
5. The Knowledge Manager reviews the evidence and makes the publish decision.
6. Approved content is published to `/wiki` as finalized markdown.
7. Infopedia presents the finalized knowledge in a read-only browse experience.

## Core Functionality

### Source intake

KMS accepts local source folders as immutable upstream inputs.
Those sources may include documents, exports, notes, reports, and extracts.

### Knowledge maintenance

KMS analyzes source material, compares it with existing knowledge, identifies contradictions or gaps, and prepares proposed updates.

### Governance and review

KMS applies validation rules before publish.
The Knowledge Manager can inspect evidence, review diffs, resolve contradictions, and make final decisions.

### Finalization

Approved content is written to `/wiki` as finalized markdown knowledge.
That content becomes the governed source of truth for the product.

### Read-only consumption

Infopedia and downstream AI systems consume finalized knowledge without changing it.

## Roles

### Knowledge Manager
The Knowledge Manager owns maintenance runs and decides what becomes finalized knowledge. This role reviews evidence, handles conflicts, and approves publication.

### Knowledge Consumer

Knowledge Consumers read and navigate finalized knowledge in Infopedia. They do not modify published truth.

### Downstream AI System

Downstream AI systems use finalized markdown as governed context for assistance, planning, validation, and execution support.

## How to Use KMS

### For Knowledge Managers

1. Place the source material you want to maintain in a local source folder.
2. Open KMI and start a maintenance run from that source path.
3. Review the discovered files, proposed changes, diffs, and validation results.
4. Inspect contradictions, missing trace, freshness issues, and other rule violations.
5. Approve the changes that are ready for publication.
6. Reject, defer, or escalate items that need more work.
7. Publish the approved updates to `/wiki`.
8. Use the run record and validation output to confirm what changed.

### For Knowledge Consumers

1. Open Infopedia.
2. Browse the knowledge tree or search for a topic.
3. Follow links between related pages.
4. Read the finalized markdown content.
5. Use the knowledge as the trusted reference source for your work.

### For AI-assisted workflows

1. Use the finalized markdown in `/wiki` as the governed context.
2. Avoid using raw source material as final truth.
3. Ground prompts, drafting, and validation in the published knowledge set.
4. Keep maintenance decisions in KMI, not in the consumption layer.

## Operating Principles

- Curated knowledge over raw retrieval
- Determinism over improvisation
- One source of truth in `/wiki`
- Separation of maintenance and consumption
- Governance-first publication
- Structured markdown over free-form sprawl
- Human control over finalization
- Extensibility toward future agentic AI use

## Repository Map

This repository contains the product contract, design, implementation, and validation layers that support KMS development.

- [`intent/`](./intent/) holds product intent and feedback inputs
- [`plan/`](./plan/) holds the current iteration workspace
- [`design/`](./design/) holds the detailed design artifacts
- [`src/`](./src/) holds implementation code
- [`tests/`](./tests/) holds validation assets and test plans
- [`dev_log/`](./dev_log/) holds the permanent execution record
- [`dev_workflow/`](./dev_workflow/) holds the workflow prompts and runbooks
- [`skills/`](./skills/) holds reusable scoped procedures
- [`.codex/`](./.codex/) holds local working context and command references

## Getting Started

If you are new to KMS, start here:

1. Read the current product intent in [`intent/product-intent.md`](./intent/product-intent.md).
2. Review the high-level product context in [`.codex/project-context.md`](./.codex/project-context.md).
3. Read the detailed design files in [`design/system-design.md`](./design/system-design.md), [`design/architecture.md`](./design/architecture.md), [`design/ux-flows.md`](./design/ux-flows.md), and [`design/acceptance-criteria.md`](./design/acceptance-criteria.md).
4. Review the current plan files in [`plan/design-update.md`](./plan/design-update.md), [`plan/code-update.md`](./plan/code-update.md), and [`plan/test-update.md`](./plan/test-update.md) if you are changing behavior.
5. Use the workflow prompts in [`dev_workflow/`](./dev_workflow/) when updating the product.
6. Use `plan/*` and `design/*` as the source of truth when implementing code.

## Notes For Contributors

- KMS is not a generic document store.
- KMS is not a chat interface.
- KMS is not a raw search engine.
- KMS is a governed knowledge control plane built around finalized markdown knowledge.

## Product Boundaries

KMS is intentionally focused on governed knowledge maintenance and consumption.

- It is not a source connector platform.
- It is not a free-form editing surface for consumers.
- It is not a chatbot product.
- It is not a generic enterprise search engine.
- It is not an uncontrolled autonomous system.
