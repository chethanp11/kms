# KMS

## Purpose
This is the application README for KMS, the governed knowledge maintenance and publishing system.

## Application summary
- Product idea: turn immutable raw source material into finalized markdown knowledge under controlled review.
- Primary users: Knowledge Managers, Knowledge Consumers, and downstream AI systems.
- Core value: preserve trusted institutional knowledge in `/wiki` while keeping maintenance, publication, and browsing separate.
- Current version: `v0.3`

## Project docs
- Application purpose and functionality details live in `src/docs/`.
- This README stays concise and points to the authoritative docs.

## Design rule
`src/` is system-managed and should implement behavior already defined in `design/`, which is itself generated from `intent/`. Do not let source intake rules, governance policy, publication gating, or browse-only behavior live only in code if they materially affect user-visible behavior.

## Startup rule
- `src/` may be empty at the beginning of a copied project.
- Create scaffolding from design first.
- If components already exist, refactor them as needed to match design.
- Add new modules only when the design calls for them.

## Recommended structure
- `app/`: application entrypoints, transport layer wiring, and runtime bootstrapping.
- `agents/`: maintenance assistants or reviewer roles if the project uses them.
- `workflows/`: source intake, proposal generation, review, publication, and browse flows.
- `tools/`: filesystem, wiki publication, and navigation adapters.
- `services/`: deterministic domain logic for governance, traceability, and publication rules.
- `models/`: typed request, response, event, and persistence schemas.
- `config/`: runtime configuration, environment loading, and feature flags.
- `utils/`: small shared helpers with low domain significance.

## Practical rules
- Humans should usually not edit `src/` directly in this workflow; Codex should update it through intent-driven design work.
- Add folders only when the design requires them.
- Keep prompt-building logic close to the owning workflow or agent.
- Keep external side effects inside `tools/` or clearly named adapters.
- Put schemas that cross module boundaries in `models/`.
- Prefer comments that reference IDs such as `REQ-*` or `AI-*` over vague explanatory comments.
- Keep evaluation harnesses, fixtures, and benchmark data in `tests/`, not `src/`, unless they are shipped product features.
