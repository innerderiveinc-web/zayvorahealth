def _create_patient(client, headers, mrn="MRN-0001"):
    payload = {"mrn": mrn, "full_name": "Ayesha Test Patient", "sex": "female"}
    return client.post("/api/v1/patients", json=payload, headers=headers).json()


def _create_encounter(client, headers, patient_id):
    return client.post(
        "/api/v1/encounters", json={"patient_id": patient_id, "chief_complaint": "Fatigue"}, headers=headers
    ).json()


def test_create_encounter(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    resp = client.post(
        "/api/v1/encounters", json={"patient_id": patient["id"], "chief_complaint": "Chronic fatigue"}, headers=auth_headers
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "open"


def test_create_encounter_for_unknown_patient_404s(client, auth_headers):
    import uuid

    resp = client.post("/api/v1/encounters", json={"patient_id": str(uuid.uuid4())}, headers=auth_headers)
    assert resp.status_code == 404


def test_close_encounter(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    resp = client.post(f"/api/v1/encounters/{encounter['id']}/close", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "closed"
    assert resp.json()["closed_at"] is not None


def test_cannot_close_already_closed_encounter(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    client.post(f"/api/v1/encounters/{encounter['id']}/close", headers=auth_headers)
    resp = client.post(f"/api/v1/encounters/{encounter['id']}/close", headers=auth_headers)
    assert resp.status_code == 409


def test_create_clinical_note(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    resp = client.post(
        "/api/v1/clinical-notes",
        json={"encounter_id": encounter["id"], "subjective": "Fatigue x3mo", "assessment": "Suspected low mizaj balance"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    note = resp.json()
    assert note["is_current"] is True
    assert note["amends_note_id"] is None


def test_amending_a_note_creates_new_version_and_supersedes_original(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    original = client.post(
        "/api/v1/clinical-notes",
        json={"encounter_id": encounter["id"], "assessment": "Initial assessment"},
        headers=auth_headers,
    ).json()

    amended_resp = client.post(
        f"/api/v1/clinical-notes/{original['id']}/amend",
        json={"assessment": "Corrected assessment after review"},
        headers=auth_headers,
    )
    assert amended_resp.status_code == 201
    amended = amended_resp.json()
    assert amended["amends_note_id"] == original["id"]
    assert amended["is_current"] is True
    assert amended["id"] != original["id"]

    # The ORIGINAL row must still exist, unedited, just no longer "current".
    # We can only verify this via the /history endpoint since the list
    # endpoint hides superseded notes by default (checked below too).
    history = client.get(f"/api/v1/clinical-notes/{original['id']}/history", headers=auth_headers).json()
    assert len(history) == 2
    assert history[0]["id"] == original["id"]
    assert history[0]["assessment"] == "Initial assessment"  # original text untouched
    assert history[1]["id"] == amended["id"]


def test_cannot_amend_an_already_superseded_note(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    original = client.post(
        "/api/v1/clinical-notes", json={"encounter_id": encounter["id"], "assessment": "v1"}, headers=auth_headers
    ).json()
    client.post(f"/api/v1/clinical-notes/{original['id']}/amend", json={"assessment": "v2"}, headers=auth_headers)

    # Trying to amend the now-stale original again should fail.
    resp = client.post(f"/api/v1/clinical-notes/{original['id']}/amend", json={"assessment": "v3"}, headers=auth_headers)
    assert resp.status_code == 409


def test_list_notes_hides_superseded_versions_by_default(client, auth_headers):
    patient = _create_patient(client, auth_headers)
    encounter = _create_encounter(client, auth_headers, patient["id"])
    original = client.post(
        "/api/v1/clinical-notes", json={"encounter_id": encounter["id"], "assessment": "v1"}, headers=auth_headers
    ).json()
    client.post(f"/api/v1/clinical-notes/{original['id']}/amend", json={"assessment": "v2"}, headers=auth_headers)

    current_only = client.get(f"/api/v1/clinical-notes/by-patient/{patient['id']}", headers=auth_headers).json()
    assert len(current_only) == 1
    assert current_only[0]["assessment"] == "v2"

    with_history = client.get(
        f"/api/v1/clinical-notes/by-patient/{patient['id']}?include_superseded=true", headers=auth_headers
    ).json()
    assert len(with_history) == 2
