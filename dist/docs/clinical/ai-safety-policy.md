# ZAYVORA Health OS™ — Clinical AI Safety Policy

## 1. Scope & SaMD Classification
The Hakeem Sahab™ Clinical Copilot and ZAPE Personalization Engine are categorized as Class B / Class C Software as a Medical Device (SaMD) under CDSCO Medical Device Rules 2017 and IEC 62304:2006/Amd 1:2015.

## 2. Core Safety Guardrails
1. **Zero Autonomous Prescribing:** AI can suggest, cite, and cross-reference, but never lock or issue.
2. **Epistemological Grounding:** Every therapeutic suggestion must cite an authentic classical source (e.g. Al-Qanoon fit-Tibb, Kitab al-Hawi) or an official pharmacopoeial monograph (UPI / NFUM). Pure hallucinated citations trigger automated validation rejection.
3. **Mandatory Epistemological Separation:** AI responses must explicitly delineate:
   - **FACT:** Structured data documented in patient chart.
   - **EVIDENCE:** Explicitly cited literature or clinical trials.
   - **INFERENCE:** Algorithmic reasoning connecting facts to patterns.
   - **RECOMMENDATION:** Proposed considerations for treating clinician.
   - **UNCERTAINTY:** Missing information or clinical limitations.
4. **Mandatory Disclaimer:** Every AI response terminates with: *"ADVISORY ONLY: Requires review and digital sign-off by treating clinician prior to any medical decision."*
