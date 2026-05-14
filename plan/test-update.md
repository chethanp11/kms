# Test Update Plan

## Current scope
- `TEST-024`: Validate semantic candidate decomposition, duplicate auto-rejection visibility, per-candidate review decisions, source-path publication, and confidence-scored Infopedia search.

## Validation
- Add/extend unit coverage for duplicate comparison and auto-rejected candidates that remain visible in candidate APIs.
- Add/extend runtime coverage for approve selected, reject selected, approve with modifications, publish approved to `sources/`, and no `candidates/` wiki folder.
- Extend frontend scaffold tests for Select all, per-candidate Approve/Reject/Approve with Mods, Publish to wiki copy, and absence of LLM/provider/Knowledge Manager frontend copy.
- Extend Infopedia tests for finalized-only semantic+keyword search confidence scores.
- Run targeted tests first, then unit discovery, Python compile, and whitespace checks.
