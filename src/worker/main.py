"""Worker entrypoint."""
from __future__ import annotations
from src.worker.jobs.intake import run_intake
def main(source_path: str, *, run_id: str = "run-1", auto_approve: bool = False) -> int:
    result = run_intake(source_path, run_id=run_id, auto_approve=auto_approve)
    return 0 if result.run.state.value in {"completed", "blocked"} else 1
__all__ = ["main", "run_intake"]
