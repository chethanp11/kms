from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .models import DiscoveredSource

SUPPORTED_EXTENSIONS = {
    ".md": ("markdown", "markdown"),
    ".markdown": ("markdown", "markdown"),
    ".txt": ("text", "plain-text"),
    ".csv": ("tabular", "tabular-parser"),
    ".json": ("json", "json-parser"),
    ".html": ("html", "html-parser"),
    ".htm": ("html", "html-parser"),
}


@dataclass
class DiscoveryResult:
    sources: list[DiscoveredSource]


def checksum_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_source_files(source_root: Path) -> DiscoveryResult:
    sources: list[DiscoveredSource] = []
    for file_path in sorted(p for p in source_root.rglob("*") if p.is_file()):
        extension = file_path.suffix.lower()
        classification, parser_route = SUPPORTED_EXTENSIONS.get(
            extension, ("unsupported", None)
        )
        support_status = "supported" if parser_route else "unsupported"
        sources.append(
            DiscoveredSource(
                absolute_path=str(file_path.resolve()),
                relative_path=str(file_path.relative_to(source_root)),
                file_name=file_path.name,
                file_size_bytes=file_path.stat().st_size,
                extension=extension,
                checksum_sha256=checksum_sha256(file_path),
                support_status=support_status,
                classification=classification,
                parser_route=parser_route,
            )
        )
    return DiscoveryResult(sources=sources)
