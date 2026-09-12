from app.core.config import Settings
from app.main import HOP_BY_HOP_HEADERS, _resolve_target_service, create_gateway_app
try:
    from fastapi.testclient import TestClient
except ImportError:
    TestClient = None


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
    if TestClient is None:
        settings = Settings()
        assert _resolve_target_service("/api/v1/unregistered/path", settings) is None
        return

    app = create_gateway_app()
    with TestClient(app) as client:
        resp = client.get("/api/v1/unregistered/path")
        assert resp.status_code == 404
        assert "No microservice registered" in resp.json()["detail"]


def test_hop_by_hop_headers_defined():
    assert "connection" in HOP_BY_HOP_HEADERS
    assert "transfer-encoding" in HOP_BY_HOP_HEADERS
    assert "host" in HOP_BY_HOP_HEADERS


def test_rate_limiter_token_bucket_behavior():
    from app.middleware.rate_limiter import TokenBucketRateLimiter

    class DummyRequest:
        def __init__(self, headers=None, client_ip="127.0.0.1"):
            self.headers = headers or {}
            self.client = type("Client", (), {"host": client_ip})()

    limiter = TokenBucketRateLimiter(unauthenticated_limit=3, authenticated_limit=5, window_seconds=60)
    unauth_req = DummyRequest()

    # 3 allowed requests
    for i in range(3):
        allowed, hdrs = limiter.check(unauth_req)
        assert allowed is True
        assert hdrs["X-RateLimit-Limit"] == "3"

    # 4th request must be blocked with HTTP 429 semantics
    blocked, hdrs = limiter.check(unauth_req)
    assert blocked is False
    assert "Retry-After" in hdrs

    # Authenticated client has separate limit of 5
    auth_req = DummyRequest(headers={"Authorization": "Bearer token-12345"})
    for i in range(5):
        allowed, hdrs = limiter.check(auth_req)
        assert allowed is True
        assert hdrs["X-RateLimit-Limit"] == "5"

    blocked_auth, hdrs = limiter.check(auth_req)
    assert blocked_auth is False

