"""Shared pytest fixtures for the gateway service test suite."""
import pytest


@pytest.fixture
def settings():
    """Return a gateway Settings object pointing at test URLs."""
    from app.core.config import Settings
    return Settings(
        identity_service_url="http://identity-test:8001",
        clinical_service_url="http://clinical-test:8002",
        knowledge_service_url="http://knowledge-test:8003",
        therapeutic_service_url="http://therapeutic-test:8004",
        ai_service_url="http://ai-test:8005",
    )
