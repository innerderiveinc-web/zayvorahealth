# ZAYVORA Health OS™ — Production Risk Register

| Risk ID | Category | Risk Description | Severity | Mitigation Strategy | Residual Risk | Status |
|---|---|---|---|---|---|---|
| **RSK-01** | Clinical Safety | AI autonomous diagnostic or prescribing hallucination | Critical | Hardcoded `safe_to_lock = False`; clinician signature mandatory | LOW | **MITIGATED** |
| **RSK-02** | Toxicity | Dispensing toxic Schedule E(1) botanicals without purification | High | Enforced Mudabbar certificate hash validation before lot release | LOW | **MITIGATED** |
| **RSK-03** | Data Privacy | Cross-tenant patient PHR leakage | Critical | Organization-level tenant scoping and RBAC permission checks | LOW | **MITIGATED** |
| **RSK-04** | Expiry Loss | Dispensing expired or degraded herbal extracts | Medium | Automated FEFO lot allocation prioritizing earliest expiry date | LOW | **MITIGATED** |
| **RSK-05** | Audit Tampering | Unauthorized alteration of locked clinical notes | High | SHA-256 Merkle root chaining with tamper-evident audit ledger | LOW | **MITIGATED** |
| **RSK-06** | Emergency Risk | Delay in emergency hospital transfer for acute chest pain/stroke | Critical | Deterministic Safety Firewall halts outpatient consultation and triggers immediate Code Red | LOW | **MITIGATED** |
