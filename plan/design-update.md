# Design Update Plan

## Current scope
- `REQ-023`: Add a three-stage KMI candidate approval workflow backed by LLM extraction and Infopedia publication visibility.

## Design updates
1. Update KMI UX flow to present create-candidates, review/approve, and load-to-wiki stages.
2. Clarify candidate approval as a required boundary before wiki publication.
3. Clarify Infopedia displays finalized approved candidate pages only after publication.

## Boundaries
- Keep AI outputs proposal-oriented until user approval.
- Do not publish unapproved candidates.
- Do not modify framework/control-plane files in this app-mode cycle.
