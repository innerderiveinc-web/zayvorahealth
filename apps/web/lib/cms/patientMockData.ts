export interface PatientProfileData {
  mrn: string;
  abhaId: string;
  fullName: string;
  age: number;
  gender: string;
  primaryMizaj: string;
  suEMizaj: string;
  bloodGroup: string;
  phone: string;
  email: string;
  address: string;
  emergencyContact: string;
  allergies: string[];
}

export interface PatientAppointment {
  id: string;
  doctorName: string;
  doctorSpecialty: string;
  date: string;
  timeSlot: string;
  mode: "In-Clinic OPD" | "Video Consultation";
  facilityLocation: string;
  tokenNumber: string;
  status: "Confirmed" | "Waiting" | "Completed" | "Rescheduled";
  joinVideoUrl?: string;
}

export interface ActiveCarePlanData {
  programName: string;
  condition: string;
  currentPhase: string;
  phaseNumber: number;
  totalPhases: number;
  progressPercent: number;
  startDate: string;
  nextReviewDate: string;
  attendingPhysician: string;
  clinicalNotes: string;
  dietaryDirectives: string[];
  lifestyleDirectives: string[];
}

export interface PatientPrescriptionDose {
  medicineName: string;
  form: string;
  dosage: string;
  timing: string;
  instructions: string;
  anupan: string;
  adherenceChecked: boolean;
}

export interface PatientLabReport {
  id: string;
  title: string;
  testDate: string;
  labName: string;
  status: "Verified" | "Pending Review";
  fileSize: string;
  downloadUrl: string;
}

export interface PatientMessage {
  id: string;
  senderName: string;
  senderRole: string;
  timestamp: string;
  messageText: string;
  isDoctor: boolean;
}

export interface PatientInvoice {
  invoiceId: string;
  serviceDescription: string;
  date: string;
  amount: number;
  paymentMode: string;
  status: "Paid" | "Pending";
  receiptNumber: string;
}

export const MOCK_PATIENT_PROFILE: PatientProfileData = {
  mrn: "MRN-2026-0814",
  abhaId: "91-1234-5678-9012",
  fullName: "Hamza Farooqi",
  age: 44,
  gender: "Male",
  primaryMizaj: "Balghami (Cold & Moist)",
  suEMizaj: "Su-e-Mizaj Barid Balghami (Grade 2 Phlegmatic Dyscrasia)",
  bloodGroup: "B+",
  phone: "+91 98110 44219",
  email: "hamza.farooqi@gmail.com",
  address: "Flat 402, Al-Aman Apartments, Okhla, New Delhi - 110025",
  emergencyContact: "Zainab Farooqi (Wife) • +91 98110 44220",
  allergies: ["Sonf (Fennel) hypersensitivity (mild rash)"]
};

export const MOCK_PATIENT_APPOINTMENT: PatientAppointment = {
  id: "APT-2026-0915-01",
  doctorName: "Hakeem Dr. Irfan Ashraf",
  doctorSpecialty: "Senior Consultant Tabeeb • Musculoskeletal & Nabz",
  date: "2026-09-15",
  timeSlot: "10:30 AM IST",
  mode: "In-Clinic OPD",
  facilityLocation: "ZAYVORA Matab™ Central Care Centre, OPD Room 3",
  tokenNumber: "T-104",
  status: "Confirmed",
  joinVideoUrl: "/patient/teleconsult?session=ENC-2026-0814"
};

export const MOCK_CARE_PLAN: ActiveCarePlanData = {
  programName: "Mafasil Knee Joint Reversal Protocol",
  condition: "Waja-ul-Mafasil Barid Balghami (Bilateral Knee Osteoarthritis)",
  currentPhase: "Stage 1: Humoral Cleansing & Concoction (Tanqiya)",
  phaseNumber: 1,
  totalPhases: 4,
  progressPercent: 65,
  startDate: "2026-09-02",
  nextReviewDate: "2026-09-16",
  attendingPhysician: "Hakeem Dr. Irfan Ashraf (NCISM-BUMS)",
  clinicalNotes: "Patient demonstrates marked reduction in synovial crepitus. Morning stiffness reduced from 45 min to 18 min. Progressing towards Phase 2 (Tahleel) following lab review.",
  dietaryDirectives: [
    "Drink warm ginger-infused water with meals; strictly avoid chilled yogurt and cold sodas.",
    "Incorporate boiled barley water (Maa-ul-Sha'eer) daily.",
    "Dinner must be completed by 8:00 PM."
  ],
  lifestyleDirectives: [
    "Gentle local fomentation (Natool) with warm water followed by Roghan-e-Balsan.",
    "Avoid prolonged cross-legged floor sitting (Chowki usage recommended).",
    "15 minutes gentle quadriceps isometrics daily."
  ]
};

export const MOCK_MEDICINES: PatientPrescriptionDose[] = [
  {
    medicineName: "Majun Suranjan (Mudabbar Formulation)",
    form: "Confection / Paste",
    dosage: "5 grams (approx. 1 level teaspoon)",
    timing: "Twice daily — Morning post-breakfast and Night post-dinner",
    instructions: "Take with lukewarm water or warm milk. Do not skip scheduled doses.",
    anupan: "Warm water with a pinch of black pepper or lukewarm milk",
    adherenceChecked: true
  },
  {
    medicineName: "Roghan-e-Balsan (Clinical Joint Oil)",
    form: "External Medicated Oil",
    dosage: "5 to 10 drops",
    timing: "Nighttime before sleep",
    instructions: "Gentle massage over both knees without vigorous pressure (Dalak Layyin). Cover with warm flannel.",
    anupan: "External use only",
    adherenceChecked: true
  }
];

export const MOCK_REPORTS: PatientLabReport[] = [
  {
    id: "REP-101",
    title: "Serum hs-CRP & Rheumatoid Factor Panel",
    testDate: "2026-09-03",
    labName: "ZAYVORA Clinical Diagnostics Laboratory",
    status: "Verified",
    fileSize: "1.2 MB PDF",
    downloadUrl: "#"
  },
  {
    id: "REP-102",
    title: "Digital Bilateral Knee X-Ray (AP & Lateral Weight Bearing)",
    testDate: "2026-08-28",
    labName: "ZAYVORA Medical Imaging Wing",
    status: "Verified",
    fileSize: "4.8 MB PDF",
    downloadUrl: "#"
  },
  {
    id: "REP-103",
    title: "Complete Blood Count (CBC) & Serum Uric Acid",
    testDate: "2026-08-28",
    labName: "ZAYVORA Clinical Diagnostics Laboratory",
    status: "Verified",
    fileSize: "850 KB PDF",
    downloadUrl: "#"
  }
];

export const MOCK_MESSAGES: PatientMessage[] = [
  {
    id: "msg-1",
    senderName: "Hakeem Dr. Irfan Ashraf",
    senderRole: "Senior Consultant Tabeeb",
    timestamp: "Yesterday, 04:30 PM",
    messageText: "Dear Hamza, your hs-CRP levels show a favorable decline towards 4.8 mg/L. Please continue with the morning Majun Suranjan and do not miss the evening warm fomentation before your follow-up visit on the 15th.",
    isDoctor: true
  },
  {
    id: "msg-2",
    senderName: "Hamza Farooqi",
    senderRole: "Patient",
    timestamp: "Yesterday, 05:15 PM",
    messageText: "Thank you Dr. Mansoor. The morning stiffness is noticeably easier when waking up. I will see you at OPD Room 3 on Wednesday.",
    isDoctor: false
  }
];

export const MOCK_INVOICES: PatientInvoice[] = [
  {
    invoiceId: "INV-2026-0814",
    serviceDescription: "Integrative Consultation & 10-Ajnas Evaluation + Majun Suranjan Dispensary Batch",
    date: "2026-09-02",
    amount: 1250,
    paymentMode: "UPI (Razorpay Verified)",
    status: "Paid",
    receiptNumber: "REC-ZAY-99014"
  }
];

// Compatibility aliases
export const MOCK_ACTIVE_CARE_PLAN = MOCK_CARE_PLAN;
export const MOCK_PRESCRIPTIONS = MOCK_MEDICINES;
export const MOCK_LAB_REPORTS = MOCK_REPORTS;
export const MOCK_PATIENT_MESSAGES = MOCK_MESSAGES;
export const MOCK_PATIENT_INVOICES = MOCK_INVOICES;

