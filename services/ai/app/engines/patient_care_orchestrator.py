"""
ZAYVORA Health OS™ — AI Care Orchestrator (Care Intelligence 2.0)
================================================================
Reference:
  - Book 2: ZAYVORA Clinical Handbook (Triage & Continuum Care)
  - Non-Autonomous AI Doctrine: AI triages, routes, and assists; clinicians and pharmacists review and authorize.
  - Human Bedside Manner Rule 5: Empathetic, respectful, collegiate tone without robotic tropes.

Capabilities:
  1. Front-door natural language intent parsing (WhatsApp / App / Web).
  2. Statutory Red-Flag & Emergency detection with instant hard-stop.
  3. Context-aware agentic routing to:
     - Pharmacy Refill Desk (stock & FEFO allocation check)
     - Appointment Scheduling Desk (protocol-aligned follow-up windows)
     - Clinical Decision Desk (symptom flare-up review & VAS delta)
     - Diagnostic Laboratory Desk (lab result explanation)
  4. Human escalation & ticket generation with audit trail.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import datetime
import re
import hashlib
from services.clinical.app.engines.emergency_red_flag_guard import EmergencyRedFlagGuard, RED_FLAG_CRITERIA


class CareIntentType:
    EMERGENCY_RED_FLAG = "EMERGENCY_RED_FLAG"
    MEDICINE_REFILL = "MEDICINE_REFILL"
    APPOINTMENT_REQUEST = "APPOINTMENT_REQUEST"
    REPORT_INQUIRY = "REPORT_INQUIRY"
    SYMPTOM_FLARE_UP = "SYMPTOM_FLARE_UP"
    DIET_LIFESTYLE_QUERY = "DIET_LIFESTYLE_QUERY"
    GENERAL_INQUIRY = "GENERAL_INQUIRY"


@dataclass
class OrchestratorRouteDecision:
    intent: str
    confidence: float
    is_emergency: bool
    escalation_required: bool
    assigned_desk: str
    target_action: str
    ticket_payload: Dict[str, Any]
    patient_response: str
    clinical_alert: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


class PatientCareOrchestrator:
    """
    Agentic Front-Door Care Orchestrator that triages patient requests,
    enforces clinical safety firewalls, and routes to appropriate operational desks.
    """

    INTENT_KEYWORDS = {
        CareIntentType.MEDICINE_REFILL: [
            "dawai", "medicine", "dawa", "khatam", "refill", "order", "delivery", "suranjan",
            "majoon", "sharbat", "syrup", "capsule", "tablet", "khatam ho gayi", "reorder", "pharmacy"
        ],
        CareIntentType.APPOINTMENT_REQUEST: [
            "appointment", "follow-up", "followup", "doctor", "mulaqat", "dr", "booking", "schedule",
            "time", "slot", "milna", "visit", "checkup", "consultation", "reschedule"
        ],
        CareIntentType.REPORT_INQUIRY: [
            "report", "test", "lab", "cbc", "crp", "esr", "uric acid", "samajh nahi", "result",
            "investigation", "blood test", "x-ray", "scan", "biomarker"
        ],
        CareIntentType.SYMPTOM_FLARE_UP: [
            "dard", "pain", "swelling", "sojan", "worsened", "barh gaya", "takleef", "stiffness",
            "fever", "flare", "severe", "vomiting", "weakness", "symptoms wapas", "khujli"
        ],
        CareIntentType.DIET_LIFESTYLE_QUERY: [
            "parhez", "khana", "diet", "khorak", "exercise", "walk", "lifestyle", "water",
            "tadbeer", "hijama", "ghee", "milk", "chawal", "roti"
        ]
    }

    @classmethod
    def process_inbound_message(
        cls,
        patient_id: str,
        message_text: str,
        patient_context: Optional[Dict[str, Any]] = None
    ) -> OrchestratorRouteDecision:
        """
        Parses inbound message, applies safety firewall, and generates actionable route decision.
        """
        patient_context = patient_context or {}
        patient_name = patient_context.get("name", "Mohtaram Mareez")
        msg_clean = message_text.strip().lower()

        # Step 1: Emergency & Red Flag Evaluation
        red_flag_res = EmergencyRedFlagGuard.screen_patient_for_red_flags(
            symptoms=[msg_clean],
            labs={},
            notes=""
        )

        # Check explicit emergency phrases
        emergency_triggers = [
            "chest pain", "angina", "dil mein dard", "shortness of breath", "saans lene mein dushwari",
            "paralysis", "slurred speech", "zubaan ladkhadana", "suicidal", "khoon ki ulti",
            "severe headache", "unconscious", "behosh"
        ]
        is_stat_emergency = (not red_flag_res.get("is_safe_for_unani_care", True)) or any(trig in msg_clean for trig in emergency_triggers)

        if is_stat_emergency:
            alert_msg = (
                f"STAT ALERT: Patient {patient_name} ({patient_id}) reported urgent symptoms requiring immediate emergency review. "
                f"Emergency referral activated."
            )
            patient_reply = (
                f"Mohtaram {patient_name}, aapke bataye hue alamaat fori tawajjoh talab hain. "
                f"Bara-e-meherbani bila taakheer qareebi emergency hospital tashreef le jayein ya 108/112 par call karein. "
                f"Hamare duty doctor ko bhi foran muttala kar diya gaya hai."
            )
            return OrchestratorRouteDecision(
                intent=CareIntentType.EMERGENCY_RED_FLAG,
                confidence=1.0,
                is_emergency=True,
                escalation_required=True,
                assigned_desk="EMERGENCY_CLINICAL_ESCALATION",
                target_action="STAT_EMERGENCY_DISPATCH",
                ticket_payload={
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "inbound_message": message_text,
                    "urgency": "EMERGENCY_STAT",
                    "triage_summary": red_flag_res.get("statutory_note", "Acute severe symptoms reported")
                },
                patient_response=patient_reply,
                clinical_alert=alert_msg
            )

        # Step 2: Intent Classification
        scores: Dict[str, int] = {}
        for intent, kws in cls.INTENT_KEYWORDS.items():
            matched = sum(1 for kw in kws if kw in msg_clean)
            if matched > 0:
                scores[intent] = matched

        if scores:
            detected_intent = max(scores, key=scores.get)
            confidence = min(0.95, 0.65 + (scores[detected_intent] * 0.10))
        else:
            detected_intent = CareIntentType.GENERAL_INQUIRY
            confidence = 0.50

        # Step 3: Desk Assignment & Action Payload
        if detected_intent == CareIntentType.MEDICINE_REFILL:
            assigned_desk = "PHARMACY_REFILL_DESK"
            target_action = "INITIATE_REFILL_TICKET"
            patient_reply = (
                f"Adaab {patient_name} Sahab, aapki dawai ke refill ki darkhwast darj kar li gayi hai. "
                f"Hamare pharmacy team aapke active nuskha aur batch stock ko check karke jald update degi."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "workflow": "FEFO_REFILL_VERIFICATION",
                "inbound_text": message_text,
                "current_nuskha_id": patient_context.get("active_prescription_id", "RX-2026-ACTIVE")
            }

        elif detected_intent == CareIntentType.APPOINTMENT_REQUEST:
            assigned_desk = "APPOINTMENT_SCHEDULING_DESK"
            target_action = "PROPOSE_SLOTS"
            patient_reply = (
                f"Adaab {patient_name} Sahab, aapke clinical follow-up ke liye slots dekh rahe hain. "
                f"Aapki protocol timeline ke hisaab se agli mulaqat Dr. Sahab ke saath tay ki ja rahi hai."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "workflow": "PROTOCOL_FOLLOW_UP_BOOKING",
                "preferred_window": "NEXT_3_DAYS"
            }

        elif detected_intent == CareIntentType.REPORT_INQUIRY:
            assigned_desk = "DIAGNOSTIC_INTERPRETATION_DESK"
            target_action = "CLINICAL_REPORT_EXPLANATION"
            patient_reply = (
                f"Aapki report hamare clinical desk par receive ho chuki hai. "
                f"Hum iske ahem markers ko aasan zabaan mein tayyar karke doctor sahab ke notes ke saath aapko share karenge."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "workflow": "REPORT_PATIENT_TRANSLATION",
                "lab_reference": patient_context.get("latest_lab_id", "LAB-RECENT")
            }

        elif detected_intent == CareIntentType.SYMPTOM_FLARE_UP:
            assigned_desk = "DOCTOR_CLINICAL_DESK"
            target_action = "CLINICAL_TRAJECTORY_REVIEW"
            patient_reply = (
                f"Mohtaram {patient_name}, aapki takleef ki tafseel note kar li gayi hai. "
                f"Aapke moalij (doctor) ko foran alert bhej diya gaya hai taake wo aapke nuskha aur parhez ka jaiza le sakein."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "workflow": "SYMPTOM_FLARE_TRIAGE",
                "symptom_notes": message_text,
                "requires_clinician_callback": True
            }

        elif detected_intent == CareIntentType.DIET_LIFESTYLE_QUERY:
            assigned_desk = "TADBEER_GHIZA_DESK"
            target_action = "DELIVER_DIETETIC_GUIDANCE"
            patient_reply = (
                f"Aapki ghiza aur parhez ke mutalliq hidayat aapke mizaj ke mutabiq verify ki ja rahi hain. "
                f"Baraye meherbani thandi aur baadi cheezon se parhez rakhein jab tak tafseeli chart share na ho."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "workflow": "TADBEER_LIFESTYLE_ASSIST"
            }

        else:
            assigned_desk = "PATIENT_SUPPORT_DESK"
            target_action = "GENERAL_ASSISTANCE"
            patient_reply = (
                f"Adaab {patient_name} Sahab, aapka paigham receive ho gaya hai. "
                f"ZAYVORA care coordinator jald aapki rehnumai karega."
            )
            ticket_payload = {
                "patient_id": patient_id,
                "message": message_text
            }

        escalation = (detected_intent == CareIntentType.SYMPTOM_FLARE_UP)

        return OrchestratorRouteDecision(
            intent=detected_intent,
            confidence=round(confidence, 2),
            is_emergency=False,
            escalation_required=escalation,
            assigned_desk=assigned_desk,
            target_action=target_action,
            ticket_payload=ticket_payload,
            patient_response=patient_reply,
            clinical_alert=(f"Care Alert: Patient {patient_id} reported symptom changes." if escalation else None)
        )
