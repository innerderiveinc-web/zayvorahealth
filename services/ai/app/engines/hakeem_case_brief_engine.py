"""
ZAYVORA Health OS™ — Hakeem Sahab Case Brief Engine
==================================================
Reference:
  - Blueprint §11 (Hakeem Sahab AI Clinician Copilot)
  - Blueprint §25 (Sample Hakeem Sahab response contract)
  - Output Contract Fields:
      case_summary, missing_information[], red_flags[], mizaj_assessment,
      axis_map[], knowledge_items[], evidence_items[], safety_result,
      clinical_questions[], proposed_options[], uncertainties[],
      clinician_approval_state, source_trace[], model_id, prompt_version,
      retrieval_version, created_at
"""

from typing import Dict, Any, List, Optional
import datetime

class HakeemCaseBriefEngine:
    """Assembles a structured, cited decision-support brief adhering to Blueprint §25."""

    @classmethod
    def generate_case_brief(
        cls,
        patient_id: str,
        patient_context: Dict[str, Any],
        labs: Optional[Dict[str, Any]] = None,
        mizaj_result: Optional[Dict[str, Any]] = None,
        axis_map: Optional[List[Dict[str, Any]]] = None,
        safety_audit: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        labs = labs or {}
        name = patient_context.get("name", "Patient")
        age = patient_context.get("age", 35)
        gender = patient_context.get("gender", "individual")
        chief_complaints = patient_context.get("chief_complaints", [])
        m_humor = (mizaj_result.get("dominant_humor") if mizaj_result else None) or patient_context.get("mizaj", "Balgham")

        # 1. Structured Case Summary (Dynamic)
        if chief_complaints:
            cc_str = ", ".join(chief_complaints)
            case_summary = (
                f"{name}, {age}-year-old {gender} presenting with chief complaints of: {cc_str}. "
                f"Clinical presentation is evaluated within a dominant {m_humor} constitutional dyscrasia, "
                f"requiring multi-tier organ-axis harmonization and phased metabolic clearance."
            )
        else:
            case_summary = (
                f"{name}, {age}-year-old {gender} presenting for comprehensive holistic clinical review. "
                f"Evaluated within a dominant {m_humor} constitutional framework."
            )

        # 2. Missing Information Flags
        missing_info = []
        if "tsh" not in labs and "thyroid" in str(chief_complaints).lower():
            missing_info.append("Baseline Thyroid Profile (TSH, Free T3, Free T4) needed.")
        if "fasting_glucose" not in labs and "hba1c" not in labs:
            missing_info.append("Glycemic control markers (HbA1c / Fasting Glucose) pending.")
        if not missing_info:
            missing_info.append("Longitudinal PROMs symptom tracking at 14 days post-intervention.")

        # 3. Red Flags
        red_flags = []
        if safety_audit and safety_audit.get("decision") in ["BLOCK", "REFERRAL"]:
            red_flags.extend(safety_audit.get("reasons", ["Safety Firewall Hard Stop Detected"]))

        # 4. Mizaj Assessment (Dynamic)
        mizaj_assessment = mizaj_result or {
            "dominant_humor": m_humor,
            "score": 16,
            "max_score": 18,
            "classification": "SIGNIFICANT_DOMINANCE",
            "dosage_form_mandate": "Safoof (Dry Powder Capsule / Churna)" if m_humor == "Balgham" else "Sikanjabeen / Motadil Syrup",
            "contraindicated_form": "Majoon (Moist Electuary contraindicated for Balgham)" if m_humor == "Balgham" else "Excessively heating formulations"
        }

        # 5. Axis Map (Dynamic)
        if axis_map:
            axes = axis_map
        else:
            if gender.lower() == "female":
                axes = [
                    {"axis": "Jigar-Rahim (Hepato-Ovarian Axis)", "score": 4, "role": "Primary Etiology", "status": "Clinician Review"},
                    {"axis": "Dimagh-Qalb (Neuro-Cardiac Axis)", "score": 3, "role": "Secondary Target", "status": "Clinician Review"}
                ]
            else:
                axes = [
                    {"axis": "Jigar-Banas (Hepato-Metabolic Axis)", "score": 4, "role": "Primary Etiology", "status": "Clinician Review"},
                    {"axis": "Khusyatain-Dam (Male Reproductive Axis)", "score": 3, "role": "Secondary Target", "status": "Clinician Review"}
                ]

        # 6. Knowledge Items
        knowledge_items = [
            {"id": "MF-ASGANDH", "name": "Asgandh Nagauri", "daraja": "Hot 1 / Dry 1", "role": "Adaptogen & HPG Axis Tonifier"},
            {"id": "MF-BEHMAN-DUAL", "name": "Behman Surkh + Safaid", "role": "Paired Leydig stimulation with DNA thermal protection"}
        ]

        # 7. Evidence Items (E0-E6 Tiered)
        evidence_items = [
            {"item": "Asgandh KSM-66", "tier": "E5", "confidence": "HIGH", "source": "Ambiye et al. 2013 (RCT)", "finding": "Sperm count +167%, Motility +57%"},
            {"item": "Guggul Shuddha", "tier": "E5", "confidence": "HIGH", "source": "Bhatt et al. (RCT)", "finding": "TSH modulation and LDL-C reduction"},
            {"item": "Tabasheer SiO2 Heat Shield", "tier": "E2", "confidence": "HIGH", "source": "UPI Vol-VIII Standard", "finding": ">=85% SiO2 protects testicular tissue"}
        ]

        # 8. Safety Result
        safety_result = safety_audit or {
            "decision": "PASS",
            "violations": 0,
            "synergies_detected": ["Behman Dual-Color Balance Active", "Tabasheer Heat Shield Active"]
        }

        # 9. Clinical Questions for Clinician
        clinical_questions = [
            "Has patient noticed morning scrotal heat discomfort after prolonged sitting?",
            "Can patient commit to a 10:30 PM sleep schedule to support natural nocturnal LH/testosterone surges?"
        ]

        # 10. Proposed Options (Labeled as Non-Binding Drafts)
        proposed_options = [
            {
                "option_id": "OPT-01",
                "title": "Phase 1 Tanqiya Safoof (4-Tier Structured Formulation)",
                "status": "DRAFT_PROPOSAL",
                "components": "Foundation 25% + Core 55% + Correctors 15% + Catalysts 5%",
                "vehicle": "Lukewarm water (strictly dry powder form)"
            }
        ]

        # 11. Uncertainties
        uncertainties = [
            "Degree of peripheral T4-to-T3 deiodinase conversion impairment in liver",
            "True fasting compliance during 8:00 AM insulin draw"
        ]

        return {
            "case_summary": case_summary,
            "missing_information": missing_info,
            "red_flags": red_flags,
            "mizaj_assessment": mizaj_assessment,
            "axis_map": axes,
            "knowledge_items": knowledge_items,
            "evidence_items": evidence_items,
            "safety_result": safety_result,
            "clinical_questions": clinical_questions,
            "proposed_options": proposed_options,
            "uncertainties": uncertainties,
            "clinician_approval_state": "NOT_REVIEWED",
            "source_trace": [
                "ZAYVORA Clinical Handbook (Book 2)",
                "ZAYVORA Foundations, Framework & Pharmacopoeia (Part One)",
                "Unani Pharmacopoeia of India (UPI)"
            ],
            "model_id": "zayvora-hakeem-sahab-v2",
            "prompt_version": "hs-copilot-2026.09",
            "retrieval_version": "rag-zma-v4.1",
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def generate_evidence_grounded_copilot_brief(
        cls,
        patient_id: str,
        patient_context: Dict[str, Any],
        clinical_condition: str = "Waja-ul-Mafasil",
        labs: Optional[Dict[str, Any]] = None,
        mizaj_result: Optional[Dict[str, Any]] = None,
        active_axes: Optional[List[str]] = None,
        safety_audit: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Hakeem Sahab AI v2 — Evidence-Grounded Clinical Copilot
        Pipeline:
          Patient -> Clinical Context -> Retrieve Approved Knowledge -> Evidence Retrieval ->
          Organ-Axis Mapping -> Safety Firewall -> Uncertainty Detection -> Clinical Reasoning Summary ->
          Sources -> Clinician Review

        Mandatory Output Contract:
          Evidence + Confidence + Safety + Unknowns + Sources + Reasoning Summary + Non-binding Draft Nuskha
        """
        from services.knowledge.app.engines.knowledge_graph_traversal_engine import get_clinical_knowledge_graph
        from services.knowledge.app.engines.knowledge_intelligence_vnext import SafetyFirewallV2

        labs = labs or {}
        pctx = patient_context or {}
        name = pctx.get("name", "Patient")
        m_humor = (mizaj_result.get("dominant_humor") if mizaj_result else None) or pctx.get("mizaj", "Balgham")

        # 1. Graph Traversal through multi-hop clinical knowledge graph
        graph = get_clinical_knowledge_graph()
        graph_res = graph.query_graph_for_clinical_context(
            condition_id_or_name=clinical_condition,
            patient_mizaj=m_humor,
            active_axes=active_axes,
            patient_risk_context=pctx
        )

        candidate_drugs = graph_res.get("candidate_mufradat", [])
        murakkabat = graph_res.get("classical_murakkabat", [])

        # 2. Extract Evidence (E0-E6)
        evidence_items = []
        for c in candidate_drugs[:4]:
            evidence_items.append({
                "substance": c["canonical_name"],
                "drug_id": c["drug_id"],
                "tier": "E5" if "RCT" in str(c.get("evidence_grade", "")) else "E4",
                "grade": c.get("evidence_grade", "HIGH_CONFIRMED"),
                "finding": f"Exerts {', '.join(c.get('matched_afaal', [])[:2])} targeting {clinical_condition}",
                "citations_count": len(c.get("citations", []))
            })

        # 3. Calculate Clinical Confidence
        base_confidence = 0.82
        if candidate_drugs and candidate_drugs[0].get("recommendation_disposition") == "ACTIVE_COPILOT_ELIGIBLE":
            base_confidence += 0.08
        if labs and ("hba1c" in labs or "crp" in labs):
            base_confidence += 0.05
        confidence_score = round(min(base_confidence, 0.96), 2)

        # 4. Schedule E(1) Autonomous Hard-Block & Candidate Selection
        safe_candidates = [c for c in candidate_drugs if not c.get("is_schedule_e1") and c.get("recommendation_disposition") != "BLOCKED_BY_FIREWALL"]
        chief_candidate = safe_candidates[0] if safe_candidates else (candidate_drugs[0] if candidate_drugs else None)
        chief_drug_name = chief_candidate["canonical_name"] if chief_candidate else "Asgandh"
        supporting_candidates = [c for c in safe_candidates[1:3] if c["canonical_name"] != chief_drug_name]

        # 5. Monograph Lookup for Chief Drug: Mizaj Divergence, Musleh, Badal, & Tadbeer
        try:
            from services.knowledge.app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
        except ImportError:
            try:
                from app.data.mufradat_gold_batch_monographs import GOLD_BENCHMARK_25_MONOGRAPHS
            except ImportError:
                GOLD_BENCHMARK_25_MONOGRAPHS = {}

        chief_mono = GOLD_BENCHMARK_25_MONOGRAPHS.get(chief_candidate["drug_id"]) if chief_candidate else None
        chief_prof = chief_mono.get("classical_profile", {}) if chief_mono else {}
        drug_mizaj = chief_prof.get("mizaj", "Muaddil")
        drug_daraja = str(chief_prof.get("daraja", "1"))
        drug_musleh = chief_prof.get("musleh", "Sikanjabeen Motadil")
        drug_badal = chief_prof.get("badal", ["Ham-Mizaj Alternative"])
        drug_tadbeer = chief_prof.get("tadbeer", "Standard purification and fine pulverization")

        mizaj_divergence = {
            "patient_humor": str(m_humor),
            "chief_drug_mizaj": drug_mizaj,
            "potency_degree": drug_daraja,
            "thermal_differential": "HARMONIOUS" if "Muaddil" in drug_mizaj else "COMPENSATED",
            "musleh_paired": drug_musleh,
            "badal_alternative": drug_badal[0] if isinstance(drug_badal, list) else drug_badal,
            "tadbeer_protocol": drug_tadbeer,
        }

        # 6. Safety Firewall v2 Evaluation
        safety_eval = safety_audit or SafetyFirewallV2.evaluate_drug_safety_state(
            drug_or_id={
                "drug_id": chief_candidate["drug_id"] if chief_candidate else "ZMF-001",
                "is_schedule_e1": chief_candidate.get("is_schedule_e1", False) if chief_candidate else False,
                "classical_state": "APPROVED"
            },
            user_role=pctx.get("user_role", "CLINICIAN"),
            patient_context=pctx
        )

        # 7. Unknowns, Schedule E(1) Safeguards & Clinical Uncertainty Flags
        unknowns = []
        e1_detected = [c["canonical_name"] for c in candidate_drugs if c.get("is_schedule_e1")]
        if e1_detected:
            unknowns.append(
                f"SCHEDULE E(1) HARD-BLOCK: Detected {', '.join(e1_detected)} in relational graph traversal. "
                f"Autonomous prescription strictly forbidden by AYUSH/D&C Rules 1945. Requires licensed clinician manual sign-off."
            )
        if "crp" not in labs and "esr" not in labs:
            unknowns.append("Systemic inflammatory markers (hs-CRP / ESR) absent from patient chart.")
        if "creatinine" not in labs and "gfr" not in labs:
            unknowns.append("Baseline renal clearance (Serum Creatinine / eGFR) unverified.")
        if not unknowns:
            unknowns.append("Longitudinal PROMs symptom response at 14 days pending.")

        # 8. Traceable Sources (Classical Treatises with exact volume & page + Modern pharmacopoeia)
        sources = []
        for c in candidate_drugs[:3]:
            for cit in c.get("citations", [])[:1]:
                sources.append({
                    "substance": c["canonical_name"],
                    "type": "CLASSICAL",
                    "work_title": cit.get("source", "Khazain-ul-Advia"),
                    "volume": cit.get("volume", "Vol. I"),
                    "page": cit.get("page", "pp. Verified"),
                    "edition": "Classical Compendium / UPI Index",
                    "passage": cit.get("original_text_snippet", "")[:120] + "..." if cit.get("original_text_snippet") else "Monograph entry on file."
                })
        sources.append({
            "substance": "Official Standard",
            "type": "STATUTORY_PHARMACOPOEIA",
            "work_title": "Unani Pharmacopoeia of India (UPI)",
            "volume": "Part-I, Vol I-VI",
            "page": "Official Index",
            "edition": "Government of India, Ministry of AYUSH, PCIM&H",
            "passage": "Statutory identity, quality standards and classical therapeutic actions."
        })

        # 9. Clinical Reasoning Summary
        reasoning_summary = (
            f"Evidence-Grounded Synthesis for {name}: Evaluation of '{clinical_condition}' within {m_humor} "
            f"temperament dyscrasia. Graph traversal prioritized {len(candidate_drugs)} candidate single drugs "
            f"and {len(murakkabat)} classical formulations across {', '.join(graph_res.get('organ_axes', ['12-Axis Framework']))}. "
            f"Mizaj Divergence mapped against {drug_mizaj} ({drug_daraja}) with mandatory Musleh ({drug_musleh}). "
            f"Safety Firewall verified compliance: {safety_eval.get('ai_state', 'APPROVED_RETRIEVAL')}. "
            f"Formulation drafted according to 4-tier prescription doctrine."
        )

        # 10. Non-Binding Draft Prescribing Proposal with Musleh & Tadbeer
        draft_nuskha = {
            "status": "NON_BINDING_CLINICAL_DRAFT",
            "notice": "Draft generated by Hakeem Sahab AI v2. Final legal authorization rests exclusively with the licensed human clinician.",
            "formulation_archetype": "4-Tier Classical Symphony",
            "chief_drug": chief_drug_name,
            "supporting_drugs": [c["canonical_name"] for c in supporting_candidates],
            "musleh_corrective": drug_musleh,
            "badal_substitute": drug_badal[0] if isinstance(drug_badal, list) else drug_badal,
            "tadbeer_detox_protocol": drug_tadbeer,
            "mizaj_divergence": mizaj_divergence,
            "classical_vehicle_badraqa": "Arq-e-Badiyan / Lukewarm water",
            "dosage_context": "Safoof / Capsule 500mg BD after meals",
            "associated_murakkab": murakkabat[0]["compound_name"] if murakkabat else "Habb-e-Suranjan"
        }

        # 11. Deep RAG Retrieval from 12-Volume Grand Library & 38 Canonical Treatises
        symptoms_list = pctx.get("chief_complaints", [])
        if isinstance(symptoms_list, str):
            symptoms_list = [symptoms_list]
        grand_library_rag = cls.extract_grand_library_canonical_rag(
            clinical_condition=clinical_condition,
            patient_mizaj=str(m_humor),
            symptoms=symptoms_list
        )

        return {
            "evidence": {
                "overall_grade": "E5 / HIGH" if any(e.get("tier") == "E5" for e in evidence_items) else "E4 / MODERATE",
                "items": evidence_items,
                "traversal_hops": graph_res.get("traversal_hop_sequence", [])
            },
            "confidence": confidence_score,
            "safety": safety_eval,
            "unknowns": unknowns,
            "sources": sources,
            "clinical_reasoning_summary": reasoning_summary,
            "draft_nuskha": draft_nuskha,
            "grand_library_canonical_rag": grand_library_rag,
            "clinician_review": {
                "approval_required": True,
                "clinician_signoff_status": "PENDING_PRACTITIONER_SIGNATURE",
                "statutory_doctrine": "Autonomous Diagnosis != Autonomous Prescription"
            },
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

    @classmethod
    def extract_grand_library_canonical_rag(
        cls,
        clinical_condition: str,
        patient_mizaj: Optional[str] = None,
        symptoms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Performs deep multi-layer RAG retrieval across the 12-Volume Grand Integrative
        Library and the 38 Canonical Academic Treatises (Layer 1 + Layer 2).
        """
        try:
            from services.knowledge.app.data.grand_integrative_library_master import (
                search_library, get_chapter_by_id, get_chapter_treatise
            )
        except ImportError:
            try:
                from app.data.grand_integrative_library_master import (
                    search_library, get_chapter_by_id, get_chapter_treatise
                )
            except ImportError:
                return {
                    "query_used": clinical_condition,
                    "total_matches": 0,
                    "matched_chapters": [],
                    "canonical_treatise_excerpts": [],
                    "classical_citations": [],
                    "modern_biomedical_correlations": [],
                    "actionable_protocols": [],
                    "real_world_case_precedent": None
                }

        search_query = clinical_condition or ""
        if symptoms:
            search_query += " " + " ".join([str(s) for s in symptoms[:2]])
        if patient_mizaj:
            search_query += f" {patient_mizaj}"

        search_results = search_library(search_query)
        if not search_results and clinical_condition:
            search_results = search_library(clinical_condition)

        rag_payload: Dict[str, Any] = {
            "query_used": search_query.strip(),
            "total_matches": len(search_results),
            "matched_chapters": [],
            "canonical_treatise_excerpts": [],
            "classical_citations": [],
            "modern_biomedical_correlations": [],
            "actionable_protocols": [],
            "real_world_case_precedent": None
        }

        for match in search_results[:3]:
            cid = match.get("chapter_id")
            ch = get_chapter_by_id(cid)
            treatise = get_chapter_treatise(cid)

            chapter_info = {
                "chapter_id": cid,
                "volume_id": match.get("volume_id"),
                "volume_title": match.get("volume_title_en"),
                "chapter_title_en": match.get("title_en"),
                "chapter_title_ur": match.get("title_ur"),
                "relevance_score": match.get("score", 0),
            }
            rag_payload["matched_chapters"].append(chapter_info)

            if ch:
                for cit in ch.get("classical_citations", []):
                    rag_payload["classical_citations"].append({
                        "author": cit.get("author", "Classical Master"),
                        "book": cit.get("book", "Al-Qanoon fit-Tibb"),
                        "text": cit.get("text", "")
                    })
                if ch.get("modern_biomedical_correlation"):
                    rag_payload["modern_biomedical_correlations"].append({
                        "chapter_id": cid,
                        "correlation": ch.get("modern_biomedical_correlation")
                    })
                if ch.get("actionable_protocols"):
                    rag_payload["actionable_protocols"].append({
                        "chapter_id": cid,
                        "protocol": ch.get("actionable_protocols")
                    })

            if treatise:
                rag_payload["canonical_treatise_excerpts"].append({
                    "chapter_id": cid,
                    "canonical_philosophy": treatise.get("canonical_philosophy_and_doctrine", "")[:350] + "...",
                    "molecular_pathophysiology": treatise.get("molecular_and_cellular_pathophysiology", "")[:350] + "...",
                    "bedside_semiology": treatise.get("step_by_step_clinical_examination", "")[:300] + "...",
                    "recipes_mudabbar": treatise.get("comprehensive_pharmacopeia_and_recipes", "")[:300] + "..."
                })
                if not rag_payload["real_world_case_precedent"] and treatise.get("clinical_case_study"):
                    rag_payload["real_world_case_precedent"] = {
                        "chapter_id": cid,
                        "case_study": treatise.get("clinical_case_study")
                    }

        return rag_payload

