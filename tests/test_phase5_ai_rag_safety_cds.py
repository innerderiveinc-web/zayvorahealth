#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 5 AI ORCHESTRATOR, MULTI-MODEL FAILOVER, HYBRID RAG & CDS TEST SUITE
SUITE-14: Comprehensive Automated Integration Verification Harness

Verifies:
1.  Classical UPI pharmacopoeial monograph catalog retrieval.
2.  Monograph search and organ-axis filtering with Schedule E(1) flags.
3.  Deterministic Safety Firewall: Emergency biomedical red flag referral (REFER).
4.  Deterministic Safety Firewall: Statutory Schedule E(1) unpurified botanical block (DO_NOT_RECOMMEND).
5.  Deterministic Safety Firewall: Drug-Herb interaction detection (Warfarin + Roghan/Allium).
6.  Deterministic Safety Firewall: Pregnancy contraindication hard barrier.
7.  ZAPE 2.0 Posology Scaling: Geriatric age adjustment.
8.  ZAPE 2.0 Posology Scaling: Renal impairment (CKD eGFR) dosage adjustment.
9.  ZAPE 2.0 Posology Scaling: Pediatric Young/Cowling rule adjustment.
10. Master Hakeem Sahab™ 5-Layer AI Copilot structured clinical consultation.
11. Non-delegable clinician review decision barrier (safe_to_lock = False mandatory).
12. Resilient multi-model failover orchestrator & degradation telemetry logging.
13. RBAC Barrier: Non-clinical roles (Patient, Receptionist) blocked from AI consultation (HTTP 403).
14. Multi-Tenancy Barrier: Cross-tenant AI consultation blocked (HTTP 403).
15. 21 CFR Part 11 Merkle audit trail anchoring & zero developer jargon verification.
"""

import sys
import os
import json
import sqlite3
import time
import uuid
from io import BytesIO

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH

PROHIBITED_JARGON = [
    "sqlite", "database error", "traceback", "stack trace", "exception in thread",
    "syntax error", "null pointer", "undefined is not a function", "query failed",
    "operationalerror", "integrityerror", "cursor", "unhandled rejection", "500 internal"
]

class DirectTestClient:
    def request(self, method, path, data=None, headers=None):
        body_bytes = json.dumps(data).encode("utf-8") if data is not None else b""
        
        raw_headers = f"{method} {path} HTTP/1.1\r\n"
        raw_headers += "Host: localhost:8000\r\n"
        raw_headers += "Content-Type: application/json\r\n"
        raw_headers += f"Content-Length: {len(body_bytes)}\r\n"
        
        if headers:
            for k, v in headers.items():
                raw_headers += f"{k}: {v}\r\n"
        raw_headers += "\r\n"
        
        input_stream = BytesIO(raw_headers.encode("utf-8") + body_bytes)
        output_stream = BytesIO()

        class DummySocket:
            def __init__(self, rfile, wfile):
                self.rfile = rfile
                self.wfile = wfile
            def makefile(self, mode, *args, **kwargs):
                if "b" in mode:
                    return self.rfile if "r" in mode else self.wfile
                raise NotImplementedError()
            def sendall(self, b):
                self.wfile.write(b)

        dummy_sock = DummySocket(input_stream, output_stream)
        handler = ZayvoraApiHandler(dummy_sock, ("127.0.0.1", 12345), None)
        
        output_stream.seek(0)
        response_bytes = output_stream.getvalue()
        
        parts = response_bytes.split(b"\r\n\r\n", 1)
        header_lines = parts[0].decode("utf-8").split("\r\n")
        status_line = header_lines[0]
        status_code = int(status_line.split(" ")[1])
        
        resp_body = {}
        if len(parts) > 1 and parts[1]:
            try:
                resp_body = json.loads(parts[1].decode("utf-8"))
            except Exception:
                resp_body = {"raw": parts[1].decode("utf-8")}
            
        return status_code, resp_body

def run_tests():
    print("=" * 76)
    print(" ZAYVORA HEALTH OS™ — PHASE 5 AI ORCHESTRATOR, HYBRID RAG & CDS TEST SUITE")
    print("=" * 76)

    client = DirectTestClient()
    passed = 0
    failed = 0

    # Obtain session tokens for testing
    status, body = client.request("POST", "/api/v1/auth/login", {"email": "mansoor.alam@zayvora.health", "password": "doctor123"})
    doctor_token = body.get("token")
    doctor_headers = {"Authorization": f"Bearer {doctor_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "sirajuddin@zayvora.health", "password": "doctor123"})
    branch_doctor_token = body.get("token")
    branch_doctor_headers = {"Authorization": f"Bearer {branch_doctor_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "reception.opd@zayvora.health", "password": "reception123"})
    rec_token = body.get("token")
    rec_headers = {"Authorization": f"Bearer {rec_token}"}

    # 1. Classical UPI Pharmacopoeial Monograph Retrieval
    try:
        status, body = client.request("GET", "/api/v1/knowledge/monographs", headers=doctor_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert body["ok"] is True
        assert body["count"] >= 5, f"Expected at least 5 monographs, got {body['count']}"
        first_item = body["monographs"][0]
        assert "canonical_name" in first_item
        assert "mizaj" in first_item
        print(f"[PASS] Test 01: Classical UPI Monograph Catalog - Retrieved {body['count']} canonical Unani monographs")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 01: Classical UPI Monograph Catalog ({e})")
        failed += 1

    # 2. Monograph Search & Organ-Axis Filtering with Schedule E(1)
    try:
        status, body = client.request("GET", "/api/v1/knowledge/monographs?search=suranjan&is_schedule_e1=true", headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["count"] >= 1
        suranjan = body["monographs"][0]
        assert "Suranjan" in suranjan["canonical_name"]
        assert suranjan["is_schedule_e1"] is True
        assert "mudabbar_protocol" in suranjan
        print(f"[PASS] Test 02: Monograph Filter & Schedule E(1) Flag - Matched {suranjan['canonical_name']} (Schedule E1: True)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 02: Monograph Filter & Schedule E(1) ({e})")
        failed += 1

    # 3. Deterministic Safety Firewall: Emergency Red Flag Referral (REFER)
    try:
        status, body = client.request("POST", "/api/v1/ai/safety-check", {
            "patient": {
                "age": 58,
                "gender": "Male",
                "chief_complaint": "Crushing substernal chest pain radiating to left arm and jaw with severe sweating",
                "allergies": [],
                "current_medications": []
            },
            "items": [{"name": "Sharbat Bazoori Motadil", "dose_mg": 20.0}]
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["verdict"] == "REFER", f"Expected REFER for chest pain red flag, got {body['verdict']}"
        assert body["isClinicalHold"] is True
        assert body["safeToLock"] is False
        assert any("chest pain" in r.lower() for r in body["reasons"])
        print(f"[PASS] Test 03: Safety Firewall Emergency Red Flag - Verdict REFER: '{body['reasons'][0]}'")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 03: Safety Firewall Emergency Red Flag ({e})")
        failed += 1

    # 4. Deterministic Safety Firewall: Statutory Schedule E(1) Unpurified Block
    try:
        status, body = client.request("POST", "/api/v1/ai/safety-check", {
            "patient": {
                "age": 45,
                "gender": "Female",
                "chief_complaint": "Joint aching",
                "allergies": [],
                "current_medications": []
            },
            "items": [{"name": "Suranjan Talkh", "dose_mg": 200.0, "is_mudabbar": False}]
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["verdict"] in ("DO_NOT_RECOMMEND", "MODIFY")
        assert any("mudabbar" in r.lower() or "schedule e(1)" in r.lower() for r in body["reasons"])
        print(f"[PASS] Test 04: Safety Firewall Unpurified Botanical Block - Verdict {body['verdict']}: Mudabbar protocol mandatory")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 04: Safety Firewall Unpurified Botanical Block ({e})")
        failed += 1

    # 5. Deterministic Safety Firewall: Drug-Herb Interaction Interception
    try:
        status, body = client.request("POST", "/api/v1/ai/safety-check", {
            "patient": {
                "age": 64,
                "gender": "Male",
                "chief_complaint": "General weakness",
                "allergies": [],
                "current_medications": ["Warfarin 5mg daily"]
            },
            "items": [{"name": "Roghan-e-Badam Shirin", "dose_mg": 10.0}]
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["verdict"] in ("CAUTION", "MODIFY", "DO_NOT_RECOMMEND")
        assert any("warfarin" in r.lower() or "inr" in r.lower() or "bleeding" in r.lower() for r in body["reasons"])
        print(f"[PASS] Test 05: Safety Firewall Drug-Herb Interaction - Detected anticoagulant interaction with Warfarin")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 05: Safety Firewall Drug-Herb Interaction ({e})")
        failed += 1

    # 6. Deterministic Safety Firewall: Pregnancy Contraindication Hard Gate
    try:
        status, body = client.request("POST", "/api/v1/ai/safety-check", {
            "patient": {
                "age": 28,
                "gender": "Female",
                "pregnancy_status": "pregnant",
                "chief_complaint": "Dyspepsia",
                "allergies": [],
                "current_medications": []
            },
            "items": [{"name": "Jawarish Kamuni", "dose_mg": 5.0}]
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["verdict"] == "DO_NOT_RECOMMEND"
        assert any("pregnant" in r.lower() for r in body["reasons"])
        print(f"[PASS] Test 06: Safety Firewall Pregnancy Contraindication - Verdict DO_NOT_RECOMMEND for pregnancy")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 06: Safety Firewall Pregnancy Contraindication ({e})")
        failed += 1

    # 7. ZAPE 2.0 Posology Scaling: Geriatric Age Adjustment
    try:
        status, body = client.request("POST", "/api/v1/ai/posology/scale", {
            "age": 72,
            "weight_kg": 65.0,
            "baseDoseMg": 500.0
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["category"] == "Geriatric"
        assert body["scalingFactor"] <= 0.75
        assert body["scaledDoseMg"] == 500.0 * body["scalingFactor"]
        print(f"[PASS] Test 07: ZAPE Geriatric Posology Scaling - Scaled 500mg -> {body['scaledDoseMg']}mg (Factor: {body['scalingFactor']})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 07: ZAPE Geriatric Posology Scaling ({e})")
        failed += 1

    # 8. ZAPE 2.0 Posology Scaling: Renal Impairment (CKD eGFR) Adjustment
    try:
        status, body = client.request("POST", "/api/v1/ai/posology/scale", {
            "age": 68,
            "egfr": 25.0,
            "baseDoseMg": 1000.0
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["scalingFactor"] <= 0.40
        assert body["scaledDoseMg"] == 1000.0 * body["scalingFactor"]
        assert any("ckd" in w.lower() or "renal" in w.lower() for w in body["warnings"])
        print(f"[PASS] Test 08: ZAPE Renal Impairment Staging - Severe CKD (eGFR 25): Factor {body['scalingFactor']} (Scaled: {body['scaledDoseMg']}mg)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 08: ZAPE Renal Impairment Staging ({e})")
        failed += 1

    # 9. ZAPE 2.0 Posology Scaling: Pediatric Young & Cowling Formula
    try:
        status, body = client.request("POST", "/api/v1/ai/posology/scale", {
            "age": 8,
            "baseDoseMg": 500.0
        }, headers=doctor_headers)
        assert status == 200
        assert body["ok"] is True
        assert body["category"] == "Child"
        assert 0.30 <= body["scalingFactor"] <= 0.45
        assert any("pediatric" in w.lower() for w in body["warnings"])
        print(f"[PASS] Test 09: ZAPE Pediatric Young/Cowling Rule - Age 8 Child: Factor {body['scalingFactor']} (Dose: {body['scaledDoseMg']}mg)")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 09: ZAPE Pediatric Young/Cowling Rule ({e})")
        failed += 1

    # 10. Master Hakeem Sahab™ 5-Layer AI Copilot Structured Clinical Consultation
    consult_id = None
    try:
        status, body = client.request("POST", "/api/v1/ai/consult", {
            "mrn": "MRN-2026-0814",
            "chiefComplaint": "Persistent bilateral knee stiffness and dull pain in cold rainy weather",
            "organAxis": "mafasil-asab"
        }, headers=doctor_headers)
        assert status == 201, f"Expected 201, got {status}: {body}"
        assert body["ok"] is True
        consult_id = body["id"]
        assert "layers" in body
        layers = body["layers"]
        assert "layerA_classicalKnowledge" in layers
        assert "layerB_clinicalReasoning" in layers
        assert "layerC_biomedicalIntegration" in layers
        assert "layerD_safetyContraindications" in layers
        assert "layerE_clinicianReviewBarrier" in layers
        assert len(body["parsed_sections"]) >= 10
        print(f"[PASS] Test 10: Master 5-Layer AI Copilot Advisory - Synthesized consult {body['consultationNumber']} with all 5 layers")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 10: Master 5-Layer AI Copilot Advisory ({e})")
        failed += 1

    # 11. Mandatory Clinician Review Non-Delegable Decision Barrier
    try:
        assert body["safeToLock"] is False
        assert body["safe_to_lock"] is False
        assert body["layers"]["layerE_clinicianReviewBarrier"]["safeToLock"] is False
        assert body["layers"]["layerE_clinicianReviewBarrier"]["requiresDoctorReview"] is True
        assert "decision-support" in body["statutoryDisclaimer"].lower() or "clinical governance" in body["statutoryDisclaimer"].lower()
        print(f"[PASS] Test 11: Non-Delegable Clinician Decision Barrier - safe_to_lock = False strictly enforced across response layers")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 11: Non-Delegable Clinician Decision Barrier ({e})")
        failed += 1

    # 12. Chained Failover Orchestrator & Degradation Telemetry
    try:
        status, body = client.request("POST", "/api/v1/ai/consult", {
            "mrn": "MRN-2026-0814",
            "chiefComplaint": "Severe morning stiffness and lumbar pain",
            "simulatedFailure": {
                "primary": True,
                "secondary": True,
                "vllm": True
            }
        }, headers=doctor_headers)
        assert status == 201
        assert body["ok"] is True
        assert body["fallbackOccurred"] is True
        assert body["providerUsed"] == "Deterministic Classical Unani Knowledge Fallback"
        assert len(body["degradationLogs"]) >= 3
        print(f"[PASS] Test 12: Chained Failover & Telemetry - Failed over to Classical Fallback (Degradation log count: {len(body['degradationLogs'])})")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 12: Chained Failover & Telemetry ({e})")
        failed += 1

    # 13. RBAC Barrier: Non-Clinical Roles Blocked from AI Consultation
    try:
        status, body = client.request("POST", "/api/v1/ai/consult", {
            "mrn": "MRN-2026-0814",
            "chiefComplaint": "Self-prescribing inquiry"
        }, headers=rec_headers)
        assert status == 403, f"Expected 403 Forbidden for receptionist, got {status}"
        assert body["ok"] is False
        assert "authorized" in body["error"].lower() or "restricted" in body["error"].lower()
        print(f"[PASS] Test 13: RBAC Clinical Role Barrier - Receptionist blocked with HTTP 403: '{body['error']}'")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 13: RBAC Clinical Role Barrier ({e})")
        failed += 1

    # 14. Multi-Tenancy Barrier: Cross-Tenant AI Consultation Blocked
    try:
        # HQ Doctor attempting consultation on Branch Patient (PAT-0901)
        status, body = client.request("POST", "/api/v1/ai/consult", {
            "mrn": "PAT-0901",
            "chiefComplaint": "Cross-facility consultation attempt"
        }, headers=doctor_headers)
        assert status == 403, f"Expected 403 Forbidden for cross-tenant access, got {status}"
        assert body["ok"] is False
        assert body["code"] == "CROSS_TENANT_ACCESS_DENIED"
        print(f"[PASS] Test 14: Multi-Tenancy Cross-Facility Barrier - Blocked cross-tenant consult with HTTP 403: '{body['error']}'")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 14: Multi-Tenancy Cross-Facility Barrier ({e})")
        failed += 1

    # 15. 21 CFR Part 11 Merkle Audit Anchoring & Zero Developer Jargon Audit
    try:
        # Verify Merkle audit anchoring
        status_audit, body_audit = client.request("GET", "/api/v1/audit/logs", headers={"Authorization": f"Bearer {doctor_token}"})
        # Check database directly for audit ledger event
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit_ledger WHERE event_type = 'AI_CONSULTATION_GENERATED' ORDER BY block_number DESC LIMIT 1")
            audit_row = cur.fetchone()
            assert audit_row is not None, "AI consultation event not found in audit_ledger"
            leaf_hash = audit_row[2]
            assert len(leaf_hash) == 64

        # Verify zero developer jargon
        all_text = json.dumps(body).lower()
        found_jargon = [j for j in PROHIBITED_JARGON if j in all_text]
        assert len(found_jargon) == 0, f"Found prohibited developer jargon: {found_jargon}"
        print(f"[PASS] Test 15: Merkle Audit Anchoring & Zero Jargon - Consultation anchored in block #{audit_row[0]} (Hash: {leaf_hash[:16]}...); 0 jargon found")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Test 15: Merkle Audit Anchoring & Zero Jargon ({e})")
        failed += 1

    print("=" * 76)
    print(f"PHASE 5 VERIFICATION SUMMARY: {passed} PASSED | {failed} FAILED (TOTAL {passed + failed})")
    print("=" * 76)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
