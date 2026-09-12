from tests.conftest import seed_org_role_permission


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_signup_creates_user_and_returns_token(client, db_session):
    seed_org_role_permission(db_session)
    resp = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["user"]["email"] == "doc@clinic-1.com"
    assert body["roles"] == ["Doctor"]
    assert "patient.create" in body["permissions"]
    assert body["access_token"]


def test_signup_rejects_short_password(client, db_session):
    seed_org_role_permission(db_session)
    resp = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "short",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    assert resp.status_code == 422


def test_signup_rejects_unknown_organization(client):
    resp = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@nowhere.com",
            "full_name": "Dr Nobody",
            "password": "SuperSecurePass123!",
            "organization_slug": "does-not-exist",
            "role_name": "Doctor",
        },
    )
    assert resp.status_code == 404


def test_signup_rejects_duplicate_email(client, db_session):
    seed_org_role_permission(db_session)
    payload = {
        "email": "doc@clinic-1.com",
        "full_name": "Dr One",
        "password": "SuperSecurePass123!",
        "organization_slug": "clinic-1",
        "role_name": "Doctor",
    }
    first = client.post("/api/v1/auth/signup", json=payload)
    assert first.status_code == 201
    second = client.post("/api/v1/auth/signup", json=payload)
    assert second.status_code == 409


def test_login_succeeds_with_correct_credentials(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "doc@clinic-1.com", "password": "SuperSecurePass123!", "organization_slug": "clinic-1"},
    )
    assert resp.status_code == 200
    assert resp.json()["roles"] == ["Doctor"]


def test_login_fails_with_wrong_password(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "doc@clinic-1.com", "password": "wrong-password", "organization_slug": "clinic-1"},
    )
    assert resp.status_code == 401


def test_login_failure_does_not_distinguish_unknown_user_from_wrong_password(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    unknown = client.post(
        "/api/v1/auth/login",
        json={"email": "ghost@clinic-1.com", "password": "whatever123", "organization_slug": "clinic-1"},
    )
    wrong_pw = client.post(
        "/api/v1/auth/login",
        json={"email": "doc@clinic-1.com", "password": "wrong-password", "organization_slug": "clinic-1"},
    )
    assert unknown.status_code == wrong_pw.status_code == 401
    assert unknown.json() == wrong_pw.json()


def test_repeated_failed_logins_are_rate_limited(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    last_status = None
    for _ in range(10):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "doc@clinic-1.com", "password": "wrong-password", "organization_slug": "clinic-1"},
        )
        last_status = resp.status_code
    assert last_status == 429


def test_session_endpoint_requires_bearer_token(client):
    resp = client.get("/api/v1/auth/session")
    assert resp.status_code == 401


def test_session_endpoint_works_with_valid_token(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "doc@clinic-1.com",
            "full_name": "Dr One",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "doc@clinic-1.com", "password": "SuperSecurePass123!", "organization_slug": "clinic-1"},
    )
    token = login_resp.json()["access_token"]
    resp = client.get("/api/v1/auth/session", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["roles"] == ["Doctor"]


def test_session_endpoint_rejects_garbage_token(client):
    resp = client.get("/api/v1/auth/session", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_jwks_endpoint_returns_valid_keys(client):
    for path in ["/.well-known/jwks.json", "/api/v1/auth/jwks.json"]:
        resp = client.get(path)
        assert resp.status_code == 200
        data = resp.json()
        assert "keys" in data
        assert len(data["keys"]) > 0
        key = data["keys"][0]
        assert "kty" in key
        assert "alg" in key


def test_logout_revokes_bearer_token(client, db_session):
    seed_org_role_permission(db_session)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "logout-test@clinic-1.com",
            "full_name": "Dr Logout",
            "password": "SuperSecurePass123!",
            "organization_slug": "clinic-1",
            "role_name": "Doctor",
        },
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "logout-test@clinic-1.com", "password": "SuperSecurePass123!", "organization_slug": "clinic-1"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Active token succeeds
    resp1 = client.get("/api/v1/auth/session", headers={"Authorization": f"Bearer {token}"})
    assert resp1.status_code == 200

    # Logout
    logout_resp = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_resp.status_code == 200
    assert logout_resp.json()["message"] == "Logged out successfully"

    # Subsequent use of revoked token fails
    resp2 = client.get("/api/v1/auth/session", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 401
    assert "revoked" in resp2.json()["detail"].lower()

