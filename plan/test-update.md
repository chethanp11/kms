# Test Update Plan

## Purpose
Capture validation changes required by this cycle.

## Current intent signal
- Validate `src/`-only scaffold shape and absence of rejected scaffold locations.

## Required changes
1. `TEST-018`: Replace stale component/script scaffold tests with tests for the detailed `src/`-only runtime scaffold.
2. `TEST-018`: Validate key placeholder files exist under `src/` and rejected folders do not exist.
3. `TEST-018`: Run unit tests, Python compile checks for `src`, whitespace checks, and Codex contract validation.

## Existing drift or deviation
1. Tests currently reflect prior scaffold attempts rather than the corrected `src/`-only expectation.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-018`
2. `DEV-018`
3. `TEST-018`
