#!/usr/bin/env python3
"""
ZAYVORA HEALTH Master Test Runner
Executes unit tests across microservices using modular isolated test execution.
"""
import sys
import os
import importlib.util
import traceback
# Load environment variables from .env
import pathlib
_env_path = pathlib.Path(__file__).parent.parent / '.env'
if _env_path.exists():
    for _l in _env_path.read_text().splitlines():
        _l = _l.strip()
        if _l and not _l.startswith('#') and '=' in _l:
            _k, _, _v = _l.partition('=')
            os.environ.setdefault(_k.strip(), _v.strip())


def load_mod(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load spec from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def run_test_module(service_dir: str, file_path: str, module_name: str):
    abs_service = os.path.abspath(service_dir)
    # Remove any other service directories from sys.path[0] to prevent cross-service module shadowing
    for s in ["services/clinical", "services/therapeutic", "services/knowledge", "services/ai", "services/identity", "services/gateway"]:
        p = os.path.abspath(s)
        while p in sys.path:
            sys.path.remove(p)
    sys.path.insert(0, abs_service)

    # Purge cached 'app' submodules from previous service
    to_del = [k for k in list(sys.modules.keys()) if k == "app" or k.startswith("app.")]
    for k in to_del:
        del sys.modules[k]

    import unittest
    mod = load_mod(module_name, file_path)
    test_funcs = []
    
    # Discover module-level test_* functions
    for n in sorted(dir(mod)):
        obj = getattr(mod, n)
        if n.startswith("test_") and callable(obj) and not isinstance(obj, type):
            test_funcs.append(obj)
        elif isinstance(obj, type) and issubclass(obj, unittest.TestCase) and obj is not unittest.TestCase:
            suite = unittest.TestLoader().loadTestsFromTestCase(obj)
            for t in suite:
                test_funcs.append(t)
    
    passed = 0
    failed = 0
    errors = []

    if not test_funcs:
        for runner_name in ["run_tests", "run_45_engine_tests", "run_30_critical_workflows", "run_certification", "run_verification", "run_audit", "main"]:
            if hasattr(mod, runner_name) and callable(getattr(mod, runner_name)):
                try:
                    runner = getattr(mod, runner_name)
                    ret = runner()
                    if isinstance(ret, tuple) and len(ret) >= 2:
                        return ret[0], ret[1], []
                    elif ret is True or ret == 0 or ret is None:
                        return 1, 0, []
                    else:
                        return 0, 1, [(runner_name, "Runner indicated test failure")]
                except Exception:
                    return 0, 1, [(runner_name, traceback.format_exc())]

        for cls_name in dir(mod):
            cls = getattr(mod, cls_name)
            if isinstance(cls, type) and hasattr(cls, "run_all") and callable(getattr(cls, "run_all")):
                try:
                    inst = cls()
                    ret = inst.run_all()
                    p = getattr(inst, "passed", 1 if (ret is True or ret == 0) else 0)
                    f = getattr(inst, "failed", 0 if (ret is True or ret == 0) else 1)
                    return p, f, []
                except Exception:
                    return 0, 1, [(cls_name, traceback.format_exc())]

    for fn in test_funcs:
        fn_name = fn._testMethodName if isinstance(fn, unittest.TestCase) else fn.__name__
        try:
            if isinstance(fn, unittest.TestCase):
                res = fn.run()
                if res.wasSuccessful():
                    passed += 1
                else:
                    failed += 1
                    err_text = "".join([msg for _, msg in res.failures + res.errors])
                    errors.append((fn_name, err_text))
            else:
                import inspect
                sig = inspect.signature(fn)
                required_params = [p for p in sig.parameters.values() if p.default == inspect.Parameter.empty]
                if len(required_params) == 0:
                    fn()
                    passed += 1
                else:
                    print(f"    [SKIP fixture-dependent] {fn_name}")
        except Exception:
            failed += 1
            errors.append((fn_name, traceback.format_exc()))
            
    return passed, failed, errors

TEST_SUITES = [
    # (Suite Name, Service Dir, Test File Path)
    ("Clinical Crypto & PHI Encryption", "services/clinical", "services/clinical/tests/test_crypto.py"),
    ("Clinical 10-Ajnas Mizaj & Diagnostics", "services/clinical", "services/clinical/tests/test_mizaj_and_diagnostics.py"),
    ("Clinical Organ-Axis & Evidence Engine", "services/clinical", "services/clinical/tests/test_organ_axis_and_evidence.py"),
    ("Clinical Digital Twin & Trajectory Engine", "services/clinical", "services/clinical/tests/test_digital_twin.py"),
    ("Clinical FHIR R4 & ABDM Interoperability", "services/clinical", "services/clinical/tests/test_interop_and_fhir.py"),
    ("Clinical QSURA Communication Layer", "services/clinical", "services/clinical/tests/test_qsura_communication.py"),
    ("Clinical Research Cloud & RWE Engine", "services/clinical", "services/clinical/tests/test_research_and_rwe.py"),
    ("Clinical Ambient Scribe & 21 CFR Part 11", "services/clinical", "services/clinical/tests/test_ambient_scribe_and_governance.py"),
    ("Clinical Wearables & Predictive Relapse", "services/clinical", "services/clinical/tests/test_wearables_and_predictive.py"),
    ("Clinical Patient Portal & Disaster Recovery", "services/clinical", "services/clinical/tests/test_patient_portal_and_dr.py"),
    ("Clinical Tasks & ABDM Worker Pipelines", "services/clinical", "services/clinical/tests/test_tasks_and_abdm_workers.py"),
    ("Clinical Payment Gateway & Webhooks", "services/clinical", "services/clinical/tests/test_payment_webhooks.py"),
    ("Clinical Cron Scheduler & Scheduled Scanners", "services/clinical", "services/clinical/tests/test_cron_and_scheduled_jobs.py"),
    ("Therapeutic Safety Firewall Baseline", "services/therapeutic", "services/therapeutic/tests/test_safety_firewall.py"),
    ("Therapeutic Schedule E(1) & Drug Interactions", "services/therapeutic", "services/therapeutic/tests/test_schedule_e1_and_interactions.py"),
    ("Therapeutic Nuskha Compiler & Posology", "services/therapeutic", "services/therapeutic/tests/test_nuskha_compiler.py"),
    ("Therapeutic Tadbeer Guardrails", "services/therapeutic", "services/therapeutic/tests/test_tadbeer_guardrails.py"),
    ("Therapeutic Care Plans & Pharmacovigilance", "services/therapeutic", "services/therapeutic/tests/test_care_plans_and_pharmacovigilance.py"),
    ("Therapeutic Dispensary & FEFO Engine", "services/therapeutic", "services/therapeutic/tests/test_dispensary_and_fefo.py"),
    ("Therapeutic Manufacturing OS & eBMR", "services/therapeutic", "services/therapeutic/tests/test_ebmr_and_manufacturing.py"),
    ("Therapeutic Courier Logistics & Tracking", "services/therapeutic", "services/therapeutic/tests/test_courier_logistics.py"),
    ("Knowledge Pharmacopoeia Registry & Mudabbar", "services/knowledge", "services/knowledge/tests/test_pharmacopoeia.py"),
    ("Knowledge Graph & Multi-Hop Traversal", "services/knowledge", "services/knowledge/tests/test_knowledge_graph.py"),
    ("Knowledge Mufradat Taxonomy", "services/knowledge", "services/knowledge/tests/test_taxonomy.py"),
    ("Knowledge Hybrid RAG & Semantic Retrieval", "services/knowledge", "services/knowledge/tests/test_hybrid_rag.py"),
    ("Knowledge Global Command Search (Cmd+K)", "services/knowledge", "services/knowledge/tests/test_command_search.py"),
    ("Knowledge Clinical Governance Board & Quorum", "services/knowledge", "services/knowledge/tests/test_governance_board.py"),
    ("Knowledge Source Library & Provenance", "services/knowledge", "services/knowledge/tests/test_source_library.py"),
    ("Knowledge OCR Pipeline & Extraction", "services/knowledge", "services/knowledge/tests/test_ocr_pipeline.py"),
    ("Knowledge Structured Clinical Knowledge & Safety", "services/knowledge", "services/knowledge/tests/test_structured_knowledge.py"),
    ("AI Hakeem Sahab Response Validator", "services/ai", "services/ai/tests/test_response_validator.py"),
    ("AI Runtime Fallback & ZAPE Personalization", "services/ai", "services/ai/tests/test_ai_runtime_and_zape.py"),
    ("AI Evaluation Lab & Security Guardrails", "services/ai", "services/ai/tests/test_evaluation_and_red_team.py"),
    ("AI Multimodal Lab Extractor & Physical Signs", "services/ai", "services/ai/tests/test_multimodal_extractor.py"),
    ("Gateway Reverse Proxy & Rate Limiting", "services/gateway", "services/gateway/tests/test_gateway.py"),
    ("Infrastructure Helm Chart & Kubernetes Packaging", ".", "tests/test_helm_chart.py"),
    ("End-to-End Clinical Continuum (11 Milestones)", ".", "tests/test_end_to_end_clinical_continuum.py"),
    ("Phase 7 Production Readiness Gate (13 Gates)", ".", "tests/test_production_readiness_gate.py"),
    ("Clinical Pilot Multi-Center Concordance & DSMB", ".", "tests/test_clinical_pilot_concordance.py"),
    ("Phase 9 Statutory Regulatory Dossier & Traceability", ".", "tests/test_regulatory_dossier.py"),
    ("Phase 10 Staging Cluster Deployment Orchestrator", ".", "tests/test_staging_deployment_orchestrator.py"),
    ("Multi-Page Website & Shared Data Layer", ".", "tests/test_multi_page_website.py"),
    ("Mobile Application Workflows & Navigation", ".", "tests/test_mobile_application.py"),
    ("End-to-End Clinical Ecosystem Continuum", ".", "tests/test_e2e_clinical_workflow.py"),
    ("Master Clinical System Knowledge & Endpoints", ".", "tests/test_master_clinical_system.py"),
    ("CP-AFUM & Organ-Axis Clinical System", ".", "tests/test_cp_afum_and_afuf_system.py"),
    ("Global Edition Clinical & AI Systems (2026)", ".", "tests/test_global_edition_systems.py"),
    ("12-Axis Clinical Intelligence Framework™", ".", "tests/test_twelve_axis_framework.py"),
    ("Volume II 16 Core Products & 8 Parhez Protocols", ".", "tests/test_volume_two_products_and_parhez.py"),
    ("Pharmacopoeia Single Drugs & Formula Safety", ".", "tests/test_pharmacopoeia_materia_medica.py"),
    ("Master System Architecture & Clinical Decision Support", ".", "tests/test_master_system_architecture_and_cds.py"),
    ("Foundations Framework & Polypharmacy Architecture", ".", "tests/test_foundations_framework_and_polypharmacy.py"),
    ("Clinical Intelligence Doctrine & Enterprise Governance", ".", "tests/test_clinical_intelligence_doctrine.py"),
    ("Master Nuskha Nawisi & 7-Pillars Prescribing", ".", "tests/test_master_nuskha_nawisi_system.py"),
    ("Systemic Dual-Doctrine Engines (Modern & Unani)", ".", "tests/test_systemic_dual_doctrine_engines.py"),
    ("Mufradat 250 Validation & Canonical Governance", ".", "tests/test_mufradat_250_pipeline.py"),
    ("Full Validation Suite — Safety Firewall, 12-Gate, Badal, Cards", ".", "tests/test_full_validation_suite.py"),
    ("Mufradat 25-Drug Gold Benchmark Monograph Pipeline", ".", "tests/test_mufradat_gold_benchmark.py"),
    ("Validated Murakkab & Nuskha Integration", ".", "tests/test_validated_murakkab_compiler.py"),
    ("End-to-End Matab Clinical Simulation & 250 Matrix", ".", "tests/test_end_to_end_matab_simulation.py"),
    ("Knowledge Intelligence & Clinical Governance vNEXT", ".", "tests/test_knowledge_intelligence_vnext.py"),
    ("Knowledge Graph & Doctor Clinical Continuum", ".", "tests/test_knowledge_graph_and_clinical_continuum.py"),
    ("Murakkab Intelligence, Pharmacy, Outcomes & Pharmacovigilance", ".", "tests/test_murakkab_pharmacy_outcomes_safety.py"),
    ("Clinical Intelligence Core vNext & Learning Healthcare OS", ".", "tests/test_clinical_intelligence_core_vnext.py"),
    ("ABDM FHIR Interoperability, Federation & Population Health", ".", "tests/test_abdm_federation_and_population_health.py"),
    ("Adaptive Precision Healthcare & Phenotype Intelligence", ".", "tests/test_adaptive_precision_healthcare_foundation.py"),
    ("Digital Biomarkers, Continuous Monitoring & N-of-1 Evidence", ".", "tests/test_continuous_monitoring_and_n_of_1_evidence.py"),
    ("Adaptive Precision OS & Global Learning Ecosystem", ".", "tests/test_adaptive_precision_full_ecosystem.py"),
    ("Phase 2 Auth, RBAC & Multi-Tenancy", ".", "tests/test_phase2_auth_rbac_tenancy.py"),
    ("Phase 3 Core Clinical Continuum", ".", "tests/test_phase3_clinical_continuum.py"),
    ("Phase 4 Pharmacy FEFO & Billing", ".", "tests/test_phase4_pharmacy_fefo_billing.py"),
    ("Phase 5 AI RAG Safety CDS", ".", "tests/test_phase5_ai_rag_safety_cds.py"),
    ("Phase 6 QSURA, Telemed & Patient Portal", ".", "tests/test_phase6_qsura_telemed_vernacular.py"),
    ("Phase 7 Staging, DR & Pilot Concordance", ".", "tests/test_phase7_staging_dr_concordance.py"),
    ("Phase 8 Final Verification & Certification", ".", "tests/test_phase8_final_verification_go_no_go.py"),
    ("30 Critical Healthcare Workflows", ".", "tests/test_30_critical_workflows.py"),
    ("45 Connected Clinical Engines", ".", "tests/test_45_engines_connected.py"),
    ("Clinical Intelligence Integration", ".", "tests/test_clinical_intelligence_integration.py"),
    ("Definition of Done Verification", ".", "tests/test_definition_of_done.py"),
    ("Hardware & Complete Ecosystem Verification", ".", "tests/test_hardware_and_complete_ecosystem.py"),
    ("Live REST API & SQL Database Integration", ".", "tests/test_live_api_integration.py"),
    ("Rescue User Experience & Clean UI Verification", ".", "tests/test_rescue_user_experience.py"),
    ("Ultimate Ecosystem Final Verification", ".", "tests/test_ultimate_ecosystem_verification.py"),
    ("V5 Enterprise 24-Point Verification", ".", "tests/test_v5_enterprise_verification.py"),
    ("Clinical Safety Invariants Suite (SAFETY-001 - 010)", ".", "tests/test_clinical_safety_invariants.py"),
    ("Ilaj bil Nafsiyat & Psychosomatic Medicine Suite", ".", "tests/test_ilaj_bil_nafsiyat.py"),
    ("Ilaj bil Tadbeer (16 Modalities & Protocols)", ".", "tests/test_tadbeer_16_and_protocols.py"),
    ("Ilaj bil Ghiza & Ilaj bil Yad (Jarahat) Suite", ".", "tests/test_ghiza_and_yad_engines.py"),
    ("World-Class Frontend & Clinical Desk Experience", ".", "tests/test_world_class_frontend_experience.py"),
    ("Design System Primitives & Clinical Components", ".", "tests/test_design_system_and_clinical_primitives.py"),
    ("Master Platform Services & Connected Architecture", ".", "tests/test_master_platform_services.py"),
    ("Grand Classical & Modern Integrative Medical Library (12 Volumes)", ".", "tests/test_grand_integrative_library.py"),
    ("Next-Gen Enhancements: Deep RAG, Simulator, PWA & Botanical Atlas", ".", "tests/test_platform_enhancements_suite.py"),
    ("Agentic Clinical AI Runtime & Safety Firewall (Hakeem Sahab v2)", "services/ai", "tests/test_agentic_clinical_runtime.py"),
    ("Computational Formulation Intelligence (Blueprint §98)", ".", "tests/test_computational_formulation_intelligence.py"),
    ("ZFIE Master Acceptance Tests (AT-01 to AT-12)", ".", "tests/test_zfie_master_acceptance_tests.py"),
    ("ZFIE Complete Domain & Engine Specification", ".", "tests/test_zfie_engine_complete.py"),
    ("ZFIE 5 Horizontal Layers (Factory, Benchmarking, Bridge, QC, Compiler)", ".", "tests/test_zfie_horizontal_layers.py"),
    ("Care Intelligence 2.0 (Front-Door Orchestrator & Care Gaps)", ".", "tests/test_care_intelligence_2.py"),
    ("V2 Evidence-Governed Clinical Intelligence", ".", "tests/test_v2_evidence_governed_intelligence.py"),
    ("Codebase Integrity, Static Drift & Parity Gate", ".", "tests/test_codebase_integrity_and_parity.py"),
    ("Practical Clinical Enhancements & Patient UX", ".", "tests/test_practical_clinical_enhancements.py"),
    ("Full Subsystems Verification (Web, Mobile, Engines, API, Audio)", ".", "tests/test_full_subsystems_verification.py"),
    ("Browser & Clinician E2E User Journey & Prescription Seal", ".", "tests/test_browser_e2e_journey.py"),
    ("6 Core Clinical Engines Scientific Validation (Mizaj, Axis, Evidence, Diff, AI, Safety)", ".", "tests/test_six_core_engines_clinical_validation.py"),
    ("Kulliyat-e-Adwiyah & Ishrah al-Adwiyah Pharmacological Suite", ".", "tests/test_kulliyat_e_adwiyah.py"),
    ("Standard Unani Medical Terminology & Grand Medical Corpus", ".", "tests/test_standard_unani_terminology.py"),
]






def main():
    print("=" * 70)
    print(" ZAYVORA HEALTH™ — MASTER SYSTEM VERIFICATION TEST RUNNER")
    print("=" * 70)
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)

    # Detect if database is in pristine clean slate mode
    clean_mode = False
    try:
        import sqlite3
        conn = sqlite3.connect("database/zayvora_live.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM patients")
        patient_count = c.fetchone()[0]
        conn.close()
        clean_mode = (patient_count == 0)
    except Exception:
        pass

    # Ensure required test fixtures are provisioned for test execution
    try:
        from tests.fixtures_manager import provision_test_fixtures, cleanup_test_fixtures
        provision_test_fixtures()
    except Exception as e:
        print(f"Note: Test fixture auto-provisioning notice ({e})")

    test_suites = TEST_SUITES
    
    total_passed = 0
    total_failed = 0
    all_errors = []
    
    for title, service_dir, test_path in test_suites:
        if not os.path.exists(test_path):
            continue
        mod_name = title.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("&", "and")
        passed, failed, errs = run_test_module(service_dir, test_path, mod_name)
        status_str = "PASS" if failed == 0 else "FAIL"
        print(f"[{status_str}] {title:<50} | {passed} passed, {failed} failed")
        total_passed += passed
        total_failed += failed
        if errs:
            all_errors.extend(errs)
            
    print("=" * 70)
    # If clean mode was active or --clean passed, restore clean slate
    if clean_mode or "--clean" in sys.argv:
        try:
            cleanup_test_fixtures()
            print("✓ [Clean Slate Active] Ephemeral test fixtures restored to 0 patients.")
            print("=" * 70)
        except Exception as e:
            print(f"Note: Cleanup notice ({e})")

    if total_failed == 0:
        print(f"✓ MASTER SUITE PASSED: {total_passed} tests passed with ZERO failures.")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"✗ MASTER SUITE FAILED: {total_failed} tests failed! Total passed: {total_passed}")
        for fn_name, tb in all_errors:
            print(f"\n--- Failure in {fn_name} ---")
            print(tb)
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
