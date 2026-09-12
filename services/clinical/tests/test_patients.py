def _patient_payload(**overrides):
    payload = {
        "mrn": "MRN-0001",
        "full_name": "Ayesha Test Patient",
        "date_of_birth": "1990-05-14",
        "sex": "female",
        "contact_phone": "9999999999",
        "allergies": ["penicillin"],
        "current_medications": ["Warfarin"],
        "consent_given": True,
    }
    payload.update(overrides)
    return payload


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200


def test_create_patient_requires_auth(client):
    resp = client.post("/api/v1/patients", json=_patient_payload())
    assert resp.status_code == 401


def test_create_patient_requires_permission(client, org_id):
    from tests.conftest import make_token

    token = make_token(organization_id=org_id, permissions=["patient.read"])  # no patient.create
    resp = client.post("/api/v1/patients", json=_patient_payload(), headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_create_and_get_patient(client, auth_headers):
    resp = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers)
    assert resp.status_code == 201, resp.text
    patient = resp.json()
    assert patient["full_name"] == "Ayesha Test Patient"
    assert patient["allergies"] == ["penicillin"]

    get_resp = client.get(f"/api/v1/patients/{patient['id']}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["mrn"] == "MRN-0001"


def test_duplicate_mrn_within_org_rejected(client, auth_headers):
    client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers)
    resp = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers)
    assert resp.status_code == 409


def test_same_mrn_allowed_across_different_organizations(client, auth_headers, other_org_headers):
    first = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers)
    second = client.post("/api/v1/patients", json=_patient_payload(), headers=other_org_headers)
    assert first.status_code == 201
    assert second.status_code == 201


def test_patient_not_visible_across_organizations(client, auth_headers, other_org_headers):
    created = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers).json()
    resp = client.get(f"/api/v1/patients/{created['id']}", headers=other_org_headers)
    assert resp.status_code == 404


def test_patient_list_scoped_to_organization(client, auth_headers, other_org_headers):
    client.post("/api/v1/patients", json=_patient_payload(mrn="A1"), headers=auth_headers)
    client.post("/api/v1/patients", json=_patient_payload(mrn="B1"), headers=other_org_headers)

    mine = client.get("/api/v1/patients", headers=auth_headers).json()
    theirs = client.get("/api/v1/patients", headers=other_org_headers).json()
    assert [p["mrn"] for p in mine] == ["A1"]
    assert [p["mrn"] for p in theirs] == ["B1"]


def test_update_patient(client, auth_headers):
    created = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers).json()
    resp = client.patch(
        f"/api/v1/patients/{created['id']}",
        json={"contact_phone": "8888888888", "allergies": ["penicillin", "sulfa"]},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["contact_phone"] == "8888888888"
    assert resp.json()["allergies"] == ["penicillin", "sulfa"]
    # Untouched fields survive a partial update.
    assert resp.json()["mrn"] == "MRN-0001"


def test_create_patient_rejects_invalid_sex(client, auth_headers):
    resp = client.post("/api/v1/patients", json=_patient_payload(sex="unknown-value"), headers=auth_headers)
    assert resp.status_code == 422


def test_create_patient_rejects_missing_mrn(client, auth_headers):
    payload = _patient_payload()
    del payload["mrn"]
    resp = client.post("/api/v1/patients", json=payload, headers=auth_headers)
    assert resp.status_code == 422


def test_create_patient_with_pregnancy_and_comorbidities(client, auth_headers):
    payload = _patient_payload(
        pregnancy_status="pregnant",
        comorbidities=["type-2-diabetes", "hypertension"],
    )
    resp = client.post("/api/v1/patients", json=payload, headers=auth_headers)
    assert resp.status_code == 201, resp.text
    patient = resp.json()
    assert patient["pregnancy_status"] == "pregnant"
    assert patient["comorbidities"] == ["type-2-diabetes", "hypertension"]


def test_update_pregnancy_status_and_comorbidities(client, auth_headers):
    created = client.post("/api/v1/patients", json=_patient_payload(), headers=auth_headers).json()
    assert created["pregnancy_status"] == "not_applicable"
    assert created["comorbidities"] == []

    resp = client.patch(
        f"/api/v1/patients/{created['id']}",
        json={"pregnancy_status": "pregnant", "comorbidities": ["chronic-kidney-disease"]},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["pregnancy_status"] == "pregnant"
    assert updated["comorbidities"] == ["chronic-kidney-disease"]


def test_reject_invalid_pregnancy_status(client, auth_headers):
    resp = client.post("/api/v1/patients", json=_patient_payload(pregnancy_status="invalid_status"), headers=auth_headers)
    assert resp.status_code == 422

