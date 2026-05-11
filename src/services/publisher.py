"""Governed publisher: the only service that writes finalized pages to /wiki."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.contracts import ApprovalRecord, GateResult, KnowledgePage, QAReport, ValidationError
from src.services.approval import approval_allows_publish
from src.storage.wiki_store import WikiStore


@dataclass(frozen=True)
class PublishSummary:
    page_path: str
    output_path: Path
    published: bool
    message: str


def publish_page(page: KnowledgePage, qa_report: QAReport, approval: ApprovalRecord | None, wiki_store: WikiStore) -> PublishSummary:
    if qa_report.result is not GateResult.PASS:
        raise ValidationError("cannot publish page with failing QA report")
    if not approval_allows_publish(approval):
        raise ValidationError("cannot publish page without approved human decision")
    output_path = wiki_store.write_page(page)
    return PublishSummary(page.path, output_path, True, "published")


__all__ = ["PublishSummary", "publish_page"]
