"""Deterministic source analysis for initial KMS runtime."""

from __future__ import annotations

from dataclasses import dataclass

from src.contracts import SourceDocument


@dataclass(frozen=True)
class AnalysisProposal:
    proposal_id: str
    title: str
    page_type: str
    summary: str
    source_document_id: str
    source_ref: str


def analyze_sources(documents: tuple[SourceDocument, ...]) -> tuple[AnalysisProposal, ...]:
    proposals: list[AnalysisProposal] = []
    for index, document in enumerate(documents, start=1):
        first_line = next((line.strip() for line in document.text.splitlines() if line.strip()), document.title)
        summary = first_line[:240]
        source_ref = str(document.metadata.get("relative_path", document.source_document_id))
        proposals.append(AnalysisProposal(f"proposal-{index}", document.title, "source-note", summary, document.source_document_id, source_ref))
    return tuple(proposals)


__all__ = ["AnalysisProposal", "analyze_sources"]
