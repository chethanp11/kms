# Code Update Plan

## Current scope
- `DEV-021`: Add deterministic stdlib candidate extraction and governed artifact wiring to the existing runtime slice.

## Implementation steps
1. Add domain contracts for candidate type, confidence, relevance, candidate records, extraction bundles, and draft bundles.
2. Implement deterministic extraction heuristics as a bounded stand-in for AI-assisted understanding.
3. Add relevance filtering, confidence scoring, and inspectable JSON/markdown artifact renderers.
4. Wire extraction between parsing and source analysis/drafting; block publication when generated candidate review is pending.
5. Add tests proving candidates remain proposals and do not auto-publish `/wiki`.

## Risks
- Do not make candidate artifacts authoritative.
- Do not let `auto_approve` bypass candidate review.
- Preserve current source-note runtime behavior where possible while adding the new governance boundary.
