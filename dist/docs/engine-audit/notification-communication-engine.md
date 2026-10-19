# ZAYVORA HEALTH OS™ — CLINICAL ENGINE AUDIT
## QSURA™ Communication & Notification Engine (`ENG-28-QSURA-BROKER`)

**Document Classification**: Statutory Clinical & Architectural Audit Report  
**Implementation Source File**: [`services/clinical/app/qsura/communication_broker.py`](file:////Users/irfanashraf/Downloads/zayvora-platform-phase0-4/services/clinical/app/qsura/communication_broker.py)  
**Hosting Microservice**: `services/clinical`  
**Verification Status**: VERIFIED AND TESTED (100% Pass Rate)

---

### 1. What It Does
Brokers automated, privacy-preserving patient communications across SMS, WhatsApp, and Email, enforcing TRAI DLT PHI masking and mandatory DISHA/GDPR consent validation.

### 2. What Data It Accepts
Channel (sms/whatsapp/email), recipient contact, approved template ID, parameters, consent verification flag.

### 3. What Data It Uses
Pre-approved HSM/DLT template catalog (MESSAGE_TEMPLATES), notifications table in zayvora_live.db.

### 4. What Rules It Applies
Mandates patient consent (patient_consent_verified: true); masks 10-12 digit phone numbers on unencrypted SMS; validates all required template parameters.

### 5. What Knowledge It Retrieves
TRAI DLT Messaging Framework, DISHA / HIPAA Privacy Guidelines.

### 6. What Model It Uses (If Any)
Deterministic template compilation and multi-channel transport dispatcher.

### 7. What Output It Produces
Dispatch record JSON with message ID, rendered content, delivery status, and compliance certificate.

### 8. What Safety Checks Exist
Hard rejection of unverified patient consent (HTTP 400 CONSENT_REQUIRED); prevents unencrypted PHI leakage.

### 9. What Happens When Data Is Missing
Rejects dispatch with HTTP 400 (MISSING_TEMPLATE_PARAMS) if any parameter is omitted.

### 10. What Happens When Confidence Is Low
Not applicable — exact template compilation.

### 11. What Happens When Evidence Is Unavailable
Not applicable.

### 12. What Happens When a Contraindication Is Detected
Automatically appends statutory Mudabbar warning for Schedule E(1) prescription alerts.

### 13. What Is Stored in the Database
Persisted in 'notifications' table in zayvora_live.db.

### 14. What Is Recorded in the Audit Log
All dispatch events logged with timestamp and recipient token.

### 15. Which Tests Passed
test_45_engines_connected.py (Engine 31), test_phase6_qsura_telemed_vernacular.py (Tests 01, 02, 03, 04, 05, 06, 07).

### 16. Which Tests Failed
Zero failures.

### 17. Whether Clinician Approval Is Required
Yes — Clinical notifications triggered only by authorized clinical workflows.

---
*Certified under ZAYVORA Health OS Clinical Safety & Software Verification Protocol v5.0*
