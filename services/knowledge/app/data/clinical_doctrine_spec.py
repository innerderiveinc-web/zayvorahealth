"""
ZAYVORA Health OS™ — Clinical Intelligence Doctrine & Enterprise Implementation Blueprint Spec
=============================================================================================
Reference:
  - ZAYVORA Health OS™ Clinical Intelligence Doctrine & Enterprise Implementation Blueprint (v1.0 - September 2026)
  - Core Doctrine: Mufradat -> Murakkab -> Nuskha | Mizaj | Organ-Axis | Evidence | Safety Firewall | Hakeem Sahab | Clinician Approval
  - Standard: Ancient Wisdom. Modern Science. Intelligent Care.
"""

from typing import Dict, Any, List, Optional

# ============================================================================
# 1. THE 9-LAYER CLINICAL REASONING STACK (Blueprint §1, §3)
# ============================================================================
CLINICAL_STACK_LAYERS: Dict[str, Dict[str, Any]] = {
    "1_MUFRADAT": {
        "layer_number": 1,
        "name": "Mufradat",
        "role": "Therapeutic Building Block",
        "definition": "The atomic therapeutic knowledge unit; smallest reusable, provenance-aware clinical object.",
        "required_domains": ["identity", "traditional_profile", "preparation_tadbeer", "safety", "evidence", "regulatory", "ai_state"],
        "validation_rule": "Authentication source + monograph where available. Must not treat raw scraped text as production knowledge."
    },
    "2_MURAKKAB": {
        "layer_number": 2,
        "name": "Murakkab",
        "role": "Engineered Combination",
        "definition": "The controlled combination layer supporting three strictly separated formulation classes.",
        "classes": {
            "CLASS_A": "Authentic Classical Murakkab (Immutable source-linked composition from UPI/NFUM/Qarabadeen)",
            "CLASS_B": "Classical Adaptation (Adapted for documented reasons, requires change rationale & compatibility review)",
            "CLASS_C": "ZAYVORA R&D Formulation (Research state only until safety, QC, and regulatory gates are satisfied)"
        },
        "validation_rule": "Must answer 'Why is this ingredient here?' and 'What changes if removed/substituted?' without inventing pharmacology."
    },
    "3_NUSKHA": {
        "layer_number": 3,
        "name": "Nuskha",
        "role": "Patient-Specific Application",
        "definition": "Where formulation knowledge meets the individual patient with clinical context, risks, and objectives.",
        "rule": "Never jump directly from disease label to recipe. Must establish context, risks, objectives and clinician authorization."
    },
    "4_MIZAJ": {
        "layer_number": 4,
        "name": "Mizaj",
        "role": "Individualized Traditional Framework",
        "definition": "Personalization layer modeled as a clinical assessment with provenance, not hidden AI intuition.",
        "governance": "Versioned instrument, allows indeterminate/mixed states, clinical override with audit log, no automatic prescription."
    },
    "5_ORGAN_AXIS": {
        "layer_number": 5,
        "name": "Organ-Axis",
        "role": "Functional Reasoning Layer",
        "definition": "Proprietary clinical organization framework mapping symptoms, labs, and disease patterns to organ axes.",
        "foundational_lineage": ["Jigar-Khasiya", "Jigar-Rahim", "Dimagh-Kuli"],
        "total_axes": 12,
        "status_labels": ["Not Assessed", "Assessment In Progress", "Clinician Review", "Monitoring", "Stable", "Follow-up Needed", "Urgent Referral Flag"]
    },
    "6_EVIDENCE": {
        "layer_number": 6,
        "name": "Evidence",
        "role": "Confidence and Limitations",
        "definition": "Distinguishes the strength and type of knowledge across E0 to E6 tiers; makes uncertainty visible.",
        "ai_rule": "AI must never collapse evidence levels into a single 'proven' label. UI must show confidence, limitations, and source trail."
    },
    "7_SAFETY_FIREWALL": {
        "layer_number": 7,
        "name": "Safety Firewall",
        "role": "Risk Control",
        "definition": "Deterministic, explainable, and auditable policy engine executing between knowledge retrieval and clinical action.",
        "decision_contract": {
            "inputs": ["patient_context", "proposed_intervention"],
            "checks": ["identity", "eligibility", "contraindications", "interactions", "special_population", "organ_status", "toxicity", "regulatory", "red_flags"],
            "outputs": ["PASS", "CAUTION", "BLOCK", "REFERRAL"]
        }
    },
    "8_HAKEEM_SAHAB": {
        "layer_number": 8,
        "name": "Hakeem Sahab AI",
        "role": "Clinician Copilot",
        "definition": "Retrieval-grounded clinical copilot for traceability, structured thinking, and uncertainty management.",
        "invariants": "Autonomous Diagnosis != Autonomous Prescription != Autonomous Treatment Decision."
    },
    "9_CLINICIAN_APPROVAL": {
        "layer_number": 9,
        "name": "Clinician Approval",
        "role": "Final Legal Authority",
        "definition": "Final Nuskha, treatment plan, modification, and execution remains exclusively under qualified human clinician control."
    }
}


# ============================================================================
# 2. EVIDENCE HIERARCHY E0 TO E6 (Blueprint §9)
# ============================================================================
EVIDENCE_TIERS_E0_E6: Dict[str, Dict[str, Any]] = {
    "E0": {
        "tier": "E0",
        "name": "Tradition-Only / Historical Mention",
        "typical_source": "Classical folklore, unreferenced oral tradition",
        "allowed_representation": "Historical context; strictly not clinical efficacy proof",
        "confidence_level": "LOWEST_CONTEXTUAL",
        "weight": 0.1
    },
    "E1": {
        "tier": "E1",
        "name": "Classical Formulation / Official Formulary",
        "typical_source": "Unani Pharmacopoeia of India (UPI), NFUM, Bayaz-e-Kabir, Qarabadeen",
        "allowed_representation": "Source-backed classical formulation fact with authentic historical composition",
        "confidence_level": "PHARMACOPOEIAL_TRADITIONAL",
        "weight": 0.4
    },
    "E2": {
        "tier": "E2",
        "name": "Pharmacognosy / Analytical Quality Evidence",
        "typical_source": "HPTLC fingerprinting, ICP-MS heavy metals, marker standardization assays",
        "allowed_representation": "Chemical identity, purity, safety profile, and mechanistic quality context",
        "confidence_level": "ANALYTICAL_VALIDATED",
        "weight": 0.6
    },
    "E3": {
        "tier": "E3",
        "name": "Preclinical / In-Vitro / Animal In-Vivo",
        "typical_source": "Peer-reviewed pharmacological in-vitro bioassays and rodent disease models",
        "allowed_representation": "Hypothesis or biological mechanistic pathway support only; no human clinical claim",
        "confidence_level": "BIOLOGICAL_MECHANISTIC",
        "weight": 0.7
    },
    "E4": {
        "tier": "E4",
        "name": "Observational / Case Series / Clinical Audit",
        "typical_source": "Institutional hospital audits, documented case series, cohort registries",
        "allowed_representation": "Preliminary clinical signal with documented study limitations and confounders",
        "confidence_level": "OBSERVATIONAL_SIGNAL",
        "weight": 0.8
    },
    "E5": {
        "tier": "E5",
        "name": "Controlled Clinical Evidence (Human RCTs)",
        "typical_source": "Randomized, double-blind, placebo- or active-controlled human clinical trials",
        "allowed_representation": "Statistically significant clinical efficacy and safety evidence with defined study constraints",
        "confidence_level": "CONTROLLED_CLINICAL",
        "weight": 0.95
    },
    "E6": {
        "tier": "E6",
        "name": "High-Confidence Synthesis (Meta-Analysis / Guidelines)",
        "typical_source": "Systematic reviews, Cochrane-grade meta-analyses, consensus clinical guidelines",
        "allowed_representation": "Gold-standard high-confidence clinical synthesis; highest grade evidence",
        "confidence_level": "SYSTEMATIC_SYNTHESIS",
        "weight": 1.0
    }
}


# ============================================================================
# 3. KNOWLEDGE STATE MACHINE (Blueprint §19, §39)
# ============================================================================
KNOWLEDGE_STATES = [
    "DRAFT",
    "SOURCE_VERIFIED",
    "STRUCTURED",
    "UNANI_EXPERT_REVIEW",
    "SAFETY_REVIEW",
    "REGULATORY_REVIEW",
    "CLINICAL_APPROVED",
    "AI_AVAILABLE",
    "MONITORED",
    "UPDATE_RE_REVIEW_RETIRE"
]

VALID_KNOWLEDGE_TRANSITIONS = {
    "DRAFT": ["SOURCE_VERIFIED"],
    "SOURCE_VERIFIED": ["STRUCTURED", "DRAFT"],
    "STRUCTURED": ["UNANI_EXPERT_REVIEW"],
    "UNANI_EXPERT_REVIEW": ["SAFETY_REVIEW", "STRUCTURED"],
    "SAFETY_REVIEW": ["REGULATORY_REVIEW", "UNANI_EXPERT_REVIEW"],
    "REGULATORY_REVIEW": ["CLINICAL_APPROVED", "SAFETY_REVIEW"],
    "CLINICAL_APPROVED": ["AI_AVAILABLE"],
    "AI_AVAILABLE": ["MONITORED", "UPDATE_RE_REVIEW_RETIRE"],
    "MONITORED": ["UPDATE_RE_REVIEW_RETIRE"],
    "UPDATE_RE_REVIEW_RETIRE": ["DRAFT", "RETIRED"]
}


# ============================================================================
# 4. TEN INVARIANTS: WHAT MUST NEVER HAPPEN (Blueprint §44)
# ============================================================================
WHAT_MUST_NEVER_HAPPEN: List[Dict[str, str]] = [
    {
        "id": "INV-01",
        "rule": "No Scraped Clinical Usability",
        "description": "A scraped or AI-generated drug monograph must never become clinically usable without formal expert and safety review."
    },
    {
        "id": "INV-02",
        "rule": "No Silent Classical Merging",
        "description": "The system must never silently merge conflicting classical formulations; discrepancies must be preserved as variant versions."
    },
    {
        "id": "INV-03",
        "rule": "No Unscreened Toxic Retrieval",
        "description": "A restricted, toxic, or ambiguous ingredient must never be suggested without passing through the deterministic Safety Firewall."
    },
    {
        "id": "INV-04",
        "rule": "No False AI Authoritativeness",
        "description": "An AI-generated answer must never appear more authoritative than the original primary literature from which it was derived."
    },
    {
        "id": "INV-05",
        "rule": "Full AI Suggestion Explainability",
        "description": "A clinician must never be presented with an AI suggestion whose underlying evidence and reasoning steps cannot be inspected."
    },
    {
        "id": "INV-06",
        "rule": "No Unaudited Prescription Editing",
        "description": "An approved Nuskha must never be edited without formal version incrementation and an immutable audit event."
    },
    {
        "id": "INV-07",
        "rule": "No Ungoverned Patient Data Research",
        "description": "Patient health records must never be incorporated into research or RWE cohorts without auditable consent under the Digital Personal Data Protection Act, 2023 (read with DPDP Rules, 2025)."
    },
    {
        "id": "INV-08",
        "rule": "No Exaggerated Regulatory Claims",
        "description": "A product must never be marketed or labeled with claims exceeding its statutory evidence tier and D&C Act Rule 161 approvals."
    },
    {
        "id": "INV-09",
        "rule": "No Silent Observational Learning",
        "description": "Clinical algorithms and decision rules must never silently mutate based on observational patient outcomes without formal board review."
    },
    {
        "id": "INV-10",
        "rule": "No Unsubstantiated Certification Claims",
        "description": "The platform must never be labeled clinically validated, secure, or globally certified without independent empirical proof."
    }
]


# ============================================================================
# 5. CLINICAL GOVERNANCE BOARD ROLES (Blueprint §33)
# ============================================================================
GOVERNANCE_BOARD_ROLES: Dict[str, str] = {
    "UNANI_CLINICAL_LEAD": "Classical framework, Mufradat/Murakkabat interpretation, Usool-e-Ilaj concordance",
    "MEDICAL_SAFETY_LEAD": "Adverse events, drug-herb interactions, contraindications, red flags, special populations",
    "BIOMEDICAL_EVIDENCE_LEAD": "Modern scientific literature synthesis, clinical trials, evidence tier grading (E0-E6)",
    "PHARMACY_QUALITY_LEAD": "Botanical identity, Tadbeer SOPs, ICP-MS heavy metals, GMP release gates",
    "REGULATORY_LEAD": "Drugs & Cosmetics Act 1940, Rule 161 compliance, AYUSH proprietary licenses, CITES controls",
    "AI_SAFETY_LEAD": "Copilot model grounding, prompt registries, hallucination audits, permission boundary enforcement",
    "ENGINEERING_LEAD": "Architecture, zero-trust security, immutable audit logging, automated test suites, DR recovery",
    "DATA_PRIVACY_LEAD": "ABDM compliance, FHIR R4 interoperability, consent lifecycle, Digital Personal Data Protection Act 2023 / DPDP Rules 2025 governance"
}


# ============================================================================
# 6. HELPER FUNCTIONS
# ============================================================================
def get_clinical_doctrine() -> Dict[str, Any]:
    """Returns the complete ZAYVORA Clinical Intelligence Doctrine specification."""
    return {
        "framework": "ZAYVORA Health OS™ Clinical Intelligence Doctrine",
        "version": "1.0 - September 2026",
        "motto": "Ancient Wisdom. Modern Science. Intelligent Care.",
        "stack_layers": CLINICAL_STACK_LAYERS,
        "evidence_tiers": EVIDENCE_TIERS_E0_E6,
        "knowledge_lifecycle": KNOWLEDGE_STATES,
        "invariants": WHAT_MUST_NEVER_HAPPEN,
        "governance_board": GOVERNANCE_BOARD_ROLES,
        "definition_of_done": (
            "ZAYVORA Clinical OS is implementation-complete only when every clinical knowledge item has provenance; "
            "every intervention passes a safety gate; every AI output is traceable; every clinician decision is versioned; "
            "every dispense is auditable; outcomes are measurable; external integrations are tested; security and recovery "
            "are evidenced; and governance can explain what the system did, why it did it, which sources it used and who approved."
        )
    }


def get_evidence_tier_e(tier_key: str) -> Optional[Dict[str, Any]]:
    """Retrieves an E0-E6 evidence tier specification."""
    return EVIDENCE_TIERS_E0_E6.get(tier_key.upper())


def validate_knowledge_state_transition(current_state: str, next_state: str) -> Dict[str, Any]:
    """
    Validates whether a knowledge item can transition from current_state to next_state
    in the governed knowledge engineering pipeline.
    """
    curr = current_state.upper()
    nxt = next_state.upper()

    if curr not in VALID_KNOWLEDGE_TRANSITIONS:
        return {"valid": False, "reason": f"Unknown current state '{curr}'"}

    allowed_next = VALID_KNOWLEDGE_TRANSITIONS[curr]
    if nxt not in allowed_next:
        return {
            "valid": False,
            "reason": f"Illegal transition from '{curr}' to '{nxt}'. Allowed next states: {allowed_next}"
        }

    return {
        "valid": True,
        "current_state": curr,
        "next_state": nxt,
        "gate_passed": True
    }
