import { LegalPageData } from "./types";

export const privacyPolicyData: LegalPageData = {
  title: "Data Protection & Privacy Policy",
  lastUpdated: "20 September 2026",
  version: "v5.0.0 (DPDP Act 2023 & DPDP Rules 2025 Staged Compliance)",
  sections: [
    {
      heading: "1. Scope, Data Fiduciary Identity & Statutory Framework",
      content: [
        "ZAYVORA Health Systems Private Limited ('ZAYVORA Health', 'we', 'our', or 'us') acts as the Data Fiduciary regarding the personal data, demographic identifiers, biometric telemetry, and Protected Health Information (PHI) processed across our digital healthcare platforms, clinical operating system, mobile applications, and clinical Matab complexes.",
        "This policy is formulated in strict accordance with the Digital Personal Data Protection (DPDP) Act, 2023 and the DPDP Rules, 2025 (adhering to the phased, staged commencement provisions notified by the Ministry of Electronics and Information Technology - MeitY), along with the Ayushman Bharat Digital Mission (ABDM) Health Data Management Policy and international healthcare cybersecurity standards."
      ]
    },
    {
      heading: "2. Categories of Data Processed",
      content: [
        "Personal & Demographic Data: Full legal name, date of birth, biological sex, contact telephone number, residential address, emergency contacts, and Ayushman Bharat Health Account (ABHA ID / ABHA Address) when linked by the patient.",
        "Clinical & Diagnostic Data: Presenting complaints, medical and surgical history, quantitative Mizaj (temperament) assessments, 12-Organ-Axis pathophysiological profiles, 10-Ajnas pulse (Nabz) biometric waveforms, lingual chromametric images, vital signs, laboratory test reports, and clinician consultation notes.",
        "Prescription & Therapeutic Regimens: Personalized botanical formulations (Nuskha), Schedule E(1) Mudabbar verification records, dietary regimens (Ilaj-bil-Ghiza), regimenal therapy records (Ilaj-bil-Tadbeer), and patient-reported outcome measures (PROMs).",
        "Clinical AI Assistive Logs: Encrypted decision-support interaction logs generated during Hakeem Sahab AI™ assisted consultations, recording clinician validation and digital signature sign-offs.",
        "Telemetry & Audit Metadata: Cryptographic session tokens, IP addresses, browser user-agents, and immutable, tamper-evident audit records generated under 21 CFR Part 11 requirements."
      ]
    },
    {
      heading: "3. Lawful Basis and Purpose of Processing",
      content: [
        "Primary Healthcare Delivery: Conducting outpatient and inpatient clinical consultations, individualized temperament assessments, teleconsultations, and authorizing medical prescriptions.",
        "Closed-Loop Botanical Dispensing: Fulfilling electronic pharmacy orders, ensuring First-Expired-First-Out (FEFO) batch accuracy, and tracking delivery logistics.",
        "Patient Safety & Pharmacovigilance: Continuous active surveillance for adverse botanical reactions, drug-herb interactions (CYP450 metabolism), and Schedule E(1) detoxification compliance.",
        "Statutory & Regulatory Compliance: Maintaining clinical audit ledgers, fulfilling NCISM clinical documentation mandates, and cooperating with public health disease surveillance.",
        "Academic & Observational Research: Processing anonymized, de-identified datasets for Real-World Evidence (RWE) observational cohort studies where explicit, informed research consent has been obtained."
      ]
    },
    {
      heading: "4. Consent Management & Withdrawal Rights",
      content: [
        "Consent is collected on a granular, freely given, specific, and informed basis before clinical onboarding, teleconsultation initiation, or linkage of ABHA records.",
        "Patients maintain the unconditional right to withdraw consent for secondary purposes (such as academic research participation or promotional health literacy advisories) at any time via the patient portal settings or by written notice.",
        "Withdrawal of consent for primary clinical records is subject to mandatory statutory medical record retention timelines prescribed by the National Commission for Indian System of Medicine (NCISM) and state medical council regulations."
      ]
    },
    {
      heading: "5. Data Sharing, Interoperability & Cross-Border Transfers",
      content: [
        "ABDM Health Information Exchange: When authorized via the ABDM Consent Manager, health records are shared with certified Health Information Users (HIU) using end-to-end encrypted FHIR R4 clinical bundles.",
        "Authorized Service Processors: Data is accessible only to vetted enterprise cloud infrastructure providers, SMS/WhatsApp posology notification gateways (QSURA), and licensed payment gateways under strict Data Processing Agreements (DPAs).",
        "Zero Commercial Data Monetization: ZAYVORA Health does not sell, lease, monetize, or trade patient health data, clinical profiles, or contact information with third-party advertisers or insurance brokers.",
        "Data Localization: All primary clinical databases, electronic health records, and diagnostic telemetry are securely hosted within enterprise sovereign cloud facilities located physically inside the Union of India."
      ]
    },
    {
      heading: "6. Cryptographic Security, Access Controls & Data Retention",
      content: [
        "Encryption in Transit: All client-server communications enforce Transport Layer Security (TLS 1.3) with perfect forward secrecy.",
        "Encryption at Rest: All electronic patient databases and digital prescription repositories are encrypted using AES-256 with tenant-segregated cryptographic keys.",
        "Role-Based Access Control (RBAC): Healthcare staff have access restricted strictly on a need-to-know basis (e.g. pharmacists see dispensing and allergy data; administrative staff see only demographic and billing records).",
        "Tamper-Evident Audit Trails: All clinical modifications, encounter sign-offs, and prescription approvals are cryptographically sealed with SHA-256 hashes.",
        "Retention Period: In-patient and out-patient clinical records are preserved in secure archives for a minimum duration of 3 years from the date of the last consultation, as mandated by clinical establishment standards."
      ]
    },
    {
      heading: "7. Patient Rights Under the DPDP Act, 2023",
      content: [
        "Right to Access: Patients can view, review, and export their complete medical record, clinical timeline, and active prescription records via the 'My ZAYVORA™' patient portal.",
        "Right to Correction & Erasure: Patients can request correction of inaccurate demographic data or completion of incomplete health profiles.",
        "Right of Grievance Redressal: Patients have access to an accessible, transparent internal grievance redressal mechanism with mandatory turnaround timelines.",
        "Right to Nominate: Patients may designate a legal representative or nominee to manage their healthcare access and consent in the event of incapacity."
      ]
    },
    {
      heading: "8. Data Protection Officer (DPO) & Grievance Contact",
      content: [
        "For grievances, statutory rights requests, or inquiries regarding personal data protection, contact our designated Data Protection Officer:",
        "Data Protection Officer: Office of Privacy & Regulatory Governance",
        "ZAYVORA Health Systems Private Limited, Institutional Area, New Delhi - 110062, India",
        "Email: privacy@zayvora.com • Regulatory Helpline: +91 97738 82657",
        "Expected Grievance Resolution: Within 7 business days from formal logged receipt."
      ]
    }
  ]
};

export const termsConditionsData: LegalPageData = {
  title: "Terms and Conditions of Clinical Service",
  lastUpdated: "20 September 2026",
  version: "v5.0.0 (Clinical Establishment & Telemedicine Aligned)",
  sections: [
    {
      heading: "1. Acceptance of Terms",
      content: [
        "By accessing or using the ZAYVORA Health OS™ platform, patient portal, clinical scheduling desk, or visiting ZAYVORA Matab™ hospital complexes, you enter into a legally binding agreement governed by these Terms and Conditions.",
        "If you do not agree with any provision of these terms, you must immediately discontinue use of the platform and digital services."
      ]
    },
    {
      heading: "2. Clinical Care Delivery & Professional Accountability",
      content: [
        "ZAYVORA Health OS™ provides digital clinical workspace infrastructure connecting patients with board-certified practitioners registered under the National Commission for Indian System of Medicine (NCISM) Act, 2020.",
        "All diagnostic assessments, constitutional Mizaj evaluations, personalized Nuskha formulation authoring, and regimenal orders (Ilaj-bit-Tadbeer) are rendered solely by licensed practitioners exercising independent professional clinical judgment.",
        "Informational content, interactive self-assessments, and Hakeem Sahab AI™ clinical reasoning tools are assistive decision-support resources and do not constitute autonomous medical care."
      ]
    },
    {
      heading: "3. Teleconsultation Standards & Inherent Limitations",
      content: [
        "Teleconsultations conform to statutory telemedicine practice guidelines. Patients acknowledge that remote video/audio consultations lack direct tactile palpatory examination and in-person 10-Ajnas pulse diagnosis.",
        "Attending clinicians maintain full medical discretion to require an in-person physical follow-up, laboratory panel, or referral to emergency services whenever clinically warranted."
      ]
    },
    {
      heading: "4. Prescription Dispensing & Schedule E(1) Compliance",
      content: [
        "Herbal compound prescriptions are dispensed strictly against a valid, digitally signed prescription issued by an attending ZAYVORA clinician.",
        "Prescriptions incorporating Schedule E(1) substances undergo mandatory Mudabbar electronic safety checks and cannot be dispensed if batch analytical safety assays fail."
      ]
    },
    {
      heading: "5. Intellectual Property Rights & Ownership",
      content: [
        "The ZAYVORA Health OS™ software architecture, proprietary 12-Organ-Axis diagnostic cross-talk engines, 4-Stage Afaal treatment cascade models, 10-Ajnas pulse waveform digital signal processing, and clinical interface designs are the exclusive intellectual property of Hakeem Dr. Irfan Ashraf, Founder, Chairman & Chief Architect.",
        "Unauthorized reproduction, reverse engineering, unauthorized API scraping, or commercial exploitation of proprietary diagnostic matrices is strictly prohibited and subject to legal remedies."
      ]
    },
    {
      heading: "6. Limitation of Liability & Emergency Care Disclaimer",
      content: [
        "ZAYVORA Health and its clinical faculty are not liable for adverse outcomes resulting from patient non-disclosure of medical history, unapproved allopathic drug-herb co-administration, failure to adhere to prescribed dietary restrictions (Parhez), or delays in seeking emergency hospital care for acute conditions.",
        "In all medical emergencies, users must immediately contact emergency services (112) or proceed to the nearest trauma hospital."
      ]
    }
  ]
};
