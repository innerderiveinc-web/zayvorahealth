def _create_mufrad(client, headers, name="Asrul"):
    return client.post(
        "/api/v1/mufradat", json={"name": name, "afal": ["Muqawwi-e-Meda"]}, headers=headers
    ).json()


def test_add_classical_evidence(client, auth_headers):
    mufrad = _create_mufrad(client, auth_headers)
    resp = client.post(
        f"/api/v1/mufradat/{mufrad['id']}/evidence",
        json={
            "level": "E0",
            "knowledge_world": "A",
            "source": "Al-Qanoon fi al-Tibb",
            "summary": "Classical description of digestive-strengthening action",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    evidence = resp.json()
    assert evidence["level"] == "E0"
    assert evidence["knowledgeWorld"] == "A"
    assert evidence["reviewStatus"] == "pending"


def test_evidence_defaults_to_pending_review_never_auto_approved(client, auth_headers):
    """ZAYVORA Clinical Architecture Specification v4.0 §23: 'Never transform E0 into E3/E4
    automatically.' Verified here as: adding evidence never sets
    review_status to anything but what was explicitly passed (default
    'pending'), regardless of the evidence level given."""
    mufrad = _create_mufrad(client, auth_headers)
    resp = client.post(
        f"/api/v1/mufradat/{mufrad['id']}/evidence",
        json={"level": "E4", "knowledge_world": "B", "source": "Systematic review XYZ"},
        headers=auth_headers,
    )
    assert resp.json()["reviewStatus"] == "pending"


def test_add_evidence_rejects_invalid_level(client, auth_headers):
    mufrad = _create_mufrad(client, auth_headers)
    resp = client.post(
        f"/api/v1/mufradat/{mufrad['id']}/evidence",
        json={"level": "E9", "knowledge_world": "A"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_add_evidence_rejects_invalid_knowledge_world(client, auth_headers):
    mufrad = _create_mufrad(client, auth_headers)
    resp = client.post(
        f"/api/v1/mufradat/{mufrad['id']}/evidence",
        json={"level": "E0", "knowledge_world": "Z"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_add_evidence_to_unknown_mufrad_404s(client, auth_headers):
    resp = client.post(
        "/api/v1/mufradat/does-not-exist/evidence",
        json={"level": "E0", "knowledge_world": "A"},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_list_evidence_ordered_by_level(client, auth_headers):
    mufrad = _create_mufrad(client, auth_headers)
    for level, world in [("E4", "B"), ("E0", "A"), ("E2", "B")]:
        client.post(
            f"/api/v1/mufradat/{mufrad['id']}/evidence",
            json={"level": level, "knowledge_world": world},
            headers=auth_headers,
        )
    resp = client.get(f"/api/v1/mufradat/{mufrad['id']}/evidence", headers=auth_headers)
    assert resp.status_code == 200
    levels = [e["level"] for e in resp.json()]
    assert levels == sorted(levels)  # E0, E2, E4


def test_mufrad_with_no_evidence_can_be_explicitly_flagged_insufficient(client, auth_headers):
    """Not a distinct field yet — but confirms the honest baseline: a
    freshly created Mufrad has zero evidence, not fabricated evidence.
    ZAYVORA Clinical Architecture Specification v4.0 §24: if no reliable source exists, the system
    must say so rather than inventing one."""
    mufrad = _create_mufrad(client, auth_headers)
    resp = client.get(f"/api/v1/mufradat/{mufrad['id']}/evidence", headers=auth_headers)
    assert resp.json() == []


def test_evidence_write_requires_evidence_write_permission(client, org_id):
    from tests.conftest import make_token

    setup_headers = {"Authorization": f"Bearer {make_token(organization_id=org_id, permissions=['pharmacopoeia.write'])}"}
    mufrad = client.post("/api/v1/mufradat", json={"name": "Asrul"}, headers=setup_headers).json()

    limited_headers = {"Authorization": f"Bearer {make_token(organization_id=org_id, permissions=['pharmacopoeia.read'])}"}
    resp = client.post(
        f"/api/v1/mufradat/{mufrad['id']}/evidence",
        json={"level": "E0", "knowledge_world": "A"},
        headers=limited_headers,
    )
    assert resp.status_code == 403
