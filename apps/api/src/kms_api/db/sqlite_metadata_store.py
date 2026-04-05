from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from threading import RLock
from typing import Any, Callable, TypeVar

from kms_domain import (
    AgentExecutionRecord,
    ApprovalRecord,
    ContradictionRecord,
    InfopediaNode,
    IntakeArtifact,
    ImpactRecord,
    LintFinding,
    MetadataStore,
    QAReport,
    Run,
    RunEvent,
    SearchDocument,
    SourceDocument,
    SourceFile,
    SourceNote,
    WikiPage,
    WikiPageRevision,
)

T = TypeVar("T")


class SQLiteMetadataStore(MetadataStore):
    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        if self._db_path != Path(":memory:"):
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def create_run(self, run: Run) -> Run:
        return self._upsert("run", run.run_id, run)

    def get_run(self, run_id: str) -> Run | None:
        return self._get("run", run_id, Run)

    def list_runs(self) -> list[Run]:
        return self._list("run", Run)

    def upsert_source_file(self, source_file: SourceFile) -> SourceFile:
        return self._upsert("source_file", source_file.source_file_id, source_file)

    def list_source_files(self, run_id: str) -> list[SourceFile]:
        return self._filter(self._list("source_file", SourceFile), run_id=run_id)

    def upsert_source_document(self, source_document: SourceDocument) -> SourceDocument:
        return self._upsert("source_document", source_document.source_document_id, source_document)

    def list_source_documents(self, run_id: str) -> list[SourceDocument]:
        return self._filter(self._list("source_document", SourceDocument), run_id=run_id)

    def upsert_source_note(self, source_note: SourceNote) -> SourceNote:
        return self._upsert("source_note", source_note.source_note_id, source_note)

    def list_source_notes(self, run_id: str) -> list[SourceNote]:
        return self._filter(self._list("source_note", SourceNote), run_id=run_id)

    def record_intake_artifact(self, artifact: IntakeArtifact) -> IntakeArtifact:
        return self._upsert("intake_artifact", artifact.artifact_id, artifact)

    def list_intake_artifacts(self, run_id: str) -> list[IntakeArtifact]:
        return self._filter(self._list("intake_artifact", IntakeArtifact), run_id=run_id)

    def record_impact(self, impact: ImpactRecord) -> ImpactRecord:
        return self._upsert("impact_record", impact.impact_id, impact)

    def list_impact_records(self, run_id: str | None = None) -> list[ImpactRecord]:
        return self._filter(self._list("impact_record", ImpactRecord), run_id=run_id)

    def upsert_wiki_page(self, page: WikiPage) -> WikiPage:
        return self._upsert("wiki_page", page.page_id, page)

    def get_wiki_page_by_slug(self, slug: str) -> WikiPage | None:
        for page in self._list("wiki_page", WikiPage):
            if page.slug == slug:
                return page
        return None

    def list_wiki_pages(self) -> list[WikiPage]:
        return self._list("wiki_page", WikiPage)

    def upsert_wiki_page_revision(self, revision: WikiPageRevision) -> WikiPageRevision:
        return self._upsert("wiki_page_revision", revision.revision_id, revision)

    def list_wiki_page_revisions(self, page_id: str | None = None) -> list[WikiPageRevision]:
        return self._filter(self._list("wiki_page_revision", WikiPageRevision), page_id=page_id)

    def record_approval(self, approval: ApprovalRecord) -> ApprovalRecord:
        return self._upsert("approval", approval.approval_id, approval)

    def list_approvals(self, revision_id: str | None = None) -> list[ApprovalRecord]:
        return self._filter(self._list("approval", ApprovalRecord), revision_id=revision_id)

    def record_contradiction(self, record: ContradictionRecord) -> ContradictionRecord:
        return self._upsert("contradiction", record.contradiction_id, record)

    def list_contradictions(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[ContradictionRecord]:
        return self._filter(
            self._list("contradiction", ContradictionRecord),
            run_id=run_id,
            page_id=page_id,
            revision_id=revision_id,
        )

    def record_qa_report(self, report: QAReport) -> QAReport:
        return self._upsert("qa_report", report.qa_report_id, report)

    def list_qa_reports(
        self,
        run_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[QAReport]:
        return self._filter(self._list("qa_report", QAReport), run_id=run_id, revision_id=revision_id)

    def record_lint_finding(self, finding: LintFinding) -> LintFinding:
        return self._upsert("lint_finding", finding.lint_finding_id, finding)

    def list_lint_findings(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        revision_id: str | None = None,
    ) -> list[LintFinding]:
        return self._filter(
            self._list("lint_finding", LintFinding),
            run_id=run_id,
            page_id=page_id,
            revision_id=revision_id,
        )

    def record_run_event(self, event: RunEvent) -> RunEvent:
        return self._upsert("run_event", event.event_id, event)

    def list_run_events(self, run_id: str | None = None) -> list[RunEvent]:
        return self._filter(self._list("run_event", RunEvent), run_id=run_id)

    def record_agent_execution(self, execution: AgentExecutionRecord) -> AgentExecutionRecord:
        return self._upsert("agent_execution", execution.execution_id, execution)

    def list_agent_executions(
        self,
        run_id: str | None = None,
        stage: str | None = None,
    ) -> list[AgentExecutionRecord]:
        return self._filter(self._list("agent_execution", AgentExecutionRecord), run_id=run_id, stage=stage)

    def record_search_document(self, document: SearchDocument) -> SearchDocument:
        return self._upsert("search_document", document.search_doc_id, document)

    def list_search_documents(
        self,
        run_id: str | None = None,
        page_id: str | None = None,
        scope: str | None = None,
    ) -> list[SearchDocument]:
        return self._filter(
            self._list("search_document", SearchDocument),
            run_id=run_id,
            page_id=page_id,
            scope=scope,
        )

    def replace_search_documents(self, documents: list[SearchDocument]) -> None:
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM records WHERE kind = ?", ("search_document",))
            for document in documents:
                self._write("search_document", document.search_doc_id, document)

    def record_infopedia_node(self, node: InfopediaNode) -> InfopediaNode:
        return self._upsert("infopedia_node", node.node_id, node)

    def list_infopedia_nodes(self, page_id: str | None = None, status: str | None = None) -> list[InfopediaNode]:
        return self._filter(self._list("infopedia_node", InfopediaNode), page_id=page_id, status=status)

    def replace_infopedia_nodes(self, nodes: list[InfopediaNode]) -> None:
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM records WHERE kind = ?", ("infopedia_node",))
            for node in nodes:
                self._write("infopedia_node", node.node_id, node)

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def _ensure_schema(self) -> None:
        with self._lock, self._conn:
            for table_name in _TABLE_NAMES.values():
                self._conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        entity_id TEXT PRIMARY KEY,
                        payload TEXT NOT NULL
                    )
                    """
                )

    def _upsert(self, kind: str, entity_id: str, obj: T) -> T:
        with self._lock, self._conn:
            self._write(kind, entity_id, obj)
        return obj

    def _write(self, kind: str, entity_id: str, obj: Any) -> None:
        table_name = _table_name(kind)
        self._conn.execute(
            f"INSERT OR REPLACE INTO {table_name}(entity_id, payload) VALUES (?, ?)",
            (entity_id, json.dumps(asdict(obj))),
        )

    def _get(self, kind: str, entity_id: str, cls: type[T]) -> T | None:
        table_name = _table_name(kind)
        with self._lock:
            row = self._conn.execute(
                f"SELECT payload FROM {table_name} WHERE entity_id = ?",
                (entity_id,),
            ).fetchone()
        if row is None:
            return None
        return cls(**json.loads(row["payload"]))

    def _list(self, kind: str, cls: type[T]) -> list[T]:
        table_name = _table_name(kind)
        with self._lock:
            rows = self._conn.execute(
                f"SELECT payload FROM {table_name} ORDER BY rowid",
            ).fetchall()
        return [cls(**json.loads(row["payload"])) for row in rows]

    def _filter(self, items: list[T], **criteria: Any) -> list[T]:
        filtered = items
        for field_name, expected in criteria.items():
            if expected is None:
                continue
            filtered = [item for item in filtered if getattr(item, field_name) == expected]
        return filtered


_TABLE_NAMES = {
    "run": "runs",
    "source_file": "source_files",
    "source_document": "source_documents",
    "source_note": "source_notes",
    "intake_artifact": "intake_artifacts",
    "impact_record": "impact_records",
    "wiki_page": "wiki_pages",
    "wiki_page_revision": "wiki_page_revisions",
    "approval": "approvals",
    "contradiction": "contradictions",
    "qa_report": "qa_reports",
    "lint_finding": "lint_findings",
    "run_event": "run_events",
    "agent_execution": "agent_executions",
    "search_document": "search_documents",
    "infopedia_node": "infopedia_nodes",
}


def _table_name(kind: str) -> str:
    try:
        return _TABLE_NAMES[kind]
    except KeyError as exc:
        raise KeyError(f"Unknown metadata kind: {kind}") from exc
