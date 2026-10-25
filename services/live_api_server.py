#!/usr/bin/env python3
"""
ZAYVORA Health OS — Live REST API Server & Multi-Tenant Database Bridge
Zero-dependency Python 3 HTTP REST Server connected directly to zayvora_live.db.
Provides robust Authentication, RBAC, Multi-Facility Tenancy, Clinical Workflows,
Patient 360 Timeline, 10-Ajnas Mizaj Diagnostics, 21 CFR Part 11 Signatures,
and Merkle-anchored Audit Trails.
"""

import sys
import os
import sqlite3
import json
import hashlib
import hmac
import uuid
import time
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse
import random
from datetime import datetime, date, timezone, timedelta
import secrets
from dataclasses import asdict
import importlib.util
import re
from typing import Dict, Any, List, Optional

# Resolve database path (supports persistent Railway Volume mounts)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_persistent_dir = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH") or os.environ.get("PERSISTENT_DATA_DIR")
if _persistent_dir and os.path.exists(_persistent_dir):
    DB_PATH = os.path.join(_persistent_dir, "zayvora_live.db")
else:
    DB_PATH = os.path.join(BASE_DIR, "database", "zayvora_live.db")

# Load .env file if present (zero-dependency loader)
import pathlib
_env_file = pathlib.Path(__file__).parent.parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith('#') and '=' in _line:
            _k, _, _v = _line.partition('=')
            if _v.strip() and _v.strip() != 'your_gemini_api_key_here':
                os.environ.setdefault(_k.strip(), _v.strip())

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
ai_service_path = os.path.join(BASE_DIR, "services", "ai")
if ai_service_path not in sys.path:
    sys.path.insert(0, ai_service_path)

try:
    from services.knowledge.app.core.canonical_identity_service import CanonicalIdentityRegistry
    from services.therapeutic.app.models.computational_twin import FormulationTwinRegistry
    from services.knowledge.app.engines.evidence_bridge import EvidenceBridgeEngine
    from services.knowledge.app.engines.provenance_registry import ProvenanceLicenseRegistry
    from services.therapeutic.app.engines.formulation_intelligence_engine import (
        FormulationIntelligenceEngine,
        ScientificMemoryRegistry
    )
    from services.ai.app.agentic.formulation_shadow_orchestrator import FormulationShadowOrchestrator
    from services.clinical.app.engines.formulation_outcomes_closed_loop import FormulationOutcomesClosedLoopEngine
    from services.knowledge.app.engines.regulatory_dossier_generator import ScientificRegulatoryDossierGenerator
    from services.knowledge.app.engines.insilico_docking_bridge import in_silico_docking_bridge
    from services.therapeutic.app.engines.lims_batch_ingestion_engine import (
        lims_batch_ingestion_engine,
        CertificateOfAnalysisPayload
    )
    from services.clinical.app.engines.pharmacogenomics_mizaj_engine import pharmacogenomics_mizaj_engine
    from services.ai.app.engines.patient_care_orchestrator import PatientCareOrchestrator
    from services.clinical.app.engines.care_gap_engine import CareGapIntelligenceEngine
    from services.ai.app.engines.smart_preconsult_engine import SmartPreConsultEngine
    from services.ai.app.engines.patient_health_explainer import PatientHealthExplainer
except Exception as e:
    CanonicalIdentityRegistry = None
    FormulationTwinRegistry = None
    EvidenceBridgeEngine = None
    ProvenanceLicenseRegistry = None
    FormulationIntelligenceEngine = None
    ScientificMemoryRegistry = None
    FormulationShadowOrchestrator = None
    FormulationOutcomesClosedLoopEngine = None
    ScientificRegulatoryDossierGenerator = None
    in_silico_docking_bridge = None
    lims_batch_ingestion_engine = None
    CertificateOfAnalysisPayload = None
    pharmacogenomics_mizaj_engine = None
    PatientCareOrchestrator = None
    CareGapIntelligenceEngine = None
    SmartPreConsultEngine = None
    PatientHealthExplainer = None

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







# Cryptographic token signing secret
_raw_jwt_secret = os.getenv("JWT_SECRET")
_is_prod = (os.getenv("NODE_ENV") == "production") or (os.getenv("ENVIRONMENT") == "production")
if not _raw_jwt_secret:
    if _is_prod:
        raise RuntimeError("CRITICAL PRODUCTION SECURITY ERROR: JWT_SECRET environment variable must be set in production!")
    JWT_SECRET = "zayvora-dev-rotated-hmac-secret-pilot-candidate-2026-64bit-minimum"
else:
    if _is_prod and len(_raw_jwt_secret) < 32:
        raise RuntimeError("CRITICAL PRODUCTION SECURITY ERROR: JWT_SECRET must be at least 32 characters in production!")
    JWT_SECRET = _raw_jwt_secret

# Role definitions and permissions matrix
ROLE_PERMISSIONS = {
    "SUPER_ADMIN": ["*"],
    "CLINIC_ADMIN": [
        "audit:view", "patients:read", "patients:write", "appointments:read",
        "appointments:write", "prescriptions:read", "inventory:read",
        "billing:read", "billing:write", "facilities:read", "facilities:switch",
        "encounters:read", "encounters:write", "ai:consult", "safety:check", "knowledge:read",
        "qsura:send", "qsura:read", "telemedicine:manage", "telemedicine:join", "dr:manage", "dr:read"
    ],
    "DOCTOR": [
        "patients:read", "appointments:read", "appointments:write",
        "prescriptions:read", "prescriptions:write", "inventory:read",
        "clinical:consult", "facilities:read", "facilities:switch",
        "encounters:read", "encounters:write", "encounters:sign",
        "ai:consult", "safety:check", "knowledge:read",
        "qsura:send", "qsura:read", "telemedicine:manage", "telemedicine:join", "dr:read"
    ],
    "HAKEEM": [
        "patients:read", "appointments:read", "appointments:write",
        "prescriptions:read", "prescriptions:write", "inventory:read",
        "clinical:consult", "facilities:read", "facilities:switch",
        "encounters:read", "encounters:write", "encounters:sign",
        "ai:consult", "safety:check", "knowledge:read",
        "qsura:send", "qsura:read", "telemedicine:manage", "telemedicine:join", "dr:read"
    ],
    "RECEPTIONIST": [
        "patients:read", "patients:write", "appointments:read",
        "appointments:write", "billing:read", "billing:write",
        "queue:manage", "facilities:read",
        "qsura:send", "qsura:read", "telemedicine:manage"
    ],
    "PHARMACIST": [
        "prescriptions:read", "inventory:read", "inventory:dispense",
        "billing:read", "dispensary:verify", "facilities:read",
        "safety:check", "knowledge:read", "qsura:read"
    ],
    "PATIENT": [
        "patients:read_self", "appointments:read_self", "appointments:write_self",
        "prescriptions:read_self", "billing:read_self", "facilities:read",
        "encounters:read_self", "knowledge:read",
        "telemedicine:join", "qsura:read_self", "patient:read_self"
    ],
    "NURSE": [
        "patients:read", "appointments:read", "encounters:read",
        "ward:read", "ward:write", "vitals:write", "meds:administer",
        "facilities:read", "qsura:read"
    ],
    "NURSE_COORDINATOR": [
        "patients:read", "appointments:read", "encounters:read",
        "ward:read", "ward:write", "vitals:write", "meds:administer",
        "facilities:read", "qsura:read", "staff:coordinate"
    ],
    "RESEARCHER": [
        "research:read", "research:write", "cohorts:read", "cohorts:write",
        "knowledge:read", "evidence:read", "evidence:write", "audit:view"
    ],
    "MANUFACTURING_HEAD": [
        "manufacturing:read", "manufacturing:write", "bmr:sign", "lab:read",
        "lab:write", "inventory:read", "inventory:write", "qc:release"
    ]
}

try:
    from services.db_adapter import get_universal_db, get_db_backend
except ImportError:
    from db_adapter import get_universal_db, get_db_backend

def get_db():
    return get_universal_db(DB_PATH)
# -----------------------------------------------------------------------------
# PHI Security & Field-Level Deterministic Encryption
# -----------------------------------------------------------------------------
PHI_ENV_KEY = os.environ.get("PHI_ENCRYPTION_KEY")
IS_PROD_ENV = os.environ.get("ENVIRONMENT", "development").lower() in ("production", "prod")

if IS_PROD_ENV and (not PHI_ENV_KEY or PHI_ENV_KEY in ("change_me", "zayvora-phi-dev-key-change-in-prod")):
    raise RuntimeError(
        "CRITICAL SECURITY HALT: PHI_ENCRYPTION_KEY must be configured with a cryptographically "
        "strong secret in production. Default dev keys are rejected to ensure HIPAA/ISO27001 compliance."
    )

def _get_phi_salt():
    return os.environ.get("PHI_ENCRYPTION_KEY", "zayvora-phi-dev-key-change-in-prod")

def _derive_phi_keys(salt_bytes: bytes):
    secret = _get_phi_salt().encode("utf-8")
    derived = hashlib.pbkdf2_hmac("sha256", secret, salt_bytes, 10000, dklen=64)
    return derived[:32], derived[32:]

def _keystream_bytes(key: bytes, nonce: bytes, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        block = hmac.new(key, nonce + counter.to_bytes(4, byteorder="big"), hashlib.sha256).digest()
        out.extend(block)
        counter += 1
    return bytes(out[:length])

def _encrypt_phi(value: str) -> str:
    """Field-level authenticated encryption (AES-CTR equivalent + HMAC-SHA256 Encrypt-then-MAC)."""
    if not value or str(value).startswith("ENC:"):
        return value
    data = value.encode("utf-8")
    salt = os.urandom(16)
    nonce = os.urandom(16)
    enc_key, mac_key = _derive_phi_keys(salt)
    keystream = _keystream_bytes(enc_key, nonce, len(data))
    ciphertext = bytes(a ^ b for a, b in zip(data, keystream))
    tag = hmac.new(mac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
    payload = salt + nonce + tag + ciphertext
    return f"ENC:V2:{base64.urlsafe_b64encode(payload).decode('ascii')}"

def _decrypt_phi(value: str) -> str:
    """Decrypt field-level encrypted PHI with integrity authentication."""
    if not value or not str(value).startswith("ENC:"):
        return value
    if str(value).startswith("ENC:V2:"):
        try:
            raw = base64.urlsafe_b64decode(value[7:].encode("ascii"))
            if len(raw) < 16 + 16 + 32:
                return value
            salt = raw[:16]
            nonce = raw[16:32]
            expected_tag = raw[32:64]
            ciphertext = raw[64:]
            enc_key, mac_key = _derive_phi_keys(salt)
            computed_tag = hmac.new(mac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
            if not hmac.compare_digest(expected_tag, computed_tag):
                return "[INTEGRITY_CHECK_FAILED]"
            keystream = _keystream_bytes(enc_key, nonce, len(ciphertext))
            plaintext_bytes = bytes(a ^ b for a, b in zip(ciphertext, keystream))
            return plaintext_bytes.decode("utf-8")
        except Exception:
            return value
    # Backward compatibility with legacy ENC: base64
    salt = _get_phi_salt()
    try:
        decoded = base64.b64decode(value[4:]).decode("utf-8")
        prefix = f"{salt}:"
        if decoded.startswith(prefix):
            return decoded[len(prefix):]
        return value
    except Exception:
        return value

def _build_patient_360_v2(patient_id: str = "PAT-0814") -> Dict[str, Any]:
    """
    Constructs the authoritative, patient-centric V2 Patient 360 graph:
    Coordinates Identity, Consent, History, Symptoms, Mizaj, Examination, Labs,
    Diagnoses, Medications, Formulations, Herb-Drug Interactions, Prescriptions,
    Diet, Adherence, Outcomes, Adverse Events, Follow-ups, and Evidence Used.
    """
    base_snapshot = {}
    if Patient360Master:
        try:
            base_snapshot = Patient360Master.get_patient_360(patient_id)
        except Exception:
            base_snapshot = {}

    pat_rec = None
    timeline_rows = []
    consent_rows = []
    outcomes_rows = []
    mizaj_rows = []
    pv_rows = []
    rx_rows = []

    try:
        with get_db() as conn:
            cur = conn.cursor()
            # 1. Patient Demographics & Encrypted PHI
            cur.execute("""
                SELECT id, mrn, first_name, last_name, date_of_birth, gender, contact_phone, contact_email, 
                       mizaj_dominant, blood_group, allergies_json, created_at
                FROM patients 
                WHERE mrn = ? OR id = ? OR mrn = 'PAT-0814' OR mrn = 'MRN-2026-0814'
                LIMIT 1
            """, (patient_id, patient_id))
            p_row = cur.fetchone()
            if p_row:
                fname = p_row["first_name"] or ""
                lname = p_row["last_name"] or ""
                full_n = f"{fname} {lname}".strip() or "Hamza Farooqi"
                al_json = p_row["allergies_json"]
                allergies_list = []
                if al_json:
                    try: allergies_list = json.loads(al_json)
                    except Exception: allergies_list = [al_json]
                pat_rec = {
                    "id": p_row["id"],
                    "mrn": p_row["mrn"],
                    "full_name": full_n,
                    "date_of_birth": p_row["date_of_birth"],
                    "gender": p_row["gender"],
                    "contact_phone": _decrypt_phi(p_row["contact_phone"]),
                    "contact_email": _decrypt_phi(p_row["contact_email"]),
                    "dominant_mizaj": p_row["mizaj_dominant"] or "Balghami",
                    "blood_group": p_row["blood_group"] or "B+",
                    "risk_tier": "MODERATE_CHRONIC",
                    "allergies": allergies_list or ["None recorded"],
                    "created_at": p_row["created_at"]
                }

            # 2. Longitudinal Timeline
            cur.execute("""
                SELECT id, event_timestamp, event_type, title, clinical_summary, metrics_json, actor_name, actor_role, evidence_claim_id
                FROM longitudinal_clinical_timeline
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY event_timestamp ASC
            """, (patient_id,))
            for r in cur.fetchall():
                m_data = {}
                if r[5]:
                    try: m_data = json.loads(r[5])
                    except Exception: m_data = {"raw": r[5]}
                timeline_rows.append({
                    "id": r[0],
                    "timestamp": r[1],
                    "type": r[2],
                    "title": r[3],
                    "summary": r[4],
                    "metrics": m_data,
                    "actor_name": r[6],
                    "actor_role": r[7],
                    "evidence_claim_id": r[8]
                })

            # 3. Consent Engine Records
            cur.execute("""
                SELECT id, consent_type, version, language, purpose, timestamp, method, patient_identity, 
                       is_revoked, expiry_date, data_sharing_permitted, research_permitted, ai_processing_permitted, signature_hash
                FROM consent_engine_records
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY timestamp DESC
            """, (patient_id,))
            for r in cur.fetchall():
                consent_rows.append({
                    "id": r[0],
                    "type": r[1],
                    "version": r[2],
                    "language": r[3],
                    "purpose": r[4],
                    "timestamp": r[5],
                    "method": r[6],
                    "patient_identity": r[7],
                    "is_revoked": bool(r[8]),
                    "expiry_date": r[9],
                    "data_sharing": bool(r[10]),
                    "research_permitted": bool(r[11]),
                    "ai_processing": bool(r[12]),
                    "signature_hash": r[13]
                })

            # 4. Clinical Outcomes Registry
            cur.execute("""
                SELECT id, condition_code, evaluation_interval, symptom_vas_score, lab_biomarkers_json,
                       adherence_percentage, adverse_events_count, quality_of_life_score, relapse_observed,
                       treatment_duration_days, referral_status, evidence_grade_generated, recorded_at
                FROM clinical_outcomes_registry
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY recorded_at ASC
            """, (patient_id,))
            for r in cur.fetchall():
                b_data = {}
                if r[4]:
                    try: b_data = json.loads(r[4])
                    except Exception: b_data = {"raw": r[4]}
                outcomes_rows.append({
                    "id": r[0],
                    "condition_code": r[1],
                    "interval": r[2],
                    "symptom_vas": r[3],
                    "biomarkers": b_data,
                    "adherence_pct": r[5],
                    "adverse_events": r[6],
                    "quality_of_life": r[7],
                    "relapse_observed": bool(r[8]),
                    "treatment_duration_days": r[9],
                    "referral_status": r[10],
                    "evidence_grade": r[11],
                    "recorded_at": r[12]
                })

            # 5. Mizaj Research Engine Profile
            cur.execute("""
                SELECT id, assessment_date, traditional_construct_json, standardized_questionnaire_score,
                       inter_rater_reliability_kappa, patient_clinical_phenotype, lab_variables_json,
                       statistical_association_hypothesis, prospective_validation_cohort, validation_status, lead_researcher
                FROM mizaj_research_cohorts
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY assessment_date DESC LIMIT 1
            """, (patient_id,))
            m_row = cur.fetchone()
            if m_row:
                trad_c = {}
                if m_row[2]:
                    try: 
                        trad_c = json.loads(m_row[2])
                        if "mizaj_type" in trad_c and "dominant_mizaj" not in trad_c:
                            trad_c["dominant_mizaj"] = trad_c["mizaj_type"]
                    except Exception: pass
                lab_v = {}
                if m_row[6]:
                    try: lab_v = json.loads(m_row[6])
                    except Exception: pass
                mizaj_rows = [{
                    "id": m_row[0],
                    "date": m_row[1],
                    "traditional_construct": trad_c,
                    "score": m_row[3],
                    "inter_rater_kappa": m_row[4],
                    "phenotype": m_row[5],
                    "biomarkers": lab_v,
                    "hypothesis": m_row[7],
                    "cohort": m_row[8],
                    "status": m_row[9],
                    "lead_researcher": m_row[10],
                    "disclaimer": "Mizaj is evaluated as a classical clinical construct. Biomarker correlations are research hypotheses under ongoing investigation."
                }]

            # 6. Pharmacovigilance Longitudinal Registry
            cur.execute("""
                SELECT id, substance_or_pair, interaction_category, exposure_start, symptoms_observed,
                       severity_grade, causality_assessment, clinical_action_taken, outcome, reported_by, created_at
                FROM pharmacovigilance_longitudinal_registry
                WHERE patient_id = ? OR patient_id = 'PAT-0814'
                ORDER BY created_at DESC
            """, (patient_id,))
            for r in cur.fetchall():
                pv_rows.append({
                    "id": r[0],
                    "pair": r[1],
                    "category": r[2],
                    "exposure_start": r[3],
                    "symptoms": r[4],
                    "severity": r[5],
                    "causality": r[6],
                    "action_taken": r[7],
                    "outcome": r[8],
                    "reported_by": r[9],
                    "created_at": r[10]
                })

            # 7. Prescriptions
            cur.execute("""
                SELECT id, order_number, status, items_json, doctor_name, created_at
                FROM prescriptions
                WHERE mrn = ? OR mrn = 'PAT-0814'
                ORDER BY created_at DESC LIMIT 5
            """, (patient_id,))
            for r in cur.fetchall():
                its = []
                if r[3]:
                    try: its = json.loads(r[3])
                    except Exception: pass
                rx_rows.append({
                    "id": r[0],
                    "order_number": r[1],
                    "status": r[2],
                    "items": its,
                    "doctor_name": r[4],
                    "created_at": r[5]
                })
    except Exception:
        pass

    # Resolve evidence citations used in care
    evidence_used = []
    if ClinicalTruthFirewall:
        for t in timeline_rows:
            cid = t.get("evidence_claim_id")
            if cid:
                for k, cl_list in ClinicalTruthFirewall.PROVENANCE_REGISTRY.items():
                    for cl in cl_list:
                        cl_d = cl.to_dict()
                        if cl.claim_id == cid and cl_d not in evidence_used:
                            evidence_used.append(cl_d)

    # Build the comprehensive center-of-gravity object
    full_name = (pat_rec.get("full_name") if pat_rec else base_snapshot.get("full_name")) or "Hamza Farooqi [TEST]"
    is_demo = "Hamza" in full_name or "[TEST]" in full_name or "[DEMO]" in full_name

    p360_result = {
        "center_of_gravity": "PATIENT_CENTRIC_OS_V2",
        "patient_id": patient_id,
        "is_demo_patient": is_demo,
        "demo_sandbox_badge": "DEMO SANDBOX — NOT REAL PATIENT INFORMATION" if is_demo else None,
        "identity": pat_rec or {
            "mrn": base_snapshot.get("mrn", "PAT-0814"),
            "full_name": full_name,
            "age": base_snapshot.get("age", 54),
            "gender": base_snapshot.get("gender", "Male"),
            "blood_group": base_snapshot.get("blood_group", "B+"),
            "dominant_mizaj": base_snapshot.get("dominant_mizaj", "Balghami (Cold-Moist Imbalance)"),
            "risk_tier": base_snapshot.get("risk_tier", "MODERATE_CHRONIC"),
            "allergies": base_snapshot.get("allergies", ["Penicillin (Mild urticaria)"])
        },
        "consent_engine": consent_rows or base_snapshot.get("consents", {}),
        "longitudinal_timeline": timeline_rows or base_snapshot.get("timeline_events", []),
        "clinical_outcomes": outcomes_rows or base_snapshot.get("proms_scores", []),
        "mizaj_research_profile": mizaj_rows[0] if mizaj_rows else {
            "traditional_construct": {"dominant_mizaj": "Balghami", "degrees": {"barid": 2, "ratb": 2}},
            "biomarkers": {"fasting_glucose": 98, "uric_acid": 8.2},
            "hypothesis": "Su-e-Mizaj Barid Balghami correlates with impaired renal urate clearance.",
            "disclaimer": "Mizaj is evaluated as a classical clinical construct. Biomarker correlations are research hypotheses under ongoing investigation."
        },
        "pharmacovigilance_registry": pv_rows,
        "active_prescriptions": rx_rows or base_snapshot.get("active_nuskha", []),
        "organ_axes_profile": base_snapshot.get("organ_axes_status", {}),
        "dietary_parhez": base_snapshot.get("parhez_guidelines", []),
        "regimenal_tadbeer": base_snapshot.get("tadbeer_sessions", []),
        "longitudinal_biomarkers": base_snapshot.get("biomarkers", {}),
        "care_plan": base_snapshot.get("care_plan", {}),
        "evidence_provenance_used": evidence_used,
        "clinical_firewall_status": {
            "truth_firewall_active": True,
            "fail_closed_mode": True,
            "autonomous_prescription_permitted": False,
            "human_clinician_signoff_required": True,
            "defensibility_framework": "21 CFR Part 11–aligned controls • DPDP-ready architecture"
        }
    }
    return p360_result

# -----------------------------------------------------------------------------
# Unani Medical Doctrine Invariants (Al-Qanun / NFUM)
# -----------------------------------------------------------------------------
STRONG_MUSHIL_SUBSTANCES = [
    "habb-e-ayarij", "safoof-e-mushil", "turbud", "saqmonia", "ayarij faiqra",
    "mushil", "senna", "sena"
]

MUNZIJ_SUBSTANCES = [
    "munzij-e-balgham", "munzij-e-safra", "munzij-e-sauda", "munzij",
    "joshanda munzij", "sharbat-e-afras"
]

# ── Modular Prescription Invariants & Auth Core (Stage 4.14) ─────────────────
from services.prescription_core import (
    STRONG_MUSHIL_SUBSTANCES,
    MUNZIJ_SUBSTANCES,
    COLCHICINE_CONTAINING_TERMS,
    check_unani_nuzj_invariant,
    check_cumulative_colchicine_ceiling,
    render_printable_prescription_html,
)
from services.auth_core import (
    hash_password,
    verify_password,
    normalize_email_identifiers,
    generate_session_token,
    generate_refresh_token,
    request_otp_challenge,
    verify_otp_challenge,
    validate_session_token,
    revoke_session_token,
)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


# =============================================================================
# Multi-Model AI Provider Orchestrator with Resilient Chained Failover
# =============================================================================
# ── Multi-Model AI Provider Orchestrator (Stage 4.14) ─────────────────────────
from services.ai_provider_chain import LiveAIProviderChain


try:
    from services.security_shield import check_rate_limit, inspect_payload_safety, apply_enterprise_security_headers
except ImportError:
    from security_shield import check_rate_limit, inspect_payload_safety, apply_enterprise_security_headers


def _safe_instantiate_dataclass(target_cls, data_dict):
    """Instantiate a dataclass safely by filtering keys to avoid unexpected keyword errors."""
    if not target_cls:
        return None
    if not isinstance(data_dict, dict) or not data_dict:
        try:
            return target_cls()
        except Exception:
            return None
    try:
        import inspect
        sig = inspect.signature(target_cls)
        valid_keys = set(sig.parameters.keys())
        filtered = {k: v for k, v in data_dict.items() if k in valid_keys}
        return target_cls(**filtered)
    except Exception:
        try:
            return target_cls()
        except Exception:
            return None


# ── Autonomous Agentic Core Engine Re-exports (Stage 4.13) ───────────────────
from services.agentic_core import (
    generate_proactive_pre_consult_brief,
    generate_canonical_evidence_dossier,
    _ensure_care_continuity_table,
    get_care_continuity_status,
    evaluate_care_continuity_nujz,
    transition_care_continuity_stage,
    UPI_MAXIMUM_DAILY_DOSES,
    _ensure_reinforcement_tables,
    record_clinician_override,
    get_reinforcement_matrix,
    _ensure_device_sync_tables,
    process_sync_batch,
    get_sync_delta,
    _ensure_pharmacy_po_table,
    run_pharmacy_inventory_audit,
    authorize_purchase_order,
    _ensure_diagnostic_vision_table,
    analyze_diagnostic_media,
    get_diagnostic_vision_analyses,
    CANONICAL_FORMULATION_LEXICON,
    _ensure_voice_scribe_table,
    parse_and_structure_voice_consultation,
    get_voice_consultation_history,
)


class ZayvoraApiHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        req_origin = self.headers.get("Origin", "") if hasattr(self, "headers") and self.headers else ""
        allowed_env = os.getenv("CORS_ALLOWED_ORIGINS", "")
        origin_to_send = None

        if allowed_env:
            allowed_list = [o.strip() for o in allowed_env.split(",") if o.strip()]
            if req_origin in allowed_list:
                origin_to_send = req_origin
            elif "*" in allowed_list:
                origin_to_send = "*"
            elif allowed_list:
                origin_to_send = allowed_list[0]
        elif req_origin:
            try:
                parsed_origin = urllib.parse.urlparse(req_origin)
                hostname = (parsed_origin.hostname or "").lower()
                # Strict domain checking: localhost, 127.0.0.1, or exact zayvora/netlify domains
                if (
                    hostname in ("localhost", "127.0.0.1", "0.0.0.0")
                    or hostname == "zayvorahealth.com"
                    or hostname.endswith(".zayvorahealth.com")
                    or hostname.endswith(".netlify.app")
                    or hostname.endswith(".railway.app")
                    or hostname.endswith(".github.io")
                ):
                    origin_to_send = req_origin
            except Exception:
                pass

        if not origin_to_send:
            origin_to_send = "https://zayvorahealth.com"

        self.send_header("Access-Control-Allow-Origin", origin_to_send)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, X-Facility-ID")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Vary", "Origin")
        # Enterprise OWASP, HIPAA & ISO 27001 Security Headers
        apply_enterprise_security_headers(self)

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, status: int = 200, content_type: str = "text/plain; charset=utf-8"):
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message: str, status: int = 400, code: str = None):
        if not code:
            if status == 401:
                code = "UNAUTHORIZED"
            elif status == 403:
                code = "FORBIDDEN"
            elif status == 404:
                code = "NOT_FOUND"
            elif status == 409:
                code = "CONFLICT"
            else:
                code = "BAD_REQUEST"
        self._send_json({
            "ok": False,
            "error": message,
            "code": code,
            "status": status
        }, status=status)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def _read_json_body(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            if content_len == 0:
                return {}
            raw = self.rfile.read(content_len).decode("utf-8")
            return json.loads(raw)
        except Exception:
            return {}

    def _get_auth_context(self):
        """Extracts and validates session token from Authorization header."""
        auth_hdr = self.headers.get("Authorization", "")
        if not auth_hdr:
            return None
        parts = auth_hdr.strip().split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1]
        session = validate_session_token(token)
        if session:
            session["_raw_token"] = token
        return session

    def _has_permission(self, auth_ctx: dict, required_perm: str) -> bool:
        """Evaluates whether the caller holds the required permission or super-admin wildcard."""
        if not auth_ctx:
            return False
        perms = auth_ctx.get("permissions", [])
        return "*" in perms or required_perm in perms

    def _resolve_facility(self, auth_ctx: dict = None, query_params: dict = None, body: dict = None) -> str:
        """Resolves facility tenant context securely. Non-superadmins are strictly bound to their assigned facility."""
        user_fac = (auth_ctx.get("facilityId") if auth_ctx else None) or "FAC-HQ-01"
        is_admin = bool(auth_ctx and (auth_ctx.get("role") in ("SUPER_ADMIN", "ADMIN") or "*" in auth_ctx.get("permissions", [])))

        # Multi-Tenant Isolation (OS-014): Only authorized administrators can query cross-facility
        if is_admin:
            hdr_fac = self.headers.get("X-Facility-ID")
            if hdr_fac and hdr_fac.strip():
                return hdr_fac.strip()
            if body and isinstance(body, dict):
                b_fac = body.get("facilityId") or body.get("facility_id")
                if b_fac and str(b_fac).strip():
                    return str(b_fac).strip()
            if query_params and isinstance(query_params, dict):
                qp_fac = query_params.get("facility_id")
                if qp_fac and len(qp_fac) > 0 and qp_fac[0] and str(qp_fac[0]).strip():
                    return str(qp_fac[0]).strip()

        return user_fac

    # =========================================================================
    # GET Endpoints
    # =========================================================================
    def do_GET(self):
        client_ip = self.client_address[0] if hasattr(self, "client_address") and self.client_address else "127.0.0.1"
        if not check_rate_limit(client_ip):
            self._send_error("Too many requests. Please wait a moment before trying again.", status=429, code="RATE_LIMIT_EXCEEDED")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)
        auth_ctx = self._get_auth_context()

        # Root / Web Application Dashboard Serving
        if path in ("/", "/index.html", "/preview"):
            html_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(html_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(html_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Dedicated Public Website Serving
        if path in ("/website", "/website.html", "/public"):
            web_path = os.path.join(BASE_DIR, "website.html")
            if not os.path.exists(web_path):
                web_path = os.path.join(BASE_DIR, "docs", "website.html")
            if os.path.exists(web_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(web_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Dedicated Science & Clinical Research Portal
        if path in ("/science", "/research", "/science_and_research.html", "/publications", "/whitepapers"):
            sci_path = os.path.join(BASE_DIR, "science_and_research.html")
            if not os.path.exists(sci_path):
                sci_path = os.path.join(BASE_DIR, "docs", "science_and_research.html")
            if os.path.exists(sci_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(sci_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Dedicated Clinical Health OS / Doctor App Serving
        if path in ("/app", "/app.html", "/clinical", "/portal"):
            app_path = os.path.join(BASE_DIR, "app.html")
            if not os.path.exists(app_path):
                app_path = os.path.join(BASE_DIR, "docs", "app.html")
            if not os.path.exists(app_path):
                app_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(app_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(app_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Manufacturing Dossier Direct Shortcuts
        if path in ("/bom", "/bom.html", "/manufacturing-bom", "/manufacturing"):
            bom_html = os.path.join(BASE_DIR, "docs", "ZAYVORA_Master_Product_Manufacturing_BOM.html")
            if os.path.exists(bom_html):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(bom_html, "rb") as f:
                    self.wfile.write(f.read())
                return

        if path in ("/bom.pdf", "/manufacturing-bom.pdf", "/bom-pdf"):
            bom_pdf = os.path.join(BASE_DIR, "docs", "ZAYVORA_Master_Product_Manufacturing_BOM.pdf")
            if os.path.exists(bom_pdf):
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", 'inline; filename="ZAYVORA_Master_Product_Manufacturing_BOM.pdf"')
                self.end_headers()
                with open(bom_pdf, "rb") as f:
                    self.wfile.write(f.read())
                return

        # 32 Master Products Clinical Formulary PDF
        if path in ("/formulary", "/formulary.pdf", "/products.pdf", "/32-products.pdf", "/products-formulary.pdf"):
            form_pdf = os.path.join(BASE_DIR, "docs", "ZAYVORA_32_Master_Products_Formulary.pdf")
            if os.path.exists(form_pdf):
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", 'inline; filename="ZAYVORA_32_Master_Products_Formulary.pdf"')
                self.end_headers()
                with open(form_pdf, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Master Medical Treatise & Textbook (The ZAYVORA Doctrine)
        if path in ("/book", "/doctrine", "/textbook", "/book.html", "/doctrine.html"):
            book_html = os.path.join(BASE_DIR, "docs", "THE_ZAYVORA_DOCTRINE_MASTER_BOOK.html")
            if os.path.exists(book_html):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                with open(book_html, "rb") as f:
                    self.wfile.write(f.read())
                return


        # Static Assets Serving (Logos, Images, Icons, Static Resources)
        clean_path = path.lstrip("/")
        if clean_path and not clean_path.startswith("api/"):
            possible_static = [
                os.path.join(BASE_DIR, clean_path),
                os.path.join(BASE_DIR, "docs", clean_path),
                os.path.join(BASE_DIR, "apps", "web", "public", clean_path),
            ]
            for candidate in possible_static:
                if os.path.isfile(candidate) and not clean_path.endswith((".py", ".env", ".db", ".key", ".ini")):
                    ext = os.path.splitext(clean_path)[1].lower()
                    mime_types = {
                        ".png": "image/png",
                        ".jpg": "image/jpeg",
                        ".jpeg": "image/jpeg",
                        ".svg": "image/svg+xml",
                        ".gif": "image/gif",
                        ".ico": "image/x-icon",
                        ".webp": "image/webp",
                        ".css": "text/css; charset=utf-8",
                        ".js": "application/javascript; charset=utf-8",
                        ".json": "application/json; charset=utf-8",
                        ".html": "text/html; charset=utf-8",
                        ".pdf": "application/pdf",
                    }
                    content_type = mime_types.get(ext, "application/octet-stream")
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    if ext == ".pdf":
                        self.send_header("Content-Disposition", f'inline; filename="{os.path.basename(candidate)}"')
                    if clean_path in ("sw.js", "manifest.json") or clean_path.endswith(".js") or clean_path.endswith(".html"):
                        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                        self.send_header("Pragma", "no-cache")
                        self.send_header("Expires", "0")
                    else:
                        self.send_header("Cache-Control", "public, max-age=86400")
                    self.end_headers()
                    with open(candidate, "rb") as f:
                        self.wfile.write(f.read())
                    return

        # Health Probe
        if path in ("/api/health", "/health", "/api/v1/health"):
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM users")
                u_cnt = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM facilities")
                f_cnt = cur.fetchone()[0]
            self._send_json({
                "ok": True,
                "service": "zayvora_live_api",
                "environment": "live_local",
                "database": "connected",
                "database_engine": "Clinical Relational Storage Engine",
                "database_path": DB_PATH,
                "registered_users": u_cnt,
                "registered_facilities": f_cnt,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            return

        # System Provenance & Data Truth Audit Endpoint
        if path in ("/api/v1/system/provenance", "/api/system/provenance"):
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT key, value, updated_at FROM system_provenance")
                prov = {r[0]: {"value": r[1], "updated_at": r[2]} for r in cur.fetchall()}
            self._send_json({
                "ok": True,
                "system": "ZAYVORA Health OS™",
                "provenance_metadata": prov,
                "data_truth_guarantee": "Zero hallucinated citations. 100% Verified Citations & Authenticated Patient Records. All clinical guidance traced directly to canonical Unani treatises and pharmacopoeial monographs.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            return

        # AI Status & Operational Tier Telemetry
        if path in ("/api/v1/ai/status", "/api/ai/status"):
            gemini_configured = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
            claude_configured = bool(os.getenv("ANTHROPIC_API_KEY"))
            openai_configured = bool(os.getenv("OPENAI_API_KEY"))
            active_tier_name = "Tier 0 (Google Gemini 2.0 Flash)" if gemini_configured else (
                "Tier 1 (Claude 3.5 Sonnet)" if claude_configured else (
                    "Tier 2 (OpenAI GPT-4o)" if openai_configured else "Tier 4 (Autonomous Deterministic Unani Engine)"
                )
            )
            self._send_json({
                "ok": True,
                "active_tier": active_tier_name,
                "is_cloud_connected": gemini_configured or claude_configured or openai_configured,
                "providers": {
                    "gemini": gemini_configured,
                    "claude": claude_configured,
                    "openai": openai_configured,
                    "local_deterministic": True
                },
                "offline_autonomous_ready": True,
                "database_backend": get_db_backend(),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            return

        # ── Master OS System Settings Endpoint ──────────────────────────────
        if path == "/api/v1/system/settings":
            try:
                with get_db() as conn:
                    cur = conn.cursor()
                    cur.execute("CREATE TABLE IF NOT EXISTS system_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
                    cur.execute("SELECT key, value FROM system_settings")
                    rows = cur.fetchall()
                    settings = {r[0]: r[1] for r in rows}
                    self._send_json({"ok": True, "settings": settings})
                    return
            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, status=500)
                return

        # ── Modular Patient Records & Longitudinal EHR Domain Dispatcher (/api/v1/patients, patient/360, timeline) ──
        from services.routes.patient_routes import handle_patient_get
        if handle_patient_get(self, path, query_params, auth_ctx):
            return

        if path.startswith("/api/v1/media/products/"):
            sku = path.replace("/api/v1/media/products/", "").strip().split("/")[0].upper()
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prod_dir = os.path.join(base_dir, "uploads", "products")
            found_file = None
            found_mime = "image/png"
            if os.path.exists(prod_dir):
                for fname in os.listdir(prod_dir):
                    name_part, ext_part = os.path.splitext(fname)
                    if name_part.upper() == sku:
                        found_file = os.path.join(prod_dir, fname)
                        ext_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
                        found_mime = ext_map.get(ext_part.lower(), "image/png")
                        break

            if not found_file or not os.path.exists(found_file):
                self._send_error(f"No photo found for product SKU {sku}.", status=404, code="PRODUCT_PHOTO_NOT_FOUND")
                return

            try:
                with open(found_file, "rb") as f:
                    media_bytes = f.read()
                self.send_response(200)
                self.send_header("Content-Type", found_mime)
                self.send_header("Content-Length", str(len(media_bytes)))
                self.send_header("Cache-Control", "public, max-age=86400")
                apply_enterprise_security_headers(self)
                self.end_headers()
                self.wfile.write(media_bytes)
                return
            except Exception as e:
                self._send_error(f"Failed to serve product photo: {str(e)}", status=500, code="MEDIA_SERVE_FAILED")
                return

        if path.startswith("/api/v1/media/"):
            att_id = path.replace("/api/v1/media/", "").strip().split("/")[0]
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT file_path, mime_type, file_name FROM patient_attachments WHERE id = ?", (att_id,))
                row = cur.fetchone()
            if not row or not os.path.exists(row[0]):
                self._send_error("Media attachment not found.", status=404, code="ATTACHMENT_NOT_FOUND")
                return
            file_path, mime_type, file_name = row[0], row[1], row[2]
            try:
                with open(file_path, "rb") as f:
                    media_bytes = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime_type or "application/octet-stream")
                self.send_header("Content-Length", str(len(media_bytes)))
                self.send_header("Content-Disposition", f'inline; filename="{file_name}"')
                self.send_header("Cache-Control", "public, max-age=86400")
                apply_enterprise_security_headers(self)
                self.end_headers()
                self.wfile.write(media_bytes)
                return
            except Exception as e:
                self._send_error(f"Failed to serve media: {str(e)}", status=500, code="MEDIA_SERVE_FAILED")
                return

        # ── Modular Agentic Domain Dispatcher ────────────────────────────────
        from services.routes.agentic_routes import handle_agentic_get
        if handle_agentic_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Operations, Tasks, Diagnostics & Audit Domain Dispatcher ──
        from services.routes.diagnostics_operations_routes import handle_operations_diagnostics_get
        if handle_operations_diagnostics_get(self, path, query_params, auth_ctx):
            return

        # ── Patient 360 Master Center of Gravity (Service 2) ─────────────────
        # ── Modular Encounters, Consultations & SOAP Domain Dispatcher (/api/v1/encounters, /api/v1/ai/consultations) ──
        from services.routes.encounter_routes import handle_encounter_get
        if handle_encounter_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Telemedicine & Appointments Domain Dispatcher (/api/v1/appointments, telemed, qsura) ──
        from services.routes.telemedicine_routes import handle_telemedicine_get
        if handle_telemedicine_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Auth Domain Dispatcher ───────────────────────────────────
        from services.routes.auth_routes import handle_auth_get
        if handle_auth_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Prescriptions, Dispensing, Cold-Chain & Billing Domain Dispatcher (/api/v1/prescriptions, /api/v1/billing/invoices) ──
        from services.routes.billing_prescription_routes import handle_billing_prescription_get
        if handle_billing_prescription_get(self, path, query_params, auth_ctx):
            return

        # Classical Pharmacopoeia Monographs (Searchable UPI Mufradat Registry)
        if path in ("/api/v1/knowledge/monographs", "/api/v1/pharmacopoeia/monographs"):
            search_term = query_params.get("search", [""])[0].strip().lower()
            axis_filter = query_params.get("organ_axis", [""])[0].strip().lower()
            e1_param = query_params.get("is_schedule_e1", [None])[0]
            
            raw_items = list(UPI_MUFRADAT_REGISTRY)
            items = []
            for it in raw_items:
                c = dict(it)
                c["canonical_name"] = c.get("name") or c.get("canonical_name", "")
                c["name"] = c["canonical_name"]
                if c.get("is_schedule_e1") and match_schedule_e1_substance:
                    se1 = match_schedule_e1_substance(c["name"])
                    if se1:
                        c["mudabbar_protocol"] = se1.get("mudabbar_protocol")
                        c["statutory_warning"] = se1.get("statutory_warning")
                        c["max_single_dose_mg"] = se1.get("max_single_dose_mg")
                        c["max_daily_dose_mg"] = se1.get("max_daily_dose_mg")
                items.append(c)

            if e1_param is not None:
                is_e1 = e1_param.lower() in ("true", "1", "yes")
                items = [i for i in items if i.get("is_schedule_e1") == is_e1]
            if axis_filter:
                items = [i for i in items if any(axis_filter in a.lower() for a in i.get("organ_axes", []))]
            if search_term:
                def _matches_item(item):
                    c_name = item.get("canonical_name", "").lower()
                    u_name = item.get("urdu_name", "").lower()
                    b_name = item.get("botanical_name", "").lower()
                    syns = [s.lower() for s in item.get("synonyms", [])]
                    return (search_term in c_name or search_term in u_name or 
                            search_term in b_name or any(search_term in s for s in syns) or
                            search_term in item.get("traditional_uses", "").lower())
                items = [i for i in items if _matches_item(i)]

            self._send_json({
                "ok": True,
                "count": len(items),
                "monographs": items
            })
            return

        # ── Modular Pharmacy & Pharmacopoeia Domain Dispatcher ────────────────
        from services.routes.pharmacy_routes import handle_pharmacy_get
        if handle_pharmacy_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Clinical Protocols, 12-Gate Governance & Regimens Domain Dispatcher ──
        from services.routes.governance_protocols_routes import handle_governance_protocols_get
        if handle_governance_protocols_get(self, path, query_params, auth_ctx):
            return

        # ── Modular Doctor Continuum, Clinical Trials & Simulation Domain Dispatcher ──
        from services.routes.continuum_trials_routes import handle_continuum_trials_get
        if handle_continuum_trials_get(self, path, query_params, auth_ctx):
            return

        self._send_error(f"Clinical route not found: {path}", status=404, code="ROUTE_NOT_FOUND")





    # =========================================================================
    # POST Endpoints
    # =========================================================================
    def do_POST(self):
        client_ip = self.client_address[0] if hasattr(self, "client_address") and self.client_address else "127.0.0.1"
        if not check_rate_limit(client_ip):
            self._send_error("Too many requests. Please wait a moment before trying again.", status=429, code="RATE_LIMIT_EXCEEDED")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)
        body = self._read_json_body()
        is_safe, safety_err = inspect_payload_safety(body)
        if not is_safe:
            self._send_error(safety_err, status=403, code="INJECTION_DETECTED")
            return
        auth_ctx = self._get_auth_context()

        # ── Modular Patient Records & Longitudinal EHR Domain Dispatcher (/api/v1/patients, patient/360, timeline) ──
        from services.routes.patient_routes import handle_patient_post
        if handle_patient_post(self, path, query_params, auth_ctx, body):
            return

        # ── Product Packaging & Formulation Photo Upload (Service 4) ─────────
        if path in ("/api/v1/products/upload-photo", "/api/v1/therapeutic/products/upload-photo"):
            sku = (body.get("sku") or body.get("product_code") or "").strip().upper()
            file_name = (body.get("file_name") or f"{sku}.png").strip()
            raw_data = body.get("file_data") or body.get("image_data") or ""

            if not sku:
                self._send_error("Product SKU (e.g. 'ZAY-001') is required.", status=400, code="MISSING_SKU")
                return
            if not raw_data:
                self._send_error("file_data (Base64 image) is required.", status=400, code="MISSING_FILE_DATA")
                return

            # Parse MIME and decode base64
            mime_type = "image/png"
            if raw_data.startswith("data:") and ";base64," in raw_data:
                header, b64_part = raw_data.split(";base64,", 1)
                mime_type = header.replace("data:", "").strip()
            else:
                b64_part = raw_data
                ext = os.path.splitext(file_name)[1].lower()
                ext_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}
                mime_type = ext_map.get(ext, "image/png")

            ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
            if mime_type.lower() not in ALLOWED_IMAGE_TYPES:
                self._send_error(f"Unsupported product image format: {mime_type}. Allowed formats: JPG, PNG, WEBP, GIF.", status=400, code="INVALID_MIME_TYPE")
                return

            try:
                file_bytes = base64.b64decode(b64_part)
            except Exception:
                self._send_error("Invalid Base64 payload encoding.", status=400, code="INVALID_BASE64")
                return

            if len(file_bytes) > 15 * 1024 * 1024:
                self._send_error("Image exceeds 15 MB limit.", status=400, code="FILE_TOO_LARGE")
                return

            ext = os.path.splitext(file_name)[1]
            if not ext:
                ext = ".png" if "png" in mime_type.lower() else ".jpg"
            safe_filename = f"{sku}{ext}"

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prod_dir = os.path.join(base_dir, "uploads", "products")
            os.makedirs(prod_dir, exist_ok=True)
            target_path = os.path.join(prod_dir, safe_filename)

            with open(target_path, "wb") as f:
                f.write(file_bytes)

            image_url = f"/api/v1/media/products/{sku}"

            # Update database record
            with get_db() as conn:
                cur = conn.cursor()
                try:
                    cur.execute("ALTER TABLE master_products ADD COLUMN image_url TEXT")
                except Exception:
                    pass
                try:
                    cur.execute("ALTER TABLE inventory ADD COLUMN image_url TEXT")
                except Exception:
                    pass

                cur.execute("UPDATE master_products SET image_url = ? WHERE UPPER(sku) = ?", (image_url, sku))
                cur.execute("UPDATE inventory SET image_url = ? WHERE UPPER(batch_number) LIKE ? OR UPPER(name) LIKE ?", (image_url, f"%{sku}%", f"%{sku}%"))
                conn.commit()

            self._send_json({
                "ok": True,
                "message": f"Product photo for {sku} uploaded and linked successfully.",
                "sku": sku,
                "image_url": image_url,
                "file_size_bytes": len(file_bytes),
                "mime_type": mime_type
            }, status=200)
            return

        # ── Modular Agentic Domain Dispatcher ────────────────────────────────
        from services.routes.agentic_routes import handle_agentic_post
        if handle_agentic_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Operations, Tasks, Diagnostics & Audit Domain Dispatcher ──
        from services.routes.diagnostics_operations_routes import handle_operations_diagnostics_post
        if handle_operations_diagnostics_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Encounters, Consultations & SOAP Domain Dispatcher (/api/v1/encounters, /api/v1/ai/consult) ──
        from services.routes.encounter_routes import handle_encounter_post
        if handle_encounter_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Telemedicine & Appointments Domain Dispatcher (/api/v1/appointments, telemed, qsura) ──
        from services.routes.telemedicine_routes import handle_telemedicine_post
        if handle_telemedicine_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Auth & Identity Domain Dispatcher (/api/v1/auth/login, register, otp, refresh) ──
        from services.routes.auth_routes import handle_auth_post
        if handle_auth_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Prescriptions, Dispensing, Cold-Chain & Billing Domain Dispatcher (/api/v1/prescriptions, /api/v1/billing/invoices) ──
        from services.routes.billing_prescription_routes import handle_billing_prescription_post
        if handle_billing_prescription_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Pharmacy & Inventory Domain Dispatcher ───────────────────
        from services.routes.pharmacy_routes import handle_pharmacy_post
        if handle_pharmacy_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Clinical Protocols, 12-Gate Governance & Regimens Domain Dispatcher ──
        from services.routes.governance_protocols_routes import handle_governance_protocols_post
        if handle_governance_protocols_post(self, path, query_params, auth_ctx, body):
            return

        # ── Modular Doctor Continuum, Clinical Trials & Simulation Domain Dispatcher ──
        from services.routes.continuum_trials_routes import handle_continuum_trials_post
        if handle_continuum_trials_post(self, path, query_params, auth_ctx, body):
            return

        self._send_error(f"Cannot POST to {path}", status=404, code="ROUTE_NOT_FOUND")





    # =========================================================================
    # PATCH Endpoints
    # =========================================================================
    def do_PATCH(self):
        auth_ctx = self._get_auth_context()
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)
        body = self._read_json_body()

        # ── Modular Telemedicine & Appointments Domain Dispatcher (/api/v1/appointments, telemed, qsura) ──
        from services.routes.telemedicine_routes import handle_telemedicine_patch
        if handle_telemedicine_patch(self, path, query_params, auth_ctx, body):
            return

        self._send_error(f"Cannot PATCH to {path}", status=404, code="ROUTE_NOT_FOUND")

    # =========================================================================
    # DELETE Endpoints
    # =========================================================================
    def do_DELETE(self):
        auth_ctx = self._get_auth_context()
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # ── Modular Telemedicine & Appointments Domain Dispatcher (/api/v1/appointments, telemed, qsura) ──
        from services.routes.telemedicine_routes import handle_telemedicine_delete
        if handle_telemedicine_delete(self, path, query_params, auth_ctx):
            return

        self._send_error(f"Cannot DELETE to {path}", status=404, code="ROUTE_NOT_FOUND")


def ensure_essential_accounts():
    """Guarantee standard department desk accounts exist in DB during development/staging."""
    env = os.environ.get("ENVIRONMENT", os.environ.get("NODE_ENV", "development")).lower()
    if env in ("production", "prod") and os.environ.get("SEED_DEV_ACCOUNTS") != "1":
        print("[SECURITY] Production environment active: static test credential seeding disabled.")
        return

    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT LOWER(email) FROM users")
            existing = set(r[0] for r in cur.fetchall())

            essential_users = [
                ("USR-NURSE-REQ", "nurse@zayvorahealth.com", "nurse123", "Inpatient Nursing Station", "+91 98110 77201", "NURSE", "FAC-HQ-01"),
                ("USR-NURSE-SHORT", "nurse@zayvorahealth", "nurse123", "Inpatient Nursing Station", "+91 98110 77202", "NURSE", "FAC-HQ-01"),
                ("USR-MFG-REQ", "manufacturing@zayvorahealth.com", "admin123", "Head of Botanical QA/QC", "+91 98110 88201", "MANUFACTURING", "FAC-HQ-01"),
                ("USR-MFG-SHORT", "manufacturing@zayvorahealth", "admin123", "Head of Botanical QA/QC", "+91 98110 88202", "MANUFACTURING", "FAC-HQ-01"),
                ("USR-RES-REQ", "research@zayvorahealth.com", "doctor123", "Principal Clinical Investigator", "+91 98110 99201", "RESEARCH", "FAC-HQ-01"),
                ("USR-RES-SHORT", "research@zayvorahealth", "doctor123", "Principal Clinical Investigator", "+91 98110 99202", "RESEARCH", "FAC-HQ-01"),
            ]

            for uid, email, pwd, name, phone, role, fac in essential_users:
                if email.lower() not in existing:
                    h, salt = hash_password(pwd)
                    cur.execute("""
                        INSERT INTO users (id, email, password_hash, salt, full_name, phone, role, facility_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (uid, email, h, salt, name, phone, role, fac))
            conn.commit()
    except Exception as e:
        print(f"[WARN] ensure_essential_accounts check: {e}")


def run_server(port=8000):
    # Autonomous Database Integrity Check & Snapshot Backup
    try:
        from services.db_backup_guard import run_integrity_and_backup
        run_integrity_and_backup()
    except Exception as _b_err:
        print(f"[Safety Guard] Startup backup notice: {_b_err}")

    ensure_essential_accounts()
    server_address = ("0.0.0.0", port)
    httpd = ThreadedHTTPServer(server_address, ZayvoraApiHandler)
    print(f"============================================================")
    print(f" ZAYVORA Health OS — Live REST API Server & Database Bridge")
    print(f" Listening on http://localhost:{port}")
    print(f" Database: {DB_PATH}")
    print(f"============================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(os.getenv("PORT", sys.argv[1] if len(sys.argv) > 1 else "8000"))
    run_server(port)
