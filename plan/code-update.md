# Code Update Plan

This file is generated from the active AppFlow cycle. Do not edit directly outside the workflow.

## Purpose
Capture implementation and scaffolding changes required by the current iteration.

## Current intent signal
- Update project scaffolding to match design requirements, including scripts scaffolding, while avoiding unnecessary `src/` expansion.

## Required changes
1. `DEV-015`: Add top-level `scripts/` scaffold with a README and deterministic validation helper for scaffold shape.
2. `DEV-015`: Keep current `src/` module families unchanged unless validation exposes a direct scaffold defect.
3. `DEV-015`: Preserve correction that `src/__init__.py` only exports present modules.

## Existing drift or deviation
1. Top-level `scripts/` scaffold is missing despite being part of the design repository structure.
2. No deterministic script currently checks project scaffold shape.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-015`
2. `DEV-015`
3. `TEST-015`
