import { MOCK_PATIENT_PROFILE } from "../cms/patientMockData";
import { UserRoleType } from "../shared/statusEnums";

export interface UserSession {
  token: string;
  user: {
    id: string;
    fullName: string;
    email: string;
    phone: string;
    role: UserRoleType;
    roleDisplayName: string;
    mrn?: string;
    regNumber?: string;
    facilityId: string;
    facilityName: string;
    primaryMizaj?: string;
    permissions: string[];
  };
  expiresAt: number;
}

const SESSION_STORAGE_KEY = "zayvora_unified_session_v5";

export const ROLE_DEFINITIONS: Record<UserRoleType, {
  displayName: string;
  defaultFacility: string;
  defaultPath: string;
  permissions: string[];
}> = {
  SUPER_ADMIN: {
    displayName: "Super Administrator",
    defaultFacility: "Central Governance & University Consortium",
    defaultPath: "/admin",
    permissions: ["all:manage", "audit:merkle", "facilities:manage", "rbac:manage"]
  },
  CLINIC_ADMIN: {
    displayName: "Clinic Administrator",
    defaultFacility: "Jamia Hamdard AUTC - Main Hospital",
    defaultPath: "/admin",
    permissions: ["clinic:manage", "staff:manage", "appointments:slots", "billing:reports"]
  },
  DOCTOR: {
    displayName: "Senior Consulting Tabeeb",
    defaultFacility: "Jamia Hamdard AUTC - Main Hospital, OPD Room 3",
    defaultPath: "/dashboard",
    permissions: ["clinical:consult", "nuskha:prescribe", "21cfr:sign", "hakeem:copilot"]
  },
  HAKEEM: {
    displayName: "Specialist Hakeem (Tadbeer)",
    defaultFacility: "Jamia Hamdard AUTC - Regimenal Therapy Wing",
    defaultPath: "/doctor",
    permissions: ["clinical:consult", "tadbeer:prescribe", "mizaj:assess"]
  },
  RECEPTIONIST: {
    displayName: "Reception Desk Coordinator",
    defaultFacility: "Jamia Hamdard AUTC - Main OPD Reception",
    defaultPath: "/receptionist",
    permissions: ["queue:manage", "patients:register", "appointments:book", "billing:collect"]
  },
  PHARMACIST: {
    displayName: "Registered Chief Pharmacist",
    defaultFacility: "Jamia Hamdard Central Dispensary",
    defaultPath: "/pharmacy",
    permissions: ["dispensary:verify", "fefo:allocate", "mudabbar:gate", "inventory:manage"]
  },
  NURSE_COORDINATOR: {
    displayName: "Clinical Care Coordinator",
    defaultFacility: "Jamia Hamdard AUTC - Triage Desk",
    defaultPath: "/clinic",
    permissions: ["vitals:record", "queue:triage", "followup:outreach"]
  },
  PATIENT: {
    displayName: "Patient (Personal Health Record)",
    defaultFacility: "Jamia Hamdard AUTC - Outpatient Care",
    defaultPath: "/patient",
    permissions: ["phr:view", "appointments:request", "reports:upload", "messages:doctor"]
  },
  SUPPORT_STAFF: {
    displayName: "Technical Support Staff",
    defaultFacility: "National Digital Health Operations",
    defaultPath: "/website/contact",
    permissions: ["support:tickets", "logistics:track"]
  }
};

export class AuthService {
  static getSession(): UserSession | null {
    if (typeof window === "undefined") return null;
    try {
      const stored = localStorage.getItem(SESSION_STORAGE_KEY);
      if (!stored) return null;
      const session = JSON.parse(stored) as UserSession;
      if (Date.now() > session.expiresAt) {
        localStorage.removeItem(SESSION_STORAGE_KEY);
        return null;
      }
      return session;
    } catch {
      return null;
    }
  }

  static login(identifier: string, pass: string, requestedRole: UserRoleType = "PATIENT"): UserSession {
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered email address or mobile number.");
    }
    if (!pass || pass.length < 4) {
      throw new Error("Please enter your password (minimum 4 characters).");
    }

    const roleMeta = ROLE_DEFINITIONS[requestedRole] || ROLE_DEFINITIONS.PATIENT;

    const session: UserSession = {
      token: "sess-zyv-" + Date.now(),
      user: {
        id: requestedRole === "PATIENT" ? "PAT-774901" : "STF-2026-9042",
        fullName: requestedRole === "PATIENT" ? MOCK_PATIENT_PROFILE.fullName : "Prof. (Dr.) Mansoor Alam",
        email: requestedRole === "PATIENT" ? MOCK_PATIENT_PROFILE.email : "mansoor.alam@zayvora.health",
        phone: requestedRole === "PATIENT" ? MOCK_PATIENT_PROFILE.phone : "+91 98110 44219",
        role: requestedRole,
        roleDisplayName: roleMeta.displayName,
        mrn: requestedRole === "PATIENT" ? MOCK_PATIENT_PROFILE.mrn : undefined,
        regNumber: requestedRole === "DOCTOR" || requestedRole === "HAKEEM" ? "CCIM-U-1988-0412" : undefined,
        facilityId: "FAC-HQ-01",
        facilityName: roleMeta.defaultFacility,
        primaryMizaj: requestedRole === "PATIENT" ? MOCK_PATIENT_PROFILE.primaryMizaj : undefined,
        permissions: roleMeta.permissions
      },
      expiresAt: Date.now() + 7200 * 1000
    };

    if (typeof window !== "undefined") {
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
    }
    return session;
  }

  static switchRole(newRole: UserRoleType): UserSession {
    const current = this.getSession();
    const roleMeta = ROLE_DEFINITIONS[newRole] || ROLE_DEFINITIONS.PATIENT;

    const session: UserSession = {
      token: "sess-zyv-" + Date.now(),
      user: {
        id: newRole === "PATIENT" ? "PAT-774901" : "STF-2026-9042",
        fullName: newRole === "PATIENT" ? MOCK_PATIENT_PROFILE.fullName : "Prof. (Dr.) Mansoor Alam",
        email: newRole === "PATIENT" ? MOCK_PATIENT_PROFILE.email : "mansoor.alam@zayvora.health",
        phone: newRole === "PATIENT" ? MOCK_PATIENT_PROFILE.phone : "+91 98110 44219",
        role: newRole,
        roleDisplayName: roleMeta.displayName,
        mrn: newRole === "PATIENT" ? MOCK_PATIENT_PROFILE.mrn : undefined,
        regNumber: newRole === "DOCTOR" || newRole === "HAKEEM" ? "CCIM-U-1988-0412" : undefined,
        facilityId: "FAC-HQ-01",
        facilityName: roleMeta.defaultFacility,
        primaryMizaj: newRole === "PATIENT" ? MOCK_PATIENT_PROFILE.primaryMizaj : undefined,
        permissions: roleMeta.permissions
      },
      expiresAt: Date.now() + 7200 * 1000
    };

    if (typeof window !== "undefined") {
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
    }
    return session;
  }

  static register(data: {
    fullName: string;
    email: string;
    mobile: string;
    age: number;
    gender: string;
    consent: boolean;
  }): UserSession {
    if (!data.fullName || data.fullName.trim().length < 3) {
      throw new Error("Please provide your full legal name.");
    }
    const cleanMobile = data.mobile.replace(/\D/g, "");
    if (cleanMobile.length < 10) {
      throw new Error("Please enter a valid 10-digit mobile number.");
    }
    if (!data.consent) {
      throw new Error("Please accept the HIPAA & ABDM patient consent agreement.");
    }

    const session: UserSession = {
      token: "sess-pat-" + Date.now(),
      user: {
        id: "PAT-" + Math.floor(100000 + Math.random() * 900000),
        fullName: data.fullName,
        email: data.email,
        phone: data.mobile,
        role: "PATIENT",
        roleDisplayName: "Patient (Personal Health Record)",
        mrn: "MRN-2026-" + Math.floor(1000 + Math.random() * 9000),
        facilityId: "FAC-HQ-01",
        facilityName: "Jamia Hamdard AUTC - Outpatient Care",
        primaryMizaj: "Assessment Pending",
        permissions: ROLE_DEFINITIONS.PATIENT.permissions
      },
      expiresAt: Date.now() + 7200 * 1000
    };

    if (typeof window !== "undefined") {
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
    }
    return session;
  }

  static requestPasswordReset(identifier: string): boolean {
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered mobile or email to receive recovery OTP.");
    }
    return true;
  }

  static verifyOtp(identifier: string, otp: string): boolean {
    if (!otp || otp.length < 4) {
      throw new Error("Please enter a valid verification OTP.");
    }
    return true;
  }

  static logout(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem(SESSION_STORAGE_KEY);
    }
  }
}
