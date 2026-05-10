"""Unit coverage for TEST-005 knowledge-model contracts."""

from __future__ import annotations

import unittest

from src.contracts import KnowledgePage, SourceFile, ValidationError


class KnowledgePageTests(unittest.TestCase):
    def test_renders_required_frontmatter_and_heading(self) -> None:
        page = KnowledgePage(
            page_type="definition",
            path="metrics/revenue.md",
            title="Revenue",
            body="Revenue is recognized after approval.",
        )

        markdown = page.to_markdown()

        self.assertIn("title: Revenue", markdown)
        self.assertIn("type: definition", markdown)
        self.assertIn("# Revenue", markdown)
        self.assertTrue(markdown.endswith("Revenue is recognized after approval.\n"))

    def test_rejects_invalid_page_path(self) -> None:
        with self.assertRaises(ValidationError):
            KnowledgePage(
                page_type="definition",
                path="../secrets.md",
                title="Invalid",
                body="Invalid path.",
            )


class SourceFileTests(unittest.TestCase):
    def test_rejects_invalid_sha256(self) -> None:
        with self.assertRaises(ValidationError):
            SourceFile(relative_path="source.md", sha256="not-a-digest", size_bytes=10)


if __name__ == "__main__":
    unittest.main()
