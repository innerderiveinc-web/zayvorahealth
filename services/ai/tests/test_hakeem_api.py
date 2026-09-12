def test_consult_requires_auth(client, sample_patient_id):
    resp = client.post("/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"})
    assert resp.status_code == 401


def test_consult_requires_permission(client, org_id, sample_patient_id):
    from tests.conftest import make_token

    token = make_token(organization_id=org_id, permissions=[])
    resp = client.post(
        "/api/v1/hakeem/consult",
        json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_consult_stores_and_returns_a_valid_consultation(client, auth_headers, sample_patient_id):
    resp = client.post(
        "/api/v1/hakeem/consult",
        json={"patient_id": sample_patient_id, "chief_complaint": "chronic fatigue", "organ_axis": "meda-amaa"},
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["is_valid"] is True
    assert body["missing_sections"] == []
    assert "CLINICAL SUMMARY" in body["raw_response"]
    assert body["reviewed_by_clinician"] is False
    assert body["candidate_mufradat"] == [{"name": "Sonf"}, {"name": "Asrul"}]


def test_consult_for_unknown_patient_404s(client, auth_headers):
    import uuid

    resp = client.post(
        "/api/v1/hakeem/consult",
        json={"patient_id": str(uuid.uuid4()), "chief_complaint": "fatigue"},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_get_consultation_by_id(client, auth_headers, sample_patient_id):
    created = client.post(
        "/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"}, headers=auth_headers
    ).json()
    resp = client.get(f"/api/v1/hakeem/consultations/{created['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_consultation_not_visible_across_organizations(client, auth_headers, sample_patient_id):
    from tests.conftest import make_token

    created = client.post(
        "/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"}, headers=auth_headers
    ).json()
    other_headers = {"Authorization": f"Bearer {make_token()}"}
    resp = client.get(f"/api/v1/hakeem/consultations/{created['id']}", headers=other_headers)
    assert resp.status_code == 404


def test_mark_reviewed_records_clinician_review_and_optional_nuskha_link(client, auth_headers, sample_patient_id):
    created = client.post(
        "/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"}, headers=auth_headers
    ).json()
    resp = client.post(
        f"/api/v1/hakeem/consultations/{created['id']}/mark-reviewed",
        json={"converted_to_nuskha_draft_id": "some-nuskha-draft-id"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["reviewed_by_clinician"] is True
    assert resp.json()["converted_to_nuskha_draft_id"] == "some-nuskha-draft-id"


def test_list_consultations_for_patient(client, auth_headers, sample_patient_id):
    client.post("/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "fatigue"}, headers=auth_headers)
    client.post("/api/v1/hakeem/consult", json={"patient_id": sample_patient_id, "chief_complaint": "joint pain"}, headers=auth_headers)

    resp = client.get(f"/api/v1/hakeem/consultations/by-patient/{sample_patient_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2
