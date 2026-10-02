#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — Computational Formulation Intelligence Test Suite
Governed Scientific Intelligence Layer (Blueprint §98 Build Priorities 1–10)

Verifies:
1. Canonical Identity Standards (ZAY-MUF-XXXX, ZAY-CMP-XXXX, ZAY-TGT-XXXX, ZAY-PW-XXXX)
2. Formulation Digital Twin & Semantic Formula Versioning (v1.1 vs Batch)
3. Hierarchical Evidence Bridge (E0 to E6 Multidimensional Matrix)
4. Provenance & License Registry (ChEMBL, Reactome, Open Targets, UPI)
5. Multi-Scale Mapping (Constituents -> Compounds -> Targets -> Pathways -> Organ-Axis)
6. Synergy Analysis & Classical Musleh Toxicity Mitigation Principle
7. Independent Safety Engine (PASS, CAUTION, BLOCK, UNKNOWN)
8. Scientific Memory™ & Contradiction Engine (Negative Knowledge)
9. Shadow-Mode Clinical Advisory & Statutory Notice Invariant
10. Live REST API Dispatch & Endpoints
"""

import io
import json
import os
import sys
import unittest
import base64
import hmac as _hmac
import hashlib as _hashlib
import time as _time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
ai_service_path = os.path.join(BASE_DIR, "services", "ai")
if ai_service_path not in sys.path:
    sys.path.insert(0, ai_service_path)

from services.knowledge.app.core.canonical_identity_service import (
    CanonicalIdentityRegistry,
    CanonicalSubstanceRecord,
    CanonicalCompoundRecord,
    CanonicalTargetRecord,
    CanonicalPathwayRecord,
    EntityType
)
from services.therapeutic.app.models.computational_twin import (
    FormulationDigitalTwin,
    FormulationTwinRegistry,
    BatchManufacturingTwin,
    ConstituentRole,
    QualityStatus
)
from services.knowledge.app.engines.evidence_bridge import (
    EvidenceBridgeEngine,
    EvidenceLevel,
    ReplicabilityStatus
)
from services.knowledge.app.engines.provenance_registry import (
    ProvenanceLicenseRegistry,
    LicenseType
)
from services.therapeutic.app.engines.formulation_intelligence_engine import (
    FormulationIntelligenceEngine,
    ScientificMemoryRegistry,
    SafetyVerdict
)
from services.ai.app.agentic.formulation_shadow_orchestrator import FormulationShadowOrchestrator
from services.clinical.app.engines.formulation_outcomes_closed_loop import (
    FormulationOutcomesClosedLoopEngine,
    TrajectoryVelocity
)
from services.knowledge.app.engines.regulatory_dossier_generator import ScientificRegulatoryDossierGenerator
from services.knowledge.app.engines.insilico_docking_bridge import (
    in_silico_docking_bridge,
    ADMETRiskLevel
)
from services.therapeutic.app.engines.lims_batch_ingestion_engine import (
    lims_batch_ingestion_engine,
    CertificateOfAnalysisPayload,
    BatchReleaseStatus
)
from services.clinical.app.engines.pharmacogenomics_mizaj_engine import (
    pharmacogenomics_mizaj_engine
)
from services.live_api_server import ZayvoraApiHandler


class MockSocket:
    def __init__(self, request_bytes):
        self.rfile = io.BytesIO(request_bytes)
        self.wfile = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, b):
        self.wfile.write(b)


def dispatch_request(method="GET", path="/", body=None, extra_headers=None):
    headers = {"Host": "localhost:8088"}
    if extra_headers:
        headers.update(extra_headers)
    body_bytes = b""
    if body is not None:
        body_bytes = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body_bytes))
    lines = [f"{method} {path} HTTP/1.1"] + [f"{k}: {v}" for k, v in headers.items()] + ["", ""]
    raw_req = "\r\n".join(lines).encode("latin1") + body_bytes
    sock = MockSocket(raw_req)
    ZayvoraApiHandler(sock, ("127.0.0.1", 8088), None)
    raw_resp = sock.wfile.getvalue().decode("utf-8", errors="replace")
    header_part, _, body_part = raw_resp.partition("\r\n\r\n")
    status_code = int(header_part.splitlines()[0].split()[1])
    try:
        body_data = json.loads(body_part) if body_part else {}
    except Exception:
        body_data = {"raw_text": body_part}
    return status_code, body_data


def make_test_token(role="DOCTOR", uid="TEST-LAB-DIRECTOR-001", fac="FAC-HQ-01"):
    """Generates a valid zyv. session token for test dispatch requests."""
    JWT_SECRET = "zayvora-dev-rotated-hmac-secret-pilot-candidate-2026-64bit-minimum"
    payload = {
        "uid": uid,
        "email": "lab-director@zayvora.com",
        "name": "Test Lab Director",
        "role": role,
        "fac": fac,
        "mrn": None,
        "exp": int(_time.time()) + 3600
    }
    b64_payload = base64.urlsafe_b64encode(
        json.dumps(payload).encode()
    ).rstrip(b"=").decode()
    sig = _hmac.new(JWT_SECRET.encode(), b64_payload.encode(), _hashlib.sha256).hexdigest()
    return f"zyv.{b64_payload}.{sig}"


class TestComputationalFormulationIntelligence(unittest.TestCase):
    """Full blueprint test coverage for governed computational formulation intelligence."""

    def test_01_canonical_identity_standards(self):
        """Verifies identifier schema (ZAY-MUF, ZAY-CMP, ZAY-TGT, ZAY-PW) and synonym lookup."""
        sub = CanonicalIdentityRegistry.get_substance("ZAY-MUF-0001")
        self.assertIsNotNone(sub)
        self.assertEqual(sub.unani_name, "Suranjan Shirin")
        self.assertTrue(sub.canonical_id.startswith("ZAY-MUF-"))
        self.assertTrue(len(sub.hash_signature) == 64)

        # Synonym resolution
        resolved = CanonicalIdentityRegistry.resolve_identifier("hermodactylus")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved["entity_type"], EntityType.MUFRAD.value)
        self.assertEqual(resolved["record"]["canonical_id"], "ZAY-MUF-0001")

        # Compound resolution
        cmp_rec = CanonicalIdentityRegistry.get_compound("ZAY-CMP-0001")
        self.assertIsNotNone(cmp_rec)
        self.assertEqual(cmp_rec.compound_name, "Colchicine")
        self.assertEqual(cmp_rec.pubchem_cid, 6167)
        self.assertEqual(cmp_rec.chembl_id, "CHEMBL84")

    def test_02_formulation_digital_twin_and_batch_distinction(self):
        """Verifies twin models, formula semantic versioning vs manufacturing batch distinction."""
        twin = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        self.assertIsNotNone(twin)
        self.assertEqual(twin.canonical_name, "Majun Suranjan")
        self.assertEqual(twin.formula_version, "v1.1")
        self.assertTrue(len(twin.constituents) >= 3)

        # Batch distinction
        batches = FormulationTwinRegistry.list_batches_for_formulation("ZAY-FORM-0001")
        self.assertTrue(len(batches) >= 2)
        batch = batches[0]
        self.assertEqual(batch["formulation_id"], "ZAY-FORM-0001")
        self.assertEqual(batch["quality_status"], QualityStatus.CERTIFIED.value)
        self.assertIn("ZAY-CMP-0001", batch["assayed_markers"])

        # Formula versioning is NOT a batch
        self.assertNotEqual(twin.formula_version, batch["batch_id"])

    def test_03_hierarchical_evidence_bridge_e0_to_e6(self):
        """Verifies E0 to E6 hierarchical evidence model and multidimensional matrix."""
        items = EvidenceBridgeEngine.get_evidence_for_entity("ZAY-FORM-0001")
        self.assertTrue(len(items) >= 1)
        highest = EvidenceBridgeEngine.get_highest_evidence_level("ZAY-FORM-0001")
        self.assertEqual(highest, EvidenceLevel.E6_CONTROLLED_CLINICAL)

        # Verify in-silico hypothesis is graded E0
        e0_items = [it for it in EvidenceBridgeEngine.get_evidence_for_entity("ZAY-CMP-0005") if it["evidence_level"] == "E0"]
        self.assertTrue(len(e0_items) >= 1)
        self.assertEqual(e0_items[0]["replicability_status"], ReplicabilityStatus.UNTESTED.value)

    def test_04_provenance_and_license_registry(self):
        """Verifies provenance tracking, external biological databases, and open source licenses."""
        sources = ProvenanceLicenseRegistry.list_sources()
        self.assertTrue(len(sources) >= 5)
        chembl = ProvenanceLicenseRegistry.get_source("SRC-CHEMBL")
        self.assertIsNotNone(chembl)
        self.assertEqual(chembl.license_type, LicenseType.CC_BY_SA_3_0)
        self.assertTrue(chembl.commercial_use_allowed)
        self.assertIn("ChEMBL", chembl.mandatory_attribution)

    def test_05_multiscale_mapping_engine(self):
        """Verifies multi-scale mapping: Botanical -> Phytochemical -> Target -> Pathway -> Organ-Axis."""
        summary = FormulationIntelligenceEngine.get_formulation_intelligence_summary("ZAY-FORM-0001")
        self.assertIsNotNone(summary)
        self.assertEqual(summary["primary_organ_axis"], "mafasil")
        self.assertTrue(len(summary["active_compounds"]) >= 3)
        self.assertTrue(len(summary["targets"]) >= 3)
        self.assertTrue(len(summary["pathways"]) >= 3)

        # Verify tubulin and inflammasome targets are linked
        gene_symbols = [t["gene_symbol"] for t in summary["targets"]]
        self.assertIn("TUBA1A", gene_symbols)
        self.assertIn("NLRP3", gene_symbols)

    def test_06_synergy_and_musleh_toxicity_mitigation(self):
        """Verifies synergy analysis and classical Musleh principle."""
        summary = FormulationIntelligenceEngine.get_formulation_intelligence_summary("ZAY-FORM-0001")
        self.assertTrue(len(summary["synergy_pairs"]) >= 1)
        pair = summary["synergy_pairs"][0]
        self.assertIn("Colchicine", pair["compound_a"])
        self.assertIn("6-Gingerol", pair["compound_b"])
        self.assertIn("Musleh", pair["synergy_type"])

    def test_07_independent_safety_engine_verdicts(self):
        """Verifies independent safety engine: PASS, CAUTION, BLOCK verdicts."""
        # 1. Normal safe patient -> PASS
        res_pass = FormulationIntelligenceEngine.evaluate_independent_safety(
            "ZAY-FORM-0001",
            {"egfr": 95, "alt_u_l": 25, "is_pregnant": False}
        )
        self.assertEqual(res_pass.verdict, SafetyVerdict.PASS)
        self.assertTrue(res_pass.safety_score > 0.9)

        # 2. Severe renal impairment (eGFR < 30) -> BLOCK
        res_renal = FormulationIntelligenceEngine.evaluate_independent_safety(
            "ZAY-FORM-0001",
            {"egfr": 24, "alt_u_l": 25}
        )
        self.assertEqual(res_renal.verdict, SafetyVerdict.BLOCK)
        self.assertFalse(res_renal.organ_clearance_ok)

        # 3. Pregnancy with Schedule E1 formulation -> BLOCK
        res_preg = FormulationIntelligenceEngine.evaluate_independent_safety(
            "ZAY-FORM-0001",
            {"egfr": 90, "is_pregnant": True}
        )
        self.assertEqual(res_preg.verdict, SafetyVerdict.BLOCK)

        # 4. Concurrent potent CYP3A4 inhibitor -> BLOCK
        res_cyp = FormulationIntelligenceEngine.evaluate_independent_safety(
            "ZAY-FORM-0001",
            {"egfr": 90, "current_medications": ["clarithromycin"]}
        )
        self.assertEqual(res_cyp.verdict, SafetyVerdict.BLOCK)

    def test_08_scientific_memory_and_contradiction_engine(self):
        """Verifies Scientific Memory negative knowledge and contradiction detection."""
        contradictions = ScientificMemoryRegistry.list_contradictions()
        self.assertTrue(len(contradictions) >= 3)
        matches = ScientificMemoryRegistry.check_for_contradictions("Suranjan Shirin")
        self.assertTrue(len(matches) >= 1)
        self.assertIn("Mudabbar", matches[0]["claim_refuted"])

    def test_09_shadow_mode_orchestrator_invariants(self):
        """Verifies shadow-mode decision support, statutory notice, and non-autonomous prescribing."""
        insight = FormulationShadowOrchestrator.analyze_prescription_candidate(
            "ZAY-FORM-0001",
            {"egfr": 90}
        )
        self.assertIsNotNone(insight)
        self.assertIn("ZAYVORA SCIENTIFIC NOTICE", insight.statutory_caveat)
        self.assertIn("CLEARED", insight.clinician_action_summary)
        self.assertTrue(len(insight.molecular_mechanisms) >= 2)

    def test_10_live_api_endpoints_dispatch(self):
        """Verifies all GET and POST computational endpoints over HTTP dispatch."""
        # GET substances
        status, res = dispatch_request("GET", "/api/v1/computational/substances")
        self.assertEqual(status, 200)
        self.assertTrue(res["ok"])
        self.assertTrue(res["count"] >= 5)

        # GET single substance
        status, res = dispatch_request("GET", "/api/v1/computational/substances/ZAY-MUF-0001")
        self.assertEqual(status, 200)
        self.assertEqual(res["substance"]["canonical_id"], "ZAY-MUF-0001")

        # GET formulations
        status, res = dispatch_request("GET", "/api/v1/computational/formulations")
        self.assertEqual(status, 200)
        self.assertTrue(res["count"] >= 2)

        # GET single formulation intelligence summary
        status, res = dispatch_request("GET", "/api/v1/computational/formulations/ZAY-FORM-0001")
        self.assertEqual(status, 200)
        self.assertEqual(res["intelligence_summary"]["canonical_name"], "Majun Suranjan")

        # GET batches
        status, res = dispatch_request("GET", "/api/v1/computational/batches/ZAY-BATCH-2026-001")
        self.assertEqual(status, 200)
        self.assertEqual(res["batch"]["lot_number"], "MS-2026-LOT5")

        # GET evidence matrix
        status, res = dispatch_request("GET", "/api/v1/computational/evidence-matrix/ZAY-FORM-0001")
        self.assertEqual(status, 200)
        self.assertEqual(res["highest_level"], "E6")

        # GET contradictions
        status, res = dispatch_request("GET", "/api/v1/computational/contradictions")
        self.assertEqual(status, 200)
        self.assertTrue(res["count"] >= 3)

        # GET provenance
        status, res = dispatch_request("GET", "/api/v1/computational/provenance")
        self.assertEqual(status, 200)
        self.assertTrue(res["count"] >= 6)

        # POST safety-eval
        status, res = dispatch_request("POST", "/api/v1/computational/safety-eval", {
            "formulation_id": "ZAY-FORM-0001",
            "patient_context": {"egfr": 95}
        })
        self.assertEqual(status, 200)
        self.assertEqual(res["safety_evaluation"]["verdict"], "PASS")

        # POST shadow-consult
        status, res = dispatch_request("POST", "/api/v1/computational/shadow-consult", {
            "formulation_id": "ZAY-FORM-0001",
            "patient_context": {"egfr": 95}
        })
        self.assertEqual(status, 200)
        self.assertIn("CLEARED", res["shadow_insight"]["clinician_action_summary"])

        # GET outcomes-closed-loop
        status, res = dispatch_request("GET", "/api/v1/computational/outcomes-closed-loop")
        self.assertEqual(status, 200)
        self.assertTrue(res["ok"])
        self.assertTrue(res["count"] >= 1)

        # POST outcomes-closed-loop
        status, res = dispatch_request("POST", "/api/v1/computational/outcomes-closed-loop", {
            "patient_id": "PAT-774901",
            "prescription_id": "RX-2026-TEST",
            "formulation_id": "ZAY-FORM-0001",
            "batch_id": "ZAY-BATCH-2026-001",
            "baseline_markers": {"hs-CRP": 9.0, "ESR": 40.0},
            "current_markers": {"hs-CRP": 4.5, "ESR": 20.0},
            "vas_baseline": 8.0,
            "vas_current": 3.0,
            "stiffness_baseline_min": 90,
            "stiffness_current_min": 25,
            "day": 21
        })
        self.assertEqual(status, 201)
        self.assertEqual(res["record"]["trajectory_velocity"], "RAPID_RESPONDER")

        # GET dossier JSON
        status, res = dispatch_request("GET", "/api/v1/computational/dossier/ZAY-FORM-0001")
        self.assertEqual(status, 200)
        self.assertIn("DOSSIER-ZAY-FORM-0001", res["dossier"]["dossier_id"])

        # GET dossier Markdown
        status, res = dispatch_request("GET", "/api/v1/computational/dossier/ZAY-FORM-0001?format=markdown")
        self.assertEqual(status, 200)
        self.assertIn("SCIENTIFIC & REGULATORY DOSSIER", res.get("raw_text", ""))

        # GET dossier HTML
        status, res = dispatch_request("GET", "/api/v1/computational/dossier/ZAY-FORM-0001?format=html")
        self.assertEqual(status, 200)
        self.assertIn("<html", res.get("raw_text", ""))

    def test_11_hero_formulation_twins_ecosystem(self):
        """Verifies all 5 hero formulation digital twins (Majun Suranjan, Glucovora, LiverPrime, Cardiovora, Neurovora)."""
        twins = FormulationTwinRegistry.list_twins()
        self.assertEqual(len(twins), 5)
        twin_ids = [t["formulation_id"] for t in twins]
        self.assertIn("ZAY-FORM-0001", twin_ids) # Majun Suranjan
        self.assertIn("ZAY-FORM-0002", twin_ids) # Glucovora
        self.assertIn("ZAY-FORM-0003", twin_ids) # LiverPrime
        self.assertIn("ZAY-FORM-0004", twin_ids) # Cardiovora
        self.assertIn("ZAY-FORM-0005", twin_ids) # Neurovora

        # Verify Majun Suranjan has Schedule E1 Suranjan with verified Mudabbar
        ms = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        self.assertIsNotNone(ms)
        suranjan_const = [c for c in ms.constituents if c.substance_id == "ZAY-MUF-0001"][0]
        self.assertTrue(suranjan_const.is_schedule_e1)
        self.assertTrue(suranjan_const.mudabbar_verified)

        # Verify LiverPrime twin has Kasni, Revand Chini, Gaozaban
        lp = FormulationTwinRegistry.get_twin("ZAY-FORM-0003")
        self.assertIsNotNone(lp)
        self.assertEqual(lp.canonical_name, "LiverPrime Core")
        self.assertTrue(len(lp.constituents) >= 3)
        lp_substances = [c.substance_id for c in lp.constituents]
        self.assertIn("ZAY-MUF-0005", lp_substances) # Kasni
        self.assertIn("ZAY-MUF-0006", lp_substances) # Revand Chini

        # Verify Cardiovora twin has NOS3 and ACE targets
        cv = FormulationTwinRegistry.get_twin("ZAY-FORM-0004")
        self.assertIsNotNone(cv)
        self.assertEqual(cv.canonical_name, "Cardiovora Core")
        self.assertIn("ZAY-TGT-0012", cv.resolved_targets) # NOS3
        self.assertIn("ZAY-TGT-0013", cv.resolved_targets) # ACE

        # Verify Neurovora twin has ACHE and BDNF targets
        nv = FormulationTwinRegistry.get_twin("ZAY-FORM-0005")
        self.assertIsNotNone(nv)
        self.assertEqual(nv.canonical_name, "Neurovora Core")
        self.assertIn("ZAY-TGT-0014", nv.resolved_targets) # ACHE
        self.assertIn("ZAY-TGT-0016", nv.resolved_targets) # BDNF

    def test_12_biomarker_closed_loop_feedback_engine(self):
        """Verifies longitudinal biomarker trajectory feedback, RWE concordance, and batch reverse-correlation."""
        record = FormulationOutcomesClosedLoopEngine.evaluate_patient_trajectory(
            patient_id="PAT-774901",
            prescription_id="RX-2026-0441",
            formulation_id="ZAY-FORM-0001",
            batch_id="ZAY-BATCH-2026-001",
            baseline_markers={"hs-CRP": 8.4, "ESR": 38.0, "Serum Uric Acid": 7.2},
            current_markers={"hs-CRP": 4.8, "ESR": 22.0, "Serum Uric Acid": 5.4},
            vas_baseline=7.0,
            vas_current=3.0,
            stiffness_baseline_min=75,
            stiffness_current_min=20,
            day=21,
            clinician_notes="Marked knee flexion restoration."
        )
        self.assertIsNotNone(record)
        self.assertEqual(record.trajectory_velocity, TrajectoryVelocity.RAPID_RESPONDER)
        self.assertGreaterEqual(record.rwe_concordance_index, 0.90)
        self.assertEqual(record.morning_stiffness_reduction_min, 55)
        self.assertTrue(len(record.biomarker_deltas) >= 3)
        self.assertTrue(all(d.direction_beneficial for d in record.biomarker_deltas))
        self.assertTrue(len(record.tamper_proof_seal) == 64) # SHA256

        # Query patient outcome
        out = FormulationOutcomesClosedLoopEngine.get_outcome_for_patient("PAT-774901", "ZAY-FORM-0001")
        self.assertIsNotNone(out)
        self.assertEqual(out["lot_number"], "MS-2026-LOT5")

    def test_13_scientific_regulatory_dossier_generator(self):
        """Verifies exportable ICH CTD / AYUSH regulatory dossier compilation across all 5 modules."""
        dossier = ScientificRegulatoryDossierGenerator.generate_dossier("ZAY-FORM-0001")
        self.assertIsNotNone(dossier)
        self.assertEqual(dossier["schema_version"], "ICH-CTD-AYUSH-v1.0")
        self.assertTrue(len(dossier["cryptographic_integrity_hash"]) == 64)

        # Module 1
        m1 = dossier["module_1_administrative"]
        self.assertIn("Majun Suranjan", m1["formulation_name"])
        self.assertIn("ASU Drugs Rule 158-B", m1["regulatory_category"])

        # Module 2
        m2 = dossier["module_2_quality_summary"]
        self.assertTrue(len(m2["botanical_composition"]) >= 3)
        self.assertTrue(len(m2["phytochemical_markers"]) >= 3)

        # Module 3
        m3 = dossier["module_3_quality_manufacturing"]
        self.assertTrue(len(m3["manufacturing_batches"]) >= 2)
        self.assertIn("heavy_metals_limits", m3["specification_standards"])

        # Module 4
        m4 = dossier["module_4_nonclinical_mechanisms"]
        self.assertTrue(len(m4["target_mapping"]) >= 2)
        self.assertTrue(len(m4["pathway_mapping"]) >= 2)

        # Module 5
        m5 = dossier["module_5_clinical_rwe"]
        self.assertTrue(m5["evidence_matrix_e0_to_e6"]["total_claims"] >= 1)
        self.assertTrue(len(m5["closed_loop_patient_outcomes"]) >= 1)

        # Export formats verification
        md_text = ScientificRegulatoryDossierGenerator.export_markdown("ZAY-FORM-0001")
        self.assertIn("# SCIENTIFIC & REGULATORY DOSSIER", md_text)
        self.assertIn("Module 1:", md_text)

        html_text = ScientificRegulatoryDossierGenerator.export_html("ZAY-FORM-0001")
        self.assertIn("<!DOCTYPE html>", html_text)
        self.assertIn("ZAYVORA HEALTH OS™ — SCIENTIFIC REGULATORY DOSSIER", html_text)

        json_ld = ScientificRegulatoryDossierGenerator.export_json_ld("ZAY-FORM-0001")
        self.assertIn('"@type": "Drug"', json_ld)
        self.assertIn("Majun Suranjan", json_ld)

    def test_14_insilico_molecular_docking_and_admet_bridge(self):
        """Verifies in-silico binding affinities, Ki calculations, and ADMET profiles."""
        # Colchicine docking
        poses = in_silico_docking_bridge.get_docking_poses("ZAY-CMP-0001")
        self.assertTrue(len(poses) >= 2)
        tubulin_pose = next(p for p in poses if p["target_gene"] == "TUBA1A")
        self.assertAlmostEqual(tubulin_pose["binding_energy_kcal_mol"], -9.4, delta=0.2)
        self.assertEqual(tubulin_pose["evidence_level"], "E0")

        # ADMET profile
        admet = in_silico_docking_bridge.get_admet_profile("ZAY-CMP-0001")
        self.assertIsNotNone(admet)
        self.assertEqual(admet["lipinski_rule_of_5_violations"], 0)
        self.assertFalse(admet["blood_brain_barrier_permeable"])
        self.assertEqual(admet["herg_inhibition_risk"], ADMETRiskLevel.LOW)

        # Polyherbal evaluation
        poly = in_silico_docking_bridge.evaluate_polyherbal_docking_profile(["ZAY-CMP-0001", "ZAY-CMP-0002"])
        self.assertEqual(poly["compounds_evaluated"], 2)
        self.assertIn("TUBA1A", poly["unique_targets_docked"])
        self.assertIn("ABCB1", poly["unique_targets_docked"])
        self.assertTrue(poly["mean_binding_energy_kcal_mol"] < -7.0)

        # Live API dispatch
        status, res = dispatch_request("GET", "/api/v1/computational/docking/ZAY-CMP-0001")
        self.assertEqual(status, 200)
        self.assertTrue(res["ok"])
        self.assertEqual(res["compound_id"], "ZAY-CMP-0001")
        self.assertTrue(len(res["poses"]) >= 2)

    def test_15_lims_batch_coa_ingestion_and_quality_gate(self):
        """Verifies LIMS Certificate of Analysis (CoA) verification, heavy metal screening, and release seal."""
        # 1. Standard Compliant Batch -> PASSED_RELEASED
        valid_coa = CertificateOfAnalysisPayload(
            batch_number="ZAY-BATCH-2026-TEST1",
            formulation_canonical_id="ZAY-FORM-0001",
            manufacturing_date="2026-09-01",
            expiry_date="2029-08-31",
            testing_lab_name="AYUSH Central Drug Testing Laboratory",
            testing_lab_accreditation="NABL ISO/IEC 17025",
            active_marker_name="Colchicine",
            active_marker_assay_pct=0.21,
            active_marker_min_pct=0.18,
            active_marker_max_pct=0.25,
            heavy_metals={"pb": 1.2, "cd": 0.05, "as": 0.8, "hg": 0.08},
            microbial_load={"tamc": 1500, "tymc": 120, "e_coli": False, "salmonella": False},
            physical_chemistry={"lod_pct": 5.4, "total_ash_pct": 4.1}
        )
        rep_valid = lims_batch_ingestion_engine.verify_and_ingest_coa(valid_coa)
        self.assertEqual(rep_valid.release_status, BatchReleaseStatus.PASSED_RELEASED)
        self.assertEqual(rep_valid.assay_status, "WITHIN_SPEC")
        self.assertEqual(rep_valid.metals_status, "PASSED")
        self.assertEqual(rep_valid.microbial_status, "PASSED")
        self.assertTrue(rep_valid.cryptographic_release_seal.startswith("ZAY-SEAL-"))

        # 2. Heavy Metal Out-of-Spec -> REJECTED_OUT_OF_SPEC
        toxic_coa = CertificateOfAnalysisPayload(
            batch_number="ZAY-BATCH-2026-FAIL1",
            formulation_canonical_id="ZAY-FORM-0001",
            manufacturing_date="2026-09-01",
            expiry_date="2029-08-31",
            testing_lab_name="Third-party Lab",
            testing_lab_accreditation="ISO 17025",
            active_marker_name="Colchicine",
            active_marker_assay_pct=0.22,
            active_marker_min_pct=0.18,
            active_marker_max_pct=0.25,
            heavy_metals={"pb": 18.5, "cd": 0.05, "as": 0.8, "hg": 0.08}, # Pb > 10.0 ppm limit!
            microbial_load={"tamc": 1000, "tymc": 50, "e_coli": False, "salmonella": False},
            physical_chemistry={"lod_pct": 5.0, "total_ash_pct": 4.0}
        )
        rep_fail = lims_batch_ingestion_engine.verify_and_ingest_coa(toxic_coa)
        self.assertEqual(rep_fail.release_status, BatchReleaseStatus.REJECTED_OUT_OF_SPEC)
        self.assertEqual(rep_fail.metals_status, "EXCEEDED_LIMIT")
        self.assertTrue(rep_fail.cryptographic_release_seal.startswith("QUARANTINE-"))

        # Live API dispatch
        lims_token = make_test_token(role="PHARMACIST")
        status, res = dispatch_request(
            "POST",
            "/api/v1/computational/lims/verify-batch",
            valid_coa.to_dict(),
            extra_headers={"Authorization": f"Bearer {lims_token}"}
        )
        self.assertEqual(status, 200)
        self.assertTrue(res["ok"])
        self.assertEqual(res["report"]["release_status"], "PASSED_RELEASED")

    def test_16_pharmacogenomics_and_mizaj_stratification(self):
        """Verifies Mizaj-to-Pharmacogenomics stratification, CYP450 mapping, and dose titration."""
        # 1. Safrawi patient (Rapid metabolizer / elevated inflammation)
        strat_safrawi = pharmacogenomics_mizaj_engine.stratify_patient("Safrawi Damawi", "ZAY-FORM-0001")
        self.assertIsNotNone(strat_safrawi)
        prof_s = strat_safrawi["pharmacogenomic_profile"]
        self.assertIn("Rapid Metabolizer", prof_s["primary_cyp_phenotype"])
        self.assertEqual(strat_safrawi["recommended_dose_multiplier"], 0.85)

        # 2. Balghami patient (Slow metabolizer / lymph stasis)
        strat_balghami = pharmacogenomics_mizaj_engine.stratify_patient("Balghami", "ZAY-FORM-0001")
        prof_b = strat_balghami["pharmacogenomic_profile"]
        self.assertIn("Slow Metabolizer", prof_b["primary_cyp_phenotype"])
        self.assertEqual(strat_balghami["recommended_dose_multiplier"], 1.10)

        # Live API dispatch
        status, res = dispatch_request("POST", "/api/v1/computational/mizaj-pharmacogenomics/evaluate", {
            "mizaj": "Safrawi",
            "formulation_id": "ZAY-FORM-0001"
        })
        self.assertEqual(status, 200)
        self.assertTrue(res["ok"])
        self.assertEqual(res["stratification"]["recommended_dose_multiplier"], 0.85)


if __name__ == "__main__":
    unittest.main()
