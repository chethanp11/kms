from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Union

SectionValue = Union[str, List[str]]


@dataclass(frozen=True)
class WikiLink:
    title: str
    path: str


@dataclass(frozen=True)
class WikiPageBlueprint:
    page_type: str
    folder: str
    template_file: str
    body_sections: tuple[str, ...]


@dataclass
class WikiDraftInput:
    title: str
    page_type: str
    domain: str
    section_content: dict[str, SectionValue] = field(default_factory=dict)
    source_refs: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    owners: list[str] = field(default_factory=list)
    last_updated: str = ""
    confidence: Literal["low", "medium", "high", "provisional"] = "medium"
    review_required: bool = True
    status: Literal["draft", "review_required", "finalized", "archived"] = "review_required"
    identity_key: str | None = None


@dataclass
class WikiDraftResult:
    title: str
    slug: str
    page_type: str
    domain: str
    path: str
    content_markdown: str
    frontmatter: dict[str, object]
    template_file: str
    section_content: dict[str, SectionValue] = field(default_factory=dict)


@dataclass
class WikiRevisionWriteResult:
    page_id: str
    revision_id: str
    path: str
    written_to_wiki: bool
    change_type: Literal["create", "update"]
    page_status: Literal["draft", "finalized"]
