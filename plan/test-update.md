# Test Update Plan

## Purpose
Capture validation changes required by this cycle.

## Current intent signal
- Validate completed core domain contracts and existing scaffold compatibility.

## Required changes
1. `TEST-019`: Add unit tests covering all requested core contracts, their identifiers, relationships, state enums, derived projection flags, and validation behavior.
2. `TEST-019`: Preserve existing contract/scaffold tests.
3. `TEST-019`: Run unit discovery, Python compile checks, whitespace checks, and Codex contract validation.

## Existing drift or deviation
1. Existing contract tests only cover a small subset of the domain model.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-019`
2. `DEV-019`
3. `TEST-019`
