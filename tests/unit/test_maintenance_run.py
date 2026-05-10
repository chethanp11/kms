"""Unit coverage for TEST-001 source-bundle discovery and source notes."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.execution import discover_source_bundle, source_note_for_bundle


class MaintenanceRunTests(unittest.TestCase):
    def test_discovers_sources_in_deterministic_order(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "b.md").write_text("second", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "a.md").write_text("first", encoding="utf-8")

            bundle = discover_source_bundle(root)

        self.assertEqual([item.relative_path for item in bundle.files], ["b.md", "nested/a.md"])
        self.assertEqual(len(bundle.files[0].sha256), 64)

    def test_source_note_contains_discovered_files(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "source.md").write_text("source body", encoding="utf-8")

            note = source_note_for_bundle(discover_source_bundle(root))

        self.assertIn("# Source Bundle", note)
        self.assertIn("source.md", note)
        self.assertIn("SHA-256", note)


if __name__ == "__main__":
    unittest.main()
