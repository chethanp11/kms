"""Worker job for source intake runs."""
from __future__ import annotations
from src.services.run_orchestration import KMSRuntime, RuntimeResult
def run_intake(source_path: str, *, run_id: str = "run-1", auto_approve: bool = False, runtime: KMSRuntime | None = None) -> RuntimeResult:
    return (runtime or KMSRuntime.create()).start_run(source_path, run_id=run_id, auto_approve=auto_approve)
__all__ = ["run_intake"]
