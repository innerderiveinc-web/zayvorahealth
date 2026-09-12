import uuid

from tests.conftest import make_token


def _safe_payload(**overrides):
    payload = {
        "patient_id": str(uuid.uuid4()),
        "encounter_id": str(uuid.uuid4()),
        "patient_safety_context": {
            "age": 35,
            "pregnancy_status": "not_applicable",
            "lactation_status": "no",
            "allergies": [],
            "current_medications": [],
            "comorbidities": [],
            "chief_complaint": "mild fatigue",
        },
        "tashkhis": "Suspected Balghami imbalance",
        "usool_e_ilaj": "Strengthen digestive fire",
        "therapeutic_objective": "Improve energy and digestion",
        "ingredients": [{"name": "Sonf", "afal": "Muqawwi-e-Meda", "miqdaar": "3g"}],
        "dosage_form": "Powder",
        "dose": "3g twice daily",
    }
    payload.update(overrides)
    return payload


def _pregnant_payload(**overrides):
    payload = _safe_payload()
    payload["patient_safety_context"]["pregnancy_status"] = "pregnant"
    payload.update(overrides)
    return payload


def test_create_draft_requires_auth(client):
    resp = client.post("/api/v1/nuskha-drafts", json=_safe_payload())
    assert resp.status_code == 401


def test_create_draft_requires_permission(client, org_id):
    token = make_token(organization_id=org_id, permissions=["nuskha.read"])  # no nuskha.create
    resp = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_create_draft_always_starts_as_draft_status(client, auth_headers):
    resp = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers)
    assert resp.status_code == 201, resp.text
    draft = resp.json()
    assert draft["status"] == "draft"
    assert draft["reviewed_by_user_id"] is None


def test_create_draft_runs_safety_firewall_and_stores_result(client, auth_headers):
    resp = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers)
    draft = resp.json()
    assert draft["safety_verdict"] == "SAFE_TO_CONSIDER"
    assert len(draft["safety_reasons"]) >= 1


def test_create_draft_requires_at_least_one_ingredient(client, auth_headers):
    resp = client.post("/api/v1/nuskha-drafts", json=_safe_payload(ingredients=[]), headers=auth_headers)
    assert resp.status_code == 422


def test_approve_safe_draft_succeeds(client, auth_headers):
    draft = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers).json()
    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={}, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "approved"
    assert resp.json()["reviewed_by_user_id"] is not None


def test_cannot_approve_already_approved_draft(client, auth_headers):
    draft = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers).json()
    client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={}, headers=auth_headers)
    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={}, headers=auth_headers)
    assert resp.status_code == 409


def test_reject_draft(client, auth_headers):
    draft = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers).json()
    resp = client.post(
        f"/api/v1/nuskha-drafts/{draft['id']}/reject", json={"rejection_reason": "Insufficient history"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"
    assert resp.json()["rejection_reason"] == "Insufficient history"


def test_reject_requires_a_reason(client, auth_headers):
    draft = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers).json()
    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/reject", json={"rejection_reason": ""}, headers=auth_headers)
    assert resp.status_code == 422


# --- Clinical Authority Guardrail: the core safety-critical behavior ---

def test_approving_a_pregnancy_blocked_draft_fails_without_override_permission(client, org_id):
    creator_headers = {"Authorization": f"Bearer {make_token(organization_id=org_id, permissions=['nuskha.create', 'nuskha.approve'])}"}
    draft = client.post("/api/v1/nuskha-drafts", json=_pregnant_payload(), headers=creator_headers).json()
    assert draft["safety_verdict"] == "DO_NOT_RECOMMEND"

    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={}, headers=creator_headers)
    assert resp.status_code == 403
    assert "override" in resp.json()["detail"].lower()


def test_approving_a_blocked_draft_fails_without_justification_even_with_override_permission(client, org_id):
    headers = {
        "Authorization": f"Bearer {make_token(organization_id=org_id, permissions=['nuskha.create', 'nuskha.approve', 'safety_firewall.override'])}"
    }
    draft = client.post("/api/v1/nuskha-drafts", json=_pregnant_payload(), headers=headers).json()

    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={"safety_override_justification": ""}, headers=headers)
    assert resp.status_code == 422


def test_approving_a_blocked_draft_succeeds_with_override_permission_and_justification(client, org_id):
    headers = {
        "Authorization": f"Bearer {make_token(organization_id=org_id, permissions=['nuskha.create', 'nuskha.approve', 'safety_firewall.override'])}"
    }
    draft = client.post("/api/v1/nuskha-drafts", json=_pregnant_payload(), headers=headers).json()

    resp = client.post(
        f"/api/v1/nuskha-drafts/{draft['id']}/approve",
        json={"safety_override_justification": "Reviewed with senior Hakeem; obstetric-safe formulation confirmed ingredient by ingredient."},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "approved"
    assert "senior Hakeem" in resp.json()["safety_override_justification"]


def test_non_blocking_verdict_does_not_require_override_even_without_that_permission(client, auth_headers):
    """Sanity check the guardrail only fires for actually-blocking
    verdicts — a CAUTION-level draft (e.g. elderly patient) should approve
    normally without needing safety_firewall.override at all."""
    payload = _safe_payload()
    payload["patient_safety_context"]["age"] = 75  # triggers CAUTION, not a blocking verdict
    draft = client.post("/api/v1/nuskha-drafts", json=payload, headers=auth_headers).json()
    assert draft["safety_verdict"] == "CAUTION"

    resp = client.post(f"/api/v1/nuskha-drafts/{draft['id']}/approve", json={}, headers=auth_headers)
    assert resp.status_code == 200


def test_drafts_scoped_to_organization(client, auth_headers, other_org_headers):
    draft = client.post("/api/v1/nuskha-drafts", json=_safe_payload(), headers=auth_headers).json()
    resp = client.get(f"/api/v1/nuskha-drafts/{draft['id']}", headers=other_org_headers)
    assert resp.status_code == 404


def test_list_drafts_by_patient(client, auth_headers):
    payload = _safe_payload()
    patient_id = payload["patient_id"]
    client.post("/api/v1/nuskha-drafts", json=payload, headers=auth_headers)
    client.post("/api/v1/nuskha-drafts", json=_safe_payload(patient_id=patient_id), headers=auth_headers)

    resp = client.get(f"/api/v1/nuskha-drafts/by-patient/{patient_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2
