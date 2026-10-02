from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.clients.clinical_client import ClinicalClient
from app.clients.knowledge_client import KnowledgeClient
from app.core.config import Settings, get_settings
from app.core.database import init_db
from app.providers.base import AIProvider
from app.routers import hakeem, evaluation, security, multimodal, agentic


def create_app(
    settings: Settings | None = None,
    clinical_client: ClinicalClient | None = None,
    knowledge_client: KnowledgeClient | None = None,
    ai_provider: AIProvider | None = None,
) -> FastAPI:
    settings = settings or get_settings()
    settings.validate_runtime()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not settings.is_production:
            init_db()

        app.state.clinical_client = clinical_client
        if app.state.clinical_client is None:
            from app.clients.clinical_client import HttpClinicalClient

            app.state.clinical_client = HttpClinicalClient(settings.clinical_service_url)

        app.state.knowledge_client = knowledge_client
        if app.state.knowledge_client is None:
            from app.clients.knowledge_client import HttpKnowledgeClient

            app.state.knowledge_client = HttpKnowledgeClient(settings.knowledge_service_url)

        app.state.ai_provider = ai_provider
        if app.state.ai_provider is None:
            import os

            from app.providers.anthropic_provider import AnthropicProvider
            from app.providers.deterministic_fallback_provider import DeterministicSafeFallbackProvider
            from app.providers.fallback_router import ChainedFallbackRouter
            from app.providers.local_vllm_provider import LocalVLLMProvider
            from app.providers.openai_provider import OpenAIProvider

            safe_fallback = DeterministicSafeFallbackProvider()

            chain = []
            if settings.anthropic_api_key:
                chain.append(AnthropicProvider(api_key=settings.anthropic_api_key, model=settings.anthropic_model))

            openai_key = os.environ.get("OPENAI_API_KEY", "")
            if openai_key:
                chain.append(OpenAIProvider(api_key=openai_key))

            local_vllm_url = os.environ.get("LOCAL_VLLM_URL", "")
            if local_vllm_url:
                chain.append(LocalVLLMProvider(base_url=local_vllm_url))

            if len(chain) > 0:
                app.state.ai_provider = ChainedFallbackRouter(providers=chain, deterministic_fallback=safe_fallback)
            else:
                # Fall back gracefully to deterministic rule-based posology engine
                app.state.ai_provider = safe_fallback


        yield

    app = FastAPI(
        title="ZAYVORA AI Service",
        version="0.1.0-phase4",
        description="Hakeem Sahab clinical copilot — orchestrates services/clinical + "
        "services/knowledge context, calls a model-agnostic AI provider, and structurally "
        "validates the response before storing it as an AI Governance audit record (ZAYVORA Clinical Architecture Specification v4.0 Phase 4).",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(hakeem.router)
    app.include_router(evaluation.router)
    app.include_router(security.router)
    app.include_router(multimodal.router)
    app.include_router(agentic.router)

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "ai", "version": app.version, "environment": settings.environment}

    return app


app = create_app()
