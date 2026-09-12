import pytest

from app.clients.clinical_client import FakeClinicalClient
from app.clients.knowledge_client import FakeKnowledgeClient
from app.engines.hakeem_sahab import run_hakeem_consultation
from app.providers.fake_provider import DEFAULT_WELL_FORMED_RESPONSE, ScriptedFakeProvider


def test_consultation_fetches_patient_context_and_mufradat_then_calls_provider():
    patient_id = "patient-1"
    clinical = FakeClinicalClient(patients={patient_id: {"age": 40, "allergies": ["garlic"], "current_medications": []}})
    knowledge = FakeKnowledgeClient(mufradat_by_axis={"meda-amaa": [{"name": "Sonf"}]})
    provider = ScriptedFakeProvider()

    result = run_hakeem_consultation(
        chief_complaint="chronic fatigue",
        organ_axis="meda-amaa",
        patient_id=patient_id,
        auth_header="Bearer token",
        clinical_client=clinical,
        knowledge_client=knowledge,
        ai_provider=provider,
    )

    assert result["valid"] is True
    assert result["candidateMufradat"] == [{"name": "Sonf"}]
    # The prompt actually sent to the provider should carry through the
    # fetched context — this is what proves orchestration happened, not
    # just that a canned response was returned.
    assert "chronic fatigue" in provider.last_user_prompt
    assert "garlic" in provider.last_user_prompt
    assert "Sonf" in provider.last_user_prompt


def test_unknown_patient_raises_value_error():
    clinical = FakeClinicalClient(patients={})
    knowledge = FakeKnowledgeClient()
    provider = ScriptedFakeProvider()

    with pytest.raises(ValueError, match="not found"):
        run_hakeem_consultation(
            chief_complaint="x",
            organ_axis=None,
            patient_id="does-not-exist",
            auth_header="Bearer token",
            clinical_client=clinical,
            knowledge_client=knowledge,
            ai_provider=provider,
        )


def test_malformed_provider_response_is_flagged_invalid_not_silently_accepted():
    clinical = FakeClinicalClient(patients={"p1": {"age": 30}})
    knowledge = FakeKnowledgeClient()
    provider = ScriptedFakeProvider(response="Sorry, I can't help with that.")

    result = run_hakeem_consultation(
        chief_complaint="x",
        organ_axis=None,
        patient_id="p1",
        auth_header="Bearer token",
        clinical_client=clinical,
        knowledge_client=knowledge,
        ai_provider=provider,
    )

    assert result["valid"] is False
    assert len(result["missingSections"]) == 13  # every required section missing
    assert result["sections"] == {}
    # Even an invalid response is still marked as requiring clinician
    # review — there's no path where this engine implies "safe to skip
    # review because the format was bad."
    assert result["requiresClinicianReview"] is True


def test_no_organ_axis_returns_all_known_mufradat():
    clinical = FakeClinicalClient(patients={"p1": {"age": 30}})
    knowledge = FakeKnowledgeClient(mufradat_by_axis={"axis-a": [{"name": "A"}], "axis-b": [{"name": "B"}]})
    provider = ScriptedFakeProvider()

    result = run_hakeem_consultation(
        chief_complaint="x", organ_axis=None, patient_id="p1", auth_header="Bearer token",
        clinical_client=clinical, knowledge_client=knowledge, ai_provider=provider,
    )
    names = {m["name"] for m in result["candidateMufradat"]}
    assert names == {"A", "B"}


def test_consultation_prompt_includes_pregnancy_and_comorbidities():
    patient_id = "pregnant-patient"
    clinical = FakeClinicalClient(
        patients={
            patient_id: {
                "age": 28,
                "pregnancy_status": "pregnant",
                "comorbidities": ["gestational-diabetes", "mild-hypertension"],
                "allergies": [],
                "current_medications": [],
            }
        }
    )
    knowledge = FakeKnowledgeClient()
    provider = ScriptedFakeProvider()

    result = run_hakeem_consultation(
        chief_complaint="morning nausea",
        organ_axis="meda-amaa",
        patient_id=patient_id,
        auth_header="Bearer token",
        clinical_client=clinical,
        knowledge_client=knowledge,
        ai_provider=provider,
    )

    assert result["valid"] is True
    assert "Pregnancy status: pregnant" in provider.last_user_prompt
    assert "gestational-diabetes, mild-hypertension" in provider.last_user_prompt

