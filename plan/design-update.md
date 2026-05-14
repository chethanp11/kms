# Design Update Plan

## Current scope
- `REQ-024`: Intelligent semantic candidate decomposition with duplicate comparison against existing finalized source/wiki knowledge and KMI duplicate awareness.
- `REQ-025`: KMI candidate review UX with select-all, per-candidate Approve/Reject/Approve with Mods, Publish to wiki copy, and no frontend LLM/provider/Knowledge Manager implementation wording.
- `REQ-026`: Approved candidate publication into `sources/` wiki pages only; no `candidates/` wiki folder.
- `REQ-027`: Infopedia semantic-plus-keyword search with confidence scores per finalized source/wiki result.

## Design updates
1. Update candidate-governance design so extraction is semantic decomposition first, duplicate comparison is automatic, duplicates are auto-rejected, and rejected duplicates remain visible in KMI.
2. Update KMI UX flow: create candidates, select/review with per-candidate decisions and optional modification text, then publish approved candidates.
3. Update wiki publication design so candidate-derived finalized pages use `sources/` paths and candidate artifacts remain run/metadata artifacts only.
4. Update Infopedia search design so results include confidence scores derived from semantic and keyword signals.

## Boundaries
- AI/LLM implementation details stay server-side and must not appear in frontend copy.
- Candidate artifacts remain proposal/review artifacts until approved and published.
- Infopedia remains read-only and only searches finalized wiki pages by default.
- Do not modify framework/control-plane files in this app-mode cycle.
