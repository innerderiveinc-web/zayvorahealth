"""
ZAYVORA Identity Service – application factory.

Phase 2 additions:
- SecurityHeadersMiddleware: injects OWASP-recommended HTTP response headers.
- LoginLockoutManager: tracks failed login attempts per identifier and locks
  out callers after a configurable number of consecutive failures (default 5).
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.core.rate_limit import LoginLockoutManager, RateLimiter
from app.core.security_headers import SecurityHeadersMiddleware
from app.routers import auth, tenancy


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct and configure the FastAPI application.

    Args:
        settings: Optional pre-built ``Settings`` instance (useful in tests
                  to inject overrides without touching the LRU-cached singleton).

    Returns:
        A fully configured ``FastAPI`` application ready to be served by uvicorn.
    """
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
        version="0.1.0-phase2",
        description=(
            "Auth, tenancy (organizations), RBAC (roles/permissions), and audit logging. "
            "Foundation service every other ZAYVORA service depends on for tenant isolation. "
            "Phase 2: refresh tokens, security headers, lockout, MFA scaffolding."
        ),
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # Middleware – order matters: outermost middleware runs first on request
    # and last on response.
    # ------------------------------------------------------------------

    # Phase-2: inject OWASP security headers on every response
    app.add_middleware(SecurityHeadersMiddleware)

    # CORS must sit inside SecurityHeadersMiddleware so the security headers
    # are always present, even on pre-flight OPTIONS responses.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # App state – shared objects available to route handlers via request.app.state
    # ------------------------------------------------------------------

    # Sliding-window rate limiter (IP-based + per-user)
    app.state.rate_limiter = RateLimiter(redis_url=settings.redis_url or None)

    # Phase-2: lockout manager – 5 failures → 15-minute lockout
    app.state.lockout_manager = LoginLockoutManager(
        redis_url=settings.redis_url or None,
        max_attempts=5,
        lockout_seconds=900,  # 15 minutes
    )

    # ------------------------------------------------------------------
    # Routers
    # ------------------------------------------------------------------
    app.include_router(auth.router)
    app.include_router(tenancy.router)

    # ------------------------------------------------------------------
    # Well-known & health endpoints
    # ------------------------------------------------------------------

    @app.get("/.well-known/jwks.json", include_in_schema=False)
    def root_jwks():
        from app.core.security import get_jwks

        return get_jwks()

    @app.get("/api/health")
    def health():
        return {
            "ok": True,
            "service": "identity",
            "version": app.version,
            "environment": settings.environment,
        }

    return app


app = create_app()

