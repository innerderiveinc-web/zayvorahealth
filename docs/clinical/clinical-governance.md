# ZAYVORA Health OS™ — Clinical Governance Framework

## 1. Statutory Mandate & Philosophy
The ZAYVORA Health OS™ operates under strict adherence to the National Commission for Indian System of Medicine (NCISM) Act 2020, the Drugs and Cosmetics Act 1940 (specifically §33EEC and Schedule E(1)), and the AYUSH Telemedicine Practice Guidelines.

## 2. The Non-Delegable Prescribing Barrier
- **Statutory Rule:** Clinical diagnosis, medical treatment selection, and prescription locking are strictly non-delegable professional acts reserved exclusively for qualified, registered medical practitioners (`ROLE_SENIOR_TABEEB`).
- **AI Invariant:** Artificial intelligence models, algorithms, and copilot modules are classified as Clinical Decision Support (CDS) tools. Under no circumstance can an AI output autonomously lock a prescription or create an active dispensing order.
- **Architectural Safeguard:** All AI-synthesized consultation notes and nuskha drafts are initialized with `safe_to_lock = False`. Any attempt by an unauthenticated or non-practitioner actor to lock a prescription triggers a statutory RBAC refusal (`403 Forbidden`).

## 3. Quorum Requirements for Formulary Revision
- Any modification to the approved UPI Mufradat register, NFUM compound formulations, Schedule E(1) dosage ceilings, or evidence grading levels requires a minimum 2-of-3 (or 3-of-3 for Schedule E1) Clinical Governance Board quorum.
- Attestations are cryptographically recorded with HMAC-SHA256 digital seals in an immutable governance ledger.
