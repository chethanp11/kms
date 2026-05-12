# Design Update Plan

## Current scope
- `REQ-022`: Configure API-key-backed GPT-4o use for AI-assisted knowledge understanding while preserving governance boundaries.

## Design updates
1. Document server-side OpenAI configuration through local environment variables and `.env` placeholders.
2. Clarify that API-backed extraction is optional and must fail closed to deterministic extraction when unavailable.
3. Preserve candidate artifacts as proposal-only Run outputs; API responses cannot publish or approve `/wiki` changes.

## Boundaries
- Real API keys must never be committed.
- KMI/Infopedia clients must not receive the API key.
- `/wiki` publication still requires deterministic validation and Knowledge Manager approval.
