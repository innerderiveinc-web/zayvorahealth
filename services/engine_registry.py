"""
ZAYVORA Health OS — Subsystem Engine Registry & Microservice Facade
====================================================================
Dynamic loader and fallback facade for all core clinical, knowledge,
therapeutic, identity, and AI engines across the 6 microservices.
"""

import importlib.util
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------------------------------------------------------
# Modular Engine Loaders for Phase 5 AI, Knowledge, Safety & Posology
# -----------------------------------------------------------------------------
def _load_engine(name, rel_path):
    p = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(p):
        return None
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

try:
    pharmacopoeia_mod = _load_engine("pharmacopoeia_core", "services/knowledge/app/core/pharmacopoeia.py")
    UPI_MUFRADAT_REGISTRY = getattr(pharmacopoeia_mod, "UPI_MUFRADAT_REGISTRY", [])
    UPI_PART2_VOL4_MONOGRAPHS = getattr(pharmacopoeia_mod, "UPI_PART2_VOL4_MONOGRAPHS", [])
    match_schedule_e1_substance = getattr(pharmacopoeia_mod, "match_schedule_e1_substance", lambda x: None)
    get_upi_mufradat = getattr(pharmacopoeia_mod, "get_upi_mufradat", lambda: UPI_MUFRADAT_REGISTRY)
    convert_classical_weight = getattr(pharmacopoeia_mod, "convert_classical_weight", lambda q, u: {"quantity": q, "unit": u})
    CLASSICAL_WEIGHTS_METRIC_MAP = getattr(pharmacopoeia_mod, "CLASSICAL_WEIGHTS_METRIC_MAP", {})
    TADBIR_E_ADVIYAH_SOP = getattr(pharmacopoeia_mod, "TADBIR_E_ADVIYAH_SOP", {})
    CANONICAL_LIBRARY_REGISTRY = getattr(pharmacopoeia_mod, "CANONICAL_LIBRARY_REGISTRY", {})
    get_upi_vol4_compound_by_name = getattr(pharmacopoeia_mod, "get_upi_vol4_compound_by_name", lambda x: None)
except Exception:
    pharmacopoeia_mod = None
    UPI_MUFRADAT_REGISTRY = []
    UPI_PART2_VOL4_MONOGRAPHS = []
    match_schedule_e1_substance = lambda x: None
    get_upi_mufradat = lambda: []
    convert_classical_weight = lambda q, u: {"quantity": q, "unit": u}
    CLASSICAL_WEIGHTS_METRIC_MAP = {}
    TADBIR_E_ADVIYAH_SOP = {}
    CANONICAL_LIBRARY_REGISTRY = {}
    get_upi_vol4_compound_by_name = lambda x: None

try:
    kulliyat_mod = _load_engine("kulliyat_core", "services/knowledge/app/core/kulliyat_e_adwiyah.py")
    get_all_pharmacological_actions = getattr(kulliyat_mod, "get_all_pharmacological_actions", lambda: [])
    search_actions = getattr(kulliyat_mod, "search_actions", lambda q: [])
    get_action_by_id_or_name = getattr(kulliyat_mod, "get_action_by_id_or_name", lambda q: None)
    get_taste_pharmacodynamics = getattr(kulliyat_mod, "get_taste_pharmacodynamics", lambda t=None: {})
    get_temperament_degree = getattr(kulliyat_mod, "get_temperament_degree", lambda d: None)
    get_all_compounding_rules = getattr(kulliyat_mod, "get_all_compounding_rules", lambda: [])
    get_antagonism_mechanisms = getattr(kulliyat_mod, "get_antagonism_mechanisms", lambda: {})
    get_kulliyat_metadata = getattr(kulliyat_mod, "get_kulliyat_metadata", lambda: {})
except Exception:
    kulliyat_mod = None
    get_all_pharmacological_actions = lambda: []
    search_actions = lambda q: []
    get_action_by_id_or_name = lambda q: None
    get_taste_pharmacodynamics = lambda t=None: {}
    get_temperament_degree = lambda d: None
    get_all_compounding_rules = lambda: []
    get_antagonism_mechanisms = lambda: {}
    get_kulliyat_metadata = lambda: {}

try:
    terminology_mod = _load_engine("standard_unani_terminology", "services/knowledge/app/core/standard_unani_terminology.py")
    get_terminology_engine = getattr(terminology_mod, "get_terminology_engine", lambda: None)
except Exception:
    terminology_mod = None
    get_terminology_engine = lambda: None

try:
    corpus_mod = _load_engine("grand_medical_books_corpus", "services/knowledge/app/data/grand_medical_books_corpus.py")
    get_all_medical_books_in_corpus = getattr(corpus_mod, "get_all_medical_books_in_corpus", lambda: [])
    search_corpus = getattr(corpus_mod, "search_corpus", lambda q: [])
    get_corpus_categories_summary = getattr(corpus_mod, "get_corpus_categories_summary", lambda: {})
except Exception:
    corpus_mod = None
    get_all_medical_books_in_corpus = lambda: []
    search_corpus = lambda q: []
    get_corpus_categories_summary = lambda: {}


# Production Hardening: FAIL-CLOSED Safety Firewall
# If the safety engine is unavailable, the system MUST NOT silently default to SAFE_TO_CONSIDER.
# It MUST issue a clinical hold / block and alert the practitioner.
def _fail_closed_safety_firewall(**k):
    return {
        "verdict": "DO_NOT_RECOMMEND",
        "reasons": ["CRITICAL CLINICAL HOLD: Safety firewall module unavailable. Fail-closed policy enforced; prescription must be manually authorized."],
        "isClinicalHold": True,
        "requiresPractitionerSignoff": True,
        "failClosedTriggered": True
    }

try:
    safety_mod = _load_engine("safety_firewall_core", "services/therapeutic/app/engines/safety_firewall.py")
    run_safety_firewall = getattr(safety_mod, "run_safety_firewall", _fail_closed_safety_firewall)
except Exception as _e:
    safety_mod = None
    run_safety_firewall = _fail_closed_safety_firewall

try:
    zape_mod = _load_engine("zape_core", "services/ai/app/engines/zape_personalization.py")
    run_zape_personalization = getattr(zape_mod, "run_zape_personalization", None)
    calculate_age_and_renal_posology = getattr(zape_mod, "calculate_age_and_renal_posology", None)
except Exception:
    zape_mod = None
    run_zape_personalization = None
    calculate_age_and_renal_posology = None

try:
    validator_mod = _load_engine("validator_core", "services/ai/app/engines/response_validator.py")
    parse_sections = getattr(validator_mod, "parse_sections", lambda text: {})
    validate_response_structure = getattr(validator_mod, "validate_response_structure", lambda text: [])
except Exception:
    validator_mod = None
    parse_sections = lambda text: {}
    validate_response_structure = lambda text: []

try:
    qsura_mod = _load_engine("qsura_broker_core", "services/clinical/app/qsura/communication_broker.py")
    QSURACommunicationBroker = getattr(qsura_mod, "QSURACommunicationBroker", None)
    MESSAGE_TEMPLATES = getattr(qsura_mod, "MESSAGE_TEMPLATES", {})
except Exception:
    qsura_mod = None
    QSURACommunicationBroker = None
    MESSAGE_TEMPLATES = {}
try:
    zmie_firewall_mod = _load_engine("zmie_provenance_firewall", "services/knowledge/app/engines/zmie_provenance_firewall.py")
    EVIDENCE_LADDER_TIERS = getattr(zmie_firewall_mod, "EVIDENCE_LADDER_TIERS", {})
    EvidenceProvenanceClaim = getattr(zmie_firewall_mod, "EvidenceProvenanceClaim", None)
    TripartiteKnowledgeUnit = getattr(zmie_firewall_mod, "TripartiteKnowledgeUnit", None)
    UncertaintyAssessment = getattr(zmie_firewall_mod, "UncertaintyAssessment", None)
    ScientificMizajEvaluation = getattr(zmie_firewall_mod, "ScientificMizajEvaluation", None)
    ClinicalCopilotAdvisory = getattr(zmie_firewall_mod, "ClinicalCopilotAdvisory", None)
    ClinicalTruthFirewall = getattr(zmie_firewall_mod, "ClinicalTruthFirewall", None)
except Exception:
    EVIDENCE_LADDER_TIERS = {}
    ClinicalTruthFirewall = None

# -----------------------------------------------------------------------------
try:
    organ_axes_mod = _load_engine("organ_axes_master", "services/knowledge/app/data/organ_axes_master.py")
    MASTER_ORGAN_AXES = getattr(organ_axes_mod, "MASTER_ORGAN_AXES", {})
    score_organ_axes = getattr(organ_axes_mod, "score_organ_axes", None)
    get_all_axes = getattr(organ_axes_mod, "get_all_axes", lambda: list(MASTER_ORGAN_AXES.values()))
    get_axis_by_id = getattr(organ_axes_mod, "get_axis_by_id", lambda x: None)
except Exception:
    organ_axes_mod = None
    MASTER_ORGAN_AXES = {}
    score_organ_axes = None
    get_all_axes = lambda: []
    get_axis_by_id = lambda x: None

try:
    protocols_mod = _load_engine("protocols_master", "services/knowledge/app/data/protocols_master.py")
    MASTER_PROTOCOLS = getattr(protocols_mod, "MASTER_PROTOCOLS", {})
    get_all_protocols = getattr(protocols_mod, "get_all_protocols", lambda: list(MASTER_PROTOCOLS.values()))
    get_protocol_by_id = getattr(protocols_mod, "get_protocol_by_id", lambda x: None)
except Exception:
    protocols_mod = None
    MASTER_PROTOCOLS = {}
    get_all_protocols = lambda: []
    get_protocol_by_id = lambda x: None

try:
    products_mod = _load_engine("products_master", "services/knowledge/app/data/products_master.py")
    MASTER_PRODUCTS = getattr(products_mod, "MASTER_PRODUCTS", {})
    get_all_products = getattr(products_mod, "get_all_products", lambda: list(MASTER_PRODUCTS.values()))
    get_product_by_sku = getattr(products_mod, "get_product_by_sku", lambda x: None)
except Exception:
    products_mod = None
    MASTER_PRODUCTS = {}
    get_all_products = lambda: []
    get_product_by_sku = lambda x: None

try:
    kits_mod = _load_engine("kits_master", "services/knowledge/app/data/kits_master.py")
    MASTER_KITS = getattr(kits_mod, "MASTER_KITS", {})
    get_all_kits = getattr(kits_mod, "get_all_kits", lambda: list(MASTER_KITS.values()))
    get_kit_by_id = getattr(kits_mod, "get_kit_by_id", lambda x: None)
except Exception:
    kits_mod = None
    MASTER_KITS = {}
    get_all_kits = lambda: []
    get_kit_by_id = lambda x: None

try:
    parhez_mod = _load_engine("parhez_master", "services/knowledge/app/data/parhez_master.py")
    MASTER_PARHEZ = getattr(parhez_mod, "MASTER_PARHEZ", {})
    get_all_parhez = getattr(parhez_mod, "get_all_parhez", lambda: list(MASTER_PARHEZ.values()))
    get_parhez_by_code = getattr(parhez_mod, "get_parhez_by_code", lambda x: None)
except Exception:
    parhez_mod = None
    MASTER_PARHEZ = {}
    get_all_parhez = lambda: []
    get_parhez_by_code = lambda x: None

try:
    interactions_mod = _load_engine("drug_interactions_master", "services/knowledge/app/data/drug_interactions_master.py")
    check_drug_herb_interactions = getattr(interactions_mod, "check_drug_herb_interactions", lambda *a, **k: [])
    get_all_interactions = getattr(interactions_mod, "get_all_interactions", lambda: [])
    get_universal_contraindications = getattr(interactions_mod, "get_universal_contraindications", lambda: {})
except Exception:
    interactions_mod = None
    check_drug_herb_interactions = lambda *a, **k: []
    get_all_interactions = lambda: []
    get_universal_contraindications = lambda: {}

try:
    zmai_mod = _load_engine("zmai_scoring_tool", "services/knowledge/app/data/zmai_scoring_tool.py")
    calculate_zmai_score = getattr(zmai_mod, "calculate_zmai_score", None)
    calculate_mizaj_2_matrix = getattr(zmai_mod, "calculate_mizaj_2_matrix", None)
    MIZAJ_2_DOMAINS = getattr(zmai_mod, "MIZAJ_2_DOMAINS", [])
    get_all_domains = getattr(zmai_mod, "get_all_domains", lambda: {})
except Exception:
    zmai_mod = None
    calculate_zmai_score = None
    calculate_mizaj_2_matrix = None
    MIZAJ_2_DOMAINS = []
    get_all_domains = lambda: {}

try:
    nuskha_compiler_mod = _load_engine("nuskha_compiler_core", "services/therapeutic/app/engines/nuskha_compiler.py")
    verify_four_tier_nuskha_architecture = getattr(nuskha_compiler_mod, "verify_four_tier_nuskha_architecture", None)
except Exception:
    nuskha_compiler_mod = None
    verify_four_tier_nuskha_architecture = None

try:
    udc_mod = _load_engine("udc_engine", "services/clinical/app/engines/udc_engine.py")
    generate_udc = getattr(udc_mod, "generate_udc", None)
    parse_udc = getattr(udc_mod, "parse_udc", None)
except Exception:
    generate_udc = None
    parse_udc = None

try:
    mizaj_dose_mod = _load_engine("mizaj_dose_engine", "services/clinical/app/engines/mizaj_dose_engine.py")
    calculate_mizaj_dose_adjustments = getattr(mizaj_dose_mod, "calculate_mizaj_dose_adjustments", None)
except Exception:
    calculate_mizaj_dose_adjustments = None

try:
    functional_lab_mod = _load_engine("functional_lab_engine", "services/clinical/app/engines/functional_lab_engine.py")
    calculate_homa_ir = getattr(functional_lab_mod, "calculate_homa_ir", None)
    calculate_tg_hdl_ratio = getattr(functional_lab_mod, "calculate_tg_hdl_ratio", None)
    evaluate_semen_analysis = getattr(functional_lab_mod, "evaluate_semen_analysis", None)
    evaluate_five_non_negotiable_lab_trigger_rules = getattr(functional_lab_mod, "evaluate_five_non_negotiable_lab_trigger_rules", None)
    verify_humoral_biomarker_correlation = getattr(functional_lab_mod, "verify_humoral_biomarker_correlation", None)
except Exception:
    calculate_homa_ir = None
    calculate_tg_hdl_ratio = None
    evaluate_semen_analysis = None
    evaluate_five_non_negotiable_lab_trigger_rules = None
    verify_humoral_biomarker_correlation = None

try:
    phase_eng_mod = _load_engine("phase_therapeutic_engine", "services/clinical/app/engines/phase_therapeutic_engine.py")
    evaluate_phase_trigger_rules = getattr(phase_eng_mod, "evaluate_phase_trigger_rules", None)
    verify_phase_1_exit = getattr(phase_eng_mod, "verify_phase_1_exit", None)
    verify_phase_2_exit = getattr(phase_eng_mod, "verify_phase_2_exit", None)
except Exception:
    evaluate_phase_trigger_rules = None
    verify_phase_1_exit = None
    verify_phase_2_exit = None

try:
    dual_track_mod = _load_engine("dual_track_engine", "services/therapeutic/app/engines/dual_track_engine.py")
    evaluate_clinical_delivery_track = getattr(dual_track_mod, "evaluate_clinical_delivery_track", None)
    GMP_PRODUCTS_MASTER = getattr(dual_track_mod, "GMP_PRODUCTS_MASTER", {})
except Exception:
    evaluate_clinical_delivery_track = None
    GMP_PRODUCTS_MASTER = {}

try:
    ilaj_hierarchy_mod = _load_engine("ilaj_hierarchy_engine", "services/therapeutic/app/engines/ilaj_hierarchy_engine.py")
    evaluate_ilaj_hierarchy_compliance = getattr(ilaj_hierarchy_mod, "evaluate_ilaj_hierarchy_compliance", None)
    TADBEER_MODALITIES = getattr(ilaj_hierarchy_mod, "TADBEER_MODALITIES", {})
except Exception:
    evaluate_ilaj_hierarchy_compliance = None
    TADBEER_MODALITIES = {}

try:
    tadbeer_guard_mod = _load_engine("tadbeer_guardrails", "services/therapeutic/app/engines/tadbeer_guardrails.py")
    TADBEER_MODALITIES_16 = getattr(tadbeer_guard_mod, "TADBEER_MODALITIES_16", {})
    USOOL_E_TADBEER_PRINCIPLES = getattr(tadbeer_guard_mod, "USOOL_E_TADBEER_PRINCIPLES", {})
    MULTI_MODAL_TREATMENT_TRAJECTORIES = getattr(tadbeer_guard_mod, "MULTI_MODAL_TREATMENT_TRAJECTORIES", {})
    HOME_SELF_CARE_SPEC = getattr(tadbeer_guard_mod, "HOME_SELF_CARE_SPEC", {})
    run_tadbeer_guardrails = getattr(tadbeer_guard_mod, "run_tadbeer_guardrails", None)
except Exception:
    TADBEER_MODALITIES_16 = {}
    USOOL_E_TADBEER_PRINCIPLES = {}
    MULTI_MODAL_TREATMENT_TRAJECTORIES = {}
    HOME_SELF_CARE_SPEC = {}
    run_tadbeer_guardrails = None

try:
    safety_firewall_mod = _load_engine("safety_firewall_ext", "services/therapeutic/app/engines/safety_firewall.py")
    evaluate_cp_afum_clinical_safety = getattr(safety_firewall_mod, "evaluate_cp_afum_clinical_safety", None)
except Exception:
    evaluate_cp_afum_clinical_safety = None

try:
    curriculum_mod = _load_engine("cp_afum_curriculum", "services/clinical/app/engines/cp_afum_curriculum.py")
    get_curriculum_summary = getattr(curriculum_mod, "get_curriculum_summary", None)
except Exception:
    get_curriculum_summary = None

try:
    practicum_mod = _load_engine("practicum_registry", "services/clinical/app/engines/practicum_registry.py")
    validate_practicum_case = getattr(practicum_mod, "validate_practicum_case", None)
    evaluate_practicum_portfolio = getattr(practicum_mod, "evaluate_practicum_portfolio", None)
except Exception:
    validate_practicum_case = None
    evaluate_practicum_portfolio = None

try:
    cert_mod = _load_engine("certification_engine", "services/clinical/app/engines/certification_engine.py")
    evaluate_practitioner_tier = getattr(cert_mod, "evaluate_practitioner_tier", None)
    CERTIFICATION_LEVELS = getattr(cert_mod, "CERTIFICATION_LEVELS", {})
except Exception:
    evaluate_practitioner_tier = None
    CERTIFICATION_LEVELS = {}

# ── ZAYVORA Global Edition (Second Edition 2026) Engines ─────────────────
try:
    zape_mod = _load_engine("zape_engine", "services/clinical/app/engines/zape_engine.py")
    ZAPEEngine = getattr(zape_mod, "ZAPEEngine", None)
except Exception:
    ZAPEEngine = None

try:
    regimen_mod = _load_engine("regimental_hydrotherapy_engine", "services/therapeutic/app/engines/regimental_hydrotherapy_engine.py")
    RegimentalHydrotherapyEngine = getattr(regimen_mod, "RegimentalHydrotherapyEngine", None)
except Exception:
    RegimentalHydrotherapyEngine = None

try:
    protocols_mod = _load_engine("global_protocols_engine", "services/clinical/app/engines/global_protocols_engine.py")
    GlobalProtocolsEngine = getattr(protocols_mod, "GlobalProtocolsEngine", None)
except Exception:
    GlobalProtocolsEngine = None

try:
    evidence_mod = _load_engine("evidence_glossary_engine", "services/knowledge/app/engines/evidence_glossary_engine.py")
    EvidenceGlossaryEngine = getattr(evidence_mod, "EvidenceGlossaryEngine", None)
except Exception:
    EvidenceGlossaryEngine = None

# ── ZAYVORA 12-Axis Clinical Intelligence Framework™ ─────────────────────
try:
    axes12_schema_mod = _load_engine("organ_axes_12_schema", "services/knowledge/app/data/organ_axes_12_schema.py")
    ORGAN_AXES_12 = getattr(axes12_schema_mod, "ORGAN_AXES_12", {})
    get_all_organ_axes = getattr(axes12_schema_mod, "get_all_organ_axes", lambda: list(ORGAN_AXES_12.values()))
    get_axis_by_id = getattr(axes12_schema_mod, "get_axis_by_id", lambda x: None)
except Exception:
    ORGAN_AXES_12 = {}
    get_all_organ_axes = lambda: []
    get_axis_by_id = lambda x: None

try:
    twelve_axis_mod = _load_engine("twelve_axis_engine", "services/clinical/app/engines/twelve_axis_engine.py")
    TwelveAxisEngine = getattr(twelve_axis_mod, "TwelveAxisEngine", None)
except Exception:
    TwelveAxisEngine = None

# ── ZAYVORA Volume II: 16 Core Products & 8 Parhez Protocols ───────────────
try:
    prod16_mod = _load_engine("product_matrix_16", "services/therapeutic/app/data/product_matrix_16.py")
    CORE_PRODUCTS_16 = getattr(prod16_mod, "CORE_PRODUCTS_16", {})
    get_all_core_products = getattr(prod16_mod, "get_all_core_products", lambda: list(CORE_PRODUCTS_16.values()))
    get_product_by_id = getattr(prod16_mod, "get_product_by_id", lambda x: None)
except Exception:
    CORE_PRODUCTS_16 = {}
    get_all_core_products = lambda: []
    get_product_by_id = lambda x: None

try:
    parhez8_mod = _load_engine("parhez_protocols_8", "services/clinical/app/data/parhez_protocols_8.py")
    PARHEZ_PROTOCOLS_8 = getattr(parhez8_mod, "PARHEZ_PROTOCOLS_8", {})
    get_all_parhez_protocols = getattr(parhez8_mod, "get_all_parhez", lambda: list(PARHEZ_PROTOCOLS_8.values()))
    get_parhez_protocol_by_code = getattr(parhez8_mod, "get_parhez_by_code", lambda x: None)
except Exception:
    PARHEZ_PROTOCOLS_8 = {}
    get_all_parhez_protocols = lambda: []
    get_parhez_protocol_by_code = lambda x: None

# ── ZAYVORA Pharmacopoeia: Classical Single Drugs & Formula Safety ─────────
try:
    pharmacopoeia_mod = _load_engine("pharmacopoeia_monographs", "services/knowledge/app/data/pharmacopoeia_monographs.py")
    MONOGRAPHS = getattr(pharmacopoeia_mod, "MONOGRAPHS", {})
    get_all_monographs = getattr(pharmacopoeia_mod, "get_all_monographs", lambda: list(MONOGRAPHS.values()))
    get_monograph_by_key = getattr(pharmacopoeia_mod, "get_monograph_by_key", lambda x: MONOGRAPHS.get(x.upper()) if isinstance(x, str) else None)
    search_monographs = getattr(pharmacopoeia_mod, "search_monographs", lambda q: [])
except Exception:
    pharmacopoeia_mod = None
    MONOGRAPHS = {}
    get_all_monographs = lambda: []
    get_monograph_by_key = lambda x: None
    search_monographs = lambda q: []

try:
    safety_checker_mod = _load_engine("formula_safety_checker", "services/therapeutic/app/engines/formula_safety_checker.py")
    FormulaSafetyChecker = getattr(safety_checker_mod, "FormulaSafetyChecker", None)
except Exception:
    safety_checker_mod = None
    FormulaSafetyChecker = None

# ── ZAYVORA Master Clinical Architecture: Dual-Tier & Clinical Decision Support ─
try:
    dual_tier_mod = _load_engine("dual_tier_product_catalog", "services/knowledge/app/data/dual_tier_product_catalog.py")
    DUAL_TIER_CATALOG = getattr(dual_tier_mod, "DUAL_TIER_CATALOG", {})
    get_all_dual_tier_products = getattr(dual_tier_mod, "get_all_dual_tier_products", lambda: list(DUAL_TIER_CATALOG.values()))
    get_dual_tier_product = getattr(dual_tier_mod, "get_dual_tier_product", lambda x: DUAL_TIER_CATALOG.get(x.upper()) if isinstance(x, str) else None)
    validate_80_20_compliance = getattr(dual_tier_mod, "validate_80_20_compliance", None)
except Exception:
    DUAL_TIER_CATALOG = {}
    get_all_dual_tier_products = lambda: []
    get_dual_tier_product = lambda x: None
    validate_80_20_compliance = None

try:
    pricing_mod = _load_engine("program_packages_pricing", "services/knowledge/app/data/program_packages_pricing.py")
    PROGRAM_TIER_SPECS = getattr(pricing_mod, "PROGRAM_TIER_SPECS", {})
    PROGRAM_SPECIFIC_PRICING = getattr(pricing_mod, "PROGRAM_SPECIFIC_PRICING", {})
    get_program_pricing = getattr(pricing_mod, "get_program_pricing", lambda *a: None)
    calculate_clinic_revenue_projection = getattr(pricing_mod, "calculate_clinic_revenue_projection", None)
except Exception:
    PROGRAM_TIER_SPECS = {}
    PROGRAM_SPECIFIC_PRICING = {}
    get_program_pricing = lambda *a: None
    calculate_clinic_revenue_projection = None

try:
    matab_mod = _load_engine("matab_compounding_formulas", "services/knowledge/app/data/matab_compounding_formulas.py")
    MATAB_FORMULAS = getattr(matab_mod, "MATAB_FORMULAS", {})
    get_all_matab_formulas = getattr(matab_mod, "get_all_matab_formulas", lambda: list(MATAB_FORMULAS.values()))
    get_matab_formula = getattr(matab_mod, "get_matab_formula", lambda x: MATAB_FORMULAS.get(x.upper()) if isinstance(x, str) else None)
except Exception:
    MATAB_FORMULAS = {}
    get_all_matab_formulas = lambda: []
    get_matab_formula = lambda x: None

try:
    edu_mod = _load_engine("patient_education_modules", "services/knowledge/app/data/patient_education_modules.py")
    PATIENT_EDUCATION_CHAPTERS = getattr(edu_mod, "PATIENT_EDUCATION_CHAPTERS", {})
    get_all_patient_education_modules = getattr(edu_mod, "get_all_patient_education_modules", lambda: list(PATIENT_EDUCATION_CHAPTERS.values()))
    get_patient_education_module = getattr(edu_mod, "get_patient_education_module", lambda x: None)
except Exception:
    PATIENT_EDUCATION_CHAPTERS = {}
    get_all_patient_education_modules = lambda: []
    get_patient_education_module = lambda x: None

try:
    cds_ext_mod = _load_engine("clinical_decision_support_ext", "services/clinical/app/engines/clinical_decision_support_ext.py")
    ClinicalDecisionSupportExt = getattr(cds_ext_mod, "ClinicalDecisionSupportExt", None)
except Exception:
    ClinicalDecisionSupportExt = None

try:
    red_flag_mod = _load_engine("emergency_red_flag_guard", "services/clinical/app/engines/emergency_red_flag_guard.py")
    EmergencyRedFlagGuard = getattr(red_flag_mod, "EmergencyRedFlagGuard", None)
except Exception:
    EmergencyRedFlagGuard = None

try:
    evidence_matrix_mod = _load_engine("evidence_grading_matrix", "services/knowledge/app/data/evidence_grading_matrix.py")
    get_all_evidence_tiers = getattr(evidence_matrix_mod, "get_all_evidence_tiers", lambda: [])
    get_evidence_tier_details = getattr(evidence_matrix_mod, "get_evidence_tier_details", lambda x: None)
    validate_product_claim = getattr(evidence_matrix_mod, "validate_product_claim", None)
except Exception:
    get_all_evidence_tiers = lambda: []
    get_evidence_tier_details = lambda x: None
    validate_product_claim = None

try:
    nafsiyat_mod = _load_engine("ilaj_bil_nafsiyat_engine", "services/clinical/app/engines/ilaj_bil_nafsiyat_engine.py")
    IlajBilNafsiyatEngine = getattr(nafsiyat_mod, "IlajBilNafsiyatEngine", None)
    NafsiyatAssessmentInput = getattr(nafsiyat_mod, "NafsiyatAssessmentInput", None)
    VERIFIED_CASE_STUDY_PROTOCOLS = getattr(nafsiyat_mod, "VERIFIED_CASE_STUDY_PROTOCOLS", {})
    CLASSICAL_NAFSIYAT_TAXONOMY = getattr(nafsiyat_mod, "CLASSICAL_NAFSIYAT_TAXONOMY", {})
    ITRAFAT_AROMATHERAPY_CATALOG = getattr(nafsiyat_mod, "ITRAFAT_AROMATHERAPY_CATALOG", {})
    TANAFFUS_BREATHWORK_PROTOCOLS = getattr(nafsiyat_mod, "TANAFFUS_BREATHWORK_PROTOCOLS", {})
except Exception:
    IlajBilNafsiyatEngine = None
    NafsiyatAssessmentInput = None
    VERIFIED_CASE_STUDY_PROTOCOLS = {}
    CLASSICAL_NAFSIYAT_TAXONOMY = {}
    ITRAFAT_AROMATHERAPY_CATALOG = {}
    TANAFFUS_BREATHWORK_PROTOCOLS = {}


try:
    ghiza_mod = _load_engine("ilaj_bil_ghiza_engine", "services/therapeutic/app/engines/ilaj_bil_ghiza_engine.py")
    IlajBilGhizaEngine = getattr(ghiza_mod, "IlajBilGhizaEngine", None)
    GhizaAssessmentInput = getattr(ghiza_mod, "GhizaAssessmentInput", None)
    CANONICAL_THERAPEUTIC_PREPARATIONS = getattr(ghiza_mod, "CANONICAL_THERAPEUTIC_PREPARATIONS", {})
    CANONICAL_FOOD_ANTAGONISMS = getattr(ghiza_mod, "CANONICAL_FOOD_ANTAGONISMS", [])
    NUTRIENT_CATEGORIES = getattr(ghiza_mod, "NUTRIENT_CATEGORIES", {})
except Exception:
    IlajBilGhizaEngine = None
    GhizaAssessmentInput = None
    CANONICAL_THERAPEUTIC_PREPARATIONS = {}
    CANONICAL_FOOD_ANTAGONISMS = []
    NUTRIENT_CATEGORIES = {}

try:
    yad_mod = _load_engine("ilaj_bil_yad_engine", "services/therapeutic/app/engines/ilaj_bil_yad_engine.py")
    IlajBilYadEngine = getattr(yad_mod, "IlajBilYadEngine", None)
    SurgicalAssessmentInput = getattr(yad_mod, "SurgicalAssessmentInput", None)
    CLASSICAL_JARAHAT_MODALITIES = getattr(yad_mod, "CLASSICAL_JARAHAT_MODALITIES", {})
    AL_ZAHRAWI_INSTRUMENTS = getattr(yad_mod, "AL_ZAHRAWI_INSTRUMENTS", {})
    CICATRIZING_STYPTIC_FORMULARY = getattr(yad_mod, "CICATRIZING_STYPTIC_FORMULARY", {})
except Exception:
    IlajBilYadEngine = None
    SurgicalAssessmentInput = None
    CLASSICAL_JARAHAT_MODALITIES = {}
    AL_ZAHRAWI_INSTRUMENTS = {}
    CICATRIZING_STYPTIC_FORMULARY = {}

try:
    doctrine_mod = _load_engine("clinical_doctrine_spec", "services/knowledge/app/data/clinical_doctrine_spec.py")
    get_clinical_doctrine = getattr(doctrine_mod, "get_clinical_doctrine", lambda: {})
    get_evidence_tier_e = getattr(doctrine_mod, "get_evidence_tier_e", lambda x: None)
    validate_knowledge_state_transition = getattr(doctrine_mod, "validate_knowledge_state_transition", None)
except Exception:
    get_clinical_doctrine = lambda: {}
    get_evidence_tier_e = lambda x: None
    validate_knowledge_state_transition = None

try:
    nuskha_sm_mod = _load_engine("nuskha_state_machine", "services/therapeutic/app/engines/nuskha_state_machine.py")
    NuskhaStateMachine = getattr(nuskha_sm_mod, "NuskhaStateMachine", None)
except Exception:
    NuskhaStateMachine = None

try:
    copilot_guard_mod = _load_engine("copilot_permission_guard", "services/ai/app/security/copilot_permission_guard.py")
    CopilotPermissionGuard = getattr(copilot_guard_mod, "CopilotPermissionGuard", None)
except Exception:
    CopilotPermissionGuard = None

try:
    patient_360_mod = _load_engine("patient_360_engine", "services/clinical/app/engines/patient_360_engine.py")
    Patient360Engine = getattr(patient_360_mod, "Patient360Engine", None)
except Exception:
    Patient360Engine = None

try:
    php_mod = _load_engine("personal_health_profile_engine", "services/clinical/app/engines/personal_health_profile_engine.py")
    PersonalHealthProfileEngine = getattr(php_mod, "PersonalHealthProfileEngine", None)
except Exception:
    PersonalHealthProfileEngine = None

try:
    afaal_mod = _load_engine("afaal_cascade_engine", "services/clinical/app/engines/afaal_cascade_engine.py")
    AFAAL_STAGES = getattr(afaal_mod, "AFAAL_STAGES", {})
except Exception:
    AFAAL_STAGES = {}

try:
    canonical_safety_mod = _load_engine("canonical_safety_service", "services/therapeutic/app/engines/canonical_safety_service.py")
    CanonicalSafetyService = getattr(canonical_safety_mod, "CanonicalSafetyService", None)
except Exception:
    CanonicalSafetyService = None

try:
    case_brief_mod = _load_engine("hakeem_case_brief_engine", "services/ai/app/engines/hakeem_case_brief_engine.py")
    HakeemCaseBriefEngine = getattr(case_brief_mod, "HakeemCaseBriefEngine", None)
except Exception:
    HakeemCaseBriefEngine = None

try:
    master_nuskha_mod = _load_engine("master_nuskha_architect", "services/therapeutic/app/engines/master_nuskha_architect.py")
    synthesize_master_nuskha = getattr(master_nuskha_mod, "synthesize_master_nuskha", None)
    ORGAN_BADRAQA_CONDUIT_REGISTRY = getattr(master_nuskha_mod, "ORGAN_BADRAQA_CONDUIT_REGISTRY", {})
    ORGAN_PARHEZ_MATRIX = getattr(master_nuskha_mod, "ORGAN_PARHEZ_MATRIX", {})
except Exception:
    synthesize_master_nuskha = None
    ORGAN_BADRAQA_CONDUIT_REGISTRY = {}
    ORGAN_PARHEZ_MATRIX = {}

try:
    qaroorah_mod = _load_engine("qaroorah_diagnostic_engine", "services/clinical/app/engines/qaroorah_diagnostic_engine.py")
    QaroorahDiagnosticEngine = getattr(qaroorah_mod, "QaroorahDiagnosticEngine", None)
    QaroorahPhysicalInspection = getattr(qaroorah_mod, "QaroorahPhysicalInspection", None)
    ModernUrinalysisData = getattr(qaroorah_mod, "ModernUrinalysisData", None)
except Exception:
    QaroorahDiagnosticEngine = None
    QaroorahPhysicalInspection = None
    ModernUrinalysisData = None

try:
    baraaz_mod = _load_engine("baraaz_diagnostic_engine", "services/clinical/app/engines/baraaz_diagnostic_engine.py")
    BaraazDiagnosticEngine = getattr(baraaz_mod, "BaraazDiagnosticEngine", None)
    BaraazInspectionInput = getattr(baraaz_mod, "BaraazInspectionInput", None)
except Exception:
    BaraazDiagnosticEngine = None
    BaraazInspectionInput = None

try:
    asbab_mod = _load_engine("asbab_sitta_scoring_engine", "services/clinical/app/engines/asbab_sitta_scoring_engine.py")
    AsbabSittaScoringEngine = getattr(asbab_mod, "AsbabSittaScoringEngine", None)
    AsbabSittaPatientInput = getattr(asbab_mod, "AsbabSittaPatientInput", None)
except Exception:
    AsbabSittaScoringEngine = None
    AsbabSittaPatientInput = None

try:
    munzij_mod = _load_engine("munzij_mushil_protocol_engine", "services/therapeutic/app/engines/munzij_mushil_protocol_engine.py")
    MunzijMushilProtocolEngine = getattr(munzij_mod, "MunzijMushilProtocolEngine", None)
except Exception:
    MunzijMushilProtocolEngine = None

try:
    cyp_mod = _load_engine("cyp450_interaction_engine", "services/therapeutic/app/engines/cyp450_interaction_engine.py")
    CYP450InteractionEngine = getattr(cyp_mod, "CYP450InteractionEngine", None)
except Exception:
    CYP450InteractionEngine = None

try:
    mufradat_250_mod = _load_engine("mufradat_250_registry", "services/knowledge/app/data/mufradat_250_registry.py")
    get_all_mufradat_250 = getattr(mufradat_250_mod, "get_all_mufradat_250", None)
    get_mufrad_by_id = getattr(mufradat_250_mod, "get_mufrad_by_id", None)
    get_canonical_groups_registry = getattr(mufradat_250_mod, "get_canonical_groups_registry", None)
    get_high_risk_28_registry = getattr(mufradat_250_mod, "get_high_risk_28_registry", None)
    is_high_risk_blocked = getattr(mufradat_250_mod, "is_high_risk_blocked", None)
    check_formulation_canonical_conflicts = getattr(mufradat_250_mod, "check_formulation_canonical_conflicts", None)
except Exception:
    get_all_mufradat_250 = None
    get_mufrad_by_id = None
    get_canonical_groups_registry = None
    get_high_risk_28_registry = None
    is_high_risk_blocked = None
    check_formulation_canonical_conflicts = None

try:
    twelve_gate_mod = _load_engine("twelve_gate_tracker_engine", "services/knowledge/app/engines/twelve_gate_tracker_engine.py")
    TwelveGateTrackerEngine = getattr(twelve_gate_mod, "TwelveGateTrackerEngine", None)
except Exception:
    TwelveGateTrackerEngine = None

try:
    badal_mod = _load_engine("badal_e_advia_engine", "services/therapeutic/app/engines/badal_e_advia_engine.py")
    BadalEAdviaEngine = getattr(badal_mod, "BadalEAdviaEngine", None)
except Exception:
    BadalEAdviaEngine = None

try:
    card_gen_mod = _load_engine("mufradat_card_generator", "services/knowledge/app/engines/mufradat_card_generator.py")
    MufradatCardGenerator = getattr(card_gen_mod, "MufradatCardGenerator", None)
except Exception:
    MufradatCardGenerator = None

try:
    gold_batch_mod = _load_engine("mufradat_gold_batch_monographs", "services/knowledge/app/data/mufradat_gold_batch_monographs.py")
    GoldBenchmarkRegistry = getattr(gold_batch_mod, "GoldBenchmarkRegistry", None)
except Exception:
    GoldBenchmarkRegistry = None

try:
    murakkab_mod = _load_engine("validated_murakkab_compiler", "services/therapeutic/app/engines/validated_murakkab_compiler.py")
    ValidatedMurakkabCompiler = getattr(murakkab_mod, "ValidatedMurakkabCompiler", None)
except Exception:
    ValidatedMurakkabCompiler = None

try:
    m250_mod = _load_engine("mufradat_250_monograph_matrix", "services/knowledge/app/data/mufradat_250_monograph_matrix.py")
    Master250MonographMatrix = getattr(m250_mod, "Master250MonographMatrix", None)
except Exception:
    Master250MonographMatrix = None

try:
    signoff_mod = _load_engine("clinical_multisignoff_engine", "services/clinical/app/engines/clinical_multisignoff_engine.py")
    ClinicalMultiSignoffEngine = getattr(signoff_mod, "ClinicalMultiSignoffEngine", None)
except Exception:
    ClinicalMultiSignoffEngine = None

try:
    case_sim_mod = _load_engine("case_simulator_engine", "services/knowledge/app/engines/case_simulator_engine.py")
    CaseSimulatorEngine = getattr(case_sim_mod, "CaseSimulatorEngine", None)
except Exception:
    CaseSimulatorEngine = None

try:
    botanical_atlas_mod = _load_engine("botanical_visual_atlas", "services/knowledge/app/data/botanical_visual_atlas.py")
    get_all_botanical_atlas = getattr(botanical_atlas_mod, "get_all_botanical_atlas", None)
    get_botanical_by_id = getattr(botanical_atlas_mod, "get_botanical_by_id", None)
    BOTANICAL_ATLAS = getattr(botanical_atlas_mod, "BOTANICAL_ATLAS", [])
except Exception:
    get_all_botanical_atlas = None
    get_botanical_by_id = None
    BOTANICAL_ATLAS = []

# ── ZAYVORA Health OS™ vNEXT Knowledge Intelligence & Clinical Governance ───
try:
    vnext_mod = _load_engine("knowledge_intelligence_vnext", "services/knowledge/app/engines/knowledge_intelligence_vnext.py")
    CanonicalDrugRegistry = getattr(vnext_mod, "CanonicalDrugRegistry", None)
    SourceProvenanceEngine = getattr(vnext_mod, "SourceProvenanceEngine", None)
    ClassicalValidationEngine = getattr(vnext_mod, "ClassicalValidationEngine", None)
    PharmacopoeialCrosswalkEngine = getattr(vnext_mod, "PharmacopoeialCrosswalkEngine", None)
    EvidenceEngineV2 = getattr(vnext_mod, "EvidenceEngineV2", None)
    SafetyFirewallV2 = getattr(vnext_mod, "SafetyFirewallV2", None)
    KnowledgeStateMachine = getattr(vnext_mod, "KnowledgeStateMachine", None)
    GroundedHakeemSahabVNext = getattr(vnext_mod, "GroundedHakeemSahabVNext", None)
    OrganAxisReviewEngine = getattr(vnext_mod, "OrganAxisReviewEngine", None)
    MurakkabGovernanceEngine = getattr(vnext_mod, "MurakkabGovernanceEngine", None)
    ReviewerWorkspaceEngine = getattr(vnext_mod, "ReviewerWorkspaceEngine", None)
    PatientSafetyBarrier = getattr(vnext_mod, "PatientSafetyBarrier", None)
    KnowledgeState = getattr(vnext_mod, "KnowledgeState", None)
    AISafetyState = getattr(vnext_mod, "AISafetyState", None)
    ReviewerAction = getattr(vnext_mod, "ReviewerAction", None)
    MurakkabClass = getattr(vnext_mod, "MurakkabClass", None)
    GOLD_BENCHMARK_25_IDS = getattr(vnext_mod, "GOLD_BENCHMARK_25_IDS", [])
except Exception:
    CanonicalDrugRegistry = None
    SourceProvenanceEngine = None
    ClassicalValidationEngine = None
    PharmacopoeialCrosswalkEngine = None
    EvidenceEngineV2 = None
    SafetyFirewallV2 = None
    KnowledgeStateMachine = None
    GroundedHakeemSahabVNext = None
    OrganAxisReviewEngine = None
    MurakkabGovernanceEngine = None
    ReviewerWorkspaceEngine = None
    PatientSafetyBarrier = None
    KnowledgeState = None
    AISafetyState = None
    ReviewerAction = None
    MurakkabClass = None
    GOLD_BENCHMARK_25_IDS = []

try:
    graph_mod = _load_engine("knowledge_graph_traversal_engine", "services/knowledge/app/engines/knowledge_graph_traversal_engine.py")
    get_clinical_knowledge_graph = getattr(graph_mod, "get_clinical_knowledge_graph", None)
except Exception:
    get_clinical_knowledge_graph = None

try:
    continuum_mod = _load_engine("doctor_continuum_orchestrator", "services/clinical/app/engines/doctor_continuum_orchestrator.py")
    DoctorContinuumOrchestrator = getattr(continuum_mod, "DoctorContinuumOrchestrator", None)
except Exception:
    DoctorContinuumOrchestrator = None

try:
    murakkab_intel_mod = _load_engine("murakkab_intelligence_engine", "services/therapeutic/app/engines/murakkab_intelligence_engine.py")
    MurakkabIntelligenceEngine = getattr(murakkab_intel_mod, "MurakkabIntelligenceEngine", None)
    MurakkabCategory = getattr(murakkab_intel_mod, "MurakkabCategory", None)
    IngredientRole = getattr(murakkab_intel_mod, "IngredientRole", None)
    FormulaIngredient = getattr(murakkab_intel_mod, "FormulaIngredient", None)
except Exception:
    MurakkabIntelligenceEngine = None
    MurakkabCategory = None
    IngredientRole = None
    FormulaIngredient = None

try:
    pharmacy_mod = _load_engine("closed_loop_pharmacy_engine", "services/therapeutic/app/engines/closed_loop_pharmacy_engine.py")
    ClosedLoopPharmacyEngine = getattr(pharmacy_mod, "ClosedLoopPharmacyEngine", None)
    BatchStage = getattr(pharmacy_mod, "BatchStage", None)
    InventoryLot = getattr(pharmacy_mod, "InventoryLot", None)
except Exception:
    ClosedLoopPharmacyEngine = None
    BatchStage = None
    InventoryLot = None

try:
    outcome_intel_mod = _load_engine("outcome_intelligence_engine", "services/clinical/app/engines/outcome_intelligence_engine.py")
    OutcomeIntelligenceEngine = getattr(outcome_intel_mod, "OutcomeIntelligenceEngine", None)
    BiomarkerObservation = getattr(outcome_intel_mod, "BiomarkerObservation", None)
    ClassicalOutcome = getattr(outcome_intel_mod, "ClassicalOutcome", None)
except Exception:
    OutcomeIntelligenceEngine = None
    BiomarkerObservation = None
    ClassicalOutcome = None

try:
    safety_pv_mod = _load_engine("safety_intelligence_pharmacovigilance", "services/therapeutic/app/engines/safety_intelligence_pharmacovigilance.py")
    SafetyIntelligenceEngine = getattr(safety_pv_mod, "SafetyIntelligenceEngine", None)
    ADRSeverity = getattr(safety_pv_mod, "ADRSeverity", None)
    WHOUmcCausality = getattr(safety_pv_mod, "WHOUmcCausality", None)
except Exception:
    SafetyIntelligenceEngine = None
    ADRSeverity = None
    WHOUmcCausality = None

try:
    who_smart_mod = _load_engine("who_smart_dak_engine", "services/knowledge/app/core/who_smart_dak_engine.py")
    WHOSmartDAKEngine = getattr(who_smart_mod, "WHOSmartDAKEngine", None)
except Exception:
    WHOSmartDAKEngine = None

try:
    closed_loop_mod = _load_engine("closed_loop_learning_engine", "services/clinical/app/engines/closed_loop_learning_engine.py")
    ClosedLoopLearningEngine = getattr(closed_loop_mod, "ClosedLoopLearningEngine", None)
except Exception:
    ClosedLoopLearningEngine = None

try:
    continuum_orch_mod = _load_engine("clinical_intelligence_core_orchestrator", "services/clinical/app/engines/clinical_intelligence_core_orchestrator.py")
    ClinicalIntelligenceCoreOrchestrator = getattr(continuum_orch_mod, "ClinicalIntelligenceCoreOrchestrator", None)
    ClinicalContinuumRequest = getattr(continuum_orch_mod, "ClinicalContinuumRequest", None)
except Exception:
    ClinicalIntelligenceCoreOrchestrator = None
    ClinicalContinuumRequest = None

try:
    abdm_interop_mod = _load_engine("abdm_fhir_continuum_orchestrator", "services/clinical/app/interop/abdm_fhir_continuum_orchestrator.py")
    ABDMFHIRContinuumOrchestrator = getattr(abdm_interop_mod, "ABDMFHIRContinuumOrchestrator", None)
except Exception:
    ABDMFHIRContinuumOrchestrator = None

try:
    federation_mod = _load_engine("multi_clinic_federation_engine", "services/clinical/app/engines/multi_clinic_federation_engine.py")
    MultiClinicFederationEngine = getattr(federation_mod, "MultiClinicFederationEngine", None)
except Exception:
    MultiClinicFederationEngine = None

try:
    pop_health_mod = _load_engine("population_health_engine", "services/clinical/app/engines/population_health_engine.py")
    PopulationHealthEngine = getattr(pop_health_mod, "PopulationHealthEngine", None)
    CanonicalSeason = getattr(pop_health_mod, "CanonicalSeason", None)
except Exception:
    PopulationHealthEngine = None
    CanonicalSeason = None

try:
    precision_mod = _load_engine("precision_patient_model", "services/clinical/app/engines/precision_patient_model.py")
    PrecisionPatientModel = getattr(precision_mod, "PrecisionPatientModel", None)
except Exception:
    PrecisionPatientModel = None

try:
    pheno_mod = _load_engine("phenotype_and_response_engine", "services/clinical/app/engines/phenotype_and_response_engine.py")
    PhenotypeAndResponseEngine = getattr(pheno_mod, "PhenotypeAndResponseEngine", None)
    ResponseClassificationTier = getattr(pheno_mod, "ResponseClassificationTier", None)
except Exception:
    PhenotypeAndResponseEngine = None
    ResponseClassificationTier = None

try:
    compiler_mod = _load_engine("knowledge_compiler", "services/knowledge/app/core/knowledge_compiler.py")
    KnowledgeCompiler = getattr(compiler_mod, "KnowledgeCompiler", None)
    global_knowledge_compiler = KnowledgeCompiler() if KnowledgeCompiler else None
except Exception:
    KnowledgeCompiler = None
    global_knowledge_compiler = None

try:
    monitoring_mod = _load_engine("continuous_monitoring_engine", "services/clinical/app/engines/continuous_monitoring_engine.py")
    ContinuousMonitoringEngine = getattr(monitoring_mod, "ContinuousMonitoringEngine", None)
    global_monitoring_engine = ContinuousMonitoringEngine() if ContinuousMonitoringEngine else None
except Exception:
    ContinuousMonitoringEngine = None
    global_monitoring_engine = None

try:
    n1_mod = _load_engine("n_of_1_evidence_engine", "services/clinical/app/engines/n_of_1_evidence_engine.py")
    NOf1EvidenceEngine = getattr(n1_mod, "NOf1EvidenceEngine", None)
    LongitudinalObservation = getattr(n1_mod, "LongitudinalObservation", None)
except Exception:
    NOf1EvidenceEngine = None
    LongitudinalObservation = None

try:
    ct_mod = _load_engine("clinical_trial_os_engine", "services/clinical/app/engines/clinical_trial_os_engine.py")
    ClinicalTrialOSEngine = getattr(ct_mod, "ClinicalTrialOSEngine", None)
    TrialPhase = getattr(ct_mod, "TrialPhase", None)
    BlindingType = getattr(ct_mod, "BlindingType", None)
    TreatmentArm = getattr(ct_mod, "TreatmentArm", None)
    eDCCaseReportForm = getattr(ct_mod, "eDCCaseReportForm", None)
except Exception:
    ClinicalTrialOSEngine = None
    TrialPhase = None
    BlindingType = None
    TreatmentArm = None
    eDCCaseReportForm = None

try:
    fl_mod = _load_engine("federated_learning_engine", "services/clinical/app/engines/federated_learning_engine.py")
    FederatedLearningEngine = getattr(fl_mod, "FederatedLearningEngine", None)
except Exception:
    FederatedLearningEngine = None

try:
    dt_mod = _load_engine("digital_twin_simulation_engine", "services/clinical/app/engines/digital_twin_simulation_engine.py")
    DigitalTwinSimulationEngine = getattr(dt_mod, "DigitalTwinSimulationEngine", None)
    SimulationConfig = getattr(dt_mod, "SimulationConfig", None)
except Exception:
    DigitalTwinSimulationEngine = None
    SimulationConfig = None

try:
    gl_mod = _load_engine("global_localization_engine", "services/knowledge/app/core/global_localization_engine.py")
    GlobalLocalizationEngine = getattr(gl_mod, "GlobalLocalizationEngine", None)
    RegulatoryJurisdiction = getattr(gl_mod, "RegulatoryJurisdiction", None)
except Exception:
    GlobalLocalizationEngine = None
    RegulatoryJurisdiction = None

try:
    pln_mod = _load_engine("population_learning_network", "services/clinical/app/engines/population_learning_network.py")
    PopulationLearningNetworkEngine = getattr(pln_mod, "PopulationLearningNetworkEngine", None)
    MacroWeatherTelemetry = getattr(pln_mod, "MacroWeatherTelemetry", None)
except Exception:
    PopulationLearningNetworkEngine = None
    MacroWeatherTelemetry = None

# ── 10-Service Master Healthcare OS Engines ──────────────────────────────────
try:
    task_eng_mod = _load_engine("universal_task_engine", "services/clinical/app/engines/universal_task_engine.py")
    UniversalTaskEngine = getattr(task_eng_mod, "UniversalTaskEngine", None)
    if UniversalTaskEngine:
        UniversalTaskEngine.seed_initial_clinical_tasks()
except Exception:
    UniversalTaskEngine = None

try:
    enc_os_mod = _load_engine("encounter_os_engine", "services/clinical/app/engines/encounter_os_engine.py")
    EncounterOSEngine = getattr(enc_os_mod, "EncounterOSEngine", None)
except Exception:
    EncounterOSEngine = None

try:
    p360_mod = _load_engine("patient_360_master", "services/clinical/app/engines/patient_360_master.py")
    Patient360Master = getattr(p360_mod, "Patient360Master", None)
except Exception:
    Patient360Master = None

try:
    cp_os_mod = _load_engine("care_plan_os_engine", "services/clinical/app/engines/care_plan_os_engine.py")
    CarePlanOSEngine = getattr(cp_os_mod, "CarePlanOSEngine", None)
except Exception:
    CarePlanOSEngine = None

try:
    canon_term_mod = _load_engine("canonical_terminology_service", "services/knowledge/app/core/canonical_terminology_service.py")
    CanonicalTerminologyService = getattr(canon_term_mod, "CanonicalTerminologyService", None)
except Exception:
    CanonicalTerminologyService = None

try:
    apt_os_mod = _load_engine("appointment_lifecycle_os", "services/clinical/app/engines/appointment_lifecycle_os.py")
    AppointmentLifecycleOS = getattr(apt_os_mod, "AppointmentLifecycleOS", None)
except Exception:
    AppointmentLifecycleOS = None

try:
    lab_os_mod = _load_engine("lab_diagnostics_os", "services/clinical/app/engines/lab_diagnostics_os.py")
    LabDiagnosticsOS = getattr(lab_os_mod, "LabDiagnosticsOS", None)
except Exception:
    LabDiagnosticsOS = None

try:
    ev_os_mod = _load_engine("evidence_provenance_engine", "services/knowledge/app/core/evidence_provenance_engine.py")
    EvidenceProvenanceEngine = getattr(ev_os_mod, "EvidenceProvenanceEngine", None)
except Exception:
    EvidenceProvenanceEngine = None


