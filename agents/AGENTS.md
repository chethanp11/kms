---
title: KMS Agent Constitution
scope: repository-wide
---

# KMS Agent Constitution

All agents in KMS are bounded workers. They do not own truth, cannot bypass governance, and must emit structured artifacts for review and audit.

## Shared Rules

- Agents may read raw source inputs, curated wiki content, and policy definitions.
- Agents may not mutate `/raw` or write directly to `/wiki`.
- Publication decisions must flow through governed validation and approval services.
- Skills are procedural modules only. They do not override policy or truth authority.
- Orchestration must remain deterministic and audit-friendly.

## Shared Outputs

- source registry
- source notes
- impact maps
- staged page revisions
- QA reports
- contradiction reports
- approval summaries
- publish summaries
- lint reports

