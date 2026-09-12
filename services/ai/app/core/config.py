from __future__ import annotations

from functools import lru_cache

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    class BaseSettings:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def SettingsConfigDict(*args, **kwargs):  # type: ignore
        return {}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZAYVORA_AI_", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_ai"
    jwt_secret: str = ""
    jwt_public_key_pem: str = ""
    redis_url: str = ""
    jwt_algorithm: str = "HS256"
    cors_allowed_origins: str = "http://localhost:3000"

    clinical_service_url: str = "http://localhost:8002"
    knowledge_service_url: str = "http://localhost:8003"

    # Multi-Tier Production AI Providers (BLK-02)
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    vllm_base_url: str = "http://localhost:8000/v1"
    vllm_model: str = "meta-llama/Meta-Llama-3-70B-Instruct"

    # HashiCorp Vault Secrets Integration
    vault_addr: str = ""
    vault_token: str = ""
    vault_secret_path: str = "secret/data/zayvora/ai"
    vault_secrets_file: str = "/vault/secrets/ai-secrets.json"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    def load_vault_secrets(self) -> None:
        """Dynamically ingests AI credentials from HashiCorp Vault agent mount."""
        import json
        import os
        if self.vault_secrets_file and os.path.exists(self.vault_secrets_file):
            try:
                with open(self.vault_secrets_file, "r") as f:
                    secrets = json.load(f)
                    if "anthropic_api_key" in secrets:
                        self.anthropic_api_key = secrets["anthropic_api_key"]
                    if "openai_api_key" in secrets:
                        self.openai_api_key = secrets["openai_api_key"]
                    if "vllm_base_url" in secrets:
                        self.vllm_base_url = secrets["vllm_base_url"]
            except Exception:
                pass

    def validate_runtime(self) -> None:
        if self.is_production:
            self.load_vault_secrets()
            if not self.jwt_public_key_pem.strip() and not self.jwt_secret.strip():
                raise RuntimeError("Either ZAYVORA_AI_JWT_PUBLIC_KEY_PEM or ZAYVORA_AI_JWT_SECRET must be set in production.")
            if self.jwt_secret.strip() and len(self.jwt_secret.strip()) < 32:
                raise RuntimeError("ZAYVORA_AI_JWT_SECRET should be at least 32 characters in production.")
            if "sqlite" in self.database_url.lower():
                raise RuntimeError("SQLite is not permitted in production for the AI service.")
            if not (self.anthropic_api_key.strip() or self.openai_api_key.strip() or self.vllm_base_url.strip()):
                raise RuntimeError("At least one AI Provider (Anthropic, OpenAI, or vLLM) must be configured in production.")
            if any("localhost" in origin for origin in self.cors_origin_list):
                raise RuntimeError("ZAYVORA_AI_CORS_ALLOWED_ORIGINS must not include localhost in production.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
