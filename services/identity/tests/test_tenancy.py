from tests.conftest import seed_org_role_permission


def test_create_organization_succeeds(client):
    resp = client.post("/api/v1/organizations", json={"name": "New Clinic", "slug": "new-clinic", "tier": "clinic"})
    assert resp.status_code == 201
    assert resp.json()["slug"] == "new-clinic"


def test_create_organization_rejects_duplicate_slug(client):
    client.post("/api/v1/organizations", json={"name": "New Clinic", "slug": "new-clinic", "tier": "clinic"})
    resp = client.post("/api/v1/organizations", json={"name": "Another Clinic", "slug": "new-clinic", "tier": "clinic"})
    assert resp.status_code == 409


def test_create_organization_rejects_invalid_slug(client):
    resp = client.post("/api/v1/organizations", json={"name": "Bad Slug Clinic", "slug": "Not A Valid Slug!", "tier": "clinic"})
    assert resp.status_code == 422


def test_get_organization_by_slug(client):
    client.post("/api/v1/organizations", json={"name": "New Clinic", "slug": "new-clinic", "tier": "clinic"})
    resp = client.get("/api/v1/organizations/new-clinic")
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Clinic"


def test_get_unknown_organization_404s(client):
    resp = client.get("/api/v1/organizations/does-not-exist")
    assert resp.status_code == 404


def test_new_organization_auto_provisions_owner_role_for_first_signup(client):
    """Regression guard for the bootstrap chicken-and-egg problem: a brand
    new clinic must be able to sign its first user up as 'Owner' without
    anyone already being logged in to create that role first."""
    client.post("/api/v1/organizations", json={"name": "Bootstrap Clinic", "slug": "bootstrap-clinic", "tier": "clinic"})
    resp = client.post(
        "/api/v1/auth/signup",
        json={
            "email": "owner@bootstrap-clinic.com",
            "full_name": "Founding Owner",
            "password": "SuperSecurePass123!",
            "organization_slug": "bootstrap-clinic",
            "role_name": "Owner",
        },
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["roles"] == ["Owner"]
    assert "role.manage" in body["permissions"]
    assert "patient.create" in body["permissions"]


def _login(client, db_session, *, permission_codes=("role.manage",)):
    org, role = seed_org_role_permission(db_session, permission_codes=permission_codes)
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": "admin@clinic-1.com",
            "full_name": "Admin One",
            "password": "SuperSecurePass123!",
            "organization_slug": org.slug,
            "role_name": role.name,
        },
    )
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@clinic-1.com", "password": "SuperSecurePass123!", "organization_slug": org.slug},
    )
    token = login_resp.json()["access_token"]
    return org, token


def test_create_role_requires_authentication(client):
    resp = client.post(
        "/api/v1/roles",
        json={"organization_slug": "clinic-1", "name": "Nurse", "permission_codes": []},
    )
    assert resp.status_code == 401


def test_create_role_requires_role_manage_permission(client, db_session):
    # Logged in, but the seeded role only has 'patient.create', not 'role.manage'.
    org, token = _login(client, db_session, permission_codes=("patient.create",))
    resp = client.post(
        "/api/v1/roles",
        json={"organization_slug": org.slug, "name": "Nurse", "permission_codes": []},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_create_role_succeeds_with_role_manage_permission(client, db_session):
    from app.models.identity import Permission

    org, token = _login(client, db_session, permission_codes=("role.manage",))
    db_session.add(Permission(code="nuskha.approve", description="Approve a Nuskha"))
    db_session.commit()

    resp = client.post(
        "/api/v1/roles",
        json={"organization_slug": org.slug, "name": "Senior Hakeem", "permission_codes": ["nuskha.approve"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["permission_codes"] == ["nuskha.approve"]


def test_create_role_rejects_unknown_permission_code(client, db_session):
    org, token = _login(client, db_session, permission_codes=("role.manage",))
    resp = client.post(
        "/api/v1/roles",
        json={"organization_slug": org.slug, "name": "Ghost Role", "permission_codes": ["does.not.exist"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


def test_create_organization_with_bootstrap_token_enforcement(client, monkeypatch):
    import app.core.config as cfg

    monkeypatch.setattr(cfg.get_settings(), "bootstrap_token", "secret-bootstrap-token-123")

    # Missing token -> 403
    resp = client.post(
        "/api/v1/organizations",
        json={"name": "Token Clinic", "slug": "token-clinic", "tier": "clinic"},
    )
    assert resp.status_code == 403
    assert "X-Bootstrap-Token" in resp.json()["detail"]

    # Wrong token -> 403
    resp = client.post(
        "/api/v1/organizations",
        json={"name": "Token Clinic", "slug": "token-clinic", "tier": "clinic"},
        headers={"X-Bootstrap-Token": "wrong-token"},
    )
    assert resp.status_code == 403

    # Valid token -> 201
    resp = client.post(
        "/api/v1/organizations",
        json={"name": "Token Clinic", "slug": "token-clinic", "tier": "clinic"},
        headers={"X-Bootstrap-Token": "secret-bootstrap-token-123"},
    )
    assert resp.status_code == 201
    assert resp.json()["slug"] == "token-clinic"

