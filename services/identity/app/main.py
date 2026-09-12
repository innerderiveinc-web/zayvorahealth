from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.core.rate_limit import RateLimiter
from app.routers import auth, tenancy


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    settings.validate_runtime()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not settings.is_production:
            # Dev/test convenience only — production schema changes must
            # go through database/migrations/ (Alembic), never auto-create.
            init_db()
        yield

    app = FastAPI(
        title="ZAYVORA Identity Service",
        version="0.1.0-phase0",
        description="Auth, tenancy (organizations), RBAC (roles/permissions), and audit logging. "
        "Foundation service every other ZAYVORA service depends on for tenant isolation.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.rate_limiter = RateLimiter(redis_url=settings.redis_url)
    app.include_router(auth.router)
    app.include_router(tenancy.router)

    @app.get("/.well-known/jwks.json")
    def root_jwks():
        from app.core.security import get_jwks

        return get_jwks()

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "identity", "version": app.version, "environment": settings.environment}

    return app


app = create_app()
