"""In-memory rebuildable search index."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.contracts import SearchDocument


@dataclass
class SearchIndexStore:
    documents: dict[str, SearchDocument] = field(default_factory=dict)

    def replace_all(self, documents: list[SearchDocument]) -> None:
        self.documents = {doc.search_doc_id: doc for doc in documents}

    def search(self, query: str) -> list[SearchDocument]:
        q = query.casefold().strip()
        if not q:
            return list(self.documents.values())
        return [doc for doc in self.documents.values() if q in doc.title.casefold() or q in doc.content.casefold()]


__all__ = ["SearchIndexStore"]
