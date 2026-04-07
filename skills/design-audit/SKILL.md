# Design Audit Skill

## Purpose
Validate whether implementation, tests, and logs remain aligned with the current plan, design, and version target.

## When to use
- After a development cycle completes.
- When new behavior is added.
- When design artifacts change.
- Before closeout when drift is a real risk.

## Read
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/change-log.md`
- `dev_log/decision-log.md`
- `dev_log/deviations-log.md`
- `dev_log/validation-log.md`
- `design/system-design.md`
- `design/architecture.md`
- `design/acceptance-criteria.md`
- `design/ux-flows.md`
- `src/` and `tests/` summaries
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`

## Do
1. Review the current plan, design artifacts, and active requirements.
2. Compare implementation behavior to documented acceptance criteria.
3. Check for undocumented behavior or drift from either plan or design.
4. Identify any missing or outdated traceability links.
5. Confirm copied-project documentation still matches current purpose and functionality.

## Outputs
- A concise audit summary.
- A list of findings categorized by design drift, missing tests, or scope creep.
- Recommended updates to design, tests, or backlog.

## Rules and cautions
- Do not approve implementation based solely on tests; verify against design.
- Do not approve design if it no longer reflects current intent.
- Do not make unapproved behavior changes during the audit.
- Flag any ambiguity as a design issue rather than resolving it with assumptions.
