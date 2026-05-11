"""Parse raw source files into normalized source documents."""

from __future__ import annotations

from pathlib import Path

from src.contracts import ParseStatus, SourceBundle, SourceDocument

_TEXT_PREFIXES = ("text/",)
_TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".csv"}


def parse_source_bundle(bundle: SourceBundle, *, run_id: str) -> tuple[SourceDocument, ...]:
    documents: list[SourceDocument] = []
    root = Path(bundle.root_path)
    for index, source_file in enumerate(bundle.files, start=1):
        source_path = root / source_file.relative_path
        text = ""
        status = ParseStatus.PARSED
        if source_file.media_type.startswith(_TEXT_PREFIXES) or source_path.suffix.lower() in _TEXT_SUFFIXES:
            try:
                text = source_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = source_path.read_text(encoding="utf-8", errors="replace")
                status = ParseStatus.PARTIAL
        else:
            status = ParseStatus.PARTIAL
            text = f"Binary or unsupported source retained as evidence: {source_file.relative_path}"
        documents.append(SourceDocument(
            source_document_id=f"doc-{index}", source_file_id=source_file.source_file_id or f"source-{index}", run_id=run_id,
            title=Path(source_file.relative_path).stem.replace("-", " ").replace("_", " ").title(),
            content_type=source_file.media_type, text=text, parse_status=status, metadata={"relative_path": source_file.relative_path, "sha256": source_file.sha256},
        ))
    return tuple(documents)


__all__ = ["parse_source_bundle"]
