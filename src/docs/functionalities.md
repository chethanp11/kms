# KMS Functionalities

## Core capabilities
- Accept a local source path for a governed maintenance run
- Discover source files and compare them with current finalized wiki content
- Draft markdown knowledge proposals with source references and contradiction flags
- Require Knowledge Manager approval, rejection, or escalation when needed
- Publish approved markdown into `/wiki`
- Serve read-only browse, search, and page navigation in Infopedia
- Record source trace, review decisions, freshness signals, and validation evidence

## User-facing workflows
1. Knowledge Manager starts a maintenance run from KMI.
2. The system analyzes source material and proposes knowledge updates.
3. The Knowledge Manager approves, rejects, revises, or escalates the proposal.
4. Approved knowledge is published to `/wiki`.
5. Knowledge Consumers browse the finalized knowledge through Infopedia.
6. Downstream AI systems consume finalized markdown as governed context.

## Functional boundaries
- Consumers cannot directly edit or publish finalized knowledge.
- AI can propose and summarize, but it cannot own truth.
- Raw source folders remain upstream inputs, not user-facing truth stores.

## Important notes
- Every changed page should be traceable back to source inputs and a review outcome.
- Every failed or rejected run should still leave an audit trail.
