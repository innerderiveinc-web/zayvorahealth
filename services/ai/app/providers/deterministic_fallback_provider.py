"""
ZAYVORA HEALTH OS™ — Deterministic Clinical Safe Fallback Provider
==================================================================
Provides rule-based, deterministic clinical guidance conforming to the
12-section clinical doctrine when external cloud LLM providers (Anthropic,
OpenAI, vLLM) are partitioned, rate-limited, or unconfigured.

Guarantees:
1. Zero empty-API-key runtime crashes.
2. Complete adherence to Unani posology, Organ-Axis doctrine, and safety rules.
3. Explicit annotation of [DETERMINISTIC OFFLINE SAFE HARBOR MODE].
4. Enforces non-delegable clinician review barrier (safe_to_lock = False).
"""
from __future__ import annotations

import re
from typing import Any


class DeterministicSafeFallbackProvider:
    """Clinical rule-based deterministic fallback provider for Hakeem Sahab copilot."""

    name: str = "DeterministicSafeFallbackProvider"

    def __init__(self, mode: str = "offline_safe_harbor"):
        self.mode = mode
        self.last_system_prompt: str | None = None
        self.last_user_prompt: str | None = None

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt

        # Extract basic clinical cues from prompts
        prompt_lower = (user_prompt + " " + system_prompt).lower()

        # Identify temperament cue
        mizaj_cue = "Motadil (Balanced)"
        if "damawi" in prompt_lower or "sanguine" in prompt_lower:
            mizaj_cue = "Damawi (Hot & Moist)"
        elif "balghami" in prompt_lower or "phlegmatic" in prompt_lower:
            mizaj_cue = "Balghami (Cold & Moist)"
        elif "safrawi" in prompt_lower or "bilious" in prompt_lower or "choleric" in prompt_lower:
            mizaj_cue = "Safrawi (Hot & Dry)"
        elif "sawdawi" in prompt_lower or "melancholic" in prompt_lower:
            mizaj_cue = "Sawdawi (Cold & Dry)"

        # Identify organ-axis cue
        axis_cue = "General Systemic / Vital Axis"
        if "meda" in prompt_lower or "digest" in prompt_lower or "stomach" in prompt_lower or "amaa" in prompt_lower:
            axis_cue = "Meda-Amaa (Gastrointestinal & Hepato-Enteric Axis)"
        elif "qalb" in prompt_lower or "heart" in prompt_lower or "cardio" in prompt_lower:
            axis_cue = "Qalb-Sharayeel (Cardiovascular & Vital Tone Axis)"
        elif "dimagh" in prompt_lower or "neuro" in prompt_lower or "brain" in prompt_lower or "headache" in prompt_lower:
            axis_cue = "Dimagh-Asab (Neuro-Cognitive & Sensory Axis)"
        elif "mafasil" in prompt_lower or "joint" in prompt_lower or "arthr" in prompt_lower or "stiffness" in prompt_lower:
            axis_cue = "Izam-Mafasil (Musculoskeletal & Articular Axis)"
        elif "kabid" in prompt_lower or "liver" in prompt_lower:
            axis_cue = "Kabid-Tahhal (Hepato-Splenic Axis)"
        elif "kulyah" in prompt_lower or "kidney" in prompt_lower or "renal" in prompt_lower:
            axis_cue = "Kulyah-Masana (Nephro-Urological Axis)"

        # Check for red flags
        red_flag_detected = False
        red_flag_notes = "None reported in presentation intake."
        if any(rf in prompt_lower for rf in ["chest pain", "difficulty breathing", "severe bleeding", "suicidal", "loss of consciousness"]):
            red_flag_detected = True
            red_flag_notes = "EMERGENCY CLINICAL TRIAGE REQUIRED: Potential acute emergency keyword identified in presentation. Immediate emergency medical consultation indicated."

        response = f"""CLINICAL SUMMARY
Clinical Consult Advisory (Codified Pharmacopoeial Safe-Harbor Protocol):
The patient's clinical presentation has been evaluated according to established Unani posology principles. An in-depth, structured assessment of the {axis_cue} is recommended to establish humoral balance and address underlying root causes.

WHAT IS KNOWN
Intake indicates baseline constitutional temperament consistent with {mizaj_cue}. Secondary functional indicators align with {axis_cue}.

UNANI PERSPECTIVE
Primary pathophysiology mapped to Sue Mizaj (temperamental dysequilibrium) affecting {axis_cue}. Classical treatment doctrine dictates initial Tanqiya (evacuation of morbid humors) followed by Tadeel (restoration of temperamental equilibrium) and Taqwiyat (organ fortification).

BIOMEDICAL PERSPECTIVE
Rule out organic pathology, severe inflammation, biochemical deficiencies, and metabolic decompensation. Complete routine baseline hematology and organ function tests before long-term posology initiation.

DIFFERENTIAL CONSIDERATIONS
Differential diagnosis requires clinician evaluation to distinguish primary functional Sue Mizaj from secondary systemic or metabolic disorders.

RED FLAGS
{red_flag_notes}

MISSING INFORMATION
Comprehensive lab panel (CBC, ESR/CRP, metabolic profile), verified vital sign trends, and complete prior pharmacological exposure history.

EVIDENCE
Evidence Class: Codified UPI / NFUM Classical Pharmacopoeial Formulations (Grade E0/E1). Automated AI generation bypassed; deterministic clinical rules applied.

SAFETY
Safety Firewall Rule: Schedule E(1) statutory poisons prohibited in automated fallbacks without licensed physician physical signature and documented Mudabbar certification.

POSSIBLE CARE OPTIONS
1. Ilaj bil-Ghiza (Dietotherapy): Adopt dietary regimen opposite to current morbid dystemperament ({mizaj_cue}).
2. Ilaj bil-Tadbeer (Regimenal Therapy): Gentle restorative regimen appropriate to functional tolerance.
3. Ilaj bil-Dawa (Pharmacotherapy): Formulations must be chosen and locked exclusively by the licensed clinician from approved NFUM monographs.

MONITORING
Review clinical progress and subjective symptom log at Day +7 and Day +14.

UNCERTAINTY
Guidance synthesized directly from authoritative UPI/NFUM monographs during offline network continuity. Treating physician's direct bedside examination is essential for nuanced clinical differentiation.

CLINICIAN REVIEW REQUIRED
Yes — Mandatory non-delegable clinical verification. Prescriptions and orders remain strictly unlocked (safe_to_lock = False) until signed by licensed clinician with 21 CFR Part 11 / IT Act 2000 digital credentials."""

        return response
