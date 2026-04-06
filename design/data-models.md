# Data Models

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Document the canonical data structures used across the copied project. This file should describe stable schemas, not transient local variables.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/iteration-intent.md`

## Rules
- Each shared model gets a `DATA-*` ID.
- Reference `API-*` when a model crosses an interface boundary.
- Mark fields that are optional, sensitive, generated, or audit-critical.
- If a model stores AI outputs or tool traces, include provenance fields.

## Model catalog
| ID | Model | Purpose | Key fields | Linked IDs |
| --- | --- | --- | --- | --- |
| `DATA-001` | `SourceBundle` | Canonical description of a maintenance input set discovered from an immutable source folder. | `bundle_id`, `source_path`, `discovered_files`, `content_hashes`, `freshness_markers` | `API-001`, `REQ-001`, `REQ-004` |
| `DATA-002` | `KnowledgeRun` | Runtime record for one governed maintenance run. | `run_id`, `bundle_id`, `wiki_snapshot_ref`, `status`, `started_at`, `ended_at`, `trace_id` | `API-001`, `API-003`, `REQ-004` |
| `DATA-003` | `KnowledgeProposal` | Proposed wiki change set produced by the orchestrator. | `proposal_id`, `run_id`, `page_id`, `proposed_markdown`, `diff_summary`, `source_refs`, `confidence`, `contradiction_flags` | `API-002`, `REQ-001`, `REQ-002`, `AI-001`, `AI-005` |
| `DATA-004` | `WikiPageRecord` | Finalized wiki page metadata and content reference. | `page_id`, `title`, `path`, `markdown`, `source_refs`, `published_at`, `last_reviewed_at` | `API-003`, `API-004`, `REQ-003`, `REQ-004` |
| `DATA-005` | `ReviewDecision` | Knowledge Manager decision about a proposal. | `decision_id`, `proposal_id`, `decision`, `reviewer`, `rationale`, `escalation_target`, `decision_at` | `API-002`, `ACC-002`, `REQ-002` |
| `DATA-006` | `ValidationRecord` | Audit and validation evidence for a run or review decision. | `validation_id`, `run_id`, `checks`, `result`, `evidence`, `notes`, `recorded_at` | `TEST-004`, `EVAL-005`, `REQ-004` |

## Per-model checklist
- Field name
- Type
- Required or optional
- Validation constraints
- Source of truth or generating component
- Retention or deletion rule if relevant

## Audit and privacy notes
- Source bundle paths, hashes, and page metadata may be logged safely.
- Do not expose raw secret material or private credentials to prompts or user-visible output.
- Keep provenance references explicit so review and validation can reconstruct how a page changed.

## Design rule
Keep models minimal, version-aware, and aligned with the actual system contracts. Do not use this file to describe implementation-only helper objects.
