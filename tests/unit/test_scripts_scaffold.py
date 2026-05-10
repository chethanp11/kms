"""Unit coverage for project scripts scaffold validation."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.validate_scaffold import REQUIRED_DIRS, REQUIRED_FILES, validate_scaffold


class ScriptsScaffoldTests(unittest.TestCase):
    def test_required_scaffold_lists_include_scripts_boundary(self) -> None:
        self.assertIn("scripts", REQUIRED_DIRS)
        self.assertIn("scripts/README.md", REQUIRED_FILES)
        self.assertIn("scripts/validate_scaffold.py", REQUIRED_FILES)

    def test_validate_scaffold_accepts_minimal_required_shape(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for rel in REQUIRED_DIRS:
                (root / rel).mkdir(parents=True, exist_ok=True)
            for rel in REQUIRED_FILES:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("present\n", encoding="utf-8")

            validate_scaffold(root)


if __name__ == "__main__":
    unittest.main()
