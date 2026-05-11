"""KMS API entrypoint with optional FastAPI wiring."""

from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Dict

from src.app import REPRESENTATIVE_ENDPOINTS

ASGIReceive = Callable[[], Awaitable[Dict[str, Any]]]
ASGISend = Callable[[Dict[str, Any]], Awaitable[None]]


class MinimalASGIApp:
    """Dependency-free ASGI fallback for local development health checks."""

    async def __call__(self, scope: Dict[str, Any], receive: ASGIReceive, send: ASGISend) -> None:
        if scope.get("type") != "http":
            return
        path = scope.get("path", "/")
        if path in {"/", "/api/health"}:
            status = 200
            payload: Dict[str, Any] = {"status": "ok", "name": "KMS API"}
        else:
            status = 404
            payload = {"error": "not_found", "endpoints": list(REPRESENTATIVE_ENDPOINTS)}
        body = json.dumps(payload).encode("utf-8")
        await send({"type": "http.response.start", "status": status, "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode("ascii"))]})
        await send({"type": "http.response.body", "body": body})


def create_app() -> object:
    try:
        from fastapi import FastAPI  # type: ignore
    except Exception:
        return MinimalASGIApp()
    app = FastAPI(title="KMS API")

    @app.get("/api/health")
    def _health() -> Dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
__all__ = ["MinimalASGIApp", "app", "create_app"]
