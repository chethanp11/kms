from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from kms_config import RuntimeConfig, load_runtime_config
from kms_domain import (
    IntakeArtifact,
    MetadataStore,
    Run,
    SourceDocument,
    SourceFile,
    SourceNote,
)

from .discovery import discover_source_files
from .models import IntakeRunResult
from .parsers import parse_source_file

TimestampProvider = Callable[[], str]


def default_timestamp_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_stable_id(prefix: str, *parts: str) -> str:
    import hashlib

    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


@dataclass
class IntakeRequest:
    source_root_path: str
    initiated_by: str
    domain_hint: str | None = None
    run_notes: str | None = None
    strictness: str = "standard"


class SourceIntakeService:
    def __init__(
        self,
        store: MetadataStore,
        config: RuntimeConfig | None = None,
        timestamp_provider: TimestampProvider | None = None,
    ) -> None:
        self._store = store
        self._config = config or load_runtime_config()
        self._timestamp_provider = timestamp_provider or default_timestamp_provider

    def start_intake(self, request: IntakeRequest) -> IntakeRunResult:
        source_root = Path(request.source_root_path).expanduser().resolve()
        if not source_root.exists() or not source_root.is_dir():
            raise FileNotFoundError(f"Invalid source root: {request.source_root_path}")

        run_id = make_stable_id("run", str(source_root), request.initiated_by, request.domain_hint or "")
        run = Run(
            run_id=run_id,
            status="in_progress",
            source_path=str(source_root),
            domain_hint=request.domain_hint,
            run_notes=request.run_notes,
            created_at=self._timestamp_provider(),
            started_at=self._timestamp_provider(),
            created_by=request.initiated_by,
            current_stage="discovering_sources",
        )
        self._store.create_run(run)

        discovery = discover_source_files(source_root)
        source_documents = 0
        source_notes = 0
        intake_artifacts = 0
        supported_files = 0
        unsupported_files = 0

        for discovered in discovery.sources:
            source_file_id = make_stable_id("src", run_id, discovered.relative_path, discovered.checksum_sha256)
            source_file = SourceFile(
                source_file_id=source_file_id,
                run_id=run_id,
                path=discovered.relative_path,
                file_type=discovered.classification,
                hash=discovered.checksum_sha256,
                parse_status="discovered" if discovered.support_status == "supported" else "unsupported",
                discovered_at=self._timestamp_provider(),
            )
            self._store.upsert_source_file(source_file)
            intake_artifacts += 1
            self._store.record_intake_artifact(
                IntakeArtifact(
                    artifact_id=make_stable_id("artifact", run_id, source_file_id, "registry"),
                    run_id=run_id,
                    artifact_type="source_registry",
                    status="created",
                    path=discovered.relative_path,
                    summary=f"Registered {discovered.file_name}",
                    created_at=self._timestamp_provider(),
                )
            )

            if discovered.support_status != "supported":
                unsupported_files += 1
                continue

            supported_files += 1
            parsed = parse_source_file(source_root / discovered.relative_path)
            source_file.parse_status = "parsed"
            self._store.upsert_source_file(source_file)
            source_document_id = make_stable_id("doc", run_id, source_file_id)
            source_document = SourceDocument(
                source_document_id=source_document_id,
                source_file_id=source_file_id,
                run_id=run_id,
                content_type=parsed.content_type,
                normalized_text=parsed.normalized_text,
                summary=parsed.summary,
                created_at=self._timestamp_provider(),
                title=Path(discovered.relative_path).stem,
                status="normalized",
                parse_metadata={k: str(v) for k, v in parsed.parse_metadata.items()},
            )
            self._store.upsert_source_document(source_document)
            source_documents += 1
            intake_artifacts += 1
            self._store.record_intake_artifact(
                IntakeArtifact(
                    artifact_id=make_stable_id("artifact", run_id, source_document_id, "parse"),
                    run_id=run_id,
                    artifact_type="parse_output",
                    status="created",
                    path=discovered.relative_path,
                    summary=parsed.summary,
                    created_at=self._timestamp_provider(),
                )
            )

            source_note_id = make_stable_id("note", run_id, source_document_id)
            source_note = SourceNote(
                source_note_id=source_note_id,
                run_id=run_id,
                source_document_id=source_document_id,
                title=f"{Path(discovered.relative_path).stem} Source Note",
                slug=f"source-notes/{Path(discovered.relative_path).stem}",
                summary=parsed.summary,
                source_refs=[discovered.relative_path],
                extracted_signals=parsed.extracted_signals,
                review_required=True,
                created_at=self._timestamp_provider(),
            )
            self._store.upsert_source_note(source_note)
            source_notes += 1
            intake_artifacts += 1
            self._store.record_intake_artifact(
                IntakeArtifact(
                    artifact_id=make_stable_id("artifact", run_id, source_note_id, "note"),
                    run_id=run_id,
                    artifact_type="source_note",
                    status="created",
                    path=None,
                    summary=source_note.summary,
                    created_at=self._timestamp_provider(),
                )
            )

        completed_status = "completed_with_warnings" if unsupported_files else "completed"
        run.status = completed_status
        run.completed_at = self._timestamp_provider()
        run.current_stage = "handoff"
        self._store.create_run(run)
        self._store.record_intake_artifact(
            IntakeArtifact(
                artifact_id=make_stable_id("artifact", run_id, "summary"),
                run_id=run_id,
                artifact_type="intake_summary",
                status="created",
                path=None,
                summary=f"{supported_files} supported, {unsupported_files} unsupported",
                created_at=self._timestamp_provider(),
            )
        )
        intake_artifacts += 1
        return IntakeRunResult(
            run_id=run_id,
            total_files=len(discovery.sources),
            supported_files=supported_files,
            unsupported_files=unsupported_files,
            parsed_documents=source_documents,
            source_notes=source_notes,
            intake_artifacts=intake_artifacts,
            status=completed_status,
        )
