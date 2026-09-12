from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZAYVORA_THERAPEUTIC_", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_therapeutic"
    jwt_secret: str = ""
    jwt_public_key_pem: str = ""
    redis_url: str = ""
    jwt_algorithm: str = "HS256"
    cors_allowed_origins: str = "http://localhost:3000"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    def validate_runtime(self) -> None:
        if self.is_production:
            if not self.jwt_public_key_pem.strip() and not self.jwt_secret.strip():
                raise RuntimeError("Either ZAYVORA_THERAPEUTIC_JWT_PUBLIC_KEY_PEM or ZAYVORA_THERAPEUTIC_JWT_SECRET must be set in production.")
            if self.jwt_secret.strip() and len(self.jwt_secret.strip()) < 32:
                raise RuntimeError("ZAYVORA_THERAPEUTIC_JWT_SECRET should be at least 32 characters in production.")
        if self.is_production and "sqlite" in self.database_url.lower():
            raise RuntimeError("SQLite is not permitted in production for the therapeutic service.")
        if self.is_production and any("localhost" in origin for origin in self.cors_origin_list):
            raise RuntimeError("ZAYVORA_THERAPEUTIC_CORS_ALLOWED_ORIGINS must not include localhost in production.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
