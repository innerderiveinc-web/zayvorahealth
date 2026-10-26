# ZAYVORA HEALTH™ — Engine Input / Output Contracts & Schemas
## Formal API, Dataclass, and JSON Schema Specifications
**Document ID:** ZAYV-AUD-ENG-04  
**Audit Standard:** OpenAPI 3.1.0, JSON Schema 2020-12, Pydantic V2  
**Generated:** 2026-09-12T18:52:00+05:30  
**Scope:** Strict Ingress / Egress Validation Contracts for all 25 Engines  

---

## 1. Contract Overview

Every ZAYVORA engine operates under strict type-safe contracts implemented via Python `dataclasses`, Pydantic V2 models, or explicit dictionary validators. In accordance with zero-trust clinical architecture:
- All input payloads are validated before execution.
- Extraneous fields are stripped or rejected.
- Output payloads conform to deterministic schemas.
- Clinical safety and legal invariants (e.g. `safe_to_lock = False`, `requires_peer_review = True`) are enforced at serialization time.

---

## 2. Granular Contracts by Engine

### ENG-01 & ENG-13: Differential Considerations Engine
- **Source:** `services/clinical/app/engines/differential_engine.py`
- **Function:** `match_differential_considerations(chief_complaint: str, organ_axis: str | None = None, dominant_mizaj: str | None = None) -> list[dict[str, Any]]`

#### Ingress Contract:
```python
chief_complaint: str  # Mandatory, non-empty string, max 500 chars
organ_axis: str | None  # Optional, must match canonical 12 axes (e.g. 'mafasil', 'dimagh-aasab')
dominant_mizaj: str | None  # Optional, e.g. 'Haar Yabis', 'Barid Ratab'
```

#### Egress Contract:
```json
[
  {
    "score": 8,
    "unani_disease": "Niqris (Gout)",
    "urdu_name": "نقرس",
    "icd11_code": "FA25",
    "icd11_title": "Gout and certain crystal arthropathies",
    "snomed_concept_id": "90560007",
    "organ_axis": "mafasil",
    "classical_asbab": "Stasis of morbid Safra and Balgham in peripheral joints, impaired excretion",
    "usool_e_ilaj": "Tanqiya of morbid matter via Mus-hil-e-Balgham/Safra, Taqwiyat-e-Meda and Kulyah",
    "red_flags": [
      "Hot, erythematous swollen joint with systemic fever",
      "Renal colic or anuria indicating uric acid nephrolithiasis",
      "Severe tophi ulceration with secondary purulent infection"
    ]
  }
]
```

---

### ENG-06: Mizaj Assessor Engine
- **Source:** `services/clinical/app/engines/mizaj_assessor.py`
- **Function:** `calculate_mizaj_assessment(input_data: AjnasInput) -> dict[str, Any]`

#### Ingress Contract (AjnasInput):
```python
class AjnasInput:
    complexion: str          # ['ruddy', 'pale_yellow', 'chalky_white', 'dark_earthy']
    build: str               # ['muscular', 'lean', 'medium_soft', 'heavy_adipose']
    skin_feel: str           # ['hot_dry', 'cold_moist', 'hot_moist', 'cold_dry']
    pulse_rate: str          # ['fast_strong', 'slow_deep', 'bounding_moderate', 'weak_variable']
    digestion: str           # ['hyperactive', 'slow_sluggish', 'variable', 'efficient_strong']
    sleep: str               # ['insomnia', 'deep_prolonged', 'interrupted', 'moderate_sound']
    emotional_state: str     # ['irritable', 'calm_placid', 'anxious_fearful', 'cheerful_enthusiastic']
    thermal_preference: str  # ['cold', 'warmth', 'moderate', 'variable']
    weather_sensitivity: str # ['summer', 'winter', 'spring', 'autumn']
    physical_activity: str   # ['high', 'low_sedentary', 'moderate', 'sporadic']
```

#### Egress Contract:
```json
{
  "dominant_mizaj": "Haar Yabis",
  "secondary_mizaj": "Damawi",
  "scores": {
    "dam": 20.0,
    "balgham": 10.0,
    "safra": 55.0,
    "sauda": 15.0
  },
  "confidence_score": 0.85,
  "interpretation": "Marked Bilious (Safrawi) dyscrasia with heat and dryness predominance."
}
```

---

### ENG-08: Nuskha Nawisi Engine
- **Source:** `services/therapeutic/app/engines/nuskha_compiler.py`
- **Function:** `compile_nuskha(target_organ_axes: list[str], therapeutic_objective: str, ingredients: list[dict[str, Any]], patient_context: dict[str, Any]) -> dict[str, Any]`

#### Ingress Contract:
```json
{
  "target_organ_axes": ["mafasil"],
  "therapeutic_objective": "Relieve gouty arthralgia and resolve peripheral joint swelling",
  "ingredients": [
    {
      "name": "Suranjan Talkh Mudabbar",
      "is_mudabbar": true,
      "dose_mg": 250.0
    },
    {
      "name": "Zanjabeel",
      "dose_mg": 500.0
    }
  ],
  "patient_context": {
    "age": 35,
    "pregnancy_status": "not_applicable",
    "lactation_status": "no",
    "allergies": [],
    "current_medications": [],
    "comorbidities": [],
    "chief_complaint": "mild joint stiffness"
  }
}
```

#### Egress Contract:
```json
{
  "status": "compiled",
  "safe_to_lock": false,
  "juz_e_azam": "Suranjan Talkh Mudabbar",
  "target_organ_axes": ["mafasil"],
  "compiled_drugs": [
    {
      "name": "Suranjan Talkh Mudabbar",
      "dose_mg": 250.0,
      "role": "Juz-e-Azam",
      "is_mudabbar": true
    },
    {
      "name": "Zanjabeel",
      "dose_mg": 500.0,
      "role": "Muin"
    }
  ],
  "musleh_co_prescriptions": ["Katira (Astragalus gummifer)"],
  "safety_verdict": "SAFE_TO_CONSIDER"
}
```

---

### ENG-09: Hakeem Sahab Clinical Copilot
- **Source:** `services/ai/app/engines/hakeem_sahab.py`
- **Function:** `run_hakeem_consultation(chief_complaint: str, organ_axis: str, patient_id: str, auth_header: str, ...) -> dict[str, Any]`

#### Egress Contract (13 Canonical Sections):
```json
{
  "valid": true,
  "safe_to_lock": false,
  "assessment": "Clinical presentation consistent with Su-e-Hazm Barid Ratab (phlegmatic gastric dyscrasia).",
  "differential": [
    {"syndrome": "Su-e-Hazm Barid", "icd11": "MD90", "probability": "High"}
  ],
  "kulliyatPrinciples": "Taqwiyat-e-Meda and Tanqiya of phlegmatic humors via warming carminatives.",
  "usoolEIlaj": "Administer hot/dry digestive tonics before meals; avoid cold fluids.",
  "candidateMufradat": [
    {"name": "Sonf", "dose": "5g", "mizaj": "Haar 2 Yabis 1", "afal": "Kasir-e-Riyah"}
  ],
  "candidateMurakkabat": [
    {"name": "Jawarish Kamuni", "dose": "5g post-prandial"}
  ],
  "tadbeerRecommendations": [
    {"regimen": "Dalak-e-Batan", "frequency": "Daily morning gentle abdominal massage"}
  ],
  "ghizaRecommendations": {
    "recommended": ["Warm mutton broth with cumin", "Ginger infusions"],
    "restricted": ["Cold dairy", "Iced beverages", "Excessive raw salads"]
  },
  "biomarkerCorrelations": "Serum amylase within normal limits; check H. pylori if alarm symptoms develop.",
  "redFlags": [
    "Unintentional weight loss > 5% in 3 months",
    "Persistent nocturnal vomiting",
    "Signs of gastrointestinal hemorrhage (melena)"
  ],
  "citations": [
    {"source": "UPI Part I Vol 1", "entry": "Foeniculum vulgare Mill."},
    {"source": "Al-Qanoon fi al-Tibb", "entry": "Book III, Treatise on Stomach Disorders"}
  ],
  "confidenceScore": 0.88,
  "disclaimer": "Advisory algorithmic clinical decision support. Prescriptions must be locked and signed by a licensed practitioner."
}
```

---

### ENG-10: ZAPE Personalization Engine
- **Source:** `services/ai/app/engines/zape_personalization.py`
- **Function:** `run_zape_personalization(*, patient_context: dict[str, Any], candidate_drugs: list[dict[str, Any]] | None = None, season: str | None = None) -> dict[str, Any]`

#### Ingress Contract:
```json
{
  "patient_context": {
    "age": 72,
    "egfr": 38.0,
    "mizaj": "Barid Yabis"
  },
  "candidate_drugs": [
    {
      "name": "Asgandh",
      "base_dose_mg": 3000,
      "daraja": 2,
      "mizaj": "Haar Yabis"
    }
  ],
  "season": "shita"
}
```

#### Egress Contract:
```json
{
  "adjusted_drugs": [
    {
      "name": "Asgandh",
      "base_dose_mg": 3000,
      "personalized_dose_mg": 1800,
      "reduction_percent": 40.0,
      "rationale": "Renal scaling (eGFR 38 mL/min): 0.60x factor applied; winter seasonal thermal adjustment."
    }
  ],
  "scaling_factors": {
    "age_factor": 1.0,
    "renal_factor": 0.60,
    "mizaj_factor": 1.0,
    "seasonal_factor": 1.0
  }
}
```

---

### ENG-12: Safety Firewall
- **Source:** `services/therapeutic/app/engines/safety_firewall.py`
- **Function:** `run_safety_firewall(patient_context: dict[str, Any], ingredients: list[dict[str, Any]]) -> dict[str, Any]`

#### Ingress Contract:
```json
{
  "patient_context": {
    "age": 30,
    "pregnancy_status": "pregnant",
    "lactation_status": "no",
    "allergies": ["Sonf"],
    "current_medications": ["Warfarin 5mg"],
    "comorbidities": [],
    "chief_complaint": "chest pain"
  },
  "ingredients": [
    {"name": "Sonf"}
  ]
}
```

#### Egress Contract:
```json
{
  "verdict": "REFER",
  "severity": "CRITICAL",
  "blocking": true,
  "reasons": [
    "Red flag in presenting complaint: 'chest pain' — biomedical emergency evaluation takes priority.",
    "Patient is pregnant — most Ilaj bil-Dawa formulations are contraindicated pending ingredient-specific safety review.",
    "Proposed ingredient 'sonf' conflicts with a documented allergy ('sonf').",
    "Patient is on an anticoagulant (warfarin) — many botanicals affect bleeding risk; verify each ingredient individually before finalizing."
  ],
  "violations_count": 4
}
```

---

### ENG-20: Pharmacy Dispensary Engine
- **Source:** `services/therapeutic/app/engines/dispensary_engine.py`
- **Function:** `allocate_fefo_batches(*, batches: list[dict[str, Any]], requested_quantity: float, is_schedule_e1: bool = False, current_date: date | None = None) -> dict[str, Any]`

#### Ingress Contract:
```json
{
  "requested_quantity": 75.0,
  "is_schedule_e1": false,
  "batches": [
    {
      "id": "b-late",
      "batch_number": "BATCH-DEC",
      "expiry_date": "2026-12-31",
      "available_quantity": 200.0,
      "qc_release_status": "released"
    },
    {
      "id": "b-early",
      "batch_number": "BATCH-OCT",
      "expiry_date": "2026-10-15",
      "available_quantity": 50.0,
      "qc_release_status": "released"
    }
  ]
}
```

#### Egress Contract:
```json
{
  "allocations": [
    {
      "batch_id": "b-early",
      "batch_number": "BATCH-OCT",
      "allocated_quantity": 50.0,
      "expiry_date": "2026-10-15",
      "days_until_expiry": 33,
      "mudabbar_certified": false
    },
    {
      "batch_id": "b-late",
      "batch_number": "BATCH-DEC",
      "allocated_quantity": 25.0,
      "expiry_date": "2026-12-31",
      "days_until_expiry": 110,
      "mudabbar_certified": false
    }
  ],
  "total_allocated": 75.0,
  "batches_exhausted": ["b-early"]
}
```

---

### ENG-24: Clinical Governance Board Engine
- **Source:** `services/knowledge/app/board/governance_board.py`
- **Class:** `ClinicalGovernanceBoardEngine`

#### Proposal Creation & Publication Contract:
```python
# Create Proposal
proposal = ClinicalGovernanceBoardEngine.create_proposal(
    title="Revise maximum posology ceiling for Suranjan Talkh Mudabbar",
    target_type="SCHEDULE_E1_LIMIT",
    target_id="upi-suranjan-talkh",
    proposed_diff={"field": "max_single_dose_mg", "old_val": 250, "new_val": 300},
    created_by="Hakim Zafarullah Khan"
)

# Publish Change Order Output:
{
    "change_order_id": "CO-8F2B10A9",
    "proposal_id": "PROP-CA18A411",
    "title": "Revise maximum posology ceiling for Suranjan Talkh Mudabbar",
    "attestation_quorum_met": true,
    "attestations_count": 3,
    "sha256_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "is_published": true,
    "published_at": "2026-09-12T18:48:40.123456Z"
}
```

---

### ENG-25: QSURA Notification Engine
- **Source:** `services/clinical/app/qsura/communication_broker.py`
- **Function:** `send_notification(*, channel: str, recipient: str, message_type: str, parameters: dict[str, Any], patient_consent_verified: bool = True, ...) -> dict[str, Any]`

#### Egress Contract:
```json
{
  "message_id": "MSG-10b72d0d-5b80-4a04-9d70-a9003e2538c5",
  "delivery_status": "DELIVERED",
  "channel": "whatsapp",
  "recipient": "+919876543210",
  "rendered_content": "Appointment confirmed with Hakim Irfan at ZAYVORA Health Central for 2026-09-15 10:30 AM.",
  "phi_masked": true,
  "dispatched_at": "2026-09-12T18:48:40.890123Z"
}
```
