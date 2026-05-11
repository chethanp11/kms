"""Path helpers that preserve KMS authority boundaries."""

from __future__ import annotations

from pathlib import Path

from src.contracts import ValidationError


def safe_relative_path(value: str, *, suffix: str | None = None) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value or "//" in value:
        raise ValidationError("path must be a safe relative POSIX path")
    if suffix and not value.endswith(suffix):
        raise ValidationError(f"path must end with {suffix}")
    return Path(value)


def resolve_under(root: Path, relative_path: str, *, suffix: str | None = None) -> Path:
    rel = safe_relative_path(relative_path, suffix=suffix)
    target = (root / rel).resolve()
    root_resolved = root.resolve()
    if root_resolved != target and root_resolved not in target.parents:
        raise ValidationError("resolved path escapes root")
    return target


__all__ = ["resolve_under", "safe_relative_path"]
