/**
 * ZAYVORA Health™ — Central Medical & Unani Terminology Dictionary
 * 
 * Provides dual-layer clinical definitions ensuring every specialized Unani
 * concept is medically sound and clearly comprehensible to patients without
 * sacrificing classical clinical depth.
 * 
 * All classical terms are maintained in standardized Latin/English transliteration
 * with clinical and plain-language English correlations.
 */

export interface TerminologyEntry {
  canonicalId: string;
  unaniTerm: string;
  transliteration: string;
  patientPlainLanguage: string;
  clinicalBiomedicalCorrelation: string;
  governanceNote?: string;
}

export const CENTRAL_TERMINOLOGY_DICTIONARY: Record<string, TerminologyEntry> = {
  MIZAJ: {
    canonicalId: "MIZAJ",
    unaniTerm: "Mizaj",
    transliteration: "Mizaj",
    patientPlainLanguage: "Constitutional Temperament (your unique baseline metabolic and physical tendency)",
    clinicalBiomedicalCorrelation: "Individual metabolic phenotype, neuroendocrine reactivity, and homeostatic setpoint",
    governanceNote: "Classified into Damawi (Sanguinous), Balghami (Phlegmatic), Safrawi (Choleric), and Saudawi (Melancholic)."
  },
  SU_E_MIZAJ: {
    canonicalId: "SU_E_MIZAJ",
    unaniTerm: "Su-e-Mizaj",
    transliteration: "Su-e-Mizaj",
    patientPlainLanguage: "Temperamental Imbalance (acquired deviation causing symptoms or tissue vulnerability)",
    clinicalBiomedicalCorrelation: "Pathological dyscrasia, localized inflammatory state, or metabolic dysregulation"
  },
  MUFRADAT: {
    canonicalId: "MUFRADAT",
    unaniTerm: "Mufradat",
    transliteration: "Mufradat",
    patientPlainLanguage: "Single Medicinal Substances (whole botanical, mineral, or natural ingredients)",
    clinicalBiomedicalCorrelation: "Uncompounded pharmacopoeial crude botanical or mineral drugs standardized to active phytoconstituents"
  },
  MURAKKABAT: {
    canonicalId: "MURAKKABAT",
    unaniTerm: "Murakkabat",
    transliteration: "Murakkabat",
    patientPlainLanguage: "Classical Compound Formulations (synergistic multi-herb preparations)",
    clinicalBiomedicalCorrelation: "Standardized poly-herbal pharmacopoeial formulations codified in National Formulary of Unani Medicine (NFUM)"
  },
  NUSKHA: {
    canonicalId: "NUSKHA",
    unaniTerm: "Nuskha",
    transliteration: "Nuskha",
    patientPlainLanguage: "Individualized Clinical Prescription (customized medicine and dosage order)",
    clinicalBiomedicalCorrelation: "Clinician-authorized therapeutic order incorporating posology, administration vehicle (anupan), and duration"
  },
  ILAJ_BIL_TADBEER: {
    canonicalId: "ILAJ_BIL_TADBEER",
    unaniTerm: "Ilaj-bil-Tadbeer",
    transliteration: "Ilaj-bil-Tadbeer",
    patientPlainLanguage: "Regimenal Therapy (physical therapeutic procedures such as cupping, massage, or medicated bath)",
    clinicalBiomedicalCorrelation: "Non-pharmacological physical modalities modulating autonomic tone, lymphatic drainage, and regional microcirculation"
  },
  ILAJ_BIL_GHIZA: {
    canonicalId: "ILAJ_BIL_GHIZA",
    unaniTerm: "Ilaj-bil-Ghiza",
    transliteration: "Ilaj-bil-Ghiza",
    patientPlainLanguage: "Nutritional & Dietary Therapy (individualized meal directives based on constitutional balance)",
    clinicalBiomedicalCorrelation: "Targeted macronutrient and micronutrient modulation designed to alter systemic inflammatory and metabolic markers"
  },
  ILAJ_BIL_DAWA: {
    canonicalId: "ILAJ_BIL_DAWA",
    unaniTerm: "Ilaj-bil-Dawa",
    transliteration: "Ilaj-bil-Dawa",
    patientPlainLanguage: "Pharmacotherapy (treatment using standardized herbal formulations)",
    clinicalBiomedicalCorrelation: "Evidence-informed administration of standardized botanical therapeutics"
  },
  ASBAB_E_SITTA: {
    canonicalId: "ASBAB_E_SITTA",
    unaniTerm: "Asbab-e-Sitta Zarooriya",
    transliteration: "Asbab-e-Sitta Zarooriya",
    patientPlainLanguage: "Six Essential Health Factors (Air, Diet, Movement, Sleep, Evacuation, and Mental State)",
    clinicalBiomedicalCorrelation: "Longitudinal lifestyle determinants of health: environmental exposure, nutrition, physical activity, sleep physiology, excretion, and psychosomatic stress"
  },
  TANQIYA: {
    canonicalId: "TANQIYA",
    unaniTerm: "Tanqiya",
    transliteration: "Tanqiya",
    patientPlainLanguage: "Therapeutic Evacuation / Humoral Cleansing (guided elimination of metabolic byproducts)",
    clinicalBiomedicalCorrelation: "Phase 1 coction and elimination of accrued morbid metabolites prior to tissue rejuvenation",
    governanceNote: "Never refer to this as a generic commercial 'detox'."
  },
  TADEEL: {
    canonicalId: "TADEEL",
    unaniTerm: "Ta'deel",
    transliteration: "Ta'deel",
    patientPlainLanguage: "Humoral Normalization (re-establishing baseline constitutional equilibrium)",
    clinicalBiomedicalCorrelation: "Phase 2 homeostatic correction and inflammatory resolution"
  },
  TAQWIYAT: {
    canonicalId: "TAQWIYAT",
    unaniTerm: "Taqwiyat",
    transliteration: "Taqwiyat",
    patientPlainLanguage: "Organ Toning & Strengthening (enhancing intrinsic tissue resilience)",
    clinicalBiomedicalCorrelation: "Phase 3 restorative adaptation and mitochondrial/cellular resilience strengthening"
  },
  MUDABBAR: {
    canonicalId: "MUDABBAR",
    unaniTerm: "Mudabbar",
    transliteration: "Mudabbar",
    patientPlainLanguage: "Pharmaceutical Purification (classical detoxification processing for potent botanical substances)",
    clinicalBiomedicalCorrelation: "Mandatory Schedule E(1) alkaloid mitigation process verified via chemical assay prior to dispensing"
  },
  NABZ: {
    canonicalId: "NABZ",
    unaniTerm: "Nabz",
    transliteration: "Nabz",
    patientPlainLanguage: "Arterial Pulse Examination (evaluating pulse dynamics across classical tactile qualities)",
    clinicalBiomedicalCorrelation: "Hemodynamic arterial pulse examination reflecting vascular compliance, stroke volume, and autonomic cardiovascular regulation"
  }
};

/**
 * Resolves a dual-layer term based on target audience: 'patient' or 'clinician'.
 */
export function resolveTerm(key: keyof typeof CENTRAL_TERMINOLOGY_DICTIONARY, audience: "patient" | "clinician" = "patient"): string {
  const entry = CENTRAL_TERMINOLOGY_DICTIONARY[key];
  if (!entry) return key;
  if (audience === "patient") {
    return `${entry.transliteration} (${entry.patientPlainLanguage})`;
  }
  return `${entry.transliteration} — ${entry.clinicalBiomedicalCorrelation}`;
}
