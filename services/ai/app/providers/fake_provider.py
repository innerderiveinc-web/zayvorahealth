"""
Deterministic fake provider for tests. Returns a fixed, well-formed
response by default (matching the §59 required section structure), or a
caller-supplied scripted response — never calls a real LLM.
"""
from __future__ import annotations

DEFAULT_WELL_FORMED_RESPONSE = """CLINICAL SUMMARY
Patient presents with chronic fatigue and joint stiffness, 3 months duration.

WHAT IS KNOWN
Symptoms consistent with a Balghami (cold-wet) pattern per structured intake.

UNANI PERSPECTIVE
Suggests weakened Meda-Amaa (digestive) axis function per classical framework.

BIOMEDICAL PERSPECTIVE
Differential should rule out hypothyroidism, anemia, and inflammatory arthropathy before Unani-specific treatment.

DIFFERENTIAL CONSIDERATIONS
Hypothyroidism, iron-deficiency anemia, early rheumatoid arthritis, chronic fatigue syndrome.

RED FLAGS
None reported in current presentation.

MISSING INFORMATION
TSH, CBC, ESR/CRP, RF/anti-CCP not yet available.

EVIDENCE
E0 (classical) support for digestive-strengthening Mufradat in this pattern; no E3+ evidence reviewed for this specific case yet.

SAFETY
No contraindications identified from available structured data; full Safety Firewall check required before any Nuskha is finalized.

POSSIBLE CARE OPTIONS
Consider digestive-strengthening Ilaj bil-Dawa pending labs; Ilaj bil-Tadbeer (rest, warmth) and Ilaj bil-Ghiza (warm, light meals) may be considered in parallel with biomedical workup.

MONITORING
Reassess in 2 weeks or sooner if new symptoms develop.

UNCERTAINTY
MODERATE confidence — biomedical workup pending; classical impression not yet confirmed against modern diagnostics.

CLINICIAN REVIEW REQUIRED
Yes — this is advisory only and has not been reviewed by a qualified practitioner."""


class ScriptedFakeProvider:
    def __init__(self, response: str | None = None):
        self._response = response or DEFAULT_WELL_FORMED_RESPONSE
        self.last_system_prompt: str | None = None
        self.last_user_prompt: str | None = None

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt
        return self._response
