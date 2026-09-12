from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZAYVORA_GATEWAY_", extra="ignore")

    environment: str = "development"
    port: int = 8000
    cors_allowed_origins: str = "http://localhost:3000"

    identity_service_url: str = "http://localhost:8001"
    clinical_service_url: str = "http://localhost:8002"
    knowledge_service_url: str = "http://localhost:8003"
    therapeutic_service_url: str = "http://localhost:8004"
    ai_service_url: str = "http://localhost:8005"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
