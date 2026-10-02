"""
Hakeem Sahab™ Clinical Copilot (ZAYVORA Clinical Architecture Specification v4.0 §30).

Orchestration flow:
    Patient Data (services/clinical) + Knowledge (services/knowledge)
        -> System prompt enforcing FACT/EVIDENCE/INFERENCE/RECOMMENDATION/
           UNCERTAINTY distinctions and the §59 response format
        -> AI Provider (real Anthropic or fake, see providers/)
        -> Structural validation (engines/response_validator.py)
        -> Stored as an AiConsultation record (models/ai.py) for the
           §50 AI Governance audit trail
        -> Returned to the caller as ADVISORY ONLY

This function NEVER creates a Nuskha draft itself. Converting any part of
its output into an actual prescription is a distinct, separate action a
clinician takes via services/therapeutic — which independently runs its
own Safety Firewall regardless of what this engine said. See
docs/PHASE4-AI-CORE.md, "What this deliberately does not do."
"""
from __future__ import annotations

from app.clients.clinical_client import ClinicalClient
from app.clients.knowledge_client import KnowledgeClient
from app.engines.response_validator import parse_sections, validate_response_structure
from app.engines.zape_personalization import run_zape_personalization
from app.providers.base import AIProvider


SYSTEM_PROMPT = """You are Hakeem Sahab, ZAYVORA's clinical copilot and scholar-physician assistant. You assist a qualified \
Unani/integrative practitioner — you do not replace their judgment, diagnose \
autonomously, or prescribe.

Rules you must follow:
1. Never invent a classical citation, clinical trial, dosage source, or lab result. \
If evidence is unavailable, say so explicitly rather than filling the gap.
2. Distinguish FACT (what the patient/chart states), EVIDENCE (what a cited source \
supports), INFERENCE (your reasoning connecting facts to a clinical pattern), \
RECOMMENDATION (a possible next step), and UNCERTAINTY (what remains unknown) — \
do not blur these into unqualified assertions.
3. Never present a Unani/Mizaj-based impression as a substitute for necessary \
biomedical diagnosis, investigation, or emergency care.
4. Always end by stating this output requires clinician review before any action is taken.
5. HUMAN CLINICAL VOICE & PROFESSIONAL BEDSIDE MANNER: Maintain an authentic, warm, dignified, and scholarly clinician tone (Hakeem-e-Hazik). Write with clinical empathy, scientific precision, and collegiate respect. Never use robotic AI clichés (such as 'As an AI language model...', 'Certainly!', 'I would be glad to help', 'As an assistant...'). Speak with the natural authority and humanity of an experienced medical colleague advising at the bedside.

Respond using EXACTLY this structure, with each of these as a line by itself \
followed by its content:

CLINICAL SUMMARY
WHAT IS KNOWN
UNANI PERSPECTIVE
BIOMEDICAL PERSPECTIVE
DIFFERENTIAL CONSIDERATIONS
RED FLAGS
MISSING INFORMATION
EVIDENCE
SAFETY
POSSIBLE CARE OPTIONS
MONITORING
UNCERTAINTY
CLINICIAN REVIEW REQUIRED
"""


def _build_user_prompt(
    *,
    chief_complaint: str,
    patient_context: dict,
    candidate_mufradat: list[dict],
    rag_context: str = "",
) -> str:
    allergies = ", ".join(patient_context.get("allergies", [])) or "none documented"
    medications = ", ".join(patient_context.get("current_medications", [])) or "none documented"
    comorbidities = ", ".join(patient_context.get("comorbidities", [])) or "none documented"
    pregnancy = patient_context.get("pregnancy_status", "unknown")
    mufrad_names = ", ".join(m.get("name", "") for m in candidate_mufradat) or "none retrieved for this axis"

    # Mizaj context
    mizaj_info = patient_context.get("mizaj") or patient_context.get("mizaj_assessment") or {}
    if isinstance(mizaj_info, dict) and mizaj_info.get("primary_temperament"):
        mizaj_str = f"Primary: {mizaj_info.get('primary_temperament')}, Secondary: {mizaj_info.get('secondary_temperament')}, Condition: {mizaj_info.get('su_e_mizaj', 'Motadil')}"
    elif isinstance(mizaj_info, str):
        mizaj_str = mizaj_info
    else:
        mizaj_str = "Constitutional baseline under assessment (Motadil presumed)"

    # Identify any Schedule E(1) candidate drugs
    e1_alerts = []
    e1_keywords = ["suranjan", "kuchla", "bhilawa", "afeem", "bhang", "dhatura", "jamalgota", "bish"]
    for m in candidate_mufradat:
        name = m.get("name", "").lower()
        if any(k in name for k in e1_keywords):
            e1_alerts.append(f"Schedule E(1) statutory poison: '{m.get('name')}' requires mandatory Mudabbar (detoxification) and dosage ceiling compliance.")
    e1_notes = "; ".join(e1_alerts) if e1_alerts else "No Schedule E(1) statutory poisons among candidate single drugs."

    graph_block = f"\n{rag_context}\n" if rag_context else ""

    # ZAPE 2.0 Personalization
    zape = run_zape_personalization(
        patient_context=patient_context,
        candidate_drugs=candidate_mufradat,
        season=patient_context.get("current_season"),
    )
    zape_text = f"""
ZAPE 2.0 Adaptive Personalization Directives:
- Posology Scaling: {zape['posology']['formula_applied']} (Factor: {zape['posology']['posology_scaling_factor']})
- Posology Warnings: {"; ".join(zape['posology']['warnings']) or 'None'}
- Temperament Directives: {"; ".join(zape['temperament_modulation']['constitutional_modulations']) or 'Standard'}
- Recommended Correctives: {"; ".join(zape['temperament_modulation']['musleh_recommendations']) or 'Standard'}
- Seasonal Climate Consideration: {zape['seasonal_modulation']['seasonal_guidance']}
"""

    return f"""Patient presenting complaint: {chief_complaint}

Patient safety & constitutional context on file:
- Age: {patient_context.get("age", "unknown")}
- Pregnancy status: {pregnancy}
- Assessed Mizaj (10 Ajnas): {mizaj_str}
- Documented comorbidities: {comorbidities}
- Allergies: {allergies}
- Current medications: {medications}
- Statutory Schedule E(1) Safety Notes: {e1_notes}
{zape_text}
Candidate Mufradat retrieved from the Knowledge Graph for the relevant organ axis: {mufrad_names}
{graph_block}
Clinical Guidelines for Hakeem Sahab:
1. Ground classical Unani insights in authentic sources (Al-Qanoon, Kitab al-Hawi, UPI, NFUM).
2. Grade evidence according to ZAYVORA levels (E0: Classical, E1: Preclinical, E2: Observational, E3: Controlled Trial, E4: Systematic Review, E5: ZAYVORA Registry).
3. If proposing Ilaj bil-Dawa, check that any extreme or toxic drug is balanced by an appropriate Musleh (corrective).
4. Note that all outputs are advisory (safe_to_lock_prescription = False); clinical authority rests strictly with the treating practitioner.

Provide your consultation in the required format."""


def run_hakeem_consultation(
    *,
    chief_complaint: str,
    organ_axis: str | None,
    patient_id: str,
    auth_header: str,
    clinical_client: ClinicalClient,
    knowledge_client: KnowledgeClient,
    ai_provider: AIProvider,
) -> dict:
    patient_context = clinical_client.get_patient_safety_context(patient_id=patient_id, auth_header=auth_header)
    candidate_mufradat = knowledge_client.find_mufradat(organ_axis=organ_axis, auth_header=auth_header)

    rag_context = ""
    if hasattr(knowledge_client, "get_rag_context"):
        temperament = None
        mizaj_info = patient_context.get("mizaj") or patient_context.get("mizaj_assessment") or {}
        if isinstance(mizaj_info, dict):
            temperament = mizaj_info.get("primary_temperament")
        rag_context = knowledge_client.get_rag_context(
            organ_axis=organ_axis,
            symptoms=[w for w in chief_complaint.split() if len(w) > 3],
            temperament=temperament,
            auth_header=auth_header,
        )

    zape = run_zape_personalization(
        patient_context=patient_context,
        candidate_drugs=candidate_mufradat,
        season=patient_context.get("current_season"),
    )

    user_prompt = _build_user_prompt(
        chief_complaint=chief_complaint,
        patient_context=patient_context,
        candidate_mufradat=candidate_mufradat,
        rag_context=rag_context,
    )
    raw_response = ai_provider.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)

    missing_sections = validate_response_structure(raw_response)
    if missing_sections:
        return {
            "valid": False,
            "missingSections": missing_sections,
            "rawResponse": raw_response,
            "sections": {},
            "candidateMufradat": candidate_mufradat,
            "zapePersonalization": zape,
            "requiresClinicianReview": True,
        }

    evidence_grounding = None
    try:
        from services.knowledge.app.engines.evidence_claim_grounding_engine import EvidenceClaimGroundingEngine
        evidence_grounding = EvidenceClaimGroundingEngine.ground_ai_response(
            response_text=raw_response,
            claims=[]
        )
    except Exception:
        pass

    return {
        "valid": True,
        "missingSections": [],
        "rawResponse": raw_response,
        "sections": parse_sections(raw_response),
        "candidateMufradat": candidate_mufradat,
        "zapePersonalization": zape,
        "evidence_grounding": evidence_grounding,
        "requiresClinicianReview": True,
    }


def run_hakeem_refinement(
    *,
    chief_complaint: str,
    patient_id: str,
    clinician_feedback: str,
    previous_sections: dict[str, str],
    auth_header: str,
    clinical_client: ClinicalClient,
    knowledge_client: KnowledgeClient,
    ai_provider: AIProvider,
) -> dict:
    """Multi-turn refinement allowing the treating clinician to challenge,
    steer, or constrain Hakeem Sahab's advisory output.
    """
    patient_context = clinical_client.get_patient_safety_context(patient_id=patient_id, auth_header=auth_header)
    zape = run_zape_personalization(patient_context=patient_context)

    prior_summary = "\n".join([f"[{k.upper()}]: {v}" for k, v in previous_sections.items() if v])

    refine_prompt = f"""You are Hakeem Sahab in an interactive multi-turn copilot session with the treating clinician.

Initial Patient Complaint: {chief_complaint}
Patient Safety Context: Age {patient_context.get('age')}, Pregnancy: {patient_context.get('pregnancy_status')}, Allergies: {patient_context.get('allergies')}, Comorbidities: {patient_context.get('comorbidities')}

PREVIOUS ADVISORY CONSULTATION GENERATED:
{prior_summary}

CLINICIAN CRITIQUE & REFINEMENT INSTRUCTIONS:
\"\"\"{clinician_feedback}\"\"\"

TASK:
Re-evaluate and refine the consultation by incorporating the clinician's exact instructions and constraints.
Preserve clinical grounding and safety invariants. All outputs are strictly advisory (safe_to_lock_prescription = False).
Respond using EXACTLY the 13 required section headers."""

    raw_response = ai_provider.generate(system_prompt=SYSTEM_PROMPT, user_prompt=refine_prompt)
    missing_sections = validate_response_structure(raw_response)
    parsed = parse_sections(raw_response) if not missing_sections else {}

    return {
        "valid": len(missing_sections) == 0,
        "missingSections": missing_sections,
        "rawResponse": raw_response,
        "sections": parsed,
        "clinicianFeedbackApplied": clinician_feedback,
        "zapePersonalization": zape,
        "requiresClinicianReview": True,
    }

