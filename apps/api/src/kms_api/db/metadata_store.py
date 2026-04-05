from __future__ import annotations

from typing import Dict

from kms_domain import (
    ApprovalRecord,
    ContradictionRecord,
    IntakeArtifact,
    MetadataStore,
    Run,
    SourceDocument,
    SourceFile,
    SourceNote,
    WikiPage,
    WikiPageRevision,
)


class InMemoryMetadataStore(MetadataStore):
    def __init__(self) -> None:
        self._runs: Dict[str, Run] = {}
        self._source_files: Dict[str, SourceFile] = {}
        self._source_documents: Dict[str, SourceDocument] = {}
        self._source_notes: Dict[str, SourceNote] = {}
        self._intake_artifacts: Dict[str, IntakeArtifact] = {}
        self._wiki_pages: Dict[str, WikiPage] = {}
        self._pages_by_slug: Dict[str, WikiPage] = {}
        self._revisions: Dict[str, WikiPageRevision] = {}
        self._approvals: Dict[str, ApprovalRecord] = {}
        self._contradictions: Dict[str, ContradictionRecord] = {}

    def create_run(self, run: Run) -> Run:
        self._runs[run.run_id] = run
        return run

    def get_run(self, run_id: str) -> Run | None:
        return self._runs.get(run_id)

    def list_runs(self) -> list[Run]:
        return list(self._runs.values())

    def upsert_source_file(self, source_file: SourceFile) -> SourceFile:
        self._source_files[source_file.source_file_id] = source_file
        return source_file

    def list_source_files(self, run_id: str) -> list[SourceFile]:
        return [
            source_file
            for source_file in self._source_files.values()
            if source_file.run_id == run_id
        ]

    def upsert_source_document(self, source_document: SourceDocument) -> SourceDocument:
        self._source_documents[source_document.source_document_id] = source_document
        return source_document

    def list_source_documents(self, run_id: str) -> list[SourceDocument]:
        return [
            source_document
            for source_document in self._source_documents.values()
            if source_document.run_id == run_id
        ]

    def upsert_source_note(self, source_note: SourceNote) -> SourceNote:
        self._source_notes[source_note.source_note_id] = source_note
        return source_note

    def list_source_notes(self, run_id: str) -> list[SourceNote]:
        return [source_note for source_note in self._source_notes.values() if source_note.run_id == run_id]

    def record_intake_artifact(self, artifact: IntakeArtifact) -> IntakeArtifact:
        self._intake_artifacts[artifact.artifact_id] = artifact
        return artifact

    def list_intake_artifacts(self, run_id: str) -> list[IntakeArtifact]:
        return [artifact for artifact in self._intake_artifacts.values() if artifact.run_id == run_id]

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage:
        self._wiki_pages[page.page_id] = page
        self._pages_by_slug[page.slug] = page
        return page

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None:
        return self._pages_by_slug.get(slug)

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        self._revisions[revision.revision_id] = revision
        return revision

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        self._approvals[approval.approval_id] = approval
        return approval

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        self._contradictions[record.contradiction_id] = record
        return record
