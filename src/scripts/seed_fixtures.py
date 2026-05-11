"""Create a tiny local source fixture."""
from __future__ import annotations
from pathlib import Path
def seed(root: Path | str) -> Path:
    target = Path(root); target.mkdir(parents=True, exist_ok=True)
    (target / "overview.md").write_text("KMS fixture source.\n", encoding="utf-8")
    return target
__all__ = ["seed"]
