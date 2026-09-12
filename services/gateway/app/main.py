from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any

try:
    import httpx
    from fastapi import FastAPI, HTTPException, Request, Response
    from fastapi.middleware.cors import CORSMiddleware
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    class FastAPI:  # type: ignore
        def __init__(self, *args, **kwargs):
            self.version = "0.1.0"
        def add_middleware(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def api_route(self, *args, **kwargs): return lambda f: f
    class HTTPException(Exception):  # type: ignore
        def __init__(self, status_code: int, detail: str = ""):
            self.status_code = status_code
            self.detail = detail
    class Request: pass  # type: ignore
    class Response: pass  # type: ignore
    class CORSMiddleware: pass  # type: ignore

from app.core.config import Settings, get_settings
from app.middleware.rate_limiter import RateLimitMiddleware, TokenBucketRateLimiter

# Hop-by-hop headers that must not be forwarded
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
    "host",
}


def _resolve_target_service(path: str, settings: Settings) -> str | None:
    if path.startswith("/.well-known/") or path.startswith("/api/v1/auth") or path.startswith("/api/v1/organizations") or path.startswith("/api/v1/roles"):
        return settings.identity_service_url
    if (
        path.startswith("/api/v1/patients")
        or path.startswith("/api/v1/encounters")
        or path.startswith("/api/v1/clinical-notes")
        or path.startswith("/api/v1/prescriptions")
        or path.startswith("/api/v1/appointments")
        or path.startswith("/api/v1/diagnostics")
    ):
        return settings.clinical_service_url
    if (
        path.startswith("/api/v1/taxonomy")
        or path.startswith("/api/v1/mufradat")
        or path.startswith("/api/v1/pharmacopoeia")
        or path.startswith("/api/v1/evidence")
        or path.startswith("/api/v1/graph")
    ):
        return settings.knowledge_service_url
    if (
        path.startswith("/api/v1/nuskha-drafts")
        or path.startswith("/api/v1/tadbeer-plans")
        or path.startswith("/api/v1/ghiza-plans")
        or path.startswith("/api/v1/care-plans")
    ):
        return settings.therapeutic_service_url
    if path.startswith("/api/v1/hakeem"):
        return settings.ai_service_url
    return None


def create_gateway_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if HAS_FASTAPI:
            app.state.client = httpx.AsyncClient(timeout=30.0)
            yield
            await app.state.client.aclose()
        else:
            yield

    app = FastAPI(
        title="ZAYVORA Unified API Gateway",
        version="0.1.0-phase1",
        description="Unified reverse-proxy gateway routing traffic to all 5 ZAYVORA Health microservices.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RateLimitMiddleware)

    @app.get("/api/health")
    async def aggregate_health():
        client: httpx.AsyncClient = app.state.client
        targets = {
            "identity": f"{settings.identity_service_url}/api/health",
            "clinical": f"{settings.clinical_service_url}/api/health",
            "knowledge": f"{settings.knowledge_service_url}/api/health",
            "therapeutic": f"{settings.therapeutic_service_url}/api/health",
            "ai": f"{settings.ai_service_url}/api/health",
        }

        async def _check_service(name: str, url: str) -> tuple[str, dict[str, Any]]:
            try:
                resp = await client.get(url, timeout=3.0)
                return name, {"status": "up" if resp.status_code == 200 else "degraded", "code": resp.status_code}
            except Exception as exc:
                return name, {"status": "down", "error": str(exc)}

        results = await asyncio.gather(*[_check_service(n, u) for n, u in targets.items()])
        service_statuses = dict(results)
        all_up = all(s.get("status") == "up" for s in service_statuses.values())

        return {
            "ok": all_up,
            "gateway": "up",
            "version": app.version,
            "environment": settings.environment,
            "services": service_statuses,
        }

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
    async def proxy_route(request: Request, full_path: str):
        path = f"/{full_path}"
        target_base = _resolve_target_service(path, settings)
        if not target_base:
            raise HTTPException(status_code=404, detail=f"No microservice registered for path: {path}")

        target_url = f"{target_base}{path}"
        if request.url.query:
            target_url = f"{target_url}?{request.url.query}"

        client: httpx.AsyncClient = app.state.client
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS}

        try:
            upstream_resp = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=502, detail=f"Upstream service unreachable for {path}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"Upstream service timed out for {path}")

        response_headers = {k: v for k, v in upstream_resp.headers.items() if k.lower() not in HOP_BY_HOP_HEADERS}
        return Response(
            content=upstream_resp.content,
            status_code=upstream_resp.status_code,
            headers=response_headers,
            media_type=upstream_resp.headers.get("content-type"),
        )

    return app


app = create_gateway_app()
