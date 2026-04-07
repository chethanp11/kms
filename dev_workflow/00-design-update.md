# 00 Design Update

## Purpose
Translate `plan/design-update.md` and `dev_log/*` into concrete, KMS-specific design updates before any baseline sync or implementation work.

The goal is not to summarize the plan loosely. The goal is to preserve the important distinctions in the human input, convert them into traceable design artifacts, and leave a clear record of what was decided, deferred, or still unknown.

## Read first
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/change-log.md`
- `dev_log/deviations-log.md`
- `dev_log/issue-log.md`
- `dev_log/feedback-log.md`
- `dev_log/validation-log.md`

## Translation principles
- Treat `plan/*` as the highest-priority source for work items to translate into design.
- Preserve distinctions in the plan, such as role boundaries, governance boundaries, scope boundaries, and non-goals.
- Convert meaning into design artifacts, not into vague notes or paraphrases that lose operational detail.
- If multiple plan statements collapse into one design item, make sure the design still retains the original nuance and any conditional logic.
- If plan and log signals do not fit cleanly into the current design, capture that mismatch as an open question or issue instead of papering over it.
- Keep the design reusable, but do not strip out the KMS-specific truth boundaries, browse boundaries, or publication rules that are now part of the product plan.

## Update
- `design/system-design.md`
- `design/architecture.md`
- `design/acceptance-criteria.md`
- `design/ux-flows.md`
- `src/README.md` and `src/docs/` only if the project description or functionality needs to be reflected there
- `dev_log/change-log.md` when design updates are made
- `dev_log/decision-log.md` when design tradeoffs are made
- `dev_log/deviations-log.md` when the design update resolves or introduces a mismatch
- `dev_log/issue-log.md` when the design update exposes a gap or blocker

## Required translation method
1. Read the latest plan and operational evidence.
2. Extract the active product shape, version boundary, constraints, open questions, and any feedback-driven changes.
3. Map each meaningful plan theme to one or more concrete design artifacts and IDs.
4. Retain behavioral nuance in the design layer:
   - role separation
   - authority boundaries
   - supported and unsupported behaviors
   - source, publication, and consumption boundaries
   - required human checkpoints
   - audit and validation obligations
5. Add or revise `REQ-*`, `ACC-*`, `ARCH-*`, and `TEST-*` items as needed so the design can be tested and audited.
6. Record the resulting design choice, tradeoff, or gap in the relevant `dev_log/*` file.

## Checklist
1. Read the current plan and current operational evidence.
2. Identify what the design should become before baseline sync begins.
3. Convert plan and log signals into concrete design edits, not vague notes.
4. Preserve the meaningful detail from the plan in the resulting design.
5. Update design traceability implications if the design changes.
6. Record the resulting design change, decision, or gap in `dev_log/*` through the appropriate log file.

## Stop conditions
- Intent is too vague to translate into design
- Log evidence contradicts the intended direction and cannot be resolved safely
- Required design changes would exceed the current iteration without approval

## Done when
- The design update plan is explicit
- Required design files are updated or queued
- The related design changes are recorded in `dev_log/*`
- Baseline sync can start against the updated design
