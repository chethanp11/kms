"""Read-only Infopedia projection over finalized wiki pages."""

from __future__ import annotations

from src.contracts import InfopediaNode
from src.storage.wiki_store import WikiStore


def build_tree(wiki_store: WikiStore) -> list[InfopediaNode]:
    nodes: list[InfopediaNode] = []
    for index, path in enumerate(wiki_store.list_pages(), start=1):
        content = path.read_text(encoding="utf-8")
        rel = path.relative_to(wiki_store.root).as_posix()
        slug = rel[:-3]
        title = next((line[2:].strip() for line in content.splitlines() if line.startswith("# ")), slug)
        nodes.append(InfopediaNode(f"node-{index}", f"page-{index}", slug, title, "wiki_page", breadcrumbs=tuple(slug.split("/")[:-1])))
    return nodes


def read_page(wiki_store: WikiStore, slug: str) -> str:
    return wiki_store.read_page(slug)


__all__ = ["build_tree", "read_page"]
