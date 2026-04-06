# Change Log

## Purpose
Track meaningful changes to design, code, tests, evals, workflow, or template structure.

## Intent linkage
- Record when intent was interpreted into downstream changes.
- Link the relevant `intent/*` sections whenever a change originated from human direction.

## Entry template
- ID: `DEV-001`
- Date: `[YYYY-MM-DD]`
- Area: `design / code / test / eval / workflow / template`
- Change: `[what changed]`
- Reason: `[why it changed]`
- Linked IDs: `[REQ-xxx, ACC-xxx, ARCH-xxx, API-xxx, DATA-xxx, AI-xxx, TEST-xxx, EVAL-xxx, FB-xxx]`
- Intent sources: `[INT-PROD-xxx, INT-FB-xxx, INT-CON-xxx, INT-ITER-xxx]`

## Entries
- `DEV-001` | `2026-04-06` | `template` | Strengthened the repository into a more explicit design-driven AI application template with tighter traceability, workflow prompts, validation evidence, and copy-and-reuse guidance. | The original baseline was useful but too generic to consistently drive high-quality iterations. | `REQ-001`, `REQ-004`, `AI-004`, `EVAL-005` | `[intent not yet formalized at that stage]`
- `DEV-007` | `2026-04-06` | `template` | Introduced `intent/` as the single human-editable source of truth and updated guidance, workflow, design, tests, and logs to follow an intent -> design -> implementation -> validation loop. | The previous model still required humans to edit too many downstream artifacts directly. | `REQ-001`, `REQ-004`, `AI-001`, `EVAL-005` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`, `INT-FB-*`
- `DEV-015` | `2026-04-06` | `design` | Translated the generic template scaffolding into KMS-specific governed maintenance, publication, and browse design with explicit KMI, `/wiki`, and Infopedia layers. | The product intent now describes KMS concretely, and the downstream design had to stop reading like a reusable template. | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `ARCH-001`, `ARCH-002`, `ARCH-003`, `ARCH-004`, `ARCH-005`, `ARCH-006`, `AI-001`, `AI-002`, `AI-003`, `AI-004`, `AI-005`, `AI-006`, `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `EVAL-005` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`
- `DEV-021` | `2026-04-06` | `workflow` | Improved `dev_workflow/00-design-update.md` so it preserves intent detail, carries unresolved ambiguity into design artifacts, and explicitly maps intent themes to traceable design IDs. | The prior version said to translate intent into design, but it did not sufficiently protect against detail loss during summarization. | `REQ-001`, `REQ-002`, `REQ-004`, `ARCH-001`, `ARCH-003`, `AI-001`, `AI-002`, `TEST-001`, `EVAL-001`, `DEV-022` | `INT-PROD-*`, `INT-CON-*`, `INT-ITER-*`, `INT-FB-*`
- `DEV-026` | `2026-04-06` | `design` | Tightened the build scope to explicitly call out that `intent/iteration-intent.md` is still placeholder-only, so exact next-iteration scope cannot yet be derived. | The iteration-scope workflow cannot safely invent work when the human iteration intent is still empty. | `REQ-001`, `REQ-004`, `DEV-025` | `INT-ITER-*`
