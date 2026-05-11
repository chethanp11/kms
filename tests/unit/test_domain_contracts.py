"""Unit coverage for TEST-019 core KMS domain contracts."""

from __future__ import annotations

from hashlib import sha256
import unittest

from src.contracts import (
    ApprovalDecision,
    ApprovalRecord,
    ChangeType,
    ConfidenceStatus,
    ContradictionRecord,
    ContradictionSeverity,
    ContradictionStatus,
    FreshnessStatus,
    GateResult,
    InfopediaNode,
    KnowledgePage,
    LintFinding,
    LintSeverity,
    LintStatus,
    MaintenanceRun,
    PageStatus,
    ParseStatus,
    PolicyFinding,
    QAReport,
    RevisionState,
    RunState,
    SearchDocument,
    SourceDocument,
    SourceFile,
    ValidationError,
    WikiPageRevision,
)


DIGEST = "a" * 64


class CoreDomainContractTests(unittest.TestCase):
    def test_run_exposes_design_status_and_summary_counts(self) -> None:
        run = MaintenanceRun(run_id="run-2026", source_path="/tmp/source", state=RunState.IN_PROGRESS, summary_counts={"source_files": 2})

        self.assertEqual(run.status, "in_progress")
        self.assertEqual(run.summary_counts["source_files"], 2)

    def test_source_file_keeps_legacy_and_design_names(self) -> None:
        source_file = SourceFile(relative_path="reports/q1.md", sha256=DIGEST, size_bytes=42, media_type="text/markdown")

        self.assertEqual(source_file.path, "reports/q1.md")
        self.assertEqual(source_file.file_type, "text/markdown")
        self.assertEqual(source_file.hash, DIGEST)
        self.assertEqual(source_file.parse_status, ParseStatus.DISCOVERED)

    def test_source_document_links_file_and_run(self) -> None:
        document = SourceDocument(
            source_document_id="doc-1",
            source_file_id="source-1",
            run_id="run-1",
            title="Quarterly source",
            content_type="text/markdown",
            text="Source body",
        )

        self.assertEqual(document.parse_status, ParseStatus.PARSED)
        self.assertEqual(document.source_file_id, "source-1")

    def test_wiki_page_tracks_status_and_projection_metadata(self) -> None:
        page = KnowledgePage(
            page_id="page-1",
            page_type="metric",
            path="metrics/revenue.md",
            title="Revenue",
            body="## Source Trace\n- source",
            status=PageStatus.FINALIZED,
            freshness_status=FreshnessStatus.CURRENT,
            confidence_status=ConfidenceStatus.HIGH,
            source_refs=("source-1",),
        )

        self.assertEqual(page.slug, "metrics/revenue")
        self.assertEqual(page.status, PageStatus.FINALIZED)
        self.assertEqual(page.source_refs, ("source-1",))

    def test_revision_requires_source_trace(self) -> None:
        revision = WikiPageRevision(
            revision_id="rev-1",
            page_id="page-1",
            run_id="run-1",
            status=RevisionState.REVIEW_REQUIRED,
            change_type=ChangeType.UPDATE,
            section_changes=("definition",),
            source_trace_ids=("trace-1",),
            diff_summary="Updated definition.",
        )

        self.assertEqual(revision.status, RevisionState.REVIEW_REQUIRED)

        with self.assertRaises(ValidationError):
            WikiPageRevision(
                revision_id="rev-2",
                page_id="page-1",
                run_id="run-1",
                status=RevisionState.STAGED,
                change_type=ChangeType.UPDATE,
                section_changes=("definition",),
                source_trace_ids=(),
                diff_summary="Missing trace.",
            )

    def test_approval_contradiction_qa_and_lint_contracts(self) -> None:
        approval = ApprovalRecord("approval-1", "rev-1", ApprovalDecision.APPROVED, "reviewer-1", policy_version="policy-1")
        contradiction = ContradictionRecord(
            contradiction_id="contradiction-1",
            run_id="run-1",
            page_id="page-1",
            revision_id="rev-1",
            severity=ContradictionSeverity.BLOCKING,
            status=ContradictionStatus.OPEN,
            conflicting_claims=("Claim one", "Claim two"),
            source_refs=("source-1",),
        )
        report = QAReport(GateResult.BLOCK, (PolicyFinding("rule-1", "error", "Rule failed"),), qa_report_id="qa-1", revision_id="rev-1")
        lint = LintFinding("lint-1", LintSeverity.ERROR, LintStatus.OPEN, "Broken link", page_id="page-1", path="metrics/revenue.md")

        self.assertEqual(approval.decision, ApprovalDecision.APPROVED)
        self.assertEqual(contradiction.severity, ContradictionSeverity.BLOCKING)
        self.assertFalse(report.can_publish)
        self.assertEqual(lint.status, LintStatus.OPEN)

    def test_projection_contracts_are_derived_and_validated(self) -> None:
        node = InfopediaNode(node_id="node-1", page_id="page-1", slug="metrics/revenue", title="Revenue", page_type="metric")
        search_doc = SearchDocument(
            search_doc_id="search-1",
            source_kind="wiki_page",
            source_id="page-1",
            title="Revenue",
            content="Revenue definition",
            content_hash=sha256(b"Revenue definition").hexdigest(),
            path="metrics/revenue.md",
            tags=("revenue",),
        )

        self.assertTrue(node.is_projection)
        self.assertTrue(search_doc.is_projection)
        self.assertEqual(search_doc.tags, ("revenue",))

    def test_rejects_unsafe_contract_paths_and_hashes(self) -> None:
        with self.assertRaises(ValidationError):
            SourceFile(relative_path="../source.md", sha256=DIGEST, size_bytes=1)
        with self.assertRaises(ValidationError):
            SearchDocument("search-1", "wiki_page", "page-1", "Revenue", "content", "not-a-digest")


if __name__ == "__main__":
    unittest.main()
