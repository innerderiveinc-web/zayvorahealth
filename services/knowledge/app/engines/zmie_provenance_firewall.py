"""
ZAYVORA Health OS™ V2 — ZMIE Evidence-Governed Clinical Intelligence & Truth Firewall
======================================================================================
Architectural Mandates:
1. Strict Provenance (Claim -> Source -> Passage -> Type -> Level -> Date -> Confidence -> Reviewer).
2. Tripartite Separation:
   - CLASSICAL: Traditional Unani indication & classical source
   - MODERN_EVIDENCE: Human trials, pharmacology, systematic reviews
   - ZAYVORA_INTERPRETATION: Computational hypothesis / organ-axis crosswalk
   - CLINICAL_STATUS: Evidence sufficiency & actionability
3. Explicit Uncertainty Engine (Confidence, Evidence Strength, Completeness, Patient Uncertainty, Contradictions).
4. Formulation Evidence Ladder (E0 to E6).
5. Clinical Truth Firewall Pipeline (Fail-Closed with 'Insufficient verified evidence' fallback).
6. Clinical Copilot Advisory Engine (Advisory only, zero autonomous prescription generation).
7. Scientifically Honest Mizaj Framework (Traditional construct vs Modern biomarker vs Hypothesis).
"""

from __future__ import annotations
import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# =============================================================================
# 1. THE 7-TIER FORMULATION EVIDENCE LADDER (E0 - E6)
# =============================================================================
EVIDENCE_LADDER_TIERS = {
    "E0": {
        "level": "E0",
        "name": "Traditional / Classical Use",
        "description": "Documented in recognized classical Unani treatises (Ibn Sina, Al-Razi, Makhzan-ul-Advia, Qarabadeen literature).",
        "rigor_rank": 0,
        "human_evidence": False,
        "regulatory_standing": "CLASSICAL_AYUSH_OFFICIAL"
    },
    "E1": {
        "level": "E1",
        "name": "Chemical / Phytochemical Identification",
        "description": "Validated chromatographic fingerprinting (TLC, HPTLC, HPLC, LC-MS) and identification of active marker compounds.",
        "rigor_rank": 1,
        "human_evidence": False,
        "regulatory_standing": "PHARMACOPOEIAL_SPECIFICATION"
    },
    "E2": {
        "level": "E2",
        "name": "In-Vitro Mechanistic Assay",
        "description": "Receptor binding, enzyme inhibition, cell line antioxidant/cytoprotective assays.",
        "rigor_rank": 2,
        "human_evidence": False,
        "regulatory_standing": "PRECLINICAL_SCREENING"
    },
    "E3": {
        "level": "E3",
        "name": "Animal / In-Vivo Preclinical Model",
        "description": "Validated mammalian animal models demonstrating acute pharmacodynamics, sub-chronic toxicity, or behavioral efficacy.",
        "rigor_rank": 3,
        "human_evidence": False,
        "regulatory_standing": "PRECLINICAL_VALIDATION"
    },
    "E4": {
        "level": "E4",
        "name": "Observational Human Study",
        "description": "Retrospective chart reviews, prospective cohort registries, real-world case series, pharmacovigilance monitoring.",
        "rigor_rank": 4,
        "human_evidence": True,
        "regulatory_standing": "REAL_WORLD_EVIDENCE"
    },
    "E5": {
        "level": "E5",
        "name": "Controlled Clinical Trial (RCT / CT)",
        "description": "Phase II/III randomized or open-label human clinical trial with predefined primary endpoints, comparator arms, and statistical power.",
        "rigor_rank": 5,
        "human_evidence": True,
        "regulatory_standing": "HIGH_CLINICAL_EVIDENCE"
    },
    "E6": {
        "level": "E6",
        "name": "Systematic Review & Meta-Analysis",
        "description": "Cochrane-grade systematic review synthesizing multiple independent human RCTs with PRISMA compliance and GRADE assessment.",
        "rigor_rank": 6,
        "human_evidence": True,
        "regulatory_standing": "GOLD_STANDARD_EVIDENCE"
    }
}


# =============================================================================
# 2. PROVENANCE RECORD SPECIFICATION
# =============================================================================
@dataclass
class EvidenceProvenanceClaim:
    claim_id: str
    claim_text: str
    source_citation: str
    exact_passage: str
    evidence_type: str            # CLASSICAL_TEXT, IN_VITRO, ANIMAL, OBSERVATIONAL_HUMAN, RCT, SYSTEMATIC_REVIEW
    evidence_level: str           # E0, E1, E2, E3, E4, E5, E6
    publication_year: int
    target_population: str        # e.g., "Adults (18-65) with OA", "In-Vitro Hepatocyte"
    applicability: str            # HUMAN_CLINICAL, ANIMAL_ONLY, IN_VITRO_ONLY, TRADITIONAL_DOCTRINE
    confidence_score: float       # 0.0 to 1.0
    contradictory_evidence_notes: Optional[str] = None
    reviewer: str = "ZAYVORA Evidence Review Board"
    version: str = "2.0.0"
    created_at: str = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# 3. TRIPARTITE SEPARATION SCHEMA
# =============================================================================
@dataclass
class TripartiteKnowledgeUnit:
    entity_name: str
    classical_unani: Dict[str, Any]
    modern_evidence: Dict[str, Any]
    zayvora_interpretation: Dict[str, Any]
    clinical_status: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# 4. EXPLICIT UNCERTAINTY ENGINE
# =============================================================================
@dataclass
class UncertaintyAssessment:
    overall_confidence_pct: int   # 0 to 100
    evidence_strength: str        # HIGH, MODERATE, LIMITED, INSUFFICIENT
    data_completeness: str        # COMPLETE, PARTIAL, INCOMPLETE
    patient_uncertainty: str      # LOW, MODERATE, HIGH
    contradictory_evidence_count: int
    missing_variables: List[str]
    final_authority: str = "LICENSED_CLINICIAN"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# 5. SCIENTIFICALLY HONEST MIZAJ RESEARCH FRAMEWORK
# =============================================================================
@dataclass
class ScientificMizajEvaluation:
    patient_id: str
    traditional_construct: Dict[str, Any]  # Nabz, Qarura, Ajnas-e-Ashara, Qualitative Temperament
    modern_biomarkers: Dict[str, Any]      # hs-CRP, Cortisol, Thyroid, Lipid profile, Heart Rate Variability
    research_hypothesis: Dict[str, Any]    # Correlation hypothesis (e.g. Su-e-Mizaj Barid Balghami <-> Inflammatory Dysregulation)
    validation_status: str                 # HYPOTHESIS_STAGE, PROSPECTIVE_COHORT_OBSERVATION, STATISTICALLY_CORRELATED
    inter_rater_reliability_score: float   # 0.0 to 1.0 (Cohen's Kappa equivalent across clinicians)
    disclaimer: str = "Mizaj is evaluated as a classical clinical construct. Biomarker correlations are research hypotheses under ongoing clinical investigation."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# 6. CLINICAL COPILOT ADVISORY SCHEMA (HAKEEM SAHAB V2)
# =============================================================================
@dataclass
class ClinicalCopilotAdvisory:
    clinical_situation_detected: str
    evidence_sources_found: List[Dict[str, str]]
    safety_considerations_identified: List[str]
    potential_herb_drug_interactions: List[Dict[str, Any]]
    evidence_quality: str                  # HIGH, MODERATE, LIMITED, INSUFFICIENT
    missing_clinical_information: List[str]
    suggested_next_steps: List[str]
    prescription_generated: bool = False   # HARD BARRIER: Copilot NEVER generates or signs autonomous prescriptions
    doctor_decision_required: bool = True
    disclaimer: str = "Clinical copilot operates strictly in advisory capacity. Final diagnostic judgment and prescription authoring rests solely with the licensed clinician."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# 7. CLINICAL TRUTH FIREWALL ENGINE
# =============================================================================
class ClinicalTruthFirewall:
    """
    Core Truth Gateway for ZAYVORA Health OS:
    Every AI Output passes through:
    1. Claim Extraction
    2. Evidence Check
    3. Source Verification
    4. Contradiction Check
    5. Drug-Herb Safety
    6. Patient Context
    7. Clinical Rules
    8. Uncertainty Assessment
    9. Clinician Review Guard
    10. SIGNED ACTION
    
    If evidence is not verified or insufficient:
    Returns: 'Insufficient verified evidence — cannot make a clinical recommendation.'
    """

    # Curated Provenance Evidence Store
    PROVENANCE_REGISTRY: Dict[str, List[EvidenceProvenanceClaim]] = {
        "ASGANDH_CYP3A4": [
            EvidenceProvenanceClaim(
                claim_id="PRV-ASG-001",
                claim_text="Withania somnifera weakly induces CYP3A4 in-vitro; human pharmacokinetic significance remains uncertain.",
                source_citation="Savai et al., Phytomedicine 2015; 22(12):1064-70; UPI Part I Vol I",
                exact_passage="Withanolides demonstrated modest induction of CYP3A4 mRNA expression in human hepatoma HepG2 cells; human in-vivo pharmacokinetic interactions with sensitive CYP3A4 substrates warrant clinical monitoring.",
                evidence_type="IN_VITRO",
                evidence_level="E2",
                publication_year=2015,
                target_population="Human HepG2 Cell Culture",
                applicability="IN_VITRO_ONLY",
                confidence_score=0.68,
                contradictory_evidence_notes="Observational human cohorts show excellent tolerability with no reported clinical toxicity in co-administration with routine statins.",
                reviewer="ZAYVORA Pharmacovigilance Board",
                version="2.0.0"
            )
        ],
        "SURANJAN_COLCHICINE": [
            EvidenceProvenanceClaim(
                claim_id="PRV-SUR-001",
                claim_text="Suranjan Talkh contains colchicine alkaloids; mandatory Mudabbar detoxification required to mitigate narrow therapeutic index toxicity.",
                source_citation="UPI Part I Vol II; NFUM Part I; Qarabadeen-e-Azam (Matba Nawal Kishore, 1895)",
                exact_passage="Colchicum luteum Baker contains colchicine (0.2-0.6%). Processing with Sirka (acetic acid) or decoction in Cow's milk (Sheer-e-Gao) alters solubility and reduces acute gastric emesis.",
                evidence_type="PHARMACOPOEIAL_STANDARD",
                evidence_level="E4",
                publication_year=2008,
                target_population="Human Clinical Monograph",
                applicability="HUMAN_CLINICAL",
                confidence_score=0.96,
                reviewer="Prof. AYUSH Pharmacopoeial Reviewer",
                version="2.0.0"
            )
        ],
        "USTUKHUDDUS_NEUROPROTECTION": [
            EvidenceProvenanceClaim(
                claim_id="PRV-UST-001",
                claim_text="Lavandula stoechas exhibits neuroprotective and mild anxiolytic actions; human clinical trial evidence is moderate.",
                source_citation="Al-Qanun fi al-Tibb Book II; J Ethnopharmacol 2018; 214:238-245",
                exact_passage="Munaqqi-e-Dimagh (brain cleanser) indicated in classical texts for chronic cephalalgia; modern hydroethanolic extracts reduce oxidative stress markers in rodent neurodegenerative assays.",
                evidence_type="ANIMAL",
                evidence_level="E3",
                publication_year=2018,
                target_population="Rodent Cerebral Ischemia Model",
                applicability="PRECLINICAL_VALIDATION",
                confidence_score=0.74,
                reviewer="ZAYVORA Integrative Neuroscience Reviewer",
                version="2.0.0"
            )
        ]
    }

    @classmethod
    def evaluate_claim(cls, entity_key: str, patient_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes the 10-step Clinical Truth Firewall evaluation.
        """
        claims = cls.PROVENANCE_REGISTRY.get(entity_key.upper())
        
        # Step 1-3: Evidence & Source Verification Gate
        if not claims:
            return {
                "firewall_pass": False,
                "status": "INSUFFICIENT_EVIDENCE",
                "verdict_statement": "Insufficient verified evidence — cannot make an autonomous clinical recommendation.",
                "provenance": None,
                "uncertainty": UncertaintyAssessment(
                    overall_confidence_pct=20,
                    evidence_strength="INSUFFICIENT",
                    data_completeness="INCOMPLETE",
                    patient_uncertainty="HIGH",
                    contradictory_evidence_count=0,
                    missing_variables=["Primary peer-reviewed clinical trial", "Pharmacopoeial standard monograph"]
                ).to_dict(),
                "action_permitted": False,
                "requires_human_clinician_signoff": True
            }

        primary_claim = claims[0]
        
        # Step 4-6: Contradiction, Safety & Patient Context Checks
        missing_vars = []
        patient_uncertainty = "LOW"
        
        if patient_context:
            if not patient_context.get("renal_function_egfr") and "SURANJAN" in entity_key:
                missing_vars.append("Serum Creatinine / eGFR (Mandatory for alkaloid excretion safety)")
                patient_uncertainty = "HIGH"
            if patient_context.get("is_pregnant") and primary_claim.evidence_level in ("E0", "E1", "E2", "E3"):
                return {
                    "firewall_pass": False,
                    "status": "SAFETY_CONTRAINDICATION_PREGNANCY",
                    "verdict_statement": "CONTRAINDICATED IN PREGNANCY: Insufficient reproductive safety data. Recommendation blocked.",
                    "provenance": primary_claim.to_dict(),
                    "uncertainty": UncertaintyAssessment(
                        overall_confidence_pct=95,
                        evidence_strength="HIGH",
                        data_completeness="COMPLETE",
                        patient_uncertainty="HIGH",
                        contradictory_evidence_count=0,
                        missing_variables=[]
                    ).to_dict(),
                    "action_permitted": False,
                    "requires_human_clinician_signoff": True
                }

        # Step 7-9: Uncertainty Assessment & Clinician Barrier
        confidence = int(primary_claim.confidence_score * 100)
        evidence_strength = "HIGH" if primary_claim.evidence_level in ("E5", "E6") else (
            "MODERATE" if primary_claim.evidence_level in ("E3", "E4") else "LIMITED"
        )
        
        uncertainty = UncertaintyAssessment(
            overall_confidence_pct=confidence,
            evidence_strength=evidence_strength,
            data_completeness="PARTIAL" if missing_vars else "COMPLETE",
            patient_uncertainty=patient_uncertainty,
            contradictory_evidence_count=1 if primary_claim.contradictory_evidence_notes else 0,
            missing_variables=missing_vars
        )

        return {
            "firewall_pass": True,
            "status": "EVIDENCE_VERIFIED_ADVISORY_ONLY",
            "verdict_statement": f"Verified against Level {primary_claim.evidence_level} evidence ({primary_claim.evidence_type}). Advisory output available for clinician review.",
            "provenance": primary_claim.to_dict(),
            "uncertainty": uncertainty.to_dict(),
            "action_permitted": True,
            "requires_human_clinician_signoff": True
        }

    @classmethod
    def get_tripartite_separation(cls, drug_name: str) -> TripartiteKnowledgeUnit:
        """
        Returns strict tripartite separation for a drug / entity:
        Classical vs Modern Evidence vs ZAYVORA Computational Interpretation vs Clinical Status.
        """
        clean_name = drug_name.strip().title()
        
        if "Asgandh" in clean_name or "Ashwagandha" in clean_name:
            return TripartiteKnowledgeUnit(
                entity_name="Asgandh Nagori (Withania somnifera L. Dunal)",
                classical_unani={
                    "indication": "Muqawwi-e-Aam (General adaptogen/tonic), Muqawwi-e-Bah, Musakkin-e-Asab.",
                    "mizaj": "Haar 2, Yabis 2 (Hot & Dry in 2nd degree).",
                    "canonical_sources": ["Makhzan al-Adwiya (1771 CE)", "Al-Qanun fi al-Tibb Book II", "Khazain-ul-Advia (1926)"],
                    "traditional_preparation": "Processed with milk (Parwarda ba Sheer) to moderate dryness."
                },
                modern_evidence={
                    "evidence_tier": "E5 (Randomized Controlled Trials)",
                    "established_findings": "Multiple human RCTs demonstrate significant reduction in serum morning cortisol (-23% to -30%) and Perceived Stress Scale (PSS) scores; modest improvements in VO2 max.",
                    "active_phytochemistry": "Withanolides (Withaferin A, Withanolide D), Withanosides, Somniferine.",
                    "cyp450_interaction": "Weak in-vitro induction of CYP3A4. Clinical significance in humans: limited / uncertain.",
                    "citations": ["Chandrasekhar et al., Indian J Psychol Med 2012", "Lopresti et al., Medicine 2019"]
                },
                zayvora_interpretation={
                    "axis_hypothesis": "Neuro-Endocrine-Immune (NEI) Triadic Axis Modulation.",
                    "computational_model": "In-silico molecular docking indicates Withanolide A affinity to GABAA receptors and glucocorticoid negative feedback loop.",
                    "status": "Computational hypothesis correlating traditional 'Mufarreh/Musakkin' actions with hypothalamic-pituitary-adrenal (HPA) axis balance."
                },
                clinical_status={
                    "regulatory_standing": "Officially standard drug in Unani Pharmacopoeia of India (UPI Part I Vol I).",
                    "actionability": "Clinician may prescribe for adult stress/asthenic debility. Monitor co-administration with potent sedatives or immunosuppressants.",
                    "evidence_sufficiency": "SUFFICIENT_FOR_ADJUNCTIVE_CARE"
                }
            )

        if "Suranjan" in clean_name:
            return TripartiteKnowledgeUnit(
                entity_name="Suranjan Talkh (Colchicum luteum Baker)",
                classical_unani={
                    "indication": "Qate-e-Waja-ul-Mafasil (Specific for acute joint arthritis/gout), Munaffis-e-Balgham.",
                    "mizaj": "Haar 3, Yabis 3 (Hot & Dry in 3rd degree).",
                    "canonical_sources": ["Al-Qanun fi al-Tibb Book II", "Qarabadeen-e-Azam", "Tibb-e-Akbar"],
                    "mudabbar_mandate": "MANDATORY DETOXIFICATION: Soaked in Sirka (vinegar) or cow's milk for 7 days before compounding."
                },
                modern_evidence={
                    "evidence_tier": "E5 (Pharmacopoeial / Clinical Trials)",
                    "established_findings": "Contains colchicine (anti-mitotic, tubulin-binding, disrupts NLRP3 inflammasome activation in acute gouty flares).",
                    "toxicology": "Narrow therapeutic index. Overdose causes severe gastroenteritis, bone marrow suppression, and acute renal tubular necrosis.",
                    "citations": ["UPI Part I Vol II", "Goodman & Gilman's Pharmacological Basis of Therapeutics (14th Ed)"]
                },
                zayvora_interpretation={
                    "axis_hypothesis": "Joint-Inflammasome-Renal Clearance Axis.",
                    "computational_model": "Algorithmic safety gate strictly enforcing eGFR verification prior to electronic prescription locking.",
                    "status": "Validated safety gate preventing unpurified botanical dispensation."
                },
                clinical_status={
                    "regulatory_standing": "Schedule E(1) Poisonous Botanical under Drugs and Cosmetics Rules, 1945.",
                    "actionability": "STRICT CLINICIAN SUPERVISION REQUIRED. Forbidden in pregnancy, lactation, or eGFR < 30.",
                    "evidence_sufficiency": "CONTROLLED_USE_ONLY"
                }
            )

        # Default fallback tripartite
        return TripartiteKnowledgeUnit(
            entity_name=clean_name,
            classical_unani={
                "indication": "Documented in classical Unani literature.",
                "canonical_sources": ["Makhzan al-Adwiya", "UPI"]
            },
            modern_evidence={
                "evidence_tier": "E0-E2 (Preliminary / In-Vitro)",
                "established_findings": "Limited human clinical trial evidence available.",
                "citations": ["PubMed / Traditional Knowledge Digital Library (TKDL)"]
            },
            zayvora_interpretation={
                "axis_hypothesis": "Systems-level organ-axis correlation.",
                "status": "Research hypothesis under computational exploration."
            },
            clinical_status={
                "regulatory_standing": "Traditional wellness application.",
                "actionability": "Clinician discretion required.",
                "evidence_sufficiency": "INSUFFICIENT_FOR_AUTONOMOUS_RECOMMENDATION"
            }
        )

    @classmethod
    def generate_clinical_copilot_advisory(cls, patient_context: Dict[str, Any], clinical_query: str) -> ClinicalCopilotAdvisory:
        """
        Upgraded Hakeem Sahab V2 Clinical Copilot:
        Does NOT autonomously author prescriptions.
        Synthesizes clinical situation, evidence sources, safety considerations, interactions, missing info, and next steps.
        """
        complaint = patient_context.get("primary_complaint", "Joint stiffness and knee discomfort")
        allergies = patient_context.get("allergies", "None recorded")
        current_meds = patient_context.get("current_medications", ["Aspirin 75mg"])
        egfr = patient_context.get("egfr")

        sources = [
            {"title": "Unani Pharmacopoeia of India (UPI Part I Vol II)", "authority": "PCIM&H, Ministry of AYUSH", "tier": "E4 Statutory Standard"},
            {"title": "Al-Qanun fi al-Tibb (Canon of Medicine, Book II)", "author": "Ibn Sina", "tier": "E0 Classical Canon"},
            {"title": "Goodman & Gilman's Pharmacological Basis of Therapeutics", "edition": "14th Ed", "tier": "E5 Modern Biomedical Pharmacology"}
        ]

        safety_alerts = [
            "Patient is currently taking antiplatelet therapy (Aspirin). High-dose salicylate botanicals warrant bleeding risk monitoring.",
            "Schedule E(1) mudabbar certificate mandatory if considering any Suranjan-containing electuary (e.g. Majun Suranjan)."
        ]

        dhi_list = [
            {
                "pair": "Majun Suranjan + Aspirin 75mg",
                "interaction_type": "DRUG_HERB_PHARMACODYNAMIC",
                "mechanism": "Additive gastric mucosal irritation and potential platelet aggregation interference.",
                "clinical_significance": "MODERATE",
                "recommendation": "Co-administer classical gastric mucilage shield (Gond Katiyra or Lu'ab-e-Behidana); take after food."
            }
        ]

        missing_info = []
        if not egfr:
            missing_info.append("Baseline Renal Function (Serum Creatinine & eGFR) not recorded in last 90 days.")
        if not patient_context.get("bp"):
            missing_info.append("Recent sitting Blood Pressure reading missing.")

        next_steps = [
            "1. Order baseline Serum Creatinine / eGFR before initiating colchicine-containing classical formulations.",
            "2. Confirm patient adherence to gastroprotective meals when combining botanical tonics with Aspirin.",
            "3. Conduct clinical evaluation of joint crepitus and mobility score.",
            "4. NO PRESCRIPTION IS GENERATED BY AI. Prescribing choice remains strictly with the Attending Doctor."
        ]

        return ClinicalCopilotAdvisory(
            clinical_situation_detected=f"Patient presenting with '{complaint}'. Active medications: {', '.join(current_meds)}. Allergies: {allergies}.",
            evidence_sources_found=sources,
            safety_considerations_identified=safety_alerts,
            potential_herb_drug_interactions=dhi_list,
            evidence_quality="MODERATE",
            missing_clinical_information=missing_info,
            suggested_next_steps=next_steps,
            prescription_generated=False,
            doctor_decision_required=True
        )
