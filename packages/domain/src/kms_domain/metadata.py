from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

EntityId = str
RunStatus = Literal[
    "created",
    "in_progress",
    "completed",
    "completed_with_warnings",
    "blocked",
    "failed",
]
RevisionStatus = Literal["staged", "review_required", "approved", "rejected", "finalized"]
ApprovalDecision = Literal["approved", "rejected", "deferred", "escalated"]
Severity = Literal["info", "warning", "error"]
ProjectionStatus = Literal["current", "stale", "missing"]


@dataclass
class Run:
    run_id: EntityId
    status: RunStatus
    source_path: str
    created_at: str
    domain_hint: str | None = None
    run_notes: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    created_by: str | None = None
    current_stage: str | None = None


@dataclass
class SourceFile:
    source_file_id: EntityId
    run_id: EntityId
    path: str
    file_type: str
    hash: str
    parse_status: Literal["discovered", "parsed", "unsupported", "failed"]
    discovered_at: str
    error_summary: str | None = None


@dataclass
class SourceDocument:
    source_document_id: EntityId
    source_file_id: EntityId
    run_id: EntityId
    content_type: str
    normalized_text: str
    summary: str
    created_at: str
    title: str | None = None
    status: Literal["parsed", "normalized", "rejected"] = "parsed"
    parse_metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class SourceNote:
    source_note_id: EntityId
    run_id: EntityId
    source_document_id: EntityId
    title: str
    slug: str
    summary: str
    source_refs: list[str] = field(default_factory=list)
    extracted_signals: list[str] = field(default_factory=list)
    review_required: bool = True
    created_at: str = ""


@dataclass
class IntakeArtifact:
    artifact_id: EntityId
    run_id: EntityId
    artifact_type: str
    status: Literal["created", "updated", "failed"]
    path: str | None = None
    summary: str = ""
    created_at: str = ""


@dataclass
class WikiPage:
    page_id: EntityId
    slug: str
    title: str
    page_type: str
    status: Literal["draft", "finalized", "deprecated"]
    freshness_status: ProjectionStatus
    confidence_status: Literal["low", "medium", "high"]
    updated_at: str
    current_revision_id: EntityId | None = None


@dataclass
class WikiPageRevision:
    revision_id: EntityId
    page_id: EntityId
    run_id: EntityId
    status: RevisionStatus
    change_type: Literal["create", "update", "no-op", "review"]
    section_changes: list[str] = field(default_factory=list)
    source_trace_ids: list[str] = field(default_factory=list)
    diff_summary: str = ""
    created_at: str = ""
    finalized_at: str | None = None


@dataclass
class ImpactRecord:
    impact_id: EntityId
    run_id: EntityId
    source_document_id: EntityId
    impact_type: str
    summary: str
    created_at: str
    target_page_id: EntityId | None = None


@dataclass
class ContradictionRecord:
    contradiction_id: EntityId
    run_id: EntityId
    severity: Severity
    status: Literal["open", "reviewing", "resolved", "escalated"]
    conflicting_claims: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    created_at: str = ""
    page_id: EntityId | None = None
    revision_id: EntityId | None = None
    open_question_page_id: EntityId | None = None
    resolved_at: str | None = None


@dataclass
class QAReport:
    qa_report_id: EntityId
    run_id: EntityId
    status: Literal["pass", "warn", "fail"]
    rule_ids: list[str] = field(default_factory=list)
    summary: str = ""
    created_at: str = ""
    revision_id: EntityId | None = None


@dataclass
class ApprovalRecord:
    approval_id: EntityId
    revision_id: EntityId
    decision: ApprovalDecision
    policy_version: str
    reviewed_at: str
    reviewer_id: str | None = None
    reason: str | None = None
    override_requested: bool = False


@dataclass
class LintFinding:
    lint_finding_id: EntityId
    run_id: EntityId
    severity: Severity
    code: str
    message: str
    created_at: str
    page_id: EntityId | None = None
    revision_id: EntityId | None = None
    resolved_at: str | None = None


@dataclass
class InfopediaNode:
    node_id: EntityId
    page_id: EntityId
    title: str
    slug: str
    path: str
    freshness_status: ProjectionStatus
    status: Literal["active", "hidden"]
    updated_at: str
    parent_node_id: EntityId | None = None


@dataclass
class SearchDocument:
    search_doc_id: EntityId
    title: str
    content: str
    status: ProjectionStatus
    updated_at: str
    page_id: EntityId | None = None
    run_id: EntityId | None = None


class MetadataStore(Protocol):
    def create_run(self, run: Run) -> Run: ...

    def get_run(self, run_id: EntityId) -> Run | None: ...

    def list_runs(self) -> list[Run]: ...

    def upsert_source_file(self, source_file: SourceFile) -> SourceFile: ...

    def list_source_files(self, run_id: EntityId) -> list[SourceFile]: ...

    def upsert_source_document(self, source_document: SourceDocument) -> SourceDocument: ...

    def list_source_documents(self, run_id: EntityId) -> list[SourceDocument]: ...

    def upsert_source_note(self, source_note: SourceNote) -> SourceNote: ...

    def list_source_notes(self, run_id: EntityId) -> list[SourceNote]: ...

    def record_intake_artifact(self, artifact: IntakeArtifact) -> IntakeArtifact: ...

    def list_intake_artifacts(self, run_id: EntityId) -> list[IntakeArtifact]: ...

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage: ...

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None: ...

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision: ...

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord: ...

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord: ...
