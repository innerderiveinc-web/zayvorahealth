# ZAYVORA Health OS™ — ENGINE & AUTOMATION MATRIX
**Audit Date:** September 15, 2026

---

## 1. Clinical Intelligence Engines (Clinical Service)

### Mizaj Assessor (`engines/mizaj_assessor.py` — 233 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Determines patient's Mizaj (constitutional temperament) from clinical data |
| **Inputs** | Pulse quality (Nabz), tongue exam, symptoms, seasonal context, age, gender |
| **Outputs** | `MizajResult`: dominant (Damawi/Balghami/Safrawi/Sawdawi), secondary, confidence, clinical_notes |
| **Algorithm** | Weighted scoring matrix across 4 humoral dimensions |
| **Status** | ✅ FULLY IMPLEMENTED — connected to `/mizaj` router, persisted to DB |
| **Tests** | Present in `tests/test_mizaj_and_diagnostics.py` |
| **Frontend** | 🟡 Connected via `MizajAssessmentModal.tsx` |

### Organ Axis Engine (`engines/organ_axis_engine.py` — 419 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Maps clinical symptoms to classical Unani organ systems and identifies pathological axes |
| **Inputs** | Chief complaint, examination findings, Mizaj result, wearable vitals |
| **Outputs** | `OrganAxisAssessment`: primary axis, secondary axes, afaal status, severity score |
| **Algorithm** | Multi-axis symptom-to-organ mapping with severity scoring |
| **Status** | ✅ FULLY IMPLEMENTED — connected to `/dr` router |
| **Tests** | Present in test suite |
| **Frontend** | 🔵 Tab exists in doctor workspace, not wired |

### Afaal Cascade Engine (`engines/afaal_cascade_engine.py` — 146 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Evaluates functional capacity of organs (Afaal/Quwwa assessment) |
| **Inputs** | Organ axis assessment, patient history, comorbidities |
| **Outputs** | `AfaalCascadeResult`: organ function scores, cascade risk, recommendations |
| **Status** | ✅ FULLY IMPLEMENTED — `/afaal` router |
| **Frontend** | 🔵 Tab exists, not wired to engine output |

### Differential Engine (`engines/differential_engine.py` — 145 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Dual-paradigm differential diagnosis (ICD-11 biomedical + Unani NAMASTE) |
| **Inputs** | Chief complaint, vitals, lab results, organ axis, Mizaj |
| **Outputs** | Ranked differentials with probability, ICD-11 and NAMASTE codes |
| **Status** | ✅ FULLY IMPLEMENTED — `/dr` router |
| **Frontend** | 🔴 Not surfaced in UI |

### Digital Twin Engine (`engines/digital_twin.py` — 215 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Maintains a living computational model of the patient's health state |
| **Inputs** | All clinical encounters, labs, vitals, wearables, lifestyle |
| **Outputs** | `DigitalTwinState`: organ reserve scores, risk trajectories, predicted outcomes |
| **Status** | ✅ FULLY IMPLEMENTED — `/digital-twin` router, persisted to DB |
| **Frontend** | 🟡 `DigitalTwinCockpit.tsx` component — partially connected via FHIR |

---

## 2. Therapeutic Engines (Therapeutic Service)

### Nuskha Compiler (`engines/nuskha_compiler.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Compiles a validated Unani prescription from raw ingredients |
| **Processing** | Age posology (Young's/Cowling's rules), Mizaj-based dose adjustment, unit normalization |
| **Safety Gate** | Calls Safety Firewall before finalizing |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | 🔴 `NuskhaBuilder.tsx` uses SESSION_MOCK_TOKEN — real compilation not triggered |

### Safety Firewall (`engines/safety_firewall.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Non-bypassable clinical safety gate on all prescriptions |
| **Intercepts** | Schedule E(1) unpurified herbs (MudabbarDispenseBlockError), Warfarin/Digoxin interactions, pregnancy contraindications, red-flag emergencies |
| **Enforcement** | Hard block — returns 422 with safety_code on violation |
| **Status** | ✅ FULLY IMPLEMENTED — P0 blocker RESOLVED |
| **Frontend** | ✅ Error surfaced in `NuskhaBuilder` (when real API is connected) |

### Dispensary Engine (`engines/dispensary_engine.py`)
| Attribute | Value |
|---|---|
| **Purpose** | FEFO inventory management — picks oldest-expiry stock first |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | 🟡 Pharmacy page calls dispense endpoint — FEFO logic runs server-side |

### Pharmacovigilance Engine (`engines/pharmacovigilance.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Post-market surveillance of adverse herb-drug events |
| **Data Source** | OpenFDA integration + internal adverse event reports |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | ❌ Not connected to any UI |

### Tadbeer Guardrails (`engines/tadbeer_guardrails.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Validates lifestyle/regimen prescriptions against patient contraindications |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | ❌ Not connected |

### eBMR Engine (`engines/ebmr_engine.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Electronic Bedside Medical Record engine |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | 🟡 Partially surfaced via encounter workflow |

### Courier Engine (`engines/courier_engine.py`)
| Attribute | Value |
|---|---|
| **Purpose** | Manages physical delivery of dispensed medicines |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | ❌ Not connected |

---

## 3. AI Engines (AI Service)

### Hakeem Sahab AI™ (`engines/hakeem_sahab.py` — 244 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Clinical AI copilot — 5-layer advisory architecture |
| **Layers** | Knowledge retrieval → Safety check → Clinical reasoning → Evidence citation → Response validation |
| **Invariant** | `safe_to_lock = False` ALWAYS — AI can never autonomously lock a prescription |
| **LLM Backend** | Provider-abstracted (`providers/` directory) — supports Gemini, OpenAI |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | 🔴 `HakeemReviewDrawer.tsx` uses SESSION_MOCK_TOKEN |

### Response Validator (`engines/response_validator.py` — 91 lines)
| Attribute | Value |
|---|---|
| **Purpose** | Post-processes AI responses — removes hallucinations, enforces citation format |
| **Status** | ✅ FULLY IMPLEMENTED |

### ZAPE Personalization (`engines/zape_personalization.py` — 195 lines)
| Attribute | Value |
|---|---|
| **Purpose** | ZAYVORA Adaptive Personalization Engine — adapts AI recommendations to patient profile |
| **Inputs** | Patient Mizaj, age, comorbidities, treatment history, cultural preferences |
| **Status** | ✅ FULLY IMPLEMENTED |
| **Frontend** | ❌ Not exposed in UI |

---

## 4. Background Automation & Workers

| Component | File | Type | Status |
|---|---|---|---|
| Clinical task worker | `clinical/app/workers/` | In-memory queue | 🟡 Partial — no Redis/Celery |
| Disaster Recovery backup | `clinical/app/dr/backup_engine.py` | Scheduled Python | ✅ SHA-256 snapshots |
| ABDM sync worker | `clinical/app/interop/` | Async worker | 🟡 Framework exists |
| Cron scheduler | `clinical/app/routers/cron.py` | APScheduler | ✅ |
| Pharmacovigilance monitor | `therapeutic/app/pharmacovigilance/` | Batch job | ✅ |
| RabbitMQ/NATS event bus | — | Message queue | ❌ NOT IMPLEMENTED |
| Celery async task queue | — | Distributed queue | ❌ NOT IMPLEMENTED |

---

## 5. Engine-to-Frontend Connection Status

| Engine | Backend | Frontend Component | Connection Status |
|---|---|---|---|
| Mizaj Assessor | ✅ | `MizajAssessmentModal.tsx` | 🟡 Partial |
| Organ Axis | ✅ | Doctor workspace "axis" tab | 🔵 Tab exists, not wired |
| Afaal Cascade | ✅ | Doctor workspace "afaal" tab | 🔵 Tab exists, not wired |
| Differential Engine | ✅ | Doctor workspace "assessment" tab | 🔴 Not surfaced |
| Digital Twin | ✅ | `DigitalTwinCockpit.tsx` | 🟡 Partial |
| Nuskha Compiler | ✅ | `NuskhaBuilder.tsx` | 🔴 Mock token |
| Safety Firewall | ✅ | `NuskhaBuilder.tsx` | 🔴 Mock token (never fires) |
| Dispensary Engine | ✅ | `/pharmacy` page | 🟡 Connected |
| Hakeem Sahab AI™ | ✅ | `HakeemReviewDrawer.tsx` | 🔴 Mock token |
| ZAPE Personalization | ✅ | None | ❌ Not exposed |
| Pharmacovigilance | ✅ | None | ❌ Not exposed |
