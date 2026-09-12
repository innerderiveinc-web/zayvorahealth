def _create_patient(client, headers, mrn="MRN-0001"):
    payload = {"mrn": mrn, "full_name": "Ayesha Test Patient", "sex": "female"}
    return client.post("/api/v1/patients", json=payload, headers=headers).json()


def test_timeline_aggregates_events_chronologically(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = client.post(
        "/api/v1/encounters", json={"patient_id": patient["id"], "chief_complaint": "Fatigue"}, headers=auth_headers
    ).json()
    client.post(
        "/api/v1/clinical-notes", json={"encounter_id": encounter["id"], "assessment": "Initial review"}, headers=auth_headers
    )
    client.post(
        "/api/v1/prescriptions", json={"encounter_id": encounter["id"], "medication_name": "Diabease"}, headers=auth_headers
    )
    client.post(
        "/api/v1/appointments",
        json={"patient_id": patient["id"], "scheduled_at": "2026-09-01T10:00:00Z", "reason": "Follow-up"},
        headers=auth_headers,
    )

    resp = client.get(f"/api/v1/patients/{patient['id']}/timeline", headers=auth_headers)
    assert resp.status_code == 200
    events = resp.json()
    event_types = {e["event_type"] for e in events}
    assert event_types == {"encounter", "clinical_note", "prescription", "appointment"}

    # Chronological ordering: each event's timestamp is >= the previous one.
    timestamps = [e["occurred_at"] for e in events]
    assert timestamps == sorted(timestamps)


def test_timeline_only_shows_current_note_version(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = client.post("/api/v1/encounters", json={"patient_id": patient["id"]}, headers=auth_headers).json()
    original = client.post(
        "/api/v1/clinical-notes", json={"encounter_id": encounter["id"], "assessment": "v1"}, headers=auth_headers
    ).json()
    client.post(f"/api/v1/clinical-notes/{original['id']}/amend", json={"assessment": "v2"}, headers=auth_headers)

    events = client.get(f"/api/v1/patients/{patient['id']}/timeline", headers=auth_headers).json()
    note_events = [e for e in events if e["event_type"] == "clinical_note"]
    assert len(note_events) == 1
    assert "v2" in note_events[0]["summary"]


def test_timeline_for_unknown_patient_404s(client, auth_headers):
    import uuid

    resp = client.get(f"/api/v1/patients/{uuid.uuid4()}/timeline", headers=auth_headers)
    assert resp.status_code == 404


def test_timeline_is_organization_scoped(client, auth_headers, other_org_headers):
    patient = _create_patient(client, auth_headers)
    resp = client.get(f"/api/v1/patients/{patient['id']}/timeline", headers=other_org_headers)
    assert resp.status_code == 404
