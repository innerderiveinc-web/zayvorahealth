def _mufrad_payload(**overrides):
    payload = {
        "name": "Asrul (Withania coagulans)",
        "botanical_name": "Withania coagulans",
        "part_used": "Fruit",
        "synonyms": ["Paneer Dodi"],
        "afal": ["Muqawwi-e-Meda", "Mudirr-e-Baul"],
        "traditional_uses": "Used for digestive weakness and as a mild diuretic",
        "dose": "3-5 grams",
    }
    payload.update(overrides)
    return payload


def test_create_and_get_mufrad(client, auth_headers):
    resp = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers)
    assert resp.status_code == 201, resp.text
    mufrad = resp.json()
    assert mufrad["name"] == "Asrul (Withania coagulans)"
    assert mufrad["afal"] == ["Muqawwi-e-Meda", "Mudirr-e-Baul"]

    detail = client.get(f"/api/v1/mufradat/{mufrad['id']}", headers=auth_headers)
    assert detail.status_code == 200
    assert detail.json()["mizaj"] == []
    assert detail.json()["organAxes"] == []


def test_create_mufrad_requires_auth(client):
    resp = client.post("/api/v1/mufradat", json=_mufrad_payload())
    assert resp.status_code == 401


def test_create_mufrad_requires_permission(client, org_id):
    from tests.conftest import make_token

    token = make_token(organization_id=org_id, permissions=["pharmacopoeia.read"])  # no write
    resp = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_get_unknown_mufrad_404s(client, auth_headers):
    resp = client.get("/api/v1/mufradat/does-not-exist", headers=auth_headers)
    assert resp.status_code == 404


def test_mufrad_not_visible_across_organizations(client, auth_headers, other_org_headers):
    created = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers).json()
    resp = client.get(f"/api/v1/mufradat/{created['id']}", headers=other_org_headers)
    assert resp.status_code == 404


def test_assign_mizaj_to_mufrad(client, auth_headers):
    mufrad = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers).json()
    resp = client.put(
        f"/api/v1/mufradat/{mufrad['id']}/mizaj",
        json={"temperament": "Hot", "hc_degree": 2, "wd_degree": 1},
        headers=auth_headers,
    )
    # temperament must be one of the classical four — "Hot" is not, this
    # should fail validation.
    assert resp.status_code == 422


def test_assign_valid_mizaj_temperament(client, auth_headers):
    mufrad = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers).json()
    resp = client.put(
        f"/api/v1/mufradat/{mufrad['id']}/mizaj",
        json={"temperament": "Safrawi", "hc_degree": 2, "wd_degree": 1},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["temperament"] == "Safrawi"

    detail = client.get(f"/api/v1/mufradat/{mufrad['id']}", headers=auth_headers).json()
    assert detail["mizaj"][0]["temperament"] == "Safrawi"


def test_assign_mizaj_to_unknown_mufrad_404s(client, auth_headers):
    resp = client.put(
        "/api/v1/mufradat/does-not-exist/mizaj",
        json={"temperament": "Damwi", "hc_degree": 1, "wd_degree": 1},
        headers=auth_headers,
    )
    assert resp.status_code == 404


def test_link_mufrad_to_organ_axis(client, auth_headers):
    mufrad = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers).json()
    resp = client.post(f"/api/v1/mufradat/{mufrad['id']}/organ-axes", json={"axis_code": "meda-amaa"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == "meda-amaa"


def test_link_to_unknown_axis_code_404s(client, auth_headers):
    mufrad = client.post("/api/v1/mufradat", json=_mufrad_payload(), headers=auth_headers).json()
    resp = client.post(f"/api/v1/mufradat/{mufrad['id']}/organ-axes", json={"axis_code": "not-a-real-axis"}, headers=auth_headers)
    assert resp.status_code == 404


def test_list_mufradat_filtered_by_organ_axis(client, auth_headers):
    """This is the multi-hop query the whole point of the graph model is
    to make easy: 'find every Mufrad that acts on this organ axis.'"""
    a = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Asrul"), headers=auth_headers).json()
    b = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Sonf"), headers=auth_headers).json()
    client.post(f"/api/v1/mufradat/{a['id']}/organ-axes", json={"axis_code": "meda-amaa"}, headers=auth_headers)
    client.post(f"/api/v1/mufradat/{b['id']}/organ-axes", json={"axis_code": "riya-sadr"}, headers=auth_headers)

    meda_results = client.get("/api/v1/mufradat?organ_axis=meda-amaa", headers=auth_headers).json()
    assert [m["name"] for m in meda_results] == ["Asrul"]

    riya_results = client.get("/api/v1/mufradat?organ_axis=riya-sadr", headers=auth_headers).json()
    assert [m["name"] for m in riya_results] == ["Sonf"]


def test_list_mufradat_filtered_by_mizaj_temperament(client, auth_headers):
    a = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Asrul"), headers=auth_headers).json()
    b = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Sonf"), headers=auth_headers).json()
    client.put(f"/api/v1/mufradat/{a['id']}/mizaj", json={"temperament": "Safrawi", "hc_degree": 2, "wd_degree": 1}, headers=auth_headers)
    client.put(f"/api/v1/mufradat/{b['id']}/mizaj", json={"temperament": "Balghami", "hc_degree": 1, "wd_degree": 2}, headers=auth_headers)

    results = client.get("/api/v1/mufradat?mizaj_temperament=Safrawi", headers=auth_headers).json()
    assert [m["name"] for m in results] == ["Asrul"]


def test_list_mufradat_combined_axis_and_mizaj_filter(client, auth_headers):
    a = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Asrul"), headers=auth_headers).json()
    b = client.post("/api/v1/mufradat", json=_mufrad_payload(name="Sonf"), headers=auth_headers).json()
    for m in (a, b):
        client.post(f"/api/v1/mufradat/{m['id']}/organ-axes", json={"axis_code": "meda-amaa"}, headers=auth_headers)
    client.put(f"/api/v1/mufradat/{a['id']}/mizaj", json={"temperament": "Safrawi", "hc_degree": 2, "wd_degree": 1}, headers=auth_headers)
    client.put(f"/api/v1/mufradat/{b['id']}/mizaj", json={"temperament": "Balghami", "hc_degree": 1, "wd_degree": 2}, headers=auth_headers)

    results = client.get("/api/v1/mufradat?organ_axis=meda-amaa&mizaj_temperament=Safrawi", headers=auth_headers).json()
    assert [m["name"] for m in results] == ["Asrul"]


def test_mufradat_list_scoped_to_organization(client, auth_headers, other_org_headers):
    client.post("/api/v1/mufradat", json=_mufrad_payload(name="Mine"), headers=auth_headers)
    client.post("/api/v1/mufradat", json=_mufrad_payload(name="Theirs"), headers=other_org_headers)

    mine = client.get("/api/v1/mufradat", headers=auth_headers).json()
    theirs = client.get("/api/v1/mufradat", headers=other_org_headers).json()
    assert [m["name"] for m in mine] == ["Mine"]
    assert [m["name"] for m in theirs] == ["Theirs"]
