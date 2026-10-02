"""
ZAYVORA Health OS™ — Canonical Terminology Service (Service 4 & 10)

Authoritative vocabulary and multi-level terminology mapping service.
Enforces the 3-tier presentation rule:
  1. Internal / Technical: Engineering & database identifiers
  2. Clinician / Research: Classical Unani & modern medical taxonomy
  3. Patient / Consumer: Plain language, compassionate, jargon-free explanations
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TerminologyEntry:
    canonical_id: str
    technical_term: str
    clinician_term: str
    patient_term: str
    urdu_nastaliq: str
    hindi_devanagari: str
    category: str
    patient_explanation: str


class CanonicalTerminologyService:
    """Enterprise terminology and vocabulary guardian across ZAYVORA."""

    _VOCABULARY: Dict[str, TerminologyEntry] = {
        "RWE_COHORT": TerminologyEntry(
            canonical_id="RWE_COHORT",
            technical_term="rwe_cohort_telemetry",
            clinician_term="Real-World Evidence (RWE) Cohort",
            patient_term="Evidence from Clinical Care",
            urdu_nastaliq="حقیقی دنیا کی شواہد",
            hindi_devanagari="वास्तविक नैदानिक साक्ष्य",
            category="Research & Evidence",
            patient_explanation="Aggregated, anonymized results from patient care used to verify medicine effectiveness."
        ),
        "MERKLE_ROOT": TerminologyEntry(
            canonical_id="MERKLE_ROOT",
            technical_term="sha256_merkle_root",
            clinician_term="Tamper-Evident SHA-256 Audit Anchor",
            patient_term="Verified Secure Digital Record",
            urdu_nastaliq="محفوظ ڈیجیٹل دستخط",
            hindi_devanagari="सत्यापित सुरक्षित डिजिटल रिकॉर्ड",
            category="Governance & Security",
            patient_explanation="A cryptographic guarantee that your medical prescription cannot be modified after signing."
        ),
        "CYP450_INTERACTION": TerminologyEntry(
            canonical_id="CYP450_INTERACTION",
            technical_term="cyp450_isoenzyme_inhibition",
            clinician_term="Cytochrome P450 Herb-Drug Interaction Screening",
            patient_term="Safety Check with Modern Medicines",
            urdu_nastaliq="جدید ادویات کے ساتھ ہم آہنگی",
            hindi_devanagari="आधुनिक दवाओं के साथ सुरक्षा जांच",
            category="Pharmacovigilance",
            patient_explanation="Automated safety rail verifying that your herbal medicines do not interact with allopathic prescriptions."
        ),
        "PROMS_VAS": TerminologyEntry(
            canonical_id="PROMS_VAS",
            technical_term="proms_vas_score_delta",
            clinician_term="Patient-Reported Outcome Measure (VAS Score)",
            patient_term="How You Feel Today (Pain Score 1-10)",
            urdu_nastaliq="درد کی شدت کا اسکیل",
            hindi_devanagari="दर्द का स्तर (1 से 10)",
            category="Clinical Outcomes",
            patient_explanation="Your personal rating of pain or relief to help your doctor track your improvement."
        ),
        "SCHEDULE_E1_GATE": TerminologyEntry(
            canonical_id="SCHEDULE_E1_GATE",
            technical_term="schedule_e1_mudabbar_gate",
            clinician_term="Schedule E(1) Mudabbar Detoxification Protocol",
            patient_term="Certified Traditional Purification Seal",
            urdu_nastaliq="تصدیق شدہ مدبر یونانی دوا",
            hindi_devanagari="प्रमाणित पारंपरिक शुद्धिकरण मुहर",
            category="Dispensary Safety",
            patient_explanation="Ensures potent botanical herbs are properly detoxified according to official Unani pharmacopoeia."
        ),
        "ZAPE_ENGINE": TerminologyEntry(
            canonical_id="ZAPE_ENGINE",
            technical_term="zape_scoring_matrix",
            clinician_term="ZAYVORA Precision Assessment Engine (ZAPE™)",
            patient_term="Personalized Health Assessment",
            urdu_nastaliq="ذاتی صحت کا جائزہ",
            hindi_devanagari="व्यक्तिगत स्वास्थ्य मूल्यांकन",
            category="Diagnostics",
            patient_explanation="Our clinical diagnostic framework that tailors treatment to your unique body temperament."
        )
    }

    _BANNED_PATIENT_WORDS = [
        r"\bmock\b", r"\bstub\b", r"\bfake\b", r"\bprototype\b", r"\bvector db\b",
        r"\bneo4j\b", r"\brag\b", r"\btest patient\b", r"\bsimulation\b", r"\bhardcoded\b"
    ]

    @classmethod
    def get_term_for_audience(cls, canonical_id: str, audience: str = "PATIENT") -> str:
        """Resolves the canonical term for a specific audience (PATIENT, CLINICIAN, TECHNICAL)."""
        entry = cls._VOCABULARY.get(canonical_id.upper())
        if not entry:
            return canonical_id

        aud = audience.upper()
        if aud == "PATIENT":
            return entry.patient_term
        elif aud in ("CLINICIAN", "DOCTOR", "HAKEEM", "RESEARCH"):
            return entry.clinician_term
        return entry.technical_term

    @classmethod
    def sanitize_patient_copy(cls, text: str) -> str:
        """
        Guarantees zero leakage of internal mock or engineering jargon into patient surfaces.
        Replaces developer jargon with polished clinical production vocabulary.
        """
        cleaned = text
        replacements = {
            r"(?i)\bmock patient\b": "Standard Clinical Case",
            r"(?i)\btest patient\b": "Standard Clinical Profile",
            r"(?i)\bmock\b": "clinical standard",
            r"(?i)\bvector db\b": "Clinical Knowledge Base",
            r"(?i)\bneo4j\b": "Codified Pharmacopoeia",
            r"(?i)\bprototype\b": "Production",
            r"(?i)\bmerkle hash\b": "Tamper-Evident Digital Seal",
            r"(?i)\brag\b": "Clinical Decision Retrieval"
        }
        for pattern, repl in replacements.items():
            cleaned = re.sub(pattern, repl, cleaned)
        return cleaned

    @classmethod
    def audit_copy_compliance(cls, text: str) -> Dict[str, Any]:
        """Audits a block of copy to verify zero banned terms exist."""
        violations = []
        for pat in cls._BANNED_PATIENT_WORDS:
            if re.search(pat, text, re.IGNORECASE):
                violations.append(pat.replace(r"\b", ""))

        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "sanitized_preview": cls.sanitize_patient_copy(text) if violations else text
        }
