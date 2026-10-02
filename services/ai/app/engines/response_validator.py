"""
Structural validation of a Hakeem Sahab response against the required
format in ZAYVORA Clinical Architecture Specification v4.0 §59. This is NOT a hallucination
detector (that would require a much harder factual-grounding check) — it
only verifies the response is well-formed: every required section header
is present. A response missing a required section (e.g. no SAFETY
section, no CLINICIAN REVIEW REQUIRED disclaimer) fails validation and is
never returned to a caller, on the theory that a malformed response is a
more detectable and more preventable failure than a subtly wrong one, and
catching it costs nothing to check.
"""
from __future__ import annotations

REQUIRED_SECTIONS = [
    "CLINICAL SUMMARY",
    "WHAT IS KNOWN",
    "UNANI PERSPECTIVE",
    "BIOMEDICAL PERSPECTIVE",
    "DIFFERENTIAL CONSIDERATIONS",
    "RED FLAGS",
    "MISSING INFORMATION",
    "EVIDENCE",
    "SAFETY",
    "POSSIBLE CARE OPTIONS",
    "MONITORING",
    "UNCERTAINTY",
    "CLINICIAN REVIEW REQUIRED",
]


AYUSH_STATUTORY_KEYWORDS = [
    "clinician review",
    "advisory only",
    "qualified practitioner",
    "physician",
    "hakeem",
    "statutory",
    "ayush",
    "not a replacement",
]


def validate_statutory_disclaimer(response_text: str) -> bool:
    """
    Validates that the response contains the statutory AYUSH disclaimer
    and emphasizes non-delegable clinical verification.
    """
    if "CLINICIAN REVIEW REQUIRED" not in response_text:
        return False
    parsed = parse_sections(response_text)
    review_sec = parsed.get("CLINICIAN REVIEW REQUIRED", "").lower()
    if not review_sec:
        return False
    return any(k in review_sec for k in AYUSH_STATUTORY_KEYWORDS) or "yes" in review_sec


def validate_response_structure(response_text: str) -> list[str]:
    """Returns a list of missing section headers or validation errors. Empty list = valid."""
    missing = []
    for section in REQUIRED_SECTIONS:
        if section not in response_text:
            missing.append(section)
    if "CLINICIAN REVIEW REQUIRED" not in missing and not validate_statutory_disclaimer(response_text):
        missing.append("STATUTORY_DISCLAIMER_INVALID")
    return missing


def parse_sections(response_text: str) -> dict[str, str]:
    """Best-effort split of the response into {section_name: content}.
    Assumes each required section header appears on its own line, which
    is what the system prompt instructs the model to produce — if a
    provider doesn't follow that, validate_response_structure() above
    will have already caught the missing headers before this is called."""
    sections: dict[str, str] = {}
    current_section = None
    current_lines: list[str] = []

    for line in response_text.splitlines():
        stripped = line.strip()
        if stripped in REQUIRED_SECTIONS:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = stripped
            current_lines = []
        else:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections
