"""Runtime coverage for DEV-020 working KMS application slice."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.api.dependencies import set_runtime
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


def tree_for(runtime: KMSRuntime) -> list[object]:
    from src.services.infopedia_projection import build_tree

    return build_tree(runtime.wiki)


if __name__ == "__main__":
    unittest.main()
