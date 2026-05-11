# Design Update Plan

## Purpose
Capture design updates or explicit no-change decisions for this cycle.

## Current intent signal
- Complete core KMS domain contracts from `design/architecture.md` section 9.

## Required changes
1. `REQ-019`: Extend `design/architecture.md` entity field definitions so all requested core contracts are explicit: Run, SourceFile, SourceDocument, WikiPage, WikiPageRevision, ApprovalRecord, ContradictionRecord, QAReport, LintFinding, InfopediaNode, and SearchDocument.
2. `REQ-019`: Preserve authority semantics: `/wiki` remains canonical, metadata entities are operational, and Infopedia/search entities are derived projections.

## Existing drift or deviation
1. Section 9.5 listed field definitions for only a subset of requested entities.
2. `src/contracts` is currently absent from the src-only scaffold, while existing tests and modules expect it.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-019`
2. `DEV-019`
3. `TEST-019`
