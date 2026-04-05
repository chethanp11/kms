from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class DiscoveredSource:
    absolute_path: str
    relative_path: str
    file_name: str
    file_size_bytes: int
    extension: str
    checksum_sha256: str
    support_status: Literal["supported", "unsupported"]
    classification: str
    parser_route: str | None


@dataclass
class ParsedSource:
    content_type: str
    normalized_text: str
    summary: str
    extracted_signals: list[str] = field(default_factory=list)
    parse_metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class IntakeRunResult:
    run_id: str
    total_files: int
    supported_files: int
    unsupported_files: int
    parsed_documents: int
    source_notes: int
    intake_artifacts: int
    status: str
