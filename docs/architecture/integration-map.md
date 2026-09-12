# ZAYVORA Health OS™ — Integration Map

| Target System / Protocol | Integration Purpose | Security & Compliance |
| :--- | :--- | :--- |
| **NHA ABDM Gateway** | ABHA ID verification, Consent Artifacts, Health Data Exchange (M1-M3) | mTLS, JWT, ABDM Sandbox Certified |
| **HL7 FHIR R4** | Standardized medical record export (OPConsultRecord, PrescriptionRecord) | NRCeS StructureDefinition Profiles |
| **TRAI DLT SMS Gateway** | Statutory patient notifications, OTP verification, posology alerts | Principal Entity Reg, DLT Template Whitelist |
| **WhatsApp Business API**| Care plan delivery, appointment reminders, PROMs surveys | Meta HSM Approved Templates, TLS 1.3 |
| **Razorpay / Stripe** | Automated clinical consultation billing & payment reconciliation | HMAC-SHA256 Webhook Signatures |
| **OpenTelemetry / Prometheus**| Distributed tracing, service latencies, safety tripwire monitoring| W3C Trace Context Propagation |
| **Bhashini TTS / Audio** | Vernacular regional language audio synthesis for patient medication | WAV PCM Audio, Regional Linguistic Localization |
