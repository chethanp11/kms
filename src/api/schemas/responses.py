"""Response schema helpers."""
from __future__ import annotations
from src.services.run_orchestration import RuntimeResult

def run_result_response(result: RuntimeResult) -> dict[str, object]:
    return {"run_id": result.run.run_id, "state": result.run.state.value, "summary_counts": dict(result.run.summary_counts), "published": [item.page_path for item in result.published], "warnings": list(result.warnings)}

__all__ = ["run_result_response"]
