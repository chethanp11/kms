from __future__ import annotations

import hashlib
import re
from pathlib import Path

CANONICAL_PAGE_FOLDERS: dict[str, str] = {
    "domain": "domains",
    "entity": "entities",
    "process": "processes",
    "concept": "concepts",
    "decision": "decisions",
    "metric": "metrics",
    "data-asset": "data-assets",
    "analysis-pattern": "analysis-patterns",
    "validation-rule": "validation-rules",
    "source-note": "source-notes",
    "open-question": "open-questions",
}

CANONICAL_PAGE_TYPES = tuple(CANONICAL_PAGE_FOLDERS)
SPECIAL_PAGE_NAMES = {"index": "index.md", "log": "log.md"}


def slugify(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def canonical_page_type_folder(page_type: str) -> str:
    if page_type not in CANONICAL_PAGE_FOLDERS:
        raise ValueError(f"Unsupported wiki page type: {page_type}")
    return CANONICAL_PAGE_FOLDERS[page_type]


def resolve_page_slug(
    title: str,
    page_type: str,
    domain: str,
    identity_key: str | None = None,
    existing_slugs: set[str] | None = None,
) -> str:
    existing_slugs = existing_slugs or set()
    base_slug = slugify(title) or slugify(identity_key or f"{page_type}-{domain}")
    if base_slug not in existing_slugs:
        return base_slug

    collision_basis = "::".join(
        [page_type, domain, identity_key or title, base_slug]
    ).encode("utf-8")
    suffix = hashlib.sha256(collision_basis).hexdigest()[:8]
    candidate = f"{base_slug}-{suffix}"
    if candidate not in existing_slugs:
        return candidate

    counter = 2
    while True:
        trial = f"{base_slug}-{suffix}-{counter}"
        if trial not in existing_slugs:
            return trial
        counter += 1


def canonical_page_path(page_type: str, domain: str | None, slug: str) -> Path:
    if page_type in SPECIAL_PAGE_NAMES:
        return Path(SPECIAL_PAGE_NAMES[page_type])
    if not domain:
        raise ValueError("Canonical wiki pages require a domain")
    return Path(canonical_page_type_folder(page_type)) / domain / f"{slug}.md"
