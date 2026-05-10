"""Core KMS data contracts.

These contracts intentionally use only the Python standard library so the
scaffold can be validated before runtime dependencies are selected.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import PurePosixPath
import re
from typing import Mapping

_SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")
_SAFE_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class ValidationError(ValueError):
    """Raised when a KMS contract would violate a design boundary."""


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


class ApprovalDecision(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


def _validate_relative_posix_path(path: str, *, field_name: str = "path") -> str:
    if not path or path.startswith("/") or "\\" in path:
        raise ValidationError(f"{field_name} must be a non-empty relative POSIX path")
    pure = PurePosixPath(path)
    if any(part in {"", ".", ".."} for part in pure.parts):
        raise ValidationError(f"{field_name} must not contain empty, current, or parent segments")
    if any(not _SAFE_SEGMENT_RE.match(part) for part in pure.parts):
        raise ValidationError(f"{field_name} contains an unsafe segment")
    return pure.as_posix()


@dataclass(frozen=True)
class SourceFile:
    """Immutable upstream source file discovered during intake."""

    relative_path: str
    sha256: str
    size_bytes: int
    media_type: str = "application/octet-stream"

    def __post_init__(self) -> None:
        object.__setattr__(self, "relative_path", _validate_relative_posix_path(self.relative_path, field_name="relative_path"))
        if not _SHA256_RE.match(self.sha256):
            raise ValidationError("sha256 must be a 64-character hexadecimal digest")
        if self.size_bytes < 0:
            raise ValidationError("size_bytes must be non-negative")


@dataclass(frozen=True)
class SourceBundle:
    """Deterministic inventory of raw source files for a maintenance run."""

    root_path: str
    files: tuple[SourceFile, ...]
    warnings: tuple[str, ...] = ()

    @property
    def is_empty(self) -> bool:
        return not self.files


@dataclass(frozen=True)
class KnowledgePage:
    """Canonical finalized wiki page candidate.

    This object can render markdown, but it does not publish it. Publication
    remains a governed service concern.
    """

    page_type: str
    path: str
    title: str
    body: str
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _validate_relative_posix_path(self.path))
        if not self.path.endswith(".md"):
            raise ValidationError("knowledge page path must end with .md")
        if not self.page_type.strip():
            raise ValidationError("page_type is required")
        if not self.title.strip():
            raise ValidationError("title is required")
        if not self.body.strip():
            raise ValidationError("body is required")

    def to_markdown(self) -> str:
        frontmatter = {
            "title": self.title,
            "type": self.page_type,
            "path": self.path,
            **dict(self.metadata),
        }
        lines = ["---"]
        for key in sorted(frontmatter):
            lines.append(f"{key}: {frontmatter[key]}")
        lines.extend(["---", "", f"# {self.title}", "", self.body.rstrip(), ""])
        return "\n".join(lines)


@dataclass(frozen=True)
class MaintenanceRun:
    """Run-level status exposed to KMI."""

    run_id: str
    source_path: str
    state: RunState = RunState.CREATED
    summary_counts: Mapping[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovalRecord:
    """Human approval decision that can gate publication."""

    approval_id: str
    revision_id: str
    decision: ApprovalDecision
    reviewer_id: str
    reason: str = ""


__all__ = [
    "ApprovalDecision",
    "ApprovalRecord",
    "KnowledgePage",
    "MaintenanceRun",
    "RevisionState",
    "RunState",
    "SourceBundle",
    "SourceFile",
    "ValidationError",
]
