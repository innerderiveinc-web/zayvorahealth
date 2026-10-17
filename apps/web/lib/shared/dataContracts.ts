/**
 * ZAYVORA OS — Normalized Clinical & Operational Data Contracts
 * Shared across Web App, Mobile App, and Services.
 */

import {
  AppointmentStatus,
  PrescriptionStatus,
  CarePlanPhase,
  PaymentStatus,
  DiagnosticReportStatus,
  RegulatoryCategory
} from "./statusEnums";

export interface NormalizedPatient {
  id: string;
  mrn: string;
  abhaId: string;
  fullName: string;
  age: number;
  gender: "Male" | "Female" | "Other";
  phone: string;
  email: string;
  address: string;
  emergencyContact: string;
  bloodGroup: string;
  primaryMizaj: string;
  suEMizaj: string;
  allergies: string[];
  activeProgram?: string;
  nextAppointmentDate?: string;
}

export interface NormalizedAppointment {
  id: string;
  tokenNumber: string;
  patientId: string;
  patientName: string;
  patientMrn: string;
  patientAge: number;
  patientGender: string;
  doctorId: string;
  doctorName: string;
  doctorSpecialty: string;
  date: string;
  timeSlot: string;
  mode: "In-Clinic OPD" | "Online Video Teleconsultation";
  facilityLocation: string;
  opdRoom: string;
  status: AppointmentStatus;
  chiefComplaint: string;
  feeAmount: number;
  paymentStatus: PaymentStatus;
}

export interface NormalizedPrescriptionItem {
  medicineName: string;
  regulatoryCategory: RegulatoryCategory;
  form: "Majun" | "Safoof" | "Roghan" | "Sharbat" | "Khamira" | "Hab" | "Jawarish" | "Extract";
  dosage: string;
  timing: string;
  anupan: string;
  durationDays: number;
  isScheduleE1: boolean;
  mudabbarLot?: string;
  mudabbarVerified: boolean;
  dispensedBatchNumber?: string;
  expiryDate?: string;
}

export interface NormalizedPrescription {
  id: string;
  prescriptionNumber: string;
  patientId: string;
  patientName: string;
  patientMrn: string;
  doctorId: string;
  doctorName: string;
  doctorRegNumber: string;
  date: string;
  status: PrescriptionStatus;
  items: NormalizedPrescriptionItem[];
  clinicalDirectives: string;
  dietaryProhibitions: string[];
  digitalSignatureHash?: string;
  isLocked: boolean;
}

export interface NormalizedCarePlan {
  id: string;
  patientId: string;
  programName: string;
  condition: string;
  currentPhase: CarePlanPhase;
  phaseNumber: number;
  totalPhases: number;
  progressPercent: number;
  startDate: string;
  nextReviewDate: string;
  attendingDoctor: string;
  clinicalNotes: string;
  dietaryDirectives: string[];
  lifestyleDirectives: string[];
  milestones: {
    name: string;
    targetWeek: number;
    achieved: boolean;
  }[];
}

export interface NormalizedInventoryItem {
  id: string;
  brandName: string;
  botanicalIngredients: string;
  category: RegulatoryCategory;
  batchNumber: string;
  expiryDate: string;
  stockQuantity: number;
  minimumThreshold: number;
  unitPrice: number;
  mudabbarCertified: boolean;
  storageCondition: "Cold-Chain (15-25°C)" | "Ambient Dry" | "Refrigerated (2-8°C)";
}
