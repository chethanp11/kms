"""In-memory rebuildable search index."""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from src.contracts import SearchDocument


@dataclass
class SearchIndexStore:
    documents: dict[str, SearchDocument] = field(default_factory=dict)

    def replace_all(self, documents: list[SearchDocument]) -> None:
        self.documents = {doc.search_doc_id: doc for doc in documents}

    def search(self, query: str) -> list[SearchDocument]:
        return [doc for doc, _confidence in self.search_with_confidence(query)]

    def search_with_confidence(self, query: str) -> list[tuple[SearchDocument, float]]:
        q = query.casefold().strip()
        if not q:
            return [(doc, 1.0) for doc in self.documents.values()]
        scored = [(_match_score(doc, q), doc) for doc in self.documents.values()]
        positive = [(doc, _confidence(score)) for score, doc in sorted(scored, key=lambda item: item[0], reverse=True) if score > 0]
        return positive


def _match_score(doc: SearchDocument, query: str) -> int:
    haystack = f"{doc.title} {doc.content} {' '.join(doc.tags)}".casefold()
    score = 0
    if query in haystack:
        score += 100
    query_terms = _expand_terms(_terms(query))
    haystack_terms = _expand_terms(_terms(haystack))
    semantic_overlap = len(query_terms & haystack_terms)
    literal_overlap = len(_terms(query) & _terms(haystack))
    score += 10 * literal_overlap
    score += 6 * max(0, semantic_overlap - literal_overlap)
    return score


def _confidence(score: int) -> float:
    return round(min(0.99, max(0.05, score / 140)), 2)


def _terms(value: str) -> set[str]:
    return {term for term in re.findall(r"[a-z0-9]+", value.casefold()) if len(term) > 2}


def _expand_terms(terms: set[str]) -> set[str]:
    expanded = set(terms)
    groups = (
        {"approve", "approved", "approval", "review", "trusted", "governed"},
        {"publish", "published", "wiki", "canonical", "finalized", "final"},
        {"metric", "measure", "measured", "kpi", "revenue", "rate"},
        {"process", "workflow", "procedure", "stage", "step"},
        {"decision", "decide", "decided", "choice"},
        {"contradiction", "conflict", "disagree", "disagrees", "inconsistent"},
        {"entity", "owner", "team", "system", "service"},
    )
    for group in groups:
        if expanded & group:
            expanded |= group
    return expanded


__all__ = ["SearchIndexStore"]
