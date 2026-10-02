# ZAYVORA Health OS™ — Exact Test Manifest

**Generated At:** 2026-09-16T16:11:43+0530  
**Commit SHA:** `80435f58281ea66f41f42d915f24cfb7aafd2b58`  
**Reconciliation Claim Status:** **REPRODUCED EXACTLY (319/319 passed)**  

## 1. Test Execution & Reconciliation Summary

- **Total Discovered Tests:** 324
- **Master Suite Tests (Python Native):** 319
- **Master Suite Passed:** 319
- **Master Suite Failed:** 0
- **Jest Frontend Tests Discovered:** 5
- **Jest Frontend Tests Blocked:** 5 (Node.js runtime absent in host PATH)
- **Skipped Tests:** 0
- **Security-Specific Tests:** 14
- **E2E Integration Continuum Tests:** 8

## 2. Master Suite Discovered Test Modules & Counts

| Suite Title | Test File | Category | Count | Passed | Failed | Status |
|---|---|---|---|---|---|---|
| **Clinical Crypto & PHI Encryption** | `services/clinical/tests/test_crypto.py` | `security` | 6 | 6 | 0 | `PASS` |
| **Clinical 10-Ajnas Mizaj & Diagnostics** | `services/clinical/tests/test_mizaj_and_diagnostics.py` | `clinical` | 7 | 7 | 0 | `PASS` |
| **Clinical Organ-Axis & Evidence Engine** | `services/clinical/tests/test_organ_axis_and_evidence.py` | `clinical` | 8 | 8 | 0 | `PASS` |
| **Clinical Digital Twin & Trajectory Engine** | `services/clinical/tests/test_digital_twin.py` | `clinical` | 6 | 6 | 0 | `PASS` |
| **Clinical FHIR R4 & ABDM Interoperability** | `services/clinical/tests/test_interop_and_fhir.py` | `interoperability` | 9 | 9 | 0 | `PASS` |
| **Clinical QSURA Communication Layer** | `services/clinical/tests/test_qsura_communication.py` | `communication` | 6 | 6 | 0 | `PASS` |
| **Clinical Research Cloud & RWE Engine** | `services/clinical/tests/test_research_and_rwe.py` | `research` | 3 | 3 | 0 | `PASS` |
| **Clinical Ambient Scribe & 21 CFR Part 11** | `services/clinical/tests/test_ambient_scribe_and_governance.py` | `regulatory` | 9 | 9 | 0 | `PASS` |
| **Clinical Wearables & Predictive Relapse** | `services/clinical/tests/test_wearables_and_predictive.py` | `clinical` | 8 | 8 | 0 | `PASS` |
| **Clinical Patient Portal & Disaster Recovery** | `services/clinical/tests/test_patient_portal_and_dr.py` | `patient_portal` | 6 | 6 | 0 | `PASS` |
| **Clinical Tasks & ABDM Worker Pipelines** | `services/clinical/tests/test_tasks_and_abdm_workers.py` | `interoperability` | 6 | 6 | 0 | `PASS` |
| **Clinical Payment Gateway & Webhooks** | `services/clinical/tests/test_payment_webhooks.py` | `billing` | 5 | 5 | 0 | `PASS` |
| **Clinical Cron Scheduler & Scheduled Scanners** | `services/clinical/tests/test_cron_and_scheduled_jobs.py` | `infrastructure` | 4 | 4 | 0 | `PASS` |
| **Therapeutic Safety Firewall Baseline** | `services/therapeutic/tests/test_safety_firewall.py` | `safety` | 13 | 13 | 0 | `PASS` |
| **Therapeutic Schedule E(1) & Drug Interactions** | `services/therapeutic/tests/test_schedule_e1_and_interactions.py` | `safety` | 16 | 16 | 0 | `PASS` |
| **Therapeutic Nuskha Compiler & Posology** | `services/therapeutic/tests/test_nuskha_compiler.py` | `therapeutic` | 9 | 9 | 0 | `PASS` |
| **Therapeutic Tadbeer Guardrails** | `services/therapeutic/tests/test_tadbeer_guardrails.py` | `therapeutic` | 13 | 13 | 0 | `PASS` |
| **Therapeutic Care Plans & Pharmacovigilance** | `services/therapeutic/tests/test_care_plans_and_pharmacovigilance.py` | `pharmacovigilance` | 8 | 8 | 0 | `PASS` |
| **Therapeutic Dispensary & FEFO Engine** | `services/therapeutic/tests/test_dispensary_and_fefo.py` | `pharmacy` | 5 | 5 | 0 | `PASS` |
| **Therapeutic Manufacturing OS & eBMR** | `services/therapeutic/tests/test_ebmr_and_manufacturing.py` | `manufacturing` | 5 | 5 | 0 | `PASS` |
| **Therapeutic Courier Logistics & Tracking** | `services/therapeutic/tests/test_courier_logistics.py` | `logistics` | 3 | 3 | 0 | `PASS` |
| **Knowledge Pharmacopoeia Registry & Mudabbar** | `services/knowledge/tests/test_pharmacopoeia.py` | `knowledge` | 5 | 5 | 0 | `PASS` |
| **Knowledge Graph & Multi-Hop Traversal** | `services/knowledge/tests/test_knowledge_graph.py` | `knowledge` | 7 | 7 | 0 | `PASS` |
| **Knowledge Mufradat Taxonomy** | `services/knowledge/tests/test_taxonomy.py` | `knowledge` | 5 | 5 | 0 | `PASS` |
| **Knowledge Hybrid RAG & Semantic Retrieval** | `services/knowledge/tests/test_hybrid_rag.py` | `ai_rag` | 7 | 7 | 0 | `PASS` |
| **Knowledge Global Command Search (Cmd+K)** | `services/knowledge/tests/test_command_search.py` | `search` | 6 | 6 | 0 | `PASS` |
| **Knowledge Clinical Governance Board & Quorum** | `services/knowledge/tests/test_governance_board.py` | `governance` | 3 | 3 | 0 | `PASS` |
| **Knowledge Source Library & Provenance** | `services/knowledge/tests/test_source_library.py` | `knowledge` | 9 | 9 | 0 | `PASS` |
| **Knowledge OCR Pipeline & Extraction** | `services/knowledge/tests/test_ocr_pipeline.py` | `ocr` | 5 | 5 | 0 | `PASS` |
| **Knowledge Structured Clinical Knowledge & Safety** | `services/knowledge/tests/test_structured_knowledge.py` | `safety` | 27 | 27 | 0 | `PASS` |
| **AI Hakeem Sahab Response Validator** | `services/ai/tests/test_response_validator.py` | `ai_safety` | 8 | 8 | 0 | `PASS` |
| **AI Runtime Fallback & ZAPE Personalization** | `services/ai/tests/test_ai_runtime_and_zape.py` | `ai_safety` | 11 | 11 | 0 | `PASS` |
| **AI Evaluation Lab & Security Guardrails** | `services/ai/tests/test_evaluation_and_red_team.py` | `ai_security` | 8 | 8 | 0 | `PASS` |
| **AI Multimodal Lab Extractor & Physical Signs** | `services/ai/tests/test_multimodal_extractor.py` | `ai_multimodal` | 8 | 8 | 0 | `PASS` |
| **Gateway Reverse Proxy & Rate Limiting** | `services/gateway/tests/test_gateway.py` | `gateway` | 4 | 4 | 0 | `PASS` |
| **Infrastructure Helm Chart & Kubernetes Packaging** | `tests/test_helm_chart.py` | `infrastructure` | 3 | 3 | 0 | `PASS` |
| **End-to-End Clinical Continuum (11 Milestones)** | `tests/test_end_to_end_clinical_continuum.py` | `clinical_e2e` | 1 | 1 | 0 | `PASS` |
| **Phase 7 Production Readiness Gate (13 Gates)** | `tests/test_production_readiness_gate.py` | `devops_gates` | 13 | 13 | 0 | `PASS` |
| **Clinical Pilot Multi-Center Concordance & DSMB** | `tests/test_clinical_pilot_concordance.py` | `clinical_trials` | 5 | 5 | 0 | `PASS` |
| **Phase 9 Statutory Regulatory Dossier & Traceability** | `tests/test_regulatory_dossier.py` | `regulatory` | 5 | 5 | 0 | `PASS` |
| **Phase 10 Staging Cluster Deployment Orchestrator** | `tests/test_staging_deployment_orchestrator.py` | `staging` | 5 | 5 | 0 | `PASS` |
| **Multi-Page Website & Shared Data Layer** | `tests/test_multi_page_website.py` | `web_frontend` | 7 | 7 | 0 | `PASS` |
| **Mobile Application Workflows & Navigation** | `tests/test_mobile_application.py` | `mobile_frontend` | 5 | 5 | 0 | `PASS` |
| **End-to-End Clinical Ecosystem Continuum** | `tests/test_e2e_clinical_workflow.py` | `ecosystem_e2e` | 7 | 7 | 0 | `PASS` |

## 3. Discovered Tests Detail Matrix

| Test ID | Framework | Category | Expected Result | Actual Result | Status | Duration |
|---|---|---|---|---|---|---|
| `test_crypto.py::test_decrypt_phi_with_unencrypted_plaintext` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 3.24ms |
| `test_crypto.py::test_encrypt_decrypt_none_returns_none` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_crypto.py::test_encrypt_decrypt_phi_roundtrip` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_crypto.py::test_encrypt_phi_with_empty_key_passthrough` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_crypto.py::test_envelope_key_wrap_and_unwrap_roundtrip` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_crypto.py::test_patient_phi_dict_field_encryption_and_decryption` | `pytest-compatible` | `security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_differential_considerations_dyspepsia` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_mizaj_and_diagnostics.py::test_differential_considerations_gout` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_differential_considerations_stroke_red_flags` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_mizaj_assessment_10_ajnas_safrawi_dyscrasia` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_mizaj_assessment_empty_fallback` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_mizaj_assessment_mixed_constitution` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_mizaj_and_diagnostics.py::test_mizaj_assessment_pediatric_and_geriatric_calibration` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_organ_axis_and_evidence.py::test_asbab_e_arbaa_four_causes` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_organ_axis_and_evidence.py::test_biomarker_cross_talk_mapping` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_organ_axis_and_evidence.py::test_cardio_cerebral_reflex_arc` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_organ_axis_and_evidence.py::test_complete_organ_axis_analysis_orchestration` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_organ_axis_and_evidence.py::test_dawr_e_marad_progression_stages` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_organ_axis_and_evidence.py::test_evidence_engine_study_classifier_and_grade` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.47ms |
| `test_organ_axis_and_evidence.py::test_gastro_cephalic_reflex_arc` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_organ_axis_and_evidence.py::test_organ_axes_deduction_primary_musculoskeletal` | `unittest` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_digital_twin.py::test_build_digital_twin_baseline` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.16ms |
| `test_digital_twin.py::test_digital_twin_renal_and_pathology_deductions` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_digital_twin.py::test_digital_twin_severe_mizaj_drift` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_digital_twin.py::test_mizaj_trajectory_deteriorating_trend` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_digital_twin.py::test_mizaj_trajectory_healing_trend` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_digital_twin.py::test_treatment_trajectory_simulation` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_interop_and_fhir.py::test_abdm_gateway_consent_flow` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.09ms |
| `test_interop_and_fhir.py::test_abdm_gateway_live_mode_configuration_and_packet_push` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_interop_and_fhir.py::test_abdm_gateway_verify_abha` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.19ms |
| `test_interop_and_fhir.py::test_abdm_live_discovery_and_consent_exchange` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_interop_and_fhir.py::test_abdm_op_consult_bundle` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_interop_and_fhir.py::test_fhir_condition_resource_dual_coding` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_interop_and_fhir.py::test_fhir_medication_request_schedule_e1` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_interop_and_fhir.py::test_fhir_mizaj_observation` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_interop_and_fhir.py::test_fhir_patient_resource` | `pytest-compatible` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_qsura_communication.py::test_qsura_appointment_confirmation` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_qsura_communication.py::test_qsura_consent_enforcement` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_qsura_communication.py::test_qsura_database_persistence_and_live_transport` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.34ms |
| `test_qsura_communication.py::test_qsura_missing_required_params` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_qsura_communication.py::test_qsura_mudabbar_safety_advisory` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_qsura_communication.py::test_qsura_sms_phi_masking` | `pytest-compatible` | `communication` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_research_and_rwe.py::test_anonymize_patient_id_salted_hmac` | `pytest-compatible` | `research` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_research_and_rwe.py::test_classify_therapeutic_outcome` | `pytest-compatible` | `research` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_research_and_rwe.py::test_deidentify_patient_record_hipaa_safe_harbor` | `pytest-compatible` | `research` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_ambient_scribe_and_governance.py::test_ambient_scribe_audio_streaming_and_synthesis` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 2.24ms |
| `test_ambient_scribe_and_governance.py::test_ambient_scribe_clinician_sign_and_lock` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.18ms |
| `test_ambient_scribe_and_governance.py::test_ambient_scribe_entity_extraction` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_ambient_scribe_and_governance.py::test_ambient_scribe_multilingual_detection` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.24ms |
| `test_ambient_scribe_and_governance.py::test_ambient_scribe_soap_generation_and_invariants` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_ambient_scribe_and_governance.py::test_cryptographic_audit_ledger_chain_and_tamper_detection` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_ambient_scribe_and_governance.py::test_cryptographic_audit_ledger_merkle_anchoring` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_ambient_scribe_and_governance.py::test_part11_signature_envelope_and_verification` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_ambient_scribe_and_governance.py::test_websocket_audio_stream_transcription_pipeline` | `pytest-compatible` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.65ms |
| `test_wearables_and_predictive.py::test_apple_healthkit_webhook_ingestion` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_wearables_and_predictive.py::test_google_health_connect_webhook_ingestion` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_wearables_and_predictive.py::test_predictive_relapse_forecasting_acute_deterioration` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_wearables_and_predictive.py::test_predictive_relapse_forecasting_stable` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_wearables_and_predictive.py::test_telemetry_metrics_and_prometheus_export` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_wearables_and_predictive.py::test_wearable_anomaly_detection_autonomic_exhaustion` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_wearables_and_predictive.py::test_wearable_ingestion_and_rolling_summary` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_wearables_and_predictive.py::test_wearables_database_persistence` | `pytest-compatible` | `clinical` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.27ms |
| `test_patient_portal_and_dr.py::test_bhashini_multilingual_voice_synthesizer` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 93.7ms |
| `test_patient_portal_and_dr.py::test_disaster_recovery_pitr_compliance` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_patient_portal_and_dr.py::test_disaster_recovery_snapshot_creation_and_checksum` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_patient_portal_and_dr.py::test_patient_portal_messaging_triage` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_patient_portal_and_dr.py::test_patient_portal_schedule_and_adherence` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_patient_portal_and_dr.py::test_patient_portal_voice_router_integration` | `pytest-compatible` | `patient_portal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 22.2ms |
| `test_tasks_and_abdm_workers.py::test_abdm_packet_reconciliation_dual_coding` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_tasks_and_abdm_workers.py::test_fhir_batch_import_schedule_e1_poison_detection` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_tasks_and_abdm_workers.py::test_qsura_dispatch_zero_phi_masking` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_tasks_and_abdm_workers.py::test_task_queue_enqueue_dequeue_and_complete` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_tasks_and_abdm_workers.py::test_task_retry_and_terminal_failure` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_tasks_and_abdm_workers.py::test_wearable_stream_sync_and_humoral_drift` | `unittest` | `interoperability` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_payment_webhooks.py::test_forged_webhook_signature_raises_error` | `unittest` | `billing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_payment_webhooks.py::test_razorpay_invalid_signature_rejection` | `unittest` | `billing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_payment_webhooks.py::test_razorpay_valid_hmac_signature_verification` | `unittest` | `billing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_payment_webhooks.py::test_razorpay_webhook_event_processing_and_idempotency` | `unittest` | `billing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.1ms |
| `test_payment_webhooks.py::test_stripe_signature_verification` | `unittest` | `billing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_cron_and_scheduled_jobs.py::test_appointment_reminder_worker_scans_and_dispatches` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.36ms |
| `test_cron_and_scheduled_jobs.py::test_cron_scheduler_registration_and_execution` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_cron_and_scheduled_jobs.py::test_dead_letter_queue_isolation_and_requeue` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_cron_and_scheduled_jobs.py::test_proms_followup_worker_scans_and_dispatches` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.25ms |
| `test_safety_firewall.py::test_allergy_conflict_forces_do_not_recommend` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_safety_firewall.py::test_elderly_patient_gives_caution` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_immunosuppressant_forces_do_not_recommend` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_safety_firewall.py::test_multiple_severe_issues_escalate_to_highest_verdict` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_no_allergy_conflict_when_ingredient_unrelated` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_no_concerns_gives_safe_to_consider` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_pediatric_patient_gives_caution` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_pregnancy_forces_do_not_recommend` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_red_flag_complaint_forces_refer` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_renal_comorbidity_gives_caution` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_result_always_has_required_fields` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_warfarin_alone_gives_caution_not_modify` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_safety_firewall.py::test_warfarin_plus_garlic_forces_modify` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_schedule_e1_and_interactions.py::test_antihypertensive_plus_licorice_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_schedule_e1_and_interactions.py::test_ciprofloxacin_plus_kushta_forces_modify` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_schedule_e1_and_interactions.py::test_digoxin_plus_licorice_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_schedule_e1_and_interactions.py::test_lithium_plus_gokhru_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_schedule_e1_and_interactions.py::test_metformin_plus_karela_forces_modify` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_schedule_e1_and_interactions.py::test_mizaj_contraindication_in_acute_fever` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_mudabbar_kuchla_exceeding_ceiling_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_mudabbar_kuchla_within_limit_accepted_with_caution` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_mudabbar_suranjan_talkh_accepted_with_caution` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_raw_bhilawa_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_raw_kuchla_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_raw_suranjan_talkh_blocked_as_do_not_recommend` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_ssri_plus_harmal_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_suranjan_talkh_exceeding_statutory_ceiling_blocked` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_schedule_e1_and_interactions.py::test_tazaad_e_mizaj_extreme_temperament_conflict_without_musleh` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_schedule_e1_and_interactions.py::test_tazaad_e_mizaj_resolved_with_musleh` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_nuskha_compiler.py::test_badal_substitute_suggested` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_nuskha_compiler.py::test_compile_nuskha_includes_badal_potency_ratio` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_nuskha_compiler.py::test_formulation_balanced_when_musleh_included` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_nuskha_compiler.py::test_geriatric_dose_attenuation` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_nuskha_compiler.py::test_juz_e_azam_assigned_to_primary_axis` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_nuskha_compiler.py::test_missing_musleh_detected` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_nuskha_compiler.py::test_pediatric_dose_adjustment_youngs_rule` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_nuskha_compiler.py::test_renal_clearance_dose_attenuation` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_nuskha_compiler.py::test_substitute_badal_with_posology_potency_ratio` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_cauterization_kai_in_uncontrolled_diabetes_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_tadbeer_guardrails.py::test_dalak_massage_in_dvt_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_fasd_in_pregnancy_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_fasd_over_age_60_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_fasd_under_age_14_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_hot_hammam_in_acute_fever_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_leech_therapy_in_anticoagulants_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_lumbosacral_hijama_in_pregnancy_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_qai_in_severe_hypertension_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_safe_tadbeer_procedure_passes` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_tadbeer_guardrails.py::test_wet_hijama_in_hypotension_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_wet_hijama_in_severe_anemia_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_tadbeer_guardrails.py::test_wet_hijama_on_anticoagulants_blocked` | `pytest-compatible` | `therapeutic` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_care_plans_and_pharmacovigilance.py::test_care_plan_model_invariants` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.3ms |
| `test_care_plans_and_pharmacovigilance.py::test_expanded_classical_formulation_library` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.46ms |
| `test_care_plans_and_pharmacovigilance.py::test_pharmacovigilance_exports_cioms_format` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 1.22ms |
| `test_care_plans_and_pharmacovigilance.py::test_pharmacovigilance_exports_valid_e2b_xml` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_care_plans_and_pharmacovigilance.py::test_who_umc_certain_causality` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_care_plans_and_pharmacovigilance.py::test_who_umc_possible_with_concomitants` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_care_plans_and_pharmacovigilance.py::test_who_umc_probable_causality` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_care_plans_and_pharmacovigilance.py::test_who_umc_schedule_e1_mudabbar_violation` | `unittest` | `pharmacovigilance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_dispensary_and_fefo.py::test_execute_batch_recall_directive` | `pytest-compatible` | `pharmacy` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_dispensary_and_fefo.py::test_fefo_ignores_expired_and_quarantined` | `pytest-compatible` | `pharmacy` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.67ms |
| `test_dispensary_and_fefo.py::test_fefo_orders_by_earliest_expiry` | `pytest-compatible` | `pharmacy` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_dispensary_and_fefo.py::test_schedule_e1_mudabbar_gate_allows_certified` | `pytest-compatible` | `pharmacy` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_dispensary_and_fefo.py::test_schedule_e1_mudabbar_gate_blocks_uncertified` | `pytest-compatible` | `pharmacy` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ebmr_and_manufacturing.py::test_ebmr_ipqc_fail_heavy_metals` | `pytest-compatible` | `manufacturing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_ebmr_and_manufacturing.py::test_ebmr_ipqc_pass` | `pytest-compatible` | `manufacturing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ebmr_and_manufacturing.py::test_ebmr_schedule_e1_mudabbar_gate_block` | `pytest-compatible` | `manufacturing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ebmr_and_manufacturing.py::test_ebmr_session_initialization` | `pytest-compatible` | `manufacturing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ebmr_and_manufacturing.py::test_ebmr_successful_release_and_coa_generation` | `pytest-compatible` | `manufacturing` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_courier_logistics.py::test_courier_tracking_webhook_processing` | `unittest` | `logistics` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.08ms |
| `test_courier_logistics.py::test_invalid_carrier_rejection` | `unittest` | `logistics` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_courier_logistics.py::test_shipment_creation_and_awb_generation` | `unittest` | `logistics` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_pharmacopoeia.py::test_match_schedule_e1_substance_by_synonyms` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_pharmacopoeia.py::test_nfum_compound_formulations_registry` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_pharmacopoeia.py::test_schedule_e1_poisons_registry_integrity` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_pharmacopoeia.py::test_upi_mufradat_registry` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_pharmacopoeia.py::test_wfo_taxonomy_harmonization_and_analytical_specs` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_knowledge_graph.py::test_build_canonical_graph_nodes_and_edges` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.16ms |
| `test_knowledge_graph.py::test_extract_graph_rag_context` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.23ms |
| `test_knowledge_graph.py::test_find_correctives_for_kuchla` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.18ms |
| `test_knowledge_graph.py::test_four_graph_database_settings` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_knowledge_graph.py::test_get_compound_network_majun_suranjan` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.17ms |
| `test_knowledge_graph.py::test_get_mufrad_network_suranjan_talkh` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.18ms |
| `test_knowledge_graph.py::test_in_memory_graph_repository_seeding` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.32ms |
| `test_taxonomy.py::test_evidence_levels_covers_e0_to_e6` | `unittest` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_taxonomy.py::test_health` | `unittest` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_taxonomy.py::test_knowledge_worlds_covers_a_to_d` | `unittest` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_taxonomy.py::test_mizaj_temperaments_returns_all_four` | `unittest` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_taxonomy.py::test_organ_axes_returns_all_twelve` | `unittest` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_hybrid_rag.py::test_bm25_lexical_search` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.12ms |
| `test_hybrid_rag.py::test_dense_vector_store_retrieval` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.36ms |
| `test_hybrid_rag.py::test_deterministic_embedding_provider` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.14ms |
| `test_hybrid_rag.py::test_hybrid_rag_engine_full_lifecycle` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 33.77ms |
| `test_hybrid_rag.py::test_hybrid_rag_weighted_mode` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 31.56ms |
| `test_hybrid_rag.py::test_reciprocal_rank_fusion` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_hybrid_rag.py::test_tokenizer_unigrams_and_bigrams` | `pytest-compatible` | `ai_rag` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_command_search.py::test_command_search_amraz_and_icd11` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_command_search.py::test_command_search_empty_returns_shortcuts` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_command_search.py::test_command_search_mufradat_query` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_command_search.py::test_command_search_murakkabat_query` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_command_search.py::test_command_search_schedule_e1_badge` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_command_search.py::test_command_search_tadbeer_query` | `pytest-compatible` | `search` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_governance_board.py::test_governance_proposal_lifecycle_and_single_attestation` | `pytest-compatible` | `governance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_governance_board.py::test_governance_quorum_ratification_and_publication` | `pytest-compatible` | `governance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_governance_board.py::test_governance_unauthorized_role_rejected` | `pytest-compatible` | `governance` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_source_library.py::test_author_and_book_registration` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.63ms |
| `test_source_library.py::test_canonical_source_authors_and_books` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.08ms |
| `test_source_library.py::test_complete_cryptographic_provenance_chain` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_source_library.py::test_edition_registration_and_checksum` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.25ms |
| `test_source_library.py::test_high_res_scan_ingestion_and_sha256_hashing` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.42ms |
| `test_source_library.py::test_multilingual_scholarly_translations` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.48ms |
| `test_source_library.py::test_passage_segmentation_with_bounding_boxes` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.28ms |
| `test_source_library.py::test_rights_governance_and_safety_gate` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.24ms |
| `test_source_library.py::test_source_multi_field_search` | `pytest-compatible` | `knowledge` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ocr_pipeline.py::test_clinical_entity_extraction` | `pytest-compatible` | `ocr` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.21ms |
| `test_ocr_pipeline.py::test_detect_script_and_language` | `pytest-compatible` | `ocr` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.79ms |
| `test_ocr_pipeline.py::test_ocr_confidence_scoring_and_needs_review_flag` | `pytest-compatible` | `ocr` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_ocr_pipeline.py::test_scholarly_human_correction_desk` | `pytest-compatible` | `ocr` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_ocr_pipeline.py::test_submit_ocr_job_and_processing` | `pytest-compatible` | `ocr` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_structured_knowledge.py::test_diseases_get_by_id` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_structured_knowledge.py::test_diseases_list` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_engine_singleton` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_formulation_gate_duplicate_ingredient` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_structured_knowledge.py::test_formulation_gate_e1_without_mudabbar` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_formulation_gate_unknown_botanical` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_formulation_gate_valid` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mizaj_balghami` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mizaj_damawi` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_filter_poison_false` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_filter_poison_true` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_get_by_id_not_found` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_get_by_id_valid` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_list_all` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_search_english` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_mufradat_search_latin` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_murakkabat_get_by_id_valid` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_murakkabat_list_all` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_murakkabat_search_dosage_form` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_allowed` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_blocked_dose_ceiling` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_blocked_e1_uncertified` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_blocked_herb_drug_fatal` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_structured_knowledge.py::test_safety_blocked_pediatric` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_blocked_pregnancy` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_blocked_renal_impairment` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_structured_knowledge.py::test_safety_warning_herb_drug_moderate` | `pytest-compatible` | `safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_response_validator.py::test_empty_response_is_missing_everything` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_response_validator.py::test_missing_clinician_review_required_is_detected` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_response_validator.py::test_missing_safety_section_is_detected` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_response_validator.py::test_parse_sections_extracts_content_under_each_header` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_response_validator.py::test_parse_sections_returns_all_thirteen_when_well_formed` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_response_validator.py::test_response_validator_rejects_missing_section` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_response_validator.py::test_response_validator_rejects_missing_statutory_disclaimer` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_response_validator.py::test_well_formed_response_has_no_missing_sections` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ai_runtime_and_zape.py::test_chained_fallback_router_all_fail` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.09ms |
| `test_ai_runtime_and_zape.py::test_chained_fallback_router_failover_to_secondary` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_ai_runtime_and_zape.py::test_chained_fallback_router_primary_success` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ai_runtime_and_zape.py::test_hakeem_personalize_endpoint` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_ai_runtime_and_zape.py::test_hakeem_refine_endpoint` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.87ms |
| `test_ai_runtime_and_zape.py::test_hakeem_refine_engine_logic` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_ai_runtime_and_zape.py::test_zape_geriatric_renal_titration` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ai_runtime_and_zape.py::test_zape_master_orchestration` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ai_runtime_and_zape.py::test_zape_pediatric_posology` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ai_runtime_and_zape.py::test_zape_seasonal_modulation` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_ai_runtime_and_zape.py::test_zape_temperament_safrawi` | `pytest-compatible` | `ai_safety` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_evaluation_and_red_team.py::test_evaluation_engine_citation_precision` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.8ms |
| `test_evaluation_and_red_team.py::test_evaluation_engine_completeness` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.73ms |
| `test_evaluation_and_red_team.py::test_evaluation_engine_hallucination_and_invariants` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.34ms |
| `test_evaluation_and_red_team.py::test_gold_standard_benchmark_cases_count` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_evaluation_and_red_team.py::test_robustness_suite_audit` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 1.13ms |
| `test_evaluation_and_red_team.py::test_security_output_guardrail_verifies_invariants` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_evaluation_and_red_team.py::test_security_prompt_guardrails_allows_clinical_inquiry` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_evaluation_and_red_team.py::test_security_prompt_guardrails_blocks_injection` | `pytest-compatible` | `ai_security` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_multimodal_extractor.py::test_ckd_epi_egfr_and_renal_safety_profile` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 1.54ms |
| `test_multimodal_extractor.py::test_document_stream_extraction` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.12ms |
| `test_multimodal_extractor.py::test_loinc_definitions_completeness` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_multimodal_extractor.py::test_raw_text_extraction_and_dual_synthesis` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.14ms |
| `test_multimodal_extractor.py::test_structured_measurements_extraction` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_multimodal_extractor.py::test_image_semiotics_computer_vision` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_multimodal_extractor.py::test_skin_signs_dermatological_mapping` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_multimodal_extractor.py::test_tongue_signs_semiotic_mapping` | `unittest` | `ai_multimodal` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_gateway.py::test_hop_by_hop_headers_defined` | `pytest-compatible` | `gateway` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_gateway.py::test_rate_limiter_token_bucket_behavior` | `pytest-compatible` | `gateway` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_gateway.py::test_resolve_target_service` | `pytest-compatible` | `gateway` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_gateway.py::test_unregistered_path_returns_404` | `pytest-compatible` | `gateway` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_helm_chart.py::test_chart_yaml_structure` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.12ms |
| `test_helm_chart.py::test_template_files_present` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_helm_chart.py::test_values_yaml_covers_all_microservices` | `unittest` | `infrastructure` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.09ms |
| `test_end_to_end_clinical_continuum.py::test_full_clinical_continuum_end_to_end` | `pytest-compatible` | `clinical_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 54.54ms |
| `test_production_readiness_gate.py::test_gate_01_security_no_open_p0_p1_issues` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 2.86ms |
| `test_production_readiness_gate.py::test_gate_02_clinical_safety_no_autonomous_action` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.97ms |
| `test_production_readiness_gate.py::test_gate_03_ai_human_approval_citations_safety` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.02ms |
| `test_production_readiness_gate.py::test_gate_04_knowledge_base_provenance_expert_review` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.53ms |
| `test_production_readiness_gate.py::test_gate_05_patient_data_tenant_isolation` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.08ms |
| `test_production_readiness_gate.py::test_gate_06_database_backup_restore_tested` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 7.55ms |
| `test_production_readiness_gate.py::test_gate_07_apis_integration_contract_tests_pass` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.5ms |
| `test_production_readiness_gate.py::test_gate_08_ux_critical_workflows_usable` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_production_readiness_gate.py::test_gate_09_monitoring_alerts_observability_active` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.08ms |
| `test_production_readiness_gate.py::test_gate_10_documentation_sops_complete` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_production_readiness_gate.py::test_gate_11_compliance_legal_review_completed` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_production_readiness_gate.py::test_gate_12_testing_critical_tests_pass` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_production_readiness_gate.py::test_gate_13_release_rollback_plan_ready` | `unittest` | `devops_gates` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.53ms |
| `test_clinical_pilot_concordance.py::test_01_cohort_case_ingestion` | `unittest` | `clinical_trials` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.23ms |
| `test_clinical_pilot_concordance.py::test_02_cohens_kappa_concordance_calculation` | `unittest` | `clinical_trials` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.39ms |
| `test_clinical_pilot_concordance.py::test_03_zero_tolerance_safety_interception` | `unittest` | `clinical_trials` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.3ms |
| `test_clinical_pilot_concordance.py::test_04_dsmb_interim_report_generation` | `unittest` | `clinical_trials` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.32ms |
| `test_clinical_pilot_concordance.py::test_05_pilot_tenants_seeding_and_isolation` | `unittest` | `clinical_trials` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 2.06ms |
| `test_regulatory_dossier.py::test_01_traceability_matrix_100_percent_coverage` | `unittest` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_regulatory_dossier.py::test_02_zero_orphaned_requirements` | `unittest` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_regulatory_dossier.py::test_03_regulatory_inspection_pack_generation` | `unittest` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_regulatory_dossier.py::test_04_statutory_poison_and_prescribing_traceability` | `unittest` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.01ms |
| `test_regulatory_dossier.py::test_05_dossier_document_exists_and_complete` | `unittest` | `regulatory` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_staging_deployment_orchestrator.py::test_01_orchestrator_initialization` | `unittest` | `staging` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_staging_deployment_orchestrator.py::test_02_helm_chart_packaging_verification` | `unittest` | `staging` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.04ms |
| `test_staging_deployment_orchestrator.py::test_03_database_migration_configuration` | `unittest` | `staging` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.05ms |
| `test_staging_deployment_orchestrator.py::test_04_health_smoke_checks` | `unittest` | `staging` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.03ms |
| `test_staging_deployment_orchestrator.py::test_05_full_deployment_certificate_issuance` | `unittest` | `staging` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 1.63ms |
| `test_multi_page_website.py::test_design_system_components_exist` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.12ms |
| `test_multi_page_website.py::test_header_navigation_dropdowns` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.1ms |
| `test_multi_page_website.py::test_required_routes_exist` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.2ms |
| `test_multi_page_website.py::test_shared_components_exist` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_multi_page_website.py::test_shared_data_layer_files_exist` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.09ms |
| `test_multi_page_website.py::test_site_config_values` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_multi_page_website.py::test_zero_accidental_external_branding_in_new_routes` | `unittest` | `web_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 17.19ms |
| `test_mobile_application.py::test_all_11_screens_exist` | `unittest` | `mobile_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.11ms |
| `test_mobile_application.py::test_app_navigator_exists_and_routes_screens` | `unittest` | `mobile_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.09ms |
| `test_mobile_application.py::test_mobile_services_exist` | `unittest` | `mobile_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.06ms |
| `test_mobile_application.py::test_mobile_shared_components_exist` | `unittest` | `mobile_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 0.07ms |
| `test_mobile_application.py::test_mobile_zero_external_branding` | `unittest` | `mobile_frontend` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 1.4ms |
| `test_e2e_clinical_workflow.py::test_01_patient_record_resolution` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 9.28ms |
| `test_e2e_clinical_workflow.py::test_02_appointment_booking_flow` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 5.01ms |
| `test_e2e_clinical_workflow.py::test_03_hakeem_sahab_copilot_safety` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 10.48ms |
| `test_e2e_clinical_workflow.py::test_04_prescription_authoring_and_signing` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 5.6ms |
| `test_e2e_clinical_workflow.py::test_05_pharmacy_fefo_dispensing` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 4.04ms |
| `test_e2e_clinical_workflow.py::test_06_patient_idor_prevention` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 5.89ms |
| `test_e2e_clinical_workflow.py::test_07_appointment_lifecycle_patch_delete` | `unittest` | `ecosystem_e2e` | Pass without uncaught exceptions or assertion errors | Execution successful | `PASSED` | 10.5ms |
| `apps/web/__tests__/components/admin-layout.test.tsx::renders brand logo and nav items` | `jest / react-testing-library` | `web_frontend` | Component renders and passes DOM assertions | Static AST verified; runtime blocked by missing No | `BLOCKED` | 0.0ms |
| `apps/web/__tests__/components/admin-layout.test.tsx::toggles sidebar collapse` | `jest / react-testing-library` | `web_frontend` | Component renders and passes DOM assertions | Static AST verified; runtime blocked by missing No | `BLOCKED` | 0.0ms |
| `apps/web/__tests__/pages/admin-health.test.tsx::renders system health dashboard` | `jest / react-testing-library` | `web_frontend` | Component renders and passes DOM assertions | Static AST verified; runtime blocked by missing No | `BLOCKED` | 0.0ms |
| `apps/web/__tests__/pages/admin-users.test.tsx::renders users table and search input` | `jest / react-testing-library` | `web_frontend` | Component renders and passes DOM assertions | Static AST verified; runtime blocked by missing No | `BLOCKED` | 0.0ms |
| `apps/web/__tests__/pages/admin-users.test.tsx::filters user list by name or email` | `jest / react-testing-library` | `web_frontend` | Component renders and passes DOM assertions | Static AST verified; runtime blocked by missing No | `BLOCKED` | 0.0ms |
