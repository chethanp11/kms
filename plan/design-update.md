# Design Update Plan

## Current scope
- `REQ-021`: Introduce governed AI-assisted knowledge understanding as proposal-only Run artifacts.

## Design updates
1. Extend architecture with a bounded knowledge understanding service between parsing and drafting.
2. Define candidate knowledge as operational artifacts, not canonical truth.
3. Document candidate categories, relevance/confidence requirements, contradiction candidate handling, and review/audit boundaries.
4. Update acceptance criteria so candidate outputs fail closed before publish and remain subject to approval.

## Boundaries
- `/wiki` remains the only finalized truth store.
- Candidate and draft artifacts stay in metadata/artifact storage until reviewed and approved.
- AI-assisted extraction may propose and score; it must not publish, approve, or silently rewrite canonical knowledge.
