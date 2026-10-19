# ZAYVORA Health OS™ — AI Cognitive Systems & Copilot Audit
**Document ID**: `AUDIT-AI-06`  
**Target**: `services/ai` & Cognitive Engines  
**Standard**: Explainable, Citation-Backed, Non-Delegable Clinical AI  

---

## 1. Core Architectural Pillars

### A. Hakeem Sahab Clinical Copilot
- **File**: `services/ai/app/engines/hakeem_sahab.py`
- **Role**: Advisory clinical reasoning partner.
- **Invariants**:
  1. Never auto-prescribes or finalizes diagnosis.
  2. Every response includes structured fields: `unani_reasoning`, `biomedical_correlates`, `recommended_investigations`, `differential_diagnoses`, `red_flags`, `citations`, `uncertainty_rating`.
  3. Responses cite verified sources from ZKB monographs or peer-reviewed literature.

### B. ZAPE Personalization Engine
- **File**: `services/ai/app/engines/zape_personalization.py`
- **Role**: Posology and regimen tuning based on patient context.
- **Inputs**: Chronological age, body surface area / BMI, seasonal Mizaj, geographic climate, and current vital capacity.
- **Explainability**: Every dosage modification includes algorithmic rationale and references to classical posology rules (e.g., Avicenna's *Canon of Medicine* / Ibn Sina).

### C. Multimodal Lab Extractor
- **File**: `services/ai/app/multimodal/lab_report_extractor.py`
- **Capabilities**: OCR parsing of laboratory biochemistry panels, tongue photograph topography, and arterial pulse contours.
- **Safety Gate**: PII/PHI redaction before vectorization; low confidence (<92%) requires manual practitioner validation.

---

## 2. Model Agnostic AI Gateway & Provider Fallback
- **Base Architecture**: `services/ai/app/providers/fallback_router.py`
- **Provider Chain**: Primary (High-capability LLM) ➔ Secondary (Local vLLM / Fine-tuned open model) ➔ Tertiary (Deterministic rule compiler).
- **Safety Guardrails**: Response validator (`response_validator.py`) inspects outputs for hallucinated botanical entities, unsupported posology, and missing safety caveats.
