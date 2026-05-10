"""Deterministic in-memory foundational stores for tests and early components."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.contracts import ApprovalRecord, KnowledgePage, MaintenanceRun, ValidationError
from src.governance import QAReport


@dataclass
class InMemoryMetadataStore:
    """Supporting operational store; never authoritative for knowledge truth."""

    runs: dict[str, MaintenanceRun] = field(default_factory=dict)
    approvals: dict[str, ApprovalRecord] = field(default_factory=dict)

    def save_run(self, run: MaintenanceRun) -> None:
        self.runs[run.run_id] = run

    def get_run(self, run_id: str) -> MaintenanceRun:
        try:
            return self.runs[run_id]
        except KeyError as exc:
            raise ValidationError(f"unknown run: {run_id}") from exc

    def save_approval(self, approval: ApprovalRecord) -> None:
        self.approvals[approval.approval_id] = approval


@dataclass
class InMemoryWikiStore:
    """Canonical wiki store enforcing governed writes."""

    pages: dict[str, KnowledgePage] = field(default_factory=dict)

    def read_page(self, path: str) -> KnowledgePage:
        try:
            return self.pages[path]
        except KeyError as exc:
            raise ValidationError(f"unknown wiki page: {path}") from exc

    def write_page(self, page: KnowledgePage, *, approved: bool, qa_report: QAReport) -> None:
        if not approved:
            raise ValidationError("wiki writes require approval")
        if not qa_report.can_publish:
            raise ValidationError("wiki writes require passing QA report")
        self.pages[page.path] = page


@dataclass
class InMemoryProjectionStore:
    """Derived projection store rebuildable from canonical wiki pages."""

    nodes: dict[str, str] = field(default_factory=dict)

    def rebuild_from_wiki(self, pages: tuple[KnowledgePage, ...]) -> None:
        self.nodes = {page.path: page.title for page in sorted(pages, key=lambda item: item.path)}


__all__ = ["InMemoryMetadataStore", "InMemoryProjectionStore", "InMemoryWikiStore"]
