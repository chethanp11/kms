# Code Update Plan

## Current scope
- `DEV-024`: Implement runtime/API/UI/search changes for semantic candidate creation, duplicate rejection, per-candidate review decisions, source-path publication, and confidence-scored Infopedia search.

## Implementation steps
1. Extend candidate contracts/metadata to track review status, duplicate rationale, and modification text without weakening existing approval contracts.
2. Update knowledge-understanding extraction so fallback decomposition groups text semantically and AI instructions request semantic candidates; compare new candidates against existing wiki/search content and auto-reject duplicates.
3. Update candidate approval APIs to support selected approvals, rejections, and approval with modifications.
4. Publish approved candidates to `sources/` wiki paths and remove candidate-path publication.
5. Update KMI frontend controls/copy for select-all, per-candidate decisions, Publish to wiki, and no frontend LLM/provider/Knowledge Manager wording.
6. Update Infopedia API/UI to return keyword+semantic confidence scores for finalized wiki results.

## Risks
- Preserve deterministic no-network tests and fallback behavior.
- Preserve `/wiki` authority and approval gating.
- Existing route names should remain backwards-compatible where possible.
