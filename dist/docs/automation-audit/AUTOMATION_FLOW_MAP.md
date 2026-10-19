# ZAYVORA HEALTH™ — Master Automation & Workflow Flow Map
**Classification:** Enterprise Forensic Automation Architecture  
**System Baseline:** Commit `6d37cd7` | Phase 0–10 Consolidated Repository  
**Audit Standard:** GAMP 5 / 21 CFR Part 11 / ISO 27001 / IEC 62304 / DISHA / AYUSH Schedule T  
**Date:** September 12, 2026  
**Auditor:** Autonomous Systems & Clinical Automation Auditing Desk  

---

## Executive Overview

This document provides architectural sequence, state, and pipeline flowcharts for all operational automation systems in ZAYVORA HEALTH™. Every diagram illustrates the exact lifecycle:  
$$\text{Trigger} \longrightarrow \text{Authentication / Gate} \longrightarrow \text{Execution Broker} \longrightarrow \text{Database / State Mutation} \longrightarrow \text{External API / Transport} \longrightarrow \text{Failure / Retry Path}$$

---

## 1. Multi-Tenant Asynchronous Task Queue & Worker Daemon Architecture

```mermaid
sequenceDiagram
    autonumber
    actor Clinician as Authenticated User / System
    participant Gateway as Ingress API Gateway
    participant Router as Tasks Router (/api/v1/tasks)
    participant Broker as AsyncTaskQueue
    participant Redis as Redis Cluster (zayvora:task_queue)
    participant MemQueue as In-Memory Fallback Queue
    participant Worker as WorkerDaemon Loop
    participant Handler as Task Type Handler

    Clinician->>Gateway: POST /api/v1/tasks/enqueue
    Gateway->>Router: Forward with Verified JWT Context
    Router->>Broker: enqueue(task_type, org_id, payload)
    
    alt Redis Connected
        Broker->>Redis: LPUSH zayvora:task_queue (task_id)
        Broker->>Redis: SET zayvora:task:<id> (JSON TaskRecord)
    else Redis Offline / Fallback
        Broker->>MemQueue: put(task_id) [Thread-Safe Lock]
    end
    
    Broker-->>Router: TaskRecord(status=PENDING, safe_to_lock=False)
    Router-->>Clinician: 200 OK (task_id, status=PENDING)
    
    loop Continuous Processing
        Worker->>Broker: dequeue(timeout_seconds=0.1)
        alt Redis Active
            Broker->>Redis: BRPOP zayvora:task_queue
        else In-Memory
            Broker->>MemQueue: get()
        end
        Broker-->>Worker: TaskRecord(status=PROCESSING)
        
        Worker->>Handler: Execute Registered Handler(task)
        alt Handler Success
            Handler-->>Worker: Result dict (safe_to_lock=False)
            Worker->>Broker: complete_task(task_id, result)
        else Transient Error (retry_count <= max_retries)
            Worker->>Broker: fail_task(task_id, error)
            Broker->>Broker: status=RETRYING, retry_count++
            Broker->>Redis: Re-enqueue into task queue
        else Terminal Failure (retry_count > max_retries)
            Worker->>Broker: fail_task(task_id, error)
            Broker->>Broker: status=FAILED, completed_at=now()
        end
    end
```

---

## 2. ABDM Milestone 3 Inbound Webhook, Packet Reconciliation & Dual-Coding Workflow

```mermaid
flowchart TD
    A["Inbound ABDM Transfer Webhook<br/><code>/api/v1/tasks/interop/abdm/data-flow/transfer</code>"] --> B{"Validate ABDM Signature<br/>& ABHA ID"}
    B -- "Invalid" --> C["HTTP 400 / 401 Rejection"]
    B -- "Valid" --> D["Enqueue Task:<br/><code>abdm_packet_reconciliation</code>"]
    
    D --> E["AsyncTaskQueue<br/>(status=PENDING, safe_to_lock=False)"]
    E --> F["WorkerDaemon Dequeue"]
    
    F --> G["Parse Encrypted FHIR Packets<br/>(Conditions, Observations, Medications)"]
    
    G --> H["Dual-Coding Engine:<br/>Map ICD-11 to Classical Unani Amraz<br/>(E11->Ziabetus, M10->Niqras, I10->Zaghtuddam)"]
    G --> I["Schedule E(1) Statutory Poison Scanner<br/>(Suranjan, Kuchla, Suranjan, Bhilawa)"]
    G --> J["LOINC Observation Harmonizer"]
    
    H --> K["Synthesize Reconciled Clinical Record"]
    I --> K
    J --> K
    
    K --> L{"Statutory Invariant Gate"}
    L --> M["Enforce <b>safe_to_lock = False</b><br/>(Autonomous locking strictly prohibited)"]
    M --> N["Require Physical Clinician Ratification<br/>(requires_clinician_ratification = True)"]
    
    N --> O["Commit Reconciled Timeline & Notes<br/>to Database"]
    O --> P["Mark Task COMPLETED"]
```

---

## 3. Continuous Wearable Telemetry Webhook Ingestion & Humoral Drift Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Device as Wearable Hardware (Apple Watch / Android Wear)
    participant Webhook as Wearable Webhook Endpoint
    participant Engine as WearableIngestionEngine
    participant DB as PostgreSQL / TimescaleDB
    participant Telemetry as Clinical Telemetry / Alertmanager

    Device->>Webhook: POST /api/v1/wearables/webhooks/apple-healthkit<br/>or /google-health-connect
    Webhook->>Engine: normalize_apple_healthkit() / normalize_google_health_connect()
    
    Note over Engine: Normalize HKQuantity / Health Connect records:<br/>HRV RMSSD, Resting HR, SpO2, Sleep Stages
    
    Engine->>Engine: Compute Unani Autonomic Tone:<br/>Quwwat-e-Hayawaniyyah Index (0.1 - 1.0)
    Engine->>Engine: Compute Sleep Harmony:<br/>Naum-o-Yaqzah Score (Deep sleep / 90m)
    Engine->>Engine: Detect Humoral Drift (Tahawwul-e-Mizaj):<br/>Haar Yabis (HR>90 & HRV<25) vs Barid (HR<55 & Sleep<30)
    
    Engine->>DB: Persist WearableSample & Update 7-Day Rolling Summary
    
    alt Humoral Drift Detected
        Engine->>Telemetry: Record Clinical Safety Alert (Tahawwul-e-Mizaj Warning)
        Telemetry-->>Device: Dispatch Preventive Parhez / Lifestyle Advisory
    end
    
    Engine-->>Webhook: 200 OK (sample_id, summary, autonomic_reserves)
    Webhook-->>Device: HTTP 200 PROCESSED
```

---

## 4. QSURA Multi-Channel Clinical Communication Pipeline

```mermaid
flowchart TD
    A["Trigger: Appointment / Dispense / Safety Alert / PROMs"] --> B["QSURACommunicationBroker.send_notification()"]
    
    B --> C{"Check Patient Consent<br/>(DISHA / GDPR Verification)"}
    C -- "Not Verified" --> D["Raise PermissionError<br/>(Consent Violation Block)"]
    
    C -- "Verified" --> E{"Channel Approved for<br/>Message Template?"}
    E -- "No" --> F["Raise ValueError<br/>(Unapproved Channel)"]
    
    E -- "Yes" --> G["Validate Required HSM / DLT Template Parameters"]
    G --> H["Render Message Content"]
    
    H --> I{"Channel Type"}
    
    I -- "SMS" --> J["Apply Zero-PHI Masking<br/>(Regex Mask Recipient & Numbers)"]
    J --> K["Dispatch to TRAI DLT SMS Gateway"]
    
    I -- "WhatsApp" --> L["Format Meta Cloud API JSON Payload"]
    L --> M["Dispatch to https://graph.facebook.com/v19.0"]
    
    I -- "Email / Webhook" --> N["Dispatch Secure Transport"]
    
    K --> O{"External API Status"}
    M --> O
    N --> O
    
    O -- "HTTP 200 / 201" --> P["Set delivery_status = DELIVERED"]
    O -- "Network Timeout / Error" --> Q["Set delivery_status = QUEUED_RETRY<br/>(Fallback to asynchronous queue retry)"]
    
    P --> R["Persist QSURADispatchRecord to Database"]
    Q --> R
    R --> S["Return Dispatch Ledger Summary"]
```

---

## 5. Dispensary FEFO Automated Inventory Allocation & Mudabbar Safety Gate

```mermaid
flowchart TD
    A["Clinician Prescribes Medication<br/>(Dispense Request Received)"] --> B["DispensaryEngine: allocate_fefo_batches()"]
    
    B --> C["Query Released Batches with Row-Lock<br/>(SELECT ... FOR UPDATE)"]
    
    C --> D{"Filter: Quality Release Status<br/>(qc_release_status == 'released')"}
    D -- "Not Released" --> D1["Exclude Batch"]
    D -- "Released" --> E{"Filter: Expiry Date<br/>(expiry_date > today)"}
    
    E -- "Expired" --> E1["Exclude Batch (Prevent Expired Drug Release)"]
    E -- "Valid Shelf Life" --> F{"Is Medication Schedule E(1)<br/>Statutory Poison?"}
    
    F -- "Yes" --> G{"Is Batch Mudabbar Certified?<br/>(mudabbar_certified == True)"}
    G -- "No Certificate" --> G1["Strict Exclusion of Unpurified Toxic Batch"]
    G -- "Certified" --> H["Include in Eligible Allocation Pool"]
    
    F -- "No" --> H
    
    H --> I{"Are Eligible Batches Available?"}
    I -- "No (Schedule E1 Uncertified)" --> J["<b>RAISE MudabbarDispenseBlockError</b><br/>(Statutory Dispense Gate Blocked)"]
    J --> J1["Increment Prometheus Alert:<br/><code>zayvora_mudabbar_dispense_violations_total</code>"]
    
    I -- "Yes" --> K["Sort Eligible Batches Ascending by Expiry Date<br/>(First-Expired, First-Out Priority)"]
    
    K --> L["Greedily Deduct Requested Quantity Across Lots"]
    L --> M["Update Batch Available Quantities in Database"]
    M --> N["Generate Immutable DispenseRecord Entries"]
    N --> O["Commit Transaction & Return Allocation Summary"]
```

---

## 6. Manufacturing OS Electronic Batch Manufacturing Record (eBMR) Workflow

```mermaid
stateDiagram-v2
    [*] --> STAGED: Operator Initializes Session (MFR Selected)
    
    STAGED --> IN_PROCESS: Raw Drug Sifting & Inspection (Step 1 Hold Point Signed)
    
    state IN_PROCESS {
        [*] --> MudabbarCheck
        MudabbarCheck --> MudabbarDetox: Contains Schedule E(1) Botanical
        MudabbarDetox --> StageSigned: Valid Mudabbar Certificate Attached
        MudabbarDetox --> Blocked: No Mudabbar Certificate
        MudabbarCheck --> StandardCompounding: Non-Toxic Formulation
        StandardCompounding --> StageSigned: Hold Points Electronically Signed
    }
    
    IN_PROCESS --> IPQC_TESTING: Compounding Complete, Submit Lab Samples
    
    state IPQC_TESTING {
        [*] --> AssayValidation
        AssayValidation --> Refractometer: Brix Refraction (°Bx Target: 68-74)
        AssayValidation --> pHCheck: Acidity / Alkalinity (pH Target: 4.5-6.0)
        AssayValidation --> HeavyMetals: Lead (Pb < 10ppm), Arsenic (As < 3ppm)
        AssayValidation --> Microbial: Total Bacterial Count (< 10000 CFU/g)
    }
    
    IPQC_TESTING --> RELEASED: All Hold Points Signed + Mudabbar Verified + IPQC Passed + QA Director Sign-off
    IPQC_TESTING --> REJECTED: Any IPQC Assay Out of Spec or Missing Mudabbar Detox
    
    RELEASED --> [*]: Generate Certified Certificate of Analysis (CoA)
    REJECTED --> [*]: Quarantine Batch & Emit GMP Deviation Report
```

---

## 7. Multi-Tier AI Provider Chained Fallback Cascade

```mermaid
sequenceDiagram
    autonumber
    actor Clinician as Treating Clinician
    participant Copilot as Hakeem Sahab Copilot Engine
    participant Router as ChainedFallbackRouter
    participant Claude as Tier 1: Anthropic Claude 3.5 Sonnet
    participant GPT as Tier 2: OpenAI GPT-4o
    participant vLLM as Tier 3: Local Self-Hosted vLLM
    participant Local as Tier 4: Deterministic Unani Knowledge Engine

    Clinician->>Copilot: Clinical Inquiry / Diagnostic Consultation
    Copilot->>Router: generate(system_prompt, user_prompt)
    
    critical Primary Cloud Provider
        Router->>Claude: POST /v1/messages (system, user)
        Claude--xRouter: 503 Service Unavailable / Rate Limit Exceeded
    end
    
    Note over Router: Catch Exception; Log Degradation:<br/>"AI Provider 'Claude' failed. Failing over."
    
    critical Secondary Cloud Provider
        Router->>GPT: POST /v1/chat/completions
        GPT--xRouter: Connection Timeout / Network Partition
    end
    
    Note over Router: Catch Exception; Log Degradation:<br/>"AI Provider 'GPT-4o' failed. Failing over."
    
    critical Local Air-Gapped Cluster
        Router->>vLLM: POST http://ai-inference:8000/v1/completions
        vLLM-->>Router: HTTP 200 Success (Generated Completion)
    end
    
    Router->>Router: Set last_used_provider_name = "Local vLLM"
    Router-->>Copilot: Return Verified Clinical Recommendation
    Copilot-->>Clinician: Render Verified Response (with Fallback Watermark)
```

---

## 8. 21 CFR Part 11 Cryptographic Merkle Root Anchoring Workflow

```mermaid
flowchart TD
    A["Continuous Append-Only Audit Ledger Blocks<br/>(Block 0 ... Block N)"] --> B["Periodic Sealing Trigger / Command"]
    
    B --> C["AuditTrailEngine: generate_merkle_anchor()"]
    C --> D["Extract Block Hashes for Range<br/>[last_anchored_index + 1 : len(chain) - 1]"]
    
    D --> E["Construct Binary Merkle Tree:<br/>Compute SHA-256 Hashes of Leaf Pairs"]
    E --> F["Iterate Tree Levels Until Single Root Hash Obtained:<br/><b>merkle_root = H(H_L + H_R)</b>"]
    
    F --> G["Fetch Previous Anchor Hash<br/>(Cryptographic Chaining)"]
    G --> H["Assemble Raw Anchor Payload:<br/><code>anchor_id : start : end : merkle_root : prev_hash : timestamp</code>"]
    
    H --> I["Compute SHA-256 Anchor Hash"]
    H --> J["Generate HMAC-SHA256 Digital Signature Seal<br/>using SIGNING_SECRET_KEY"]
    
    I --> K["Create AuditAnchor Record"]
    J --> K
    
    K --> L["Append Anchor to Ledger & Update last_anchored_index"]
    L --> M["verify_anchor_integrity():<br/>Continuous Mathematical Tamper-Evidence Verification"]
```

---

## 9. Database Disaster Recovery (PITR) Backup & Verification Drill Flow

```mermaid
sequenceDiagram
    autonumber
    participant Scheduler as System DR Scheduler / CLI
    participant Drill as DatabaseDisasterRecoveryDrill
    participant ProdDB as Active Production Database
    participant SnapshotDir as Secure Backup Storage (/backups)
    participant Sandbox as Isolated Verification Sandbox DB

    Scheduler->>Drill: run_backup_drill()
    Note over Drill: Record start_time (T_0)
    
    Drill->>ProdDB: Execute Point-in-Time Database Snapshot
    ProdDB->>SnapshotDir: Write SNAP-<uuid>.db
    
    Drill->>Drill: Compute SHA-256 Checksum of ProdDB
    Drill->>Drill: Compute SHA-256 Checksum of Snapshot
    Note over Drill: Assert Source Checksum == Snapshot Checksum
    
    Drill->>ProdDB: Query Source Row Counts (Orgs, Patients, Prescriptions)
    
    Drill->>Sandbox: Restore Snapshot File into Sandbox (RESTORED_SNAP-<uuid>.db)
    Drill->>Drill: Compute SHA-256 Checksum of Restored Sandbox DB
    Note over Drill: Assert Snapshot Checksum == Restored Checksum
    
    Drill->>Sandbox: Forensic Data Verification Query:<br/>Count Organizations, Patients, Prescriptions
    Note over Drill: Assert Restored Counts == Source Counts
    
    Drill->>Sandbox: Audit Clinical Invariant Integrity:<br/>SELECT COUNT(*) WHERE status='active' AND safe_to_lock=0
    Note over Drill: Assert Zero Invariant Violations
    
    Drill->>Drill: Compute Metrics:<br/>RTO = Elapsed Time (0.0079s) [< 3600s COMPLIANT]<br/>RPO = WAL Archival Lag (12s) [< 300s COMPLIANT]
    
    Drill->>Sandbox: Clean Up Sandbox Drill Files
    Drill-->>Scheduler: Emit BACKUP_AND_RESTORE_DRILL_PASSED Certificate
```

---

## 10. Automated Production Release Rollback Orchestration

```mermaid
flowchart TD
    A["Alarm / Incident: Canary Regression Detected"] --> B["ProductionRollbackOrchestrator.execute_live_rollback()"]
    
    B --> C["Step 1: Precondition & Dependency Dry-Run Validation"]
    C --> C1["Verify Alembic Config Paths (clinical, therapeutic, identity, ai)"]
    C --> C2["Validate Kubernetes Helm Chart Directory"]
    C --> C3["Validate Disaster Recovery Script Availability"]
    
    C1 --> D{"Preconditions Valid?"}
    C2 --> D
    C3 --> D
    
    D -- "Failed" --> E["ABORT Rollback & Raise FileNotFoundError"]
    D -- "Passed" --> F["Step 2: Circuit Breaker: Freeze Inbound Gateway Traffic"]
    
    F --> G["Step 3: Helm Release Rollback:<br/><code>helm rollback zayvora <target_revision></code>"]
    
    G --> H{"Schema Downgrade Required?<br/>(downgrade_db == True)"}
    H -- "Yes" --> I["Revert Database Schema Migrations Safely:<br/><code>python3 database/migrations/migrate.py downgrade</code>"]
    H -- "No" --> J["Preserve Database Schema"]
    
    I --> K["Step 4: Execute Automated Sandbox DR Verification Drill:<br/><code>python3 database/dr_backup_restore.py</code>"]
    J --> K
    
    K --> L["Step 5: Run Comprehensive System Verification Audit:<br/><code>python3 tests/run_comprehensive_verification_audit.py</code>"]
    
    L --> M{"All 281 Tests Passed?"}
    M -- "No" --> N["Escalate to Clinical Emergency Response Team"]
    M -- "Yes" --> O["Step 6: Resume Inbound Traffic & Notify Safety Board"]
    
    O --> P["Emit 21 CFR Part 11 Rollback Audit Certificate"]
```

---

## 9. Inbound Payment Gateway Webhook Settlement Flow (AUTO-09)

```mermaid
sequenceDiagram
    autonumber
    actor Gateway as Payment Provider (Razorpay / Stripe)
    participant Router as Payments Router (/api/v1/payments/webhooks/*)
    participant Engine as PaymentGatewayEngine
    participant Cache as Idempotency Cache / DB
    participant DB as PostgreSQL Database
    participant QSURA as QSURA Patient Notification

    Gateway->>Router: POST /webhooks/{provider} with HMAC Signature
    Router->>Engine: process_webhook(provider, payload, signature)
    
    rect rgb(240, 240, 255)
        Note over Engine: Cryptographic Signature Verification
        Engine->>Engine: Compute HMAC-SHA256(payload, secret)
        alt Signature Mismatch
            Engine-->>Router: 400 Bad Request (PaymentSignatureVerificationError)
            Router-->>Gateway: 400 Bad Request (Rejected)
        end
    end

    rect rgb(240, 255, 240)
        Note over Engine, Cache: Idempotency Protection
        Engine->>Cache: Check event_id / payment_id
        alt Already Processed
            Cache-->>Engine: Cached Settlement Record
            Engine-->>Router: 200 OK (ALREADY_PROCESSED)
            Router-->>Gateway: 200 OK (Duplicate Acknowledged)
        end
    end

    Engine->>DB: Update PaymentTransaction & InvoiceRecord status -> SETTLED
    Engine->>DB: Unlock Pharmacy Prescription / Confirm Appointment
    Engine->>QSURA: Dispatch Payment Receipt & Consultation Confirmation
    Engine-->>Router: 200 OK (status=PROCESSED, transaction_id)
    Router-->>Gateway: 200 OK
```

---

## 10. Periodic System Cron Daemon & Scheduled Scanners Architecture (AUTO-01, AUTO-13, AUTO-14)

```mermaid
flowchart TD
    A["System Timer / Kubernetes CronJob"] --> B["CronSchedulerDaemon"]
    
    subgraph "Scheduled Scanners"
        B --> C["Hourly Appointment Reminder Scanner<br/>(lookahead_hours = 24.5h)"]
        B --> D["Daily PROMs Follow-up Scanner<br/>(target_days = 7, 14)"]
        B --> E["Nightly HIPAA Audit Purge<br/>(retention = 7 years)"]
        B --> F["Weekly Automated DR Drill<br/>(sandbox restore)"]
    end
    
    C --> G["Query Scheduled Appointments<br/>(T-24h & T-2h windows)"]
    G --> H{"Patient Contact Available?"}
    H -- "Yes" --> I["Dispatch APPOINTMENT_CONFIRMATION<br/>via QSURA WhatsApp/SMS"]
    H -- "No" --> J["Log to Clinical Worklist"]
    
    D --> K["Query Completed Encounters<br/>(Day +7 & Day +14)"]
    K --> L["Dispatch PROMS_OUTCOME_SURVEY<br/>with Secure Survey Token"]
    
    I --> M["Persist Audit Record in QSURA Dispatch Ledger"]
    L --> M
    E --> N["Immutable Audit Ledger Archive"]
    F --> O["DR Verification Report (RTO/RPO Metrics)"]
```

---

## 11. Prescription Delivery Logistics & Courier Tracking Flow (AUTO-15)

```mermaid
sequenceDiagram
    autonumber
    actor Pharmacy as Dispensary Pharmacist
    participant LogisticsRouter as Logistics Router (/api/v1/logistics)
    participant CourierEngine as CourierLogisticsEngine
    participant CarrierAPI as 3PL Carrier (Shiprocket / Delhivery / Bluedart)
    participant DB as Courier Shipments Table
    participant Patient as Patient Portal & QSURA

    Pharmacy->>LogisticsRouter: POST /shipments/create (prescription_id, pincode, cold_chain)
    LogisticsRouter->>CourierEngine: create_shipment(...)
    CourierEngine->>CourierEngine: Validate botanical temperature requirements
    CourierEngine->>CourierEngine: Generate carrier-prefixed AWB (e.g. AWB-SHIP-...)
    CourierEngine->>DB: Persist ShipmentRecord (status=MANIFESTED)
    CourierEngine-->>LogisticsRouter: Shipment Record with AWB
    LogisticsRouter-->>Pharmacy: 200 OK (AWB, Manifest Label)

    Note over CarrierAPI, LogisticsRouter: Real-Time Milestone Tracking Webhook
    CarrierAPI->>LogisticsRouter: POST /webhooks/courier-tracking (awb, status, location)
    LogisticsRouter->>CourierEngine: process_tracking_webhook(...)
    CourierEngine->>DB: Append milestone to tracking_history (IN_TRANSIT / DELIVERED)
    alt Delivered Status
        CourierEngine->>DB: Set delivered_at timestamp
        CourierEngine->>Patient: Send delivery notification with unboxing instructions
    end
    CourierEngine-->>LogisticsRouter: 200 OK (PROCESSED)
    LogisticsRouter-->>CarrierAPI: 200 OK
```
