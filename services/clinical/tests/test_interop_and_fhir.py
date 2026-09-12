from app.interop.abdm_gateway import ABDMGateway
from app.interop.fhir_converter import (
    build_abdm_op_consult_bundle,
    create_fhir_condition_resource,
    create_fhir_medication_request,
    create_fhir_mizaj_observation,
    create_fhir_patient_resource,
)


def test_fhir_patient_resource():
    patient_data = {
        "id": "pat-123",
        "full_name": "Hakim Zayd",
        "gender": "male",
        "date_of_birth": "1985-06-15",
        "abha_number": "12-3456-7890-1234",
        "abha_address": "zayd@abdm",
    }
    res = create_fhir_patient_resource(patient_data)
    assert res["resourceType"] == "Patient"
    assert res["id"] == "pat-123"
    assert res["gender"] == "male"
    assert len(res["identifier"]) == 3  # Internal, ABHA number, ABHA address
    assert "https://nrces.in/ndhm/fhir/r4/StructureDefinition/Patient" in res["meta"]["profile"]


def test_fhir_condition_resource_dual_coding():
    cond = create_fhir_condition_resource(
        condition_id="c-1",
        patient_id="pat-123",
        diagnosis_name="Waja-ul-Mafasil (Articular Gout)",
        icd11_code="FA20.Z",
        unani_amraz_code="amraz-mafasil-01",
    )
    assert cond["resourceType"] == "Condition"
    codings = cond["code"]["coding"]
    systems = [c["system"] for c in codings]
    assert "http://id.who.int/icd/release/11/mms" in systems
    assert "https://zayvora.health/fhir/cs/unani-amraz" in systems


def test_fhir_medication_request_schedule_e1():
    rx = create_fhir_medication_request(
        rx_id="rx-1",
        patient_id="pat-123",
        medication_name="Majun Suranjan",
        dose="5g twice daily with Arq-e-Gaozaban",
        is_schedule_e1=True,
    )
    assert rx["resourceType"] == "MedicationRequest"
    assert rx["status"] == "active"
    assert any("SCHEDULE E(1) POISON" in n["text"] for n in rx["note"])


def test_fhir_mizaj_observation():
    obs = create_fhir_mizaj_observation(
        obs_id="obs-1",
        patient_id="pat-123",
        primary_temperament="Safrawi",
        heat_cold_score=2.5,
        wet_dry_score=1.2,
    )
    assert obs["resourceType"] == "Observation"
    assert obs["valueString"] == "Safrawi"
    assert len(obs["component"]) == 2


def test_abdm_op_consult_bundle():
    bundle = build_abdm_op_consult_bundle(
        patient={"id": "pat-123", "full_name": "Fatima Begum", "gender": "female"},
        conditions=[{"diagnosis_name": "Su-e-Mizaj Damwi"}],
        prescriptions=[{"medication_name": "Sharbat Bazoori", "dose": "20ml with water"}],
        mizaj_assessment={"primary_temperament": "Damwi", "heat_cold_score": 1.0, "wet_dry_score": 1.0},
    )

    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "document"
    # First resource MUST be Composition per FHIR R4 Document standard
    first_resource = bundle["entry"][0]["resource"]
    assert first_resource["resourceType"] == "Composition"
    assert "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord" in first_resource["meta"]["profile"]

    # Verify other entries
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "Patient" in types
    assert "Condition" in types
    assert "MedicationRequest" in types
    assert "Observation" in types


def test_abdm_gateway_verify_abha():
    gw = ABDMGateway()

    # Valid formats
    res1 = gw.verify_abha("12-3456-7890-1234")
    assert res1["valid"] is True
    assert res1["verification_status"] == "VERIFIED_ACTIVE"

    res2 = gw.verify_abha("zayd.khan@abdm")
    assert res2["valid"] is True

    # Invalid formats
    res3 = gw.verify_abha("invalid-abha-string")
    assert res3["valid"] is False


def test_abdm_gateway_consent_flow():
    gw = ABDMGateway()

    req = gw.request_consent(patient_abha="fatima@abdm", purpose_code="CAREMGT")
    assert req["status"] == "REQUESTED"
    cid = req["consent_request_id"]

    # Check status
    status = gw.get_consent_status(cid)
    assert status["status"] == "REQUESTED"

    # Simulate grant
    granted = gw.grant_consent_mock(cid)
    assert granted["status"] == "GRANTED"
    assert "consent_artefact_id" in granted


def test_abdm_gateway_live_mode_configuration_and_packet_push():
    """Verify live mode configuration and Milestone 3 encrypted packet push."""
    gw_live = ABDMGateway(
        client_id="zayvora-hip-test",
        client_secret="test-secret-key",
        gateway_url="https://dev.abdm.gov.in/gateway",
        live_mode=False,  # Headless test assertion
    )
    assert gw_live.client_id == "zayvora-hip-test"
    assert gw_live.gateway_url == "https://dev.abdm.gov.in/gateway"
    assert gw_live.live_mode is False

    # Test Milestone 3 packet push
    push_res = gw_live.push_health_data_packet(
        transaction_id="tx-test-9999",
        patient_abha="91-1234-5678-9012",
        encrypted_fhir_packets=[{"cipher_data": "ZV-AES-GCM-TEST"}],
    )
    assert push_res["status"] == "TRANSFER_SUCCESS"
    assert push_res["transaction_id"] == "tx-test-9999"
    assert push_res["packets_count"] == 1
