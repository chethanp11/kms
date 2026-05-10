# Test Update Plan

This file is generated from the active AppFlow cycle. Do not edit directly outside the workflow.

## Purpose
Capture validation changes required by the current iteration.

## Current intent signal
- Validate that the current scaffold, including scripts, matches the staged design baseline.

## Required changes
1. `TEST-015`: Add unit coverage for the scripts scaffold validation helper.
2. `TEST-015`: Run the scripts scaffold validator directly.
3. `TEST-015`: Run existing unit tests, source compile checks, `git diff --check`, and Codex contract validation.

## Existing drift or deviation
1. Existing tests validate `src/` scaffold behavior but do not validate top-level scripts scaffolding.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-015`
2. `DEV-015`
3. `TEST-015`
