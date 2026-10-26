# ZAYVORA Knowledge Base™ (ZKB) — Security, Safety & Governance Gap Analysis

**Document Identifier**: `ZKB-SEC-006`  
**Classification**: Clinical Safety & Cybersecurity Risk Assessment  
**Status**: DRAFT / UNDER REVIEW (Phase 1 Deliverable)  
**Governance Standard**: ISO 14971 (Medical Device Risk Management) & HIPAA/DISHA Privacy Guidelines

---

## 1. Executive Summary

This document performs an exhaustive threat model and clinical safety risk assessment of the **ZAYVORA Knowledge Base™ (ZKB)**. Because ZKB directly informs clinical prescribing, automated dose compilation, therapeutic compounding, and artificial intelligence reasoning, any failure in knowledge integrity represents a direct threat to patient safety.

---

## 2. Clinical Safety Threats & Threat Modeling

### 2.1 Threat 1: Schedule E(1) Statutory Poison Leakage Without Mudabbar Detoxification
- **Risk Severity**: **CRITICAL (CATSTROPHIC HAZARD)**
- **Clinical Manifestation**: Potent neurotoxic, cardiotoxic, or nephrotoxic botanicals/minerals (e.g., *Strychnos nux-vomica* / *Azaraqi*, *Aconitum chasmanthum* / *Bish*, *Papaver somniferum* / *Afiyun*) being compounded or prescribed in crude form without documented, authenticated *Mudabbar* (detoxification) processing.
- **Root Cause Vulnerability**: An unverified compound recipe or draft monograph lacking a mandatory relational foreign key to an attested `MudabbarProtocol`.
- **Architectural Mitigation**:
  - **Deterministic DB Constraint**: `zkb_mufradat.is_schedule_e1_poison` enforces `mudabbar_required = TRUE`.
  - **Formulation Gate**: Any `zkb_murakkabat` formulation containing a Schedule E(1) ingredient cannot transition to `CLINICALLY_APPROVED` or `AI_AVAILABLE` without a cryptographic sign-off from a Certified Toxicologist.
  - **Dispensary Interlock**: Warehouse barcode scanning at the dispensary rejects any batch where the eBMR lacks an authenticated Mudabbar certificate.

### 2.2 Threat 2: Classical Claims Injected into AI Prompts Without Empirical Grounding
- **Risk Severity**: **HIGH (SEVERE CLINICAL MALPRACTICE)**
- **Clinical Manifestation**: Classical historical claims from 10th-century texts (e.g., bloodletting for acute shock, toxic heavy metal dosages, or non-empirical infectious disease treatments) being cited by AI as contemporary clinical advice.
- **Root Cause Vulnerability**: Unfiltered semantic vector searches injecting raw historical texts directly into clinical copilot context windows.
- **Architectural Mitigation**:
  - **Physical State Partition**: Only records with `current_lifecycle_state = 'AI_AVAILABLE'` and `safe_for_ai = TRUE` are indexed into the production vector retrieval collection.
  - **Historical vs. Modern Separation**: Relational schema explicitly splits `historical_single_dose` from `approved_single_dose`. AI copilots are hardcoded to display historical dosages solely within an educational "Historical Context" collapsible card, never as an active dosing recommendation.
  - **Mandatory Provenance Citation**: Every AI assertion must output a structured markdown badge with an exact page anchor (`[Source: UPI Vol 1, Page 42]`). If the model fails citation grounding, the response is discarded by the output safety filter.

### 2.3 Threat 3: Botanical Identity Ambiguity & Vernacular Homonym Confusion
- **Risk Severity**: **HIGH (PATIENT TOXICITY / ADULTERATION)**
- **Clinical Manifestation**: Regional common names (e.g., *Brahmi* referring to either *Bacopa monnieri* or *Centella asiatica*; *Sankhaholi* referring to *Evolvulus alsinoides* or *Convolvulus pluricaulis*) resulting in incorrect substitution or therapeutic failure.
- **Root Cause Vulnerability**: Reliance on single text strings for herb identification without botanical taxonomy cross-referencing.
- **Architectural Mitigation**:
  - **POWO / WFO Botanical Identifier Invariant**: Every `zkb_mufradat` entry must link to an accepted Plants of the World Online (POWO) / World Flora Online (WFO) taxon ID.
  - **Canonical UPI Mapping**: Drugs must resolve to their statutory Unani Pharmacopoeia of India standard monograph before inclusion in prescriptions.

### 2.4 Threat 4: Autonomous AI Action & Prescribing (`safe_to_lock = False`)
- **Risk Severity**: **CRITICAL (UNREGULATED MEDICAL ACTION)**
- **Clinical Manifestation**: AI clinical assistant automatically issuing prescriptions, finalizing treatment regimens, or modifying patient records without human physician concurrence.
- **Root Cause Vulnerability**: Frontend components binding AI output directly to "Submit Prescription" APIs.
- **Architectural Mitigation**:
  - **Non-Delegable Human Clinical Gate**: The backend enforces `safe_to_lock = FALSE` for any AI agent. Only a verified, licensed clinician token (`CLINICIAN` role) can sign a prescription.
  - **Frontend Guardrails**: AI recommendations render exclusively as advisory differential drafts. The clinician must manually click, review, modify, and cryptographically sign each item.

---

## 3. Cybersecurity & Information Security Gaps

### 3.1 Gap 1: Multi-Tenant Data Leakage in Clinical & Proprietary Research
- **Current State**: While canonical Unani knowledge is global and shared, clinic-specific proprietary formulations (*Nuskha-e-Khas*) and patient case registries must remain strictly isolated.
- **Vulnerability**: Incomplete tenant scoping in database queries could allow Clinic A to view proprietary compounding formulations created by Clinic B.
- **Mitigation Requirement**:
  - Implement PostgreSQL Row-Level Security (RLS) on all non-canonical tables.
  - Add tenant context validation middleware on FastAPI and Next.js backend proxy layers.

### 3.2 Gap 2: Fail-Open vs. Fail-Closed Safety Firewall Vulnerability
- **Current State**: If the Knowledge Service (port 8002) experiences network partition, timeout, or Redis cache eviction, a poorly designed API gateway might bypass safety checks to maintain system availability.
- **Risk**: A clinician issues a prescription during an outage, and an active Schedule E(1) toxic overdose passes through unblocked.
- **Mitigation Requirement**:
  - **Enforce Fail-Closed Policy**: If the Clinical Safety Firewall is unreachable or fails to respond within 500 ms, the prescription compiler returns HTTP 503 (`SafetyVerificationUnavailableException`) and prevents order submission. Under no circumstances may a prescription proceed without explicit validation.

### 3.3 Gap 3: Tampering with Clinical Audit Ledgers
- **Current State**: Audit logs written as standard SQL rows can theoretically be modified or deleted by a rogue database administrator.
- **Mitigation Requirement**:
  - Chained cryptographic hashing: Each audit record stores `prev_entry_hash` and `entry_hash = SHA256(prev_hash + actor_id + payload)`.
  - Periodic external timestamping and export of audit hashes to write-once-read-many (WORM) storage.

---

## 4. Rights Management & Legal Intellectual Property Gaps

### 4.1 Gap 1: Ingestion of Copyrighted Modern Commentaries
- **Risk**: Accidental scanning and vectorization of proprietary contemporary textbooks published after 1928 without an explicit institutional license.
- **Mitigation Requirement**:
  - Strict metadata ingestion pre-check: Any work published after the statutory public domain cutoff date must have an accompanying `source_rights` record with verified license clearance signed by legal counsel before scanning or OCR extraction can commence.

---

## 5. Security & Safety Compliance Action Matrix

| Risk Code | Domain | Description | Current Status | Remediation Phase |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Clinical Safety | Schedule E(1) Mudabbar verification gate missing in DB | **CRITICAL GAP** | Phase 2 (Data Modeling) |
| **SEC-02** | AI Safety | Unapproved passages accessible to vector RAG | **CRITICAL GAP** | Phase 3 (RAG & Governance) |
| **SEC-03** | System Safety | Fail-closed policy not enforced during network failure | **HIGH GAP** | Phase 4 (Safety Firewall) |
| **SEC-04** | Identity | Botanical homonym confusion in classical vernaculars | **HIGH GAP** | Phase 2 (Mufradat Taxonomy) |
| **SEC-05** | Legal / Rights | Ingestion pipeline lacks copyright pre-clearance gate | **MEDIUM GAP** | Phase 2 (Source Library) |
| **SEC-06** | Data Privacy | Research queries lack automated de-identification | **MEDIUM GAP** | Phase 5 (Research Cloud) |

---
*Certified by:*  
**Chief Medical Safety Officer & Lead DevSecOps Architect**
