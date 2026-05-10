"""Unit coverage for the corrected src-only KMS runtime scaffold."""

from __future__ import annotations

from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
