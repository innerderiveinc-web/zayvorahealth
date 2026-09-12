import uuid


def test_create_tadbeer_plan(client, auth_headers):
    resp = client.post(
        "/api/v1/tadbeer-plans",
        json={
            "patient_id": str(uuid.uuid4()),
            "encounter_id": str(uuid.uuid4()),
            "name": "Hijama (cupping)",
            "category": "other",
            "indication": "Chronic joint stiffness",
            "method": "Wet cupping at Mafasil-adjacent points",
            "frequency": "Once every 3 weeks",
            "contraindications": "Not on anticoagulants; no active skin infection at site",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["status"] == "active"


def test_create_tadbeer_plan_rejects_invalid_category(client, auth_headers):
    resp = client.post(
        "/api/v1/tadbeer-plans",
        json={"patient_id": str(uuid.uuid4()), "encounter_id": str(uuid.uuid4()), "name": "X", "category": "not-a-real-category"},
        headers=auth_headers,
    )
    assert resp.status_code == 422


def test_tadbeer_plans_require_auth(client):
    resp = client.post(
        "/api/v1/tadbeer-plans",
        json={"patient_id": str(uuid.uuid4()), "encounter_id": str(uuid.uuid4()), "name": "X", "category": "rest"},
    )
    assert resp.status_code == 401


def test_list_tadbeer_plans_for_patient(client, auth_headers):
    patient_id = str(uuid.uuid4())
    client.post(
        "/api/v1/tadbeer-plans",
        json={"patient_id": patient_id, "encounter_id": str(uuid.uuid4()), "name": "Rest protocol", "category": "rest"},
        headers=auth_headers,
    )
    resp = client.get(f"/api/v1/tadbeer-plans/by-patient/{patient_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_create_ghiza_plan(client, auth_headers):
    resp = client.post(
        "/api/v1/ghiza-plans",
        json={
            "patient_id": str(uuid.uuid4()),
            "encounter_id": str(uuid.uuid4()),
            "dietary_goals": "Reduce Balgham accumulation",
            "meal_structure": "Light breakfast, main meal midday, light dinner before sunset",
            "foods_recommended": ["Barley soup", "Ginger tea"],
            "foods_to_limit": ["Dairy", "Cold beverages"],
            "hydration_guidance": "Warm water through the day",
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201, resp.text
    plan = resp.json()
    assert plan["foods_recommended"] == ["Barley soup", "Ginger tea"]
    assert plan["status"] == "active"


def test_ghiza_plans_scoped_to_organization(client, auth_headers, other_org_headers):
    patient_id = str(uuid.uuid4())
    client.post(
        "/api/v1/ghiza-plans",
        json={"patient_id": patient_id, "encounter_id": str(uuid.uuid4())},
        headers=auth_headers,
    )
    resp = client.get(f"/api/v1/ghiza-plans/by-patient/{patient_id}", headers=other_org_headers)
    assert resp.status_code == 200
    assert resp.json() == []
