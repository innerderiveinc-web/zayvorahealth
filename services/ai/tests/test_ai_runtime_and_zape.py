import uuid
import contextlib

try:
    import pytest
except ImportError:
    class MockPytest:
        @staticmethod
        @contextlib.contextmanager
        def raises(expected_exception, match=None):
            try:
                yield
            except expected_exception as e:
                if match and match not in str(e):
                    raise AssertionError(f"Expected match '{match}' in '{str(e)}'")
            else:
                raise AssertionError(f"Expected {expected_exception} to be raised")

    pytest = MockPytest()

from app.engines.zape_personalization import (
    calculate_age_and_renal_posology,
    modulate_by_season,
    modulate_by_temperament,
    run_zape_personalization,
)
from app.providers.fallback_router import ChainedFallbackRouter


class FailingProvider:
    def __init__(self, name="Failing"):
        self.name = name

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        raise ConnectionError(f"Network error in {self.name}")


class WorkingProvider:
    def __init__(self, response="Working response"):
        self.response = response
        self.called = False

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        self.called = True
        return self.response


def test_chained_fallback_router_primary_success():
    primary = WorkingProvider("Primary Success")
    secondary = WorkingProvider("Secondary Success")
    router = ChainedFallbackRouter([primary, secondary])

    result = router.generate(system_prompt="sys", user_prompt="usr")
    assert result == "Primary Success"
    assert primary.called is True
    assert secondary.called is False
    assert len(router.degradation_logs) == 0


def test_chained_fallback_router_failover_to_secondary():
    primary = FailingProvider("Primary")
    secondary = WorkingProvider("Fallback Success")
    router = ChainedFallbackRouter([primary, secondary])

    result = router.generate(system_prompt="sys", user_prompt="usr")
    assert result == "Fallback Success"
    assert secondary.called is True
    assert len(router.degradation_logs) == 1
    assert "Network error in Primary" in router.degradation_logs[0]["error"]


def test_chained_fallback_router_all_fail():
    p1 = FailingProvider("P1")
    p2 = FailingProvider("P2")
    router = ChainedFallbackRouter([p1, p2])

    with pytest.raises(RuntimeError, match="All AI providers in fallback chain failed"):
        router.generate(system_prompt="sys", user_prompt="usr")
    assert len(router.degradation_logs) == 2


def test_zape_pediatric_posology():
    res = calculate_age_and_renal_posology(age=6)
    assert res["category"] == "Child"
    assert 0.25 <= res["posology_scaling_factor"] <= 0.35
    assert any("Pediatric" in w for w in res["warnings"])


def test_zape_geriatric_renal_titration():
    # 78 yrs (base 0.65) with Stage 4 CKD (eGFR 22 -> 50% of base = 0.33)
    res = calculate_age_and_renal_posology(age=78, egfr=22)
    assert res["category"] == "Geriatric"
    assert res["posology_scaling_factor"] == 0.33
    assert any("CKD" in w for w in res["warnings"])


def test_zape_temperament_safrawi():
    mod = modulate_by_temperament("Safrawi")
    assert mod["temperament"] == "Safrawi"
    assert any("cooling correctives" in m for m in mod["musleh_recommendations"])
    assert any("Filfil Siyah" in c for c in mod["contraindicated_classes"])


def test_zape_seasonal_modulation():
    summer = modulate_by_season("summer")
    assert "Saif" in summer["season_identified"]
    assert "cooling syrups" in summer["seasonal_guidance"].lower()

    winter = modulate_by_season("winter")
    assert "Shita" in winter["season_identified"]
    assert "warming" in winter["seasonal_guidance"].lower()


def test_zape_master_orchestration():
    patient_ctx = {
        "age": 70,
        "egfr": 45.0,
        "mizaj": {"primary_temperament": "Balghami"},
    }
    result = run_zape_personalization(patient_context=patient_ctx, season="shita")
    assert "posology" in result
    assert "temperament_modulation" in result
    assert "seasonal_modulation" in result
    assert "ZAPE 2.0" in result["overall_summary"]
    assert result["posology"]["posology_scaling_factor"] < 1.0


def test_hakeem_refine_engine_logic():
    from app.clients.clinical_client import FakeClinicalClient
    from app.clients.knowledge_client import FakeKnowledgeClient
    from app.engines.hakeem_sahab import run_hakeem_refinement
    from app.providers.fake_provider import ScriptedFakeProvider

    clinical = FakeClinicalClient({"p-123": {"age": 45, "allergies": [], "comorbidities": []}})
    knowledge = FakeKnowledgeClient({})
    provider = ScriptedFakeProvider()

    result = run_hakeem_refinement(
        chief_complaint="chronic cough",
        patient_id="p-123",
        clinician_feedback="Avoid heating herbs like Filfil Siyah; focus on mucilaginous herbs.",
        previous_sections={"clinical_summary": "Patient reports 2-month cough."},
        auth_header="Bearer test-token",
        clinical_client=clinical,
        knowledge_client=knowledge,
        ai_provider=provider,
    )
    assert result["valid"] is True
    assert result["requiresClinicianReview"] is True
    assert "Avoid heating herbs" in result["clinicianFeedbackApplied"]
    assert "zapePersonalization" in result


def test_hakeem_personalize_endpoint(client=None, auth_headers=None):
    payload = {
        "patient_context": {
            "age": 30,
            "mizaj": "Safrawi",
        },
        "season": "saif",
    }
    if client is not None and auth_headers is not None:
        resp = client.post("/api/v1/hakeem/personalize", json=payload, headers=auth_headers)
        assert resp.status_code == 200, resp.text
        data = resp.json()
    else:
        data = run_zape_personalization(
            patient_context=payload["patient_context"],
            season=payload["season"],
        )
    assert data["posology"]["posology_scaling_factor"] == 1.0
    assert data["temperament_modulation"]["temperament"] == "Safrawi"
    assert "Saif" in data["seasonal_modulation"]["season_identified"]


def test_hakeem_refine_endpoint(client=None, auth_headers=None, sample_patient_id=None):
    from app.engines.hakeem_sahab import run_hakeem_refinement
    from app.clients.clinical_client import FakeClinicalClient
    from app.clients.knowledge_client import FakeKnowledgeClient
    from app.providers.fake_provider import ScriptedFakeProvider

    patient_id = sample_patient_id or str(uuid.uuid4())
    refine_payload = {
        "consultation_id": str(uuid.uuid4()),
        "clinician_feedback": "Patient has elevated blood pressure; exclude ephedra/som-e-fars and sweet syrups like Sharbat Zoofa.",
    }

    if client is not None and auth_headers is not None:
        created = client.post(
            "/api/v1/hakeem/consult",
            json={"patient_id": patient_id, "chief_complaint": "chronic cough and wheezing", "organ_axis": "meda-tanaffus"},
            headers=auth_headers,
        ).json()
        refine_payload["consultation_id"] = created["id"]
        resp = client.post("/api/v1/hakeem/refine", json=refine_payload, headers=auth_headers)
        assert resp.status_code == 200, resp.text
        refined = resp.json()
        assert refined["valid"] is True
        assert refined["consultation_id"] == created["id"]
        assert refined["clinician_feedback_applied"] == refine_payload["clinician_feedback"]
    else:
        from app.engines.hakeem_sahab import run_hakeem_refinement
        clinical = FakeClinicalClient(patients={patient_id: {"age": 45, "allergies": [], "comorbidities": []}})
        knowledge = FakeKnowledgeClient()
        refined = run_hakeem_refinement(
            chief_complaint="chronic cough and wheezing",
            patient_id=patient_id,
            clinician_feedback=refine_payload["clinician_feedback"],
            previous_sections={"1. MIZAJ DIAGNOSIS": "Su-i-Mizaj Haar"},
            auth_header="Bearer fake-token",
            clinical_client=clinical,
            knowledge_client=knowledge,
            ai_provider=ScriptedFakeProvider(),
        )
        assert refined["valid"] is True
        assert refined["requiresClinicianReview"] is True
        assert "elevated blood pressure" in refined["clinicianFeedbackApplied"]
    requires_review = refined.get("requires_clinician_review", refined.get("requiresClinicianReview"))
    assert requires_review is True
    has_zape = "zape_personalization" in refined or "zapePersonalization" in refined
    assert has_zape is True
