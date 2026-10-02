from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.routers import (
    appointments,
    clinical_notes,
    cron,
    digital_twin,
    dr,
    encounters,
    governance,
    interop,
    mizaj,
    patient_portal,
    patients,
    payments,
    predictive,
    prescriptions,
    qsura,
    research,
    scribe,
    tasks,
    timeline,
    wearables,
    afaal,
    continuum,
)
from app.observability.telemetry import GLOBAL_TELEMETRY
from fastapi.responses import PlainTextResponse






def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    settings.validate_runtime()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not settings.is_production:
            init_db()
        yield

    app = FastAPI(
        title="ZAYVORA Clinical Service",
        version="0.1.0-phase1",
        description="Patient 360, encounters, versioned clinical notes, prescriptions, "
        "appointments, and the aggregated clinical timeline (ZAYVORA Clinical Architecture Specification v4.0 Phase 1).",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(patients.router)
    app.include_router(encounters.router)
    app.include_router(clinical_notes.router)
    app.include_router(prescriptions.router)
    app.include_router(appointments.router)
    app.include_router(timeline.router)
    app.include_router(mizaj.router)
    app.include_router(digital_twin.router)
    app.include_router(interop.router)
    app.include_router(qsura.router)
    app.include_router(research.router)
    app.include_router(scribe.router)
    app.include_router(governance.router)
    app.include_router(wearables.router)
    app.include_router(predictive.router)
    app.include_router(patient_portal.router)
    app.include_router(dr.router)
    app.include_router(tasks.router)
    app.include_router(payments.router)
    app.include_router(cron.router)
    app.include_router(afaal.router)
    app.include_router(continuum.router)

    @app.get("/metrics", response_class=PlainTextResponse)
    def prometheus_metrics():
        return GLOBAL_TELEMETRY.export_prometheus_metrics()





    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "clinical", "version": app.version, "environment": settings.environment}

    return app


app = create_app()
