#!/usr/bin/env python3
"""
ZAYVORA HEALTH Master Test Runner
Executes unit tests across microservices using modular isolated test execution.
"""
import sys
import os
import importlib.util
import traceback

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

def main():
    print("=" * 70)
    print(" ZAYVORA HEALTH™ — MASTER SYSTEM VERIFICATION TEST RUNNER")
    print("=" * 70)
    
    test_suites = [
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
        ("Therapeutic Safety Firewall Baseline", "services/therapeutic", "services/therapeutic/tests/test_safety_firewall.py"),
        ("Therapeutic Schedule E(1) & Drug Interactions", "services/therapeutic", "services/therapeutic/tests/test_schedule_e1_and_interactions.py"),
        ("Therapeutic Nuskha Compiler & Posology", "services/therapeutic", "services/therapeutic/tests/test_nuskha_compiler.py"),
        ("Therapeutic Tadbeer Guardrails", "services/therapeutic", "services/therapeutic/tests/test_tadbeer_guardrails.py"),
        ("Therapeutic Care Plans & Pharmacovigilance", "services/therapeutic", "services/therapeutic/tests/test_care_plans_and_pharmacovigilance.py"),
        ("Therapeutic Dispensary & FEFO Engine", "services/therapeutic", "services/therapeutic/tests/test_dispensary_and_fefo.py"),
        ("Therapeutic Manufacturing OS & eBMR", "services/therapeutic", "services/therapeutic/tests/test_ebmr_and_manufacturing.py"),
        ("Knowledge Pharmacopoeia Registry & Mudabbar", "services/knowledge", "services/knowledge/tests/test_pharmacopoeia.py"),
        ("Knowledge Graph & Multi-Hop Traversal", "services/knowledge", "services/knowledge/tests/test_knowledge_graph.py"),
        ("Knowledge Mufradat Taxonomy", "services/knowledge", "services/knowledge/tests/test_taxonomy.py"),
        ("Knowledge Hybrid RAG & Semantic Retrieval", "services/knowledge", "services/knowledge/tests/test_hybrid_rag.py"),
        ("Knowledge Global Command Search (Cmd+K)", "services/knowledge", "services/knowledge/tests/test_command_search.py"),
        ("Knowledge Clinical Governance Board & Quorum", "services/knowledge", "services/knowledge/tests/test_governance_board.py"),
        ("AI Hakeem Sahab Response Validator", "services/ai", "services/ai/tests/test_response_validator.py"),
        ("AI Runtime Fallback & ZAPE Personalization", "services/ai", "services/ai/tests/test_ai_runtime_and_zape.py"),
        ("AI Evaluation Lab & Security Guardrails", "services/ai", "services/ai/tests/test_evaluation_and_red_team.py"),
        ("AI Multimodal Lab Extractor & Physical Signs", "services/ai", "services/ai/tests/test_multimodal_extractor.py"),
        ("Gateway Reverse Proxy & Rate Limiting", "services/gateway", "services/gateway/tests/test_gateway.py"),
        ("Infrastructure Helm Chart & Kubernetes Packaging", ".", "tests/test_helm_chart.py"),
    ]

    
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
