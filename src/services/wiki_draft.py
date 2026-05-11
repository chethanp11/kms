"""Create governed wiki page candidates from proposals."""

from __future__ import annotations

import re

from src.contracts import KnowledgePage, PageStatus
from src.services.source_analysis import AnalysisProposal


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "untitled"


def draft_pages(proposals: tuple[AnalysisProposal, ...]) -> tuple[KnowledgePage, ...]:
    pages: list[KnowledgePage] = []
    for proposal in proposals:
        slug = slugify(proposal.title)
        body = f"## Summary\n{proposal.summary}\n\n## Source Trace\n- {proposal.source_ref}\n"
        pages.append(KnowledgePage(page_id=f"page-{proposal.proposal_id.split('-')[-1]}", page_type=proposal.page_type, path=f"sources/{slug}.md", title=proposal.title, body=body, status=PageStatus.REVIEW_REQUIRED, source_refs=(proposal.source_ref,)))
    return tuple(pages)


__all__ = ["draft_pages", "slugify"]
