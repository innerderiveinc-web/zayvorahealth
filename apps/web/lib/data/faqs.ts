import { FaqItem } from "./types";

export const faqsData: FaqItem[] = [
  // General
  {
    id: "faq-what-is-zayvora",
    category: "General",
    question: "What is ZAYVORA Health™?",
    answer: "ZAYVORA Health™ is an independent healthcare organization delivering evidence-based clinical care, botanical pharmaceuticals, and health technology. Our clinical care model integrates classical Unani Medicine (Tibb-e-Unani) with modern biomedical diagnostic intelligence under strict clinician governance."
  },
  {
    id: "faq-what-is-zayvora-os",
    category: "General",
    question: "What is ZAYVORA Health OS™?",
    answer: "ZAYVORA Health OS™ is our proprietary digital operating system that orchestrates clinical EHR workflows, 10-Ajnas Mizaj assessment, Hakeem Sahab AI™ clinician decision support, FEFO pharmacy dispensing, and 21 CFR Part 11 cryptographic audit logging across clinics and hospitals."
  },
  {
    id: "faq-who-owns-zayvora",
    category: "General",
    question: "Is ZAYVORA affiliated with or owned by external universities or hospitals?",
    answer: "No. ZAYVORA Health™ is a 100% independent, proprietary healthcare brand and technology ecosystem. We are an autonomous statutory healthcare network and not a subsidiary, affiliate, or digital branch of any external corporate or university hospital. Our clinicians hold accredited qualifications from premier statutory universities, which are cited strictly as verified academic credentials."
  },

  // Clinical Care
  {
    id: "faq-what-is-mizaj",
    category: "Clinical Care",
    question: "What is Mizaj (Constitutional Temperament) and why does it matter?",
    answer: "Mizaj is the foundational concept of Unani medicine representing an individual's unique psycho-physiological and metabolic constitution. Classified into four primary humoral temperaments (Damawi / Sanguine, Safrawi / Choleric, Balghami / Phlegmatic, Sawdawi / Melancholic), understanding your Mizaj allows our Tabeebs to personalize diet, lifestyle, and herbal remedies specifically for your body."
  },
  {
    id: "faq-how-does-matab-work",
    category: "Clinical Care",
    question: "How does a consultation at ZAYVORA Matab™ work?",
    answer: "Your consultation begins with a comprehensive constitutional evaluation incorporating pulse diagnosis (Nabz), physical signs, and symptomatic history alongside modern lab investigations. The attending Tabeeb maps your organ-axis balance, consults Hakeem Sahab AI for literature evidence, and prescribes an individualized Nuskha and regimenal plan."
  },
  {
    id: "faq-can-i-book-teleconsult",
    category: "Clinical Care",
    question: "Can I consult a ZAYVORA Tabeeb online?",
    answer: "Yes. ZAYVORA provides encrypted video teleconsultations through our secure patient portal. Following your online consultation, your signed digital prescription is forwarded to our dispensary for home delivery."
  },

  // AI & Technology
  {
    id: "faq-does-ai-prescribe",
    category: "AI & Technology",
    question: "Does Hakeem Sahab AI™ independently diagnose or prescribe medicine?",
    answer: "Absolutely not. In strict compliance with clinical safety laws, Hakeem Sahab AI™ is strictly a clinician decision-support copilot. Every AI output is programmatically flagged with safe_to_lock=False and cannot finalize or seal a prescription. Final clinical decisions, diagnosis, and prescription signing are made exclusively by licensed human physicians."
  },
  {
    id: "faq-how-is-ai-trained",
    category: "AI & Technology",
    question: "What sources inform Hakeem Sahab AI™?",
    answer: "Hakeem Sahab AI retrieves information from the ZAYVORA Knowledge Base (ZKB), comprising verified classical Unani medical treatises (e.g., Al-Qanun fi al-Tibb, Kitab al-Hawi) cross-linked with modern biomedical literature from PubMed and standardized pharmacopoeial standards via hybrid dense vector and knowledge graph retrieval."
  },

  // Products
  {
    id: "faq-are-products-tested",
    category: "Products",
    question: "How does ZAYVORA verify product quality and safety?",
    answer: "All ZAYVORA Health Products™ are formulated in our AYUSH-GMP compliant cleanroom facility. Every botanical batch undergoes botanical authentication, HPTLC active marker standardization, microbial screening, and heavy metal testing via ICP-MS before release."
  },
  {
    id: "faq-what-is-mudabbar",
    category: "Products",
    question: "What is Mudabbar processing for herbal ingredients?",
    answer: "Mudabbar is a classical pharmaceutical detoxification and purification protocol. Traditional potent herbs (such as Azaraqi or Suranjan) undergo specialized processing with natural vehicles (like cow's milk or aloe) to neutralize toxicity while concentrating therapeutic bioactives. Our dispensary enforces Mudabbar certification before dispensing."
  },

  // Research & Safety
  {
    id: "faq-how-are-emergencies-handled",
    category: "Research & Safety",
    question: "How does ZAYVORA handle acute medical emergencies?",
    answer: "Our clinical system incorporates an algorithmic Red-Flag Triage Engine. If a patient presents with symptoms of acute cardiopulmonary, neurological, or surgical distress, the system immediately halts routine consultation and prompts urgent referral to an acute care emergency department."
  },
  {
    id: "faq-is-my-data-private",
    category: "Research & Safety",
    question: "How is my medical and personal data protected?",
    answer: "We adhere strictly to India's Digital Personal Data Protection (DPDP) Act 2023 and ABDM security and privacy frameworks. Patient health records are encrypted both in transit (TLS 1.3) and at rest (AES-256). Your personal health information is never sold or used for AI training without explicit, verifiable consent."
  }
];
