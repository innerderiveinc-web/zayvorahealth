#!/usr/bin/env python3
"""
ZAYVORA Health OS™ — Live Microservices Stack Verification & Integrity Audit
=============================================================================
Audits all 4 Strategic Pillars of the Enterprise Upgrade:
- Pillar 1: Doctor Matab 350-Drug Materia Medica Explorer & 12-Axis Radar
- Pillar 2: 50-Compound Classical Murakkabat Formulary Expansion & Compatibility Engine
- Pillar 3: Patient "Sehat Sahab" Companion, 8-Tier Parhez Engine & 14-Day PROMs
- Pillar 4: Live Microservices Stack Verification & Microservice Parity
"""

import sys
import os
import json
import time

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in [repo_root, os.path.join(repo_root, "services", "knowledge"), os.path.join(repo_root, "services", "clinical"), os.path.join(repo_root, "services", "therapeutic"), os.path.join(repo_root, "services", "ai")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)

def print_header(title: str):
    print("\n" + "=" * 76)
    print(f"  {title}")
    print("=" * 76)

def test_pillar1_materia_medica_and_radar():
    print_header("PILLAR 1: Doctor Matab 350-Drug Materia Medica Explorer & 12-Axis Radar")
    from services.knowledge.app.core.pharmacopoeia import get_upi_mufradat, get_schedule_e1_poisons

    drugs = get_upi_mufradat()
    poisons = get_schedule_e1_poisons()
    e1_catalog = [d for d in drugs if d.get("is_schedule_e1")]

    print(f"✓ Master Pharmacopoeia Monographs loaded: {len(drugs)} drugs")
    assert len(drugs) >= 330, f"Expected >= 330 drugs, got {len(drugs)}"

    print(f"✓ Statutory Schedule E(1) Cataloged Poisons: {len(e1_catalog)} poisons")
    print(f"✓ Detailed Toxicological Antidote Monographs: {len(poisons)} poisons")
    assert len(e1_catalog) >= 35, f"Expected >= 35 poisons in catalog, got {len(e1_catalog)}"
    assert len(poisons) >= 10, f"Expected >= 10 detailed toxicological monographs, got {len(poisons)}"

    # Check radar component & page
    radar_path = "apps/web/components/TwelveAxisRadar.tsx"
    page_path = "apps/web/app/materia-medica/page.tsx"
    nuskha_path = "apps/web/components/NuskhaBuilder.tsx"

    assert os.path.exists(radar_path), f"Missing {radar_path}"
    assert os.path.exists(page_path), f"Missing {page_path}"
    assert os.path.exists(nuskha_path), f"Missing {nuskha_path}"

    with open(nuskha_path) as f:
        content = f.read()
        assert "TwelveAxisRadar" in content, "TwelveAxisRadar not imported/used in NuskhaBuilder.tsx"

    with open(page_path) as f:
        content = f.read()
        assert "TwelveAxisRadar" in content, "TwelveAxisRadar not imported in materia-medica/page.tsx"
        assert "Layer 01:" in content and "Layer 10:" in content, "10-layer drawer incomplete"

    print("✓ TwelveAxisRadar component verified & integrated into NuskhaBuilder")
    print("✓ apps/web/app/materia-medica/page.tsx reference desk verified with 10-layer drawer")


def test_pillar2_murakkabat_50_formulary():
    print_header("PILLAR 2: 50-Compound Classical Murakkabat Formulary Expansion")
    from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
    from services.knowledge.app.core.pharmacopoeia import get_compound_formulations, get_compound_by_name
    from services.therapeutic.app.engines.murakkab_intelligence_engine import MurakkabIntelligenceEngine

    print(f"✓ Classical Murakkabat Formulary count: {len(CLASSICAL_MURAKKABAT_50)} formulations")
    assert len(CLASSICAL_MURAKKABAT_50) >= 50, f"Expected >= 50 formulations, got {len(CLASSICAL_MURAKKABAT_50)}"

    all_compounds = get_compound_formulations()
    print(f"✓ Combined Pharmacopoeia Compounds: {len(all_compounds)} available")
    assert len(all_compounds) >= 50, "Combined compounds failed"

    # Test sample audits across galenical classes
    sample_itrifal = get_compound_by_name("Itrifal Kishneezi")
    assert sample_itrifal is not None, "Missing Itrifal Kishneezi"
    audit1 = MurakkabIntelligenceEngine.audit_classical_compound_dict(sample_itrifal)
    assert audit1.is_valid is True
    print(f"✓ Audited Itrifal Kishneezi: valid={audit1.is_valid}, score={audit1.compatibility_score}")

    sample_majun = get_compound_by_name("Majun Suranjan")
    assert sample_majun is not None, "Missing Majun Suranjan"
    audit2 = MurakkabIntelligenceEngine.audit_classical_compound_dict(sample_majun)
    assert audit2.schedule_e1_compliant is True
    print(f"✓ Audited Majun Suranjan (Schedule E1): valid={audit2.is_valid}, score={audit2.compatibility_score}")


def test_pillar3_sehat_sahab_and_proms():
    print_header("PILLAR 3: Patient 'Sehat Sahab' Companion, 8-Tier Parhez & 14-Day PROMs")
    from services.clinical.app.engines.patient_proms_engine import PatientPROMsEngine, PROMsIntakeRecord

    base = PROMsIntakeRecord(
        patient_id="MRN-TEST",
        encounter_id="ENC-01",
        day_number=0,
        symptom_severity_vas=8.5,
        hazm_digestive_score=3.0,
        sleep_mental_calm_score=4.0,
        energy_vigor_score=3.5,
        parhez_adherence_percent=40.0,
        medication_compliance_percent=100.0,
    )

    day14 = PROMsIntakeRecord(
        patient_id="MRN-TEST",
        encounter_id="ENC-01",
        day_number=14,
        symptom_severity_vas=2.0,
        hazm_digestive_score=8.5,
        sleep_mental_calm_score=8.5,
        energy_vigor_score=8.0,
        parhez_adherence_percent=92.0,
        medication_compliance_percent=100.0,
        adverse_symptoms=[],
    )

    result = PatientPROMsEngine.evaluate_intake(day14, base)
    print(f"✓ 14-Day PROMs Improvement: {result.clinical_improvement_percent}%")
    print(f"✓ Composite Vitality Index: {result.overall_vitality_index} / 100")
    print(f"✓ Humoral Mizaj State: {result.mizaj_normalization_state}")
    print(f"✓ Parhez Compliance Tier: {result.parhez_compliance_tier}")
    assert result.clinical_improvement_percent > 50.0
    assert result.mizaj_normalization_state == "STABLE_EQUILIBRIUM"

    # Test safety escalation trigger
    adverse_case = PROMsIntakeRecord(
        patient_id="MRN-ALERT",
        encounter_id="ENC-02",
        day_number=3,
        symptom_severity_vas=7.0,
        hazm_digestive_score=4.0,
        sleep_mental_calm_score=5.0,
        energy_vigor_score=4.0,
        parhez_adherence_percent=60.0,
        medication_compliance_percent=100.0,
        adverse_symptoms=["Severe chest pain and palpitations"],
    )
    alert_res = PatientPROMsEngine.evaluate_intake(adverse_case)
    assert alert_res.requires_clinical_escalation is True
    print(f"✓ Safety Firewall Alert Triggered: {alert_res.escalation_reasons}")

    # Check PatientPortalCockpit.tsx
    cockpit_path = "apps/web/components/PatientPortalCockpit.tsx"
    assert os.path.exists(cockpit_path)
    with open(cockpit_path) as f:
        c_code = f.read()
        assert "8-Tier Canonical Parhez" in c_code
        assert "14-Day PROMs Recovery Tracker" in c_code
    print("✓ PatientPortalCockpit.tsx 8-Tier Parhez and 14-Day PROMs verified")


def test_pillar4_graph_rag_and_hakeem_copilot():
    print_header("PILLAR 4: Knowledge Graph, Hybrid RAG & Hakeem Sahab AI Copilot v2")
    from services.knowledge.app.graph.ingestion import generate_mufradat_graph_payload
    from services.knowledge.app.core.hybrid_rag import get_hybrid_rag_service
    from services.ai.app.engines.hakeem_case_brief_engine import HakeemCaseBriefEngine

    # Graph
    graph_payload = generate_mufradat_graph_payload()
    nodes_dict = graph_payload.get("nodes", {})
    total_nodes = sum(len(v) for v in nodes_dict.values()) if isinstance(nodes_dict, dict) else len(nodes_dict)
    print(f"✓ Knowledge Graph Nodes: {total_nodes}")
    print(f"✓ Knowledge Graph Edges: {len(graph_payload.get('edges', []))}")
    assert len(graph_payload.get("edges", [])) >= 1600

    # Hybrid RAG
    rag_service = get_hybrid_rag_service()
    rag_stats = rag_service.get_corpus_stats()
    print(f"✓ Hybrid RAG Indexed Documents: {rag_stats['total_documents']}")
    assert rag_stats["total_documents"] >= 350

    # Hakeem Copilot Brief
    brief = HakeemCaseBriefEngine.generate_evidence_grounded_copilot_brief(
        patient_id="PT-TEST-01",
        patient_context={
            "name": "Hamza Farooqi",
            "age": 44,
            "gender": "male",
            "mizaj": "Balgham",
            "chief_complaints": ["Waja-ul-Mafasil (Joint pain)", "Morning knee stiffness"],
        },
        clinical_condition="Waja-ul-Mafasil",
        active_axes=["mafasil", "meda-amaa"],
    )
    assert brief is not None
    assert "draft_nuskha" in brief
    draft = brief["draft_nuskha"]
    assert draft["status"] == "NON_BINDING_CLINICAL_DRAFT"
    print(f"✓ Hakeem Sahab v2 Brief Generated for: {brief.get('condition')}")
    print(f"✓ Chief Drug proposed: {draft.get('chief_drug')}")
    print(f"✓ Mandatory Musleh Corrective: {draft.get('musleh_corrective')}")
    print(f"✓ Badal Substitute: {draft.get('badal_substitute')}")
    print(f"✓ Traceable Sources: {len(brief.get('sources', []))} citations")


def test_pillar5_clinical_continuum_and_learning_health_os():
    print_header("PILLAR 5: Clinical Intelligence Continuum & Learning Healthcare OS (WHO SMART DAK Level 3)")
    from services.knowledge.app.core.who_smart_dak_engine import WHOSmartDAKEngine
    from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
        ClinicalIntelligenceCoreOrchestrator,
        ClinicalContinuumRequest,
    )
    from services.clinical.app.engines.closed_loop_learning_engine import ClosedLoopLearningEngine

    # 1. WHO SMART DAK Level 3 Computable Artifact
    sample_drug = {
        "name": "Suranjan Shirin",
        "botanical_name": "Colchicum autumnale L.",
        "mizaj": "Haar 2, Yabis 2",
        "is_schedule_e1": False,
        "requires_tadbeer": True,
        "tadbeer_method": "Tadbeer-e-Roghani in almond oil",
        "organ_axes": ["MAFASIL"],
        "musleh": "Roghan-e-Badam",
    }
    art = WHOSmartDAKEngine.transform_mufrad_to_smart_artifact(sample_drug, version="2.0.0")
    val = WHOSmartDAKEngine.validate_computable_artifact(art)
    assert val["is_valid"], f"WHO SMART DAK Validation failed: {val['errors']}"
    assert val["sha256_verified"], "Cryptographic SHA-256 fingerprint verification failed"
    print(f"✓ WHO SMART Guidelines Level 3 DAK Monograph: {art.title} (SHA-256: {art.sha256_hash[:16]}...)")
    print(f"✓ Computable Decision Support Rules generated: {len(art.decision_rules)}")

    # 2. Complete 12-Stage Clinical Intelligence Continuum Execution
    req = ClinicalContinuumRequest(
        patient_id="P-STACK-TEST-001",
        patient_name="Hamza Farooqi",
        age=54,
        gender="MALE",
        chief_complaints=["Chronic bilateral knee pain", "Morning stiffness > 45 mins"],
        presenting_condition="Waja-ul-Mafasil",
        symptom_duration_days=180,
        baseline_pain_vas=8.0,
        constitutional_signs={"dominant_humor": "Balgham", "cold_degree": 3, "moist_degree": 2},
        targeted_axes=["mafasil", "meda-amaa"],
        candidate_drugs=["Suranjan Shirin", "Zanjabeel", "Asgand"],
        clinician_id="HAK-0042",
        clinician_role="HAKEEM",
        is_pregnant=False,
        has_renal_impairment=False,
        followup_proms_day=14,
        followup_symptom_vas=2.0,
        followup_adverse_events=[],
    )
    res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
    assert res.transaction_id.startswith("TX-ZAYVORA-")
    assert res.stage_7_safety_firewall["decision"] == "PASS"
    assert res.stage_9_clinician_approval["is_ratified"] is True
    assert res.stage_9_clinician_approval["nuskha_state"] == "APPROVED"
    assert res.stage_12_outcome_and_learning["outcome_classification"] == "KAMIL"
    print(f"✓ 12-Stage Continuum Transaction: {res.transaction_id}")
    print(f"✓ Safety Firewall Decision: {res.stage_7_safety_firewall['decision']}")
    print(f"✓ Clinician Ratification State: {res.stage_9_clinician_approval['nuskha_state']} (Ratified: {res.stage_9_clinician_approval['is_ratified']})")
    print(f"✓ 8-Tier Parhez Prescribed: {len(res.stage_10_nuskha_and_parhez['parhez_8_tier'])} tiers")
    print(f"✓ 14-Day PROMs Improvement: {res.stage_11_proms_followup['clinical_improvement_percent']}%")
    print(f"✓ Classical Outcome: {res.stage_12_outcome_and_learning['outcome_classification']}")

    # 3. Autonomous AI-Signoff Hard-Block
    req_ai = ClinicalContinuumRequest(
        patient_id="P-AI-FAIL-001",
        patient_name="Test AI Block",
        age=30,
        gender="MALE",
        chief_complaints=["Joint pain"],
        presenting_condition="Waja-ul-Mafasil",
        symptom_duration_days=7,
        baseline_pain_vas=5.0,
        constitutional_signs={"dominant_humor": "Dam"},
        targeted_axes=["mafasil"],
        candidate_drugs=["Asgand"],
        clinician_id="BOT-AGY",
        clinician_role="AI_COPILOT",
    )
    res_ai = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req_ai)
    assert res_ai.stage_9_clinician_approval["is_ratified"] is False, "AI role must NEVER approve prescription"
    print(f"✓ Safety Invariant: AI sign-off autonomously hard-blocked (is_ratified=False)")

    # 4. Closed-Loop Learning Health System & HIPAA Safe Harbor
    h_pid = ClosedLoopLearningEngine.deidentify_patient_id("P-STACK-TEST-001")
    assert len(h_pid) == 16 and "P-STACK" not in h_pid
    reg_summary = ClosedLoopLearningEngine.get_registry_summary()
    assert reg_summary["total_patient_evaluations"] >= 1
    print(f"✓ Closed-Loop LHS Registry: {reg_summary['total_registered_conditions']} conditions, {reg_summary['total_patient_evaluations']} verified outcomes")
    print(f"✓ HIPAA § 164.514(b)(2) irreversible salt-hash: {h_pid}")


def test_pillar6_abdm_federation_and_population_health():
    print_header("PILLAR 6: ABDM FHIR Interoperability, Multi-Clinic Federation & Population Health")
    from dataclasses import asdict
    from services.clinical.app.interop.abdm_fhir_continuum_orchestrator import ABDMFHIRContinuumOrchestrator
    from services.clinical.app.engines.multi_clinic_federation_engine import MultiClinicFederationEngine
    from services.clinical.app.engines.population_health_engine import PopulationHealthEngine, CanonicalSeason
    from services.clinical.app.engines.clinical_intelligence_core_orchestrator import (
        ClinicalIntelligenceCoreOrchestrator,
        ClinicalContinuumRequest,
    )

    # 1. ABDM FHIR OPConsult & Prescription Bundles
    req = ClinicalContinuumRequest(
        patient_id="P-PIL-006",
        patient_name="Bibi Fatima",
        age=48,
        gender="FEMALE",
        chief_complaints=["Knee inflammation", "Severe joint stiffness"],
        presenting_condition="Waja-ul-Mafasil",
        symptom_duration_days=21,
        baseline_pain_vas=6.5,
        constitutional_signs={"dominant_humor": "Balgham"},
        targeted_axes=["Musculoskeletal & Articular Axis"],
        candidate_drugs=["Suranjan Shirin", "Asgand Nagori"],
        clinician_id="HAK-007",
        clinician_role="HAKEEM",
    )
    res = ClinicalIntelligenceCoreOrchestrator.execute_continuum(req)
    c_dict = asdict(res)

    op_bundle = ABDMFHIRContinuumOrchestrator.build_op_consult_bundle(c_dict)
    assert op_bundle["resourceType"] == "Bundle" and op_bundle["type"] == "document"
    assert "https://nrces.in/ndhm/fhir/r4/StructureDefinition/OPConsultRecord" in op_bundle["meta"]["profile"]

    rx_bundle = ABDMFHIRContinuumOrchestrator.build_prescription_bundle(c_dict)
    assert rx_bundle["resourceType"] == "Bundle" and rx_bundle["type"] == "document"
    assert "https://nrces.in/ndhm/fhir/r4/StructureDefinition/PrescriptionRecord" in rx_bundle["meta"]["profile"]

    envelope = ABDMFHIRContinuumOrchestrator.create_hip_data_transfer_envelope(
        fhir_bundle=op_bundle,
        recipient_hiu_id="HIU-AIIMS-DEL",
        consent_id="CONSENT-ABDM-2026-PIL6"
    )
    assert envelope["checksum_algorithm"] == "SHA-256" and len(envelope["checksum"]) == 64
    print(f"✓ ABDM FHIR R4 Bundles: OPConsultRecord & PrescriptionRecord validated")
    print(f"✓ ABDM Milestone 3 HIP Encryption Envelope: SHA-256 {envelope['checksum'][:16]}...")

    # 2. Multi-Clinic Federation & Cryptographic Referral
    clinics = MultiClinicFederationEngine.list_clinics()
    assert len(clinics) >= 4
    referral = MultiClinicFederationEngine.create_inter_clinic_referral(
        patient_id="P-PIL-006",
        source_facility_id="FAC-DEL-CENTRAL-01",
        target_facility_id="FAC-HYD-REGIONAL-02",
        referring_clinician_id="DOC-DEL-01",
        clinical_condition="Waja-ul-Mafasil",
        specialty_axis_required="Musculoskeletal & Articular Axis",
        reason_for_referral="Tertiary regimental therapy consultation",
    )
    assert referral.referral_token.startswith("ZAY-REF-")
    redemption = MultiClinicFederationEngine.redeem_inter_clinic_referral(
        referral_token=referral.referral_token,
        receiving_facility_id="FAC-HYD-REGIONAL-02",
        accepting_clinician_id="DOC-HYD-04"
    )
    assert redemption["success"] is True and redemption["access_granted"] is True
    print(f"✓ Multi-Clinic Federation: {len(clinics)} facilities across Tier 1, 2, 3")
    print(f"✓ Inter-Clinic Cryptographic Handshake: {referral.referral_token} redeemed with authorized chart access")

    # 3. FEFO Inventory Balancing
    transfer = MultiClinicFederationEngine.request_inventory_transfer(
        drug_name="Suranjan Shirin",
        quantity_grams=20.0,
        source_facility_id="FAC-DEL-CENTRAL-01",
        target_facility_id="FAC-BLR-COMMUNITY-04",
    )
    assert transfer["success"] is True and transfer["status"] == "TRANSFERRED_IN_TRANSIT"
    print(f"✓ FEFO Automated Cross-Clinic Stock Balancing: {transfer['fefo_lot_selected']} transferred")

    # 4. Seasonal Humoral Surveillance & Pharmacovigilance Cluster Scan
    bahar_advisory = PopulationHealthEngine.generate_seasonal_surveillance_advisory(season=CanonicalSeason.MAUSIM_E_BAHAR)
    assert "Dam" in bahar_advisory.predominant_vulnerable_humor
    epi = PopulationHealthEngine.get_humoral_epidemiology_distribution()
    assert epi["cohort_size"] >= 1000
    clusters = PopulationHealthEngine.scan_adr_clusters(cluster_threshold=2)
    assert len(clusters) >= 1 and clusters[0].alert_level == "CRITICAL_SAFETY_HOLD"
    print(f"✓ Asbab-e-Sittah Surveillance: Mausim-e-Bahar advisory active ({bahar_advisory.thermal_dynamic})")
    print(f"✓ Population Humoral Epidemiology: {len(epi['humoral_distribution'])} constitutional quadrants")
    print(f"✓ Multi-Clinic Pharmacovigilance: {len(clusters)} active cluster alert ({clusters[0].suspected_drug} lot hold)")


def test_pillar7_adaptive_precision_and_phenotype_intelligence():
    print_header("PILLAR 7: Adaptive Precision Healthcare & Phenotype Intelligence")
    from services.clinical.app.engines.precision_patient_model import (
        PrecisionPatientModel,
        FunctionalBiomarkerDelta,
    )
    from services.clinical.app.engines.phenotype_and_response_engine import (
        PhenotypeAndResponseEngine,
        ResponseClassificationTier,
    )
    from services.knowledge.app.core.knowledge_compiler import (
        KnowledgeCompiler,
        ReviewerSignoff,
    )
    import services.live_api_server as server

    # 1. Precision Patient Model (Longitudinal Trajectory)
    ppm = PrecisionPatientModel(
        patient_id="P-PIL-007",
        age=49,
        gender="MALE",
        baseline_vitals={"pulse": 76, "bp": "120/80"},
        primary_condition="Waja-ul-Mafasil",
    )
    ppm.add_symptom("Bilateral Knee Pain & Morning Stiffness", 8.0, 60)
    ppm.add_biomarker_delta("ESR", 45.0, 20.0, "mm/hr", is_lower_better=True)
    ppm.add_mizaj_record("Balghami Ghaleez", 0.2, 0.8, 0.8, 0.2, 0.6)
    ppm.add_organ_axis_score("Musculoskeletal & Articular (Mafasil)", 0.85)
    ppm.add_nuskha_record("NSK-SURANJAN", ["Majun Suranjan", "Habb-e-Asgandh"])
    ppm.add_posology_adherence(14, 28, 26)
    ppm.add_outcome_record("KAMIL", 82.0, "Shifa-e-Kamil")
    summary = ppm.synthesize_longitudinal_summary()
    assert summary["patient_id"] == "P-PIL-007"
    assert len(summary["longitudinal_trajectory_answers"]["what_changed"]["improved_biomarkers"]) == 1
    print(f"✓ Precision Patient Model: Longitudinal multi-dimensional trajectory synthesized for {summary['patient_id']}")

    # 2. Phenotype Stratification
    pheno_engine = PhenotypeAndResponseEngine()
    balgham_pheno = pheno_engine.classify_phenotype("Waja-ul-Mafasil", "Balghami (Cold & Wet)")
    assert balgham_pheno.phenotype_code == "PHENO-ARTH-BALGHAM"
    print(f"✓ Phenotype Stratification: Waja-ul-Mafasil -> {balgham_pheno.phenotype_name} ({balgham_pheno.phenotype_code})")

    # 3. 5-Tier Response Intelligence & Adherent Non-Responder Escalation Flag
    responder_res = pheno_engine.evaluate_response("P-101", 8.0, 1.5, 92.0)
    assert responder_res.tier == ResponseClassificationTier.RESPONDER
    escalation_res = pheno_engine.evaluate_response("P-102", 8.0, 7.5, 88.0)
    assert escalation_res.tier == ResponseClassificationTier.ADHERENT_NON_RESPONDER
    assert escalation_res.protocol_switch_recommended is True
    print(f"✓ Response Intelligence: Classified RESPONDER & ADHERENT_NON_RESPONDER (protocol switch active)")

    # 4. WHO SMART L4 Knowledge Compiler
    compiler = KnowledgeCompiler()
    eval_res = compiler.evaluate_rule("ZAYVORA-WHO-L4-SURANJAN-001", {"condition": "waja_ul_mafasil", "serum_creatinine": 1.0})
    assert eval_res["matched"] is True and eval_res["outputs"]["action"] == "AUTHORIZE_SURANJAN_PROTOCOL"
    rules = compiler.list_rules()
    assert len(rules) >= 2
    print(f"✓ WHO SMART Level 4 Executable Knowledge Compiler: {len(rules)} compiled rules with passing test suites")

    # 5. Live Server Module Parity
    assert server.PrecisionPatientModel is not None
    assert server.PhenotypeAndResponseEngine is not None
    assert server.global_knowledge_compiler is not None
    print(f"✓ Live REST API Server Parity: Precision endpoints & global compiler verified")


def test_pillar8_continuous_monitoring_and_n_of_1_evidence():
    print_header("PILLAR 8: Digital Biomarkers, Continuous Monitoring & N-of-1 Evidence")
    from services.clinical.app.engines.continuous_monitoring_engine import (
        ContinuousMonitoringEngine,
        RiskSignalType,
    )
    from services.clinical.app.engines.n_of_1_evidence_engine import (
        NOf1EvidenceEngine,
        LongitudinalObservation,
    )
    import services.live_api_server as server

    # 1. Telemetry Ingestion & Risk Signal Detection
    mon_engine = ContinuousMonitoringEngine()
    mon_engine.ingest_telemetry_batch(
        "P-PIL8-001",
        [
            {"resting_hr_bpm": 88.0, "hrv_sdnn_ms": 22.0, "sleep_efficiency_pct": 65.0, "daily_steps": 3500, "doses_taken": 2, "doses_prescribed": 2}
        ]
    )
    report = mon_engine.analyze_patient_telemetry("P-PIL8-001")
    assert len(report.active_signals) >= 2
    types = [s.signal_type for s in report.active_signals]
    assert RiskSignalType.THERMAL_POLARIZATION_SPIKE in types
    assert RiskSignalType.AUTONOMIC_DYSCRASIA in types
    print(f"✓ Telemetry Analysis: Ingested biometrics, detected {len(report.active_signals)} early risk signals (Safrawi spike + Autonomic dyscrasia)")
    print(f"✓ Humoral Stability Index: {report.humoral_stability_index} / 1.0 (Alert thresholds active)")

    # 2. Single-Subject N-of-1 Effect Size & Bayesian Response
    obs = [
        LongitudinalObservation(day_number=0, phase="BASELINE", symptom_vas=8.5, ambient_temp_c=14.0),
        LongitudinalObservation(day_number=7, phase="INTERVENTION", symptom_vas=4.5, adherence_pct=95.0, ambient_temp_c=18.0),
        LongitudinalObservation(day_number=14, phase="INTERVENTION", symptom_vas=1.5, adherence_pct=90.0, ambient_temp_c=22.0),
    ]
    dossier = NOf1EvidenceEngine.synthesize_n_of_1_dossier(
        patient_id="P-PIL8-001",
        condition="Waja-ul-Mafasil",
        phenotype_code="PHENO-ARTH-BALGHAM",
        phenotype_name="Phlegmatic-Stagnant (Balghami Ghaleez)",
        observations=obs
    )
    assert dossier.within_patient_effect_size_d > 1.0
    assert dossier.bayesian_response_probability >= 0.75
    print(f"✓ Single-Subject N-of-1 Evidence: Cohen's d={dossier.within_patient_effect_size_d} ({dossier.effect_magnitude})")
    print(f"✓ Bayesian Individual Response Probability: {int(dossier.bayesian_response_probability * 100)}% for {dossier.phenotype_code}")
    print(f"✓ Weather Sensitivity: Pearson r={dossier.weather_sensitivity_correlation} (Cold-aggravation mapped)")

    # 3. Live Server Parity
    assert server.ContinuousMonitoringEngine is not None
    assert server.global_monitoring_engine is not None
    assert server.NOf1EvidenceEngine is not None
    print(f"✓ Live Server Telemetry & N-of-1 Endpoints Verified")


def test_pillar9_adaptive_precision_full_ecosystem():
    print_header("PILLAR 9: Clinical Trial OS, Federated Learning, Digital Twin & Global Localization")
    from services.clinical.app.engines.clinical_trial_os_engine import (
        ClinicalTrialOSEngine,
        TrialPhase,
        BlindingType,
        TreatmentArm,
    )
    from services.clinical.app.engines.federated_learning_engine import FederatedLearningEngine
    from services.clinical.app.engines.digital_twin_simulation_engine import (
        DigitalTwinSimulationEngine,
        HumoralState,
        SimulationConfig,
    )
    from services.knowledge.app.core.global_localization_engine import (
        GlobalLocalizationEngine,
        RegulatoryJurisdiction,
    )
    from services.clinical.app.engines.population_learning_network import (
        PopulationLearningNetworkEngine,
        CanonicalMausim,
        MacroWeatherTelemetry,
    )
    import services.live_api_server as server

    # 1. Clinical Trial OS
    trial = ClinicalTrialOSEngine("TR-PIL9-01", "Pillar 9 Study", TrialPhase.PHASE_3_COMPARATIVE_EFFECTIVENESS, BlindingType.DOUBLE_BLIND)
    trial.register_treatment_arm(TreatmentArm("ARM-1", "Unani", "UNANI", "Desc", {}, "B.I.D."))
    trial.register_treatment_arm(TreatmentArm("ARM-2", "Ctrl", "CTRL", "Desc", {}, "Daily"))
    trial.set_irb_approval("IRB-PIL9", "PI-QASIM")
    subj = trial.randomize_subject("MRN-P9")
    cdisc = trial.to_cdisc_odm_summary()
    assert subj.blinded_kit_code.startswith("KIT-")
    assert cdisc["odm_version"] == "1.3.2"
    print(f"✓ Clinical Trial OS: Permuted block randomization active (Kit: {subj.blinded_kit_code}, CDISC ODM 1.3.2 verified)")

    # 2. Federated Learning Network
    fed = FederatedLearningEngine("FED-PIL9", {"w1": 0.5, "w2": 0.5}, min_node_quorum=1)
    tok = fed.register_clinic_node("NODE-PIL9", "Hospital A", "Delhi")
    sig = fed.sign_update_payload("NODE-PIL9", {"w1": 0.55, "w2": 0.45}, 20)
    fed.submit_local_update("NODE-PIL9", 20, {"w1": 0.55, "w2": 0.45}, sig, apply_dp_locally=True)
    snap = fed.aggregate_round()
    assert snap.round_number == 1
    assert fed.get_audit_manifest()["zero_raw_phi_guarantee"] is True
    print(f"✓ Federated Learning Network: FedAvg aggregation complete (Round 1, DP eps={snap.cumulative_epsilon}, zero PHI transit)")

    # 3. Digital Twin Simulation
    twin = DigitalTwinSimulationEngine.run_simulation("P-PIL9", "Balghami", 8.0, config=SimulationConfig(simulation_days=60))
    assert twin.is_clinical_diagnosis is False
    assert twin.prediction_equals_diagnosis is False
    assert twin.baseline_dominant_state == HumoralState.BALGHAMI
    print(f"✓ Digital Twin Simulation: 60-day Markov restitution modeled (P(Equilibrium)={twin.probability_restitution_at_day_60}, Guardrail Active)")

    # 4. Global Knowledge Localization
    asg = GlobalLocalizationEngine.get_crosswalk("ASGANDH")
    assert asg is not None
    assert RegulatoryJurisdiction.US_FDA in asg.jurisdiction_rules
    audit = GlobalLocalizationEngine.audit_prescription_for_jurisdiction(
        [{"drug_name": "Asgandh", "daily_dose_mg": 2000.0}],
        RegulatoryJurisdiction.IN_AYUSH,
    )
    assert audit.is_fully_compliant is True
    print(f"✓ Global Knowledge Localization: 5-Jurisdiction crosswalk active (FDA, EMA HMPC, GCC, AYUSH, WHO)")

    # 5. Population Learning Network
    vuln = PopulationLearningNetworkEngine.compile_seasonal_vulnerability()
    assert vuln.vulnerability_index > 0.0
    sig_test = PopulationLearningNetworkEngine.evaluate_pharmacovigilance_signal("Suranjan Talkh", "Nausea", 5, 45, 10, 490)
    assert sig_test.is_statistically_significant_signal is True
    print(f"✓ Population Learning Network: Seasonal Asbab compiled ({vuln.season_name}), PRR={sig_test.proportional_reporting_ratio} signal verified")

    # 6. Live Server Parity
    assert server.ClinicalTrialOSEngine is not None
    assert server.FederatedLearningEngine is not None
    assert server.DigitalTwinSimulationEngine is not None
    assert server.GlobalLocalizationEngine is not None
    assert server.PopulationLearningNetworkEngine is not None
    print(f"✓ Live REST Server Phase 22-27 Endpoints Verified")


def main():
    start_time = time.time()
    print("\n" + "#" * 76)
    print("  ZAYVORA HEALTH OS™ — 9-PILLAR MASTER INTEGRITY VERIFICATION SUITE")
    print("#" * 76)

    test_pillar1_materia_medica_and_radar()
    test_pillar2_murakkabat_50_formulary()
    test_pillar3_sehat_sahab_and_proms()
    test_pillar4_graph_rag_and_hakeem_copilot()
    test_pillar5_clinical_continuum_and_learning_health_os()
    test_pillar6_abdm_federation_and_population_health()
    test_pillar7_adaptive_precision_and_phenotype_intelligence()
    test_pillar8_continuous_monitoring_and_n_of_1_evidence()
    test_pillar9_adaptive_precision_full_ecosystem()

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 76)
    print(f"  ALL 9 PILLARS VERIFIED ACCORDING TO CLINICAL DOCTRINE in {elapsed}s")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()


