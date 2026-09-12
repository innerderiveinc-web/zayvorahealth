"""
Evidence Engine 2.0.

Codifies the multi-world epistemological evidence architecture:
1. Standardized Evidence Levels (E0 to E6)
2. Four Knowledge Worlds (World A, B, C, D)
3. GRADE Certainty Framework (High, Moderate, Low, Very Low)
4. Automated Study Design Classifier with strict guardrail preventing
   automatic conversion of E0 classical claims without clinician review.
"""
from __future__ import annotations

import re
from typing import Any

EVIDENCE_LEVELS: dict[str, dict[str, Any]] = {
    "E0": {
        "level": "E0",
        "name": "Classical Canonical Literature",
        "knowledge_world": "A",
        "description": "Historical treatises of Unani medicine (Ibn Sina, Razi, Majoosi, Jurjani, Kabiruddin).",
        "weight": 1.0,
        "requires_peer_review": True,
    },
    "E1": {
        "level": "E1",
        "name": "Official Pharmacopoeial Standards",
        "knowledge_world": "B",
        "description": "National pharmacopoeial monographs (UPI Vols I-VI, NFUM Vols I-VI, PLIM standards).",
        "weight": 2.0,
        "requires_peer_review": False,
    },
    "E2": {
        "level": "E2",
        "name": "Observational & Case Series",
        "knowledge_world": "C",
        "description": "Retrospective cohort studies, clinical case series, and open-label registry evaluations.",
        "weight": 3.0,
        "requires_peer_review": True,
    },
    "E3": {
        "level": "E3",
        "name": "In-Vitro & Phytochemical Characterization",
        "knowledge_world": "C",
        "description": "TLC/HPLC fingerprinting, cell line bioassays, antioxidant / receptor binding assays.",
        "weight": 4.0,
        "requires_peer_review": True,
    },
    "E4": {
        "level": "E4",
        "name": "In-Vivo Preclinical Animal Models",
        "knowledge_world": "C",
        "description": "Validated animal models of disease, acute/subacute toxicology, in-vivo pharmacodynamics.",
        "weight": 5.0,
        "requires_peer_review": True,
    },
    "E5": {
        "level": "E5",
        "name": "Controlled Clinical Trials (RCT Phase I/II)",
        "knowledge_world": "C",
        "description": "Randomized controlled trials evaluating clinical efficacy, safety endpoints, and posology.",
        "weight": 6.0,
        "requires_peer_review": True,
    },
    "E6": {
        "level": "E6",
        "name": "Multi-Centric Phase III RCT & Systematic Reviews",
        "knowledge_world": "C",
        "description": "PRISMA-compliant systematic reviews, Cochrane-style meta-analyses, and pivotal Phase III trials.",
        "weight": 7.0,
        "requires_peer_review": True,
    },
}

KNOWLEDGE_WORLDS: dict[str, dict[str, str]] = {
    "A": {
        "world": "A",
        "name": "Classical Unani Epistemology",
        "focus": "Mizaj, Akhlat, Quwa, Arwah, classical Af'al, and centuries of documented experiential safety.",
    },
    "B": {
        "world": "B",
        "name": "Contemporary Pharmacopoeial Regulatory Standards",
        "focus": "Statutory monographs (UPI/NFUM), Schedule E(1) posology limits, botanical identity, TLC finger-printing.",
    },
    "C": {
        "world": "C",
        "name": "Empirical Biomedical & Clinical Trial Literature",
        "focus": "Peer-reviewed PubMed/Medline studies, in-vitro/in-vivo pharmacokinetics, and RCT evidence.",
    },
    "D": {
        "world": "D",
        "name": "Real-World Evidence & Practice Data (RWE/RWD)",
        "focus": "ZAYVORA longitudinal patient registry, verified electronic health records, post-marketing pharmacovigilance.",
    },
}


def classify_study_design(text: str) -> dict[str, Any]:
    """Classifies a research title/abstract and suggests candidate evidence level.
    
    Invariant: Never automatically transforms an E0 claim into E5/E6 without
    explicit clinician peer-review verification.
    """
    clean = text.lower()
    
    # 1. Check for Meta-Analysis / Systematic Review (E6)
    if any(k in clean for k in ["meta-analysis", "systematic review", "prisma", "cochrane", "multi-center phase iii", "multicentric trial"]):
        predicted_level = "E6"
        study_type = "Systematic Review / Meta-Analysis"
        confidence = 0.92
    # 2. Check for Randomized Controlled Trial (E5)
    elif any(k in clean for k in ["randomized controlled", "rct", "double-blind", "placebo-controlled", "clinical trial phase"]):
        predicted_level = "E5"
        study_type = "Randomized Controlled Trial"
        confidence = 0.88
    # 3. Check for In-Vivo Preclinical (E4)
    elif any(k in clean for k in ["in vivo", "wistar rat", "mice", "animal model", "sprague-dawley", "preclinical", "induced in rats"]):
        predicted_level = "E4"
        study_type = "In-Vivo Animal Model"
        confidence = 0.85
    # 4. Check for In-Vitro / Phytochemical (E3)
    elif any(k in clean for k in ["in vitro", "phytochemical", "hplc", "tlc", "cell line", "antioxidant assay", "extract of", "spectrophotometric"]):
        predicted_level = "E3"
        study_type = "In-Vitro / Phytochemical Assay"
        confidence = 0.82
    # 5. Check for Case Series / Observational (E2)
    elif any(k in clean for k in ["case series", "case report", "observational study", "retrospective", "cohort study", "open-label"]):
        predicted_level = "E2"
        study_type = "Observational / Case Series"
        confidence = 0.80
    # 6. Check for Pharmacopoeial Monograph (E1)
    elif any(k in clean for k in ["pharmacopoeia", "monograph", "upi", "nfum", "standardization of", "physicochemical standard"]):
        predicted_level = "E1"
        study_type = "Official Pharmacopoeial Standard"
        confidence = 0.90
    # 7. Default to Classical / Theoretical (E0)
    elif any(k in clean for k in ["canon of medicine", "al-qanun", "ibn sina", "avicenna", "al-hawi", "rhazes", "classical text", "unani literature"]):
        predicted_level = "E0"
        study_type = "Classical Canonical Literature"
        confidence = 0.95
    else:
        predicted_level = "E0"
        study_type = "General Integrative Literature"
        confidence = 0.60

    level_meta = EVIDENCE_LEVELS[predicted_level]

    return {
        "predicted_level": predicted_level,
        "level_name": level_meta["name"],
        "knowledge_world": level_meta["knowledge_world"],
        "study_type": study_type,
        "confidence": confidence,
        "requires_peer_review": True,
        "peer_review_status": "pending",
        "governance_note": (
            "Evidence Engine 2.0 Invariant: Automated classifications are advisory. "
            "Formal upgrade of clinical claim weight requires clinician peer-review."
        ),
    }


def calculate_grade_certainty(
    starting_level: str,
    risk_of_bias: int = 0,
    inconsistency: int = 0,
    indirectness: int = 0,
    imprecision: int = 0,
    publication_bias: int = 0,
    large_effect_size: int = 0,
    dose_response_gradient: int = 0,
) -> dict[str, Any]:
    """Calculates GRADE (Grading of Recommendations Assessment, Development and
    Evaluation) certainty score.
    
    RCTs (E5, E6) start at HIGH (4). Observational/preclinical start at LOW (2)
    or MODERATE (3).
    """
    if starting_level in ("E5", "E6"):
        baseline_score = 4
    elif starting_level in ("E2", "E4"):
        baseline_score = 2
    elif starting_level == "E1":
        baseline_score = 3
    else:
        baseline_score = 1

    downgrades = risk_of_bias + inconsistency + indirectness + imprecision + publication_bias
    upgrades = large_effect_size + dose_response_gradient

    net_score = max(1, min(4, baseline_score - downgrades + upgrades))

    grade_map = {
        4: "HIGH",
        3: "MODERATE",
        2: "LOW",
        1: "VERY_LOW",
    }
    certainty = grade_map[net_score]

    rationales = []
    if risk_of_bias > 0:
        rationales.append(f"Downgraded -{risk_of_bias} for risk of study methodology bias")
    if inconsistency > 0:
        rationales.append(f"Downgraded -{inconsistency} for unexplained heterogeneity/inconsistency")
    if indirectness > 0:
        rationales.append(f"Downgraded -{indirectness} for indirectness of population or outcome")
    if imprecision > 0:
        rationales.append(f"Downgraded -{imprecision} for wide confidence intervals or small sample size")
    if publication_bias > 0:
        rationales.append(f"Downgraded -{publication_bias} for potential publication bias")
    if large_effect_size > 0:
        rationales.append(f"Upgraded +{large_effect_size} for significant effect magnitude")
    if dose_response_gradient > 0:
        rationales.append(f"Upgraded +{dose_response_gradient} for verified dose-response relationship")

    return {
        "starting_level": starting_level,
        "baseline_score": baseline_score,
        "total_downgrades": downgrades,
        "total_upgrades": upgrades,
        "net_grade_score": net_score,
        "grade_certainty": certainty,
        "evaluation_notes": rationales if rationales else ["Study meets standard methodology criteria without major downgrading factors."],
    }
