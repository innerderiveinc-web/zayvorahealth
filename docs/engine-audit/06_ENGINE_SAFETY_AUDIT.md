# ZAYVORA HEALTH™ — Engine Clinical Safety & Regulatory Audit
## Forensic Verification of Safety Firewalls, Toxicology, Posology, and Guardrails
**Document ID:** ZAYV-AUD-ENG-06  
**Audit Standard:** CDSCO Software as a Medical Device (SaMD), AYUSH Drugs & Cosmetics Act 1940  
**Generated:** 2026-09-12T18:54:00+05:30  
**Scope:** Safety Barriers across all 25 ZAYVORA Engines  

---

## 1. Safety Architecture Overview

ZAYVORA HEALTH™ enforces a deterministic **Safety-First Invariant**:
> *"No artificial intelligence model, automated suggestion, or heuristic rule engine is permitted to bypass statutory toxicological limits, authorize Schedule E(1) poisons without certified Mudabbar detoxification, or autonomously issue a legally binding prescription."*

Every clinical recommendation is evaluated by **Engine 12 (Safety Firewall)** and gated behind the **Non-Delegable Clinician Barrier** (`safe_to_lock = False`).

---

## 2. Safety Firewall Audit Matrix (Engine 12)

The Safety Firewall (`services/therapeutic/app/engines/safety_firewall.py`) evaluates incoming prescription candidates across eight (8) mandatory dimensions:

| Dimension | Scope & Criteria | Blocking Severity | Firewall Output Behavior |
| :--- | :--- | :--- | :--- |
| **1. Allergy Screening** | Exact match on botanical name, Urdu synonym, or botanical family. | `CRITICAL` | `DO_NOT_RECOMMEND` (Blocks compile) |
| **2. Pregnancy & Lactation** | Emmenagogues, abortifacients, high-Daraja herbs (Daraja 3/4). | `CRITICAL` | `DO_NOT_RECOMMEND` (Immediate block) |
| **3. Age Screening** | Pediatric (<12 yrs) and Geriatric (>65 yrs) posology contraindications. | `MAJOR` | `NEEDS_CAUTION` or `DO_NOT_RECOMMEND` |
| **4. Drug-Herb Interactions** | 30+ verified interaction rules between Unani herbs and modern pharmaceuticals. | `CRITICAL` / `MAJOR` | `DO_NOT_RECOMMEND` or `NEEDS_CAUTION` |
| **5. Herb-Herb Antagonisms** | Opposing pharmacological actions or acute humoral clash (*Tazaad-e-Mizaj*). | `MODERATE` | `NEEDS_CAUTION` (Requires clinical justification) |
| **6. Schedule E(1) Poisons** | Verification of mandatory detoxification status (`is_mudabbar = True`). | `FATAL` | `DO_NOT_RECOMMEND` (Hard block) |
| **7. Posology Ceilings** | Single and daily dose bounds from Unani Pharmacopoeia of India. | `CRITICAL` | `DO_NOT_RECOMMEND` (Caps dose at maximum) |
| **8. Emergency Red Flags** | Acute life-threatening symptoms (chest pain, stroke, silent chest, severe sepsis). | `EMERGENCY` | `REFER` (Immediate hospital escalation) |

---

## 3. Comprehensive Drug-Herb Interaction Verification

The platform's deterministic interaction engine enforces 30+ critical cross-system interaction rules:

```
+---------------------------------------------------------------------------------------------------------------+
|                               AUDITED DRUG-HERB INTERACTION RULES (SAMPLE)                                    |
+----------------------+--------------------------+-----------------------+------------------+------------------+
| Modern Drug          | Botanical Agent          | Mechanism of Action   | Clinical Risk    | Verdict Enforced |
+----------------------+--------------------------+-----------------------+------------------+------------------+
| Warfarin / DOACs     | Zanjabeel (Ginger)       | COX-1 / Thromboxane   | Bleeding diathesis| DO_NOT_RECOMMEND |
| Warfarin / DOACs     | Asgandh (Ashwagandha)    | CYP2C9 modulation     | Altered INR      | NEEDS_CAUTION    |
| Digoxin              | Asal-us-Soos (Licorice)  | Aldosterone mimicry   | Hypokalemia/Arrh.| DO_NOT_RECOMMEND |
| Metformin / Insulin  | Karela / Jamun           | GLUT-4 upregulation   | Severe Hypoglyc. | NEEDS_CAUTION    |
| Lithium              | Badiyan (Fennel)         | Osmotic diuresis      | Lithium toxicity | NEEDS_CAUTION    |
| SSRIs / SNRIs        | Ustukhuddus (Lavender)   | Serotonergic agonism  | Serotonin syndr. | NEEDS_CAUTION    |
| Antihypertensives    | Asrol (Rauwolfia)        | Reserpine depletion   | Profound Hypotens| DO_NOT_RECOMMEND |
| Statins              | Filfil Siyah (Piperine)  | CYP3A4 inhibition     | Rhabdomyolysis   | NEEDS_CAUTION    |
| Sedatives / BDZs     | Afyun (Papaver)          | Central GABA agonism  | Resp. depression | DO_NOT_RECOMMEND |
| Anticoagulants       | Suranjan Talkh (Colchic.)| Tubulin inhibition    | Hemorrhagic risk | DO_NOT_RECOMMEND |
+----------------------+--------------------------+-----------------------+------------------+------------------+
```

---

## 4. Schedule E(1) Statutory Poison Verification

Under the Drugs and Cosmetics Rules, 1945 (Rule 161E), Schedule E(1) identifies poisonous substances of plant, mineral, and animal origin requiring special handling and detoxification (*Shodhana* / *Tadbeer*).

### Verified Schedule E(1) Substances in ZAYVORA:
1. **Suranjan Talkh** (*Colchicum luteum Baker*): High colchicine alkaloid content. Must undergo Mudabbar process (boiling in cow's milk or almond oil) before compounding. Maximum single dose: 250mg.
2. **Kuchla** (*Strychnos nux-vomica L.*): Strychnine content. Must be detoxified by boiling in cow's ghee or milk. Single dose capped at 65mg.
3. **Dhatura** (*Datura metel L.*): Scopolamine / hyoscyamine alkaloids. Toxic anticholinergic.
4. **Bhang / Qannab** (*Cannabis sativa L.*): Regulated narcotic. Must be processed with almond oil.
5. **Afyun** (*Papaver somniferum L.*): Morphine alkaloids. Strictly controlled.
6. **Bhilawa** (*Semecarpus anacardium L.f.*): Urushiol contact vesicant. Must be purified using brick powder and water washing.

### Architectural Enforcement:
- In `services/therapeutic/app/engines/dispensary_engine.py`, allocating an unverified Schedule E(1) batch throws `MudabbarDispenseBlockError`.
- In `services/therapeutic/app/engines/ebmr_engine.py`, stage sign-off requires entering the analytical Mudabbar Certificate Number before compounding can proceed.

---

## 5. Emergency Red Flag Escalation Protocol

The Differential Assessment Engine (`differential_engine.py`) and Hakeem Sahab (`hakeem_sahab.py`) maintain active screening for biomedical emergencies:

```
========================================================================================
 EMERGENCY RED FLAG ESCALATION RULES
========================================================================================
 Organ Axis         Red Flag Presentation                       Immediate Action Required
----------------------------------------------------------------------------------------
 Qalb-Dimagh        Chest pain radiating to arm/jaw, diaphoresis Emergency ECG / Troponin
 Dimagh-Aasab       Sudden facial droop, arm weakness, aphasia   Stroke code within 4.5h
 Riya-Sadr          Silent chest, cyanosis, PEFR < 33%           Emergency bronchodilator
 Meda-Amaa          Hematemesis, melena, acute rigid abdomen     Surgical consult / endoscopy
 Mafasil            Hot erythematous joint with high fever       Aspiration (Septic arthr.)
 Kulyah-Masana      Anuria, gross hematuria, severe renal colic  Renal ultrasound / CT
========================================================================================
 When any red flag is detected, Safety Firewall immediately sets verdict = "REFER"
 and suppresses traditional outpatient herbal recommendations.
========================================================================================
```

---

## 6. The Non-Delegable Prescribing Barrier

To prevent autonomous or unsafe automated prescribing:
1. **Compilation Lock:**
   The `compile_nuskha()` engine outputs `safe_to_lock = False` and `status = 'draft'`.
2. **REST Route Protection:**
   The `/api/v1/prescriptions/{id}/lock` endpoint requires a valid JWT with the `SENIOR_TABEEB` or licensed practitioner role.
3. **Database Integrity:**
   Prescriptions in `prescriptions` table cannot be dispatched by QSURA or dispensed by the pharmacy unless `status == 'locked'` and `signed_by_user_id IS NOT NULL`.

---

## 7. Safety Audit Verdict

```
+---------------------------------------------------------------------------------------+
|                             SAFETY FIREWALL AUDIT VERDICT                             |
|                                                                                       |
|   STATUS: PASSED (ZERO P0/P1 RISKS OPEN)                                              |
|                                                                                       |
|   - 100% of Prescription Pipelines Covered by Deterministic Interceptor               |
|   - All 6 Statutory Schedule E(1) Poisons Hard-Gated with Mudabbar Verification       |
|   - Non-Delegable Clinician Prescribing Barrier Architecturally Enforced               |
|   - Emergency Red Flags Trigger Immediate Autonomous REFER Verdict                    |
+---------------------------------------------------------------------------------------+
```
