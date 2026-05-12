# Code Update Plan

## Current scope
- `DEV-023`: Implement app runtime/API/UI changes for staged candidate approval and publication.

## Implementation steps
1. Add runtime methods to create candidates without publishing source-note pages, approve candidate IDs or all candidates, and publish approved candidates to `/wiki`.
2. Add API route functions/endpoints for candidate creation, approval, publication, and Infopedia refresh/readback.
3. Replace KMI UI with a three-stage stage-oriented flow and remove create-demo-source.
4. Improve Infopedia UI styling and display finalized wiki pages/search results clearly.
5. Add deterministic unit tests for the new staged workflow and frontend contract.

## Risks
- Existing `start_run` behavior should remain backwards-compatible for current tests.
- Do not require live OpenAI network calls in tests; use existing fallback/mocked settings.
