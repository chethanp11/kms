"""KMS API entrypoint with optional FastAPI wiring."""

from __future__ import annotations

import json
from typing import Any, Awaitable, Callable, Dict, List
from urllib.parse import parse_qs

from src.api.routes.infopedia import search as search_pages
from src.api.routes.infopedia import tree as infopedia_tree
from src.api.routes.runs import create_run, get_run, list_artifacts
from src.api.routes.wiki import get_page
from src.app import REPRESENTATIVE_ENDPOINTS
from src.contracts import ValidationError

ASGIReceive = Callable[[], Awaitable[Dict[str, Any]]]
ASGISend = Callable[[Dict[str, Any]], Awaitable[None]]

_HEADERS = [
    (b"content-type", b"application/json"),
    (b"access-control-allow-origin", b"*"),
    (b"access-control-allow-methods", b"GET,POST,OPTIONS"),
    (b"access-control-allow-headers", b"content-type"),
]


class MinimalASGIApp:
    """Dependency-free ASGI fallback for local development smoke testing."""

    async def __call__(self, scope: Dict[str, Any], receive: ASGIReceive, send: ASGISend) -> None:
        if scope.get("type") != "http":
            return
        method = scope.get("method", "GET")
        path = scope.get("path", "/")
        query = parse_qs((scope.get("query_string") or b"").decode("utf-8"))
        if method == "OPTIONS":
            await self._send(send, 204, {})
            return
        try:
            status, payload = await self._dispatch(method, path, query, receive)
        except (KeyError, ValidationError, ValueError) as exc:
            status, payload = 400, {"error": str(exc)}
        except Exception as exc:  # pragma: no cover - defensive API boundary
            status, payload = 500, {"error": f"internal_error: {exc}"}
        await self._send(send, status, payload)

    async def _dispatch(self, method: str, path: str, query: Dict[str, list[str]], receive: ASGIReceive) -> tuple[int, Dict[str, Any] | list[Any]]:
        if path in {"/", "/api/health"}:
            return 200, {"status": "ok", "name": "KMS API", "endpoints": list(REPRESENTATIVE_ENDPOINTS)}
        if method == "POST" and path == "/api/runs":
            return 200, create_run(await self._read_json(receive))
        if method == "GET" and path.startswith("/api/runs/"):
            suffix = path.removeprefix("/api/runs/")
            if suffix.endswith("/artifacts"):
                return 200, {"artifacts": list_artifacts(suffix.removesuffix("/artifacts"))}
            run = get_run(suffix)
            return (200, run) if run else (404, {"error": "run_not_found"})
        if method == "GET" and path == "/api/infopedia/tree":
            return 200, infopedia_tree()
        if method == "GET" and path == "/api/infopedia/search":
            return 200, search_pages((query.get("q") or [""])[0])
        if method == "GET" and path.startswith("/api/wiki/pages/"):
            return 200, get_page(path.removeprefix("/api/wiki/pages/"))
        return 404, {"error": "not_found", "endpoints": list(REPRESENTATIVE_ENDPOINTS)}

    async def _read_json(self, receive: ASGIReceive) -> Dict[str, Any]:
        chunks = []
        more_body = True
        while more_body:
            message = await receive()
            chunks.append(message.get("body", b""))
            more_body = bool(message.get("more_body", False))
        raw = b"".join(chunks).decode("utf-8")
        return json.loads(raw or "{}")

    async def _send(self, send: ASGISend, status: int, payload: Dict[str, Any] | list[Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        await send({"type": "http.response.start", "status": status, "headers": _HEADERS + [(b"content-length", str(len(body)).encode("ascii"))]})
        await send({"type": "http.response.body", "body": body})


def create_app() -> object:
    try:
        from fastapi import FastAPI, HTTPException, Query  # type: ignore
        from fastapi.middleware.cors import CORSMiddleware  # type: ignore
    except Exception:
        return MinimalASGIApp()

    app = FastAPI(title="KMS API")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/")
    def _root() -> Dict[str, Any]:
        return {"status": "ok", "name": "KMS API", "endpoints": list(REPRESENTATIVE_ENDPOINTS)}

    @app.get("/api/health")
    def _health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.post("/api/runs")
    def _create_run(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return create_run(payload)
        except (KeyError, ValidationError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @app.get("/api/runs/{run_id}")
    def _get_run(run_id: str) -> Dict[str, Any]:
        run = get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail="run_not_found")
        return run

    @app.get("/api/runs/{run_id}/artifacts")
    def _list_artifacts(run_id: str) -> Dict[str, Any]:
        return {"artifacts": list_artifacts(run_id)}

    @app.get("/api/infopedia/tree")
    def _tree() -> List[Dict[str, Any]]:
        return infopedia_tree()

    @app.get("/api/infopedia/search")
    def _search(q: str = Query(default="")) -> List[Dict[str, Any]]:
        return search_pages(q)

    @app.get("/api/wiki/pages/{slug:path}")
    def _wiki_page(slug: str) -> Dict[str, str]:
        try:
            return get_page(slug)
        except ValidationError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

    return app


app = create_app()
__all__ = ["MinimalASGIApp", "app", "create_app"]
