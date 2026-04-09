# Design Update Skill

## Purpose
Translate `plan/*` and `dev_log/*` into concrete design updates before baseline sync or implementation.

## When to use
- At the start of an iteration.
- When intent changes and design must catch up.
- When logs reveal a design gap, deviation, or better approach.
- When copied-project docs in `src/README.md` or `src/docs/` need to reflect updated purpose or functionality.

## Read
- `plan/design-update.md`
- `plan/code-update.md`
- `plan/test-update.md`
- `dev_log/change-log.md`
- `dev_log/decision-log.md`
- `dev_log/deviations-log.md`
- `dev_log/issue-log.md`
- `dev_log/feedback-log.md`
- `dev_log/validation-log.md`
- `src/README.md`
- `src/docs/README.md`
- `src/docs/purpose.md`
- `src/docs/functionalities.md`

## Do
1. Read the current plan and the latest operational evidence together.
2. Determine what the design should change before implementation starts.
3. Update the relevant design artifacts and version notes.
4. Capture the resulting design change, decision, gap, or blocker in `dev_log/*`.
5. Flag any `src/README.md` or `src/docs/` updates needed to keep the copied project documentation aligned.

## Outputs
- Design updates ready for baseline sync.
- `dev_log/*` entries that record the design change, decision, or gap.
- A clear statement of what changed in intent-to-design translation.

## Rules and cautions
- Do not jump straight from intent to code.
- Do not hide design uncertainty inside implementation.
- Do not leave design changes undocumented in `dev_log/*`.
