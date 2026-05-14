"""Infopedia read-only API routes."""
from __future__ import annotations
from hashlib import sha256
from src.api.dependencies import get_runtime
from src.contracts import SearchDocument
from src.services.infopedia_projection import build_tree
from src.services.search_index import rebuild_search_index
from src.storage.search_index import SearchIndexStore

def tree() -> list[dict[str, object]]:
    return [node.__dict__ for node in build_tree(get_runtime().wiki)]

def search(query: str, *, include_candidates: bool = False) -> list[dict[str, object]]:
    runtime = get_runtime()
    rebuild_search_index(runtime.wiki, runtime.search)
    documents = [{**doc.__dict__, "confidence_score": confidence} for doc, confidence in runtime.search.search_with_confidence(query)]
    if include_candidates:
        candidate_index = SearchIndexStore({doc.search_doc_id: doc for doc in _candidate_search_documents()})
        documents.extend({**doc.__dict__, "confidence_score": confidence} for doc, confidence in candidate_index.search_with_confidence(query))
    return documents

def _candidate_search_documents() -> list[SearchDocument]:
    runtime = get_runtime()
    docs: list[SearchDocument] = []
    for index, candidate in enumerate(runtime.metadata.knowledge_candidates.values(), start=1):
        status = "archived" if candidate.candidate_id in runtime.metadata.archived_candidate_ids else "candidate"
        approved = "approved" if candidate.candidate_id in runtime.metadata.approved_candidate_ids else "unapproved"
        content = "\n".join([candidate.title, candidate.excerpt, candidate.rationale, candidate.source_ref, status, approved])
        docs.append(SearchDocument(
            f"candidate-search-{index}",
            "knowledge_candidate",
            candidate.candidate_id,
            candidate.title,
            content,
            sha256(content.encode()).hexdigest(),
            path=candidate.target_slug or f"candidates/{candidate.candidate_id}",
            tags=(candidate.candidate_type.value, status, approved),
        ))
    return docs

__all__ = ["search", "tree"]
