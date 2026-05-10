"""Unit coverage for the initial KMS src scaffold."""

from __future__ import annotations

import unittest

from src.app import REPRESENTATIVE_ENDPOINTS
from src.context import CANONICAL_WIKI_ROOT, INFOPEDIA_ACCESS, RAW_SOURCE_ROLE
from src.contracts import ApprovalDecision, ApprovalRecord, KnowledgePage, MaintenanceRun, RunState, SourceBundle
from src.governance import GateResult, approval_allows_publication, validate_page_candidate
from src.orchestrator import summarize_intake


class ScaffoldBoundaryTests(unittest.TestCase):
    def test_context_preserves_authority_boundaries(self) -> None:
        self.assertEqual(CANONICAL_WIKI_ROOT, "/wiki")
        self.assertIn("immutable", RAW_SOURCE_ROLE)
        self.assertEqual(INFOPEDIA_ACCESS, "read-only")

    def test_representative_api_surface_matches_design_categories(self) -> None:
        self.assertIn(("POST", "/api/runs"), REPRESENTATIVE_ENDPOINTS)
        self.assertIn(("GET", "/api/wiki/pages/{slug}"), REPRESENTATIVE_ENDPOINTS)
        self.assertIn(("GET", "/api/infopedia/search"), REPRESENTATIVE_ENDPOINTS)

    def test_policy_blocks_page_without_source_trace(self) -> None:
        page = KnowledgePage(page_type="metric", path="metrics/revenue.md", title="Revenue", body="## Summary\nRevenue.")

        report = validate_page_candidate(page)

        self.assertEqual(report.result, GateResult.BLOCK)
        self.assertFalse(report.can_publish)

    def test_policy_passes_page_with_source_trace(self) -> None:
        page = KnowledgePage(
            page_type="metric",
            path="metrics/revenue.md",
            title="Revenue",
            body="## Summary\nRevenue.\n\n## Source Trace\n- source.md",
        )

        self.assertTrue(validate_page_candidate(page).can_publish)

    def test_approval_decision_gates_publication(self) -> None:
        approved = ApprovalRecord("approval-1", "revision-1", ApprovalDecision.APPROVED, "manager")
        rejected = ApprovalRecord("approval-2", "revision-1", ApprovalDecision.REJECTED, "manager")

        self.assertTrue(approval_allows_publication(approved))
        self.assertFalse(approval_allows_publication(rejected))

    def test_orchestrator_summarizes_empty_bundle_as_blocked(self) -> None:
        run = MaintenanceRun(run_id="run-1", source_path="/tmp/source")
        bundle = SourceBundle(root_path="/tmp/source", files=(), warnings=("source bundle is empty",))

        summary = summarize_intake(run, bundle)

        self.assertEqual(summary.run.state, RunState.BLOCKED)
        self.assertEqual(summary.run.summary_counts["warnings"], 1)


if __name__ == "__main__":
    unittest.main()
