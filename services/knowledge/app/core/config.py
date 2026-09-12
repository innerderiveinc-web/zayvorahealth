from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ZAYVORA_KNOWLEDGE_", extra="ignore")

    environment: str = "development"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "zayvora_dev_password"
    neo4j_knowledge_database: str = "zayvora_knowledge"
    neo4j_formula_database: str = "zayvora_formula"
    neo4j_evidence_database: str = "zayvora_evidence"
    neo4j_patient_database: str = "zayvora_patient"
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
        if self.is_production and not self.jwt_public_key_pem.strip() and not self.jwt_secret.strip():
            raise RuntimeError("Either ZAYVORA_KNOWLEDGE_JWT_PUBLIC_KEY_PEM or ZAYVORA_KNOWLEDGE_JWT_SECRET must be set in production.")
        if self.is_production and self.neo4j_password == "zayvora_dev_password":
            raise RuntimeError("ZAYVORA_KNOWLEDGE_NEO4J_PASSWORD must be changed from the dev default in production.")
        if self.is_production and any("localhost" in origin for origin in self.cors_origin_list):
            raise RuntimeError("ZAYVORA_KNOWLEDGE_CORS_ALLOWED_ORIGINS must not include localhost in production.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
