export interface FaqItem {
  id: string;
  category: "Unani Medicine" | "Consultations" | "Safety & Quality" | "Pharmacy & Delivery";
  question: string;
  answer: string;
}

export const FAQS_DATA: FaqItem[] = [
  {
    id: "faq-1",
    category: "Unani Medicine",
    question: "What is ZAYVORA Health and how does the Modern Unani Care System work?",
    answer: "ZAYVORA Health combines classical Greco-Arab Unani medicine with modern clinical understanding, digital patient tracking, and clinician-supervised care. We evaluate each patient's unique constitutional temperament (Mizaj) and organ-axis function to deliver structured, non-invasive dietary, lifestyle (Asbab-e-Sittah), and botanical care pathways."
  },
  {
    id: "faq-2",
    category: "Unani Medicine",
    question: "How is Unani medicine different from other traditional systems?",
    answer: "Unani Tibb is rooted in the humoral theory established by Hippocrates, Galen, and Avicenna. It views health as an equilibrium among four bodily humors (Blood, Phlegm, Yellow Bile, Black Bile). Diagnosis relies heavily on the 10 dimensions of pulse (10-Ajnas Nabz), tongue inspection (Lisan), and physical signs, with treatment emphasizing the body's self-healing faculty (Tabi'at)."
  },
  {
    id: "faq-3",
    category: "Consultations",
    question: "How does an appointment with a ZAYVORA physician work?",
    answer: "You can book an Online Video Consultation or an In-Clinic OPD visit at Jamia Hamdard AUTC - Main Hospital. After completing your health history, our certified Tabeeb assesses your constitution, reviews any existing lab reports, and creates a tailored 4-phase care plan with follow-up milestones."
  },
  {
    id: "faq-4",
    category: "Consultations",
    question: "Can I consult for chronic conditions like PCOS, Fatty Liver, or Joint Pain?",
    answer: "Yes. Our clinical team specializes in multi-week structured reversal programs for metabolic disorders, musculoskeletal complaints (Waja-ul-Mafasil), female hormonal imbalances (PCOS), and male reproductive health."
  },
  {
    id: "faq-5",
    category: "Safety & Quality",
    question: "Are ZAYVORA formulations tested for safety and heavy metals?",
    answer: "Yes. Every batch undergoes rigorous inductively coupled plasma mass spectrometry (ICP-MS) to confirm heavy metals (lead, arsenic, mercury, cadmium) are well below statutory limits (<0.05 ppm). Formulations are produced in GMP-certified cleanrooms."
  },
  {
    id: "faq-6",
    category: "Safety & Quality",
    question: "What is 'Mudabbar' detoxification?",
    answer: "In classical Unani pharmacology, potent or mineral ingredients must undergo traditional purification protocols called Mudabbar (such as boiling in milk or cow ghee) to neutralize potential toxicity and enhance therapeutic efficacy. ZAYVORA mandates that Schedule E(1) ingredients are released only with verified analytical Mudabbar certification."
  },
  {
    id: "faq-7",
    category: "Pharmacy & Delivery",
    question: "Do I need a prescription to order ZAYVORA products?",
    answer: "Retail wellness teas and dietary supplements can be purchased directly. However, specialized classical formulations (such as Qurs Taqwiyat-e-Mani or Majun Suranjan) require clinician review and digital signature under 21 CFR Part 11 protocols."
  },
  {
    id: "faq-8",
    category: "Pharmacy & Delivery",
    question: "How does FEFO delivery work for medicines?",
    answer: "Our dispensary operates on a strict First-Expiry, First-Out (FEFO) automated allocation protocol. Temperature-sensitive botanical preparations are dispatched in monitored cold-chain packaging ensuring complete therapeutic integrity upon arrival."
  }
];
