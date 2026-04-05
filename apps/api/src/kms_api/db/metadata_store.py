from __future__ import annotations

from typing import Dict

from kms_domain import (
    AgentExecutionRecord,
    ApprovalRecord,
    ContradictionRecord,
    IntakeArtifact,
    ImpactRecord,
    InfopediaNode,
    MetadataStore,
    LintFinding,
    QAReport,
    RunEvent,
    Run,
    SourceDocument,
    SourceFile,
    SourceNote,
    SearchDocument,
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
        self._impact_records: Dict[str, ImpactRecord] = {}
        self._wiki_pages: Dict[str, WikiPage] = {}
        self._pages_by_slug: Dict[str, WikiPage] = {}
        self._revisions: Dict[str, WikiPageRevision] = {}
        self._approvals: Dict[str, ApprovalRecord] = {}
        self._contradictions: Dict[str, ContradictionRecord] = {}
        self._qa_reports: Dict[str, QAReport] = {}
        self._lint_findings: Dict[str, LintFinding] = {}
        self._run_events: Dict[str, RunEvent] = {}
        self._agent_executions: Dict[str, AgentExecutionRecord] = {}
        self._search_documents: Dict[str, SearchDocument] = {}
        self._infopedia_nodes: Dict[str, InfopediaNode] = {}

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

    def record_impact(self, impact: ImpactRecord) -> ImpactRecord:
        self._impact_records[impact.impact_id] = impact
        return impact

    def list_impact_records(self, run_id: str | None = None) -> list[ImpactRecord]:
        impacts = list(self._impact_records.values())
        if run_id is None:
            return impacts
        return [impact for impact in impacts if impact.run_id == run_id]

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage:
        self._wiki_pages[page.page_id] = page
        self._pages_by_slug[page.slug] = page
        return page

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None:
        return self._pages_by_slug.get(slug)

    def list_wiki_pages(self) -> list[WikiPage]:
        return list(self._wiki_pages.values())

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        self._revisions[revision.revision_id] = revision
        return revision

    def list_wiki_page_revisions(self, page_id: str | None = None) -> list[WikiPageRevision]:
        revisions = list(self._revisions.values())
        if page_id is None:
            return revisions
        return [revision for revision in revisions if revision.page_id == page_id]

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        self._approvals[approval.approval_id] = approval
        return approval

    def list_approvals(self, revision_id: str | None = None) -> list[ApprovalRecord]:
        approvals = list(self._approvals.values())
        if revision_id is None:
            return approvals
        return [approval for approval in approvals if approval.revision_id == revision_id]

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        self._contradictions[record.contradiction_id] = record
        return record

    def list_contradictions(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[ContradictionRecord]:
        contradictions = list(self._contradictions.values())
        if run_id is not None:
            contradictions = [record for record in contradictions if record.run_id == run_id]
        if page_id is not None:
            contradictions = [record for record in contradictions if record.page_id == page_id]
        if revision_id is not None:
            contradictions = [record for record in contradictions if record.revision_id == revision_id]
        return contradictions

    def record_qa_report(self, report: QAReport) -> QAReport:
        self._qa_reports[report.qa_report_id] = report
        return report

    def list_qa_reports(
        self,
        run_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[QAReport]:
        reports = list(self._qa_reports.values())
        if run_id is not None:
            reports = [report for report in reports if report.run_id == run_id]
        if revision_id is not None:
            reports = [report for report in reports if report.revision_id == revision_id]
        return reports

    def record_lint_finding(self, finding: LintFinding) -> LintFinding:
        self._lint_findings[finding.lint_finding_id] = finding
        return finding

    def list_lint_findings(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[LintFinding]:
        findings = list(self._lint_findings.values())
        if run_id is not None:
            findings = [finding for finding in findings if finding.run_id == run_id]
        if page_id is not None:
            findings = [finding for finding in findings if finding.page_id == page_id]
        if revision_id is not None:
            findings = [finding for finding in findings if finding.revision_id == revision_id]
        return findings

    def record_run_event(self, event: RunEvent) -> RunEvent:
        self._run_events[event.event_id] = event
        return event

    def list_run_events(self, run_id: str | None = None) -> list[RunEvent]:
        events = list(self._run_events.values())
        if run_id is None:
            return events
        return [event for event in events if event.run_id == run_id]

    def record_agent_execution(self, execution: AgentExecutionRecord) -> AgentExecutionRecord:
        self._agent_executions[execution.execution_id] = execution
        return execution

    def list_agent_executions(
        self,
        run_id: str | None = None,
        stage: str | None = None,
    ) -> list[AgentExecutionRecord]:
        executions = list(self._agent_executions.values())
        if run_id is not None:
            executions = [execution for execution in executions if execution.run_id == run_id]
        if stage is not None:
            executions = [execution for execution in executions if execution.stage == stage]
        return executions

    def record_search_document(self, document: SearchDocument) -> SearchDocument:
        self._search_documents[document.search_doc_id] = document
        return document

    def list_search_documents(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        scope: str | None = None,
    ) -> list[SearchDocument]:
        documents = list(self._search_documents.values())
        if run_id is not None:
            documents = [document for document in documents if document.run_id == run_id]
        if page_id is not None:
            documents = [document for document in documents if document.page_id == page_id]
        if scope is not None:
            documents = [document for document in documents if document.scope == scope]
        return documents

    def replace_search_documents(self, documents: list[SearchDocument]) -> None:
        self._search_documents = {document.search_doc_id: document for document in documents}

    def record_infopedia_node(self, node: InfopediaNode) -> InfopediaNode:
        self._infopedia_nodes[node.node_id] = node
        return node

    def list_infopedia_nodes(self, page_id: str | None = None, status: str | None = None) -> list[InfopediaNode]:
        nodes = list(self._infopedia_nodes.values())
        if page_id is not None:
            nodes = [node for node in nodes if node.page_id == page_id]
        if status is not None:
            nodes = [node for node in nodes if node.status == status]
        return nodes

    def replace_infopedia_nodes(self, nodes: list[InfopediaNode]) -> None:
        self._infopedia_nodes = {node.node_id: node for node in nodes}
