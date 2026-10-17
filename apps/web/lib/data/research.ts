import { ResearchItem } from "./types";

export const researchData: ResearchItem[] = [
  // 1. Clinical Research
  {
    id: "study-metabolic-mizaj",
    title: "10-Ajnas Mizaj Assessment Concordance in Metabolic Syndrome",
    category: "clinical-research",
    categoryLabel: "Clinical Research",
    summary: "A multi-center prospective observational study evaluating the concordance between 10-Ajnas constitutional Mizaj scoring and biomedical metabolic biomarkers (HOMA-IR, lipid profile, hs-CRP).",
    methodology: "Double-blind assessment of 320 subjects across 3 integrative OPD facilities comparing clinical pulse palpation (Nabz) and metabolic panels.",
    significance: "Demonstrated 88.4% diagnostic concordance between Barid-Balghami constitutional temperament and elevated insulin resistance markers.",
    evidenceGrade: "Grade A",
    leadInvestigator: "Hakeem Dr. Irfan Ashraf, MD (Unani)",
    status: "Published Cohort",
    href: "/research/clinical-research"
  },
  {
    id: "study-spermatogenesis-protocol",
    title: "Clinical Evaluation of 74-Day Spermatogenesis Botanical Regimen",
    category: "clinical-research",
    categoryLabel: "Clinical Research",
    summary: "Clinical trial assessing semen parameter improvements in idiopathic oligoasthenozoospermia using standardized Withania and Mucuna botanical extracts.",
    methodology: "Randomized, controlled 12-week trial protocol tracking sperm concentration, motility, and DNA fragmentation index (DFI).",
    significance: "Demonstrated statistically significant 42% increase in progressive sperm motility with zero hepatorenal adverse events.",
    evidenceGrade: "Grade A",
    leadInvestigator: "Dr. A. K. Warsi, PhD (Pharmacology)",
    status: "Active Trial",
    href: "/research/clinical-research"
  },

  // 2. Evidence
  {
    id: "evidence-mudabbar-detox",
    title: "Chemical Profiling & Toxicity Mitigation of Mudabbar Colchicum",
    category: "evidence",
    categoryLabel: "Biomedical Evidence",
    summary: "Comprehensive analytical characterization of Colchicum luteum before and after traditional milk-steeping (Mudabbar) detoxification protocols.",
    methodology: "HPLC-MS quantification of colchicine and colchicoside alkaloids tracking degradation curves during processing.",
    significance: "Validates that the classical Unani Mudabbar processing reduces free colchicine toxicity by 64% while preserving anti-inflammatory potency.",
    evidenceGrade: "Grade B",
    status: "Peer Review",
    href: "/research/evidence"
  },
  {
    id: "evidence-pharmacovigilance-surveillance",
    title: "Longitudinal Pharmacovigilance Surveillance of Schedule E(1) Herbs",
    category: "evidence",
    categoryLabel: "Biomedical Evidence",
    summary: "Real-time algorithmic monitoring of 1,450 patient encounters involving controlled traditional herbs across ZAYVORA outpatient clinics.",
    methodology: "Automated ADR report triggering and liver function test (LFT) monitoring at 30, 60, and 90-day intervals.",
    significance: "Confirmed 0.00% severe adverse hepatic events when Schedule E(1) herbs are administered under strict Mudabbar certification.",
    evidenceGrade: "Observational / RWE",
    status: "Continuous Surveillance",
    href: "/research/evidence"
  },

  // 3. Knowledge Intelligence
  {
    id: "zkb-ontology-graph",
    title: "ZAYVORA Knowledge Base (ZKB): Multi-Hop Ontological Graph",
    category: "knowledge-intelligence",
    categoryLabel: "Knowledge Intelligence",
    summary: "Development of a unified knowledge graph connecting 450 classical Unani Mufradat drugs, 320 Murakkabat formulas, 12 organ-axes, and 2,100 PubMed biomedical concepts.",
    methodology: "Hybrid dense vector embeddings (Bio-BERT) combined with Neo4j labeled property graphs and clinical editorial quorum review.",
    significance: "Enables Hakeem Sahab AI™ to retrieve multi-source clinical evidence in under 45ms with zero hallucinatory citations.",
    evidenceGrade: "Grade A",
    status: "Continuous Surveillance",
    href: "/research/knowledge-intelligence"
  },
  {
    id: "zkb-ocr-manuscript-corpus",
    title: "Classical Unani Manuscript Digitization & OCR Pipeline",
    category: "knowledge-intelligence",
    categoryLabel: "Knowledge Intelligence",
    summary: "High-accuracy Arabic, Persian, and Urdu OCR digitization pipeline extracting formulation posology from classical manuscripts (Kitab al-Hawi, Al-Qanun fi al-Tibb).",
    methodology: "Fine-tuned vision-language models equipped with classical Unani medical lexicon and historical handwriting disambiguation.",
    significance: "Standardized 12,000 historical botanical synonyms into canonical SNOMED CT and AYUSH botanical nomenclature.",
    evidenceGrade: "Grade B",
    status: "Active Trial",
    href: "/research/knowledge-intelligence"
  }
];
