"""
ZAYVORA HEALTH™ — Clinical AI Safety Guardrails & Input Validation
Defends against prompt injection, safety invariant overrides, and unauthorized clinical actions.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class SafetyViolationError(Exception):
    """Raised when an input prompt violates clinical AI safety policies."""
    def __init__(self, message: str, violation_type: str, severity: str = "HIGH"):
        super().__init__(message)
        self.violation_type = violation_type
        self.severity = severity


@dataclass
class ValidationResult:
    is_safe: bool
    sanitized_text: str
    flags: List[str] = field(default_factory=list)
    risk_level: str = "NORMAL"  # NORMAL, SUSPICIOUS, BLOCKED
    violation_reason: Optional[str] = None


class ClinicalPromptGuardrail:
    """Input and output validation guardrails for clinical AI copilot."""

    # Patterns indicating attempts to override system instructions or bypass clinical safety
    OVERRIDE_PATTERNS = [
        (r"ignore\s+(all\s+)?(?:previous|prior|above)\s+instructions", "DIRECTIVE_OVERRIDE"),
        (r"disregard\s+(all\s+)?(?:system|safety)\s+(?:rules|directives|prompts)", "DIRECTIVE_OVERRIDE"),
        (r"you\s+are\s+now\s+(?:dan|developer\s+mode|unrestricted|god\s+mode)", "JAILBREAK_ROLEPLAY"),
        (r"(?:print|display|reveal|output|leak)\s+(?:your\s+)?(?:hidden\s+)?(?:system\s+prompt|instructions|api\s*key|configuration)", "PROMPT_EXFILTRATION"),
        (r"(?:force|set|override)\s+safe_to_lock\s*[:=]\s*(?:true|1)", "SAFETY_INVARIANT_TAMPER"),
        (r"auto[ -]sign\s+without\s+(?:clinician|doctor|hakeem|review)", "CLINICAL_GOVERNANCE_BYPASS"),
        (r"(?:omit|skip|bypass)\s+(?:the\s+)?(?:mudabbar|shodhan|purification|detoxification)", "MUDABBAR_BYPASS"),
    ]

    # Regulated toxic botanical raw usage warnings
    RAW_TOXIC_PATTERNS = [
        (r"raw\s+(?:kuchla|azraqi|strychnos|aconite|bish|afiyun)", "RAW_SCHEDULE_E1_REQUEST"),
        (r"unpurified\s+(?:kuchla|azraqi|strychnos|aconite|bish)", "RAW_SCHEDULE_E1_REQUEST"),
    ]

    @classmethod
    def validate_input_prompt(cls, prompt_text: str) -> ValidationResult:
        flags = []
        text_lower = prompt_text.lower()

        # 1. Check for prompt injection / override patterns
        for pattern, flag_type in cls.OVERRIDE_PATTERNS:
            if re.search(pattern, text_lower):
                flags.append(flag_type)

        # 2. Check for raw toxic botanical evasion
        for pattern, flag_type in cls.RAW_TOXIC_PATTERNS:
            if re.search(pattern, text_lower):
                flags.append(flag_type)

        # Critical severity checks
        critical_flags = {"SAFETY_INVARIANT_TAMPER", "DIRECTIVE_OVERRIDE", "MUDABBAR_BYPASS", "RAW_SCHEDULE_E1_REQUEST"}
        is_critical = any(f in critical_flags for f in flags)

        if is_critical:
            reason = f"Blocked by Clinical AI Safety Guardrails: detected {', '.join(flags)}."
            return ValidationResult(
                is_safe=False,
                sanitized_text="",
                flags=flags,
                risk_level="BLOCKED",
                violation_reason=reason,
            )

        if flags:
            return ValidationResult(
                is_safe=True,
                sanitized_text=prompt_text,
                flags=flags,
                risk_level="SUSPICIOUS",
                violation_reason=f"Flagged for auditing: {', '.join(flags)}.",
            )

        return ValidationResult(
            is_safe=True,
            sanitized_text=prompt_text,
            flags=[],
            risk_level="NORMAL",
            violation_reason=None,
        )

    @classmethod
    def validate_output_response(cls, response_text: str) -> ValidationResult:
        """Post-inference verification ensuring safety invariants hold."""
        flags = []
        text_lower = response_text.lower()

        # Invariant 1: safe_to_lock must NEVER be true
        if re.search(r"safe_to_lock\s*[:=]\s*true", text_lower):
            flags.append("ILLEGAL_SAFE_TO_LOCK_TRUE")

        # Invariant 2: Mudabbar must accompany Schedule E(1) references
        if "strychnos" in text_lower or "kuchla" in text_lower or "azraqi" in text_lower:
            if "mudabbar" not in text_lower and "purif" not in text_lower and "shodhan" not in text_lower:
                flags.append("MISSING_MUDABBAR_FOR_KUCHLA")

        if "aconitum" in text_lower or "bish" in text_lower:
            if "mudabbar" not in text_lower and "purif" not in text_lower and "shodhan" not in text_lower:
                flags.append("MISSING_MUDABBAR_FOR_ACONITE")

        # Invariant 3: Clinician review must be explicit
        if not ("clinician" in text_lower or "physician" in text_lower or "hakeem" in text_lower or "review" in text_lower):
            flags.append("MISSING_CLINICIAN_REVIEW_DISCLAIMER")

        if flags:
            return ValidationResult(
                is_safe=False,
                sanitized_text=response_text,
                flags=flags,
                risk_level="BLOCKED",
                violation_reason=f"Output safety violation: {', '.join(flags)}",
            )

        return ValidationResult(
            is_safe=True,
            sanitized_text=response_text,
            flags=[],
            risk_level="NORMAL",
            violation_reason=None,
        )
