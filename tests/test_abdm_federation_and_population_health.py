"""
ZAYVORA Health OS™ — Test Suite #65: ABDM FHIR Interoperability, Enterprise Federation & Population Health
========================================================================================================
Validates Sequences 14–16 of the ZAYVORA Clinical Continuum:
1. Sequence 14: ABDM FHIR R4 Bundle conformance (OPConsultRecord, PrescriptionRecord, Dual ICD-11 & Amraz coding,
   10-Ajnas Mizaj Observation, 8-Tier Parhez CarePlan, and HIP Data Transfer Envelope).
2. Sequence 15: Enterprise Multi-Clinic Federation (Facility tiers, cryptographically signed HMAC referrals,
   cross-facility zero-leakage security boundary, and FEFO inventory transfers).
3. Sequence 16: Population Health & Seasonal Humoral Surveillance (Canonical 4 seasons Asbab-e-Sittah advisory,
   cohort humoral distribution, and multi-clinic ADR cluster detection with safety hold).
4. Live REST API Server integration for all Sequence 14–16 endpoints.
"""

import sys
import os
import io
import json
import unittest
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.clinical.app.interop.abdm_fhir_continuum_orchestrator import (
    ABDMFHIRContinuumOrchestrator,
    UNANI_AMRAZ_ICD11_MAP,
    UNANI_NAMING_SYSTEM,
    ICD11_SYSTEM,
    NRCES_SYSTEM,
)
from services.clinical.app.engines.multi_clinic_federation_engine import (
    MultiClinicFederationEngine,
    FacilityTier,
    ClinicFacility,
    InterClinicReferral,
)
from services.clinical.app.engines.population_health_engine import (
    PopulationHealthEngine,
    CanonicalSeason,
    SeasonalHumoralAdvisory,
    PharmacovigilanceClusterAlert,
)
from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
    ClinicalIntelligenceCoreOrchestrator,
    ClinicalContinuumRequest,
)
from services.live_api_server import ZayvoraApiHandler


def _call_get(path):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    req.headers = {}
    req.request_version = "HTTP/1.1"
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_GET()
    raw = req.wfile.getvalue().decode()
    header, _, body = raw.partition("\r\n\r\n")
    return json.loads(body) if body.strip() else {}


def _call_post(path, data):
    req = ZayvoraApiHandler.__new__(ZayvoraApiHandler)
    req.path = path
    body_bytes = json.dumps(data).encode("utf-8")
    req.headers = {"Content-Length": str(len(body_bytes)), "Content-Type": "application/json"}
    req.request_version = "HTTP/1.1"
    req.rfile = io.BytesIO(body_bytes)
    req.wfile = io.BytesIO()
    req.log_request = lambda *a, **k: None
    req.do_POST()
    raw = req.wfile.getvalue().decode()
    header, _, body = raw.partition("\r\n\r\n")
    return json.loads(body) if body.strip() else {}


class TestABDMFHIRFederationAndPopulationHealth(unittest.TestCase):

    def setUp(self):
        if not hasattr(TestABDMFHIRFederationAndPopulationHealth, "_cached_c_dict"):
            req = ClinicalContinuumRequest(
                patient_id="PAT-ABDM-001",
                patient_name="Hakim Qasim Khan",
                age=52,
                gender="MALE",
                chief_complaints=["Joint stiffness", "Bilateral knee arthralgia", "Morning stiffness > 45 mins"],
                presenting_condition="Waja-ul-Mafasil",
                symptom_duration_days=30,
                baseline_pain_vas=7.5,
                constitutional_signs={"pulse": "Azeem, Bateea", "tongue": "Saburrah bayda (white coating)"},
                targeted_axes=["Musculoskeletal & Articular Axis", "Gastrointestinal & Metabolic Axis"],
                candidate_drugs=["Suranjan Shirin", "Asgand Nagori", "Zanjabeel"],
                clinician_id="HAK-DEL-009",
                clinician_role="HAKEEM",
                followup_proms_day=14,
                followup_symptom_vas=3.0,
                followup_adverse_events=[]
            )
            res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
            TestABDMFHIRFederationAndPopulationHealth._cached_c_dict = asdict(res)
        self.c_dict = TestABDMFHIRFederationAndPopulationHealth._cached_c_dict

    # -------------------------------------------------------------------------
    # Test 1: ABDM OPConsultRecord Bundle Conformance
    # -------------------------------------------------------------------------
    def test_01_abdm_op_consult_bundle_conformance(self):
        bundle = ABDMFHIRContinuumOrchestrator.build_op_consult_bundle(self.c_dict)

        self.assertEqual(bundle.get("resourceType"), "Bundle")
        self.assertEqual(bundle.get("type"), "document")
        self.assertIn("https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord", bundle["meta"]["profile"])

        entries = bundle.get("entry", [])
        self.assertTrue(len(entries) >= 5, "OPConsult bundle must contain at least Composition, Patient, Practitioner, Condition, Observations")

        # Composition MUST be the first entry per NRCeS document bundle profile
        first_res = entries[0]["resource"]
        self.assertEqual(first_res["resourceType"], "Composition")
        self.assertEqual(first_res["status"], "final")

        section_codes = [s["code"]["coding"][0]["code"] for s in first_res.get("section", []) if "coding" in s.get("code", {})]
        self.assertIn("chief-complaints", section_codes)
        self.assertIn("diagnosis", section_codes)
        self.assertIn("unani-mizaj", section_codes)
        self.assertIn("medications", section_codes)
        self.assertIn("care-plan", section_codes)

        # Check Dual Coding on Condition entry (ICD-11 & Unani Amraz)
        condition_entry = next((e["resource"] for e in entries if e["resource"]["resourceType"] == "Condition"), None)
        self.assertIsNotNone(condition_entry, "Condition resource must be present in bundle")
        codings = condition_entry["code"]["coding"]
        systems = [c["system"] for c in codings]
        self.assertIn(UNANI_NAMING_SYSTEM, systems, "Unani Amraz coding missing")
        self.assertIn(ICD11_SYSTEM, systems, "ICD-11 dual coding missing")

        # Check 10-Ajnas Mizaj Observation present
        mizaj_obs = next((e["resource"] for e in entries if e["resource"]["resourceType"] == "Observation" and "mizaj" in e["resource"].get("id", "").lower()), None)
        self.assertIsNotNone(mizaj_obs, "Mizaj Observation must be present")
        self.assertEqual(mizaj_obs["status"], "final")

        # Check Parhez CarePlan present
        care_plan = next((e["resource"] for e in entries if e["resource"]["resourceType"] == "CarePlan"), None)
        self.assertIsNotNone(care_plan, "CarePlan must be present for 8-Tier Parhez")
        self.assertEqual(care_plan["status"], "active")

    # -------------------------------------------------------------------------
    # Test 2: ABDM PrescriptionRecord Bundle Conformance
    # -------------------------------------------------------------------------
    def test_02_abdm_prescription_bundle_conformance(self):
        bundle = ABDMFHIRContinuumOrchestrator.build_prescription_bundle(self.c_dict)

        self.assertEqual(bundle.get("resourceType"), "Bundle")
        self.assertEqual(bundle.get("type"), "document")
        self.assertIn("https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord", bundle["meta"]["profile"])

        entries = bundle.get("entry", [])
        med_requests = [e["resource"] for e in entries if e["resource"]["resourceType"] == "MedicationRequest"]
        self.assertTrue(len(med_requests) > 0, "Prescription bundle must contain MedicationRequest entries")

        for mr in med_requests:
            self.assertEqual(mr["status"], "active")
            self.assertEqual(mr["intent"], "order")
            self.assertTrue(len(mr["medicationCodeableConcept"]["coding"]) > 0)

    # -------------------------------------------------------------------------
    # Test 3: ABDM Milestone 3 HIP Data Transfer Envelope & Checksum
    # -------------------------------------------------------------------------
    def test_03_abdm_hip_data_transfer_envelope_and_checksum(self):
        bundle = ABDMFHIRContinuumOrchestrator.build_op_consult_bundle(self.c_dict)
        envelope = ABDMFHIRContinuumOrchestrator.create_hip_data_transfer_envelope(
            fhir_bundle=bundle,
            recipient_hiu_id="HIU-FORTIS-LKO",
            consent_id="CONSENT-ABDM-2026-9921"
        )

        self.assertEqual(envelope["envelope_version"], "ABDM-M3-v1.0")
        self.assertEqual(envelope["recipient_hiu_id"], "HIU-FORTIS-LKO")
        self.assertEqual(envelope["consent_id"], "CONSENT-ABDM-2026-9921")
        self.assertEqual(envelope["checksum_algorithm"], "SHA-256")
        self.assertTrue(len(envelope["checksum"]) == 64, "SHA-256 hex string must be 64 characters")
        self.assertTrue(envelope["encrypted_data"].startswith("eyJ"), "Base64 encoded ciphertext required")

    # -------------------------------------------------------------------------
    # Test 4: Multi-Clinic Topology & Facility Tiers
    # -------------------------------------------------------------------------
    def test_04_multi_clinic_topology_and_tiers(self):
        clinics = MultiClinicFederationEngine.list_clinics()
        self.assertGreaterEqual(len(clinics), 4, "Must have at least 4 registered federated clinics")

        tiers = {c["tier"] for c in clinics}
        self.assertIn(FacilityTier.TIER_1_CENTRAL_HOSPITAL.value, tiers)
        self.assertIn(FacilityTier.TIER_2_REGIONAL_SPECIALTY.value, tiers)
        self.assertIn(FacilityTier.TIER_3_COMMUNITY_MATAB.value, tiers)

        delhi = MultiClinicFederationEngine.get_clinic("FAC-DEL-CENTRAL-01")
        self.assertIsNotNone(delhi)
        self.assertEqual(delhi.tier, FacilityTier.TIER_1_CENTRAL_HOSPITAL)
        self.assertGreaterEqual(len(delhi.specialty_axes_available), 10)
        self.assertTrue(delhi.active)

    # -------------------------------------------------------------------------
    # Test 5: Cryptographic Inter-Clinic Referral Token Creation & Redemption
    # -------------------------------------------------------------------------
    def test_05_cryptographic_inter_clinic_referral_handshake(self):
        ref = MultiClinicFederationEngine.create_inter_clinic_referral(
            patient_id="PAT-FED-007",
            source_facility_id="FAC-DEL-CENTRAL-01",
            target_facility_id="FAC-HYD-REGIONAL-02",
            referring_clinician_id="DOC-DEL-01",
            clinical_condition="Waja-ul-Mafasil",
            specialty_axis_required="Musculoskeletal & Articular Axis",
            reason_for_referral="Tertiary Hijamah & Nutool specialized therapy",
            validity_days=14
        )

        self.assertTrue(ref.referral_token.startswith("ZAY-REF-"))
        self.assertEqual(ref.status, "PENDING_ACCEPTANCE")
        self.assertEqual(ref.source_facility_id, "FAC-DEL-CENTRAL-01")
        self.assertEqual(ref.target_facility_id, "FAC-HYD-REGIONAL-02")

        # Redeem token at receiving facility
        redemption = MultiClinicFederationEngine.redeem_inter_clinic_referral(
            referral_token=ref.referral_token,
            receiving_facility_id="FAC-HYD-REGIONAL-02",
            accepting_clinician_id="DOC-HYD-04"
        )

        self.assertTrue(redemption["success"])
        self.assertEqual(redemption["status"], "REDEEMED")
        self.assertTrue(redemption["access_granted"])
        self.assertEqual(redemption["patient_id"], "PAT-FED-007")

        # Attempting to redeem a second time must fail
        double_redemption = MultiClinicFederationEngine.redeem_inter_clinic_referral(
            referral_token=ref.referral_token,
            receiving_facility_id="FAC-HYD-REGIONAL-02",
            accepting_clinician_id="DOC-HYD-04"
        )
        self.assertFalse(double_redemption["success"])
        self.assertIn("already redeemed", double_redemption["error"])

    # -------------------------------------------------------------------------
    # Test 6: Cross-Facility Security Boundary & Tamper Resistance
    # -------------------------------------------------------------------------
    def test_06_cross_facility_referral_security_boundary(self):
        ref = MultiClinicFederationEngine.create_inter_clinic_referral(
            patient_id="PAT-FED-008",
            source_facility_id="FAC-DEL-CENTRAL-01",
            target_facility_id="FAC-HYD-REGIONAL-02",
            referring_clinician_id="DOC-DEL-01",
            clinical_condition="Su-e-Mizaj Damawi",
            specialty_axis_required="Hematologic & Immunologic Axis",
        )

        # 1. Redemption at WRONG clinic facility must be rejected
        wrong_clinic = MultiClinicFederationEngine.redeem_inter_clinic_referral(
            referral_token=ref.referral_token,
            receiving_facility_id="FAC-BLR-COMMUNITY-04",
            accepting_clinician_id="DOC-BLR-01"
        )
        self.assertFalse(wrong_clinic["success"])
        self.assertIn("Target clinic mismatch", wrong_clinic["error"])

        # 2. Tampered token must be rejected
        tampered_token = ref.referral_token[:-4] + "dead"
        tampered_result = MultiClinicFederationEngine.redeem_inter_clinic_referral(
            referral_token=tampered_token,
            receiving_facility_id="FAC-HYD-REGIONAL-02",
            accepting_clinician_id="DOC-HYD-04"
        )
        self.assertFalse(tampered_result["success"])
        self.assertTrue(
            "not found" in tampered_result["error"].lower()
            or "invalid" in tampered_result["error"].lower()
        )

        # 3. Non-existent target clinic during creation raises ValueError
        with self.assertRaises(ValueError):
            MultiClinicFederationEngine.create_inter_clinic_referral(
                patient_id="PAT-FED-009",
                source_facility_id="FAC-DEL-CENTRAL-01",
                target_facility_id="FAC-NON-EXISTENT",
                referring_clinician_id="DOC-DEL-01",
                clinical_condition="Test",
                specialty_axis_required="Test",
            )

    # -------------------------------------------------------------------------
    # Test 7: Federated FEFO Inventory Query & Stock Transfer
    # -------------------------------------------------------------------------
    def test_07_federated_inventory_fefo_transfer(self):
        inventory = MultiClinicFederationEngine.query_federated_inventory(drug_name="Suranjan Shirin")
        self.assertGreater(len(inventory), 0)

        # Execute a transfer from Central Hospital (Del) to Regional (Hyd)
        transfer = MultiClinicFederationEngine.request_inventory_transfer(
            drug_name="Suranjan Shirin",
            quantity=15,
            source_facility_id="FAC-DEL-CENTRAL-01",
            target_facility_id="FAC-HYD-REGIONAL-02",
            requested_by_clinician="DOC-HYD-04"
        )

        self.assertTrue(transfer["success"])
        self.assertEqual(transfer["status"], "TRANSFERRED_IN_TRANSIT")
        self.assertEqual(transfer["quantity_transferred"], 15)
        self.assertTrue(transfer["fefo_lot_selected"].startswith("LOT-SS-"))

        # Requesting more than available stock must fail gracefully
        huge_transfer = MultiClinicFederationEngine.request_inventory_transfer(
            drug_name="Suranjan Shirin",
            quantity=99999,
            source_facility_id="FAC-DEL-CENTRAL-01",
            target_facility_id="FAC-HYD-REGIONAL-02",
            requested_by_clinician="DOC-HYD-04"
        )
        self.assertFalse(huge_transfer["success"])
        self.assertIn("Insufficient stock", huge_transfer["error"])

    # -------------------------------------------------------------------------
    # Test 8: Canonical Asbab-e-Sittah Seasonal Humoral Surveillance (4 Seasons)
    # -------------------------------------------------------------------------
    def test_08_canonical_seasonal_humoral_surveillance(self):
        seasons = [
            CanonicalSeason.MAUSIM_E_BAHAR,
            CanonicalSeason.MAUSIM_E_SAIF,
            CanonicalSeason.MAUSIM_E_KHAZAN,
            CanonicalSeason.MAUSIM_E_SHITA,
        ]

        for s in seasons:
            adv = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=s)
            self.assertTrue(adv.season == s or adv.season == s.value)
            self.assertTrue(len(adv.thermal_dynamic) > 0)
            self.assertTrue(len(adv.predominant_vulnerable_humor) > 0)
            self.assertTrue(len(adv.high_risk_amraz) >= 2)
            self.assertTrue(len(adv.asbab_sitta_guidance) >= 2)
            self.assertTrue(len(adv.lifestyle_and_parhez_recommendations) >= 2)

        # Verify specific classic humoral correspondences
        bahar_adv = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=CanonicalSeason.MAUSIM_E_BAHAR)
        self.assertIn("Dam", bahar_adv.predominant_vulnerable_humor)

        saif_adv = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=CanonicalSeason.MAUSIM_E_SAIF)
        self.assertIn("Safra", saif_adv.predominant_vulnerable_humor)

        khazan_adv = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=CanonicalSeason.MAUSIM_E_KHAZAN)
        self.assertIn("Sawda", khazan_adv.predominant_vulnerable_humor)

        shita_adv = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=CanonicalSeason.MAUSIM_E_SHITA)
        self.assertIn("Balgham", shita_adv.predominant_vulnerable_humor)

    # -------------------------------------------------------------------------
    # Test 9: Humoral Epidemiology Distribution
    # -------------------------------------------------------------------------
    def test_09_humoral_epidemiology_distribution(self):
        # Overall distribution across all federated clinics
        dist = PopulationHealthEngine.get_humoral_epidemiology_distribution()
        self.assertIn("cohort_size", dist)
        self.assertGreaterEqual(dist["cohort_size"], 1000)
        self.assertIn("humor_distribution_percentage", dist)

        humors = dist["humor_distribution_percentage"]
        for h in ["Balgham (Phlegm)", "Safra (Yellow Bile)", "Dam (Blood)", "Sawda (Black Bile)"]:
            self.assertIn(h, humors)

        total_pct = sum(humors.values())
        self.assertAlmostEqual(total_pct, 100.0, delta=0.5)

        # Facility specific filter
        delhi_dist = PopulationHealthEngine.get_humoral_epidemiology_distribution(facility_id="FAC-DEL-CENTRAL-01")
        self.assertEqual(delhi_dist["facility_id"], "FAC-DEL-CENTRAL-01")

    # -------------------------------------------------------------------------
    # Test 10: Multi-Clinic Pharmacovigilance Cluster Detection
    # -------------------------------------------------------------------------
    def test_10_multi_clinic_pharmacovigilance_cluster_detection(self):
        clusters = PopulationHealthEngine.scan_adr_clusters(cluster_threshold=2)
        self.assertGreaterEqual(len(clusters), 1, "Must detect seeded multi-clinic ADR cluster for Suranjan Talkh")

        c = clusters[0]
        self.assertEqual(c.suspected_drug, "Suranjan Talkh")
        self.assertEqual(c.lot_batch_number, "B-SURT-2026-X1")
        self.assertGreaterEqual(c.reported_cases_count, 2)
        self.assertEqual(c.alert_level, "CRITICAL_SAFETY_HOLD")
        self.assertIn("quarantine", c.recommended_action.lower())
        self.assertGreaterEqual(len(c.participating_facilities), 2)

    # -------------------------------------------------------------------------
    # Test 11: Live REST API Endpoints Integration (Sequences 14–16)
    # -------------------------------------------------------------------------
    def test_11_live_api_server_endpoints_integration(self):
        # 1. GET /api/v1/clinical/continuum/federation/clinics
        clinics_res = _call_get("/api/v1/clinical/continuum/federation/clinics")
        self.assertTrue(clinics_res.get("ok"))
        self.assertGreaterEqual(clinics_res.get("total_facilities", 0), 4)

        # 2. POST /api/v1/clinical/continuum/federation/referral
        ref_payload = {
            "patient_id": "PAT-REST-999",
            "source_facility_id": "FAC-DEL-CENTRAL-01",
            "target_facility_id": "FAC-LKO-REGIONAL-03",
            "referring_clinician_id": "DOC-REST-01",
            "clinical_condition": "Irq-un-Nasa",
            "specialty_axis_required": "Neurological & Cognitive Axis",
            "reason_for_referral": "Specialized Fasd and Roghan therapy",
            "validity_days": 10
        }
        ref_res = _call_post("/api/v1/clinical/continuum/federation/referral", ref_payload)
        self.assertTrue(ref_res.get("ok"))
        token = ref_res["referral"]["referral_token"]
        self.assertTrue(token.startswith("ZAY-REF-"))

        # 3. POST /api/v1/clinical/continuum/federation/referral/redeem
        redeem_payload = {
            "referral_token": token,
            "receiving_facility_id": "FAC-LKO-REGIONAL-03",
            "accepting_clinician_id": "DOC-LKO-02"
        }
        redeem_res = _call_post("/api/v1/clinical/continuum/federation/referral/redeem", redeem_payload)
        self.assertTrue(redeem_res.get("ok"))
        self.assertEqual(redeem_res["redemption"]["status"], "REDEEMED")

        # 4. GET /api/v1/clinical/continuum/population-health/seasonal-alerts
        alerts_res = _call_get("/api/v1/clinical/continuum/population-health/seasonal-alerts?season=MAUSIM_E_BAHAR")
        self.assertTrue(alerts_res.get("ok"))
        self.assertEqual(alerts_res["advisory"]["season"], "MAUSIM_E_BAHAR")

        # 5. GET /api/v1/clinical/continuum/population-health/epidemiology
        epi_res = _call_get("/api/v1/clinical/continuum/population-health/epidemiology")
        self.assertTrue(epi_res.get("ok"))
        self.assertIn("humor_distribution_percentage", epi_res.get("epidemiology", {}))

        # 6. GET /api/v1/clinical/continuum/population-health/adr-clusters
        clusters_res = _call_get("/api/v1/clinical/continuum/population-health/adr-clusters")
        self.assertTrue(clusters_res.get("ok"))
        self.assertGreaterEqual(clusters_res.get("count", 0), 1)

        # 7. POST /api/v1/clinical/continuum/fhir-bundle/op-consult
        bundle_res = _call_post("/api/v1/clinical/continuum/fhir-bundle/op-consult", {"continuum_response": self.c_dict})
        self.assertTrue(bundle_res.get("ok"))
        self.assertEqual(bundle_res.get("abdm_profile"), "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord")
        self.assertEqual(bundle_res["fhir_bundle"]["resourceType"], "Bundle")

        # 8. POST /api/v1/clinical/continuum/fhir-bundle/prescription
        rx_bundle_res = _call_post("/api/v1/clinical/continuum/fhir-bundle/prescription", {"continuum_response": self.c_dict})
        self.assertTrue(rx_bundle_res.get("ok"))
        self.assertEqual(rx_bundle_res.get("abdm_profile"), "https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord")
        self.assertEqual(rx_bundle_res["fhir_bundle"]["resourceType"], "Bundle")


if __name__ == "__main__":
    unittest.main(verbosity=2)
