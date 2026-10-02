# ZAYVORA Health OS™ — Raw Evidence & Audit Artifact Index

**Document Reference:** `RAW_EVIDENCE_INDEX.md`  
**Generated At:** 2026-09-16T16:14:55+05:30  
**Phase:** Raw Evidence Provenance & Traceability  

---

## 1. Primary Raw Execution Artifacts

| Evidence Artifact | File Path | Format / Size | Description |
|---|---|---|---|
| **Test Manifest (JSON)** | `EXACT_TEST_MANIFEST.json` | JSON / ~230 KB | Machine-readable record of all 324 discovered tests with durations, commands, categories, and results. |
| **Test Manifest (Markdown)** | `EXACT_TEST_MANIFEST.md` | Markdown / ~74 KB | Human-readable manifest and reconciliation of the 319/319 master test suite claim. |
| **JUnit XML Test Results** | `test-results.xml` | XML / ~45 KB | Standard CI/CD JUnit test results report parsed by GitHub Actions and Jenkins. |
| **Test Summary (JSON)** | `test-summary.json` | JSON / ~14 KB | High-level summary of suites, pass/fail counts, and reconciliation status. |
| **Raw Test Logs Directory** | `audit/raw-test-logs/*.log` | Plaintext / 48 files | Raw stdout/stderr execution streams captured per test suite during independent execution. |
| **Backup & DR Drill Output** | `database/dr_backup_restore.py` | Terminal Log | Checksum verification and row counts for drill `DRILL-BF8845A0` (Snapshot `SNAP-356B034F`). |
| **Coverage Summary** | `coverage-report/summary.txt` | Plaintext | Service-by-service statement coverage breakdown and critical path analysis. |

---

## 2. Directory of Captured Raw Test Logs (`audit/raw-test-logs/`)

- `test_crypto.py.log`: Clinical Crypto & PHI Encryption (6/6 PASS)
- `test_mizaj_and_diagnostics.py.log`: Clinical 10-Ajnas Mizaj (7/7 PASS)
- `test_organ_axis_and_evidence.py.log`: Clinical Organ-Axis (8/8 PASS)
- `test_digital_twin.py.log`: Clinical Digital Twin (6/6 PASS)
- `test_interop_and_fhir.py.log`: FHIR R4 & ABDM (9/9 PASS)
- `test_qsura_communication.py.log`: QSURA Communication (6/6 PASS)
- `test_research_and_rwe.py.log`: Research Cloud & RWE (3/3 PASS)
- `test_ambient_scribe_and_governance.py.log`: Ambient Scribe & 21 CFR Part 11 (9/9 PASS)
- `test_wearables_and_predictive.py.log`: Wearables Anomaly Detection (8/8 PASS)
- `test_patient_portal_and_dr.py.log`: Patient Portal & DR (6/6 PASS)
- `test_tasks_and_abdm_workers.py.log`: ABDM Workers (6/6 PASS)
- `test_payment_webhooks.py.log`: Payment Webhooks (5/5 PASS)
- `test_cron_and_scheduled_jobs.py.log`: Cron Schedulers (4/4 PASS)
- `test_safety_firewall.py.log`: Safety Firewall Baseline (13/13 PASS)
- `test_schedule_e1_and_interactions.py.log`: Schedule E(1) Mudabbar (16/16 PASS)
- `test_nuskha_compiler.py.log`: Nuskha Compiler (9/9 PASS)
- `test_tadbeer_guardrails.py.log`: Tadbeer Guardrails (13/13 PASS)
- `test_care_plans_and_pharmacovigilance.py.log`: Pharmacovigilance (8/8 PASS)
- `test_dispensary_and_fefo.py.log`: Dispensary & FEFO Engine (5/5 PASS)
- `test_ebmr_and_manufacturing.py.log`: Manufacturing OS & eBMR (5/5 PASS)
- `test_courier_logistics.py.log`: Courier Logistics (3/3 PASS)
- `test_pharmacopoeia.py.log`: UPI Pharmacopoeia (5/5 PASS)
- `test_knowledge_graph.py.log`: Multi-Hop Knowledge Graph (7/7 PASS)
- `test_taxonomy.py.log`: Mufradat Taxonomy (5/5 PASS)
- `test_hybrid_rag.py.log`: Hybrid RAG Retrieval (7/7 PASS)
- `test_command_search.py.log`: Global Command Search (6/6 PASS)
- `test_governance_board.py.log`: Clinical Governance Board (3/3 PASS)
- `test_source_library.py.log`: Source Provenance Library (9/9 PASS)
- `test_ocr_pipeline.py.log`: OCR Pipeline Extraction (5/5 PASS)
- `test_structured_knowledge.py.log`: Structured Knowledge (27/27 PASS)
- `test_response_validator.py.log`: AI Response Validator (8/8 PASS)
- `test_ai_runtime_and_zape.py.log`: AI Failover & ZAPE Scaling (11/11 PASS)
- `test_evaluation_and_red_team.py.log`: AI Evaluation & Red Team (8/8 PASS)
- `test_multimodal_extractor.py.log`: AI Multimodal Lab Extractor (8/8 PASS)
- `test_gateway.py.log`: Gateway Rate Limiting & Proxy (4/4 PASS)
- `test_helm_chart.py.log`: Helm Chart Packaging (3/3 PASS)
- `test_end_to_end_clinical_continuum.py.log`: End-to-End Clinical Continuum (1/1 PASS)
- `test_production_readiness_gate.py.log`: Production Readiness Gates (13/13 PASS)
- `test_clinical_pilot_concordance.py.log`: Multi-Center Concordance (5/5 PASS)
- `test_regulatory_dossier.py.log`: Statutory Regulatory Dossier (5/5 PASS)
- `test_staging_deployment_orchestrator.py.log`: Staging Orchestrator (5/5 PASS)
- `test_multi_page_website.py.log`: Website & Shared Data Layer (7/7 PASS)
- `test_mobile_application.py.log`: Mobile Screens & Navigation (5/5 PASS)
- `test_e2e_clinical_workflow.py.log`: End-to-End Ecosystem Continuum (7/7 PASS)
- `jest_blocked.log`: Jest frontend unit test execution block log (5 tests blocked)
