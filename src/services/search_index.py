"""Search index service built from finalized wiki markdown."""

from __future__ import annotations

from hashlib import sha256

from src.contracts import SearchDocument
from src.storage.search_index import SearchIndexStore
from src.storage.wiki_store import WikiStore


def rebuild_search_index(wiki_store: WikiStore, index_store: SearchIndexStore) -> list[SearchDocument]:
    docs: list[SearchDocument] = []
    for index, path in enumerate(wiki_store.list_pages(), start=1):
        content = path.read_text(encoding="utf-8")
        rel = path.relative_to(wiki_store.root).as_posix()
        title = next((line[2:].strip() for line in content.splitlines() if line.startswith("# ")), rel[:-3])
        docs.append(SearchDocument(f"search-{index}", "wiki_page", f"page-{index}", title, content, sha256(content.encode()).hexdigest(), path=rel))
    index_store.replace_all(docs)
    return docs


__all__ = ["rebuild_search_index"]
