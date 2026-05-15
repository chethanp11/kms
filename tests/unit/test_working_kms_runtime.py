"""Runtime coverage for DEV-020 working KMS application slice."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.api.dependencies import set_runtime
from src.api.routes.candidates import approve_candidates, create_candidates, list_candidates, publish_approved_candidates
from src.api.routes.infopedia import search, tree
from src.api.routes.runs import create_run, get_run, list_artifacts
from src.config.settings import KMSSettings
from src.contracts import GateResult, KnowledgePage, ValidationError
from src.services.policy_validation import validate_page
from src.services.publisher import publish_page
from src.services.run_orchestration import KMSRuntime


class WorkingKMSRuntimeTests(unittest.TestCase):
    def runtime(self, root: Path) -> KMSRuntime:
        return KMSRuntime.create(KMSSettings(raw_root=root / "raw", wiki_root=root / "wiki", artifact_root=root / "artifacts"))

    def test_source_to_approved_publish_search_and_infopedia_projection(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            (source / "revenue.md").write_text("Revenue is governed knowledge.", encoding="utf-8")
            runtime = self.runtime(root)

            result = runtime.start_run(source, run_id="run-020", auto_approve=True)

            self.assertEqual(result.run.state.value, "completed")
            self.assertEqual(result.source_count, 1)
            self.assertEqual(len(result.published), 1)
            self.assertIn("# Revenue", runtime.wiki.read_page("sources/revenue"))
            self.assertEqual([doc.title for doc in runtime.search.search("revenue")], ["Revenue"])
            self.assertEqual([node.slug for node in tree_for(runtime)], ["sources/revenue"])

    def test_api_routes_use_runtime_without_storage_bypass(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            (source / "ops.md").write_text("Operations knowledge.", encoding="utf-8")
            runtime = self.runtime(root)
            set_runtime(runtime)

            response = create_run({"source_path": str(source), "run_id": "run-api", "auto_approve": True})

            self.assertEqual(response["state"], "completed")
            self.assertEqual(get_run("run-api")["summary_counts"]["published_pages"], 1)
            self.assertIn("source-note.md", list_artifacts("run-api"))
            self.assertIn("knowledge-candidates.json", list_artifacts("run-api"))
            self.assertEqual(search("operations")[0]["title"], "Ops")
            self.assertEqual(tree()[0]["slug"], "sources/ops")

    def test_publish_fails_closed_without_qa_or_approval(self) -> None:
        with TemporaryDirectory() as temp_dir:
            runtime = self.runtime(Path(temp_dir))
            page = KnowledgePage(page_id="page-1", page_type="source-note", path="sources/x.md", title="X", body="## Summary\nNo trace.")
            qa = validate_page(page, revision_id="revision-1")
            self.assertEqual(qa.result, GateResult.BLOCK)
            with self.assertRaises(ValidationError):
                publish_page(page, qa, None, runtime.wiki)

    def test_candidate_approval_workflow_publishes_to_infopedia(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            (source / "revenue.md").write_text(
                "Metric: Revenue is recognized after approved invoice.\n"
                "Decision: Finance approved revenue as a candidate.",
                encoding="utf-8",
            )
            runtime = self.runtime(root)
            set_runtime(runtime)

            created = create_candidates({"source_path": str(source), "run_id": "candidate-api"})
            self.assertEqual(created["summary_counts"]["published_pages"], 0)
            self.assertGreaterEqual(len(created["candidates"]), 2)
            self.assertEqual(search("revenue"), [])
            self.assertTrue(search("revenue", include_candidates=True))

            first_id = created["candidates"][0]["candidate_id"]
            selected = approve_candidates("candidate-api", {"candidate_ids": [first_id]})
            self.assertEqual(selected["approved_candidate_ids"], [first_id])

            approved = approve_candidates("candidate-api", {"approve_all": True})
            self.assertEqual(len(approved["approved_candidate_ids"]), len(created["candidates"]))

            published = publish_approved_candidates("candidate-api", {})

            self.assertEqual(published["summary_counts"]["published_pages"], len(created["candidates"]))
            self.assertTrue(all(path.startswith("sources/") for path in published["published"]))
            self.assertFalse((root / "wiki" / "candidates").exists())
            self.assertGreaterEqual(len(tree()), len(created["candidates"]))
            self.assertTrue(search("revenue"))
            self.assertIn("confidence_score", search("trusted")[0])
            archived = list_candidates("candidate-api")
            self.assertTrue(all(candidate["archived"] for candidate in archived))
            with self.assertRaises(ValidationError):
                publish_approved_candidates("candidate-api", {})

    def test_candidate_review_supports_reject_mods_and_duplicate_awareness(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source"
            source.mkdir()
            (source / "revenue.md").write_text(
                "Metric: Revenue rate is measured as approved invoice value.\n"
                "Process: Revenue review workflow has approval steps.\n"
                "Concept: Revenue review notes remain searchable for audit.",
                encoding="utf-8",
            )
            runtime = self.runtime(root)
            set_runtime(runtime)

            existing_page = KnowledgePage(
                page_id="page-existing",
                page_type="metric",
                path="sources/revenue-rate.md",
                title="Revenue Rate",
                body="## Summary\nRevenue rate is measured as approved invoice value.\n\n## Source Trace\n- prior.md",
                source_refs=("prior.md",),
            )
            (root / "wiki" / "sources").mkdir(parents=True)
            runtime.wiki.write_page(existing_page)

            created = create_candidates({"source_path": str(source), "run_id": "candidate-024"})
            rejected = [candidate for candidate in created["candidates"] if candidate["rejected"]]
            pending = [candidate for candidate in created["candidates"] if not candidate["rejected"]]

            self.assertTrue(rejected)
            self.assertIn("duplicate", rejected[0]["duplicate_rationale"].casefold())

            reject_response = approve_candidates("candidate-024", {"decision": "reject", "candidate_ids": [pending[0]["candidate_id"]]})
            self.assertIn(pending[0]["candidate_id"], reject_response["rejected_candidate_ids"])

            # Recreate a fresh run to prove Approve with Mods publishes modified text under sources/.
            created = create_candidates({"source_path": str(source), "run_id": "candidate-024b"})
            mod_candidate = next(candidate for candidate in created["candidates"] if not candidate["rejected"])
            approve_candidates(
                "candidate-024b",
                {
                    "candidate_ids": [mod_candidate["candidate_id"]],
                    "modifications": {mod_candidate["candidate_id"]: "Modified approved summary."},
                },
            )
            published = publish_approved_candidates("candidate-024b", {})

            self.assertTrue(all(path.startswith("sources/") for path in published["published"]))
            self.assertIn("Modified approved summary.", (root / "wiki" / published["published"][0]).read_text(encoding="utf-8"))

    def test_create_candidates_can_materialize_browser_uploaded_sources(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            runtime = self.runtime(root)
            set_runtime(runtime)

            created = create_candidates(
                {
                    "source_path": "desktop/source-selection",
                    "run_id": "upload-run",
                    "source_files": [
                        {
                            "relative_path": "folder/code/order_service.py",
                            "content": "Entity: Order service owns checkout.\nProcess: Intake validates requests.\nMetric: Success rate is measured.",
                            "media_type": "text/plain",
                        },
                        {
                            "relative_path": "folder/docs/takeaways.md",
                            "content": "Decision: Finance approved the release.\nConcept: The takeaways stay visible for review.",
                            "media_type": "text/markdown",
                        },
                    ],
                }
            )

            self.assertEqual(created["run_id"], "upload-run")
            self.assertEqual(created["summary_counts"]["source_files"], 2)
            self.assertLessEqual(len(created["candidates"]), 5)
            self.assertTrue(all(candidate["source_ref"].startswith("folder/") for candidate in created["candidates"]))


def tree_for(runtime: KMSRuntime) -> list[object]:
    from src.services.infopedia_projection import build_tree

    return build_tree(runtime.wiki)


if __name__ == "__main__":
    unittest.main()
