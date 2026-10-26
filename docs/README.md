# ZAYVORA Health OS — Enterprise Documentation Hub

Welcome to the central technical documentation and architectural repository for **ZAYVORA Health OS (V5.0.0-Enterprise)**.

This documentation suite is organized according to the international **Diátaxis Documentation Framework** (Tutorials, How-to Guides, Technical Reference, and Architectural Explanation), tailored for institutional-grade digital health systems, clinical AI governance, and multi-jurisdictional statutory compliance.

---

## 🏛️ Documentation Architecture (Diátaxis Taxonomy)

```
docs/
├── architecture/          # System design, microservice specs, data schemas, and API inventories
├── clinical/              # Evidence-based clinical protocols, AI safety, and DSMB trial vignettes
├── compliance/            # HIPAA, GDPR, ABDM, DISHA statutory mappings, RBAC, and traceability
├── security/              # Defense-in-depth security models, encryption standards, and reports
├── operations/            # Deployment runbooks, DR backup & restore, incident response, checklists
├── qa/                    # Quality assurance test plans, journey test reports, and verification matrices
├── product/               # Product feature matrices, mobile specifications, and design system
├── compendiums/           # ZAYVORA Doctrine master book, clinical compendiums, and executive booklets
├── reports/               # Phased delivery reports and historical audit archives
└── zayvora-audit/         # Regulatory dossiers, SOP manuals, and statutory compliance reviews
```

---

## 🧭 Direct Navigation Index

### 1. Architecture & System Design (`docs/architecture/`)
*Authoritative specifications, system topologies, and database schemas.*

- **[System Architecture Master Blueprint](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/FINAL_ARCHITECTURE.md)**: Master structural design and inter-service communication model.
- **[System Runtime Topology Specification](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/SYSTEM_RUNTIME_TOPOLOGY.md)**: Dual-profile runtime formalization (Modular Monolith vs Distributed Cloud).
- **[Source of Truth Specification](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/ARCHITECTURE_SOURCE_OF_TRUTH.md)**: Architectural invariants and system constraints.
- **[Database Schema & Inventory](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/FINAL_DATABASE_SCHEMA.md)**: Complete relational model, indexing strategy, and table dictionary.
- **[API Reference & Contracts](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/FINAL_API_REFERENCE.md)**: Comprehensive REST endpoint reference and JSON payload contracts.
- **[ZFIE Master Specification V1](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/ZFIE_MASTER_SPECIFICATION_V1.md)**: ZAYVORA Formulation Intelligence Engine specifications.
- **[Clinical AI Architecture](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/architecture/ZAYVORA_AGENTIC_CLINICAL_AI_ARCHITECTURE.md)**: Agentic clinical decision support systems and RAG pipelines.

### 2. Clinical Protocols & AI Safety (`docs/clinical/`)
*Algorithmic medical governance, evidence-based Unani/Tibb protocols, and DSMB concordance.*

- **[Final Unani Protocols](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/clinical/FINAL_UNANI_PROTOCOLS.md)**: Canonical clinical pathways for classical formulations.
- **[Clinical Safety & AI Governance](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/clinical/FINAL_CLINICAL_SAFETY_REPORT.md)**: 12-Gate clinical governance, drug-drug interaction matrix, and contraindication guards.
- **[50 DSMB Clinical Validation Vignettes](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/clinical/ZAYVORA_CLINICAL_VALIDATION_VIGNETTES_50.md)**: Benchmark concordance scenarios validated against expert clinician panels.
- **[Agentic Systems Action Plan](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/clinical/ZAYVORA_AGENTIC_SYSTEMS_ACTION_PLAN.md)**: Autonomous agent orchestrators and human-in-the-loop workflows.
- **[Doctor Approval Workflow](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/clinical/doctor-approval-workflow.md)**: Clinical sign-off policies and prescription verification.

### 3. Compliance, Governance & RBAC (`docs/compliance/`)
*Statutory conformance (HIPAA, GDPR, ABDM, DISHA), role-based access control, and requirements traceability.*

- **[Statutory Regulatory Mapping](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/STATUTORY_COMPLIANCE_AND_REGULATORY_MAPPING.md)**: Jurisdiction-by-jurisdiction regulatory controls.
- **[Auth & RBAC Specification](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/AUTH_RBAC_SPECIFICATION.md)**: 10-Role enterprise authorization matrix and privilege tiers.
- **[AI Identity Governance](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/AI_IDENTITY_GOVERNANCE.md)**: AI agent identity bounds and clinical guardrail adherence.
- **[Requirement Traceability Matrix](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/FINAL_REQUIREMENT_TRACEABILITY_MATRIX.md)**: 100% bidirectional verification of design requirements.
- **[HIPAA Gap Analysis](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/HIPAA_GAP_ANALYSIS.md)**: Administrative, physical, and technical safeguard audit.
- **[GDPR Gap Analysis](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compliance/GDPR_GAP_ANALYSIS.md)**: Data subject rights, consent lifecycle, and cross-border processing.

### 4. Security & Cryptographic Invariants (`docs/security/`)
*Defense-in-depth architecture, PHI protection, and security audit reports.*

- **[Final Security Model](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/security/FINAL_SECURITY_MODEL.md)**: Zero-trust network model, token rotation, and password hashing standards.
- **[Security Verification Report](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/security/FINAL_SECURITY_REPORT.md)**: Automated pen-testing, static analysis, and vulnerability mitigation.

### 5. Operations & Production Runbooks (`docs/operations/`)
*Deployment runbooks, disaster recovery strategies, and incident response playbooks.*

- **[Production Deployment Guide](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/operations/FINAL_DEPLOYMENT_GUIDE.md)**: Container orchestration, environment variables, and pre-flight checks.
- **[Disaster Recovery & Backup Guide](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/operations/BACKUP_RESTORE_GUIDE.md)**: WAL-mode atomic backup strategies, point-in-time recovery, and companion file pruning.
- **[Incident Response Playbook](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/operations/INCIDENT_RESPONSE.md)**: Severity classification, escalation matrix, and post-mortem procedures.
- **[Release Checklist](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/operations/RELEASE_CHECKLIST.md)**: Multi-gate checklist for enterprise deployments.

### 6. Quality Assurance & Verification (`docs/qa/`)
*Verification suites, user journey test runs, and test plans.*

- **[V5 Comprehensive Test Plan](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/qa/V5_TEST_PLAN.md)**: Unit, integration, end-to-end, and performance testing methodologies.
- **[End-to-End Verification Report](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/qa/FINAL_E2E_TEST_REPORT.md)**: Full clinical continuum verification runs.
- **[Doctor Journey Test Report](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/qa/DOCTOR_JOURNEY_TEST_REPORT.md)**: Practitioner consult, prescription, and triage simulation.
- **[Patient Journey Test Report](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/qa/PATIENT_JOURNEY_TEST_REPORT.md)**: Telemedicine intake, health record, and wellness plan simulation.

### 7. Product Specifications & UI/UX (`docs/product/`)
*Feature specifications, mobile app wireframes, and design standards.*

- **[System Feature Matrix](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/product/FEATURE_MATRIX.md)**: Full taxonomy of modules, clinical engines, and platform capabilities.
- **[Design System Specifications](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/product/V5_DESIGN_SYSTEM.md)**: Visual tokens, typography, dark-mode color palettes, and accessibility guidelines.
- **[Mobile Application Specification](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/product/FINAL_MOBILE_SPEC.md)**: Responsive mobile layout, PWA offline sync, and screen flows.
- **[Brand Terminology Glossary](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/product/BRAND_TERMINOLOGY_GLOSSARY.md)**: Authoritative medical and institutional nomenclature.

### 8. Institutional Compendiums & Books (`docs/compendiums/`)
*Canonical doctrines, master publications, and formulary compendiums.*

- **[The ZAYVORA Doctrine Master Book](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compendiums/THE_ZAYVORA_DOCTRINE_MASTER_BOOK.md)**: Institutional foundation, clinical philosophy, and future roadmap.
- **[Executive Booklet](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compendiums/ZAYVORA_HEALTH_OS_EXECUTIVE_BOOKLET.md)**: C-level institutional overview and clinical ROI.
- **[Client Product Booklet](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/compendiums/ZAYVORA_CLIENT_PRODUCT_BOOKLET.md)**: Patient and partner-facing product guide.

### 9. Delivery Reports & Historical Audits (`docs/reports/`)
*Milestone delivery proofs and consolidated forensic audits.*

- **[Delivery Reports](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/reports/delivery/)**: Phase-by-phase completion reports (Phase 0 through Phase 7) and release scorecards.
- **[Audit Archives](file:///Users/irfanashraf/Downloads/zayvora-platform-phase0-4/docs/reports/archive_audits/)**: Historical gap matrices, functional audits, and technical evaluations categorized by subsystem.

---

## 🛡️ Documentation Parity & Integrity Rules

1. **Static Hosting Parity**: Static web entry points (`index.html`, `app.html`, `sw.js`, `manifest.json`, `tailwind.min.js`, `zayvora-logo.png`, `CNAME`, `_redirects`, `netlify.toml`) located in `docs/` root are strictly mirrored against root assets for GitHub Pages and edge deployments. They are protected by automated integrity test gates (`tests/test_codebase_integrity_and_parity.py`).
2. **Regulatory Dossier Permanence**: The regulatory dossier files in `docs/zayvora-audit/` are permanent legal records asserted by `tests/test_production_readiness_gate.py` and must never be altered or relocated without statutory authorization.
3. **Automated Quality Gate Shield**: All documentation changes must pass the zero-defect Quality Gate shield (`python3 scripts/quality_gate.py`) and 100% test pass rate across the 726-test suite before merging to mainline branches.
