# ZAYVORA AGENTIC CLINICAL AI™ — Production Architecture
## Hakeem Sahab AI™ & The Agentic Clinical Runtime

---

### 1. SYSTEM IDENTITY

ZAYVORA Agentic Clinical AI is an AI-assisted orchestration and decision-support layer operating within ZAYVORA Health OS.

It is **not** an autonomous physician.

Its purpose is to:
* retrieve authorized information
* organize clinical context
* identify missing information
* reason over approved knowledge
* surface evidence
* evaluate safety conditions
* prepare clinical work
* perform explicitly authorized non-clinical actions
* request clinician approval when required
* verify completed actions
* maintain a complete audit trail

**Final clinical authority remains with the appropriately authorized clinician.**

---

### 2. CORE ARCHITECTURE

```text
                         ZAYVORA HEALTH OS™
                                │
                                ▼
                   AGENTIC CLINICAL RUNTIME
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
    Clinical Agent        Knowledge Agent       Operations Agent
          │                     │                     │
          └──────────────┬──────┴──────────────┬──────┘
                         ▼                     │
                   Safety Agent               │
                         │                     │
                         ▼                     │
                  Evidence Agent              │
                         │                     │
                         ▼                     │
                 HUMAN APPROVAL GATE ◄────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Clinical Action          Operational Action
             │                       │
             └───────────┬───────────┘
                         ▼
                    VERIFICATION
                         │
                         ▼
                    AUDIT / EVENT LOG
                         │
                         ▼
               OUTCOME / FOLLOW-UP LOOP
```

---

### 3. AGENT HIERARCHY

#### A. Hakeem Sahab Orchestrator
This is the top-level coordinator.

**Responsibilities:**
* understand user/clinician goal
* create execution plan
* select appropriate agents/tools
* maintain workflow state
* enforce permission boundaries
* invoke safety checks
* request approval
* verify completion
* stop when conditions are unsafe or incomplete

*It should never directly bypass safety or authorization.*

---

### 4. CLINICAL AGENT

**Purpose:**
> Organize and interpret the clinical context for clinician review.

**Inputs:**
* patient history
* current symptoms
* encounters
* observations
* laboratory results
* medications
* allergies
* relevant sensing data
* previous care plans
* clinician notes

**Outputs:**
* clinical summary
* relevant findings
* missing information
* possible clinical considerations
* follow-up considerations
* questions for clinician review

*The Clinical Agent must not silently convert its output into a diagnosis or prescription.*

---

### 5. KNOWLEDGE AGENT

**Purpose:**
> Retrieve the most relevant approved knowledge from ZAYVORA Knowledge Intelligence™.

**Sources may include:**
* Mufradat
* Murakkabat
* Unani terminology
* Nuskha knowledge
* clinical references
* pharmacology
* safety records
* evidence records
* approved care pathways

**Every retrieval must carry provenance:**
```text
source_id
knowledge_version
retrieval_timestamp
evidence_category
review_status
reviewed_by
```
*No uncontrolled web content should silently become clinical knowledge.*

---

### 6. EVIDENCE AGENT

**The Evidence Agent answers:**
> *"What supports this consideration?"*

**It must return:**
* source
* evidence type
* evidence quality
* publication date
* relevance
* limitations
* applicability
* review status

**Example Output:**
```text
Evidence:
Traditional-use evidence

Clinical evidence:
Limited

Safety evidence:
Moderate

Limitations:
Small study population
No direct comparative evidence
```

*The agent must distinguish empirical evidence from hypothesis.*

---

### 7. SAFETY AGENT

**This is a mandatory gate.**

Before any clinically meaningful action:
```text
Patient identity
↓
Allergy
↓
Drug interactions
↓
Herb-drug interactions
↓
Contraindications
↓
Age
↓
Pregnancy/lactation where relevant
↓
Relevant organ function
↓
Dose constraints
↓
Red flags
↓
Missing critical information
↓
Safety decision
```

**States:**
```text
PASS      → Action can proceed to next permitted stage.
CAUTION   → Mandatory clinician acknowledgement where defined.
BLOCK     → Action cannot proceed under any circumstances.
UNKNOWN   → Action cannot proceed until missing critical data is provided or resolved by clinician.
```

---

### 8. PATIENT AGENT

**Purpose:**
> Patient education, navigation, and communication.

**Permitted Actions:**
* explain approved care-plan information
* explain medicine instructions
* explain appointment details
* prepare questions for clinician
* remind patient of care tasks
* guide patients through intake forms
* provide approved educational material

**Strict Invariants:**
* Never independently prescribe
* Never modify treatment
* Never override clinician instructions
* Never diagnose
* Never conceal uncertainty
* Never send sensitive medical communication without appropriate authorization
* Always use simpler, patient-accessible health language

---

### 9. OPERATIONS AGENT

**Purpose:**
> Handle non-clinical administrative workflows.

**Capabilities:**
* Appointment scheduling
* Follow-up task creation
* Reminder generation
* Document requests
* Queue management
* Pharmacy task routing
* Notification orchestration

*Verification Rule*: Never report *"Message sent"* unless the downstream gateway confirms transmission.

---

### 10. PHARMACY AGENT

**Purpose:**
> Support closed-loop pharmacy operations.

**Capabilities:**
* retrieve prescription
* verify prescription status
* identify product/batch
* check expiry
* perform FEFO selection
* check stock
* prepare dispensing task
* record dispensing events

*Strict Invariant*: Pharmacy Agent must never create or modify a clinician's prescription without an authorized workflow.

---

### 11. RESEARCH AGENT

**Purpose:**
> Support research and real-world evidence (RWE) workflows.

**Capabilities:**
* identify eligible cohorts according to approved criteria
* retrieve de-identified data where authorized
* generate analysis plans
* compare outcomes
* identify clinical signals
* generate research summaries

*Explicit Rule:*
```text
RESEARCH ≠ CLINICAL CARE
```
A research finding must pass through institutional clinical governance before entering approved clinical knowledge.

---

### 12. SENSING AGENT

Connects directly to the **ZAYVORA Sensing Platform™**.

**Sources:**
* NABZ (Pulse device)
* LISAN (Tongue imaging device)
* Wearables & telemetry
* Laboratory analyzers
* Remote monitoring sensors

*First Principle*: The Sensing Agent must answer **"Is this measurement usable?"** before answering **"What might this mean?"**

---

### 13. ZAYVORA NABZ SENSING FLOW

```text
Nabz Device
↓
Raw Pulse Signal
↓
Calibration
↓
Signal Quality
↓
Feature Extraction
↓
Validated Measurement
↓
Patient + Encounter Context
↓
Unani Clinical Context
↓
Evidence
↓
Safety
↓
Hakeem Sahab
↓
Clinician Review
```

*Quality Rejection Rule:* If `Signal Quality == INVALID` $\rightarrow$ Stop interpretation immediately and request repeat measurement.

---

### 14. ZAYVORA LISAN SENSING FLOW

```text
Lisan Device
↓
Image Capture
↓
Lighting Validation
↓
Color Calibration
↓
Tongue Segmentation
↓
Image Quality Check
↓
Feature Extraction
↓
Structured Observation
↓
Clinical Context
↓
Evidence
↓
Clinician Review
```

*The system must strictly distinguish image observation from clinical interpretation.*

---

### 15. AGENT MEMORY TIERS

Healthcare memory must be strictly partitioned:

1. **Short-Term Working Memory**: Current task, patient, encounter, active tools, and workflow state only.
2. **Longitudinal Clinical Context**: Persisted, authorized patient records (history, encounters, care plans, labs, adverse events).
3. **Knowledge Memory**: Approved organizational knowledge base (Mufradat, Murakkabat, Evidence, Safety, Terminology, Protocols).

*Strict Invariant*: Never mix patient memory with organizational knowledge.

---

### 16. MEMORY PERMISSION MODEL

Every memory read requires:
```text
Actor + Role + Organization + Facility + Patient Relationship + Purpose + Permission
```
The AI must never have unrestricted access to the entire patient database.

---

### 17. TOOL REGISTRY & RISK LEVELS

Every agent tool must declare:
```text
tool_id | description | required_permission | allowed_roles | data_scope | risk_level | approval_required | audit_required
```

**Risk Classes:**
* **R0 — Informational**: (e.g., retrieve appointment availability). No clinical impact.
* **R1 — Low-risk operational**: (e.g., create reminder task).
* **R2 — Sensitive**: (e.g., access detailed patient clinical chart). Requires role authorization and audit.
* **R3 — Clinically meaningful**: (e.g., prepare a draft Nuskha). Requires clinician review.
* **R4 — High-impact clinical**: (e.g., finalize/sign prescription). Mandatory human approval and cryptographic signature.
* **R5 — Privileged/system**: (e.g., modify governance rules). Restricted administrative authorization.

*The AI must never escalate its own permission level.*

---

### 18. CLINICAL APPROVAL GATE

```text
AI Recommendation
       ↓
Safety Check
       ↓
Evidence Check
       ↓
Completeness Check
       ↓
Clinician Approval (Accept / Modify / Reject / Defer)
       ↓
Electronic Signature (SHA-256 HMAC / 21 CFR Part 11)
       ↓
Final Clinical Record Locked
```

---

### 19. AGENT WORKFLOW STATE MACHINE

```text
CREATED → PLANNING → RETRIEVING → ANALYZING → SAFETY_REVIEW → AWAITING_APPROVAL → APPROVED → EXECUTING → VERIFYING → COMPLETED
```
**Failure/Hold States:**
`BLOCKED` | `FAILED` | `PARTIAL` | `REQUIRES_INPUT` | `REQUIRES_CLINICIAN` | `EXPIRED` | `CANCELLED`

---

### 20. VERIFICATION & PROVENANCE INVARIANTS

* **Verification Loop**: Intent $\rightarrow$ Action $\rightarrow$ Server Response $\rightarrow$ Downstream Verification $\rightarrow$ Mark Complete. Never assume success based on function return alone.
* **Communication Delivery**: Status explicitly tracks `Queued` $\rightarrow$ `Sent` $\rightarrow$ `Delivered` $\rightarrow$ `Failed`.
* **Deterministic vs AI Decisions**: Critical contraindications (e.g., pregnancy, lethal herb interactions) must run on **deterministic rule engines**, never probabilistic LLM guesses.
* **Hallucination Control**: Unsupported clinical claims are blocked or explicitly labeled as `UNKNOWN`.
* **The "Why?" Interface**: Every clinical recommendation in the Clinical Desk links to an **Evidence Drawer** showing the exact source, trial data, classical treatise, and safety rule.

---

### 21. PHASED ROLLOUT STRATEGY

* **Phase 1 (V1 — Core Clinical Decision Support)**:
  * Hakeem Sahab Orchestrator
  * Clinical Agent
  * Knowledge Agent
  * Evidence Agent
  * Safety Agent
  * Human Approval Gate
* **Phase 2 (V2 — Operational & Sensing Expansion)**:
  * Patient Agent
  * Operations Agent
  * Pharmacy Agent
  * Device Intelligence Agent (Nabz/Lisan)
  * Follow-up Agent
* **Phase 3 (V3 — Population & Continuous Governance)**:
  * Research Agent
  * RWE Agent
  * Population Health Agent
  * Autonomous workflow orchestration with institutional review boards

---

### 22. CORE PRINCIPLE

> **AI proposes.**  
> **Evidence informs.**  
> **Safety constrains.**  
> **Tools execute authorized actions.**  
> **Clinician decides.**  
> **System verifies.**  
> **Governance learns.**  

---
*Official Blueprint of ZAYVORA Health OS™ Clinical AI Architecture.*
