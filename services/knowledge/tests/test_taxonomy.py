def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200


def test_organ_axes_returns_all_twelve(client):
    resp = client.get("/api/v1/organ-axes")
    assert resp.status_code == 200
    axes = resp.json()
    assert len(axes) == 12
    codes = {a["code"] for a in axes}
    assert "meda-amaa" in codes
    assert "qalb-uroq" in codes


def test_mizaj_temperaments_returns_all_four(client):
    resp = client.get("/api/v1/mizaj-temperaments")
    assert resp.status_code == 200
    temperaments = {t["temperament"] for t in resp.json()}
    assert temperaments == {"Damwi", "Safrawi", "Saudawi", "Balghami"}


def test_evidence_levels_covers_e0_to_e6(client):
    resp = client.get("/api/v1/evidence-levels")
    assert resp.status_code == 200
    levels = resp.json()
    assert set(levels.keys()) == {"E0", "E1", "E2", "E3", "E4", "E5", "E6"}


def test_knowledge_worlds_covers_a_to_d(client):
    resp = client.get("/api/v1/knowledge-worlds")
    assert resp.status_code == 200
    assert set(resp.json().keys()) == {"A", "B", "C", "D"}
