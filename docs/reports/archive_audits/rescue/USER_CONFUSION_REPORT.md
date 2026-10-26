# ZAYVORA Health OS™ — User Confusion & Friction Report

## 1. Specific Friction Points Identified

### A. Terminology Barriers
- **"25-Engine Matrix"**: Non-technical users assumed this was a car diagnostic panel or backend developer tool.
- **"safe_to_lock = False"**: Clinicians interpreted this as a software bug or crash rather than an intentional non-delegable prescribing safeguard.
- **"Deterministic Safety Firewall"**: Patients felt alarmed by the word "Firewall", associating it with computer viruses rather than medication contraindication checks.
- **"SHA-256 Merkle Leaf"**: Doctors did not know what to do with a 64-character hexadecimal hash during consultation.

### B. Navigation & Information Architecture Friction
- **No Guided Journey**: Users were dropped onto an unguided tab interface with no indication of priority or task flow.
- **Scattered Clinical Tools**: A doctor had to open the Scribe tool, then switch tabs to Mizaj, then switch tabs to Safety, then switch tabs to Prescriptions.
- **Hidden Confirmation**: When an action was completed, confirmation appeared in raw JSON or subtle text without a human-readable summary.

---

## 2. Terminology Replacement Dictionary

| Raw Engineering Term | Confusing Location | Approved Healthcare Term | Target User View |
|---|---|---|---|
| `safe_to_lock = False` | Doctor Prescription | "Pending Doctor Review & Signature" | Doctor / Pharmacy |
| `Deterministic Safety Firewall` | Clinical Screen | "Medication Safety & Interaction Review" | Doctor / Patient |
| `25-Engine Matrix` | Main Navigation | Relegated to Platform Admin IT Console | Platform Admin Only |
| `SHA-256 Merkle Leaf Hash` | Prescription Box | "Digital Signature Verified (21 CFR Part 11)" | Doctor / Pharmacy |
| `Acoustic Urdu Scribe` | Consultation Tab | "Consultation Voice Notes" | Doctor |
| `eBMR Batch Release` | Main Navigation | "Manufacturing Quality Control" | Manufacturing Only |
| `P95 Latency 1.2ms` | Safety Card | "Safety Verification Completed Instantly" | Hidden / Admin |
