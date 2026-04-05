from __future__ import annotations

from kms_domain import (
    AgentExecutionRecord,
    ApprovalRecord,
    ContradictionRecord,
    IntakeArtifact,
    ImpactRecord,
    InfopediaNode,
    LintFinding,
    MetadataStore,
    QAReport,
    Run,
    RunEvent,
    SourceDocument,
    SourceFile,
    SourceNote,
    SearchDocument,
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

    def upsert_source_document(self, source_document: SourceDocument) -> SourceDocument:
        return self._store.upsert_source_document(source_document)

    def list_source_documents(self, run_id: str) -> list[SourceDocument]:
        return self._store.list_source_documents(run_id)

    def upsert_source_note(self, source_note: SourceNote) -> SourceNote:
        return self._store.upsert_source_note(source_note)

    def list_source_notes(self, run_id: str) -> list[SourceNote]:
        return self._store.list_source_notes(run_id)

    def record_intake_artifact(self, artifact: IntakeArtifact) -> IntakeArtifact:
        return self._store.record_intake_artifact(artifact)

    def list_intake_artifacts(self, run_id: str) -> list[IntakeArtifact]:
        return self._store.list_intake_artifacts(run_id)

    def record_impact(self, impact: ImpactRecord) -> ImpactRecord:
        return self._store.record_impact(impact)

    def list_impact_records(self, run_id: str | None = None) -> list[ImpactRecord]:
        return self._store.list_impact_records(run_id)

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage:
        return self._store.upsert_wiki_page(page)

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None:
        return self._store.get_wiki_page_by_slug(slug)

    def list_wiki_pages(self) -> list[WikiPage]:
        return self._store.list_wiki_pages()

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        return self._store.upsert_wiki_page_revision(revision)

    def list_wiki_page_revisions(self, page_id: str | None = None) -> list[WikiPageRevision]:
        return self._store.list_wiki_page_revisions(page_id)

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        return self._store.record_approval(approval)

    def list_approvals(self, revision_id: str | None = None) -> list[ApprovalRecord]:
        return self._store.list_approvals(revision_id)

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        return self._store.record_contradiction(record)

    def list_contradictions(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[ContradictionRecord]:
        return self._store.list_contradictions(run_id, page_id, revision_id)

    def record_qa_report(self, report: QAReport) -> QAReport:
        return self._store.record_qa_report(report)

    def list_qa_reports(
        self,
        run_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[QAReport]:
        return self._store.list_qa_reports(run_id, revision_id)

    def record_lint_finding(self, finding: LintFinding) -> LintFinding:
        return self._store.record_lint_finding(finding)

    def list_lint_findings(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[LintFinding]:
        return self._store.list_lint_findings(run_id, page_id, revision_id)

    def record_run_event(self, event: RunEvent) -> RunEvent:
        return self._store.record_run_event(event)

    def list_run_events(self, run_id: str | None = None) -> list[RunEvent]:
        return self._store.list_run_events(run_id)

    def record_agent_execution(self, execution: AgentExecutionRecord) -> AgentExecutionRecord:
        return self._store.record_agent_execution(execution)

    def list_agent_executions(
        self,
        run_id: str | None = None,
        stage: str | None = None,
    ) -> list[AgentExecutionRecord]:
        return self._store.list_agent_executions(run_id, stage)

    def record_search_document(self, document: SearchDocument) -> SearchDocument:
        return self._store.record_search_document(document)

    def list_search_documents(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        scope: str | None = None,
    ) -> list[SearchDocument]:
        return self._store.list_search_documents(run_id, page_id, scope)

    def replace_search_documents(self, documents: list[SearchDocument]) -> None:
        self._store.replace_search_documents(documents)

    def record_infopedia_node(self, node: InfopediaNode) -> InfopediaNode:
        return self._store.record_infopedia_node(node)

    def list_infopedia_nodes(
        self,
        page_id: str | None = None,
        status: str | None = None,
    ) -> list[InfopediaNode]:
        return self._store.list_infopedia_nodes(page_id, status)

    def replace_infopedia_nodes(self, nodes: list[InfopediaNode]) -> None:
        self._store.replace_infopedia_nodes(nodes)
