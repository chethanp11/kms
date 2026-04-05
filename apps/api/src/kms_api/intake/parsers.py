from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from .models import ParsedSource


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _summarize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines[:3])[:400] if lines else ""


def _extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            headings.append(line.lstrip("#").strip())
    return headings


def _strip_html(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_source_file(path: Path) -> ParsedSource:
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown", ".txt"}:
        text = _read_text(path)
        return ParsedSource(
            content_type="text/markdown" if suffix in {".md", ".markdown"} else "text/plain",
            normalized_text=text,
            summary=_summarize_text(text),
            extracted_signals=_extract_headings(text),
            parse_metadata={"line_count": str(len(text.splitlines()))},
        )

    if suffix == ".csv":
        raw = _read_text(path)
        rows = list(csv.reader(raw.splitlines()))
        header = rows[0] if rows else []
        normalized = "\n".join([", ".join(row) for row in rows])
        return ParsedSource(
            content_type="text/csv",
            normalized_text=normalized,
            summary=f"{len(rows)} rows, {len(header)} columns",
            extracted_signals=[f"column:{column}" for column in header],
            parse_metadata={
                "row_count": str(len(rows)),
                "column_count": str(len(header)),
            },
        )

    if suffix == ".json":
        raw = _read_text(path)
        data = json.loads(raw)
        flattened = json.dumps(data, indent=2, sort_keys=True)
        keys = sorted(data.keys()) if isinstance(data, dict) else []
        return ParsedSource(
            content_type="application/json",
            normalized_text=flattened,
            summary=_summarize_text(flattened),
            extracted_signals=[f"key:{key}" for key in keys],
            parse_metadata={"top_level_keys": ",".join(keys)},
        )

    if suffix in {".html", ".htm"}:
        raw = _read_text(path)
        normalized = _strip_html(raw)
        return ParsedSource(
            content_type="text/html",
            normalized_text=normalized,
            summary=_summarize_text(normalized),
            extracted_signals=_extract_headings(normalized),
            parse_metadata={"length": str(len(normalized))},
        )

    raise ValueError(f"Unsupported source type: {path.suffix}")

