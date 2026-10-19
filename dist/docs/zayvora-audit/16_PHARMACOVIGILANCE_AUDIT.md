# ZAYVORA HEALTH™ — Production Readiness Audit
## 16. Pharmacovigilance & Adverse Drug Reaction (ADR) Audit
*Tagline: “Ancient Wisdom. Modern Science. Intelligent Care.”*

---

### 1. Scope & Causality Assessment
The Pharmacovigilance subsystem monitors post-market formulation safety:
- **Intake**: Standardized reporting of adverse events.
- **Causality Algorithm**: Implementation of WHO-UMC (Uppsala Monitoring Centre) causality categories: Certain, Probable, Possible, Unlikely, Conditional, Unassessable.

---

### 2. Findings

#### Finding PV-01: WHO-UMC Causality Assessment Engine
1. **Feature/module name**: Pharmacovigilance Causality Assessment
2. **Expected behavior**: Deterministically scores drug-event relationships based on timing, dechallenge, and rechallenge criteria.
3. **Actual implementation status**: Implemented in `care_plans.py` router under `POST /care-plans/pharmacovigilance/evaluate`.
4. **Evidence**:
   - **file path**: `services/therapeutic/app/routers/care_plans.py`
   - **function/class/component**: `evaluate_pharmacovigilance()`, `_calculate_who_umc_causality()`
   - **API route**: `POST /api/v1/therapeutic/care-plans/pharmacovigilance/evaluate`
   - **database table**: `unified_care_plans`
   - **test result**: `test_care_plans_and_pharmacovigilance.py` — PASSED (6/6 tests passing)
5. **Status**: FULLY IMPLEMENTED
6. **Severity**: P1 High
7. **Recommended fix**: Add automated export in CIOMS / MedDRA format for statutory filing.
8. **Dependencies**: `services/therapeutic`
9. **Acceptance criteria**: Evaluates adverse event reports and assigns consistent WHO-UMC causality category.
