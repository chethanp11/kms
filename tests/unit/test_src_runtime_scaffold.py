"""Unit coverage for the corrected src-only KMS runtime scaffold."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SRC_FILES = {
    "src/api/main.py",
    "src/api/routes/runs.py",
    "src/api/routes/approvals.py",
    "src/worker/main.py",
    "src/worker/jobs/intake.py",
    "src/domain/entities/run.py",
    "src/domain/entities/wiki.py",
    "src/services/run_orchestration.py",
    "src/services/publisher.py",
    "src/storage/wiki_store.py",
    "src/storage/metadata.py",
    "src/kmi/index.html",
    "src/kmi/styles.css",
    "src/kmi/app.js",
    "src/infopedia/index.html",
    "src/infopedia/styles.css",
    "src/infopedia/app.js",
    "src/config/settings.py",
    "src/agents/source_intake.py",
    "src/rules/policy.example.yaml",
    "src/templates/wiki_page.md",
    "src/observability/audit.py",
    "src/orchestrator/state_machine.py",
    "src/scripts/run_api.py",
    "src/scripts/validate_project.py",
}

REJECTED_PATHS = {
    "src/components",
    "apps",
    "packages",
    "config",
    "agents",
    "rules",
    "templates",
    "wiki",
    "raw",
    "docs",
    "scripts",
}


class SrcRuntimeScaffoldTests(unittest.TestCase):
    def test_required_runtime_scaffold_files_exist_under_src(self) -> None:
        missing = sorted(rel for rel in REQUIRED_SRC_FILES if not (ROOT / rel).is_file())
        self.assertEqual(missing, [])

    def test_rejected_runtime_scaffold_locations_are_absent(self) -> None:
        present = sorted(rel for rel in REJECTED_PATHS if (ROOT / rel).exists())
        self.assertEqual(present, [])

    def test_frontend_scaffolds_are_plain_html_css_js(self) -> None:
        for rel in ["src/kmi/index.html", "src/infopedia/index.html"]:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", text.lower())
            self.assertIn("app.js", text)
            self.assertIn("styles.css", text)

    def test_kmi_defaults_to_root_test_source_fixture(self) -> None:
        app_js = (ROOT / "src/kmi/app.js").read_text(encoding="utf-8")

        self.assertIn("tests/kmi-source", app_js)
        self.assertIn("stage-nav", app_js)
        self.assertIn("Candidate", app_js)
        self.assertIn("Review &amp; Approve", app_js)
        self.assertIn("Publish wiki", app_js)
        self.assertIn("Create candidates", app_js)
        self.assertIn("Candidate list", app_js)
        self.assertIn("Rejected candidates", app_js)
        self.assertIn("Browse local source", app_js)
        self.assertIn("localSourcePicker", app_js)
        self.assertIn("source_files", app_js)
        self.assertIn("Open review", app_js)
        self.assertIn("Apply selected reviews", app_js)
        self.assertIn("Feedback", app_js)
        self.assertIn("Candidate", app_js)
        self.assertIn("Rejected items stay visible here", app_js)
        self.assertIn("Publish approved candidates to wiki", app_js)
        self.assertIn("Publish details", app_js)
        self.assertIn("Default decision is approve", app_js)
        self.assertNotIn("Approve all candidates", app_js)
        self.assertNotIn("Load to wiki", app_js)
        self.assertNotIn("Run output", app_js)
        self.assertNotIn("Approve with Mods", app_js)
        self.assertNotIn("Open candidate", app_js)
        self.assertNotIn("OpenAI", app_js)
        self.assertNotIn("LLM", app_js)
        self.assertNotIn("Knowledge Manager", app_js)
        self.assertNotIn("seedDemo", app_js)
        self.assertIn("restart the KMS API server", app_js)
        self.assertIn("searchParams.get('candidate_id')", app_js)
        self.assertIn("Open review", app_js)
        self.assertIn("scrollIntoView", app_js)
        info_js = (ROOT / "src/infopedia/app.js").read_text(encoding="utf-8")
        self.assertIn("confidence_score", info_js)
        self.assertIn("semantic and keyword", info_js)
        self.assertIn("searchParams.get('page')", info_js)
        self.assertIn("Open published source", info_js)
        self.assertIn("pagePanel", info_js)
        self.assertNotIn("include_candidates=true", info_js)
        self.assertNotIn("Include candidate proposals", info_js)
        self.assertNotIn("LLM", info_js)
        self.assertNotIn("OpenAI", info_js)
        self.assertNotIn("Knowledge Manager", info_js)
        self.assertTrue((ROOT / "src/kmi/favicon.svg").is_file())
        self.assertTrue((ROOT / "src/infopedia/favicon.svg").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/metrics/revenue.md").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/procedures/monthly-close-procedure.md").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/codes/revenue-status-codes.md").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/data-dictionaries/revenue-data-dictionary.md").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/codes/python/order_service.py").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/codes/sql/monthly_close.sql").is_file())
        self.assertTrue((ROOT / "tests/kmi-source/codes/bash/release_audit.sh").is_file())


    def test_api_has_non_error_favicon_response(self) -> None:
        from src.api.main import MinimalASGIApp

        app = MinimalASGIApp()
        messages: list[dict[str, object]] = []

        async def receive() -> dict[str, object]:
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message: dict[str, object]) -> None:
            messages.append(message)

        import asyncio

        asyncio.run(app({"type": "http", "method": "GET", "path": "/favicon.ico", "query_string": b""}, receive, send))

        self.assertEqual(messages[0]["status"], 204)
        self.assertEqual(messages[1]["body"], b"")

    def test_representative_endpoints_are_wired_in_minimal_asgi(self) -> None:
        from src.api.main import MinimalASGIApp

        async def async_call(path: str, method: str = "GET", body: bytes = b"") -> tuple[int, str]:
            app = MinimalASGIApp()
            messages: list[dict[str, object]] = []

            async def receive() -> dict[str, object]:
                return {"type": "http.request", "body": body, "more_body": False}

            async def send(message: dict[str, object]) -> None:
                messages.append(message)

            await app({"type": "http", "method": method, "path": path, "query_string": b""}, receive, send)
            return int(messages[0]["status"]), bytes(messages[1].get("body", b"")).decode("utf-8")

        import asyncio

        def call(path: str) -> tuple[int, str]:
            return asyncio.run(async_call(path))

        self.assertEqual(call("/api/health/findings")[0], 200)
        self.assertIn("revision_not_found", call("/api/reviews/missing/diff")[1])
        self.assertIn("contradiction_not_found", call("/api/contradictions/missing")[1])

    def test_start_dev_supports_src_cwd_without_nested_src_package(self) -> None:
        start_dev = (ROOT / "src/scripts/start-dev.sh").read_text(encoding="utf-8")

        self.assertIn('export PYTHONPATH="$REPO_ROOT', start_dev)
        self.assertFalse((ROOT / "src/src").exists())
        result = subprocess.run(
            [sys.executable, "-c", "import src.api.main; print('ok')"],
            cwd=ROOT / "src",
            env={"PYTHONPATH": str(ROOT)},
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
