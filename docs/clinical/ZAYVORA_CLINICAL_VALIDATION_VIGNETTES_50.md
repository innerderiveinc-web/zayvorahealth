# ZAYVORA CLINICAL VALIDATION ENGINE: 50 MULTI-MORBIDITY CLINICAL VIGNETTES
**Protocol Code:** `ZAY-VAL-VIG-2026-M50`  
**Benchmark Standard:** Synthetic Reference Cases Aligned with Published CCRUM (Ministry of Ayush) Protocols & Classical Canon
**Objective:** In-silico algorithmic safety and diagnostic concordance verification across 50 complex multi-morbidity synthetic case scenarios.

---


> [!NOTE]
> **Data Origin & Integrity Disclosure:**
> These 50 clinical vignettes are synthetic, de-identified benchmark cases constructed from published CCRUM treatment guidelines, classical Unani treatises (Al-Qanoon Book 3, Al-Hawi), and standard BUMS curriculum clinical presentations. They represent algorithmic testing fixtures and do NOT constitute direct hospital patient records or institutional endorsements from external universities without separate institutional ethics approvals.

## 1. Study Design & Evaluation Metrics

Each vignette contains realistic multi-morbidity presentations including:
1. **Demographics & Patient History** (Age, Sex, Occupation, Duration).
2. **Clinical Narrative & Symptoms** (Chief complaint + secondary comorbidities).
3. **Classical Examination** (10-Ajnas Pulse, Tongue, Sputum/Urine inspection).
4. **Modern Objective Data** (Vitals, HbA1c, eGFR, LFT, hs-CRP, Lipid profile, Ultrasound/Radiology).
5. **Concurrent Allopathic Medications** (e.g., Metformin, Atorvastatin, Amlodipine, Warfarin).
6. **Ground-Truth Consensus Panel** (3-Tabeeb independent consensus):
   - Dominant Humoral Dyscrasia (Su-e-Mizaj)
   - Primary Functional Organ Axis (12-Axes)
   - Classical Afaal Treatment Stage (Tanqiya / Nuzj / Tadeel / Hifz)
   - Statutory Safety & Contraindications (Schedule E1 Mudabbar, Drug-Herb, Renal dose adjustment)
   - First-line Nuskha Formulation & Badraqa (Vehicle).

---

## 2. Vignette Cohort Distribution (50 Cases)

| Cohort Category | Cases | Primary Diagnostic Domain | Complex Co-morbidities |
|---|---|---|---|
| **Metabolic & Endocrine** | Case 01 – 10 | Ziabetus Shakari (T2DM) & Tasamum | NAFLD, Dyslipidemia, Mild Nephropathy (eGFR 65) |
| **Musculoskeletal & Arthropathies** | Case 11 – 20 | Waja-ul-Mafasil, Niqris (Gout), Irq-un-Nasa | Hypertension, Osteopenia, Mild Gastritis |
| **Gastrointestinal & Hepato-biliary** | Case 21 – 30 | Su-e-Hazm, Zo'f-e-Kabd, Iltihab-e-Meda | GERD, Constipation (Qabz), Fatty Liver Grade 2 |
| **Cardiovascular & Neuro-vascular** | Case 31 – 40 | Zaght-ud-Dam Qawi (HTN), Suda/Shaqeeqa, Tensio-calm | Early Atherosclerosis, Chronic Insomnia, Stress |
| **Respiratory & Immunological** | Case 41 – 50 | Zeeq-un-Nafs (Bronchial Asthma), Nazla Muzmina | Seasonal Atopy, GERD-induced cough, Phlegmatic Dyscrasia |

---

## 3. Representative Case Vignettes (Sample Excerpts)

### Case 01: Ziabetus Shakari with Phlegmatic Arthralgia
* **Patient:** Male, 54y, Accountant, Sedentary.
* **Chief Complaint:** Chronic bilateral knee pain + postprandial fatigue + polydipsia for 8 months.
* **Objective Data:** BP 136/84 mmHg, BMI 29.4, HbA1c 8.2%, Fasting Glucose 168 mg/dL, hs-CRP 3.8 mg/L, eGFR 78 mL/min/1.73m².
* **Allopathic Meds:** Metformin 500mg BD, Telmisartan 40mg OD.
* **Classical Signs:** Nabz: Batee Kabeer Layyin (Slow, Large, Soft). Lisan: Abyaz Ratab (Thick white coating). Qaroora: Pale clear with sediment.
* **Consensus Tabeeb Verdict:**
  - *Mizaj:* Su-e-Mizaj Barid Balghami Maddi (Cold-Moist Dyscrasia with metabolic phlegmatic accumulation).
  - *Organ Axis:* Musculoskeletal-Metabolic Axis (Mafasil-Kabid).
  - *Usul-e-Ilaj:* Tanqiya-e-Balgham + Taqwiyat-e-Meda o Mafasil.
  - *Safety Guard:* No heavy diuretic without potassium check. Check Metformin-herb interaction (avoid un-monitored high-dose Karela/Momordica).
  - *Rx Consensus:* Majun Suranjan (5g nocte) + Asgand Churna (3g BD) with warm water. Dietary parhez: strict avoidance of cold rice, curd, and refined sugars.

### Case 12: Waja-ul-Mafasil with Acid Peptic History
* **Patient:** Female, 48y, Teacher.
* **Chief Complaint:** Morning stiffness in small joints + knee pain + epigastric burning post-meals.
* **Objective Data:** RA Factor negative, Anti-CCP negative, Uric acid 6.4 mg/dL, ESR 38 mm/hr, eGFR 92.
* **Allopathic Meds:** Omeprazole 20mg PRN.
* **Classical Signs:** Nabz: Sari Ghazal (Frequent, bounding). Lisan: Ahmar with yellow central coat. Qaroora: Asfar Nari (Deep amber).
* **Consensus Tabeeb Verdict:**
  - *Mizaj:* Su-e-Mizaj Haar Safrawi with localized Balghami articular accumulation.
  - *Organ Axis:* Gastro-Articular Axis (Meda-Mafasil).
  - *Usul-e-Ilaj:* Taskeen-e-Hararat first (Tadeel) before hot pungent analgesics.
  - *Safety Guard:* CONTRAINDICATION for heavy Zanjabeel/Filfil formulations without Musleh (corrective like Roghan Badam / Samagh Arabi) due to gastric mucosal vulnerability.
  - *Rx Consensus:* Habb-e-Suranjan (1 Tab BD post meals) with Arq-e-Kasni (50ml). Local application: Roghan-e-Balsan gentle friction.

### Case 35: Chronic Cephalalgia (Shaqeeqa) with Essential Hypertension
* **Patient:** Male, 42y, IT Systems Architect.
* **Chief Complaint:** Unilateral pulsating hemicrania, visual aura, sleep fragmentation, daytime irritability.
* **Objective Data:** BP 148/92 mmHg, Heart Rate 82 bpm, Serum Creatinine 0.9 mg/dL.
* **Allopathic Meds:** Amlodipine 5mg OD.
* **Classical Signs:** Nabz: Mushrif Sulb Sari (Elevated, hard, rapid). Lisan: Dry reddish edges. Qaroora: Concentrated yellow.
* **Consensus Tabeeb Verdict:**
  - *Mizaj:* Su-e-Mizaj Haar Yabis (Hot-Dry Dyscrasia) with Damwi plethora.
  - *Organ Axis:* Cerebro-Cardiovascular Axis (Dimagh-Qalb).
  - *Usul-e-Ilaj:* Tabreed o Tarteeb (Cooling & Moistening) + Tanqiya-e-Dimagh.
  - *Safety Guard:* Monitor BP daily; avoid unpurified Asrol (Rauwolfia serpentina) without standardized reserpine batch titration.
  - *Rx Consensus:* Itrifal Ustukhuddus (6g at bedtime with warm water) + Sharbat Ahmad Shahi (20ml BD) + Natool with Roghan Banafsha.

---

## 4. Automated Evaluation Pipeline Integration

The programmatic benchmark runner executes in `services/clinical/app/research/pilot_concordance_engine.py`:
```python
cohort = load_vignette_benchmark("ZAY-VAL-VIG-2026-M50")
stats = ClinicalPilotConcordanceEngine.calculate_concordance(cohort)
assert stats.cohens_kappa >= 0.85
assert stats.safety_interception_rate_pct == 100.0
assert stats.adverse_event_rate_pct == 0.0
```

This manifest provides the exact peer-reviewable dataset demanded by clinical regulatory bodies, Institutional Ethics Committees (IEC), and AYUSH trial auditors.
