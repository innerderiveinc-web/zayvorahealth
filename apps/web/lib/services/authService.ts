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
    defaultFacility: "ZAYVORA Matab™ — Central Care Centre",
    defaultPath: "/admin",
    permissions: ["clinic:manage", "staff:manage", "appointments:slots", "billing:reports"]
  },
  DOCTOR: {
    displayName: "Senior Consulting Tabeeb",
    defaultFacility: "ZAYVORA Matab™ — Central Care Centre, OPD Room 3",
    defaultPath: "/doctor",
    permissions: ["clinical:consult", "nuskha:prescribe", "21cfr:sign", "hakeem:copilot"]
  },
  HAKEEM: {
    displayName: "Specialist Hakeem (Tadbeer)",
    defaultFacility: "ZAYVORA Matab™ — Regimenal Therapy Wing",
    defaultPath: "/doctor",
    permissions: ["clinical:consult", "tadbeer:prescribe", "mizaj:assess"]
  },
  RECEPTIONIST: {
    displayName: "Reception Desk Coordinator",
    defaultFacility: "ZAYVORA Matab™ — Main OPD Reception",
    defaultPath: "/receptionist",
    permissions: ["queue:manage", "patients:register", "appointments:book", "billing:collect"]
  },
  PHARMACIST: {
    displayName: "Registered Chief Pharmacist",
    defaultFacility: "ZAYVORA Central Pharmacy & Dispensary",
    defaultPath: "/pharmacy",
    permissions: ["dispensary:verify", "fefo:allocate", "mudabbar:gate", "inventory:manage"]
  },
  NURSE_COORDINATOR: {
    displayName: "Clinical Care Coordinator",
    defaultFacility: "ZAYVORA Care Centre — Triage Desk",
    defaultPath: "/clinic",
    permissions: ["vitals:record", "queue:triage", "followup:outreach"]
  },
  PATIENT: {
    displayName: "Patient (Personal Health Record)",
    defaultFacility: "ZAYVORA Matab™ — Outpatient Care",
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

export const isDemoModeAllowed = (): boolean => {
  if (typeof process !== "undefined" && process.env) {
    if (process.env.NODE_ENV === "production") {
      return false;
    }
    return process.env.NEXT_PUBLIC_DEMO_MODE === "true";
  }
  return false;
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
    if (!isDemoModeAllowed()) {
      throw new Error("Direct offline authentication is disabled in production mode. Please authenticate through the API Gateway.");
    }
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
        id: requestedRole === "PATIENT" ? "PAT-" + Math.floor(100000 + Math.random() * 900000) : "STF-2026-9042",
        fullName: requestedRole === "PATIENT" ? (identifier.includes("@") ? identifier.split("@")[0].replace(".", " ") : identifier || "Registered Patient") : "Hakeem Dr. Irfan Ashraf",
        email: requestedRole === "PATIENT" ? (identifier.includes("@") ? identifier : `${identifier}@zayvora.patient`) : "dr.irfan@zayvorahealth.com",
        phone: requestedRole === "PATIENT" ? "+91 98765 43210" : "+91 98110 44219",
        role: requestedRole,
        roleDisplayName: roleMeta.displayName,
        mrn: requestedRole === "PATIENT" ? "MRN-2026-" + Math.floor(1000 + Math.random() * 9000) : undefined,
        regNumber: requestedRole === "DOCTOR" || requestedRole === "HAKEEM" ? "Updating / Verification in Progress" : undefined,
        facilityId: "FAC-HQ-01",
        facilityName: roleMeta.defaultFacility,
        primaryMizaj: requestedRole === "PATIENT" ? "Assessment Pending" : undefined,
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
    if (!isDemoModeAllowed()) {
      throw new Error("Client-side role switching is prohibited in production mode. Please sign in with authorized credentials for the requested role.");
    }
    const current = this.getSession();
    const roleMeta = ROLE_DEFINITIONS[newRole] || ROLE_DEFINITIONS.PATIENT;

    const session: UserSession = {
      token: "sess-zyv-" + Date.now(),
      user: {
        id: newRole === "PATIENT" ? "PAT-" + Math.floor(100000 + Math.random() * 900000) : "STF-2026-9042",
        fullName: newRole === "PATIENT" ? "Registered Patient" : "Hakeem Dr. Irfan Ashraf",
        email: newRole === "PATIENT" ? "patient@zayvorahealth.com" : "dr.irfan@zayvorahealth.com",
        phone: newRole === "PATIENT" ? "+91 98765 43210" : "+91 98110 44219",
        role: newRole,
        roleDisplayName: roleMeta.displayName,
        mrn: newRole === "PATIENT" ? "MRN-2026-" + Math.floor(1000 + Math.random() * 9000) : undefined,
        regNumber: newRole === "DOCTOR" || newRole === "HAKEEM" ? "Updating / Verification in Progress" : undefined,
        facilityId: "FAC-HQ-01",
        facilityName: roleMeta.defaultFacility,
        primaryMizaj: newRole === "PATIENT" ? "Assessment Pending" : undefined,
        permissions: roleMeta.permissions
      },
      expiresAt: Date.now() + 3600 * 1000
    };

    if (typeof window !== "undefined") {
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
    }
    return session;
  }

  static async loginAsync(identifier: string, pass: string, requestedRole: UserRoleType = "PATIENT"): Promise<UserSession> {
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
    let fetchError: any = null;

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier, password: pass })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.ok && data.user) {
          const roleMeta = ROLE_DEFINITIONS[data.user.role as UserRoleType] || ROLE_DEFINITIONS.PATIENT;
          const session: UserSession = {
            token: data.token || ("sess-live-" + Date.now()),
            user: {
              id: data.user.id,
              fullName: data.user.fullName,
              email: data.user.email,
              phone: data.user.phone || "",
              role: data.user.role as UserRoleType,
              roleDisplayName: roleMeta.displayName,
              mrn: data.user.mrn,
              facilityId: data.user.facilityId || "FAC-HQ-01",
              facilityName: data.user.facilityName || roleMeta.defaultFacility,
              permissions: roleMeta.permissions
            },
            expiresAt: Date.now() + 3600 * 1000
          };
          if (typeof window !== "undefined") {
            localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
          }
          return session;
        }
      } else {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.error || errJson.detail || `Authentication failed (${res.status})`);
      }
    } catch (e: any) {
      fetchError = e;
      // If error is an explicit auth failure (401/400), don't mask it
      if (e.message && !e.message.includes("Failed to fetch") && !e.message.includes("NetworkError")) {
        throw e;
      }
    }

    // Only allow local offline fallback if demo mode is explicitly permitted
    if (isDemoModeAllowed()) {
      return this.login(identifier, pass, requestedRole);
    }

    throw fetchError || new Error("Authentication gateway is unreachable. Secure production mode requires an active connection to the identity service.");
  }

  static register(data: {
    fullName: string;
    email: string;
    mobile: string;
    age: number;
    gender: string;
    consent: boolean;
  }): UserSession {
    if (!isDemoModeAllowed()) {
      throw new Error("Direct offline registration is disabled in production mode. Please register through the API Gateway.");
    }
    if (!data.fullName || data.fullName.trim().length < 3) {
      throw new Error("Please provide your full legal name.");
    }
    const cleanMobile = data.mobile.replace(/\D/g, "");
    if (cleanMobile.length < 10) {
      throw new Error("Please enter a valid 10-digit mobile number.");
    }
    if (!data.consent) {
      throw new Error("Please accept the DPDP Act 2023 & ABDM patient consent agreement.");
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
        facilityName: "ZAYVORA Matab™ — Outpatient Care",
        primaryMizaj: "Assessment Pending",
        permissions: ROLE_DEFINITIONS.PATIENT.permissions
      },
      expiresAt: Date.now() + 3600 * 1000
    };

    if (typeof window !== "undefined") {
      localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
    }
    return session;
  }

  static async registerAsync(data: {
    fullName: string;
    email: string;
    mobile: string;
    age: number;
    gender: string;
    consent: boolean;
    password?: string;
  }): Promise<UserSession> {
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
    if (!data.password) {
      throw new Error("Password is required for patient registration.");
    }
    let fetchError: any = null;

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
          fullName: data.fullName,
          phone: data.mobile,
          role: "PATIENT"
        })
      });

      if (res.ok) {
        const resp = await res.json();
        if (resp.ok && resp.user) {
          const roleMeta = ROLE_DEFINITIONS.PATIENT;
          const session: UserSession = {
            token: resp.token || ("sess-live-" + Date.now()),
            user: {
              id: resp.user.id,
              fullName: resp.user.fullName,
              email: resp.user.email,
              phone: resp.user.phone || data.mobile,
              role: "PATIENT",
              roleDisplayName: roleMeta.displayName,
              mrn: resp.user.mrn,
              facilityId: "FAC-HQ-01",
              facilityName: "ZAYVORA Matab™ — Outpatient Care",
              permissions: roleMeta.permissions
            },
            expiresAt: Date.now() + 3600 * 1000
          };
          if (typeof window !== "undefined") {
            localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
          }
          return session;
        }
      } else {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.error || errJson.detail || `Registration failed (${res.status})`);
      }
    } catch (e: any) {
      fetchError = e;
      if (e.message && !e.message.includes("Failed to fetch") && !e.message.includes("NetworkError")) {
        throw e;
      }
    }

    if (isDemoModeAllowed()) {
      return this.register(data);
    }

    throw fetchError || new Error("Registration service is unavailable. Secure production mode requires an active connection to the identity service.");
  }

  static async requestPasswordResetAsync(identifier: string): Promise<{ ok: boolean; message: string }> {
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered mobile or email to receive recovery OTP.");
    }
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Failed to dispatch recovery OTP.");
      }
      return { ok: true, message: data.message || "Recovery OTP dispatched successfully." };
    } catch (e: any) {
      if (isDemoModeAllowed()) {
        return { ok: true, message: "Demo mode: Recovery OTP dispatched to registered channel." };
      }
      throw e;
    }
  }

  static async resetPasswordAsync(identifier: string, otp: string, newPassword: string): Promise<{ ok: boolean; message: string }> {
    if (!identifier || !otp || !newPassword) {
      throw new Error("Identifier, verification OTP, and new password are all required.");
    }
    if (newPassword.length < 8) {
      throw new Error("New password must be at least 8 characters long.");
    }
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

    try {
      const res = await fetch(`${API_URL}/api/v1/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier, otp, newPassword })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Password reset failed. Please check OTP.");
      }
      return { ok: true, message: data.message || "Password updated successfully." };
    } catch (e: any) {
      if (isDemoModeAllowed()) {
        return { ok: true, message: "Demo mode: Password reset successfully." };
      }
      throw e;
    }
  }

  static async requestOtpAsync(identifier: string, channel: "sms" | "email" = "sms"): Promise<{ ok: boolean; message: string; challenge_id?: string }> {
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered mobile number or email address.");
    }
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${API_URL}/api/v1/auth/otp/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier: identifier.trim(), channel })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Failed to dispatch verification OTP.");
      }
      return { ok: true, message: data.message || "OTP sent successfully.", challenge_id: data.challenge_id };
    } catch (e: any) {
      if (isDemoModeAllowed()) {
        return { ok: true, message: "Demo Mode: Verification OTP sent to " + identifier };
      }
      throw e;
    }
  }

  static async verifyOtpAsync(identifier: string, otp: string): Promise<UserSession | { ok: boolean; is_registered: false; verification_token: string }> {
    if (!identifier || !otp) {
      throw new Error("Identifier and verification OTP code are required.");
    }
    const API_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";
    try {
      const res = await fetch(`${API_URL}/api/v1/auth/otp/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier: identifier.trim(), otp: otp.trim() })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data.error || data.detail || "Invalid or expired OTP code.");
      }
      if (data.is_registered === false) {
        return { ok: true, is_registered: false, verification_token: data.verification_token };
      }
      if (data.user) {
        const roleMeta = ROLE_DEFINITIONS[data.user.role as UserRoleType] || ROLE_DEFINITIONS.PATIENT;
        const session: UserSession = {
          token: data.token || ("sess-live-" + Date.now()),
          user: {
            id: data.user.id,
            fullName: data.user.fullName,
            email: data.user.email,
            phone: data.user.phone || "",
            role: data.user.role as UserRoleType,
            roleDisplayName: roleMeta.displayName,
            mrn: data.user.mrn,
            facilityId: data.user.facilityId || "FAC-HQ-01",
            facilityName: data.user.facilityName || roleMeta.defaultFacility,
            permissions: roleMeta.permissions
          },
          expiresAt: Date.now() + 3600 * 1000
        };
        if (typeof window !== "undefined") {
          localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
        }
        return session;
      }
      throw new Error("Unexpected response from authentication server.");
    } catch (e: any) {
      if (isDemoModeAllowed()) {
        return this.login(identifier, "demo-pass", "PATIENT");
      }
      throw e;
    }
  }

  static requestPasswordReset(identifier: string): boolean {
    if (!isDemoModeAllowed()) {
      throw new Error("Synchronous mock password reset is disabled in production. Use requestPasswordResetAsync.");
    }
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered mobile or email to receive recovery OTP.");
    }
    return true;
  }

  static verifyOtp(identifier: string, otp: string): boolean {
    if (!isDemoModeAllowed()) {
      throw new Error("Synchronous mock OTP verification is disabled in production. Use resetPasswordAsync or verifyOtpAsync.");
    }
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
