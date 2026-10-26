# ZAYVORA Health OS™ — Clinical Engines

**25 Engines · Status Matrix**

| ID | Engine | Module | Status | Coverage | safe_to_lock |
|:---|:---|:---|:---|:---|:---|
| E01 | Mizaj Engine | Clinical | Partially Automated | 85% | Yes (AI flag) |
| E02 | Organ-Axis Mapper | Clinical | Rule-Based | 70% | Yes |
| E03 | Hakeem Sahab AI™ | AI | AI-Assisted | 60% | No — human sign-off mandatory |
| E04 | Safety Gate (Schedule E1) | Therapeutic | Fully Automated | 100% | Yes |
| E05 | Nuskha Composer | Clinical | AI-Assisted | 55% | No — draft only |
| E06 | Mizaj-to-Herb Matcher | Therapeutic | Rule-Based | 78% | Yes |
| E07 | Evidence Ranker | Knowledge | Mocked | 20% | No |
| E08 | ZKI Safety Validator | Knowledge | Partially Automated | 72% | Yes |
| E09 | Dosage Calculator | Therapeutic | Rule-Based | 90% | Yes |
| E10 | Drug Interaction Checker | Therapeutic | Partially Automated | 65% | Yes |
| E11 | Teleconsult Engine | Clinical | Mocked | 10% | N/A |
| E12 | Patient 360 Aggregator | Clinical | Partially Automated | 68% | Yes |
| E13 | Appointment Scheduler | Receptionist | Rule-Based | 80% | Yes |
| E14 | Queue Manager | Receptionist | Fully Automated | 95% | Yes |
| E15 | eBMR / Prescription Lock | Clinical | Partially Automated | 75% | Yes (HMAC) |
| E16 | Pharmacy Dispensing | Pharmacy | Manual | 40% | Yes |
| E17 | Billing Engine | Enterprise | Not Connected | 0% | N/A |
| E18 | Analytics Engine | Research | Mocked | 30% | N/A |
| E19 | Notification Service | Mobile | Partially Automated | 60% | N/A |
| E20 | Audit Logger | Security | Fully Automated | 100% | Yes |
| E21 | MFA / Auth Engine | Identity | Fully Automated | 100% | Yes |
| E22 | Vault Secret Manager | Infrastructure | Not Connected | 0% | N/A |
| E23 | Mudabbar Detox Gate | Manufacturing | Partially Automated | 70% | Yes |
| E24 | Knowledge Graph (Neo4j) | Knowledge | Not Connected | 0% | N/A |
| E25 | GDPR / Privacy Engine | Identity | Fully Automated | 90% | Yes |

## Status Definitions

- **Fully Automated** — Engine runs without human intervention for normal cases
- **Partially Automated** — Engine assists but requires clinician confirmation
- **AI-Assisted** — LLM involved; `safe_to_lock=False` always applies
- **Rule-Based** — Deterministic logic, no LLM
- **Manual** — UI provided; automation not implemented
- **Mocked** — Returns plausible mock data; not connected to real data source
- **Not Connected** — Integration not yet implemented

## Safety Invariant

Any engine with `safe_to_lock=No` **cannot** generate a signed prescription autonomously.
A licensed Hakeem or physician must review and manually sign all AI-assisted clinical outputs.
