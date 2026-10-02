"""
ZAYVORA Health OS™ - 4-Tier Evidence Grading & Claims Discipline Matrix
Reference: Part One (Chapters 8 & 14), Dr. Irfan Ashraf, BUMS.

Implements:
  1. 4-Tier Evidence Scale (Tier 1 RCT, Tier 2 Mechanistic, Tier 3 Classical Qarabadeen, Tier 4 Consensus)
  2. Claims Discipline Validator (enforces AYUSH & Rule 161 permitted supportive claims vs prohibited absolutes)
"""

from typing import Dict, Any, List, Optional


EVIDENCE_TIERS: Dict[str, Dict[str, Any]] = {
    "TIER_1": {
        "tier": "TIER_1",
        "symbol": "✅",
        "name": "Tier 1: Strong Modern Clinical Evidence",
        "definition": "Double-blind, placebo-controlled RCTs and systematic meta-analyses with consistent positive endpoints.",
        "permitted_claim_type": "Research-referenced structure/function claims (e.g. 'CoQ10 enhances sperm motility in clinical trials').",
        "examples": ["Ashwagandha KSM-66 (cortisol reduction & sperm count)", "Boswellia AKBA (5-LOX inhibition in OA)", "CoQ10 (sperm motility)", "Fenugreek (glucose homeostasis)"]
    },
    "TIER_2": {
        "tier": "TIER_2",
        "symbol": "🔶",
        "name": "Tier 2: Moderate Mechanistic & Observational Evidence",
        "definition": "In-vitro & in-vivo cellular mechanistic validation + documented clinical case series + traditional pharmacovigilance.",
        "permitted_claim_type": "Mechanism-supported claims (e.g. 'Jatamansi modulates GABA-A receptors and supports neural calming').",
        "examples": ["Jatamansi (GABA modulation)", "Guggulsterones (PPAR-gamma / thyroid deiodinase)", "Punarnava (punarnavoside diuresis)"]
    },
    "TIER_3": {
        "tier": "TIER_3",
        "symbol": "📘",
        "name": "Tier 3: Classical Textual Evidence",
        "definition": "Authoritative classical Unani documentation across Qarabadeen literature, Al-Qanun, and Makhzan-ul-Adviya + botanical pharmacognosy identification.",
        "permitted_claim_type": "Traditional indication claims: 'Traditional use in Unani medicine for [classical indication]'.",
        "examples": ["Behman Safaid & Surkh (classical spermatogenic pair)", "Salab Misri (Muwalid-e-Mani substrate)", "Mastagi Rumi"]
    },
    "TIER_4": {
        "tier": "TIER_4",
        "symbol": "💡",
        "name": "Tier 4: Expert Consensus & Rational Hypothesis",
        "definition": "Used in polypharmacy formulations based on classical Afaal logic and clinical quorum consensus with emerging modern inquiry.",
        "permitted_claim_type": "Constitutional adjuvant / supportive vehicle claims only.",
        "examples": ["Specific mineral Kushta vehicle modulators", "Aqarqarha micro-dose neural ignition"]
    }
}

PROHIBITED_CLAIM_PATTERNS: List[Dict[str, str]] = [
    {"pattern": "cure", "reason": "D&C Act and Rule 161 strictly prohibit 'cure' claims for chronic NCDs."},
    {"pattern": "treats diabetes", "reason": "Substitute with 'Used for supportive management of Madhumeha / healthy blood glucose'."},
    {"pattern": "treats hypertension", "reason": "Substitute with 'Used for management of elevated blood pressure and vascular tone'."},
    {"pattern": "beats sildenafil", "reason": "Illegal drug-comparison claim. Substitute with 'Supports healthy male sexual function through Organ-Axis mechanisms'."},
    {"pattern": "natural viagra", "reason": "Prohibited marketing comparison under AYUSH advertising guidelines."},
    {"pattern": "burns fat", "reason": "Misleading claim. Substitute with 'Supports healthy weight management as part of a balanced lifestyle'."},
    {"pattern": "no side effects", "reason": "Prohibited absolute statement under D&C Act Rule 161."},
    {"pattern": "cures infertility", "reason": "Substitute with 'Used for supportive management of sub-fertility'."}
]


def get_evidence_tier_details(tier_key: str) -> Optional[Dict[str, Any]]:
    return EVIDENCE_TIERS.get(tier_key.upper())


def get_all_evidence_tiers() -> List[Dict[str, Any]]:
    return list(EVIDENCE_TIERS.values())


def validate_product_claim(claim_text: str, evidence_tier: str = "TIER_3") -> Dict[str, Any]:
    """
    Audits an advertising, packaging, or label claim text against statutory rules
    and evidence tier permissions.
    """
    text_lower = claim_text.lower()
    violations = []

    for item in PROHIBITED_CLAIM_PATTERNS:
        if item["pattern"] in text_lower:
            violations.append(f"Prohibited language '{item['pattern']}': {item['reason']}")

    # Tier checks
    if evidence_tier in ("TIER_3", "TIER_4") and any(w in text_lower for w in ["clinically proven", "rct verified", "statistically significant"]):
        violations.append(f"Claim asserts Tier 1 clinical trial proof, but ingredient is graded {evidence_tier}.")

    is_compliant = len(violations) == 0

    return {
        "claim_compliant": is_compliant,
        "input_claim": claim_text,
        "evidence_tier": evidence_tier,
        "violations": violations,
        "recommended_action": "CLAIM APPROVED FOR LABEL / MARKETING" if is_compliant else "REVISE CLAIM PER AYUSH CLAIMS DISCIPLINE MATRIX"
    }
