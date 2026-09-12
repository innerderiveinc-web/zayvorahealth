# ZAYVORA Health OS™ — Known Limitations & Operational Boundaries

## Documented Operational Boundaries
1. **Classical Text Scope:** The canonical pharmacopoeia currently indexes official monographs from UPI Parts I & II and NFUM Parts I-VI. Rare folk Unani formulations not codified in AYUSH official literature require manual formulation review by the Clinical Governance Board.
2. **Sandbox Child Process Networking:** In local sandboxed developer environments, outgoing TCP connections to external sandboxes require bypass sandbox approval or offline test mock fixtures. All test suites incorporate high-fidelity local fixtures that validate the complete business logic offline.
3. **Telemedicine Audio Hardware:** In web preview environments, microphone audio capture relies on Web Audio API permissions granted by the client browser.
