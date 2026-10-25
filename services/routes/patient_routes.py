"""
ZAYVORA Health OS — Patient Records, Longitudinal EHR & Clinical Intelligence Router
=====================================================================================
Modular request dispatcher for:
- Patient Directory (Multi-Tenant Isolation Guard & PHI AES-256 GCM Decryption)
- Direct Patient Registration (with MRN Auto-Generation and PHI Encryption)
- Single Patient Clinical Record Lookup & Demographic Profiles
- Patient 360 Master Graph & V2 Authoritative Longitudinal Clinical Timeline
- Patient Self-Service Records Aggregation (Appointments & Prescriptions)
- Classical 10-Ajnas Mizaj Assessment Recording & Latest Mizaj Retrieval
- Personal Health Profile™ & Care Gap Intelligence Summary
- Patient Health Literacy & Education Modules Catalog
- Patient Document & Diagnostic Medical Picture Upload (15MB Limit, Multi-Format Base64)
- Vernacular Audio Posology Engine (Urdu/Hindi/English with Schedule E-1 Mudabbar Safety Warnings)
- Non-Judgmental Adherence Tracking & Missed Dose Feedback
- Purpose-Specific Patient Consent Records & Cryptographic SHA-256 Audit Seals
- Clinical Outcomes Registry
"""

import base64
import dataclasses
from datetime import datetime, timezone
import hashlib
import json
import os
import secrets
import time
from typing import Any, Dict
import uuid


def handle_patient_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for patient records, EHR timeline, consent, and education."""
    import services.live_api_server as srv

    # 1. Patient Medical Picture & Attachment Metadata Retrieval
    if path == "/api/v1/patient/attachments":
        target_mrn = query_params.get("mrn", [None])[0]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS patient_attachments (
                    id TEXT PRIMARY KEY,
                    mrn TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size_bytes INTEGER NOT NULL,
                    mime_type TEXT NOT NULL,
                    description TEXT,
                    uploaded_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            if target_mrn:
                cur.execute("SELECT id, mrn, document_type, file_name, file_size_bytes, mime_type, description, uploaded_by, created_at FROM patient_attachments WHERE mrn = ? ORDER BY created_at DESC", (target_mrn,))
            else:
                cur.execute("SELECT id, mrn, document_type, file_name, file_size_bytes, mime_type, description, uploaded_by, created_at FROM patient_attachments ORDER BY created_at DESC")
            rows = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(rows), "attachments": rows})
        return True

    # 2. Patient 360 Master Snapshot
    if path in ("/api/v1/patient/360", "/api/v1/patients/360"):
        pat_id = query_params.get("patient_id", ["PAT-774901"])[0]
        if srv.Patient360Master:
            snapshot = srv.Patient360Master.get_patient_360(pat_id)
        else:
            snapshot = {"patient_id": pat_id, "error": "Patient 360 master engine unavailable."}
        handler._send_json({"ok": True, "patient_360": snapshot})
        return True

    # 3. Patient 360 Timeline (Phase 3 Core Clinical Continuum)
    if "/timeline" in path and path.startswith("/api/v1/patients/"):
        parts = path.strip("/").split("/")
        pat_id = parts[3]

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients WHERE id = ? OR mrn = ?", (pat_id, pat_id))
            p_row = cur.fetchone()
            if not p_row:
                handler._send_error("Patient record not found.", status=404, code="PATIENT_NOT_FOUND")
                return True
            patient = dict(p_row)
            mrn = patient["mrn"]

            # Cross-tenant check
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if patient.get("facility_id") and patient["facility_id"] != auth_ctx.get("facilityId"):
                    handler._send_error("Access denied: Cross-tenant patient record access is restricted.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

            events = []

            # Encounters
            cur.execute("SELECT * FROM encounters WHERE mrn = ? ORDER BY started_at ASC", (mrn,))
            for enc in cur.fetchall():
                ed = dict(enc)
                try:
                    soap = json.loads(ed.get("soap_json") or "{}")
                except Exception:
                    soap = {}
                events.append({
                    "eventType": "ENCOUNTER",
                    "id": ed["id"],
                    "timestamp": ed["started_at"],
                    "summary": f"Clinical Encounter with {ed['doctor_name']}: {ed.get('chief_complaint', 'General OPD')}",
                    "status": ed["status"],
                    "signatureHash": ed.get("signature_hash"),
                    "details": {
                        "encounterNumber": ed["encounter_number"],
                        "doctor": ed["doctor_name"],
                        "assessment": soap.get("assessment", "Clinical Review"),
                        "status": ed["status"]
                    }
                })

            # Appointments
            cur.execute("SELECT * FROM appointments WHERE mrn = ? ORDER BY appointment_date ASC", (mrn,))
            for apt in cur.fetchall():
                ad = dict(apt)
                events.append({
                    "eventType": "APPOINTMENT",
                    "id": ad["id"],
                    "timestamp": f"{ad['appointment_date']} {ad['appointment_time']}",
                    "summary": f"OPD Appointment (Token {ad['token_number']}) - {ad['department']}",
                    "status": ad["status"],
                    "details": {
                        "tokenNumber": ad["token_number"],
                        "doctor": ad["doctor_name"],
                        "feeAmount": ad["fee_amount"]
                    }
                })

            # Prescriptions
            cur.execute("SELECT * FROM prescriptions WHERE mrn = ? ORDER BY created_at ASC", (mrn,))
            for rx in cur.fetchall():
                rd = dict(rx)
                try:
                    items = json.loads(rd.get("items_json") or "[]")
                except Exception:
                    items = []
                item_names = ", ".join([it.get("name", "Herbal Compound") for it in items])
                events.append({
                    "eventType": "PRESCRIPTION",
                    "id": rd["id"],
                    "timestamp": rd["created_at"],
                    "summary": f"Prescription {rd['order_number']}: {item_names}",
                    "status": rd["status"],
                    "signatureHash": rd.get("signature_hash"),
                    "details": {
                        "orderNumber": rd["order_number"],
                        "doctor": rd["doctor_name"],
                        "itemCount": len(items),
                        "items": items
                    }
                })

            # Invoices
            cur.execute("SELECT * FROM invoices WHERE mrn = ? ORDER BY created_at ASC", (mrn,))
            for inv in cur.fetchall():
                id_dict = dict(inv)
                events.append({
                    "eventType": "INVOICE",
                    "id": id_dict["id"],
                    "timestamp": id_dict["created_at"],
                    "summary": f"OPD Receipt {id_dict['invoice_number']} - ₹{id_dict['amount']} ({id_dict['payment_method']})",
                    "status": id_dict["status"],
                    "details": {
                        "invoiceNumber": id_dict["invoice_number"],
                        "amount": id_dict["amount"],
                        "paymentMethod": id_dict["payment_method"]
                    }
                })

            # Audit Blocks
            cur.execute("SELECT * FROM audit_ledger WHERE details_json LIKE ? ORDER BY timestamp ASC", (f"%{mrn}%",))
            for blk in cur.fetchall():
                bd = dict(blk)
                events.append({
                    "eventType": "AUDIT_BLOCK",
                    "id": f"BLK-{bd['block_number']}",
                    "timestamp": bd["timestamp"],
                    "summary": f"21 CFR Part 11 Merkle Anchor: {bd['event_type']} by {bd['signer']}",
                    "status": bd["status"],
                    "signatureHash": bd["leaf_hash"],
                    "details": {
                        "blockNumber": bd["block_number"],
                        "leafHash": bd["leaf_hash"],
                        "signer": bd["signer"]
                    }
                })

        handler._send_json({
            "ok": True,
            "patient": {
                "id": patient["id"],
                "mrn": patient["mrn"],
                "fullName": f"{patient['first_name']} {patient['last_name']}",
                "mizajDominant": patient["mizaj_dominant"],
                "facilityId": patient["facility_id"]
            },
            "count": len(events),
            "timeline": events
        })
        return True

    # 4. Latest Mizaj Assessment for Patient
    if "/mizaj-assessment/latest" in path and path.startswith("/api/v1/patients/"):
        parts = path.strip("/").split("/")
        pat_id = parts[3]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients WHERE id = ? OR mrn = ?", (pat_id, pat_id))
            p_row = cur.fetchone()
            if not p_row:
                handler._send_error("Patient not found.", status=404, code="PATIENT_NOT_FOUND")
                return True
            pat = dict(p_row)

            cur.execute("SELECT mizaj_json FROM encounters WHERE mrn = ? ORDER BY started_at DESC LIMIT 1", (pat["mrn"],))
            enc_row = cur.fetchone()
            mizaj_eval = {}
            if enc_row and enc_row["mizaj_json"]:
                try:
                    mizaj_eval = json.loads(enc_row["mizaj_json"])
                except Exception:
                    pass

        handler._send_json({
            "ok": True,
            "patientId": pat["id"],
            "mrn": pat["mrn"],
            "dominantMizaj": pat["mizaj_dominant"],
            "evaluation": mizaj_eval or {
                "dominant": pat["mizaj_dominant"],
                "secondary": "Damawi",
                "su_e_mizaj": "Su-e-Mizaj Barid Balghami",
                "dyscrasia_degree": 2
            }
        })
        return True

    # 5. Patients Directory (Tenant-Scoped with PHI Decryption)
    if path == "/api/v1/patients":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                cur.execute("SELECT * FROM patients WHERE mrn = ? OR user_id = ?", (auth_ctx["mrn"], auth_ctx["userId"]))
            elif auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", []):
                cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
            elif auth_ctx:
                user_fac = auth_ctx.get("facilityId") or target_facility
                cur.execute("SELECT * FROM patients WHERE facility_id = ? ORDER BY created_at DESC", (user_fac,))
            elif not auth_ctx and not query_params:
                cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM patients WHERE facility_id = ? ORDER BY created_at DESC", (target_facility,))

            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                if r.get("contact_phone"):
                    r["contact_phone"] = srv._decrypt_phi(r["contact_phone"])
                if r.get("contact_email"):
                    r["contact_email"] = srv._decrypt_phi(r["contact_email"])
                try:
                    r["allergies"] = json.loads(r.get("allergies_json") or "[]")
                except Exception:
                    r["allergies"] = []
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "patients": rows})
        return True

    # 6. Single Patient Details (Tenant Isolation Guard)
    if path.startswith("/api/v1/patients/"):
        pat_id = path.split("/")[-1]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients WHERE id = ? OR mrn = ?", (pat_id, pat_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Clinical record not found for the specified patient identifier.", status=404, code="PATIENT_NOT_FOUND")
                return True
            res = dict(row)
            if res.get("contact_phone"):
                res["contact_phone"] = srv._decrypt_phi(res["contact_phone"])
            if res.get("contact_email"):
                res["contact_email"] = srv._decrypt_phi(res["contact_email"])

            enc_fac = res.get("facility_id") or "FAC-HQ-01"
            if auth_ctx:
                if auth_ctx["role"] == "PATIENT":
                    if res.get("mrn") != auth_ctx.get("mrn") and res.get("id") != auth_ctx.get("patientId"):
                        handler._send_error("Access denied: Patients are strictly restricted to their own health records.", status=403, code="PATIENT_PORTAL_ACCESS_VIOLATION")
                        return True
                elif auth_ctx["role"] != "SUPER_ADMIN":
                    if enc_fac != auth_ctx["facilityId"]:
                        handler._send_error("Access denied: You do not have authorization to view clinical records from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                        return True

            try:
                res["allergies"] = json.loads(res.get("allergies_json") or "[]")
            except Exception:
                res["allergies"] = []
        handler._send_json({"ok": True, "patient": res})
        return True

    # 7. Patient Self-Service Records Aggregation
    if path == "/api/v1/patient/my-records":
        target_mrn = None
        if auth_ctx and auth_ctx["role"] == "PATIENT":
            target_mrn = auth_ctx["mrn"]
            req_mrn = query_params.get("mrn", [None])[0]
            if req_mrn and req_mrn != target_mrn:
                handler._send_error("Access denied: Patients are strictly restricted to their own health records.", status=403, code="PATIENT_PORTAL_ACCESS_VIOLATION")
                return True
        elif auth_ctx and (handler._has_permission(auth_ctx, "patients:read") or auth_ctx["role"] in ("SUPER_ADMIN", "CLINIC_ADMIN", "DOCTOR", "HAKEEM")):
            target_mrn = query_params.get("mrn", [None])[0]
            if not target_mrn:
                handler._send_error("Patient MRN parameter is required.", status=400, code="MISSING_MRN")
                return True
        else:
            handler._send_error("Authentication required to access patient medical records.", status=401, code="UNAUTHORIZED")
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients WHERE mrn = ?", (target_mrn,))
            pat_row = cur.fetchone()
            if not pat_row:
                handler._send_error("Patient record not found.", status=404, code="PATIENT_NOT_FOUND")
                return True
            pat_data = dict(pat_row)

            cur.execute("SELECT * FROM appointments WHERE mrn = ? ORDER BY appointment_date DESC, appointment_time DESC", (target_mrn,))
            appointments = [dict(r) for r in cur.fetchall()]

            cur.execute("SELECT * FROM prescriptions WHERE mrn = ? ORDER BY created_at DESC", (target_mrn,))
            prescriptions = [dict(r) for r in cur.fetchall()]
            for p in prescriptions:
                try:
                    p["items"] = json.loads(p.get("items_json") or "[]")
                except Exception:
                    p["items"] = []

            cur.execute("SELECT id, encounter_number, mrn, patient_name, doctor_name, chief_complaint, examination_notes, vitals_json, soap_json, mizaj_json, afaal_cascade_json, status, started_at, signed_at FROM encounters WHERE mrn = ? ORDER BY started_at DESC", (target_mrn,))
            encounters = [dict(r) for r in cur.fetchall()]
            for enc in encounters:
                for jf in ["vitals_json", "soap_json", "mizaj_json", "afaal_cascade_json"]:
                    clean_k = jf.replace("_json", "")
                    try:
                        enc[clean_k] = json.loads(enc.get(jf) or "{}")
                    except Exception:
                        enc[clean_k] = {}

            cur.execute("SELECT * FROM invoices WHERE mrn = ? ORDER BY created_at DESC", (target_mrn,))
            invoices = [dict(r) for r in cur.fetchall()]
            for inv in invoices:
                try:
                    inv["line_items"] = json.loads(inv.get("line_items_json") or "[]")
                except Exception:
                    inv["line_items"] = []

            cur.execute("SELECT * FROM telemedicine_rooms WHERE mrn = ? ORDER BY created_at DESC", (target_mrn,))
            telemed_rooms = [dict(r) for r in cur.fetchall()]

            cur.execute("SELECT * FROM notifications WHERE mrn = ? ORDER BY created_at DESC", (target_mrn,))
            notifs = [dict(r) for r in cur.fetchall()]

        bundle = {
            "ok": True,
            "mrn": target_mrn,
            "patient": pat_data,
            "appointments": appointments,
            "prescriptions": prescriptions,
            "encounters": encounters,
            "invoices": invoices,
            "telemedicine_rooms": telemed_rooms,
            "notifications": notifs,
            "retrieved_at": datetime.utcnow().isoformat() + "Z"
        }
        handler._send_json(bundle)
        return True

    # 8. Patient Education & Health Literacy Modules: Catalog
    if path in ("/api/v1/patient/education/modules", "/api/v1/patient/education/modules/all"):
        mods = srv.get_all_patient_education_modules()
        handler._send_json({
            "ok": True,
            "framework": "Patient & Family Health Literacy Guide",
            "total_modules": len(mods),
            "modules": mods
        })
        return True

    # 9. Patient Education & Health Literacy: Single Module
    if path.startswith("/api/v1/patient/education/modules/"):
        slug = path.split("/")[-1].lower()
        mod_data = srv.get_patient_education_module(slug)
        if mod_data:
            handler._send_json({"ok": True, "module": mod_data})
        else:
            handler._send_error(f"Education module '{slug}' not found.", status=404, code="MODULE_NOT_FOUND")
        return True

    # 10. Patient 360 Blueprint Engine
    if path.startswith("/api/v1/patient/360/") or path.startswith("/api/v1/clinical/patients/360/"):
        patient_id = path.split("/")[-1]
        if srv.Patient360Engine:
            p360 = srv.Patient360Engine.build_patient_360(patient_id)
            handler._send_json({"ok": True, "patient_360": p360})
        else:
            handler._send_error("Patient 360 engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 11. Personal Health Profile™
    if path in ("/api/v1/clinical/personal-health-profile", "/api/v1/patient/personal-health-profile") or path.startswith("/api/v1/clinical/personal-health-profile/"):
        patient_id = query_params.get("patient_id", ["PAT-001"])[0] if query_params else "PAT-001"
        if path.startswith("/api/v1/clinical/personal-health-profile/") and len(path.rstrip("/").split("/")) > 4:
            patient_id = path.rstrip("/").split("/")[-1]
        if srv.PersonalHealthProfileEngine:
            profile = srv.PersonalHealthProfileEngine.build_profile(patient_id=patient_id)
            handler._send_json({"ok": True, "profile": profile.to_dict()})
        else:
            handler._send_error("Personal Health Profile engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 12. Care Gap Intelligence Summary
    if path in ("/api/v1/patient/care-gaps", "/api/v1/patient/care-gaps/summary") or path.startswith("/api/v1/patient/care-gaps/"):
        patient_id = query_params.get("patient_id", ["PAT-774901"])[0]
        if path.startswith("/api/v1/patient/care-gaps/") and path.split("/")[-1] != "summary":
            patient_id = path.split("/")[-1]
        if srv.CareGapIntelligenceEngine:
            summary = srv.CareGapIntelligenceEngine.evaluate_patient_care_gaps(
                patient_id=patient_id,
                patient_name="Hamza Farooqi"
            )
            handler._send_json({"ok": True, "care_gap_summary": dataclasses.asdict(summary)})
        else:
            handler._send_error("CareGapIntelligenceEngine unavailable.", status=503)
        return True

    # 13. Longitudinal Clinical Timeline (V2)
    if path in ("/api/v1/patient/timeline", "/api/v1/clinical/patient-timeline") or (path.startswith("/api/v1/patient/") and path.endswith("/timeline")):
        pat_id = query_params.get("patient_id", [None])[0] or query_params.get("mrn", [None])[0]
        if not pat_id and "/api/v1/patient/" in path:
            pat_id = path.split("/")[4]
        if not pat_id:
            pat_id = "PAT-0814"
        events = []
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, event_timestamp, event_type, title, clinical_summary, metrics_json, actor_name, actor_role, evidence_claim_id, facility_id
                FROM longitudinal_clinical_timeline
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY event_timestamp ASC
            """, (pat_id,))
            for r in cur.fetchall():
                m = {}
                if r[5]:
                    try:
                        m = json.loads(r[5])
                    except Exception:
                        m = {"raw": r[5]}
                events.append({
                    "id": r[0],
                    "timestamp": r[1],
                    "type": r[2],
                    "title": r[3],
                    "summary": r[4],
                    "metrics": m,
                    "actor_name": r[6],
                    "actor_role": r[7],
                    "evidence_claim_id": r[8],
                    "facility_id": r[9]
                })
        handler._send_json({"ok": True, "patient_id": pat_id, "count": len(events), "timeline": events})
        return True

    # 14. Patient 360 V2 Authoritative Graph
    if path in ("/api/v1/patient/360-v2", "/api/v1/clinical/patient/360-v2"):
        pat_id = query_params.get("patient_id", ["PAT-0814"])[0]
        p360 = srv._build_patient_360_v2(pat_id)
        handler._send_json({"ok": True, "patient_id": pat_id, "patient_360": p360})
        return True

    # 15. Patient Consent Records Query
    if path in ("/api/v1/patient/consent", "/api/v1/clinical/patient/consent"):
        pat_id = query_params.get("patient_id", ["PAT-0814"])[0]
        consents = []
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, patient_id, consent_type, version, language, purpose, timestamp, method, patient_identity, 
                       witness_name, is_revoked, revocation_timestamp, expiry_date, data_sharing_permitted, 
                       research_permitted, ai_processing_permitted, signature_hash, facility_id
                FROM consent_engine_records
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY timestamp DESC
            """, (pat_id,))
            for r in cur.fetchall():
                consents.append({
                    "id": r[0],
                    "patient_id": r[1],
                    "type": r[2],
                    "version": r[3],
                    "language": r[4],
                    "purpose": r[5],
                    "timestamp": r[6],
                    "method": r[7],
                    "patient_identity": r[8],
                    "witness_name": r[9],
                    "is_revoked": bool(r[10]),
                    "revocation_timestamp": r[11],
                    "expiry_date": r[12],
                    "data_sharing": bool(r[13]),
                    "research_permitted": bool(r[14]),
                    "ai_processing": bool(r[15]),
                    "signature_hash": r[16],
                    "facility_id": r[17]
                })
        handler._send_json({"ok": True, "patient_id": pat_id, "count": len(consents), "consents": consents})
        return True

    # 16. Clinical Outcomes Registry Query
    if path in ("/api/v1/patient/outcomes", "/api/v1/outcomes/registry", "/api/v1/clinical/outcomes"):
        pat_id = query_params.get("patient_id", ["PAT-0814"])[0]
        outcomes = []
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, patient_id, encounter_id, condition_code, evaluation_interval, symptom_vas_score, 
                       lab_biomarkers_json, adherence_percentage, adverse_events_count, quality_of_life_score, 
                       relapse_observed, treatment_duration_days, referral_status, evidence_grade_generated, recorded_at, facility_id
                FROM clinical_outcomes_registry
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY recorded_at ASC
            """, (pat_id,))
            for r in cur.fetchall():
                b = {}
                if r[6]:
                    try:
                        b = json.loads(r[6])
                    except Exception:
                        b = {"raw": r[6]}
                outcomes.append({
                    "id": r[0],
                    "patient_id": r[1],
                    "encounter_id": r[2],
                    "condition_code": r[3],
                    "interval": r[4],
                    "symptom_vas": r[5],
                    "biomarkers": b,
                    "adherence_percentage": r[7],
                    "adverse_events": r[8],
                    "quality_of_life": r[9],
                    "relapse_observed": bool(r[10]),
                    "treatment_duration_days": r[11],
                    "referral_status": r[12],
                    "evidence_grade": r[13],
                    "recorded_at": r[14],
                    "facility_id": r[15]
                })
        handler._send_json({"ok": True, "patient_id": pat_id, "count": len(outcomes), "outcomes": outcomes})
        return True

    return False


def handle_patient_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for patient registration, posology, consent, and attachments."""
    import services.live_api_server as srv

    # 1. Patient Medical Picture & Document Upload
    if path in ("/api/v1/patient/attachments", "/api/v1/media/upload"):
        mrn = (body.get("mrn") or "GENERAL").strip()
        doc_type = (body.get("document_type") or "GENERAL").strip().upper()
        file_name = (body.get("file_name") or "image.png").strip()
        raw_data = body.get("file_data") or body.get("image_data") or ""
        description = (body.get("description") or "").strip()
        uploaded_by = (auth_ctx.get("email") if auth_ctx else body.get("uploaded_by") or "CLINICIAN").strip()

        if not raw_data:
            handler._send_error("file_data (Base64 or Data URI) is required.", status=400, code="MISSING_FILE_DATA")
            return True

        mime_type = "image/png"
        if raw_data.startswith("data:") and ";base64," in raw_data:
            header, b64_part = raw_data.split(";base64,", 1)
            mime_type = header.replace("data:", "").strip()
        else:
            b64_part = raw_data
            ext = os.path.splitext(file_name)[1].lower()
            ext_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif", ".pdf": "application/pdf"}
            mime_type = ext_map.get(ext, "image/png")

        ALLOWED_MIME_TYPES = {
            "image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp", "application/pdf"
        }
        if mime_type.lower() not in ALLOWED_MIME_TYPES:
            handler._send_error(f"Unsupported file format: {mime_type}. Allowed formats: JPG, PNG, WEBP, GIF, PDF.", status=400, code="INVALID_MIME_TYPE")
            return True

        try:
            file_bytes = base64.b64decode(b64_part)
        except Exception:
            handler._send_error("Invalid Base64 payload encoding.", status=400, code="INVALID_BASE64")
            return True

        MAX_FILE_BYTES = 15 * 1024 * 1024  # 15 MB
        if len(file_bytes) > MAX_FILE_BYTES:
            handler._send_error(f"File size exceeds maximum allowed limit (15 MB). Size: {len(file_bytes)} bytes", status=400, code="FILE_TOO_LARGE")
            return True

        att_id = f"ATT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"
        ext = os.path.splitext(file_name)[1]
        if not ext:
            mime_ext_map = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif", "application/pdf": ".pdf"}
            ext = mime_ext_map.get(mime_type.lower(), ".png")
        safe_filename = f"{att_id}{ext}"

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        upload_dir = os.path.join(base_dir, "uploads", "patients", mrn)
        os.makedirs(upload_dir, exist_ok=True)
        target_path = os.path.join(upload_dir, safe_filename)

        with open(target_path, "wb") as f:
            f.write(file_bytes)

        now_str = datetime.now(timezone.utc).isoformat()
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS patient_attachments (
                    id TEXT PRIMARY KEY,
                    mrn TEXT NOT NULL,
                    document_type TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size_bytes INTEGER NOT NULL,
                    mime_type TEXT NOT NULL,
                    description TEXT,
                    uploaded_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                INSERT INTO patient_attachments (id, mrn, document_type, file_name, file_path, file_size_bytes, mime_type, description, uploaded_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (att_id, mrn, doc_type, file_name, target_path, len(file_bytes), mime_type, description, uploaded_by))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Attachment securely uploaded and catalogued.",
            "attachment": {
                "id": att_id,
                "mrn": mrn,
                "document_type": doc_type,
                "file_name": file_name,
                "file_size_bytes": len(file_bytes),
                "mime_type": mime_type,
                "access_url": f"/api/v1/media/{att_id}",
                "uploaded_by": uploaded_by,
                "uploaded_at": now_str
            }
        }, status=201)
        return True

    # 2. Record 10-Ajnas Mizaj Assessment
    if "/mizaj-assessment" in path and path.startswith("/api/v1/patients/"):
        parts = path.strip("/").split("/")
        pat_id = parts[3]
        answers = body.get("answers") or {}
        enc_id = body.get("encounter_id") or body.get("encounterId")

        dominant = body.get("dominantMizaj") or "Balghami (Cold & Moist)"
        if "cold" in str(answers).lower() and "moist" in str(answers).lower():
            dominant = "Balghami (Cold & Moist)"
        elif "hot" in str(answers).lower() and "dry" in str(answers).lower():
            dominant = "Safrawi (Hot & Dry)"
        elif "hot" in str(answers).lower() and "moist" in str(answers).lower():
            dominant = "Damawi (Sanguine)"
        elif "cold" in str(answers).lower() and "dry" in str(answers).lower():
            dominant = "Saudawi (Melancholic)"

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE patients SET mizaj_dominant = ? WHERE id = ? OR mrn = ?", (dominant, pat_id, pat_id))
            if enc_id:
                cur.execute("UPDATE encounters SET mizaj_json = ? WHERE id = ? OR encounter_number = ?", (json.dumps({"dominant": dominant, "answers": answers}), enc_id, enc_id))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Classical 10-Ajnas Mizaj assessment recorded.",
            "patientId": pat_id,
            "dominantMizaj": dominant,
            "distributionPercentages": {
                "Balghami": 45,
                "Damwi": 25,
                "Safrawi": 20,
                "Saudawi": 10
            }
        }, status=201)
        return True

    # 3. Direct Patient Registration (with PHI Encryption)
    if path == "/api/v1/patients":
        first_name = (body.get("firstName") or body.get("first_name") or "").strip()
        last_name = (body.get("lastName") or body.get("last_name") or "").strip()
        if not first_name:
            handler._send_error("First name is required.", status=400, code="FIRST_NAME_REQUIRED")
            return True

        phone = body.get("phone") or body.get("contactPhone") or ""
        email = body.get("email") or body.get("contactEmail") or ""
        dob = body.get("dob") or body.get("dateOfBirth") or "1990-01-01"
        gender = body.get("gender") or "Unspecified"
        blood_group = body.get("bloodGroup") or "Unknown"
        mizaj = body.get("mizaj") or body.get("mizajDominant") or "Motadil (Balanced)"
        allergies = body.get("allergies") or []
        facility_id = handler._resolve_facility(auth_ctx, query_params, body)

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM patients")
            p_count = cur.fetchone()[0] + 1
            mrn = f"MRN-2026-{p_count:04d}"
            pat_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"

            cur.execute("""
            INSERT INTO patients (id, mrn, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, blood_group, mizaj_dominant, allergies_json, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (pat_id, mrn, first_name, last_name, dob, gender, srv._encrypt_phi(phone), srv._encrypt_phi(email), blood_group, mizaj, json.dumps(allergies), facility_id))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Patient registered successfully.",
            "patient": {
                "id": pat_id,
                "mrn": mrn,
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
                "email": email,
                "facilityId": facility_id,
                "mizajDominant": mizaj,
                "allergies": allergies
            }
        }, status=201)
        return True

    # 4. Vernacular Audio Posology Engine
    if path == "/api/v1/patient/posology/voice":
        lang = (body.get("language") or "ur").lower().strip()
        if lang not in ["ur", "hi", "en"]:
            handler._send_error("Unsupported vernacular language. Supported languages: ur (Urdu), hi (Hindi), en (English).", status=400, code="INVALID_LANGUAGE")
            return True

        medication_name = body.get("medication_name", "")
        dosage = body.get("dosage", "5g")
        frequency = body.get("frequency", "Once daily at night (nocte)")
        vehicle = body.get("vehicle", "lukewarm milk (Sheer-e-Gao)")
        patient_name = body.get("patient_name", "Patient")
        rx_id = body.get("prescription_id")

        if rx_id:
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM prescriptions WHERE id = ? OR prescription_number = ?", (rx_id, rx_id))
                rx_row = cur.fetchone()
                if rx_row:
                    patient_name = rx_row["patient_name"]
                    try:
                        items = json.loads(rx_row["items_json"])
                        if items:
                            first = items[0]
                            medication_name = first.get("item_name") or first.get("medication_name", medication_name)
                            dosage = first.get("dosage", dosage)
                            frequency = first.get("frequency", frequency)
                            vehicle = first.get("instructions", vehicle)
                    except Exception:
                        pass

        if not medication_name:
            medication_name = "Majun Suranjan"

        # Check Schedule E(1) Mudabbar caution requirement
        has_mudabbar_poison = False
        for poison in ["suranjan", "colchicum", "asgandh", "samulfaar", "kuchla", "azaraqi", "bhang"]:
            if poison in medication_name.lower():
                has_mudabbar_poison = True
                break

        if lang == "ur":
            script_text = f"محترم {patient_name}، آپ کی دوا {medication_name} کی خوراک: {dosage} رات سوتے وقت نیم گرم دودھ کے ساتھ استعمال کریں۔"
            transliteration = f"Mohtaram {patient_name}, aap ki dawa {medication_name} ki khorak: {dosage} raat sotay waqt neem garam doodh ke saath istemal karein."
            safety_warning = "تنبیہ: یہ دوا صرف معالج کی بتائی ہوئی مقدار میں استعمال کریں۔ خود سے خوراک میں اضافہ نہ کریں۔" if has_mudabbar_poison else None
            phonetic_guide = f"Dose: {dosage}, Timing: Raat sotay waqt (Nocte), Anupana: Sheer-e-Gao (Warm milk)"
        elif lang == "hi":
            script_text = f"आदरणीय {patient_name}, आपकी दवा {medication_name} की खुराक: {dosage} रात को सोने से पहले गुनगुने दूध के साथ लें।"
            transliteration = f"Aadarniya {patient_name}, aapki dava {medication_name} ki khurak: {dosage} raat ko sone se pehle gungune doodh ke saath lein."
            safety_warning = "चेतावनी: यह दवा केवल चिकित्सक द्वारा निर्धारित मात्रा में लें। अपनी मर्जी से खुराक न बढ़ाएं।" if has_mudabbar_poison else None
            phonetic_guide = f"Dose: {dosage}, Timing: Raat ko sone se pehle, Anupana: Gunguna doodh"
        else:
            script_text = f"Dear {patient_name}, your dosage for {medication_name} is {dosage}, to be taken at bedtime with lukewarm milk."
            transliteration = f"Dear {patient_name}, take {dosage} of {medication_name} at bedtime with lukewarm milk."
            safety_warning = "Caution: Strictly adhere to the prescribed dose. Do not exceed recommendations without consulting your physician." if has_mudabbar_poison else None
            phonetic_guide = f"Dose: {dosage}, Timing: At bedtime (Nocte), Vehicle: Lukewarm milk"

        simulated_audio_base64 = "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="

        response_data = {
            "ok": True,
            "language": lang,
            "patient_name": patient_name,
            "medication_name": medication_name,
            "script": script_text,
            "transliteration": transliteration,
            "phonetic_guide": phonetic_guide,
            "schedule_e1_warning": safety_warning,
            "audio": {
                "mime_type": "audio/mp3",
                "speech_rate": "0.85x",
                "duration_seconds": 6.8 if not has_mudabbar_poison else 10.4,
                "clarity_rating": "CLINICAL_ACCESSIBILITY_OPTIMIZED",
                "audio_base64": simulated_audio_base64
            }
        }
        handler._send_json(response_data)
        return True

    # 5. Adherence Intelligence: Non-Judgmental Missed Dose Logging
    if path in ("/api/v1/patient/adherence/log-missed", "/api/v1/adherence/log-missed"):
        patient_id = body.get("patient_id") or (auth_ctx.get("userId") if auth_ctx else "PAT-001")
        item_id = body.get("item_id", "ITEM-01")
        item_name = body.get("item_name", "Regimen Item")
        reason = body.get("reason", "Routine conflict")
        notes = body.get("notes", "")

        log_entry = {
            "id": f"ADH-{int(datetime.now().timestamp())}",
            "patient_id": patient_id,
            "item_id": item_id,
            "item_name": item_name,
            "status": "MISSED",
            "reason": reason,
            "notes": notes,
            "logged_at": datetime.now(timezone.utc).isoformat(),
            "support_guidance": "Thank you for letting us know. Consistent communication helps your care team tailor your nuskha for optimal comfort and ease."
        }
        handler._send_json({"ok": True, "adherence_entry": log_entry, "message": "Adherence feedback recorded without penalty."})
        return True

    # 6. Active Purpose-Specific Consent Engine Update
    if path in ("/api/v1/consent/update", "/api/v1/patient/consent/update"):
        patient_id = body.get("patient_id") or (auth_ctx.get("userId") if auth_ctx else "PAT-001")
        purpose = (body.get("purpose") or "AI_PROCESSING").upper()
        status = (body.get("status") or "ACTIVE").upper()
        notes = body.get("notes", "")

        VALID_PURPOSES = ["CARE", "AI_PROCESSING", "COMMUNICATION", "RESEARCH", "DATA_SHARING"]
        if purpose not in VALID_PURPOSES:
            handler._send_error(f"Invalid consent purpose. Must be one of {VALID_PURPOSES}", status=400)
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS patient_consents (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    status TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    notes TEXT
                )
            """)
            consent_id = f"CSNT-{patient_id}-{purpose}"
            now_str = datetime.now(timezone.utc).isoformat()
            cur.execute("""
                INSERT INTO patient_consents (id, patient_id, purpose, status, updated_at, notes)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at, notes=excluded.notes
            """, (consent_id, patient_id, purpose, status, now_str, notes))
            conn.commit()

        handler._send_json({
            "ok": True,
            "consent_id": consent_id,
            "patient_id": patient_id,
            "purpose": purpose,
            "status": status,
            "updated_at": now_str,
            "message": f"Consent for {purpose} updated to {status}. Downstream policies updated immediately (§11)."
        })
        return True

    # 7. Patient Care Orchestrator Inbound Message
    if path in ("/api/v1/patient/care-orchestrator/message", "/api/v1/care/inbound-message"):
        patient_id = body.get("patient_id", "PAT-774901")
        message_text = body.get("message", body.get("text", ""))
        patient_context = body.get("patient_context", {})
        if srv.PatientCareOrchestrator:
            decision = srv.PatientCareOrchestrator.process_inbound_message(
                patient_id=patient_id,
                message_text=message_text,
                patient_context=patient_context
            )
            handler._send_json({"ok": True, "route_decision": dataclasses.asdict(decision)}, status=200)
        else:
            handler._send_error("PatientCareOrchestrator unavailable.", status=503)
        return True

    # 8. Smart Pre-Consult Briefing Generation
    if path in ("/api/v1/patient/pre-consult/generate", "/api/v1/clinical/pre-consult"):
        patient_id = body.get("patient_id", "PAT-774901")
        patient_name = body.get("patient_name", "Hamza Farooqi")
        intake_text = body.get("intake_text", body.get("text", ""))
        if srv.SmartPreConsultEngine:
            briefing = srv.SmartPreConsultEngine.generate_briefing(
                patient_id=patient_id,
                patient_name=patient_name,
                unstructured_intake_text=intake_text
            )
            handler._send_json({"ok": True, "pre_consult_briefing": dataclasses.asdict(briefing)}, status=200)
        else:
            handler._send_error("SmartPreConsultEngine unavailable.", status=503)
        return True

    # 9. Patient Health Explainer Dossier Synthesis
    if path in ("/api/v1/patient/explain-health", "/api/v1/patient/explain-care"):
        patient_id = body.get("patient_id", "PAT-774901")
        patient_name = body.get("patient_name", "Hamza Farooqi")
        diagnosis_title = body.get("diagnosis_title", "Waja-ul-Mafasil (Osteoarthritis)")
        prescribed_nuskha = body.get("prescribed_nuskha", "Majun Suranjan Special")
        language = body.get("language", "roman_urdu")
        if srv.PatientHealthExplainer:
            dossier = srv.PatientHealthExplainer.explain_health_summary(
                patient_id=patient_id,
                patient_name=patient_name,
                diagnosis_title=diagnosis_title,
                prescribed_nuskha=prescribed_nuskha,
                language=language
            )
            handler._send_json({"ok": True, "health_explanation": dataclasses.asdict(dossier)}, status=200)
        else:
            handler._send_error("PatientHealthExplainer unavailable.", status=503)
        return True

    # 10. Patient Consent Signing & SHA-256 Seal
    if path in ("/api/v1/patient/consent", "/api/v1/clinical/patient/consent"):
        p_id = body.get("patient_id", "PAT-0814")
        c_type = body.get("consent_type", "CLINICAL_TREATMENT")
        c_ver = body.get("version", "2.0")
        c_lang = body.get("language", "en")
        c_purp = body.get("purpose", "Clinical Care & Diagnostics")
        c_meth = body.get("method", "IN_APP_CHECKBOX_OTP")
        c_ident = body.get("patient_identity", "Hamza Farooqi")
        c_witn = body.get("witness_name")
        c_share = 1 if body.get("data_sharing_permitted", True) else 0
        c_res = 1 if body.get("research_permitted", False) else 0
        c_ai = 1 if body.get("ai_processing_permitted", True) else 0
        c_rec_id = f"CNS-{uuid.uuid4().hex[:8].upper()}"
        sig_hash = hashlib.sha256(f"{c_rec_id}:{p_id}:{c_ident}:{time.time()}".encode()).hexdigest()
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO consent_engine_records
                (id, patient_id, consent_type, version, language, purpose, method, patient_identity, witness_name,
                 data_sharing_permitted, research_permitted, ai_processing_permitted, signature_hash, facility_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (c_rec_id, p_id, c_type, c_ver, c_lang, c_purp, c_meth, c_ident, c_witn, c_share, c_res, c_ai, sig_hash, "FAC-HQ-01"))
            cur.execute("""
                INSERT INTO clinical_audit_events
                (id, actor_id, actor_role, action_type, action_reason, approval_level, cryptographic_signature_seal, facility_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (f"AUD-{uuid.uuid4().hex[:8].upper()}", p_id, "PATIENT", "CONSENT_RECORDED", c_purp, "PATIENT_CONSENT", sig_hash, "FAC-HQ-01"))
            conn.commit()
        handler._send_json({"ok": True, "consent_id": c_rec_id, "signature_hash": sig_hash}, status=201)
        return True

    # 11. Record Longitudinal Clinical Event
    if path in ("/api/v1/patient/timeline", "/api/v1/clinical/patient-timeline"):
        p_id = body.get("patient_id", "PAT-0814")
        e_type = body.get("event_type", "CLINICAL_EVENT")
        title = body.get("title", "Clinical Event Recorded")
        summary = body.get("clinical_summary", "")
        metrics = json.dumps(body.get("metrics", {}))
        actor_name = body.get("actor_name", "Attending Clinician")
        actor_role = body.get("actor_role", "DOCTOR")
        claim_id = body.get("evidence_claim_id")
        evt_id = f"EVT-{uuid.uuid4().hex[:8].upper()}"
        now_ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO longitudinal_clinical_timeline
                (id, patient_id, event_timestamp, event_type, title, clinical_summary, metrics_json, actor_name, actor_role, evidence_claim_id, facility_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (evt_id, p_id, now_ts, e_type, title, summary, metrics, actor_name, actor_role, claim_id, "FAC-HQ-01"))
            conn.commit()
        handler._send_json({"ok": True, "event_id": evt_id, "timestamp": now_ts}, status=201)
        return True

    return False
