# ZAYVORA HEALTH™ — Enterprise Policy: Statutory Prescription Lock (safe_to_lock = False)
*Master Directive §78.1 — Clinical Authority & Algorithmic Liability Boundary*

---

## 1. Policy Statement & Foundational Invariant

Under no circumstances may any algorithmic model, copilot, automated compiler, or ambient listening scribe finalize, sign, lock, or dispense a prescription or clinical care plan autonomously.

> **MANDATORY ARCHITECTURAL DIRECTIVE**:  
> Every Nuskha prescription, care plan, SOAP consultation note, and clinical decision recommendation generated within the ZAYVORA platform must initialize with:  
> `safe_to_lock = False`  
> and `requires_clinician_signoff = True`.

This flag may only be mutated to `safe_to_lock = True` through the authenticated, deliberate, and cryptographically verified digital signature of a registered, licensed healthcare clinician.

---

## 2. Rationale & Regulatory Compliance

1. **AYUSH / CDSCO Statutory Medical Law**: Indian law stipulates that medical diagnosis and prescription of scheduled botanical/mineral drugs are exclusively within the statutory competence of licensed practitioners registered under state medical councils or the National Commission for Indian System of Medicine (NCISM).
2. **AI Liability & Risk Mitigation**: LLMs and algorithmic predictors are assistive cognitive copilots (*Mu'allim-e-Saree'a*), not medical professionals. They lack physical sensory examination faculties (*Mu'ayana*) and cannot assume legal, ethical, or criminal liability for patient outcomes.
3. **Defense-in-Depth Safety Architecture**: Even if an AI model generates a pharmacologically sound suggestion, it must undergo deterministic Safety Firewall validation (Schedule E(1) verification, renal eGFR posology scaling, herb-drug interaction checks) before presentation to the clinician for final authorization.

---

## 3. Enforcement Mechanisms Across Microservices

- **Clinical Service (`services/clinical`)**:
  - `POST /api/v1/prescriptions` rejects any payload where `safe_to_lock` is passed as `True` without a valid clinician cryptographic signature token.
- **Therapeutic Service (`services/therapeutic`)**:
  - `POST /api/v1/compiler/compile` outputs compiled formulations with `is_provisional = True` and `safe_to_lock = False`.
- **AI Service (`services/ai`)**:
  - Response validator inspects LLM output; any response failing to include Section 13 (`CLINICIAN REVIEW REQUIRED`) is marked `is_valid = False` and quarantined.
  - Prompt guardrails block any prompt injection attempting to set `safe_to_lock = True` or bypass clinician review.
- **Dispensary & Pharmacy OS (`services/therapeutic/dispensary`)**:
  - FEFO dispensing engine checks the prescription's digital signature; prescriptions with `safe_to_lock == False` trigger a hard `UnsignedPrescriptionDispenseBlock` exception.

---

## 4. Penalties for Tampering

Any attempt to bypass, spoof, or circumvent the `safe_to_lock = False` invariant triggers an immediate `SECURITY_CRITICAL` audit event in the 21 CFR Part 11 Merkle-chained audit ledger, revokes the offending session token, and alerts the Chief Information Security Officer (CISO).
