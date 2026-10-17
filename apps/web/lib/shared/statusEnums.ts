/**
 * ZAYVORA OS — Universal Status Enums
 * Shared across Web, Mobile, and Backend API contracts.
 */

export type AppointmentStatus =
  | "REQUESTED"
  | "PENDING"
  | "CONFIRMED"
  | "CHECKED_IN"
  | "WAITING"
  | "IN_CONSULTATION"
  | "COMPLETED"
  | "CANCELLED"
  | "NO_SHOW"
  | "RESCHEDULED";

export type PrescriptionStatus =
  | "DRAFT"
  | "PENDING_REVIEW"
  | "DOCTOR_SIGNED"
  | "DISPENSED"
  | "COMPLETED"
  | "CANCELLED";

export type CarePlanPhase =
  | "TASKEEN_E_ALAM"      // Stage 1: Pain & Symptom Mitigation
  | "TANQIYA_E_MAWAD"     // Stage 2: Morbid Matter Evacuation
  | "TADIL_E_MIZAJ"       // Stage 3: Temperamental Normalization
  | "TAQWIYAT_E_MAFASIL"; // Stage 4: Organ & Tissue Fortification

export type PaymentStatus =
  | "DRAFT"
  | "PENDING"
  | "PAID"
  | "FAILED"
  | "REFUNDED"
  | "CANCELLED";

export type DiagnosticReportStatus =
  | "PENDING_UPLOAD"
  | "PENDING_REVIEW"
  | "REVIEWED_NORMAL"
  | "REVIEWED_ABNORMAL"
  | "CRITICAL_ACTION_REQUIRED";

export type RegulatoryCategory =
  | "CLINIC_PRESCRIBED_UNANI" // Schedule E(1) & prescription-gated formulations
  | "CLASSICAL_RETAIL_UNANI"  // OTC Classical NFUM/UPI syrups & oils
  | "AYUSH_PROPRIETARY"       // Licensed AYUSH proprietary formulations
  | "FSSAI_DIETARY_SUPPLEMENT"; // Dietary botanical supplements & functional foods

export type UserRoleType =
  | "SUPER_ADMIN"
  | "CLINIC_ADMIN"
  | "DOCTOR"
  | "HAKEEM"
  | "RECEPTIONIST"
  | "PHARMACIST"
  | "NURSE_COORDINATOR"
  | "PATIENT"
  | "SUPPORT_STAFF";
