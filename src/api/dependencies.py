"""Runtime dependency container for API route functions."""
from __future__ import annotations
from src.services.run_orchestration import KMSRuntime
_runtime: KMSRuntime | None = None
def get_runtime() -> KMSRuntime:
    global _runtime
    if _runtime is None:
        _runtime = KMSRuntime.create()
    return _runtime
def set_runtime(runtime: KMSRuntime) -> None:
    global _runtime
    _runtime = runtime
__all__ = ["get_runtime", "set_runtime"]
