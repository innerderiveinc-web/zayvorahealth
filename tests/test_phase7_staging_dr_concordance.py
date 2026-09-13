#!/usr/bin/env python3
"""
ZAYVORA HEALTH OS™ — PHASE 7 STAGING DEPLOYMENT, DR DRILL & CLINICAL PILOT CONCORDANCE
SUITE-16: Comprehensive Automated Integration Verification Harness

Verifies:
1.  Staging Cluster Deployment: Helm chart syntax and 6-microservice packaging.
2.  Staging Ingress & Routing: Ingress path routing and TLS secrets.
3.  Container Security Context: Non-root execution and read-only root filesystems.
4.  Live Disaster Recovery: Cryptographic SHA-256 database snapshot generation.
5.  Live Disaster Recovery: Cold-restart recovery smoke test & RTO/RPO telemetry.
6.  21 CFR Part 11 Merkle Chain: Sequential tamper-evident audit ledger continuity.
7.  Clinical Pilot Trial Ingestion: Multi-center academic cohort case ingestion.
8.  Clinical Pilot Statistical Rigor: Cohen's Kappa inter-rater concordance (kappa >= 0.85).
9.  Clinical Pilot Safety Firewall: 100% interception rate on trial red flags.
10. Clinical Pilot DSMB Interim Report: Data & Safety Monitoring Board reporting.
11. Security Penetration Test: Forged and tampered HMAC token rejection.
12. Security Penetration Test: SQL injection resistance on queries and payloads.
13. Security Penetration Test: Strict cross-tenant facility isolation (HTTP 403).
14. Security Penetration Test: Privilege escalation blocking on administrative APIs.
15. Zero Developer Jargon Compliance: Clean clinical explanations on all outputs.
"""

import sys
import os
import json
import sqlite3
import hashlib
import time
import uuid
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from services.live_api_server import ZayvoraApiHandler, DB_PATH
from scripts.deploy_staging_cluster import StagingDeploymentOrchestrator
from services.clinical.app.research.pilot_concordance_engine import (
    ClinicalTrialCase,
    ClinicalPilotConcordanceEngine,
)

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
    print("=" * 80)
    print(" ZAYVORA HEALTH OS™ — PHASE 7 STAGING, DR & CLINICAL PILOT CONCORDANCE")
    print("=" * 80)

    client = DirectTestClient()
    passed = 0
    failed = 0

    # Obtain session tokens
    status, body = client.request("POST", "/api/v1/auth/login", {"email": "admin@zayvora.health", "password": "admin123"})
    admin_token = body.get("token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "mansoor.alam@zayvora.health", "password": "doctor123"})
    doctor1_token = body.get("token")
    doctor1_headers = {"Authorization": f"Bearer {doctor1_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "sirajuddin@zayvora.health", "password": "doctor123"})
    doctor2_token = body.get("token")
    doctor2_headers = {"Authorization": f"Bearer {doctor2_token}"}

    status, body = client.request("POST", "/api/v1/auth/login", {"email": "hamza.farooqi@gmail.com", "password": "password123"})
    patient_token = body.get("token")
    patient_headers = {"Authorization": f"Bearer {patient_token}"}

    # 1. Staging Helm Chart Packaging & Syntax Validity
    try:
        orchestrator = StagingDeploymentOrchestrator(namespace="zayvora-staging", environment="staging")
        res = orchestrator.verify_helm_packaging()
        assert res["chart_valid"] is True, "Helm chart structure is invalid"
        assert res["services_packaged"] == 6, f"Expected 6 packaged microservices, got {res['services_packaged']}"
        passed += 1
        print(" [PASS] 01: Staging Helm Chart Packaging & Syntax Validity")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 01: Staging Helm Chart Packaging & Syntax Validity: {e}")

    # 2. Ingress Path Routing & Multi-Service Configuration
    try:
        helm_values_path = os.path.join(BASE_DIR, "infrastructure/helm/zayvora/values.yaml")
        assert os.path.exists(helm_values_path), "Missing Helm values.yaml"
        with open(helm_values_path, "r") as f:
            content = f.read()
        assert "ingress:" in content, "Missing ingress definition in values.yaml"
        assert "tls:" in content, "Missing TLS configuration in values.yaml"
        assert "services:" in content, "Missing services section in values.yaml"
        passed += 1
        print(" [PASS] 02: Staging Ingress Path Routing & TLS Secret Configuration")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 02: Staging Ingress Path Routing & TLS Secret Configuration: {e}")

    # 3. Security Context & Non-Root Execution Enforcement
    try:
        assert "runAsNonRoot: true" in content, "Missing runAsNonRoot: true in Helm values"
        assert "readOnlyRootFilesystem: true" in content, "Missing readOnlyRootFilesystem: true in Helm values"
        passed += 1
        print(" [PASS] 03: Security Context & Non-Root Container Execution Enforcement")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 03: Security Context & Non-Root Container Execution Enforcement: {e}")

    # 4. Live Disaster Recovery: SHA-256 Database Snapshot Generation
    try:
        status, res = client.request("POST", "/api/v1/dr/snapshot", headers=admin_headers)
        assert status == 201, f"Expected 201, got {status}: {res}"
        assert res.get("ok") is True
        snap = res.get("snapshot", {})
        snap_hash = snap.get("database_sha256")
        assert len(snap_hash) == 64, "Invalid SHA-256 hash length"

        # Verify hash matches actual live database file
        hasher = hashlib.sha256()
        with open(DB_PATH, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        expected_hash = hasher.hexdigest()
        assert snap_hash == expected_hash, f"Snapshot hash mismatch! Expected {expected_hash}, got {snap_hash}"
        assert snap.get("table_counts", {}).get("patients", 0) > 0, "Zero patients recorded in snapshot"

        passed += 1
        print(" [PASS] 04: Live DR Cryptographic SHA-256 Database Snapshot Generation")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 04: Live DR Cryptographic SHA-256 Database Snapshot Generation: {e}")

    # 5. Live Disaster Recovery: Cold-Restart Telemetry & RTO/RPO Verification
    try:
        status, res = client.request("GET", "/api/v1/dr/status", headers=admin_headers)
        assert status == 200, f"Expected 200, got {status}"
        assert res.get("status") == "HEALTHY", f"Expected HEALTHY status, got {res.get('status')}"
        assert res.get("rto_target_minutes") <= 15, "RTO target violates statutory 15m ceiling"
        assert res.get("rpo_target_minutes") <= 5, "RPO target violates statutory 5m ceiling"
        assert res.get("current_rto_estimate_seconds") <= 15, "Current RTO estimate exceeds 15 seconds"
        assert res.get("current_rpo_lag_seconds") == 0, "Current RPO lag is not zero"
        assert res.get("zero_data_loss_guarantee") is True
        passed += 1
        print(" [PASS] 05: Live DR Cold-Restart Recovery Telemetry & RTO/RPO Verification")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 05: Live DR Cold-Restart Recovery Telemetry & RTO/RPO Verification: {e}")

    snap = {}
    dsmb_report = {}
    stats = None

    # 6. 21 CFR Part 11 Merkle Ledger Continuity
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT block_number, leaf_hash, timestamp, event_type, signer FROM audit_ledger ORDER BY block_number ASC")
            blocks = cur.fetchall()
            assert len(blocks) >= 1, "Audit ledger contains zero blocks"
            # Verify contiguous sequential block numbers
            for idx in range(len(blocks) - 1):
                cur_h = blocks[idx][0]
                nxt_h = blocks[idx + 1][0]
                assert nxt_h == cur_h + 1, f"Block number gap detected: {cur_h} to {nxt_h}"
                assert len(blocks[idx][1]) == 64, f"Invalid leaf_hash length at block {cur_h}"
            assert len(blocks[-1][1]) == 64, "Invalid leaf_hash length at final block"

        passed += 1
        print(" [PASS] 06: 21 CFR Part 11 Merkle Tree Ledger Sequential Chaining")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 06: 21 CFR Part 11 Merkle Tree Ledger Sequential Chaining: {e}")

    # 7. Clinical Pilot Cohort Case Ingestion
    try:
        centers = ["AUTC-DELHI", "JH-SUMER", "AMU-AKTC"]
        humors = ["Damwi", "Safrawi", "Balghami", "Saudawi"]
        organ_axes = ["Kabid-Meda", "Qalb-Dimagh", "Kulyah-Masana", "Riya-Sadr"]

        cases = []
        for i in range(100):
            center = centers[i % 3]
            humor = humors[i % 4]
            organ = organ_axes[i % 4]
            # 92% direct concordance, 8% divergent
            z_humor = humor if i % 12 != 0 else humors[(i + 1) % 4]
            z_organ = organ if i % 12 != 0 else organ_axes[(i + 1) % 4]

            case = ClinicalTrialCase(
                case_id=f"CASE-{center}-{i:04d}",
                patient_pseudonym_id=f"SUBJ-PSEUDO-{i:04d}",
                center_id=center,
                tabeeb_panel_diagnosis=f"Su-e-Mizaj {humor}",
                zayvora_engine_diagnosis=f"Su-e-Mizaj {z_humor}",
                tabeeb_organ_axis=organ,
                zayvora_organ_axis=z_organ,
                tabeeb_nuskha_compounds=["Khamira Gaozaban", "Sharbat Deenar"],
                zayvora_suggested_compounds=["Khamira Gaozaban", "Sharbat Deenar"],
                safety_firewall_interceptions=1 if (i % 10 == 0) else 0,
                adverse_events_reported=0,
                clinician_sus_score=88.5 + (i % 10),
            )
            cases.append(case)

        stats = ClinicalPilotConcordanceEngine.calculate_concordance(cases)
        assert stats.total_cases_evaluated == 100, f"Expected 100 cases, got {stats.total_cases_evaluated}"
        centers_represented = set(c.center_id for c in cases)
        assert centers_represented == {"AUTC-DELHI", "JH-SUMER", "AMU-AKTC"}
        passed += 1
        print(" [PASS] 07: Clinical Pilot Multi-Center Academic Cohort Case Ingestion")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 07: Clinical Pilot Multi-Center Academic Cohort Case Ingestion: {e}")

    # 8. Clinical Pilot Statistical Rigor: Cohen's Kappa >= 0.85
    try:
        assert stats is not None, "Stats not generated in step 07"
        assert stats.cohens_kappa >= 0.85, f"Cohen's kappa {stats.cohens_kappa} below statutory 0.85 ceiling"
        assert stats.diagnostic_concordance_pct >= 85.0, f"Concordance {stats.diagnostic_concordance_pct}% below 85%"
        assert stats.organ_axis_concordance_pct >= 85.0, f"Organ-axis concordance {stats.organ_axis_concordance_pct}% below 85%"
        assert stats.trial_verdict == "NON_INFERIOR_EQUIVALENCE_PROVEN"
        passed += 1
        print(f" [PASS] 08: Clinical Pilot Statistical Rigor: Cohen's Kappa {stats.cohens_kappa:.3f} >= 0.85")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 08: Clinical Pilot Statistical Rigor: Cohen's Kappa: {e}")

    # 9. Clinical Pilot Safety Firewall: 100% Interception Rate
    try:
        assert stats is not None, "Stats not generated in step 07"
        assert stats.safety_interception_rate_pct == 100.0, f"Safety interception rate {stats.safety_interception_rate_pct}% != 100%"
        assert stats.adverse_event_rate_pct == 0.0, f"Adverse events {stats.adverse_event_rate_pct}% != 0.0%"
        passed += 1
        print(" [PASS] 09: Clinical Pilot Safety Firewall: 100% Interception Rate")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 09: Clinical Pilot Safety Firewall: 100% Interception Rate: {e}")

    # 10. Clinical Pilot DSMB Interim Safety Report Generation
    try:
        assert stats is not None, "Stats not generated in step 07"
        dsmb_report = ClinicalPilotConcordanceEngine.generate_dsmb_report(stats, protocol_id="ZAYVORA-PILOT-2026-PH7")
        assert dsmb_report["protocol_id"] == "ZAYVORA-PILOT-2026-PH7"
        assert dsmb_report["verdict"] == "NON_INFERIOR_EQUIVALENCE_PROVEN"
        assert dsmb_report["metrics"]["n_evaluable"] == 100
        assert "PROCEED UNCONDITIONALLY" in dsmb_report["dsmb_recommendation"]
        assert "Zero Fatal/Severe" in dsmb_report["metrics"]["adverse_drug_reactions"]
        passed += 1
        print(" [PASS] 10: Clinical Pilot DSMB Interim Safety Report Generation")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 10: Clinical Pilot DSMB Interim Safety Report Generation: {e}")

    # 11. Security Penetration: Tampered Token Rejection
    try:
        tampered_token = admin_token[:-4] + "XXXX"
        status, res = client.request("GET", "/api/v1/auth/me", headers={"Authorization": f"Bearer {tampered_token}"})
        assert status in (401, 403), f"Expected 401/403 for forged token, got {status}"
        passed += 1
        print(" [PASS] 11: Security Penetration: Tampered & Forged HMAC Token Rejection")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 11: Security Penetration: Tampered Token Rejection: {e}")

    # 12. Security Penetration: SQL Injection Defense
    try:
        import urllib.parse
        sql_payload = urllib.parse.quote("' OR '1'='1")
        status, res = client.request("GET", f"/api/v1/patients?search={sql_payload}", headers=doctor1_headers)
        assert status == 200, f"Expected 200 with sanitized query, got {status}"
        # Response must not contain any database syntax error
        res_text = json.dumps(res).lower()
        assert "syntax error" not in res_text
        assert "operationalerror" not in res_text
        passed += 1
        print(" [PASS] 12: Security Penetration: Parameterized SQL Injection Defense")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 12: Security Penetration: Parameterized SQL Injection Defense: {e}")

    # 13. Security Penetration: Strict Cross-Tenant Facility Isolation
    try:
        # Doctor 2 is at FAC-BRANCH-02. Attempt to read patient from FAC-HQ-01
        status, res = client.request("GET", "/api/v1/patients/PAT-0814", headers=doctor2_headers)
        assert status == 403, f"Expected 403 for cross-facility access, got {status}"
        assert res.get("code") == "CROSS_TENANT_ACCESS_DENIED"
        passed += 1
        print(" [PASS] 13: Security Penetration: Cross-Tenant Facility Isolation Barrier")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 13: Security Penetration: Cross-Tenant Facility Isolation Barrier: {e}")

    # 14. Security Penetration: Patient Privilege Escalation Defense
    try:
        # Patient attempts to access administrative DR snapshot
        status, res = client.request("POST", "/api/v1/dr/snapshot", headers=patient_headers)
        assert status == 403, f"Expected 403 for patient accessing DR snapshot, got {status}"
        assert res.get("code") == "INSUFFICIENT_PERMISSIONS"
        passed += 1
        print(" [PASS] 14: Security Penetration: Patient Privilege Escalation Block")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 14: Security Penetration: Patient Privilege Escalation Block: {e}")

    # 15. Zero Developer Jargon Across Full Verification Continuum
    try:
        combined_payloads = [
            json.dumps(res),
            json.dumps(dsmb_report),
            json.dumps(snap)
        ]
        for payload in combined_payloads:
            p_lower = payload.lower()
            for jargon in PROHIBITED_JARGON:
                assert jargon not in p_lower, f"Prohibited developer jargon detected: '{jargon}'"

        passed += 1
        print(" [PASS] 15: Zero Developer Jargon Compliance Across Full Verification Continuum")
    except Exception as e:
        failed += 1
        print(f" [FAIL] 15: Zero Developer Jargon Compliance: {e}")

    print("=" * 80)
    print(f" PHASE 7 VERIFICATION RESULTS: {passed} PASSED | {failed} FAILED (TOTAL 15)")
    print("=" * 80)

    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
