"""Run artifact storage for derived evidence."""

from __future__ import annotations

from pathlib import Path

from src.config.paths import resolve_under


class ArtifactStore:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def write_text(self, run_id: str, name: str, content: str) -> Path:
        target = resolve_under(self.root, f"{run_id}/{name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def list_run_artifacts(self, run_id: str) -> list[str]:
        run_root = resolve_under(self.root, run_id)
        if not run_root.exists():
            return []
        return sorted(path.relative_to(run_root).as_posix() for path in run_root.rglob("*") if path.is_file())


__all__ = ["ArtifactStore"]
