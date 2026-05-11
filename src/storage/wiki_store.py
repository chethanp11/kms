"""Filesystem-backed governed wiki store."""

from __future__ import annotations

from pathlib import Path

from src.config.paths import resolve_under
from src.contracts import KnowledgePage, ValidationError


class WikiStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def write_page(self, page: KnowledgePage) -> Path:
        target = resolve_under(self.root, page.path, suffix=".md")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page.to_markdown(), encoding="utf-8")
        return target

    def read_page(self, slug: str) -> str:
        path = f"{slug}.md" if not slug.endswith(".md") else slug
        target = resolve_under(self.root, path, suffix=".md")
        if not target.exists():
            raise ValidationError(f"wiki page not found: {slug}")
        return target.read_text(encoding="utf-8")

    def list_pages(self) -> list[Path]:
        return sorted(path for path in self.root.rglob("*.md") if path.is_file())


__all__ = ["WikiStore"]
