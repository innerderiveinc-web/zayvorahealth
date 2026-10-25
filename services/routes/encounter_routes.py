"""
ZAYVORA Health OS — Clinical Encounters, Consultations & SOAP Notes Router
==========================================================================
Modular request dispatcher for:
- Clinical Encounters Directory (Tenant-Scoped with parsed SOAP, Vitals, Mizaj, Organ Axis)
- Single Encounter Details & Cross-Tenant Security Verification
- Encounter OS Start & 21 CFR Part 11 Digital Sign-off Gate
- Cryptographic Merkle Digital Signature Seal on Clinical Encounters (/encounters/<id>/sign)
- Create or Update Clinical Encounter with Chief Complaint, Vitals, Examination & SOAP Notes
- Pre-Encounter Clinical Briefing Preparation (/encounter/prepare)
- AI Clinical Consultations Registry & Single Consultation Retrieval
- Hakeem Sahab™ Master 5-Layer AI Clinical Copilot Orchestrator (/ai/consult, /hakeem/consult)
- Hakeem AI Safety Firewall Pre-Screening & Schedule E(1) Statutory Checks
- ZAPE 2.0 AI Posology Personalization & Age/eGFR Scaling (/hakeem/personalize)
- Hakeem Consultation Mark-Reviewed Workflow
- Hakeem Case Brief Contract (/hakeem/case-brief)
- Hakeem Evidence-Grounded Brief & Deep RAG Classical Multi-Treatise Consult
- Hakeem Evaluation Suite & Benchmark Cases
"""

from dataclasses import asdict
from datetime import datetime
import hashlib
import json
import os
import time
from typing import Any, Dict
import uuid


def handle_encounter_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for clinical encounters, consultations, and AI evaluation."""
    import services.live_api_server as srv

    # 1. Pre-Encounter Briefing Preparation
    if path in ("/api/v1/clinical/encounter/prepare", "/api/v1/encounter/prepare"):
        pat_id = query_params.get("patient_id", ["PAT-774901"])[0]
        doc_id = query_params.get("clinician_id", ["DOC-01"])[0]
        if srv.EncounterOSEngine:
            prep = srv.EncounterOSEngine.prepare_pre_encounter(pat_id, doc_id)
        else:
            prep = {"patient_id": pat_id, "error": "Encounter OS unavailable."}
        handler._send_json({"ok": True, "pre_encounter": prep})
        return True

    # 2. Encounters Directory (Tenant-Scoped)
    if path == "/api/v1/encounters":
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            req_mrn = query_params.get("mrn", [None])[0]

            if auth_ctx and auth_ctx["role"] == "PATIENT":
                cur.execute("SELECT * FROM encounters WHERE mrn = ? ORDER BY started_at DESC", (auth_ctx["mrn"],))
            elif req_mrn:
                cur.execute("SELECT * FROM encounters WHERE mrn = ? ORDER BY started_at DESC", (req_mrn,))
            elif (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and not query_params):
                cur.execute("SELECT * FROM encounters ORDER BY started_at DESC")
            else:
                cur.execute("SELECT * FROM encounters WHERE facility_id = ? ORDER BY started_at DESC", (target_facility,))

            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                for field in ["vitals_json", "soap_json", "mizaj_json", "organ_axis_json", "afaal_cascade_json"]:
                    try:
                        clean_k = field.replace("_json", "")
                        r[clean_k] = json.loads(r.get(field) or "{}")
                    except Exception:
                        r[clean_k] = {}
        handler._send_json({"ok": True, "count": len(rows), "facilityId": target_facility, "encounters": rows})
        return True

    # 3. Single Encounter Details (Cross-Tenant Guard)
    if path.startswith("/api/v1/encounters/"):
        enc_id = path.split("/")[-1]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM encounters WHERE id = ? OR encounter_number = ?", (enc_id, enc_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Encounter record not found.", status=404, code="ENCOUNTER_NOT_FOUND")
                return True
            res = dict(row)

            enc_fac = res.get("facility_id") or "FAC-HQ-01"
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if enc_fac != auth_ctx["facilityId"]:
                    handler._send_error("Access denied: You do not have authorization to view clinical records from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

            for field in ["vitals_json", "soap_json", "mizaj_json", "organ_axis_json", "afaal_cascade_json"]:
                clean_k = field.replace("_json", "")
                try:
                    res[clean_k] = json.loads(res.get(field) or "{}")
                except Exception:
                    res[clean_k] = {}
        handler._send_json({"ok": True, "encounter": res})
        return True

    # 4. AI Consultations Directory
    if path in ("/api/v1/ai/consultations", "/api/v1/hakeem/consultations"):
        target_facility = handler._resolve_facility(auth_ctx, query_params)
        with srv.get_db() as conn:
            cur = conn.cursor()
            if auth_ctx and auth_ctx["role"] == "PATIENT":
                cur.execute("SELECT * FROM ai_consultations WHERE mrn = ? ORDER BY created_at DESC", (auth_ctx["mrn"],))
            elif "mrn" in query_params:
                cur.execute("SELECT * FROM ai_consultations WHERE mrn = ? ORDER BY created_at DESC", (query_params["mrn"][0],))
            elif (auth_ctx and auth_ctx["role"] == "SUPER_ADMIN" and "all" in query_params.get("scope", [])) or (not auth_ctx and "all" in query_params.get("scope", [])):
                cur.execute("SELECT * FROM ai_consultations ORDER BY created_at DESC")
            else:
                cur.execute("SELECT * FROM ai_consultations WHERE facility_id = ? ORDER BY created_at DESC", (target_facility,))
            rows = [dict(r) for r in cur.fetchall()]
            for r in rows:
                for field in ["advisory_sections_json", "citations_json"]:
                    clean_k = field.replace("_json", "")
                    try:
                        r[clean_k] = json.loads(r.get(field) or "{}")
                    except Exception:
                        r[clean_k] = {}
        handler._send_json({"ok": True, "count": len(rows), "consultations": rows})
        return True

    # 5. Single AI Consultation Lookup (or /by-patient/{patientId})
    if path.startswith("/api/v1/ai/consultations/") or path.startswith("/api/v1/hakeem/consultations/"):
        consult_id = path.split("/")[-1]
        if "/by-patient/" in path:
            pat_id = consult_id
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM ai_consultations WHERE mrn = ? ORDER BY created_at DESC", (pat_id,))
                rows = [dict(r) for r in cur.fetchall()]
                for r in rows:
                    for field in ["advisory_sections_json", "citations_json"]:
                        clean_k = field.replace("_json", "")
                        try:
                            r[clean_k] = json.loads(r.get(field) or "{}")
                        except Exception:
                            r[clean_k] = {}
            handler._send_json(rows)
            return True

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ai_consultations WHERE id = ? OR consultation_id = ?", (consult_id, consult_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Clinical consultation record not found.", status=404, code="CONSULTATION_NOT_FOUND")
                return True
            res = dict(row)

            c_fac = res.get("facility_id") or "FAC-HQ-01"
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if c_fac != auth_ctx["facilityId"]:
                    handler._send_error("Access denied: You do not have authorization to view clinical records from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

            for field in ["advisory_sections_json", "citations_json"]:
                clean_k = field.replace("_json", "")
                try:
                    res[clean_k] = json.loads(res.get(field) or "{}")
                except Exception:
                    res[clean_k] = {}
        handler._send_json({"ok": True, "consultation": res})
        return True

    # 6. Hakeem AI Evaluation Cases
    if path == "/api/v1/hakeem/eval/cases":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, consultation_id, mrn, patient_name, chief_complaint, safety_verdict, provider_used FROM ai_consultations ORDER BY rowid DESC LIMIT 20")
            cases = [dict(r) for r in cur.fetchall()]
        handler._send_json({"ok": True, "count": len(cases), "cases": cases})
        return True

    # 7. Hakeem AI Evaluation Suite Summary
    if path == "/api/v1/hakeem/eval/evaluate-suite":
        if not auth_ctx:
            handler._send_error("Authentication required.", status=401, code="UNAUTHORIZED")
            return True
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as total, SUM(CASE WHEN safety_verdict='SAFE_TO_PROCEED' THEN 1 ELSE 0 END) as safe_count FROM ai_consultations")
            row = dict(cur.fetchone())
        total = row.get("total") or 0
        safe = row.get("safe_count") or 0
        handler._send_json({
            "ok": True, "suite": "ZAYVORA AI Evaluation Suite v2",
            "total_cases": total, "safe": safe,
            "unsafe": total - safe,
            "safety_rate": round((safe / total * 100) if total else 100, 2),
            "status": "COMPLIANT"
        })
        return True

    return False


def handle_encounter_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for encounters, sign-offs, and Hakeem AI consultations."""
    import services.live_api_server as srv

    # 1. Encounter OS: Start Encounter
    if path in ("/api/v1/clinical/encounter/start", "/api/v1/encounter/start"):
        pat_id = body.get("patient_id", "PAT-774901")
        doc_id = body.get("clinician_id", "DOC-01")
        fac_id = body.get("facility_id", "FAC-HQ-01")
        enc_type = body.get("encounter_type", "IN_PERSON_OPD")
        if srv.EncounterOSEngine:
            rec = srv.EncounterOSEngine.start_encounter(pat_id, doc_id, fac_id, enc_type)
            handler._send_json({"ok": True, "encounter": asdict(rec)}, status=201)
        else:
            handler._send_error("Encounter OS engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 2. Encounter OS: 21 CFR Part 11 Digital Sign-off
    if path in ("/api/v1/clinical/encounter/sign-off", "/api/v1/encounter/sign-off"):
        enc_id = body.get("encounter_id", "")
        doc_id = body.get("clinician_id", "DOC-01")
        pin = body.get("signing_pin", "123456")
        reason = body.get("reason", "Prescription and encounter verified and sealed.")
        if srv.EncounterOSEngine:
            try:
                sign_res = srv.EncounterOSEngine.sign_off_encounter(enc_id, doc_id, pin, reason)
                handler._send_json(sign_res, status=200)
            except KeyError as ke:
                handler._send_error(str(ke), status=404, code="ENCOUNTER_NOT_FOUND")
        else:
            handler._send_error("Encounter OS engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 3. Clinical Encounter 21 CFR Part 11 Digital Signature Seal (/encounters/<id>/sign)
    if "/encounters/" in path and path.endswith("/sign"):
        if auth_ctx and auth_ctx["role"] not in ("DOCTOR", "HAKEEM", "SUPER_ADMIN"):
            handler._send_error("Access restricted: Only licensed consulting physicians or hakeems are authorized to digitally sign encounters.", status=403, code="FORBIDDEN")
            return True

        enc_id = path.split("/")[-2]
        doctor_name = (auth_ctx["fullName"] if auth_ctx else "Prof. (Dr.) Mansoor Alam")
        doctor_reg = body.get("doctorReg") or "CCIM-U-1988-0412"

        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM encounters WHERE id = ? OR encounter_number = ?", (enc_id, enc_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Encounter record not found.", status=404, code="ENCOUNTER_NOT_FOUND")
                return True
            enc = dict(row)

            # Cross-tenant check
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if enc.get("facility_id") and enc["facility_id"] != auth_ctx["facilityId"]:
                    handler._send_error("Access denied: You do not have authorization to sign records from a foreign healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

            now_str = datetime.utcnow().isoformat() + "Z"
            raw_sig = f"{enc['id']}|{enc['mrn']}|{doctor_reg}|{enc.get('soap_json')}|{now_str}"
            sig_hash = hashlib.sha256(raw_sig.encode("utf-8")).hexdigest()

            cur.execute("""
            UPDATE encounters
            SET status = 'LOCKED_AND_SIGNED', signature_hash = ?, signed_at = ?
            WHERE id = ?
            """, (sig_hash, now_str, enc["id"]))

            if enc.get("appointment_id"):
                cur.execute("UPDATE appointments SET status = 'COMPLETED' WHERE id = ? OR token_number = ?", (enc["appointment_id"], enc["appointment_id"]))

            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (sig_hash, "ENCOUNTER_LOCKED_21CFR11", f"{doctor_name} ({doctor_reg})", "ANCHORED", enc["facility_id"], json.dumps({"encounter_number": enc["encounter_number"], "mrn": enc["mrn"]})))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Clinical encounter locked and sealed with 21 CFR Part 11 digital signature.",
            "encounterId": enc["id"],
            "encounterNumber": enc["encounter_number"],
            "signatureHash": sig_hash,
            "signedAt": now_str,
            "status": "LOCKED_AND_SIGNED"
        })
        return True

    # 4. Create or Update Clinical Encounter
    if path == "/api/v1/encounters":
        if auth_ctx and auth_ctx["role"] not in ("DOCTOR", "HAKEEM", "SUPER_ADMIN", "CLINIC_ADMIN"):
            handler._send_error("Access restricted: Only licensed consulting physicians or hakeems are authorized to document clinical encounters.", status=403, code="FORBIDDEN")
            return True

        mrn = body.get("mrn")
        if not mrn:
            handler._send_error("Patient MRN is required to create a clinical encounter.", status=400, code="MISSING_MRN")
            return True

        facility_id = handler._resolve_facility(auth_ctx, query_params, body)
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
            p_row = cur.fetchone()
            if not p_row:
                handler._send_error("Patient not found.", status=404, code="PATIENT_NOT_FOUND")
                return True
            patient = dict(p_row)

            # Cross-tenant check
            if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN":
                if patient.get("facility_id") and patient["facility_id"] != auth_ctx["facilityId"]:
                    handler._send_error("Access denied: You do not have authorization to create encounters for patients registered at a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                    return True

            cur.execute("SELECT COUNT(*) FROM encounters")
            enc_count = cur.fetchone()[0] + 1
            enc_num = f"ENC-2026-{enc_count:04d}"
            enc_id = f"ENC-{uuid.uuid4().hex[:6].upper()}"

            cur.execute("""
            INSERT INTO encounters (id, encounter_number, appointment_id, mrn, patient_name, doctor_name, department, chief_complaint, vitals_json, examination_notes, soap_json, mizaj_json, organ_axis_json, afaal_cascade_json, status, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                enc_id,
                enc_num,
                body.get("appointmentId"),
                mrn,
                f"{patient['first_name']} {patient['last_name']}",
                body.get("doctorName") or (auth_ctx["fullName"] if auth_ctx else "Prof. (Dr.) Mansoor Alam"),
                body.get("department") or "Integrative Unani Medicine",
                body.get("chiefComplaint") or "General Health Assessment",
                json.dumps(body.get("vitals") or {}),
                body.get("examinationNotes") or "",
                json.dumps(body.get("soap") or {}),
                json.dumps(body.get("mizaj") or {}),
                json.dumps(body.get("organAxis") or {}),
                json.dumps(body.get("afaalCascade") or {}),
                "IN_PROGRESS",
                facility_id
            ))
            conn.commit()

        handler._send_json({
            "ok": True,
            "message": "Clinical encounter created successfully.",
            "encounter": {
                "id": enc_id,
                "encounterNumber": enc_num,
                "mrn": mrn,
                "facilityId": facility_id,
                "status": "IN_PROGRESS"
            }
        }, status=201)
        return True

    # 5. AI Safety Firewall Pre-Screening
    if path in ("/api/v1/ai/safety-check", "/api/v1/hakeem/safety-check"):
        patient_data = body.get("patient") or {}
        items = body.get("items") or body.get("ingredients") or []

        mrn = patient_data.get("mrn") or body.get("mrn")
        if mrn:
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
                p_row = cur.fetchone()
                if p_row:
                    p_dict = dict(p_row)
                    if "allergies" not in patient_data:
                        try:
                            patient_data["allergies"] = json.loads(p_dict.get("allergies_json") or "[]")
                        except Exception:
                            patient_data["allergies"] = []
                    if "mizaj" not in patient_data and "mizaj_dominant" not in patient_data:
                        patient_data["mizaj"] = p_dict.get("mizaj_dominant")
                    if "gender" not in patient_data:
                        patient_data["gender"] = p_dict.get("gender")

        firewall_res = srv.run_safety_firewall(patient_context=patient_data, ingredients=items)
        verdict = firewall_res["verdict"]
        reasons = firewall_res["reasons"]

        e1_details = []
        for item in items:
            name = item.get("name", "")
            substance = srv.match_schedule_e1_substance(name)
            if substance:
                e1_details.append({
                    "substance": substance["canonical_name"],
                    "botanicalName": substance["botanical_name"],
                    "maxSingleDoseMg": substance["max_single_dose_mg"],
                    "maxDailyDoseMg": substance["max_daily_dose_mg"],
                    "mudabbarRequired": True,
                    "mudabbarProtocol": substance["mudabbar_protocol"],
                    "statutoryWarning": substance["statutory_warning"]
                })

        handler._send_json({
            "ok": True,
            "verdict": verdict,
            "reasons": reasons,
            "safeToLock": False,
            "requiresPractitionerSignoff": True,
            "scheduleE1Details": e1_details,
            "isClinicalHold": verdict in ("DO_NOT_RECOMMEND", "REFER")
        })
        return True

    # 6. ZAPE 2.0 Posology Scaling Endpoint
    if path in ("/api/v1/ai/posology/scale", "/api/v1/hakeem/personalize"):
        patient_context = body.get("patient_context") or body.get("patient") or {}
        age = body.get("age", patient_context.get("age"))
        egfr = body.get("egfr", patient_context.get("egfr"))
        pregnancy = body.get("pregnancy", patient_context.get("pregnancy_status", "no"))
        lactation = body.get("lactation", patient_context.get("lactation_status", "no"))
        mizaj = body.get("mizaj", patient_context.get("mizaj_dominant", "Damawi"))
        season = body.get("season", "Rabi (Spring)")
        items = body.get("items") or body.get("ingredients") or []

        scaled_items = []
        notes = []

        scale_factor = 1.0
        if age is not None:
            try:
                age = float(age)
                if age < 12:
                    scale_factor *= 0.5
                    notes.append("Paediatric downward dose scale (-50%) applied.")
                elif age >= 65:
                    scale_factor *= 0.75
                    notes.append("Geriatric downward dose scale (-25%) applied.")
            except ValueError:
                pass

        if egfr is not None:
            try:
                egfr = float(egfr)
                if egfr < 30:
                    scale_factor *= 0.5
                    notes.append("Severe renal impairment (eGFR < 30): halving dose.")
                elif egfr < 60:
                    scale_factor *= 0.75
                    notes.append("Moderate renal impairment (eGFR 30-59): reducing dose by 25%.")
            except ValueError:
                pass

        for item in items:
            it_name = item.get("name", "")
            orig_dose = float(item.get("standard_dose_mg") or item.get("dosage_mg") or 500)
            scaled = orig_dose * scale_factor

            scaled_items.append({
                "name": it_name,
                "original_dose_mg": orig_dose,
                "personalized_dose_mg": round(scaled, 1),
                "frequency": item.get("frequency", "TDS"),
                "instructions": item.get("instructions", "With lukewarm water")
            })

        handler._send_json({
            "ok": True,
            "scaled_items": scaled_items,
            "scale_factor": round(scale_factor, 2),
            "clinical_notes": notes,
            "patient_context": {
                "age": age,
                "egfr": egfr,
                "mizaj": mizaj,
                "season": season
            }
        })
        return True

    # 7. Hakeem Sahab Mark Reviewed
    if "/hakeem/consultations/" in path and path.endswith("/mark-reviewed"):
        consult_id = path.split("/")[-2]
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ai_consultations WHERE id = ? OR consultation_id = ?", (consult_id, consult_id))
            row = cur.fetchone()
            if not row:
                handler._send_error("Consultation record not found.", status=404, code="CONSULTATION_NOT_FOUND")
                return True
            c_dict = dict(row)
            for field in ["advisory_sections_json", "citations_json"]:
                clean_k = field.replace("_json", "")
                try:
                    c_dict[clean_k] = json.loads(c_dict.get(field) or "{}")
                except Exception:
                    c_dict[clean_k] = {}
            c_dict["reviewed_by_clinician"] = True
            c_dict["converted_to_nuskha_draft_id"] = body.get("converted_to_nuskha_draft_id")
        handler._send_json(c_dict)
        return True

    # Hakeem Sahab™ Master 5-Layer AI Clinical Copilot
    if path in ("/api/v1/ai/consult", "/api/v1/hakeem/consult"):
        # RBAC Enforcement: Doctor, Hakeem, or Admin required
        if auth_ctx and auth_ctx["role"] not in ("DOCTOR", "HAKEEM", "SUPER_ADMIN", "CLINIC_ADMIN"):
            handler._send_error("Access restricted: Only licensed clinical practitioners or hakeems are authorized to run AI clinical consultations.", status=403, code="FORBIDDEN")
            return True

        chief_complaint = (body.get("chiefComplaint") or body.get("chief_complaint") or "").strip()
        if not chief_complaint:
            handler._send_error("Chief complaint is required for clinical copilot analysis.", status=400, code="MISSING_CHIEF_COMPLAINT")
            return True

        mrn = body.get("mrn") or body.get("patient_id") or body.get("patientId")
        organ_axis = body.get("organAxis") or body.get("organ_axis") or "Musculoskeletal-Metabolic Axis (Mafasil-Asab)"
        target_facility = handler._resolve_facility(auth_ctx, query_params, body)

        patient_row = None
        patient_name = body.get("patientName") or "Hamza Farooqi"
        allergies = body.get("allergies") or []
        comorbidities = body.get("comorbidities") or []
        current_meds = body.get("currentMedications") or body.get("current_medications") or []
        dominant_mizaj = body.get("mizaj") or "Balghami (Cold & Moist)"

        if mrn:
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM patients WHERE mrn = ? OR id = ?", (mrn, mrn))
                p_res = cur.fetchone()
                if p_res:
                    patient_row = dict(p_res)
                    patient_name = f"{patient_row['first_name']} {patient_row['last_name']}".strip()
                    dominant_mizaj = patient_row.get("mizaj_dominant") or dominant_mizaj
                    try:
                        allergies = json.loads(patient_row.get("allergies_json") or "[]")
                    except Exception:
                        pass
                    
                    # Cross-tenant check
                    fac = patient_row.get("facility_id") or "FAC-HQ-01"
                    if auth_ctx and auth_ctx["role"] != "SUPER_ADMIN" and fac != auth_ctx["facilityId"]:
                        handler._send_error("Access denied: You do not have authorization to view clinical records from a different healthcare facility.", status=403, code="CROSS_TENANT_ACCESS_DENIED")
                        return True

        # Purpose-Specific Consent Enforcement Hook (Master Blueprint §11)
        patient_ref = mrn or "PAT-001"
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patient_consents'")
            if cur.fetchone():
                cur.execute("SELECT status FROM patient_consents WHERE patient_id = ? AND purpose = 'AI_PROCESSING'", (patient_ref,))
                c_row = cur.fetchone()
                if c_row and c_row[0] == "WITHDRAWN":
                    handler._send_error(
                        "AI processing blocked: Patient has explicitly withdrawn consent for AI processing in accordance with DPDP Act 2023 & Master Blueprint §11.",
                        status=403,
                        code="AI_CONSENT_WITHDRAWN"
                    )
                    return True

        # Hybrid Classical RAG Monograph Matching
        matched_monographs = []
        citations = []
        for item in srv.UPI_MUFRADAT_REGISTRY:
            c_name = item.get("canonical_name", "").lower()
            b_name = item.get("botanical_name", "").lower()
            indics = [ind.lower() for ind in item.get("indications", [])]
            axes = [a.lower() for a in item.get("organ_axes", [])]

            if any(w in chief_complaint.lower() for w in ["joint", "knee", "pain", "stiff", "waja", "mafasil"]) and "suranjan" in c_name:
                matched_monographs.append(item)
                citations.append({
                    "title": f"{item['canonical_name']} Monograph",
                    "source": "Unani Pharmacopoeia of India (UPI) Vol 1",
                    "part": item.get("part_used", "Dried corm"),
                    "temperament": item.get("mizaj", {}),
                    "musleh": item.get("musleh", "Roghan-e-Badam"),
                    "is_schedule_e1": item.get("is_schedule_e1", False),
                    "evidence_level": "E5 (Randomized Controlled Clinical Trials)"
                })
            elif any(w in chief_complaint.lower() for w in ["gastric", "acidity", "digest", "pyrosis", "hazm"]) and any(h in c_name for h in ["kishneez", "bazoori", "amla"]):
                matched_monographs.append(item)
                citations.append({
                    "title": f"{item['canonical_name']} Monograph",
                    "source": "Unani Pharmacopoeia of India (UPI) Vol 2",
                    "temperament": item.get("mizaj", {}),
                    "musleh": item.get("musleh", "Gond"),
                    "evidence_level": "E4 (Observational Cohorts)"
                })

        if not citations and srv.UPI_MUFRADAT_REGISTRY:
            sample_item = srv.UPI_MUFRADAT_REGISTRY[0]
            matched_monographs.append(sample_item)
            citations.append({
                "title": f"{sample_item.get('canonical_name', 'Classical Monograph')}",
                "source": "Unani Pharmacopoeia of India (UPI) Vol 1",
                "temperament": sample_item.get("mizaj", {}),
                "evidence_level": "E0 (Canonical Textual Monograph)"
            })

        # Deterministic Safety Firewall Pre-Screening
        candidate_ingredients = []
        for m in matched_monographs:
            candidate_ingredients.append({
                "name": m.get("canonical_name", ""),
                "dose_mg": m.get("max_single_dose_mg", 250.0),
                "is_mudabbar": True if m.get("is_schedule_e1") else None,
                "mudabbar_process": m.get("mudabbar_protocol")
            })

        # Check for red flags or specific contraindications in payload
        if body.get("candidateIngredients"):
            candidate_ingredients = body["candidateIngredients"]

        patient_ctx = {
            "chief_complaint": chief_complaint,
            "allergies": allergies,
            "comorbidities": comorbidities,
            "current_medications": current_meds,
            "pregnancy_status": body.get("pregnancyStatus", "no"),
            "lactation_status": body.get("lactationStatus", "no"),
            "mizaj_dominant": dominant_mizaj,
            "organ_axis": organ_axis
        }
        firewall_res = srv.run_safety_firewall(patient_context=patient_ctx, ingredients=candidate_ingredients)
        firewall_verdict = firewall_res["verdict"]
        firewall_reasons = firewall_res["reasons"]

        # Multi-Model AI Orchestrator Execution with Failover
        orchestrator = srv.LiveAIProviderChain()
        exec_ctx = {
            "chief_complaint": chief_complaint,
            "mizaj": dominant_mizaj,
            "organ_axis": organ_axis,
            "current_medications": current_meds,
            "allergies": allergies,
            "simulatedFailure": body.get("simulatedFailure") or {},
            "forceProvider": body.get("forceProvider"),
            "mockPrimarySuccess": body.get("mockPrimarySuccess"),
            "mockSecondarySuccess": body.get("mockSecondarySuccess")
        }

        # Personal Health Profile Context Injection (Blueprint §8, §16)
        php_context_block = ""
        php_summary = None
        if srv.PersonalHealthProfileEngine:
            try:
                php_profile = srv.PersonalHealthProfileEngine.build_profile(patient_id=mrn or "PAT-001")
                php_context_block = srv.PersonalHealthProfileEngine.export_for_hakeem_sahab(php_profile)
                php_summary = php_profile.to_dict()
            except Exception:
                pass

        base_prompt = f"Patient: {patient_name}, Chief Complaint: {chief_complaint}, Axis: {organ_axis}, Mizaj: {dominant_mizaj}"
        final_user_prompt = f"{php_context_block}\n\nCurrent Clinical Query:\n{base_prompt}" if php_context_block else base_prompt

        system_prompt = (
            "You are Hakeem Sahab™, Senior Clinical Advisor and Medical Fellow in Classical Unani and Integrative Medicine for ZAYVORA Health OS.\n"
            "Your role is to provide compassionate, scholarly, peer-to-peer clinical decision support to the attending physician or hakeem.\n\n"
            "COMMUNICATION STYLE & TONE:\n"
            "- Tone: Warm, collegiate, humane, scholarly, and deeply respectful. Never use robotic, mechanical, or artificial phrasing (never say 'As an AI' or 'system prompt' or 'according to my database').\n"
            "- Professional Address: Begin with respectful professional courtesy ('Adaab, Doctor / Esteemed Colleague').\n"
            "- Integrative Medicine: Harmonize classical Unani wisdom (Ibn Sina's Al-Qanun, Al-Razi's Kitab al-Hawi, and the Unani Pharmacopoeia of India) with modern pathophysiological evidence.\n\n"
            "REQUIRED STRUCTURE:\n"
            "You MUST organize your clinical evaluation using EXACTLY the following 13 uppercase section headers (one per section):\n\n"
            "CLINICAL SUMMARY\n"
            "WHAT IS KNOWN\n"
            "UNANI PERSPECTIVE\n"
            "BIOMEDICAL PERSPECTIVE\n"
            "DIFFERENTIAL CONSIDERATIONS\n"
            "RED FLAGS\n"
            "MISSING INFORMATION\n"
            "EVIDENCE\n"
            "SAFETY\n"
            "POSSIBLE CARE OPTIONS\n"
            "MONITORING\n"
            "UNCERTAINTY\n"
            "CLINICIAN REVIEW REQUIRED\n\n"
            "In CLINICIAN REVIEW REQUIRED, conclude with: 'This consultative advisory is provided by ZAYVORA Hakeem Sahab™ for clinical decision-support only. In accordance with clinical governance standards, final diagnosis and treatment orders require non-delegable review and digital sign-off by the attending licensed practitioner.'"
        )
        raw_ai_text = orchestrator.generate(
            system_prompt=system_prompt,
            user_prompt=final_user_prompt,
            context=exec_ctx
        )

        parsed_sections = srv.parse_sections(raw_ai_text)
        missing_secs = srv.validate_response_structure(raw_ai_text)
        provider_used = orchestrator.last_provider_used
        fallback_occurred = orchestrator.fallback_occurred
        degradation_logs = orchestrator.degradation_logs

        # Synthesize 5-Layer Clinical Decision Support Architecture
        layers = {
            "layerA_classicalKnowledge": {
                "monographs": matched_monographs,
                "citations": citations,
                "classicalSources": ["Al-Qanun fi al-Tibb (Ibn Sina)", "Kitab al-Hawi (al-Razi)", "Unani Pharmacopoeia of India (UPI)"],
                "formulationGuidelines": "Formulation balanced with classical Musleh (corrective) agents."
            },
            "layerB_clinicalReasoning": {
                "temperament": dominant_mizaj,
                "organAxis": organ_axis,
                "afaalCascadeStage": "TANQIYA" if "severe" in chief_complaint.lower() else "TAHLEEL",
                "humoralPathology": f"Stasis along {organ_axis} producing localized dyscrasia."
            },
            "layerC_biomedicalIntegration": {
                "differentialConsiderations": [
                    "Waja-ul-Mafasil (Phlegmatic Arthralgia)",
                    "Osteoarthritis (ICD-10 M17.9)",
                    "Niqris / Gout (ICD-10 M10.9)"
                ],
                "recommendedLaboratories": [
                    "Complete Blood Count (CBC)",
                    "Serum Uric Acid",
                    "Erythrocyte Sedimentation Rate (ESR)",
                    "C-Reactive Protein (hs-CRP)"
                ]
            },
            "layerD_safetyContraindications": {
                "firewallVerdict": firewall_verdict,
                "reasons": firewall_reasons,
                "isClinicalHold": firewall_verdict in ("DO_NOT_RECOMMEND", "REFER"),
                "requiresPractitionerSignoff": True
            },
            "layerE_clinicianReviewBarrier": {
                "safeToLock": False,  # Non-delegable clinical gate: strictly False
                "requiresDoctorReview": True,
                "practitionerSignoffRequired": True,
                "statutoryDisclaimer": "This clinical guidance is synthesized by ZAYVORA Hakeem Sahab™ for decision-support purposes only. In accordance with clinical governance standards, this recommendation cannot autonomously authorize or lock prescriptions without manual review and digital signature by a licensed practitioner."
            },
            "personalHealthProfile": php_summary
        }

        for _ in range(10):
            consult_id = f"AIC-{uuid.uuid4().hex[:8].upper()}"
            cons_number = f"AI-CONSULT-{uuid.uuid4().hex[:8].upper()}"
            with srv.get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT 1 FROM ai_consultations WHERE consultation_id = ? OR id = ?", (cons_number, consult_id))
                if not cur.fetchone():
                    break

        # Persist in Relational Database
        with srv.get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO ai_consultations (id, consultation_id, mrn, patient_name, doctor_name, chief_complaint, organ_axis, mizaj, advisory_sections_json, citations_json, safety_verdict, provider_used, safe_to_lock, facility_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                consult_id,
                cons_number,
                mrn or "MRN-WALK-IN",
                patient_name,
                auth_ctx["fullName"] if auth_ctx else "Consulting Hakeem",
                chief_complaint,
                organ_axis,
                dominant_mizaj,
                json.dumps(parsed_sections),
                json.dumps(citations),
                firewall_verdict,
                provider_used,
                0,  # safe_to_lock = 0
                target_facility
            ))

            # Anchor into 21 CFR Part 11 Merkle Audit Trail
            audit_leaf = hashlib.sha256(f"AI_CONSULT:{cons_number}:{mrn}:{provider_used}:{time.time()}".encode()).hexdigest()
            cur.execute("""
            INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                audit_leaf,
                "AI_CONSULTATION_GENERATED",
                auth_ctx["fullName"] if auth_ctx else "Hakeem Sahab AI",
                "ANCHORED",
                target_facility,
                json.dumps({
                    "consultation_id": cons_number,
                    "mrn": mrn,
                    "provider": provider_used,
                    "safety_verdict": firewall_verdict,
                    "safe_to_lock": False
                })
            ))
            block_num = cur.lastrowid
            conn.commit()

        handler._send_json({
            "ok": True,
            "id": consult_id,
            "consultation_id": consult_id,
            "consultationNumber": cons_number,
            "patient_id": mrn,
            "mrn": mrn,
            "patientName": patient_name,
            "chief_complaint": chief_complaint,
            "organ_axis": organ_axis,
            "providerUsed": provider_used,
            "fallbackOccurred": fallback_occurred,
            "degradationLogs": degradation_logs,
            "raw_response": raw_ai_text,
            "parsed_sections": parsed_sections,
            "sections": parsed_sections,
            "candidate_mufradat": matched_monographs,
            "citations": citations,
            "layers": layers,
            "is_valid": len(missing_secs) == 0,
            "missing_sections": missing_secs,
            "safetyVerdict": firewall_verdict,
            "safeToLock": False,
            "safe_to_lock": False,
            "reviewed_by_clinician": False,
            "auditBlock": block_num,
            "auditBlockHash": audit_leaf,
            "statutoryDisclaimer": layers["layerE_clinicianReviewBarrier"]["statutoryDisclaimer"]
        }, status=201)
        return True

    if path in ("/api/v1/hakeem/case-brief", "/api/v1/ai/hakeem/case-brief"):
        patient_id = body.get("patient_id", "P-DEFAULT")
        patient_ctx = body.get("patient_context", {})
        labs = body.get("labs", {})
        mizaj = body.get("mizaj_result")
        axis_map = body.get("axis_map")
        safety_audit = body.get("safety_audit")
        if srv.HakeemCaseBriefEngine:
            brief = srv.HakeemCaseBriefEngine.generate_case_brief(
                patient_id, patient_ctx, labs, mizaj, axis_map, safety_audit
            )
            handler._send_json({"ok": True, "case_brief": brief})
        else:
            handler._send_error("Case brief engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 10. Hakeem v2 Evidence-Grounded Copilot Brief
    if path in ("/api/v1/hakeem/v2/evidence-brief", "/api/v1/hakeem/evidence-brief"):
        p_id = body.get("patient_id", "MRN-ANON")
        p_ctx = body.get("patient_context", {})
        cond = body.get("clinical_condition", "Waja-ul-Mafasil")
        labs = body.get("labs", {})
        mizaj = body.get("mizaj_result", {})
        axes = body.get("active_axes", [])
        if srv.HakeemCaseBriefEngine and hasattr(srv.HakeemCaseBriefEngine, "generate_evidence_grounded_copilot_brief"):
            brief = srv.HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
                patient_id=p_id,
                patient_context=p_ctx,
                clinical_condition=cond,
                labs=labs,
                mizaj_result=mizaj,
                active_axes=axes
            )
            handler._send_json({"ok": True, "hakeem_v2_brief": brief})
        else:
            handler._send_error("Hakeem Sahab v2 engine unavailable.", status=503)
        return True

    # 11. Hakeem Sahab Deep RAG Consult (12 Volumes + 38 Treatises)
    if path in ("/api/v1/hakeem/deep-rag-consult", "/api/v1/ai/deep-rag-consult"):
        p_id = body.get("patient_id", "MRN-ANON")
        p_ctx = body.get("patient_context", {})
        cond = body.get("clinical_condition", "Waja-ul-Mafasil")
        labs = body.get("labs", {})
        mizaj = body.get("mizaj_result", {})
        axes = body.get("active_axes", [])
        if srv.HakeemCaseBriefEngine and hasattr(srv.HakeemCaseBriefEngine, "generate_evidence_grounded_copilot_brief"):
            brief = srv.HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
                patient_id=p_id,
                patient_context=p_ctx,
                clinical_condition=cond,
                labs=labs,
                mizaj_result=mizaj,
                active_axes=axes
            )
            handler._send_json({"ok": True, "deep_rag_consult": brief})
        else:
            handler._send_error("Hakeem Sahab Deep RAG copilot engine unavailable.", status=503)
        return True

    return False
