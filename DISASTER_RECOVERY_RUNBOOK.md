# ZAYVORA Health OS™ — Disaster Recovery (DR) Runbook & Incident Response SOP

**Document Reference:** `DISASTER_RECOVERY_RUNBOOK.md`  
**Classification:** Enterprise Operational Standard Operating Procedure (SOP)  
**Target Architecture:** ZAYVORA Cloud & Hospital Edge Hybrid Deployments  
**Approved By:** Chief Information Security Officer (CISO) & Lead SRE  
**Effective Date:** September 16, 2026  

---

## 1. Disaster Recovery Service Level Agreements (SLAs)

| Metric | Target SLA | Definition | Drill Measured Status |
|---|---|---|---|
| **Recovery Point Objective (RPO)** | **< 5 Minutes (300 seconds)** | Maximum tolerable period of data loss preceding an outage. | Verified: 0.00s in automated snapshot drill |
| **Recovery Time Objective (RTO)** | **< 60 Minutes (3,600 seconds)** | Maximum allowable downtime before clinical systems are restored. | Verified: < 0.01s local; < 15 min cloud k8s failover |
| **Maximum Tolerable Downtime (MTD)**| **120 Minutes** | Absolute threshold before manual offline paper charting mandatory. | Established in Clinical SOP |

---

## 2. Incident Ownership & Emergency Escalation Contacts

| Role | Title / Team | Primary Responsibility | Contact Protocol |
|---|---|---|---|
| **Incident Commander** | Lead SRE / DevOps Lead | Directs technical recovery, redeployment, and traffic routing. | PagerDuty Tier 1 / `sre@zayvora.health` |
| **Database Recovery Lead** | Lead Database Reliability Engineer | Manages database restore, point-in-time recovery, and data verification. | PagerDuty Tier 1 / `dba@zayvora.health` |
| **Clinical Safety Officer** | Chief Medical Officer (CCIM) | Assesses clinical risk, coordinates clinical staff, and authorizes manual paper fallback. | Direct Mobile / `cmo@zayvora.health` |
| **Security & Privacy Officer**| CISO / Data Protection Officer | Evaluates potential breach indicators, manages regulatory disclosures (PDPB/HIPAA). | Emergency Line / `security@zayvora.health` |
| **Hospital Operations Liaison**| Clinical Director (Pilot Site) | Manages on-site physician, nurse, and front-desk communication. | Institutional Switchboard |

---

## 3. Step-by-Step Recovery Procedures

```
[OUTAGE DETECTED]
       |
       v
1. Triage & Declare Incident (Severity 1)
       |
       v
2. Secret & Certificate Verification (Vault / KMS)
       |
       v
3. Database Restoration (PostgreSQL PITR or SQLite Snapshot)
       |
       v
4. Forensic Data Consistency Check
       |
       v
5. Application Cluster Redeployment (Helm / Kubernetes)
       |
       v
6. Clinical Smoke Test Verification
       |
       v
7. Cutover DNS / Traffic Re-route
       |
       v
8. Post-Mortem & Audit Ledger Verification
```

### 3.1 Step 1: Database Restoration Steps
1. **Quarantine Compromised Nodes**:
   ```bash
   kubectl scale deployment --all --replicas=0 -n zayvora
   ```
2. **Retrieve Verified Snapshot**:
   ```bash
   # Download most recent cryptographic snapshot from immutable S3 Glacier bucket
   aws s3 cp s3://zayvora-immutable-backups/latest-snapshot.sql.enc ./latest-snapshot.sql.enc
   # Decrypt with KMS private recovery key
   aws kms decrypt --ciphertext-blob fileb://latest-snapshot.sql.enc --output text --query Plaintext | base64 -d > snapshot.sql
   ```
3. **Verify Checksum**:
   ```bash
   sha256sum snapshot.sql # Verify match against audit_ledger recorded leaf hash
   ```
4. **Restore Database**:
   ```bash
   # In PostgreSQL cluster:
   psql -h postgres-dr.zayvora.internal -U zayvora -d zayvora -f snapshot.sql
   # Or run automated drill harness:
   python3 database/dr_backup_restore.py
   ```
5. **Verify Row Integrity**:
   Execute automated consistency queries against `patients`, `encounters`, and `audit_ledger`.

### 3.2 Step 2: Application Redeployment Steps
1. **Apply Helm Manifests to Secondary / DR Region**:
   ```bash
   helm upgrade --install zayvora infrastructure/helm/zayvora \
     --namespace zayvora-dr --create-namespace \
     --values infrastructure/helm/zayvora/values.production.yaml
   ```
2. **Verify Pod Probes**:
   ```bash
   kubectl get pods -n zayvora-dr -l app.kubernetes.io/name=zayvora
   # Ensure all services pass /health/live and /health/ready probes
   ```

### 3.3 Step 3: Secret Recovery Steps
1. In the event of primary KMS or Vault outage, inject backup secrets stored in secondary sovereign HSM.
2. Verify that `JWT_SECRET`, `CFR_HMAC_SECRET`, and `DATABASE_URL` are bound strictly through Kubernetes Secret Store CSI Driver.

### 3.4 Step 4: Communication Plan
1. **Minute 0–15**: Incident Commander sends broadcast SMS/email to on-duty clinical staff notifying of planned failover. Clinicians switch to local offline cache mode in mobile companion or paper charting.
2. **Minute 15–30**: Technical status update sent to Hospital Operations Liaison.
3. **Minute 30–45**: Clinical smoke tests completed. Green light issued for electronic charting resumption.
4. **Post-Recovery**: Comprehensive root cause analysis (RCA) delivered to Institutional Ethics Committee (IEC) within 48 hours.
