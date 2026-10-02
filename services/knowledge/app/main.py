from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.graph.repository import GraphRepository
from app.routers import clinical_knowledge, evidence, governance_board, graph, mufradat, ocr, ocr_vision, pharmacopoeia, rag, search, sources, taxonomy, taxonomy_custom, diet, hybrid_rag


def create_app(settings: Settings | None = None, graph_repository: GraphRepository | None = None) -> FastAPI:
    settings = settings or get_settings()
    settings.validate_runtime()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        repo = graph_repository
        if repo is None:
            from app.graph.neo4j_repository import Neo4jGraphRepository

            repo = Neo4jGraphRepository(
                settings.neo4j_uri,
                settings.neo4j_user,
                settings.neo4j_password,
                knowledge_db=settings.neo4j_knowledge_database,
                formula_db=settings.neo4j_formula_database,
                evidence_db=settings.neo4j_evidence_database,
                patient_db=settings.neo4j_patient_database,
            )
            repo.verify_connectivity()
            repo.seed_pharmacopoeia_graph()
        # Seed structured knowledge graph (Phase 5)
        from app.core.graph_seeder import seed_all
        seed_all(repo)
        app.state.graph_repository = repo
        yield
        if hasattr(repo, "close"):
            repo.close()

    app = FastAPI(
        title="ZAYVORA Knowledge Service",
        version="0.1.0-phase2",
        description="Pharmacopoeia (Mufradat monographs), Mizaj/Organ-Axis taxonomy, "
        "and provenance-tracked Evidence — the Knowledge Graph core (ZAYVORA Clinical Architecture Specification v4.0 Phase 2).",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(taxonomy.router)
    app.include_router(mufradat.router)
    app.include_router(pharmacopoeia.router)
    app.include_router(evidence.router)
    app.include_router(evidence.evidence_engine_router)
    app.include_router(graph.router)
    app.include_router(rag.router)
    app.include_router(search.router)
    app.include_router(governance_board.router)
    app.include_router(sources.router)
    app.include_router(ocr.router)
    app.include_router(ocr_vision.router)
    app.include_router(taxonomy_custom.router)
    app.include_router(diet.router)
    app.include_router(clinical_knowledge.router)
    app.include_router(hybrid_rag.router)

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "knowledge", "version": app.version, "environment": settings.environment}

    return app


app = create_app()
