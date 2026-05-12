"""Core KMS domain contracts.

These contracts intentionally stay lightweight and stdlib-only so the current
src scaffold can validate KMS identities, relationships, and state boundaries
before persistence or API serializers are introduced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Mapping


class ValidationError(ValueError):
    """Raised when a KMS contract receives invalid data."""


class RunState(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class RevisionState(str, Enum):
    STAGED = "staged"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    FINALIZED = "finalized"


class PageStatus(str, Enum):
    DRAFT = "draft"
    REVIEW_REQUIRED = "review_required"
    FINALIZED = "finalized"
    ARCHIVED = "archived"


class FreshnessStatus(str, Enum):
    CURRENT = "current"
    STALE = "stale"
    UNKNOWN = "unknown"


class ConfidenceStatus(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ParseStatus(str, Enum):
    DISCOVERED = "discovered"
    PARSED = "parsed"
    PARTIAL = "partial"
    FAILED = "failed"


class ChangeType(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    NO_OP = "no_op"


class KnowledgeCandidateType(str, Enum):
    ENTITY = "entity"
    PROCESS = "process"
    METRIC = "metric"
    DECISION = "decision"
    CONCEPT = "concept"
    CONTRADICTION = "contradiction"


class ApprovalDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CHANGES = "needs_changes"


class ContradictionSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKING = "blocking"


class ContradictionStatus(str, Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    ACCEPTED_RISK = "accepted_risk"


class GateResult(str, Enum):
    PASS = "pass"
    REVIEW_REQUIRED = "review_required"
    BLOCK = "block"


QAResult = GateResult


class LintSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


class LintStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9/-]*$")


def _validate_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field_name} must be a non-empty string")


def _validate_identifier(value: str, field_name: str) -> None:
    _validate_non_empty(value, field_name)
    if not _IDENTIFIER_RE.match(value):
        raise ValidationError(f"{field_name} must be a stable identifier")


def _validate_relative_posix_path(value: str, field_name: str, *, suffix: str | None = None) -> None:
    _validate_non_empty(value, field_name)
    if value.startswith("/") or ".." in value.split("/") or "//" in value:
        raise ValidationError(f"{field_name} must be a safe relative POSIX path")
    if suffix and not value.endswith(suffix):
        raise ValidationError(f"{field_name} must end with {suffix}")


def _validate_sha256(value: str, field_name: str = "sha256") -> None:
    if not isinstance(value, str) or not _SHA256_RE.match(value):
        raise ValidationError(f"{field_name} must be a lowercase SHA-256 digest")


def _tuple(value: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    return tuple(value or ())


def _mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(value or {})


@dataclass(frozen=True)
class MaintenanceRun:
    run_id: str
    source_path: str
    state: RunState = RunState.CREATED
    domain_hint: str = ""
    run_notes: str = ""
    created_at: str = ""
    started_at: str = ""
    completed_at: str = ""
    created_by: str = ""
    summary_counts: Mapping[str, int] = field(default_factory=dict)
    blocked_reason: str = ""

    def __post_init__(self) -> None:
        _validate_identifier(self.run_id, "run_id")
        _validate_non_empty(self.source_path, "source_path")
        object.__setattr__(self, "summary_counts", dict(self.summary_counts))

    @property
    def status(self) -> str:
        return self.state.value


Run = MaintenanceRun


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    sha256: str
    size_bytes: int
    media_type: str = "application/octet-stream"
    source_file_id: str = ""
    run_id: str = ""
    discovered_at: str = ""
    parse_status: ParseStatus = ParseStatus.DISCOVERED
    document_count: int = 0
    error_summary: str = ""

    def __post_init__(self) -> None:
        _validate_relative_posix_path(self.relative_path, "relative_path")
        _validate_sha256(self.sha256)
        if self.size_bytes < 0:
            raise ValidationError("size_bytes must be non-negative")
        if self.document_count < 0:
            raise ValidationError("document_count must be non-negative")
        if self.source_file_id:
            _validate_identifier(self.source_file_id, "source_file_id")
        if self.run_id:
            _validate_identifier(self.run_id, "run_id")

    @property
    def path(self) -> str:
        return self.relative_path

    @property
    def file_type(self) -> str:
        return self.media_type

    @property
    def hash(self) -> str:
        return self.sha256


@dataclass(frozen=True)
class SourceBundle:
    root_path: str
    files: tuple[SourceFile, ...]
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_non_empty(self.root_path, "root_path")
        object.__setattr__(self, "files", tuple(self.files))
        object.__setattr__(self, "warnings", _tuple(self.warnings))


@dataclass(frozen=True)
class SourceDocument:
    source_document_id: str
    source_file_id: str
    run_id: str
    title: str
    content_type: str
    text: str
    structure: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    parse_status: ParseStatus = ParseStatus.PARSED
    created_at: str = ""
    error_summary: str = ""

    def __post_init__(self) -> None:
        for field_name in ("source_document_id", "source_file_id", "run_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        _validate_non_empty(self.title, "title")
        _validate_non_empty(self.content_type, "content_type")
        object.__setattr__(self, "structure", _mapping(self.structure))
        object.__setattr__(self, "metadata", _mapping(self.metadata))


@dataclass(frozen=True)
class KnowledgePage:
    page_type: str
    path: str
    title: str
    body: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    page_id: str = ""
    slug: str = ""
    status: PageStatus = PageStatus.FINALIZED
    freshness_status: FreshnessStatus = FreshnessStatus.UNKNOWN
    confidence_status: ConfidenceStatus = ConfidenceStatus.UNKNOWN
    current_revision_id: str = ""
    updated_at: str = ""
    source_refs: tuple[str, ...] = ()
    owners: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _validate_non_empty(self.page_type, "page_type")
        _validate_relative_posix_path(self.path, "path", suffix=".md")
        _validate_non_empty(self.title, "title")
        if self.page_id:
            _validate_identifier(self.page_id, "page_id")
        if self.current_revision_id:
            _validate_identifier(self.current_revision_id, "current_revision_id")
        slug = self.slug or self.path[:-3]
        if not _SLUG_RE.match(slug):
            raise ValidationError("slug must be lowercase POSIX-safe text")
        object.__setattr__(self, "slug", slug)
        object.__setattr__(self, "metadata", _mapping(self.metadata))
        object.__setattr__(self, "source_refs", _tuple(self.source_refs))
        object.__setattr__(self, "owners", _tuple(self.owners))
        object.__setattr__(self, "tags", _tuple(self.tags))

    def to_markdown(self) -> str:
        frontmatter: dict[str, Any] = {
            "title": self.title,
            "type": self.page_type,
            **self.metadata,
        }
        lines = ["---"]
        for key in sorted(frontmatter):
            lines.append(f"{key}: {frontmatter[key]}")
        lines.extend(["---", "", f"# {self.title}", "", self.body.rstrip(), ""])
        return "\n".join(lines)


WikiPage = KnowledgePage


@dataclass(frozen=True)
class WikiPageRevision:
    revision_id: str
    page_id: str
    run_id: str
    status: RevisionState
    change_type: ChangeType
    section_changes: tuple[str, ...]
    source_trace_ids: tuple[str, ...]
    diff_summary: str
    created_at: str = ""
    finalized_at: str = ""

    def __post_init__(self) -> None:
        for field_name in ("revision_id", "page_id", "run_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        object.__setattr__(self, "section_changes", _tuple(self.section_changes))
        object.__setattr__(self, "source_trace_ids", _tuple(self.source_trace_ids))
        if not self.source_trace_ids:
            raise ValidationError("source_trace_ids must contain at least one source trace")
        _validate_non_empty(self.diff_summary, "diff_summary")


@dataclass(frozen=True)
class ImpactRecord:
    impact_id: str
    run_id: str
    source_document_id: str
    page_id: str
    affected_sections: tuple[str, ...]
    rationale: str = ""

    def __post_init__(self) -> None:
        for field_name in ("impact_id", "run_id", "source_document_id", "page_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        object.__setattr__(self, "affected_sections", _tuple(self.affected_sections))


@dataclass(frozen=True)
class ContradictionRecord:
    contradiction_id: str
    run_id: str
    page_id: str
    revision_id: str
    severity: ContradictionSeverity
    status: ContradictionStatus
    conflicting_claims: tuple[str, ...]
    source_refs: tuple[str, ...]
    open_question_page_id: str = ""
    created_at: str = ""

    def __post_init__(self) -> None:
        for field_name in ("contradiction_id", "run_id", "page_id", "revision_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        if self.open_question_page_id:
            _validate_identifier(self.open_question_page_id, "open_question_page_id")
        object.__setattr__(self, "conflicting_claims", _tuple(self.conflicting_claims))
        object.__setattr__(self, "source_refs", _tuple(self.source_refs))
        if len(self.conflicting_claims) < 2:
            raise ValidationError("conflicting_claims must contain at least two claims")
        if not self.source_refs:
            raise ValidationError("source_refs must contain at least one source reference")


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    revision_id: str
    decision: ApprovalDecision
    reviewer_id: str
    reason: str = ""
    reviewed_at: str = ""
    override_requested: bool = False
    policy_version: str = ""

    def __post_init__(self) -> None:
        for field_name in ("approval_id", "revision_id", "reviewer_id"):
            _validate_identifier(getattr(self, field_name), field_name)


@dataclass(frozen=True)
class PolicyFinding:
    rule_id: str
    severity: str
    message: str

    def __post_init__(self) -> None:
        _validate_identifier(self.rule_id, "rule_id")
        _validate_non_empty(self.severity, "severity")
        _validate_non_empty(self.message, "message")


@dataclass(frozen=True)
class QAReport:
    result: GateResult
    findings: tuple[PolicyFinding, ...] = ()
    qa_report_id: str = ""
    run_id: str = ""
    revision_id: str = ""
    policy_version: str = ""
    checked_at: str = ""
    summary: str = ""

    def __post_init__(self) -> None:
        if self.qa_report_id:
            _validate_identifier(self.qa_report_id, "qa_report_id")
        if self.run_id:
            _validate_identifier(self.run_id, "run_id")
        if self.revision_id:
            _validate_identifier(self.revision_id, "revision_id")
        object.__setattr__(self, "findings", tuple(self.findings))

    @property
    def can_publish(self) -> bool:
        return self.result is GateResult.PASS


@dataclass(frozen=True)
class LintFinding:
    lint_finding_id: str
    severity: LintSeverity
    status: LintStatus
    message: str
    page_id: str = ""
    revision_id: str = ""
    run_id: str = ""
    path: str = ""
    rule_id: str = ""
    created_at: str = ""

    def __post_init__(self) -> None:
        _validate_identifier(self.lint_finding_id, "lint_finding_id")
        for field_name in ("page_id", "revision_id", "run_id", "rule_id"):
            value = getattr(self, field_name)
            if value:
                _validate_identifier(value, field_name)
        if self.path:
            _validate_relative_posix_path(self.path, "path")
        _validate_non_empty(self.message, "message")


@dataclass(frozen=True)
class InfopediaNode:
    node_id: str
    page_id: str
    slug: str
    title: str
    page_type: str
    parent_node_id: str = ""
    children: tuple[str, ...] = ()
    related_page_ids: tuple[str, ...] = ()
    breadcrumbs: tuple[str, ...] = ()
    updated_at: str = ""

    def __post_init__(self) -> None:
        for field_name in ("node_id", "page_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        if self.parent_node_id:
            _validate_identifier(self.parent_node_id, "parent_node_id")
        if not _SLUG_RE.match(self.slug):
            raise ValidationError("slug must be lowercase POSIX-safe text")
        _validate_non_empty(self.title, "title")
        _validate_non_empty(self.page_type, "page_type")
        object.__setattr__(self, "children", _tuple(self.children))
        object.__setattr__(self, "related_page_ids", _tuple(self.related_page_ids))
        object.__setattr__(self, "breadcrumbs", _tuple(self.breadcrumbs))

    @property
    def is_projection(self) -> bool:
        return True


@dataclass(frozen=True)
class SearchDocument:
    search_doc_id: str
    source_kind: str
    source_id: str
    title: str
    content: str
    content_hash: str
    path: str = ""
    tags: tuple[str, ...] = ()
    updated_at: str = ""

    def __post_init__(self) -> None:
        for field_name in ("search_doc_id", "source_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        _validate_non_empty(self.source_kind, "source_kind")
        _validate_non_empty(self.title, "title")
        _validate_non_empty(self.content, "content")
        _validate_sha256(self.content_hash, "content_hash")
        if self.path:
            _validate_relative_posix_path(self.path, "path")
        object.__setattr__(self, "tags", _tuple(self.tags))

    @property
    def is_projection(self) -> bool:
        return True


@dataclass(frozen=True)
class KnowledgeCandidate:
    candidate_id: str
    run_id: str
    source_document_id: str
    source_ref: str
    candidate_type: KnowledgeCandidateType
    title: str
    excerpt: str
    relevance_score: float
    confidence_score: float
    rationale: str
    target_slug: str = ""
    related_candidate_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("candidate_id", "run_id", "source_document_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        _validate_non_empty(self.source_ref, "source_ref")
        _validate_non_empty(self.title, "title")
        _validate_non_empty(self.excerpt, "excerpt")
        _validate_non_empty(self.rationale, "rationale")
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValidationError("relevance_score must be between 0.0 and 1.0")
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValidationError("confidence_score must be between 0.0 and 1.0")
        if self.target_slug and not _SLUG_RE.match(self.target_slug):
            raise ValidationError("target_slug must be lowercase POSIX-safe text")
        object.__setattr__(self, "related_candidate_ids", _tuple(self.related_candidate_ids))

    @property
    def is_proposal(self) -> bool:
        return True


@dataclass(frozen=True)
class CandidateDraft:
    draft_id: str
    run_id: str
    candidate_ids: tuple[str, ...]
    title: str
    markdown: str
    publishable: bool = False

    def __post_init__(self) -> None:
        for field_name in ("draft_id", "run_id"):
            _validate_identifier(getattr(self, field_name), field_name)
        object.__setattr__(self, "candidate_ids", _tuple(self.candidate_ids))
        if not self.candidate_ids:
            raise ValidationError("candidate_ids must contain at least one candidate")
        for candidate_id in self.candidate_ids:
            _validate_identifier(candidate_id, "candidate_id")
        _validate_non_empty(self.title, "title")
        _validate_non_empty(self.markdown, "markdown")

    @property
    def is_intermediate_artifact(self) -> bool:
        return True


__all__ = [
    "ApprovalDecision",
    "ApprovalRecord",
    "ChangeType",
    "ConfidenceStatus",
    "ContradictionRecord",
    "ContradictionSeverity",
    "ContradictionStatus",
    "FreshnessStatus",
    "GateResult",
    "ImpactRecord",
    "InfopediaNode",
    "KnowledgePage",
    "CandidateDraft",
    "LintFinding",
    "LintSeverity",
    "LintStatus",
    "MaintenanceRun",
    "PageStatus",
    "ParseStatus",
    "PolicyFinding",
    "KnowledgeCandidate",
    "KnowledgeCandidateType",
    "QAReport",
    "QAResult",
    "RevisionState",
    "Run",
    "RunState",
    "SearchDocument",
    "SourceBundle",
    "SourceDocument",
    "SourceFile",
    "ValidationError",
    "WikiPage",
    "WikiPageRevision",
]
