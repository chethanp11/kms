from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from kms_domain import InfopediaNode, MetadataStore, SearchDocument, WikiPage, WikiPageRevision

from kms_api.wiki.conventions import canonical_page_path, slugify

WIKI_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class ProjectionRefreshResult:
    generated_at: str
    wiki_node_count: int
    operational_doc_count: int
    wiki_doc_count: int
    stale_page_count: int


@dataclass(frozen=True)
class InfopediaProjectionService:
    store: MetadataStore
    wiki_root: Path

    def refresh(self) -> ProjectionRefreshResult:
        finalized_pages = self._finalized_pages()
        page_payloads = [self._page_payload(page) for page in finalized_pages]
        link_map = self._link_map(page_payloads)

        nodes: list[InfopediaNode] = []
        wiki_docs: list[SearchDocument] = []
        stale_page_count = 0

        for payload in page_payloads:
            related_slugs = sorted(link_map["outgoing"].get(payload["slug"], set()))
            backlink_slugs = sorted(link_map["incoming"].get(payload["slug"], set()))
            freshness = payload["freshness"]
            if freshness != "current":
                stale_page_count += 1
            node = InfopediaNode(
                node_id=payload["page_id"],
                page_id=payload["page_id"],
                title=payload["title"],
                slug=payload["slug"],
                path=payload["path"],
                freshness_status=freshness,
                status="active",
                updated_at=payload["updated_at"],
                page_type=payload["page_type"],
                domain=payload["domain"],
                confidence_status=payload["confidence"],
                source_trace_summary=payload["source_trace_summary"],
                related_slugs=related_slugs,
                backlink_count=len(backlink_slugs),
                summary=payload["summary"],
            )
            nodes.append(node)
            wiki_docs.append(
                SearchDocument(
                    search_doc_id=payload["page_id"],
                    title=payload["title"],
                    content=payload["content"],
                    status=freshness,
                    updated_at=payload["updated_at"],
                    scope="wiki",
                    document_type=payload["page_type"],
                    slug=payload["slug"],
                    page_type=payload["page_type"],
                    domain=payload["domain"],
                    freshness_status=freshness,
                    confidence_status=payload["confidence"],
                    snippet=_build_snippet(payload["content"]),
                    source_trace_summary=payload["source_trace_summary"],
                    related_slugs=related_slugs,
                    backlink_count=len(backlink_slugs),
                    page_id=payload["page_id"],
                    run_id=payload["run_id"],
                )
            )

        operational_docs = self._build_operational_documents()
        self.store.replace_infopedia_nodes(nodes)
        self.store.replace_search_documents([*wiki_docs, *operational_docs])

        return ProjectionRefreshResult(
            generated_at=_timestamp(),
            wiki_node_count=len(nodes),
            operational_doc_count=len(operational_docs),
            wiki_doc_count=len(wiki_docs),
            stale_page_count=stale_page_count,
        )

    def tree(self, *, domain: Optional[str] = None) -> Dict[str, Any]:
        self._ensure_projection_state()
        nodes = self._finalized_nodes(domain=domain)
        grouped: Dict[str, Dict[str, Any]] = {}
        for node in nodes:
            domain_key = node.domain or "unknown"
            family = node.page_type
            domain_bucket = grouped.setdefault(
                domain_key,
                {
                    "domain": domain_key,
                    "title": _titleize(domain_key),
                    "count": 0,
                    "children": {},
                },
            )
            family_bucket = domain_bucket["children"].setdefault(
                family,
                {
                    "page_type": family,
                    "title": _page_family_title(family),
                    "count": 0,
                    "pages": [],
                },
            )
            family_bucket["count"] += 1
            family_bucket["pages"].append(_node_leaf(node))
            domain_bucket["count"] += 1

        domains = []
        for domain_name in sorted(grouped):
            domain_bucket = grouped[domain_name]
            children = [domain_bucket["children"][page_type] for page_type in sorted(domain_bucket["children"])]
            domains.append(
                {
                    "domain": domain_bucket["domain"],
                    "title": domain_bucket["title"],
                    "count": domain_bucket["count"],
                    "children": children,
                }
            )

        return {
            "generated_at": _timestamp(),
            "summary": {"page_count": len(nodes), "domain_count": len(domains)},
            "domains": domains,
        }

    def search(
        self,
        *,
        query: str = "",
        domain: Optional[str] = None,
        page_type: Optional[str] = None,
        freshness: Optional[str] = None,
        confidence: Optional[str] = None,
        status: Optional[str] = None,
        scope: str = "wiki",
    ) -> Dict[str, Any]:
        self._ensure_projection_state()
        query_text = query.strip().lower()
        docs = self.store.list_search_documents(scope=scope)
        filtered: list[SearchDocument] = []
        for document in docs:
            if domain and document.domain != domain:
                continue
            if page_type and document.page_type != page_type:
                continue
            if freshness and document.freshness_status != freshness:
                continue
            if confidence and document.confidence_status != confidence:
                continue
            if status and document.status != status:
                continue
            if query_text and query_text not in _search_blob(document):
                continue
            filtered.append(document)

        facets = _facet_counts(filtered)
        return {
            "generated_at": _timestamp(),
            "query": query,
            "filters": {
                "domain": domain,
                "page_type": page_type,
                "freshness": freshness,
                "confidence": confidence,
                "status": status,
                "scope": scope,
            },
            "total": len(filtered),
            "items": [_search_result(document) for document in filtered],
            "facets": facets,
        }

    def page(self, slug: str) -> Dict[str, Any]:
        self._ensure_projection_state()
        node = self._node_by_slug(slug)
        if node is None:
            raise KeyError(slug)
        revision = self._revision_for_page_id(node.page_id)
        content = self._read_content(revision)
        related_pages, backlinks = self._link_payloads()
        related = related_pages.get(node.slug, [])
        backlink_links = backlinks.get(node.slug, [])
        page_record = _node_payload(node)
        page_record["status"] = "finalized"
        page_record["current_revision_id"] = revision.revision_id if revision is not None else None
        return {
            "generated_at": _timestamp(),
            "page": page_record,
            "breadcrumbs": _breadcrumbs(page_record),
            "content_markdown": content,
            "source_trace_summary": list(node.source_trace_summary),
            "related_pages": related,
            "backlinks": backlink_links,
            "siblings": self._siblings(node),
        }

    def search_documents(self, *, scope: Optional[str] = None) -> list[SearchDocument]:
        self._ensure_projection_state()
        return self.store.list_search_documents(scope=scope)

    def infopedia_nodes(self, *, domain: Optional[str] = None) -> list[InfopediaNode]:
        self._ensure_projection_state()
        nodes = self._finalized_nodes(domain=domain)
        return nodes

    def _ensure_projection_state(self) -> None:
        if not self.store.list_infopedia_nodes(status="active") or not self.store.list_search_documents():
            self.refresh()

    def _finalized_pages(self) -> list[WikiPage]:
        pages = [page for page in self.store.list_wiki_pages() if page.status == "finalized"]
        pages.sort(key=lambda page: (page.slug, page.title))
        return pages

    def _finalized_nodes(self, *, domain: Optional[str] = None) -> list[InfopediaNode]:
        nodes = self.store.list_infopedia_nodes(status="active")
        if domain:
            nodes = [node for node in nodes if node.domain == domain]
        nodes.sort(key=lambda node: (node.domain, node.page_type, node.title))
        return nodes

    def _page_payload(self, page: WikiPage) -> Dict[str, Any]:
        revision = self._revision_for_page_id(page.page_id)
        content = self._read_content(revision)
        domain = revision.draft_domain if revision is not None else ""
        related = list(_normalize_related_tokens(revision.draft_frontmatter.get("related", []) if revision else []))
        path = revision.draft_path if revision is not None else str(canonical_page_path(page.page_type, domain or None, page.slug))
        summary = _page_summary(content)
        return {
            "page_id": page.page_id,
            "run_id": revision.run_id if revision is not None else None,
            "slug": page.slug,
            "title": page.title,
            "page_type": page.page_type,
            "domain": domain,
            "status": page.status,
            "freshness": page.freshness_status,
            "confidence": page.confidence_status,
            "updated_at": page.updated_at,
            "path": path,
            "source_trace_summary": list(revision.source_trace_ids) if revision else [],
            "related_slugs": related,
            "content": content,
            "summary": summary,
        }

    def _revision_for_page_id(self, page_id: str) -> WikiPageRevision | None:
        revisions = self.store.list_wiki_page_revisions(page_id)
        if not revisions:
            return None
        revisions.sort(key=lambda revision: revision.created_at, reverse=True)
        return revisions[0]

    def _read_content(self, revision: WikiPageRevision | None) -> str:
        if revision is None:
            return ""
        content_path = self.wiki_root / revision.draft_path
        if content_path.exists():
            return content_path.read_text(encoding="utf-8")
        return revision.draft_markdown

    def _build_operational_documents(self) -> list[SearchDocument]:
        docs: list[SearchDocument] = []
        for run in self.store.list_runs():
            docs.append(
                SearchDocument(
                    search_doc_id=f"run::{run.run_id}",
                    title=f"Run {run.run_id}",
                    content=_run_summary_text(run),
                    status="current",
                    updated_at=run.completed_at or run.started_at or run.created_at,
                    scope="operational",
                    document_type="run",
                    freshness_status="current",
                    confidence_status="medium",
                    snippet=_run_summary_text(run),
                    source_trace_summary=[],
                    related_slugs=[],
                    backlink_count=0,
                    run_id=run.run_id,
                )
            )
        for revision in self.store.list_wiki_page_revisions():
            docs.append(
                SearchDocument(
                    search_doc_id=f"revision::{revision.revision_id}",
                    title=revision.draft_title or revision.revision_id,
                    content=revision.diff_summary,
                    status="current" if revision.status == "finalized" else "stale",
                    updated_at=revision.finalized_at or revision.created_at,
                    scope="operational",
                    document_type="revision",
                    slug=revision.draft_slug,
                    page_type=revision.draft_page_type,
                    domain=revision.draft_domain,
                    freshness_status="current" if revision.status == "finalized" else "stale",
                    confidence_status=_confidence_from_revision(revision),
                    snippet=_build_snippet(revision.diff_summary),
                    source_trace_summary=list(revision.source_trace_ids),
                    related_slugs=list(_normalize_related_tokens(revision.draft_frontmatter.get("related", []))),
                    backlink_count=0,
                    page_id=revision.page_id,
                    run_id=revision.run_id,
                )
            )
        for contradiction in self.store.list_contradictions():
            docs.append(
                SearchDocument(
                    search_doc_id=f"contradiction::{contradiction.contradiction_id}",
                    title=contradiction.contradiction_id,
                    content=" | ".join(contradiction.conflicting_claims),
                    status="current" if contradiction.status == "resolved" else "stale",
                    updated_at=contradiction.resolved_at or contradiction.created_at,
                    scope="operational",
                    document_type="contradiction",
                    slug=contradiction.contradiction_id,
                    freshness_status="current" if contradiction.status == "resolved" else "stale",
                    confidence_status=_severity_to_confidence(contradiction.severity),
                    snippet=" | ".join(contradiction.conflicting_claims),
                    source_trace_summary=list(contradiction.source_refs),
                    related_slugs=[],
                    backlink_count=0,
                    page_id=contradiction.page_id,
                    run_id=contradiction.run_id,
                )
            )
        for finding in self.store.list_lint_findings():
            docs.append(
                SearchDocument(
                    search_doc_id=f"lint::{finding.lint_finding_id}",
                    title=finding.code,
                    content=finding.message,
                    status="current" if finding.resolved_at else "stale",
                    updated_at=finding.resolved_at or finding.created_at,
                    scope="operational",
                    document_type="lint",
                    slug=finding.lint_finding_id,
                    freshness_status="current" if finding.resolved_at else "stale",
                    confidence_status="medium",
                    snippet=finding.message,
                    source_trace_summary=[],
                    related_slugs=[],
                    backlink_count=0,
                    page_id=finding.page_id,
                    run_id=finding.run_id,
                )
            )
        return docs

    def _link_payloads(self) -> tuple[Dict[str, list[Dict[str, Any]]], Dict[str, list[Dict[str, Any]]]]:
        nodes = self._finalized_nodes()
        nodes_by_slug = {node.slug: node for node in nodes}
        outgoing: Dict[str, set[str]] = defaultdict(set)
        incoming: Dict[str, set[str]] = defaultdict(set)
        for node in nodes:
            for related_slug in node.related_slugs:
                if related_slug not in nodes_by_slug:
                    continue
                outgoing[node.slug].add(related_slug)
                incoming[related_slug].add(node.slug)
        return (
            {slug: [_node_link_payload(nodes_by_slug[target_slug]) for target_slug in sorted(targets)] for slug, targets in outgoing.items()},
            {slug: [_node_link_payload(nodes_by_slug[source_slug]) for source_slug in sorted(sources)] for slug, sources in incoming.items()},
        )

    def _siblings(self, node: InfopediaNode) -> list[Dict[str, Any]]:
        siblings = []
        for candidate in self._finalized_nodes(domain=node.domain):
            if candidate.slug == node.slug or candidate.page_type != node.page_type:
                continue
            siblings.append(_node_link_payload(candidate))
        return siblings

    def _node_by_slug(self, slug: str) -> InfopediaNode | None:
        for node in self._finalized_nodes():
            if node.slug == slug:
                return node
        return None

    def _link_map(self, page_payloads: list[Dict[str, Any]]) -> Dict[str, Dict[str, set[str]]]:
        outgoing: Dict[str, set[str]] = defaultdict(set)
        incoming: Dict[str, set[str]] = defaultdict(set)
        payloads_by_slug = {page["slug"]: page for page in page_payloads}
        for payload in page_payloads:
            for related_slug in payload["related_slugs"]:
                if related_slug not in payloads_by_slug:
                    continue
                outgoing[payload["slug"]].add(related_slug)
                incoming[related_slug].add(payload["slug"])
            for related_slug in _extract_link_slugs(payload["content"]):
                if related_slug not in payloads_by_slug:
                    continue
                outgoing[payload["slug"]].add(related_slug)
                incoming[related_slug].add(payload["slug"])
        return {"outgoing": outgoing, "incoming": incoming}


def _search_blob(document: SearchDocument) -> str:
    parts = [
        document.title,
        document.content,
        document.scope,
        document.document_type,
        document.page_type,
        document.domain,
        document.status,
        document.freshness_status,
        document.confidence_status,
        " ".join(document.source_trace_summary),
    ]
    return "\n".join(part.lower() for part in parts if part)


def _facet_counts(documents: list[SearchDocument]) -> Dict[str, Any]:
    def tally(values: Iterable[str]) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for value in values:
            counts[str(value)] += 1
        return dict(sorted(counts.items()))

    return {
        "domains": tally(document.domain for document in documents if document.domain),
        "page_types": tally(document.page_type for document in documents if document.page_type),
        "freshness": tally(document.freshness_status for document in documents),
        "confidence": tally(document.confidence_status for document in documents),
        "status": tally(document.status for document in documents),
    }


def _search_result(document: SearchDocument) -> Dict[str, Any]:
    return {
        "slug": document.slug or document.page_id or document.search_doc_id,
        "title": document.title,
        "page_type": document.page_type,
        "domain": document.domain,
        "status": document.status,
        "freshness": document.freshness_status,
        "confidence": document.confidence_status,
        "updated_at": document.updated_at,
        "path": "",
        "snippet": document.snippet or _build_snippet(document.content),
        "source_trace_summary": list(document.source_trace_summary),
        "related_count": len(document.related_slugs),
        "backlink_count": document.backlink_count,
    }


def _node_leaf(node: InfopediaNode) -> Dict[str, Any]:
    return {
        "slug": node.slug,
        "title": node.title,
        "page_type": node.page_type,
        "domain": node.domain,
        "status": node.status,
        "freshness": node.freshness_status,
        "confidence": node.confidence_status,
        "updated_at": node.updated_at,
    }


def _node_payload(node: InfopediaNode) -> Dict[str, Any]:
    return {
        "page_id": node.page_id,
        "slug": node.slug,
        "title": node.title,
        "page_type": node.page_type,
        "domain": node.domain,
        "status": node.status,
        "freshness": node.freshness_status,
        "confidence": node.confidence_status,
        "updated_at": node.updated_at,
        "current_revision_id": node.page_id,
        "path": node.path,
        "source_trace_summary": list(node.source_trace_summary),
        "related_slugs": list(node.related_slugs),
        "summary": node.summary,
    }


def _node_link_payload(node: InfopediaNode) -> Dict[str, Any]:
    return {
        "slug": node.slug,
        "title": node.title,
        "page_type": node.page_type,
        "domain": node.domain,
        "status": node.status,
        "freshness": node.freshness_status,
        "confidence": node.confidence_status,
    }


def _breadcrumbs(page: Dict[str, Any]) -> list[Dict[str, str]]:
    return [
        {"title": "Infopedia", "slug": "/"},
        {"title": _titleize(page["domain"]), "slug": f"/?domain={page['domain']}"},
        {"title": _page_family_title(page["page_type"]), "slug": f"/search?page_type={page['page_type']}&domain={page['domain']}"},
        {"title": page["title"], "slug": f"/page/{page['slug']}"},
    ]


def _extract_link_slugs(content: str) -> Iterable[str]:
    for match in WIKI_LINK_PATTERN.finditer(content or ""):
        slug = _normalize_target(match.group(1))
        if slug:
            yield slug


def _normalize_related_tokens(tokens: Iterable[Any]) -> Iterable[str]:
    for token in tokens:
        slug = _normalize_target(str(token))
        if slug:
            yield slug


def _normalize_target(target: str) -> str:
    raw = target.strip()
    if not raw or raw.startswith("raw:"):
        return ""
    raw = raw.split("#", 1)[0]
    if raw.startswith("/wiki/"):
        raw = raw[len("/wiki/") :]
    if raw.startswith("/"):
        raw = raw[1:]
    if raw.endswith(".md"):
        raw = raw[:-3]
    if "/" in raw:
        parts = [part for part in raw.split("/") if part]
        if len(parts) >= 3:
            return parts[-1]
        if len(parts) == 2:
            return parts[-1]
    return slugify(raw)


def _titleize(value: str) -> str:
    return value.replace("-", " ").replace("_", " ").title()


def _page_family_title(page_type: str) -> str:
    return {
        "domain": "Domains",
        "entity": "Entities",
        "process": "Processes",
        "concept": "Concepts",
        "decision": "Decisions",
        "metric": "Metrics",
        "data-asset": "Data Assets",
        "analysis-pattern": "Analysis Patterns",
        "validation-rule": "Validation Rules",
        "source-note": "Source Notes",
        "open-question": "Open Questions",
    }.get(page_type, page_type.replace("-", " ").title())


def _build_snippet(content: str, query_text: str = "") -> str:
    plain = re.sub(r"^#{1,6}\s+", "", content or "", flags=re.MULTILINE)
    plain = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", plain)
    plain = re.sub(r"`([^`]*)`", r"\1", plain)
    plain = re.sub(r"\n{2,}", "\n", plain).strip()
    if query_text:
        index = plain.lower().find(query_text.lower())
        if index >= 0:
            start = max(0, index - 80)
            end = min(len(plain), index + 160)
            return plain[start:end].strip()
    return plain[:220]


def _page_summary(content: str) -> str:
    for line in (content or "").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            return stripped[2:]
        return stripped
    return ""


def _run_summary_text(run: Any) -> str:
    parts = [
        f"Run {run.run_id}",
        f"Status: {run.status}",
        f"Source path: {run.source_path}",
        f"Stage: {run.current_stage or 'created'}",
    ]
    if getattr(run, "domain_hint", None):
        parts.append(f"Domain: {run.domain_hint}")
    if getattr(run, "run_notes", None):
        parts.append(f"Notes: {run.run_notes}")
    return "\n".join(parts)


def _confidence_from_revision(revision: WikiPageRevision) -> str:
    status = str(revision.status)
    if status == "finalized":
        return "high"
    if status == "approved":
        return "medium"
    return "medium"


def _severity_to_confidence(severity: str) -> str:
    if severity == "error":
        return "low"
    if severity == "warning":
        return "medium"
    return "high"


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
