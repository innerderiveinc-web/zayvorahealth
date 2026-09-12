def _create_patient(client, headers, mrn="MRN-0001"):
    payload = {"mrn": mrn, "full_name": "Ayesha Test Patient", "sex": "female"}
    return client.post("/api/v1/patients", json=payload, headers=headers).json()


def _create_encounter(client, headers, patient_id):
    return client.post("/api/v1/encounters", json={"patient_id": patient_id}, headers=headers).json()


def test_create_prescription(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    resp = client.post(
        "/api/v1/prescriptions",
        json={"encounter_id": encounter["id"], "medication_name": "Diabease", "dose": "10ml", "frequency": "BD"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "active"


def test_discontinue_prescription(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    rx = client.post(
        "/api/v1/prescriptions", json={"encounter_id": encounter["id"], "medication_name": "Diabease"}, headers=auth_headers
    ).json()
    resp = client.post(
        f"/api/v1/prescriptions/{rx['id']}/discontinue", json={"reason": "No longer needed"}, headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "discontinued"
    assert resp.json()["discontinued_reason"] == "No longer needed"


def test_cannot_discontinue_twice(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    rx = client.post(
        "/api/v1/prescriptions", json={"encounter_id": encounter["id"], "medication_name": "Diabease"}, headers=auth_headers
    ).json()
    client.post(f"/api/v1/prescriptions/{rx['id']}/discontinue", json={}, headers=auth_headers)
    resp = client.post(f"/api/v1/prescriptions/{rx['id']}/discontinue", json={}, headers=auth_headers)
    assert resp.status_code == 409


def test_discontinued_prescription_row_is_kept_not_deleted(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    rx = client.post(
        "/api/v1/prescriptions", json={"encounter_id": encounter["id"], "medication_name": "Diabease"}, headers=auth_headers
    ).json()
    client.post(f"/api/v1/prescriptions/{rx['id']}/discontinue", json={}, headers=auth_headers)

    all_rx = client.get(f"/api/v1/prescriptions/by-patient/{patient['id']}", headers=auth_headers).json()
    active_rx = client.get(f"/api/v1/prescriptions/by-patient/{patient['id']}?active_only=true", headers=auth_headers).json()
    assert len(all_rx) == 1
    assert len(active_rx) == 0


def test_create_appointment(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    resp = client.post(
        "/api/v1/appointments",
        json={"patient_id": patient["id"], "scheduled_at": "2026-09-01T10:00:00Z", "reason": "Follow-up"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "scheduled"


def test_update_appointment_status(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    appt = client.post(
        "/api/v1/appointments", json={"patient_id": patient["id"], "scheduled_at": "2026-09-01T10:00:00Z"}, headers=auth_headers
    ).json()
    resp = client.patch(f"/api/v1/appointments/{appt['id']}", json={"status": "completed"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"


def test_update_appointment_rejects_invalid_status(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    appt = client.post(
        "/api/v1/appointments", json={"patient_id": patient["id"], "scheduled_at": "2026-09-01T10:00:00Z"}, headers=auth_headers
    ).json()
    resp = client.patch(f"/api/v1/appointments/{appt['id']}", json={"status": "not-a-real-status"}, headers=auth_headers)
    assert resp.status_code == 422
