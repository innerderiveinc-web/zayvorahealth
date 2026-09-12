# ZAYVORA Health OS™ — 25 Clinical Engines Forensic Audit
**Document ID**: `AUDIT-ENG-07`  
**Target**: Clinical, Therapeutic, and Knowledge Engines  
**Standard**: Level 4 Clinically Governed End-to-End Automation  

---

## 1. 25-Engine Verification Matrix

| # | Engine Name | Implementation Path | Automation Level | Statutory Clinician Gate | Unit Test Status |
|---|---|---|---|---|---|
| 1 | Unani Intelligence | `services/clinical/app/engines/` | Level 4 Governed | Mandatory Sign-off | **PASS** |
| 2 | Biomedical Intelligence | `services/clinical/app/engines/` | Level 4 Governed | Mandatory Sign-off | **PASS** |
| 3 | ZAYVORA Knowledge Base (ZKB) | `services/knowledge/app/core/` | Level 4 Governed | 3/3 Quorum Gate | **PASS** |
| 4 | Mufradat Intelligence | `services/knowledge/app/core/` | Level 4 Governed | Monograph Approval | **PASS** |
| 5 | Murakkabat Formulation | `services/therapeutic/app/engines/` | Level 4 Governed | Formula Verification | **PASS** |
| 6 | Mizaj Assessment | `services/clinical/app/engines/mizaj_assessor.py` | Level 4 Governed | Clinician Review | **PASS** |
| 7 | Organ-Axis Cross-talk | `services/clinical/app/engines/organ_axis_engine.py`| Level 4 Governed | Clinician Review | **PASS** |
| 8 | Nuskha Nawisi Draft | `services/therapeutic/app/engines/nuskha_compiler.py`| Level 4 Governed | Mandatory Sign-off | **PASS** |
| 9 | Hakeem Sahab Copilot | `services/ai/app/engines/hakeem_sahab.py` | Level 4 Governed | Advisory Only | **PASS** |
| 10 | ZAPE Personalization | `services/ai/app/engines/zape_personalization.py` | Level 4 Governed | Clinician Approval | **PASS** |
| 11 | Evidence Intelligence | `services/knowledge/app/core/evidence_engine.py` | Level 4 Governed | Peer Review | **PASS** |
| 12 | Safety Firewall | `services/therapeutic/app/engines/safety_firewall.py`| Deterministic Rule | Hard-lock Interception| **PASS** |
| 13 | Differential Assessment | `services/clinical/app/engines/differential_engine.py`| Level 4 Governed | Clinician Review | **PASS** |
| 14 | Ilaj bil-Dawa | `services/therapeutic/app/engines/nuskha_compiler.py`| Level 4 Governed | Mandatory Sign-off | **PASS** |
| 15 | Ilaj bil-Tadbeer | `services/therapeutic/app/engines/tadbeer_guardrails.py`| Level 4 Governed | Regimen Consent | **PASS** |
| 16 | Ilaj bil-Ghiza | `services/therapeutic/app/routers/ghiza.py` | Level 4 Governed | Dietitian Sign-off | **PASS** |
| 17 | Patient 360 / Timeline | `services/clinical/app/routers/timeline.py` | Level 4 Governed | Identity Bound | **PASS** |
| 18 | Follow-up & Outcomes | `services/clinical/app/workers/proms_followup_worker.py`| Level 4 Governed | Automated Trigger | **PASS** |
| 19 | Pharmacovigilance | `services/therapeutic/app/pharmacovigilance/` | Level 4 Governed | Regulatory E2B Gate | **PASS** |
| 20 | Pharmacy Inventory | `services/therapeutic/app/engines/dispensary_engine.py`| Level 4 Governed | FEFO & Detox Lock | **PASS** |
| 21 | Manufacturing eBMR | `services/therapeutic/app/engines/ebmr_engine.py` | Level 4 Governed | QA Release Sign-off | **PASS** |
| 22 | AI / RAG Retrieval | `services/knowledge/app/core/hybrid_rag.py` | Level 4 Governed | Approved Sources Only| **PASS** |
| 23 | Knowledge Graph | `services/knowledge/app/graph/neo4j_repository.py` | Level 4 Governed | Provenance Chained | **PASS** |
| 24 | Clinical Governance | `services/clinical/app/governance/` | Level 4 Governed | 21 CFR Part 11 Audit | **PASS** |
| 25 | Notification Center | `services/clinical/app/qsura/communication_broker.py`| Level 4 Governed | Event-Driven Bus | **PASS** |

---

## 2. Statutory Safety Gates
1. **Schedule E(1) Mudabbar Gate**: Toxic botanical ingredients (*Suranjan Talkh*, *Kuchla*, *Aconite*) cannot be dispensed without authenticated detoxification hash verification.
2. **Deterministic Herb-Drug Matrix**: Over 30 established drug-herb interaction rules (e.g., Warfarin + *Zanjabeel*, SSRIs + *Ustukhuddus*) evaluated by pure deterministic code.
3. **Emergency Red Flag Freeze**: Immediate escalation on critical vital signs (e.g. SBP > 180, severe acute chest pain).
