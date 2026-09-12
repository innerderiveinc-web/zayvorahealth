"""
Identity service settings. Deliberately mirrors the production-guardrail
philosophy already proven out in the v8.0 codebase's backend/config.py
(AppSettings.validate_runtime) — a misconfigured production deploy should
fail loudly at startup, not silently serve traffic insecurely.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZAYVORA_IDENTITY_", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://zayvora:zayvora@localhost:5432/zayvora_identity"
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 60 * 60 * 8  # 8 hours
    min_password_length: int = 12
    login_rate_limit_attempts: int = 6
    login_rate_limit_window_seconds: int = 300
    cors_allowed_origins: str = "http://localhost:3000"
    bootstrap_token: str = ""
    redis_url: str = ""
    jwt_private_key_pem: str = ""
    jwt_public_key_pem: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    def validate_runtime(self) -> None:
        if self.is_production:
            if not self.jwt_private_key_pem.strip() and not self.jwt_secret.strip():
                raise RuntimeError("Either ZAYVORA_IDENTITY_JWT_PRIVATE_KEY_PEM (RS256) or ZAYVORA_IDENTITY_JWT_SECRET (HS256) must be set in production.")
            if self.jwt_secret.strip() and len(self.jwt_secret.strip()) < 32:
                raise RuntimeError("ZAYVORA_IDENTITY_JWT_SECRET should be at least 32 characters in production.")
            if not self.bootstrap_token.strip():
                raise RuntimeError("ZAYVORA_IDENTITY_BOOTSTRAP_TOKEN must be set in production.")
        if self.is_production and "sqlite" in self.database_url.lower():
            raise RuntimeError("SQLite is not permitted in production for the identity service.")
        if self.is_production and any("localhost" in origin for origin in self.cors_origin_list):
            raise RuntimeError("ZAYVORA_IDENTITY_CORS_ALLOWED_ORIGINS must not include localhost in production.")
        if self.min_password_length < 8:
            raise RuntimeError("ZAYVORA_IDENTITY_MIN_PASSWORD_LENGTH must be at least 8.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
