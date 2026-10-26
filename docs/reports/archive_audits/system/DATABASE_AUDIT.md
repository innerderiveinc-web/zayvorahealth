# ZAYVORA Health OS™ — Database Architecture & Integrity Audit
**Document ID**: `AUDIT-DB-04`  
**Target**: PostgreSQL (Transactional ACID) & Neo4j (Knowledge Graph)  
**Standard**: 21 CFR Part 11 Tamper-Resistant Relational Storage  

---

## 1. Relational Schema Inventory (32 Core Tables)

### Clinical Schema (`services/clinical/app/models/`):
1. `patients` (Master Patient 360 demographic record, MRN, allergies, baseline Mizaj)
2. `clinical_encounters` (Consultation records, timestamps, provider IDs)
3. `clinical_notes` (Append-only SOAP notes with version chaining via `amends_note_id`)
4. `prescriptions` (Master clinical prescriptions, digital signatures, status)
5. `appointments` (Scheduled clinic visits, queues, status)
6. `diagnostic_reports` (Laboratory, imaging, and physical examination records)
7. `mizaj_evaluations` (10-Ajnas qualitative criteria and quantitative temperament vectors)
8. `organ_axis_states` (Biomarker cross-talk, impairment scores, affected pathways)
9. `digital_twin_states` (Dynamic physiological digital twin snapshots)
10. `relapse_forecasts` (Predictive recurrence signals and risk scores)
11. `task_items` (Clinical workflow tasks, reminders, and departmental handoffs)
12. `wearable_streams` (IoT continuous physiological sensor telemetry)
13. `consent_records` (ABDM / DISHA purpose-specific patient consent artifacts)
14. `invoices` (Billing records, fee schedules, payment statuses)
15. `payment_transactions` (Webhook-validated payment logs, gateway IDs)

### Therapeutic Schema (`services/therapeutic/app/models/`):
16. `nuskha_drafts` (Formulation drafts, component ratios, Badal, Musleh)
17. `nuskha_prescriptions` (Finalized prescriptions pending or granted clinician signature)
18. `tadbeer_plans` (Regimenal therapies: Hijama, Fasd, Dalak, Hammam)
19. `ghiza_plans` (Dietary intervention schedules and caloric/temperament matrices)
20. `care_plans` (Unified multi-horizon integrative health care plans)
21. `adverse_event_reports` (ICH E2B pharmacovigilance reports and causality scores)
22. `posology_overrides` (Justified clinician overrides with cryptographic hash)
23. `inventory_batches` (FEFO stock batches, expiration dates, Mudabbar poison certificates)
24. `dispense_records` (Pharmacy fulfillment logs, dispensed lots, pharmacist IDs)
25. `pharmacy_products` (Catalog of botanical, mineral, and compound preparations)
26. `product_variants` (SKUs, dosage forms: Majun, Safoof, Arq, Qurs)
27. `suppliers` (Raw material and manufactured goods suppliers)
28. `purchase_orders` (Procurement orders, receiving verification)
29. `courier_shipments` (Delivery tracking, cold-chain compliance)

### Identity Schema (`services/identity/app/models/`):
30. `users` (Clinicians, pharmacists, administrators, patients)
31. `organizations` (Multi-tenant medical centers, clinics, academic institutes)
32. `roles`, `permissions`, `user_roles`, `audit_logs` (RBAC access matrix and immutable logs)

---

## 2. Multi-Tenant Isolation & Integrity Guarantees
- **Composite Org Indexing**: Strict `organization_id` indexing on every table (`idx_patients_org_mrn`).
- **No Orphaned Records**: Foreign key cascades and explicit constraints prevent detached child records.
- **Append-Only Clinical History**: Clinical notes and prescriptions are never overwritten; modifications generate cryptographically referenced amendment records.
