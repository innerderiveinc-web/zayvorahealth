"""
ZAYVORA Health OS — Agentic Domain Router
==========================================
Modular request dispatcher for Autonomous AI Clinical, Research, and Operations Agents:
1. Proactive Pre-Consultation Agent (Autonomous Triage)
2. Autonomous Canonical Research Agent
3. Closed-Loop Care Continuity Agent
4. Clinician Reinforcement Agent
5. Cloud Deployment & Multi-Device Sync Engine
6. Autonomous Pharmacy & FEFO Inventory Agent
7. Autonomous Diagnostic Vision Agent
8. Autonomous Voice Scribe Agent
"""

from typing import Any, Dict


def handle_agentic_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for agentic pipelines. Returns True if handled, False otherwise."""
    import services.live_api_server as srv

    # 1. Proactive Pre-Consultation Agent (Autonomous Triage)
    if path == "/api/v1/clinical/agent/pre-consult-brief":
        target_mrn = query_params.get("mrn", ["PAT-0816"])[0]
        with srv.get_db() as conn:
            brief = srv.generate_proactive_pre_consult_brief(mrn=target_mrn, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-ProactiveTriage", "brief": brief})
        return True

    # 2. Autonomous Canonical Research Agent
    if path in ("/api/v1/research/agent/canonical-dossier", "/api/v1/research/canonical-dossier"):
        target_query = query_params.get("query", ["Waja-ul-Mafasil"])[0]
        depth = query_params.get("depth", ["comprehensive"])[0]
        with srv.get_db() as conn:
            dossier = srv.generate_canonical_evidence_dossier(query=target_query, depth=depth, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-CanonResearchAgent", "dossier": dossier})
        return True

    # 3. Closed-Loop Care Continuity Agent: Status
    if path in ("/api/v1/clinical/agent/care-continuity/status", "/api/v1/clinical/care-continuity/status"):
        target_mrn = query_params.get("mrn", ["PAT-0816"])[0]
        with srv.get_db() as conn:
            status_res = srv.get_care_continuity_status(mrn=target_mrn, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-CareContinuityAgent", "plan": status_res})
        return True

    # 4. Clinician Reinforcement Agent: Preference Matrix
    if path in ("/api/v1/clinical/agent/reinforcement/matrix", "/api/v1/clinical/reinforcement/matrix"):
        target_axis = query_params.get("axis", [None])[0]
        target_form = query_params.get("formulation", [None])[0]
        limit_val = int(query_params.get("limit", ["50"])[0])
        with srv.get_db() as conn:
            matrix_res = srv.get_reinforcement_matrix(organ_axis=target_axis, formulation_name=target_form, limit=limit_val, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-ReinforcementAgent", "preferences": matrix_res})
        return True

    # 5. Cloud Deployment & Multi-Device Sync: Delta Sync
    if path in ("/api/v1/sync/delta", "/api/v1/sync/status"):
        dev_id = query_params.get("device_id", ["MOBILE-01"])[0]
        since_ts = query_params.get("since", [None])[0]
        with srv.get_db() as conn:
            sync_delta = srv.get_sync_delta(device_id=dev_id, since=since_ts, conn=conn)
        handler._send_json(sync_delta)
        return True

    # 6. Autonomous Pharmacy & FEFO Inventory Agent: Audit
    if path in ("/api/v1/pharmacy/agent/inventory-audit", "/api/v1/pharmacy/inventory-audit"):
        fac_id = query_params.get("facility_id", ["FAC-HQ-01"])[0]
        with srv.get_db() as conn:
            audit_res = srv.run_pharmacy_inventory_audit(facility_id=fac_id, conn=conn)
        handler._send_json(audit_res)
        return True

    # 7. Autonomous Diagnostic Vision Agent: Analyses History
    if path in ("/api/v1/clinical/agent/vision/analyses", "/api/v1/clinical/vision/analyses"):
        target_mrn = query_params.get("mrn", ["PAT-0816"])[0]
        with srv.get_db() as conn:
            v_analyses = srv.get_diagnostic_vision_analyses(mrn=target_mrn, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-DiagnosticVisionAgent", "analyses": v_analyses})
        return True

    # 8. Autonomous Voice Scribe Agent: History
    if path in ("/api/v1/clinical/agent/voice/history", "/api/v1/clinical/voice/history"):
        target_mrn = query_params.get("mrn", ["PAT-0816"])[0]
        with srv.get_db() as conn:
            v_hist = srv.get_voice_consultation_history(mrn=target_mrn, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-VoiceAgenticScribe", "history": v_hist})
        return True

    return False


def handle_agentic_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for agentic pipelines. Returns True if handled, False otherwise."""
    import services.live_api_server as srv

    # 1. Proactive Pre-Consultation Agent (Autonomous Triage)
    if path in ("/api/v1/clinical/agent/pre-consult-brief", "/api/v1/clinical/pre-consult-brief"):
        mrn = body.get("mrn", "PAT-0816")
        p_name = body.get("patient_name", "")
        age = int(body.get("age", 40))
        gender = body.get("gender", "Male")
        vitals = body.get("vitals", {})
        complaint = body.get("chief_complaint", "")
        mizaj = body.get("mizaj", "")
        allopathic = body.get("allopathic_meds", [])
        with srv.get_db() as conn:
            brief = srv.generate_proactive_pre_consult_brief(
                mrn=mrn, patient_name=p_name, age=age, gender=gender,
                vitals=vitals, chief_complaint=complaint, mizaj=mizaj,
                allopathic_meds=allopathic, conn=conn
            )
        handler._send_json({"ok": True, "agent_version": "v1.0-ProactiveTriage", "brief": brief})
        return True

    # 2. Autonomous Canonical Research Agent
    if path in ("/api/v1/research/agent/canonical-dossier", "/api/v1/research/canonical-dossier"):
        target_query = body.get("query", "Waja-ul-Mafasil")
        depth = body.get("depth", "comprehensive")
        with srv.get_db() as conn:
            dossier = srv.generate_canonical_evidence_dossier(query=target_query, depth=depth, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-CanonResearchAgent", "dossier": dossier})
        return True

    # 3. Closed-Loop Care Continuity Agent: Evaluate Nujz & Transition
    if path in ("/api/v1/clinical/agent/care-continuity/evaluate-nujz", "/api/v1/clinical/care-continuity/evaluate-nujz"):
        mrn = body.get("mrn", "PAT-0816")
        day = int(body.get("day", 1))
        adherence = bool(body.get("adherence_confirmed", True))
        qaroorah = str(body.get("qaroorah_sediment", "normal"))
        bowel = bool(body.get("bowel_regular", True))
        pulse = str(body.get("pulse_quality", "batee"))
        stiff = int(body.get("stiffness_resolved_pct", 20))
        tongue = bool(body.get("tongue_clearing", False))
        notes = str(body.get("notes", ""))
        with srv.get_db() as conn:
            res = srv.evaluate_care_continuity_nujz(
                mrn=mrn, day=day, adherence_confirmed=adherence,
                qaroorah_sediment=qaroorah, bowel_regular=bowel,
                pulse_quality=pulse, stiffness_resolved_pct=stiff,
                tongue_clearing=tongue, notes=notes, conn=conn
            )
        handler._send_json({"ok": True, "agent_version": "v1.0-CareContinuityAgent", "evaluation": res})
        return True

    if path in ("/api/v1/clinical/agent/care-continuity/transition-stage", "/api/v1/clinical/care-continuity/transition-stage"):
        mrn = body.get("mrn", "PAT-0816")
        target_phase = body.get("target_phase", "PHASE_2_TANQIYA")
        doc_id = body.get("doctor_id", "DOC-01")
        notes = body.get("notes", "")
        with srv.get_db() as conn:
            res = srv.transition_care_continuity_stage(mrn=mrn, target_phase=target_phase, doctor_id=doc_id, notes=notes, conn=conn)
        handler._send_json({"ok": True, "agent_version": "v1.0-CareContinuityAgent", "transition": res})
        return True

    # 4. Clinician Reinforcement Agent: Record Override
    if path in ("/api/v1/clinical/agent/reinforcement/record-override", "/api/v1/clinical/reinforcement/record-override"):
        mrn = body.get("mrn", "PAT-0816")
        doc_id = body.get("doctor_id", "DOC-01")
        form_name = body.get("formulation_name", "")
        ai_dose = body.get("ai_proposed_dose", "")
        doc_dose = body.get("doctor_prescribed_dose", "")
        action = body.get("action_type", "DOSE_CHANGE")
        rationale = body.get("clinical_rationale", "")
        organ_axis = body.get("organ_axis", "General")
        if not form_name:
            handler._send_json({"ok": False, "error": "formulation_name is required"}, status=400)
            return True
        with srv.get_db() as conn:
            res = srv.record_clinician_override(
                mrn=mrn, doctor_id=doc_id, formulation_name=form_name,
                ai_proposed_dose=ai_dose, doctor_prescribed_dose=doc_dose,
                action_type=action, clinical_rationale=rationale, organ_axis=organ_axis,
                conn=conn
            )
        handler._send_json({"ok": True, "agent_version": "v1.0-ReinforcementAgent", "result": res})
        return True

    # 5. Cloud Deployment & Multi-Device Sync: Batch Mutations
    if path in ("/api/v1/sync/batch", "/api/v1/sync/mutations"):
        dev_id = body.get("device_id", "MOBILE-01")
        muts = body.get("mutations", [])
        with srv.get_db() as conn:
            batch_res = srv.process_sync_batch(device_id=dev_id, mutations=muts, conn=conn)
        handler._send_json(batch_res)
        return True

    # 6. Autonomous Pharmacy & FEFO Inventory Agent: Authorize PO
    if path in ("/api/v1/pharmacy/agent/authorize-po", "/api/v1/pharmacy/authorize-po"):
        po_num = body.get("po_number", "ALL_DRAFT")
        auth_by = body.get("authorized_by", "PHARM-01")
        notes = body.get("notes", "")
        with srv.get_db() as conn:
            auth_res = srv.authorize_purchase_order(po_number=po_num, authorized_by=auth_by, notes=notes, conn=conn)
        handler._send_json(auth_res)
        return True

    # 7. Autonomous Diagnostic Vision Agent: Analyze Media
    if path in ("/api/v1/clinical/agent/vision/analyze", "/api/v1/clinical/vision/analyze"):
        att_id = body.get("attachment_id")
        mrn = body.get("mrn", "PAT-0816")
        modality = body.get("modality", "AUTO")
        raw_fn = body.get("file_name", "")
        with srv.get_db() as conn:
            v_res = srv.analyze_diagnostic_media(attachment_id=att_id, mrn=mrn, modality=modality, raw_filename=raw_fn, conn=conn)
        handler._send_json(v_res)
        return True

    # 8. Autonomous Voice Scribe Agent: Transcribe & Structure
    if path in ("/api/v1/clinical/agent/voice/transcribe-structure", "/api/v1/clinical/voice/transcribe-structure"):
        txt = body.get("transcript", "")
        mrn = body.get("mrn", "PAT-0816")
        with srv.get_db() as conn:
            scribe_res = srv.parse_and_structure_voice_consultation(transcript=txt, mrn=mrn, conn=conn)
        handler._send_json(scribe_res)
        return True

    return False
