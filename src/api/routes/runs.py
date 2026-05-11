"""Run API route functions."""
from __future__ import annotations
from src.api.dependencies import get_runtime
from src.api.schemas.responses import run_result_response

def create_run(payload: dict[str, object]) -> dict[str, object]:
    result = get_runtime().start_run(str(payload["source_path"]), run_id=str(payload.get("run_id", "run-1")), auto_approve=bool(payload.get("auto_approve", False)))
    return run_result_response(result)

def get_run(run_id: str) -> dict[str, object] | None:
    run = get_runtime().metadata.get_run(run_id)
    return None if run is None else {"run_id": run.run_id, "state": run.state.value, "summary_counts": dict(run.summary_counts)}

def list_artifacts(run_id: str) -> list[str]:
    return get_runtime().artifacts.list_run_artifacts(run_id)
__all__ = ["create_run", "get_run", "list_artifacts"]
