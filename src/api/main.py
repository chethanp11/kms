"""KMS API entrypoint with optional FastAPI wiring."""
from __future__ import annotations
from src.app import REPRESENTATIVE_ENDPOINTS

def create_app() -> object:
    try:
        from fastapi import FastAPI  # type: ignore
    except Exception:
        return {"name": "KMS API", "endpoints": REPRESENTATIVE_ENDPOINTS}
    app = FastAPI(title="KMS API")
    @app.get("/api/health")
    def _health() -> dict[str, str]:
        return {"status": "ok"}
    return app

app = create_app()
__all__ = ["app", "create_app"]
