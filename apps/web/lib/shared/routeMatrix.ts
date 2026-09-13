/**
 * ZAYVORA OS — Centralized Route & Role Matrix
 * Single source of truth mapping web routes, mobile screens, roles, and permissions.
 */

import { UserRoleType } from "./statusEnums";

export interface RouteDefinition {
  id: string;
  name: string;
  webUrl: string;
  mobileScreen: string;
  parentModule: "MARKETING" | "CLINICAL" | "PATIENT_PORTAL" | "OPERATIONS" | "PHARMACY" | "ADMIN" | "INTELLIGENCE";
  allowedRoles: UserRoleType[];
  isPublic: boolean;
  navLocation: "SIDEBAR" | "HEADER" | "BOTTOM_NAV" | "SUBPAGE" | "FOOTER";
  mobileBottomTab?: string;
  description: string;
}

export const ZAYVORA_ROUTE_MATRIX: RouteDefinition[] = [
  // PUBLIC MARKETING
  {
    id: "website_home",
    name: "Public Home",
    webUrl: "/website",
    mobileScreen: "PublicHomeScreen",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "Flagship 12-section modern Unani healthcare organization homepage."
  },
  {
    id: "website_programs",
    name: "Health Programs",
    webUrl: "/website/programs",
    mobileScreen: "ProgramsScreen",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "Directory of 6 clinical specialty programs with Afaal treatment cascades."
  },
  {
    id: "website_herbals",
    name: "Herbal Formulations",
    webUrl: "/website/herbals",
    mobileScreen: "HerbalsCatalogScreen",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "Regulatory-categorized botanical formulations catalog."
  },
  {
    id: "website_doctors",
    name: "Clinical Faculty",
    webUrl: "/website/doctors",
    mobileScreen: "DoctorsScreen",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "Verified senior Tabeebs and integrative medical faculty."
  },
  {
    id: "website_knowledge",
    name: "Knowledge Centre",
    webUrl: "/website/knowledge-centre",
    mobileScreen: "KnowledgeScreen",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "9-category clinical and lifestyle publication library."
  },
  {
    id: "website_book",
    name: "Book Consultation",
    webUrl: "/website/book",
    mobileScreen: "BookAppointmentModal",
    parentModule: "MARKETING",
    allowedRoles: ["PATIENT", "DOCTOR", "SUPER_ADMIN", "CLINIC_ADMIN", "RECEPTIONIST", "PHARMACIST", "HAKEEM", "NURSE_COORDINATOR", "SUPPORT_STAFF"],
    isPublic: true,
    navLocation: "HEADER",
    description: "Multi-step interactive consultation booking wizard."
  },

  // DOCTOR / CLINICIAN
  {
    id: "doctor_dashboard",
    name: "Doctor Dashboard",
    webUrl: "/dashboard",
    mobileScreen: "DoctorHomeScreen",
    parentModule: "CLINICAL",
    allowedRoles: ["DOCTOR", "HAKEEM", "SUPER_ADMIN", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    mobileBottomTab: "home",
    description: "Consultation overview, KPI metrics, waiting queue, and clinical safety alerts."
  },
  {
    id: "clinical_workspace",
    name: "Clinical Workspace",
    webUrl: "/doctor",
    mobileScreen: "ClinicalEncounterScreen",
    parentModule: "CLINICAL",
    allowedRoles: ["DOCTOR", "HAKEEM", "SUPER_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    description: "12-step consultation encounter, SOAP notes, Mizaj calculation, and 21 CFR lock."
  },
  {
    id: "hakeem_ai_copilot",
    name: "AI Doctor — Hakeem Sahab",
    webUrl: "/ai",
    mobileScreen: "AiDoctorScreen",
    parentModule: "INTELLIGENCE",
    allowedRoles: ["DOCTOR", "HAKEEM", "SUPER_ADMIN", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    mobileBottomTab: "ai",
    description: "Clinician decision-support copilot with UPI monograph citations and safety gates."
  },

  // PATIENT PORTAL
  {
    id: "patient_portal",
    name: "Patient Dashboard",
    webUrl: "/patient",
    mobileScreen: "PatientHomeScreen",
    parentModule: "PATIENT_PORTAL",
    allowedRoles: ["PATIENT", "SUPER_ADMIN", "DOCTOR", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    mobileBottomTab: "home",
    description: "Personal health record, care plan, appointments, and audio posology."
  },

  // RECEPTION / CLINIC OPERATIONS
  {
    id: "reception_desk",
    name: "Receptionist Desk",
    webUrl: "/receptionist",
    mobileScreen: "ReceptionHomeScreen",
    parentModule: "OPERATIONS",
    allowedRoles: ["RECEPTIONIST", "SUPER_ADMIN", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    mobileBottomTab: "queue",
    description: "OPD queue token management, check-in, check-out, doctor roster, and billing."
  },
  {
    id: "clinic_opd",
    name: "Clinic OPD Queue",
    webUrl: "/clinic",
    mobileScreen: "ClinicQueueScreen",
    parentModule: "OPERATIONS",
    allowedRoles: ["RECEPTIONIST", "SUPER_ADMIN", "CLINIC_ADMIN", "DOCTOR"],
    isPublic: false,
    navLocation: "SIDEBAR",
    description: "Hospital OPD patient queue, room allocation, and doctor availability."
  },

  // PHARMACY / DISPENSARY
  {
    id: "pharmacy_dispensary",
    name: "Pharmacy & Dispensary",
    webUrl: "/pharmacy",
    mobileScreen: "PharmacyHomeScreen",
    parentModule: "PHARMACY",
    allowedRoles: ["PHARMACIST", "SUPER_ADMIN", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    description: "Prescription verification queue, 4-tier regulatory inventory, and FEFO allocation."
  },

  // ADMIN CONSOLE
  {
    id: "admin_console",
    name: "Enterprise Admin",
    webUrl: "/admin",
    mobileScreen: "AdminMonitoringScreen",
    parentModule: "ADMIN",
    allowedRoles: ["SUPER_ADMIN", "CLINIC_ADMIN"],
    isPublic: false,
    navLocation: "SIDEBAR",
    description: "17-section hospital administration, staff roles, facilities, and Merkle audit logs."
  }
];
