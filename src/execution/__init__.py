"""Source intake execution helpers."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import mimetypes
from tempfile import mkdtemp

from src.config.paths import resolve_under
from src.contracts import SourceBundle, SourceFile, UploadedSourceFile, ValidationError


def discover_source_bundle(root: Path | str) -> SourceBundle:
    """Discover files below a raw source root in deterministic order."""

    root_path = Path(root).expanduser().resolve()
    if not root_path.exists():
        raise ValidationError(f"source root does not exist: {root_path}")
    if not root_path.is_dir():
        raise ValidationError(f"source root is not a directory: {root_path}")

    files: list[SourceFile] = []
    for path in sorted(item for item in root_path.rglob("*") if item.is_file()):
        digest = sha256(path.read_bytes()).hexdigest()
        rel = path.relative_to(root_path).as_posix()
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        files.append(SourceFile(relative_path=rel, sha256=digest, size_bytes=path.stat().st_size, media_type=media_type))

    warnings = ("source bundle is empty",) if not files else ()
    return SourceBundle(root_path=str(root_path), files=tuple(files), warnings=warnings)


def source_note_for_bundle(bundle: SourceBundle) -> str:
    """Render a deterministic source-note summary for review."""

    lines = ["# Source Bundle", "", f"Root: `{bundle.root_path}`", "", "| Path | Size | SHA-256 | Media Type |", "|---|---:|---|---|"]
    for item in bundle.files:
        lines.append(f"| `{item.relative_path}` | {item.size_bytes} | `{item.sha256}` | {item.media_type} |")
    if bundle.warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {warning}" for warning in bundle.warnings)
    return "\n".join(lines) + "\n"


def materialize_uploaded_source_files(files: tuple[UploadedSourceFile, ...], *, run_id: str) -> Path:
    """Write browser-selected source files into a temp root for governed parsing."""

    root = Path(mkdtemp(prefix=f"kms-upload-{run_id}-")).resolve()
    for item in files:
        target = resolve_under(root, item.relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(item.content, encoding="utf-8")
    return root


__all__ = ["discover_source_bundle", "materialize_uploaded_source_files", "source_note_for_bundle"]
