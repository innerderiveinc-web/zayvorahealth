# ZAYVORA Algorithmic Personalization Engine (ZAPE 2.0) — Context Injection Template
*Multi-Factor Clinical Context Adaptation for Hakeem Sahab™ Copilot*

```markdown
### ZAPE 2.0 Algorithmic Patient Context Payload

Patient Demographic & Functional Context:
- Age: {patient_age} years | Biological Category: {age_category} (Pediatric / Adult / Geriatric)
- Biological Sex: {patient_gender} | Pregnancy / Trimester: {pregnancy_status}
- Weight / BMI: {patient_weight_kg} kg / {patient_bmi}

Mizaj (Temperamental Assessment - 10 Ajnas):
- Primary Temperament: {mizaj_primary} (Degree: {mizaj_degree})
- Secondary Temperament: {mizaj_secondary}
- Quwa Status: {quwa_status} (Qawi / Motadil / Dha'eef)

Biomedical Organ Function & Lab Markers:
- Serum Creatinine: {serum_creatinine} mg/dL
- Calculated eGFR (CKD-EPI): {egfr_value} mL/min/1.73m² (Renal Stage: {renal_stage})
- Active Comorbidities: {comorbidities_list}
- Documented Allergies: {allergies_list}
- Current Pharmaceutical Medications: {current_allopathic_medications}

Environmental & Chronobiological Factors (Asbab #1 & #6):
- Season (Fasl): {current_season} (Rabi' / Saif / Khareef / Shita)
- Geographical Climate: {geographical_climate}
- Ambient Temperature / Moisture: {ambient_weather_conditions}

ZAPE Titration Multipliers Applied:
- Age Scaling Factor: {age_scaling_factor}
- Renal Scaling Factor: {renal_scaling_factor}
- Net Active Compound Scaling Factor: {net_posology_scaling_factor}
- Mandatory Musleh Correctives: {recommended_musleh_list}
- Contraindicated Botanicals / Minerals: {contraindicated_drugs_list}
```
