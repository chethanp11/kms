"""Contradiction detection service."""

from __future__ import annotations

from src.contracts import ContradictionRecord, ContradictionSeverity, ContradictionStatus, SourceDocument


def detect_contradictions(documents: tuple[SourceDocument, ...], *, run_id: str) -> tuple[ContradictionRecord, ...]:
    records: list[ContradictionRecord] = []
    seen: dict[str, SourceDocument] = {}
    for document in documents:
        key = document.title.casefold()
        previous = seen.get(key)
        if previous and previous.text.strip() != document.text.strip():
            records.append(ContradictionRecord(
                contradiction_id=f"contradiction-{len(records)+1}", run_id=run_id, page_id="page-open-question", revision_id="revision-open-question",
                severity=ContradictionSeverity.MEDIUM, status=ContradictionStatus.OPEN, conflicting_claims=(previous.text[:120] or previous.title, document.text[:120] or document.title),
                source_refs=(str(previous.metadata.get("relative_path", previous.source_document_id)), str(document.metadata.get("relative_path", document.source_document_id))),
            ))
        seen.setdefault(key, document)
    return tuple(records)


__all__ = ["detect_contradictions"]
