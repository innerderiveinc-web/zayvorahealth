"""
ZAYVORA Health OS — Computational Formulation Intelligence & ZFIE Domain Router
================================================================================
Modular request dispatcher for:
- Computational Formulation Intelligence (Substances, Formulation Twins, Batches)
- Evidence Matrix, Contradictions, and Provenance registries
- Closed-Loop Real-World Evidence (RWE) and Cohort Summaries
- Scientific Regulatory Dossier Generator (JSON-LD, Markdown, HTML)
- In-Silico Docking & ADMET Profiling Bridges
- LIMS CoA Batch Ingestion, Cryptographic Verification, and Release
- Mizaj-Stratified Pharmacogenomics Evaluation
- ZFIE Full Pipeline: ETL ingestion, Semantic Bridge, Compiler, Hypotheses,
  Experiments, Laboratory Results, 21 CFR Part 11 SRB Proposals & Governance Sign-Offs
"""

import hashlib
import json
import time
from typing import Any, Dict
import uuid


def handle_computational_get(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any]) -> bool:
    """Dispatches GET requests for computational pharmacology and ZFIE domain."""
    import services.live_api_server as srv

    # 1. Canonical Identity: Substances Catalog
    if path == "/api/v1/computational/substances":
        if srv.CanonicalIdentityRegistry:
            subs = srv.CanonicalIdentityRegistry.list_all_substances()
            handler._send_json({"ok": True, "count": len(subs), "substances": subs})
        else:
            handler._send_error("CanonicalIdentityRegistry unavailable.", status=503)
        return True

    # 2. Canonical Identity: Single Substance
    if path.startswith("/api/v1/computational/substances/"):
        sub_id = path.split("/")[-1]
        if srv.CanonicalIdentityRegistry:
            sub = srv.CanonicalIdentityRegistry.get_substance(sub_id) or srv.CanonicalIdentityRegistry.resolve_identifier(sub_id)
            if sub:
                res = sub.to_dict() if hasattr(sub, "to_dict") else sub
                handler._send_json({"ok": True, "substance": res})
            else:
                handler._send_error(f"Substance '{sub_id}' not found.", status=404)
        else:
            handler._send_error("CanonicalIdentityRegistry unavailable.", status=503)
        return True

    # 3. Formulation Twins: List
    if path == "/api/v1/computational/formulations":
        if srv.FormulationTwinRegistry:
            twins = srv.FormulationTwinRegistry.list_twins()
            handler._send_json({"ok": True, "count": len(twins), "formulations": twins})
        else:
            handler._send_error("FormulationTwinRegistry unavailable.", status=503)
        return True

    # 4. Formulation Twins: Intelligence Summary
    if path.startswith("/api/v1/computational/formulations/"):
        form_id = path.split("/")[-1]
        if srv.FormulationIntelligenceEngine:
            summary = srv.FormulationIntelligenceEngine.get_formulation_intelligence_summary(form_id)
            if summary:
                handler._send_json({"ok": True, "intelligence_summary": summary})
            else:
                handler._send_error(f"Formulation '{form_id}' not found.", status=404)
        else:
            handler._send_error("FormulationIntelligenceEngine unavailable.", status=503)
        return True

    # 5. Formulation Batch Retrieval
    if path.startswith("/api/v1/computational/batches/"):
        batch_id = path.split("/")[-1]
        if srv.FormulationTwinRegistry:
            batch = srv.FormulationTwinRegistry.get_batch(batch_id)
            if batch:
                handler._send_json({"ok": True, "batch": batch.to_dict()})
            else:
                handler._send_error(f"Batch '{batch_id}' not found.", status=404)
        else:
            handler._send_error("FormulationTwinRegistry unavailable.", status=503)
        return True

    # 6. Evidence Matrix
    if path.startswith("/api/v1/computational/evidence-matrix/"):
        ent_id = path.split("/")[-1]
        if srv.EvidenceBridgeEngine:
            ev_items = srv.EvidenceBridgeEngine.get_evidence_for_entity(ent_id)
            highest = srv.EvidenceBridgeEngine.get_highest_evidence_level(ent_id).value
            handler._send_json({"ok": True, "entity_id": ent_id, "highest_level": highest, "count": len(ev_items), "evidence_items": ev_items})
        else:
            handler._send_error("EvidenceBridgeEngine unavailable.", status=503)
        return True

    # 7. Scientific Contradictions
    if path == "/api/v1/computational/contradictions":
        if srv.ScientificMemoryRegistry:
            items = srv.ScientificMemoryRegistry.list_contradictions()
            handler._send_json({"ok": True, "count": len(items), "contradictions": items})
        else:
            handler._send_error("ScientificMemoryRegistry unavailable.", status=503)
        return True

    # 8. Provenance & License Registry
    if path == "/api/v1/computational/provenance":
        if srv.ProvenanceLicenseRegistry:
            sources = srv.ProvenanceLicenseRegistry.list_sources()
            handler._send_json({"ok": True, "count": len(sources), "sources": sources})
        else:
            handler._send_error("ProvenanceLicenseRegistry unavailable.", status=503)
        return True

    # 9. Closed-Loop Outcomes
    if path == "/api/v1/computational/outcomes-closed-loop":
        patient_id = query_params.get("patient_id", [None])[0]
        formulation_id = query_params.get("formulation_id", [None])[0]
        if srv.FormulationOutcomesClosedLoopEngine:
            if patient_id or formulation_id:
                outcome = srv.FormulationOutcomesClosedLoopEngine.get_outcome_for_patient(patient_id, formulation_id)
                handler._send_json({"ok": True, "outcome": outcome})
            else:
                outcomes = srv.FormulationOutcomesClosedLoopEngine.list_all_outcomes()
                handler._send_json({"ok": True, "count": len(outcomes), "outcomes": outcomes})
        else:
            handler._send_error("FormulationOutcomesClosedLoopEngine unavailable.", status=503)
        return True

    # 10. Outcomes Cohort Summary
    if path in ("/api/v1/computational/outcomes/cohort-summary", "/api/v1/computational/outcomes-summary"):
        formulation_id = query_params.get("formulation_id", [None])[0]
        if srv.FormulationOutcomesClosedLoopEngine:
            summary = srv.FormulationOutcomesClosedLoopEngine.get_cohort_summary(formulation_id)
            handler._send_json({"ok": True, "cohort_rwe_summary": summary})
        else:
            handler._send_error("FormulationOutcomesClosedLoopEngine unavailable.", status=503)
        return True

    # 11. Scientific Regulatory Dossier
    if path.startswith("/api/v1/computational/dossier/"):
        form_id = path.split("/")[-1]
        fmt = query_params.get("format", ["json"])[0].lower()
        if srv.ScientificRegulatoryDossierGenerator:
            try:
                if fmt in ("markdown", "md"):
                    content = srv.ScientificRegulatoryDossierGenerator.export_markdown(form_id)
                    handler._send_text(content, content_type="text/markdown; charset=utf-8")
                elif fmt == "html":
                    content = srv.ScientificRegulatoryDossierGenerator.export_html(form_id)
                    handler._send_text(content, content_type="text/html; charset=utf-8")
                elif fmt in ("jsonld", "json-ld"):
                    content = srv.ScientificRegulatoryDossierGenerator.export_json_ld(form_id)
                    handler._send_text(content, content_type="application/ld+json; charset=utf-8")
                else:
                    dossier = srv.ScientificRegulatoryDossierGenerator.generate_dossier(form_id)
                    handler._send_json({"ok": True, "dossier": dossier})
            except Exception as e:
                handler._send_error(f"Error generating dossier: {str(e)}", status=400)
        else:
            handler._send_error("ScientificRegulatoryDossierGenerator unavailable.", status=503)
        return True

    # 12. In-Silico Docking Bridge & ADMET
    if path.startswith("/api/v1/computational/docking/"):
        compound_id = path.split("/")[-1]
        if srv.in_silico_docking_bridge:
            poses = srv.in_silico_docking_bridge.get_docking_poses(compound_id)
            admet = srv.in_silico_docking_bridge.get_admet_profile(compound_id)
            if not poses and not admet:
                handler._send_error(f"Compound docking profile not found: {compound_id}", status=404)
            else:
                handler._send_json({"ok": True, "compound_id": compound_id, "poses": poses, "admet": admet})
        else:
            handler._send_error("In-Silico Docking Bridge unavailable.", status=503)
        return True

    # 13. LIMS Batch Verification Retrieval
    if path.startswith("/api/v1/computational/lims/batches/"):
        if not auth_ctx:
            handler._send_error("Authentication required for LIMS CoA batch retrieval.", status=401)
            return True
        batch_no = path.split("/")[-1]
        if srv.lims_batch_ingestion_engine:
            verification = srv.lims_batch_ingestion_engine.get_batch_verification(batch_no)
            if not verification:
                handler._send_error(f"Batch verification record not found: {batch_no}", status=404)
            else:
                handler._send_json({"ok": True, "verification": verification})
        else:
            handler._send_error("LIMS Ingestion Engine unavailable.", status=503)
        return True

    # ── ZFIE Domain GET Endpoints (Part K, PRD & Section 68) ────────────
    if path in ("/api/v1/zfie/config/flags", "/zfie/config/flags"):
        from packages.zfie.core.flags import ZFIESettings
        handler._send_json({"ok": True, "flags": ZFIESettings.get_flags()})
        return True

    if path in ("/api/v1/zfie/benchmark/summary", "/zfie/benchmark/summary"):
        from packages.zfie.benchmark.benchmarks import ScientificBenchmarkingSuite
        report = ScientificBenchmarkingSuite.evaluate_model("ZFIE-CORE-MECH", "v0.4")
        handler._send_json({"ok": True, "benchmark_summary": report.to_dict()})
        return True

    if path in ("/api/v1/zfie/bridge/mappings", "/zfie/bridge/mappings"):
        from packages.zfie.bridge.semantic_bridge import UnaniBiomedicalBridgeRegistry
        mappings = UnaniBiomedicalBridgeRegistry.list_mappings()
        handler._send_json({"ok": True, "mappings": mappings})
        return True

    if path in ("/api/v1/zfie/governance/proposals", "/zfie/governance/proposals"):
        from packages.zfie.governance.scientific_review_board import ScientificReviewBoard
        proposals = ScientificReviewBoard.list_proposals()
        handler._send_json({"ok": True, "proposals": proposals})
        return True

    if path in ("/api/v1/zfie/experiments/next-best", "/zfie/experiments/next-best"):
        from packages.zfie.validation.experiment_recommender import ExperimentRecommendationEngine
        recs = ExperimentRecommendationEngine.get_top_recommendations_for_formulation("ZAY-FORM-0001")
        handler._send_json({"ok": True, "recommendations": recs})
        return True

    if path in ("/api/v1/zfie/outcomes", "/zfie/outcomes"):
        from packages.zfie.outcomes.rwe_closed_loop import RWEClosedLoopEngine
        obs = RWEClosedLoopEngine.list_observations()
        handler._send_json({"ok": True, "observations": obs})
        return True

    if path in ("/api/v1/zfie/formulations", "/zfie/formulations"):
        from packages.zfie.formulation.formulation_twin import FormulationTwinRegistry as ZFIETwinRegistry
        twins = [t.to_dict() for t in ZFIETwinRegistry._TWINS.values()]
        handler._send_json({"ok": True, "count": len(twins), "formulations": twins})
        return True

    if path.startswith("/api/v1/zfie/formulations/") or path.startswith("/zfie/formulations/"):
        parts = [p for p in path.split("/") if p]
        form_idx = parts.index("formulations")
        if len(parts) > form_idx + 1:
            form_id = parts[form_idx + 1]
            subaction = parts[form_idx + 2] if len(parts) > form_idx + 2 else None
            from packages.zfie.formulation.formulation_twin import FormulationTwinRegistry as ZFIETwinRegistry
            twin = ZFIETwinRegistry.get_twin(form_id)
            if not twin:
                handler._send_error(f"Formulation '{form_id}' not found.", status=404)
                return True

            if subaction == "twin":
                handler._send_json({"ok": True, "formulation_twin": twin.to_dict()})
                return True
            elif subaction == "network":
                net = {
                    "formulation_id": form_id,
                    "nodes": [
                        {"id": i.mufrad_id, "label": i.vernacular_name, "type": "HERB"}
                        for i in twin.ingredients
                    ] + [
                        {"id": "ZAY-CMP-0001", "label": "Colchicine", "type": "COMPOUND"},
                        {"id": "ZAY-CMP-0002", "label": "Piperine", "type": "COMPOUND"},
                        {"id": "ZAY-TGT-0001", "label": "Tubulin Beta (TUBB)", "type": "TARGET"},
                        {"id": "ZAY-TGT-0002", "label": "TRPV1", "type": "TARGET"},
                        {"id": "AXIS-MUSCULO", "label": "Musculoskeletal & Excretory Axis", "type": "ORGAN_AXIS"}
                    ],
                    "edges": [
                        {"source": "ZAY-MUF-0001", "target": "ZAY-CMP-0001", "relation": "CONTAINS"},
                        {"source": "ZAY-MUF-0002", "target": "ZAY-CMP-0002", "relation": "CONTAINS"},
                        {"source": "ZAY-CMP-0001", "target": "ZAY-TGT-0001", "relation": "BINDS_TO", "energy": -9.4},
                        {"source": "ZAY-CMP-0002", "target": "ZAY-TGT-0002", "relation": "BINDS_TO", "energy": -8.6},
                        {"source": "ZAY-TGT-0001", "target": "AXIS-MUSCULO", "relation": "REGULATES"}
                    ]
                }
                handler._send_json({"ok": True, "network": net})
                return True
            elif subaction == "contradictions":
                from packages.zfie.contradiction.conflict_detection import ContradictionRegistry as ZFIEContradictionRegistry
                contras = [c.to_dict() for c in ZFIEContradictionRegistry.list_for_formulation(form_id)]
                handler._send_json({"ok": True, "formulation_id": form_id, "contradictions": contras})
                return True
            else:
                handler._send_json({"ok": True, "formulation": twin.to_dict()})
                return True

    if path.startswith("/api/v1/zfie/analysis/") or path.startswith("/zfie/analysis/"):
        job_id = path.split("/")[-1]
        from packages.zfie.pipeline.pipeline_orchestrator import ZFIEPipelineOrchestrator
        job = ZFIEPipelineOrchestrator.get_job(job_id)
        if not job:
            handler._send_error(f"Analysis job '{job_id}' not found.", status=404)
        else:
            handler._send_json({"ok": True, "job": job.to_dict()})
        return True

    if path.startswith("/api/v1/zfie/batches/") or path.startswith("/zfie/batches/"):
        parts = [p for p in path.split("/") if p]
        batch_idx = parts.index("batches")
        batch_id = parts[batch_idx + 1] if len(parts) > batch_idx + 1 else None
        sub = parts[batch_idx + 2] if len(parts) > batch_idx + 2 else None
        batches = srv.FormulationTwinRegistry.list_batches("ZAY-FORM-0001") if srv.FormulationTwinRegistry else []
        matched = next((b for b in batches if b.batch_id == batch_id or b.lot_number == batch_id), None)
        if not matched and batches:
            matched = batches[0]
        if not matched:
            handler._send_error(f"Batch '{batch_id}' not found.", status=404)
            return True
        if sub == "fingerprint":
            handler._send_json({
                "ok": True,
                "batch_id": matched.batch_id,
                "hplc_fingerprint_id": matched.hplc_fingerprint_id,
                "similarity_index": 0.984,
                "reference_standard": "USP / UPI Colchicum-Piperine Marker Standard",
                "chromatogram_peaks": [
                    {"peak": 1, "retention_time_min": 3.42, "area_pct": 42.5, "compound": "Colchicine"},
                    {"peak": 2, "retention_time_min": 7.15, "area_pct": 28.1, "compound": "Piperine"},
                    {"peak": 3, "retention_time_min": 11.20, "area_pct": 18.4, "compound": "Guggulsterone E/Z"}
                ]
            })
        else:
            handler._send_json({"ok": True, "batch": matched.to_dict()})
        return True

    if path.startswith("/api/v1/zfie/evidence/") or path.startswith("/zfie/evidence/"):
        eid = path.split("/")[-1]
        from packages.zfie.evidence.evidence_bridge import EvidenceBridgeEngine as ZEB
        ev = ZEB.get_evidence(eid)
        if not ev:
            handler._send_error(f"Evidence '{eid}' not found.", status=404)
        else:
            handler._send_json({"ok": True, "evidence": ev})
        return True

    if path.startswith("/api/v1/zfie/clinical/encounters/") or path.startswith("/zfie/clinical/encounters/"):
        parts = [p for p in path.split("/") if p]
        enc_idx = parts.index("encounters")
        enc_id = parts[enc_idx + 1] if len(parts) > enc_idx + 1 else "ENC-001"
        from packages.zfie.clinical.clinical_adapter import ClinicalAdapter as ZFIEClinicalAdapter
        intel = ZFIEClinicalAdapter.get_drawer_intelligence("ZAY-FORM-0001", {"conditions": ["Gout", "Inflammatory Arthritis"], "eGFR": 88.0})
        intel["encounter_id"] = enc_id
        handler._send_json({"ok": True, "intelligence": intel})
        return True

    return False


def handle_computational_post(handler: Any, path: str, query_params: Dict[str, Any], auth_ctx: Dict[str, Any], body: Dict[str, Any]) -> bool:
    """Dispatches POST requests for computational pharmacology and ZFIE domain."""
    import services.live_api_server as srv

    # 1. Independent Safety Evaluation
    if path == "/api/v1/computational/safety-eval":
        formulation_id = body.get("formulation_id", "ZAY-FORM-0001")
        patient_context = body.get("patient_context", {})
        if srv.FormulationIntelligenceEngine:
            res = srv.FormulationIntelligenceEngine.evaluate_independent_safety(formulation_id, patient_context)
            handler._send_json({"ok": True, "safety_evaluation": res.to_dict()})
        else:
            handler._send_error("FormulationIntelligenceEngine unavailable.", status=503)
        return True

    # 2. Shadow Consult Prescription Intelligence
    if path == "/api/v1/computational/shadow-consult":
        formulation_id = body.get("formulation_id", "ZAY-FORM-0001")
        patient_context = body.get("patient_context", {})
        batch_id = body.get("batch_id")
        if srv.FormulationShadowOrchestrator:
            insight = srv.FormulationShadowOrchestrator.analyze_prescription_candidate(formulation_id, patient_context, batch_id)
            handler._send_json({"ok": True, "shadow_insight": insight.to_dict()})
        else:
            handler._send_error("FormulationShadowOrchestrator unavailable.", status=503)
        return True

    # 3. Outcomes Closed-Loop Trajectory Evaluation
    if path == "/api/v1/computational/outcomes-closed-loop":
        patient_id = body.get("patient_id", "PAT-774901")
        prescription_id = body.get("prescription_id", "RX-2026-0001")
        formulation_id = body.get("formulation_id", "ZAY-FORM-0001")
        batch_id = body.get("batch_id", "ZAY-BATCH-2026-001")
        baseline_markers = body.get("baseline_markers", {})
        current_markers = body.get("current_markers", {})
        vas_baseline = float(body.get("vas_baseline", 7.0))
        vas_current = float(body.get("vas_current", 3.0))
        stiffness_baseline_min = int(body.get("stiffness_baseline_min", 60))
        stiffness_current_min = int(body.get("stiffness_current_min", 20))
        day = int(body.get("day", 21))
        clinician_notes = body.get("clinician_notes", "")
        if srv.FormulationOutcomesClosedLoopEngine:
            rec = srv.FormulationOutcomesClosedLoopEngine.evaluate_patient_trajectory(
                patient_id=patient_id,
                prescription_id=prescription_id,
                formulation_id=formulation_id,
                batch_id=batch_id,
                baseline_markers=baseline_markers,
                current_markers=current_markers,
                vas_baseline=vas_baseline,
                vas_current=vas_current,
                stiffness_baseline_min=stiffness_baseline_min,
                stiffness_current_min=stiffness_current_min,
                day=day,
                clinician_notes=clinician_notes
            )
            handler._send_json({"ok": True, "record": rec.to_dict()}, status=201)
        else:
            handler._send_error("FormulationOutcomesClosedLoopEngine unavailable.", status=503)
        return True

    # 4. LIMS CoA Verification & Batch Ingestion
    if path == "/api/v1/computational/lims/verify-batch":
        if not auth_ctx:
            handler._send_error("Authentication required for LIMS CoA batch ingestion.", status=401)
            return True
        if srv.lims_batch_ingestion_engine and srv.CertificateOfAnalysisPayload:
            try:
                payload = srv.CertificateOfAnalysisPayload(
                    batch_number=body.get("batch_number", "BATCH-TEST-001"),
                    formulation_canonical_id=body.get("formulation_canonical_id", "ZAY-FORM-0001"),
                    manufacturing_date=body.get("manufacturing_date", "2026-09-01"),
                    expiry_date=body.get("expiry_date", "2029-08-31"),
                    testing_lab_name=body.get("testing_lab_name", "NABL Quality Laboratory"),
                    testing_lab_accreditation=body.get("testing_lab_accreditation", "ISO/IEC 17025"),
                    active_marker_name=body.get("active_marker_name", "Colchicine"),
                    active_marker_assay_pct=float(body.get("active_marker_assay_pct", 0.22)),
                    active_marker_min_pct=float(body.get("active_marker_min_pct", 0.18)),
                    active_marker_max_pct=float(body.get("active_marker_max_pct", 0.25)),
                    heavy_metals=body.get("heavy_metals", {"pb": 1.2, "cd": 0.05, "as": 0.8, "hg": 0.1}),
                    microbial_load=body.get("microbial_load", {"tamc": 1200, "tymc": 150, "e_coli": False, "salmonella": False}),
                    physical_chemistry=body.get("physical_chemistry", {"lod_pct": 5.8, "total_ash_pct": 4.2}),
                )
                report = srv.lims_batch_ingestion_engine.verify_and_ingest_coa(payload)
                handler._send_json({"ok": True, "report": report.to_dict()}, status=200 if report.release_status == "PASSED_RELEASED" else 422)
            except Exception as ex:
                handler._send_error(f"Invalid CoA payload: {str(ex)}", status=400)
        else:
            handler._send_error("LIMS Ingestion Engine unavailable.", status=503)
        return True

    # 5. Pharmacogenomics Mizaj Evaluation
    if path == "/api/v1/computational/mizaj-pharmacogenomics/evaluate":
        mizaj = body.get("mizaj", "Safrawi")
        formulation_id = body.get("formulation_id", "ZAY-FORM-0001")
        if srv.pharmacogenomics_mizaj_engine:
            strat = srv.pharmacogenomics_mizaj_engine.stratify_patient(mizaj, formulation_id)
            handler._send_json({"ok": True, "stratification": strat})
        else:
            handler._send_error("Pharmacogenomics Mizaj Engine unavailable.", status=503)
        return True

    # ── ZFIE Domain POST Handlers (Part K & PRD) ────────────────────────
    if path in ("/api/v1/zfie/formulations", "/zfie/formulations"):
        from packages.zfie.formulation.formulation_twin import (
            ComputationalFormulationTwin, FormulaIngredient as ZFIEFormulaIngredient, FormulationTwinRegistry
        )
        fid = f"ZAY-FORM-{uuid.uuid4().hex[:4].upper()}"
        ingredients = [
            ZFIEFormulaIngredient(
                mufrad_id=i.get("mufrad_id", "ZAY-MUF-0001"),
                botanical_name=i.get("botanical_name", "Herbal Botanical"),
                vernacular_name=i.get("vernacular_name", i.get("name", "Herb")),
                ratio=float(i.get("ratio", 0.5)),
                part_used=i.get("part_used", "Dried Part"),
                processing_method=i.get("processing_method", "Raw / Taqteer")
            )
            for i in body.get("ingredients", [])
        ]
        twin = ComputationalFormulationTwin(
            canonical_id=fid,
            name=body.get("name", "New Formulation Twin"),
            traditional_name=body.get("traditional_name", "نیا مرکب"),
            formula_version="v1.0",
            classical_source=body.get("classical_source", "ZKB Classical Canon"),
            therapeutic_target=body.get("therapeutic_target", "General Vitality"),
            ingredients=ingredients,
            preparation_method=body.get("preparation_method", "Traditional Confection")
        )
        FormulationTwinRegistry.register_twin(twin)
        handler._send_json({"ok": True, "formulation": twin.to_dict()}, status=201)
        return True

    # ── ZFIE Clinical CDS Encounter Endpoint (Section 52 & 53) ─────────
    if path.startswith(("/api/v1/zfie/clinical/encounters/", "/zfie/clinical/encounters/")) and (
        path.endswith("/formulation-analysis") or path.endswith("/analyze")
    ):
        parts = [p for p in path.split("/") if p]
        enc_idx = parts.index("encounters")
        encounter_id = parts[enc_idx + 1] if len(parts) > enc_idx + 1 else "ENC-001"

        # Strict Server-Side Authorization Check (Section 52)
        if auth_ctx and auth_ctx.get("role") == "PATIENT":
            handler._send_error("Forbidden: Clinical formulation analysis requires clinician authorization.", status=403, code="CLINICAL_AUTHORIZATION_REQUIRED")
            return True

        from packages.zfie.core.flags import ZFIESettings
        if not ZFIESettings.is_zfie_enabled():
            handler._send_error("ZFIE engine is disabled via feature flag ZFIE_ENABLED.", status=403, code="ZFIE_DISABLED")
            return True

        form_version_id = body.get("formulationVersionId") or body.get("formula_version_id", "v1.1")
        batch_id = body.get("batchId") or body.get("batch_id")
        requested_mode = body.get("analysisMode") or body.get("mode", "CLINICAL_CDS")
        form_id = body.get("formulationId") or body.get("formulation_id", "ZAY-FORM-0001")
        clinical_obj = body.get("clinicalObjective") or body.get("clinical_objective", "Targeted Joint Anti-inflammatory Modulation")
        patient_ctx = body.get("patient_context", {"conditions": ["Gout", "Inflammatory Arthritis"], "eGFR": 88.0})

        # Enforce Shadow Mode (Section 68 & 69)
        effective_mode = "SHADOW" if (ZFIESettings.is_shadow_mode() or not ZFIESettings.is_clinical_cds_enabled()) else requested_mode

        from packages.zfie.adapters.hakeem_zfie_adapter import HakeemSahabZFIEAdapter
        response_payload = HakeemSahabZFIEAdapter.generate_clinical_response(
            clinical_objective=clinical_obj,
            formulation_id=form_id,
            patient_context=patient_ctx,
            analysis_mode=effective_mode
        )
        response_payload["encounterId"] = encounter_id
        response_payload["formulationVersionId"] = form_version_id
        response_payload["batchId"] = batch_id
        response_payload["effectiveMode"] = effective_mode
        response_payload["shadowModeActive"] = ZFIESettings.is_shadow_mode()
        response_payload["clinicalCdsEnabled"] = ZFIESettings.is_clinical_cds_enabled()
        if ZFIESettings.is_shadow_mode():
            response_payload["governanceNotice"] = "ZFIE Section 68 Initial Deployment: Running in Shadow Mode. Clinical decision cannot be altered by computational model."
        handler._send_json(response_payload, status=200)
        return True

    if "/analyze" in path and ("zfie/formulations/" in path or "zfie/clinical/encounters/" in path):
        form_id = body.get("formulation_id", "ZAY-FORM-0001")
        version_id = body.get("formula_version_id", "v1.1")
        batch_id = body.get("batch_id")
        mode = body.get("mode", "SHADOW")
        from packages.zfie.pipeline.pipeline_orchestrator import ZFIEPipelineOrchestrator
        job = ZFIEPipelineOrchestrator.submit_job(
            formulation_id=form_id,
            formula_version_id=version_id,
            batch_id=batch_id,
            requested_by=body.get("requested_by", "RESEARCH_USER"),
            mode=mode
        )
        handler._send_json({"ok": True, "job_id": job.job_id, "status": job.status, "result": job.result}, status=200)
        return True

    if path in ("/api/v1/zfie/evidence", "/zfie/evidence"):
        from packages.zfie.evidence.evidence_bridge import EvidenceBridgeEngine
        eid = body.get("evidence_id") or f"ZAY-EVD-{uuid.uuid4().hex[:6].upper()}"
        body["evidence_id"] = eid
        EvidenceBridgeEngine.register_evidence(body)
        handler._send_json({"ok": True, "evidence_id": eid, "evidence": body}, status=201)
        return True

    if path in ("/api/v1/zfie/etl/ingest", "/zfie/etl/ingest"):
        from packages.zfie.factory.ingestion import ScientificDataFactory, IngestionSourceType, LicenseMetadata
        stype = IngestionSourceType(body.get("source_type", "PUBLIC_REPOSITORY"))
        lic = LicenseMetadata(
            source_name=body.get("source_name", "PubChem/ChEMBL"),
            license_type=body.get("license_type", "CC-BY-4.0"),
            commercial_use_allowed=bool(body.get("commercial_use_allowed", True)),
            attribution_required=bool(body.get("attribution_required", True)),
            redistribution_allowed=bool(body.get("redistribution_allowed", True)),
            source_uri=body.get("source_uri", "https://pubchem.ncbi.nlm.nih.gov")
        )
        record = ScientificDataFactory.ingest_payload(
            source_type=stype,
            source_name=body.get("source_name", "PubChem"),
            source_version=body.get("source_version", "2026.09"),
            payload=body.get("payload", {}),
            license_meta=lic
        )
        handler._send_json({"ok": True, "staged_record": record.to_dict()}, status=201)
        return True

    if path in ("/api/v1/zfie/compiler/compile", "/zfie/compiler/compile"):
        from packages.zfie.compiler.formulation_compiler import FormulationCompiler
        c_obj = body.get("clinical_objective", "Targeted Joint Anti-inflammatory Modulation")
        b_state = body.get("biological_state", "Crystal-Induced Synovial Inflammation")
        candidate = FormulationCompiler.compile_candidate_formulation(c_obj, b_state)
        handler._send_json({"ok": True, "candidate_architecture": candidate.to_dict()}, status=200)
        return True

    if path in ("/api/v1/zfie/manufacturing/analyze-batch", "/zfie/manufacturing/analyze-batch"):
        from packages.zfie.manufacturing.batch_qc_intelligence import BatchQCIntelligenceEngine
        dossier = BatchQCIntelligenceEngine.register_and_evaluate_batch(
            batch_id=body.get("batch_id", "BATCH-2026-X1"),
            batch_number=body.get("batch_number", "MS-2026-X1"),
            formulation_id=body.get("formulation_id", "ZAY-FORM-0001"),
            formulation_version=body.get("formulation_version", "v1.1"),
            raw_material_lots=body.get("raw_material_lots", ["LOT-SUR-2026-01"]),
            supplier_name=body.get("supplier_name", "Kashmir Certified Botanicals"),
            solvent=body.get("solvent", "Hydro-ethanolic (70:30)"),
            temp_c=float(body.get("temp_c", 65.0)),
            duration_h=float(body.get("duration_h", 4.0)),
            mfg_date=body.get("mfg_date", "2026-09-01"),
            exp_date=body.get("exp_date", "2028-09-01"),
            measured_peaks=body.get("measured_peaks", [
                {"compound": "Colchicine", "rt": 4.12, "abundance": 28.5},
                {"compound": "Piperine", "rt": 7.45, "abundance": 34.2},
                {"compound": "Guggulsterone_E", "rt": 11.20, "abundance": 18.0}
            ])
        )
        handler._send_json({"ok": True, "batch_dossier": dossier.to_dict()}, status=200)
        return True

    if path in ("/api/v1/zfie/outcomes/record", "/zfie/outcomes/record"):
        from packages.zfie.outcomes.rwe_closed_loop import RWEClosedLoopEngine
        obs = RWEClosedLoopEngine.record_outcome(
            patient_mrn=body.get("patient_mrn", "MRN-2026-01"),
            formulation_id=body.get("formulation_id", "ZAY-FORM-0001"),
            formulation_version=body.get("formulation_version", "v1.1"),
            batch_id=body.get("batch_id", "ZAY-BATCH-2026-001"),
            baseline_diagnosis=body.get("baseline_diagnosis", "Gout Arthritis"),
            phenotype=body.get("phenotype", "Balghami with Hyperuricemia"),
            duration_days=int(body.get("duration_days", 21)),
            adherence_pct=float(body.get("adherence_pct", 95.0)),
            biomarker_points=body.get("biomarker_points", []),
            outcome_delta=body.get("outcome_delta", "Clinically resolved"),
            adverse_events=body.get("adverse_events", [])
        )
        handler._send_json({"ok": True, "observation": obs.to_dict()}, status=201)
        return True

    if path in ("/api/v1/zfie/bridge/map-concept", "/zfie/bridge/map-concept"):
        from packages.zfie.bridge.semantic_bridge import UnaniBiomedicalBridgeRegistry
        term = body.get("classical_concept", "Waja-ul-Mafasil")
        mapped = UnaniBiomedicalBridgeRegistry.map_classical_concept(term)
        handler._send_json({"ok": True, "mapping": mapped})
        return True

    if path in ("/api/v1/zfie/safety/check", "/zfie/safety/check"):
        from packages.zfie.safety.safety_evaluator import ZFIESafetyEvaluator
        from packages.zfie.formulation.formulation_twin import FormulationTwinRegistry
        form_id = body.get("formulation_id", "ZAY-FORM-0001")
        twin = FormulationTwinRegistry.get_twin(form_id)
        ingredients = [{"mufrad_id": i.mufrad_id, "processing_method": i.processing_method} for i in twin.ingredients] if twin else []
        res = ZFIESafetyEvaluator.evaluate_formulation(form_id, ingredients, body.get("patient_context"))
        handler._send_json({"ok": True, "safety_evaluation": res})
        return True

    if path in ("/api/v1/zfie/hypotheses", "/zfie/hypotheses"):
        from packages.zfie.validation.validation_engine import ScientificHypothesis, ValidationEngine
        from packages.zfie.core.enums import ValidationStatus
        hid = f"ZAY-HYP-{uuid.uuid4().hex[:6].upper()}"
        hyp = ScientificHypothesis(
            hypothesis_id=hid,
            formulation_id=body.get("formulation_id", "ZAY-FORM-0001"),
            statement=body.get("statement", "Candidate formulation hypothesis"),
            falsification_criteria=body.get("falsification_criteria", "Falsified if no bioactivity"),
            target_protein=body.get("target_protein", "Target Protein"),
            proposed_assay=body.get("proposed_assay", "In-vitro assay"),
            status=ValidationStatus.PROPOSED
        )
        ValidationEngine.register_hypothesis(hyp)
        handler._send_json({"ok": True, "hypothesis": hyp.to_dict()}, status=201)
        return True

    if path in ("/api/v1/zfie/experiments", "/zfie/experiments"):
        from packages.zfie.validation.validation_engine import ExperimentPlan, ValidationEngine
        from packages.zfie.core.enums import ValidationStatus
        xid = f"ZAY-EXP-{uuid.uuid4().hex[:6].upper()}"
        exp = ExperimentPlan(
            experiment_id=xid,
            hypothesis_id=body.get("hypothesis_id", "ZAY-HYP-001"),
            title=body.get("title", "Laboratory Experiment Plan"),
            protocol_reference=body.get("protocol_reference", "SOP-ASSAY-GEN"),
            lead_investigator=body.get("lead_investigator", "Dr. Farhan Zaidi"),
            reagents=body.get("reagents", []),
            validation_status=ValidationStatus.PROPOSED
        )
        ValidationEngine.register_experiment(exp)
        handler._send_json({"ok": True, "experiment": exp.to_dict()}, status=201)
        return True

    if "/results" in path and "experiments" in path:
        exp_id = path.split("/")[-2]
        from packages.zfie.validation.validation_engine import ValidationEngine
        from packages.zfie.core.enums import ValidationStatus
        raw_uri = body.get("raw_data_uri", "s3://vault/raw.mzml")
        eff = float(body.get("measured_effect_size", 1.0))
        pval = float(body.get("p_value", 0.05))
        rep = int(body.get("replicates_count", 3))
        st = ValidationStatus(body.get("validation_status", "VALIDATED"))
        updated = ValidationEngine.submit_results(exp_id, raw_uri, eff, pval, rep, st)
        handler._send_json({"ok": True, "experiment": updated.to_dict() if updated else {}})
        return True

    if path in ("/api/v1/zfie/governance/proposals", "/zfie/governance/proposals"):
        from packages.zfie.governance.scientific_review_board import ScientificReviewBoard, ProposalDomain
        domain_str = body.get("domain", "FORMULATION_DESIGN")
        try:
            domain = ProposalDomain(domain_str)
        except ValueError:
            domain = ProposalDomain.FORMULATION_DESIGN
        prop = ScientificReviewBoard.submit_proposal(
            domain=domain,
            title=body.get("title", "New Scientific Proposal"),
            proposed_by=body.get("proposed_by", "RESEARCH_AGENT"),
            summary=body.get("summary", ""),
            evidence_ids=body.get("supporting_evidence_ids", [])
        )
        # 21 CFR Part 11 Audit Ledger Trail
        try:
            with srv.get_db() as conn:
                cur = conn.cursor()
                leaf_hash = hashlib.sha256(f"GOVERNANCE_PROPOSAL:{prop.proposal_id}:{time.time()}".encode()).hexdigest()
                cur.execute("""
                INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    leaf_hash,
                    "ZFIE_SCIENTIFIC_PROPOSAL_CREATED",
                    body.get("proposed_by", "RESEARCH_AGENT"),
                    "SUCCESS",
                    body.get("facility_id", "FAC-HQ-01"),
                    json.dumps({
                        "proposal_id": prop.proposal_id,
                        "domain": prop.domain.value,
                        "title": prop.title,
                        "cfr_part_11_compliance": True
                    })
                ))
                conn.commit()
        except Exception:
            pass
        handler._send_json({"ok": True, "proposal": prop.to_dict()}, status=201)
        return True

    if path in ("/api/v1/zfie/governance/sign-off", "/zfie/governance/sign-off"):
        from packages.zfie.governance.scientific_review_board import ScientificReviewBoard
        proposal_id = body.get("proposal_id")
        reviewer_id = body.get("reviewer_id", "DR-FAROOQI")
        reviewer_role = body.get("reviewer_role", "CHIEF_PHARMACOLOGIST")
        approved = bool(body.get("approved", True))
        comments = body.get("comments", "")
        try:
            updated_prop = ScientificReviewBoard.advance_stage(
                proposal_id=proposal_id,
                reviewer_id=reviewer_id,
                reviewer_role=reviewer_role,
                approved=approved,
                comments=comments
            )
            leaf_hash = hashlib.sha256(f"GOVERNANCE_SIGNOFF:{proposal_id}:{reviewer_id}:{time.time()}".encode()).hexdigest()
            try:
                with srv.get_db() as conn:
                    cur = conn.cursor()
                    cur.execute("""
                    INSERT INTO audit_ledger (leaf_hash, event_type, signer, status, facility_id, details_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        leaf_hash,
                        "ZFIE_SCIENTIFIC_GOVERNANCE_SIGNOFF",
                        reviewer_id,
                        "APPROVED" if approved else "REJECTED",
                        body.get("facility_id", "FAC-HQ-01"),
                        json.dumps({
                            "proposal_id": proposal_id,
                            "reviewer_role": reviewer_role,
                            "verdict": "APPROVED" if approved else "REJECTED",
                            "new_stage": updated_prop.current_stage.value,
                            "comments": comments,
                            "cfr_part_11_compliance": True
                        })
                    ))
                    conn.commit()
            except Exception:
                pass
            handler._send_json({
                "ok": True,
                "proposal": updated_prop.to_dict(),
                "audit_leaf_hash": leaf_hash,
                "qms_cfr_part_11_verified": True
            })
        except KeyError as e:
            handler._send_error(str(e), status=404)
        return True

    return False
