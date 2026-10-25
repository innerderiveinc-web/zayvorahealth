"""
ZAYVORA Health OS — Clinical Intelligence & Diagnostics Domain Router
======================================================================
Modular request dispatcher for:
- 12-Organ Axis Physiological Scoring and Patient 360 Axis Maps
- Asbab-e-Sittah Zarooriya Lifestyle Equilibrium Evaluation
- Classical Diagnostics: Qaroorah (Urinalysis) & Baraaz (Alimentary)
- Volume II 8-Parhez Dietary & Clinical Restriction Protocols
"""

from typing import Any, Dict


def handle_clinical_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for clinical dietary protocols and diagnostic registries."""
    import services.live_api_server as srv

    # 1. Volume II 8 Parhez Clinical Protocols: Catalog
    if path in ("/api/v1/clinical/parhez-8/all", "/api/v1/clinical/parhez-8"):
        handler._send_json({
            "ok": True,
            "framework": "8 Parhez Clinical Protocols (Volume II)",
            "total_protocols": len(srv.get_all_parhez_protocols()),
            "protocols": srv.get_all_parhez_protocols()
        })
        return True

    # 2. Volume II 8 Parhez Clinical Protocols: Single Code Lookup
    if path.startswith("/api/v1/clinical/parhez-8/"):
        pz_code = path.split("/")[-1].upper()
        pz_data = srv.get_parhez_protocol_by_code(pz_code)
        if pz_data:
            handler._send_json({"ok": True, "parhez": pz_data})
        else:
            handler._send_error(f"Parhez protocol '{pz_code}' not found.", status=404, code="PARHEZ_NOT_FOUND")
        return True

    return False


def handle_clinical_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for 12-Organ Axis scoring, Asbab-e-Sittah, and classical diagnostics."""
    import services.live_api_server as srv

    # 1. ZAYVORA 12-Axis Clinical Intelligence Framework: Calculate Activity
    if path == "/api/v1/clinical/axes-12/score":
        axis_id = body.get("axis_id", "AXIS_01")
        sym = float(body.get("symptoms_score", 0))
        hist = float(body.get("history_score", 0))
        inv = float(body.get("investigations_score", 0))
        life = float(body.get("lifestyle_score", 0))
        clin = body.get("clinician_assessment")
        red = bool(body.get("has_red_flags", False))
        if srv.TwelveAxisEngine:
            res = srv.TwelveAxisEngine.calculate_single_axis_activity(axis_id, sym, hist, inv, life, clin, red)
            handler._send_json({"ok": True, "axis_score": res})
        else:
            handler._send_error("12-Axis engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 2. ZAYVORA 12-Axis: Patient 360 Axis Map
    if path == "/api/v1/clinical/axes-12/patient-map":
        patient_data = body.get("patient_data", body)
        if srv.TwelveAxisEngine:
            res = srv.TwelveAxisEngine.generate_patient_360_axis_map(patient_data)
            handler._send_json({"ok": True, "patient_360_map": res})
        else:
            handler._send_error("12-Axis engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 3. ZAYVORA 12-Axis: AI Draft Synthesis
    if path == "/api/v1/clinical/axes-12/ai-draft":
        patient_summary = body.get("patient_summary", body)
        if srv.TwelveAxisEngine:
            res = srv.TwelveAxisEngine.generate_hakeem_sahab_ai_draft(patient_summary)
            handler._send_json({"ok": True, "hakeem_sahab_draft": res})
        else:
            handler._send_error("12-Axis engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 4. Classical Qaroorah (Urine) & Modern Urinalysis Diagnostics
    if path in ("/api/v1/clinical/diagnostics/qaroorah-analyze", "/api/v1/clinical/qaroorah"):
        patient_id = body.get("patient_id", "P-ANON")
        insp_data = body.get("inspection", {})
        labs_data = body.get("modern_labs", {})
        clinical_ctx = body.get("clinical_context", {})
        if srv.QaroorahDiagnosticEngine and srv.QaroorahPhysicalInspection and srv.ModernUrinalysisData:
            insp = srv._safe_instantiate_dataclass(srv.QaroorahPhysicalInspection, insp_data)
            labs = srv._safe_instantiate_dataclass(srv.ModernUrinalysisData, labs_data)
            res = srv.QaroorahDiagnosticEngine.analyze_qaroorah(patient_id, insp, labs, clinical_ctx)
            handler._send_json({"ok": True, "qaroorah_diagnostic": res})
        else:
            handler._send_error("Qaroorah diagnostic engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 5. Classical Baraaz (Stool & Alimentary) Diagnostics
    if path in ("/api/v1/clinical/diagnostics/baraaz-analyze", "/api/v1/clinical/baraaz"):
        patient_id = body.get("patient_id", "P-ANON")
        insp_data = body.get("inspection", {})
        clinical_ctx = body.get("clinical_context", {})
        if srv.BaraazDiagnosticEngine and srv.BaraazInspectionInput:
            inp = srv._safe_instantiate_dataclass(srv.BaraazInspectionInput, insp_data)
            res = srv.BaraazDiagnosticEngine.analyze_baraaz(patient_id, inp, clinical_ctx)
            handler._send_json({"ok": True, "baraaz_diagnostic": res})
        else:
            handler._send_error("Baraaz diagnostic engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    # 6. Asbab Sitta Zarooriya Dynamic Lifestyle Scoring
    if path in ("/api/v1/clinical/lifestyle/asbab-sitta-score", "/api/v1/clinical/asbab-sitta"):
        patient_id = body.get("patient_id", "P-ANON")
        patient_mizaj = body.get("patient_mizaj", "Motadil")
        lifestyle_data = body.get("lifestyle", {})
        if srv.AsbabSittaScoringEngine and srv.AsbabSittaPatientInput:
            inp = srv._safe_instantiate_dataclass(srv.AsbabSittaPatientInput, lifestyle_data)
            res = srv.AsbabSittaScoringEngine.evaluate_lifestyle_equilibrium(patient_id, patient_mizaj, inp)
            handler._send_json({"ok": True, "asbab_sitta_evaluation": res})
        else:
            handler._send_error("Asbab Sitta scoring engine unavailable.", status=500, code="ENGINE_UNAVAILABLE")
        return True

    return False
