# Code Update Plan

## Current scope
- `DEV-022`: Add stdlib OpenAI Responses API client support to knowledge understanding.

## Implementation steps
1. Add `.env.example` placeholders and ignore local `.env` files.
2. Extend settings with AI enablement, model, timeout, and API key loading from environment or local `.env`.
3. Add a small server-side OpenAI Responses API client using stdlib HTTP and structured JSON prompts.
4. Wire knowledge understanding to call GPT-4o when configured, then validate and map outputs into existing candidate contracts.
5. Preserve deterministic extraction as fallback and record provider metadata in artifacts.

## Risks
- Avoid adding SDK dependencies unless necessary.
- Avoid network calls in unit tests.
- Validate AI output shape before creating candidates.
