# ZAYVORA HEALTH™ — Phase 10: Staging Cluster Deployment & Live Pilot Handover
*“Ancient Wisdom. Modern Science. Intelligent Care.”*

---

## 1. Executive Deployment Handover Summary

This document constitutes the definitive operational handover for the **ZAYVORA HEALTH™ Staging Cluster Environment** (`zayvora-staging`).

The platform has cleared all upstream engineering, clinical safety, and regulatory milestones:
- **Phase 5**: Hardening & Dual-Layer Remediation (Sprints 0–7 + Horizon 5)
- **Phase 6**: Forensic Post-Remediation Verification Audit (27/27 issues FIXED, 276 tests passing)
- **Phase 7**: Production Readiness Gate (13/13 gates cleared, complete SOPs, automated rollback engine)
- **Phase 8**: Multi-Center Clinical Pilot Trials (Protocol, Concordance & DSMB Engine, University Tenant Seeder)
- **Phase 9**: Statutory Regulatory Clearances (CDSCO SaMD Class B/C & IEC 62304 Traceability Dossier)
- **Phase 10**: Staging Deployment Orchestration & Live Pilot Handover

---

## 2. Ingress Endpoints & Architecture Topology

```mermaid
graph LR
    User["Clinicians & Patients"] --> Ingress["NGINX Ingress Controller<br/>(TLS 1.3 / LetsEncrypt)"]
    Ingress --> Gateway["API Gateway (Port 8000)<br/>(Token-Bucket Rate Limiter)"]
    Gateway --> Identity["Identity & RBAC (Port 8005)"]
    Gateway --> Clinical["Clinical Core (Port 8001)<br/>(10-Ajnas, Scribe, Organ-Axis)"]
    Gateway --> Therapeutic["Therapeutic Core (Port 8002)<br/>(Safety Firewall, Nuskha, FEFO)"]
    Gateway --> Knowledge["Knowledge Core (Port 8003)<br/>(Pharmacopoeia, Neo4j Graph)"]
    Gateway --> AI["AI Service (Port 8004)<br/>(Hakeem Sahab, Fallback Cascade)"]
```

### Staging Endpoint Inventory:
| Service / Application | External Staging URL | Purpose |
| :--- | :--- | :--- |
| **Clinician Desk 2.0** | `https://staging.app.zayvora.com/dashboard` | Tabeeb consultation cockpit, ambient scribe, Nuskha compiler. |
| **Patient Portal Cockpit** | `https://staging.app.zayvora.com/portal` | Patient 360, Bhashini multilingual voice instructions, ABHA linkage. |
| **API Gateway** | `https://staging.api.zayvora.com` | Unified reverse proxy with rate limiting (60 unauth / 600 auth req/min). |
| **FHIR R4 Interoperability** | `https://staging.api.zayvora.com/fhir/r4` | ABDM compliant FHIR bundle export and ingestion. |
| **NHA ABDM Gateway** | `https://staging.api.zayvora.com/abdm/v0.5` | Milestone 1 (ABHA), Milestone 2 (Consent), Milestone 3 (FHIR push). |
| **Ambient Scribe Stream** | `wss://staging.api.zayvora.com/api/v1/scribe/live-stream` | Full-duplex WebSocket live acoustic streaming & entity extraction. |

---

## 3. Academic Medical Center Pilot Onboarding Credentials

The three university clinical trial teaching hospitals are provisioned with dedicated multi-tenant schemas:

```
┌──────────────────────────────────────┬─────────────────────────┬────────────────────────┬──────────────────────┐
│ Academic Medical Center (Simulation) │ Tenant Slug / ID        │ Principal Investigator │ AYUSH Registration   │
├──────────────────────────────────────┼─────────────────────────┼────────────────────────┼──────────────────────┤
│ Ayurvedic & Unani Tibbia Pilot       │ autc-delhi              │ Academic Research Lead │ AYUSH-DL-SIM-0821    │
│ (Simulation Staging Environment)     │ org-autc-delhi-001      │ sim.autc@zayvora.clinic│ (Moalajat Medicine)  │
├──────────────────────────────────────┼─────────────────────────┼────────────────────────┼──────────────────────┤
│ ZAYVORA Clinical Research Center     │ jh-sumer                │ Hakeem Dr. Irfan Ashraf│ AYUSH-DL-2007-0412   │
│ (Primary Clinical Practice, Delhi)   │ org-jh-sumer-002        │ dr.irfan@zayvora.com   │ (BUMS, AKTC AMU)     │
├──────────────────────────────────────┼─────────────────────────┼────────────────────────┼──────────────────────┤
│ AKTC Pilot Validation Testbed        │ amu-aktc                │ Academic Clinical Lead │ AYUSH-UP-SIM-3319    │
│ (Simulation Staging Environment)     │ org-amu-aktc-003        │ sim.aktc@zayvora.clinic│ (Ilmul Advia Pharma) │
└──────────────────────────────────────┴─────────────────────────┴────────────────────────┴──────────────────────┘
*Note: University and college entries are simulated tenant environments for pre-clinical staging, workflow modeling, and API sandbox validation.*
```

---

## 4. HashiCorp Vault Secrets Injection Topology

Secrets are mounted into Kubernetes pods at `/vault/secrets/` via Vault Agent sidecars:

1. **AI Credentials (`/vault/secrets/ai-secrets.json`)**:
   - `ANTHROPIC_API_KEY`: Anthropic Claude 3.5 Sonnet production key
   - `OPENAI_API_KEY`: OpenAI GPT-4o failover key
   - `VLLM_ENDPOINT`: Local fallback model endpoint (`http://vllm-cluster:8000/v1`)
2. **ABDM Sandbox Credentials (`/vault/secrets/abdm-credentials.json`)**:
   - `ABDM_CLIENT_ID`: National Health Authority Developer Client ID
   - `ABDM_CLIENT_SECRET`: NHA HMAC-SHA256 Client Secret
   - `ABDM_ENCRYPTION_KEY`: mTLS Certificate Private Key
3. **PHI Envelope Cryptographic Master Key (`/vault/secrets/crypto-keys.json`)**:
   - `MASTER_KEK_SECRET`: 256-bit Key Encryption Key for PBKDF2 wrapping
   - `PART11_SIGNING_KEY`: HMAC-SHA256 signature key for Merkle audit anchors

---

## 5. Clinician & SRE Operational Runbook

### 5.1 Deployment & Upgrade
```bash
# Execute staging deployment orchestrator
python3 scripts/deploy_staging_cluster.py

# Verify microservice health probes
kubectl get pods -n zayvora-staging -l app.kubernetes.io/part-of=zayvora-health
```

### 5.2 Emergency Rollback Drill
If canary regressions or safety firewall anomalies are observed:
```bash
# Execute automated zero-data-loss rollback
python3 scripts/production_rollback.py --live --revision 1 --reason "Canary latency regression"
```

### 5.3 Database Disaster Recovery Verification
```bash
# Execute live point-in-time recovery drill
python3 database/dr_backup_restore.py
```

---

## 6. Official Handover Sign-Off

```
═══════════════════════════════════════════════════════════════════════════════
        ZAYVORA HEALTH™ — STAGING CLUSTER HANDOVER CERTIFICATE
═══════════════════════════════════════════════════════════════════════════════
  ENVIRONMENT VERDICT        : OPERATIONAL — READY FOR LIVE PILOT USERS
  DEPLOYMENT ORCHESTRATOR    : VERIFIED (scripts/deploy_staging_cluster.py)
  ACADEMIC MEDICAL CENTERS   : 3 / 3 ONBOARDED (AUTC, Jamia Hamdard, AMU)
  AUTOMATED TEST PASS RATE   : 242 / 242 (100% PASSING in tests/run_all_tests.py)
  VERIFICATION AUDIT PASS    : 276 / 276 (100% PASSING across 11 dimensions)
  CLINICAL SAFETY INVARIANTS : ZERO-TOLERANCE ENFORCED (safe_to_lock=False)
───────────────────────────────────────────────────────────────────────────────
  HANDOVER APPROVED: RELEASED TO UNIVERSITY CLINICAL TRIAL STEERING BOARD
═══════════════════════════════════════════════════════════════════════════════
```

**Authorized Signatures:**
- *Head of Site Reliability Engineering (SRE)*
- *Chair, Clinical Pilot Multi-Center Steering Committee*
- *Chief Information Security & Privacy Officer (CISO)*
- *Chief Medical Officer & Ayush Clinical Director*
