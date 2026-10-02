# ZAYVORA Health OS™ — Master Institutional Specification v2.0
**Clinician-Governed Digital Healthcare Operating Platform for Structured Unani-Tibb & Integrative Care**

*Document Status: Institutional Architectural Standard*  
*Version: 2.0-Defensible*  
*Applicability: Clinical Engineering, AI Governance, Regulatory Affairs, and Institutional Deployments*

---

## 1. Master System Definition & Positioning

### Master Definition
> **ZAYVORA Health OS™** is a clinician-governed digital healthcare operating platform designed to structure Unani clinical care across constitutional assessment, clinical documentation, evidence-informed decision support, individualized Nuskha workflows, pharmacy operations, longitudinal follow-up, research, and governance.

### Component Sub-Definitions:
* **Hakeem Sahab AI™**: An AI-assisted clinical decision-support system (CDSS) that retrieves approved knowledge, organizes clinical context, surfaces evidence and safety considerations, and prepares recommendations for review and final decision by an authorized human clinician.
* **ZAYVORA Sensing Platform™**: A connected measurement and telemetry layer for standardized physiological, imaging, and wearable data acquisition, pre-gate signal quality assessment, and integration into the longitudinal clinical record.
* **Structured Nuskha Authoring Framework**: A phased clinical formulation framework enabling registered clinicians to author, calibrate, and digitally authorize multi-tiered Unani therapeutic regimens (*Munzij/Mushil*, *Mu’addil*, *Muqawwi*, and *Ilaj-bit-Tadbeer*).

---

## 2. Institutional Boundaries & Intended Use

To ensure absolute clarity across clinical, legal, and regulatory domains, ZAYVORA operates across **5 Explicitly Segregated Boundaries**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       ZAYVORA HEALTH OS™ BOUNDARIES                                     │
├───────────────────┬───────────────────┬────────────────────┬─────────────────────┬──────────────────────┤
│ 1. CLINICAL CARE  │ 2. AI DECISION-   │ 3. SENSING &       │ 4. RESEARCH &       │ 5. REGULATORY &      │
│    (Human-in-Loop)│    SUPPORT (CDSS) │    HARDWARE (IoT)  │    SIMULATION       │    GOVERNANCE        │
├───────────────────┼───────────────────┼────────────────────┼─────────────────────┼──────────────────────┤
│ Licensed Clinician│ Non-autonomous    │ Validated pulse,   │ De-identified RWE   │ Secure electronic    │
│ holds sole legal  │ registrar; surfaces│ tongue, and lab   │ cohorts & academic  │ records, audit logs, │
│ authority to      │ evidence, dosage  │ telemetry. Pre-gate│ simulator; strictly │ Mudabbar SOP checks, │
│ diagnose and sign │ rules & safety    │ signal validation  │ marked: "For        │ CDSCO/ABDM sandbox   │
│ prescriptions.    │ constraints.      │ before review.     │ Education/R&D Only".│ alignment.           │
└───────────────────┴───────────────────┴────────────────────┴─────────────────────┴──────────────────────┘
```

---

## 3. The 10-Layer System Architecture

ZAYVORA Health OS is architected into **10 Interlocking Operational Layers**, serving role-based experiences (Doctor, Patient, Pharmacist, Researcher, Admin):

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             ROLE EXPERIENCES                                     │
│            [Doctor Desk]  [Patient Portal]  [Pharmacy]  [Admin]  [RWE]           │
├──────────────────────────────────────────────────────────────────────────────────┤
│ 10. GOVERNANCE / AUDIT / KNOWLEDGE RELEASE  (Versioned release gates, Merkle)    │
├──────────────────────────────────────────────────────────────────────────────────┤
│  9. OUTCOMES / RESEARCH / RWE               (Longitudinal registries, RWE)       │
├──────────────────────────────────────────────────────────────────────────────────┤
│  8. NUSKHA / PHARMACY / CARE EXECUTION      (Structured Nuskha, FEFO, Mudabbar)  │
├──────────────────────────────────────────────────────────────────────────────────┤
│  7. HAKEEM SAHAB AGENTIC AI (CDSS)          (10-State Machine, Human Gate)       │
├──────────────────────────────────────────────────────────────────────────────────┤
│  6. EVIDENCE & SAFETY                       (Deterministic Firewall: PASS/BLOCK) │
├──────────────────────────────────────────────────────────────────────────────────┤
│  5. UNANI KNOWLEDGE & REASONING             (Mufradat, Murakkabat, Bibliographic)│
├──────────────────────────────────────────────────────────────────────────────────┤
│  4. SENSING & MEASUREMENT                   (Device gateway, Signal Pre-Gate)    │
├──────────────────────────────────────────────────────────────────────────────────┤
│  3. CLINICAL ENCOUNTER                      (13-Tab Consultation, Asbab-e-Sitta) │
├──────────────────────────────────────────────────────────────────────────────────┤
│  2. PATIENT & CLINICAL RECORD               (Master Index, Longitudinal Profile) │
├──────────────────────────────────────────────────────────────────────────────────┤
│  1. IDENTITY & ACCESS CONTROL               (RBAC, Multi-tenant isolation)       │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Observation vs. Measurement vs. Clinical Diagnosis Separation

Under ZAYVORA clinical engineering invariants, **no sensor or AI model ever makes an automated diagnosis**. Every diagnostic consideration must follow a strict 7-stage evidentiary pipeline:

```text
[1. Clinical Observation]
           ↓
[2. Objective Measurement / Feature Extraction]
           ↓
[3. Signal Quality Pre-Gate Validation]  (If INVALID → Stop & Re-acquire)
           ↓
[4. Patient Clinical Context]
           ↓
[5. Published Pharmacopoeial Evidence]
           ↓
[6. Clinical Interpretation Support (Non-Autonomous)]
           ↓
[7. Registered Clinician Review & Decision]
```

### Application Across Core Diagnostic Modalities:

#### A. Radial Pulse (Nabz Acquisition Framework)
* **Status**: *Structured Pulse Acquisition & Telemetry (Device Integration Phase)*
* **Quality & Validation Layer**:
  - Repeatability and inter-operator variability tracking.
  - Sensor contact pressure thresholds ($10 \text{ to } 30 \text{ kPa}$).
  - Signal-to-Noise Ratio threshold ($\text{SNR} \ge 15 \text{ dB}$).
  - Environmental temperature & patient resting state logging ($>10 \text{ min}$ rest).
* **Clinical Boundary**: Nabz features (depth, rate, tension, elasticity) provide *kinetic waveform observations*, never an autonomous diagnosis of pathology.

#### B. Tongue Inspection (Lisaan Acquisition Framework)
* **Status**: *Standardized Image Capture & Observation Layer*
* **Quality & Validation Layer**:
  - Illumination validation threshold ($\ge 300 \text{ lux}$).
  - Color calibration target verification (standardized Macbeth/color reference card).
  - Defocus/sharpness scoring ($\ge 0.65$).
* **Clinical Boundary**: Lisaan inspection records coating, color, and moisture *observations*, which are correlated with digestive and humoral status exclusively by the clinician.

#### C. Physical Urinalysis (Qaroorah Acquisition Framework)
* **Status**: *Standardized Organoleptic & Classical Parameter Logger*
* **Parameters Recorded**: Color, consistency, transparency, sediment (*Rasub*), froth (*Zabad*), quantity, and odor.
* **Clinical Boundary**: Urinalysis features indicate *excretory humoral markers*, which require correlation with modern laboratory renal/hepatic profiles (LFT, KFT, urine microscopy) by the physician.

---

## 5. Posology Decision-Support Engine (Formerly ZAPE)

ZAYVORA does **not** employ an "exact automated dosing engine". It uses a **Posology Decision-Support Engine** configured as follows:

```text
Patient Factors (Age, Weight, Vital Strength / Quwa, Pregnancy)
                     +
Formulation Specification (UPI / NFUM Monograph Standard)
                     +
Classical Posology Constraints (Minimum / Maximum Therapeutic Bounds)
                     +
Safety Firewall Constraints (Renal / Hepatic eGFR, Allergies)
                     +
Herb-Drug Interaction Matrix (e.g., Warfarin + Guggul)
                     +
Clinician-Defined Patient Specifics
                     ↓
[Suggested Posology Range for Human Clinician Review]
                     ↓
[Clinician Decides, Modifies, or Overrides]
```

---

## 6. Structured Nuskha Authoring Framework

Replaces informal or marketing terminology ("symphonic") with a disciplined clinical formulation hierarchy:

1. **Tier 1: Munzij / Mushil (Where Clinically Appropriate)**:
   - *Indication*: Vitiated humor requiring concoction and physiological elimination in accordance with classical protocols (*Usool-e-Ilaj*).
   - *Safety Rule*: Contraindicated in acute exhaustion, severe dehydration, or pregnancy.
2. **Tier 2: Mu’addil (Constitutional Temperament Balancer)**:
   - *Indication*: Restoring specific organ temperament toward individual baseline equilibrium (*I'tidal*).
3. **Tier 3: Muqawwi (Vital Organ Tonic & Adaptogen)**:
   - *Indication*: Supporting vital organ faculties (*Quwa-e-Tabi'iyya, Hayawaniyya, Nafsaniyya*).
4. **Tier 4: Ilaj-bit-Tadbeer (Regimenal Interventions)**:
   - *Indication*: Non-pharmacological therapies (Hijama, Dalk, Hammam, Riyazat) indicated as primary or adjunctive regimens.

---

## 7. Knowledge Governance: 12-Volume Library & Treatises

To transform literary references into an auditable knowledge layer, every clinical monograph must fulfill the **ZAYVORA Knowledge Governance Protocol**:

| Governance Requirement | Specification |
| :--- | :--- |
| **Bibliographic Identity** | Canonical title, Author, Classical treatise code. |
| **Edition & Publisher** | Critical peer-reviewed academic edition, Publication date, ISBN/Publisher. |
| **Language & Translation** | Original language (Arabic/Persian/Urdu), Authorized English translation authority. |
| **Exact Citation Location** | Maqala (Discourse), Fasl (Chapter), Page, Monograph Number. |
| **Digitization Status** | OCR confidence score, Human-expert scholarly validation stamp. |
| **Clinical Interpretation Layer** | Commentary by authorized Academic Review Board separating empirical claims from modern pharmacological trials. |
| **Review Status** | `DRAFT` $\rightarrow$ `PEER_REVIEWED` $\rightarrow$ `GOVERNANCE_VERIFIED`. |

---

## 8. Closed-Loop Pharmacy & Inventory Controls

Replaces absolute marketing claims ("eliminating expired inventory") with defensible risk-reduction SOPs:

* **FEFO Workflow**: Automated First-Expiry-First-Out batch sorting designed to systematically **reduce expiry-related dispensing errors**.
* **Schedule E(1) & Hazardous Botanical Gate**:
  - Regulated under Drugs & Cosmetics Rules, 1945 (Schedule E-1).
  - Enforces digital lockout on unpurified toxic botanicals/minerals (*Aconitum ferox/Bish*, *Strychnos nux-vomica/Azaraqi*, *Arsenic trioxide/Samm-ul-Far*).
  - Dispensation is physically and digitally blocked until a verified laboratory batch detoxification certificate (*Mudabbar SOP*) is validated.
* **Bedside Dispensing Verification**: Dual-identifier barcode matching between patient identifier and medication lot.

---

## 9. Offline-Capable Clinical Mode

Replaces "100% Offline PWA" with an enterprise-grade disconnected clinical architecture:

```text
[Local Encrypted SQLite / IndexedDB Cache]
                     ↓
[Offline Clinical Encounter & Vitals Capture]
                     ↓
[Pending Synchronization Queue with Timestamping]
                     ↓
[Connectivity Restored]
                     ↓
[Conflict Detection & Cryptographic Reconciliation]
                     ↓
[Central Merkle Audit Log Verification]
```

*Offline Signature Governance*: Offline prescription signing is permitted only when local asymmetric cryptographic key management, tamper-evident hardware tokens, and deterministic conflict-resolution rules are active.

---

## 10. Educational Case Simulator vs. Core Clinical Operations

* **Status**: *Education & Research Workspace Only*
* **Explicit Boundary**: The Case Simulator is strictly partitioned from the production hospital electronic health record.
* **Disclaimer**: *"For Clinical Education, Academic Simulation, and Continuing Medical Education (CME) Use Only. Not for live diagnostic guidance."*

---

## 11. Objective Longitudinal Reassessment

Replaces outcome claims ("migration toward equilibrium") with objective documentation:
* Recorded as: **Longitudinal Mizaj Reassessment** or **Change in Assessed Mizaj-Related Clinical Features Over Time**.
* Equilibrium (*I'tidal*) is evaluated based on clinician-verified symptomatology, validated quality-of-life scales, and laboratory biomarker progression.

---

## 12. Regulatory Readiness & Software Classification

### A. US FDA Scope Clarification
* **Secure Electronic Records & Signatures**: System implements SHA-256 HMAC digital signatures, role-based access control, and hash-linked audit logging.
* **Part 11 Status**: Internal *Part 11 Technical Controls Implemented*. Formal validation and applicability assessment are conducted on a per-customer, per-facility deployment basis where FDA predicate rules apply.

### B. ABDM Interoperability Architecture
* **Standard**: ABDM-aligned interoperability architecture utilizing HL7 FHIR R4-based health data exchange.
* **Status**: *Milestone 1, 2, and 3 (M1, M2, M3) Sandbox Tested & In Progress*. Production milestone validation is subject to facility-level empanelment and gateway certification.

### C. CDSCO Medical Devices Rules, 2017 (India)
* Software used for specific clinical decision support and physiological signal interpretation is governed under the **Medical Devices Rules, 2017** and CDSCO Medical Device Software Guidance (July 2026).
* ZAYVORA modules are architected as **Non-Autonomous Decision Support (Class B SaMD equivalent)** where the physician retains ultimate diagnostic discretion.

---

## 13. System Implementation & Readiness Matrix

| Architectural Module | Current System State | Intended Role | Regulatory / Validation Pathway |
| :--- | :--- | :--- | :--- |
| **1. Identity & RBAC** | **Implemented & Verified** | Core Access Control | Role-based segregation, audit logging |
| **2. Patient Master Index** | **Implemented & Verified** | Longitudinal Profile | FHIR R4 Patient Resource alignment |
| **3. Clinical Encounter** | **Implemented & Verified** | 13-Tab Consultation | Clinician-governed documentation |
| **4. Sensing Quality Pre-Gate** | **Implemented & Verified** | Signal Telemetry Gate | Rejects SNR < 15, Motion, Lux < 300 |
| **5. Unani Knowledge Layer** | **Implemented & Verified** | Pharmacopoeial Reference | Bibliographic & scholarly governance |
| **6. Deterministic Safety Firewall** | **Implemented & Verified** | Safety Interlocking | Hardcoded rules (PASS, CAUTION, BLOCK, UNKNOWN) |
| **7. Hakeem Sahab AI (CDSS)** | **Implemented & Verified** | Decision Support | Non-autonomous; human approval gate |
| **8. Structured Nuskha & FEFO** | **Implemented & Verified** | Dispensary Governance | Mudabbar detox SOP verification gate |
| **9. RWE & Case Simulator** | **Implemented & Isolated** | Research & Education | Explicitly marked: For R&D/Education Only |
| **10. Audit Ledger & Signatures** | **Implemented & Verified** | Cryptographic Integrity | Merkle tree audit logs, SHA-256 HMAC |
| **Hardware Devices (Nabz/Lisan)** | **Prototype / Gateway Ready** | Connected Sensing | Subject to clinical validation & CDSCO registration |
| **ABDM Production Bridge** | **Sandbox Tested / In Progress** | Interoperability | NHA production milestone certification |

---

## 14. Verification vs. Validation Distinction

* **Software Verification**: 981 automated unit and integration tests verify deterministic software behavior, schema integrity, and permission invariants with zero failures (`tests/run_all_tests.py`).
* **Clinical Validation**: Institutional clinical trials evaluating clinician concordance and real-world outcomes will be conducted in partnership with authorized teaching hospitals.
* **Regulatory Empanelment**: Ongoing compliance tracking under CDSCO Medical Devices Rules (2017), ABDM Integration milestones, and applicable data privacy statutes.

---
*Approved Architectural Blueprint for ZAYVORA Health OS™ v2.0.*
