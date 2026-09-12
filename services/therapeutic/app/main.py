from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.routers import care_plans, dispensary, ghiza, logistics, nuskha, tadbeer



def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    settings.validate_runtime()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not settings.is_production:
            init_db()
        yield

    app = FastAPI(
        title="ZAYVORA Therapeutic Service",
        version="0.1.0-phase3",
        description="Nuskha Nawisi (with Safety Firewall gate + Clinical Authority "
        "Guardrail), Ilaj bil-Tadbeer, and Ilaj bil-Ghiza — Master Build Prompt v4.0 Phase 3.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(nuskha.router)
    app.include_router(tadbeer.router)
    app.include_router(ghiza.router)
    app.include_router(care_plans.router)
    app.include_router(dispensary.router)
    app.include_router(logistics.router)


    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "therapeutic", "version": app.version, "environment": settings.environment}

    return app


app = create_app()
