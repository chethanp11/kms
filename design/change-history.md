# Design Change History

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Maintain a concise history of design changes that affect version behavior, validation expectations, or architecture.

## Intent sources
- Relevant sections from `intent/*` that triggered design changes

## Entry template
- Date: `[YYYY-MM-DD]`
- Version: `[Version]`
- Change summary: `[what changed in design]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, ACC-xxx, ARCH-xxx, API-xxx, DATA-xxx, AI-xxx, EVAL-xxx, DEV-xxx]`

## Entries
- `2026-04-06` | `v0.3` | Strengthened the template to use clearer design boundaries, stronger ID discipline, explicit validation evidence, and tighter workflow prompts. | The initial baseline was structurally sound but too generic for repeated real-world use. | `REQ-001`, `REQ-004`, `ARCH-005`, `AI-004`, `EVAL-005`, `DEV-001`
- `2026-04-06` | `v0.3` | Introduced an intent-first operating model with a dedicated `intent/` folder as the single human-editable source of truth, and updated downstream artifacts to be system-managed translations of intent. | The template needed a clearer split between human-authored product direction and workflow-managed design, code, tests, and logs. | `REQ-001`, `REQ-004`, `ARCH-001`, `AI-001`, `EVAL-005`, `DEV-007`
- `2026-04-06` | `v0.3` | Translated the generic template scaffolding into a KMS-specific governed knowledge-control design with explicit KMI, `/wiki`, and Infopedia layers, plus concrete maintenance, review, publication, and audit contracts. | The product intent now describes KMS in concrete terms and the design needed to match that domain instead of remaining template-shaped. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `AI-001`, `AI-002`, `AI-003`, `AI-004`, `AI-005`, `AI-006`, `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `EVAL-005`, `DEV-011`

## Notes
- Record only meaningful design changes, not every wording tweak.
- If the change alters release expectations, update the relevant version brief too.
