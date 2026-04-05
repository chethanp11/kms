from __future__ import annotations

from kms_domain import (
    ApprovalRecord,
    ContradictionRecord,
    MetadataStore,
    Run,
    SourceFile,
    WikiPage,
    WikiPageRevision,
)


class MetadataService:
    def __init__(self, store: MetadataStore) -> None:
        self._store = store

    def create_run(self, run: Run) -> Run:
        return self._store.create_run(run)

    def get_run(self, run_id: str) -> Run | None:
        return self._store.get_run(run_id)

    def list_runs(self) -> list[Run]:
        return self._store.list_runs()

    def upsert_source_file(self, source_file: SourceFile) -> SourceFile:
        return self._store.upsert_source_file(source_file)

    def list_source_files(self, run_id: str) -> list[SourceFile]:
        return self._store.list_source_files(run_id)

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage:
        return self._store.upsert_wiki_page(page)

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None:
        return self._store.get_wiki_page_by_slug(slug)

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        return self._store.upsert_wiki_page_revision(revision)

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        return self._store.record_approval(approval)

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        return self._store.record_contradiction(record)
