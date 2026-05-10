"""Foundational ports for KMS components.

Ports define explicit contracts between services and stores so future concrete
components can be swapped without bypassing KMS authority boundaries.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.contracts import ApprovalRecord, KnowledgePage, MaintenanceRun, SourceBundle
from src.governance import QAReport


@runtime_checkable
class SourceRepository(Protocol):
    def discover(self, root_path: str) -> SourceBundle:
        """Return immutable source inventory for a raw source path."""


@runtime_checkable
class MetadataRepository(Protocol):
    def save_run(self, run: MaintenanceRun) -> None:
        """Persist operational run state."""

    def get_run(self, run_id: str) -> MaintenanceRun:
        """Fetch operational run state."""

    def save_approval(self, approval: ApprovalRecord) -> None:
        """Persist human approval evidence."""


@runtime_checkable
class WikiRepository(Protocol):
    def read_page(self, path: str) -> KnowledgePage:
        """Read finalized wiki content."""

    def write_page(self, page: KnowledgePage, *, approved: bool, qa_report: QAReport) -> None:
        """Write finalized wiki content only after governance passes."""


@runtime_checkable
class PolicyValidator(Protocol):
    def validate(self, page: KnowledgePage) -> QAReport:
        """Validate a candidate wiki page."""


@runtime_checkable
class ProjectionRepository(Protocol):
    def rebuild_from_wiki(self, pages: tuple[KnowledgePage, ...]) -> None:
        """Rebuild derived navigation/search projection from canonical wiki pages."""


__all__ = [
    "MetadataRepository",
    "PolicyValidator",
    "ProjectionRepository",
    "SourceRepository",
    "WikiRepository",
]
