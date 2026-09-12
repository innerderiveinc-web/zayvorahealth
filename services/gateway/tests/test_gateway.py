from app.core.config import Settings
from app.main import HOP_BY_HOP_HEADERS, _resolve_target_service, create_gateway_app
from fastapi.testclient import TestClient


def test_resolve_target_service():
    settings = Settings(
        identity_service_url="http://identity:8001",
        clinical_service_url="http://clinical:8002",
        knowledge_service_url="http://knowledge:8003",
        therapeutic_service_url="http://therapeutic:8004",
        ai_service_url="http://ai:8005",
    )

    assert _resolve_target_service("/.well-known/jwks.json", settings) == "http://identity:8001"
    assert _resolve_target_service("/api/v1/auth/login", settings) == "http://identity:8001"
    assert _resolve_target_service("/api/v1/organizations", settings) == "http://identity:8001"
    assert _resolve_target_service("/api/v1/roles", settings) == "http://identity:8001"

    assert _resolve_target_service("/api/v1/patients", settings) == "http://clinical:8002"
    assert _resolve_target_service("/api/v1/encounters/123", settings) == "http://clinical:8002"
    assert _resolve_target_service("/api/v1/clinical-notes", settings) == "http://clinical:8002"
    assert _resolve_target_service("/api/v1/prescriptions", settings) == "http://clinical:8002"
    assert _resolve_target_service("/api/v1/appointments", settings) == "http://clinical:8002"

    assert _resolve_target_service("/api/v1/taxonomy/organ-axes", settings) == "http://knowledge:8003"
    assert _resolve_target_service("/api/v1/mufradat", settings) == "http://knowledge:8003"
    assert _resolve_target_service("/api/v1/pharmacopoeia/schedule-e1", settings) == "http://knowledge:8003"
    assert _resolve_target_service("/api/v1/evidence/mufrad-123", settings) == "http://knowledge:8003"

    assert _resolve_target_service("/api/v1/nuskha-drafts", settings) == "http://therapeutic:8004"
    assert _resolve_target_service("/api/v1/tadbeer-plans", settings) == "http://therapeutic:8004"
    assert _resolve_target_service("/api/v1/ghiza-plans", settings) == "http://therapeutic:8004"

    assert _resolve_target_service("/api/v1/hakeem/consult", settings) == "http://ai:8005"
    assert _resolve_target_service("/api/v1/unknown-service", settings) is None


def test_unregistered_path_returns_404():
    app = create_gateway_app()
    with TestClient(app) as client:
        resp = client.get("/api/v1/unregistered/path")
        assert resp.status_code == 404
        assert "No microservice registered" in resp.json()["detail"]


def test_hop_by_hop_headers_defined():
    assert "connection" in HOP_BY_HOP_HEADERS
    assert "transfer-encoding" in HOP_BY_HOP_HEADERS
    assert "host" in HOP_BY_HOP_HEADERS
