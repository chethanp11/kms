# Code Update Plan

## Purpose
Capture implementation changes required by this cycle.

## Current intent signal
- Implement complete core domain contracts in `src/contracts` only as needed.

## Required changes
1. `DEV-019`: Restore and complete `src/contracts/__init__.py` with dataclass contracts for Run, SourceFile, SourceDocument, WikiPage, WikiPageRevision, ApprovalRecord, ContradictionRecord, QAReport, LintFinding, InfopediaNode, and SearchDocument.
2. `DEV-019`: Include enums/states needed by the design: run state, revision state, page status, confidence, freshness, approval decision, contradiction severity/status, QA result, lint severity/status.
3. `DEV-019`: Preserve compatibility with existing tests that instantiate `KnowledgePage`, `SourceFile`, `MaintenanceRun`, and `ApprovalRecord`.

## Existing drift or deviation
1. `src/contracts` is missing, causing current imports to be fragile or failing.

## Open questions or blockers
1. None.

## Linked IDs
1. `REQ-019`
2. `DEV-019`
3. `TEST-019`
