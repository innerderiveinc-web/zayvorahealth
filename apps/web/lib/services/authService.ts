import { MOCK_PATIENT_PROFILE, PatientProfileData } from "../cms/patientMockData";

export interface UserSession {
  token: string;
  user: {
    id: string;
    fullName: string;
    email: string;
    phone: string;
    role: string;
    mrn: string;
    primaryMizaj: string;
  };
  expiresAt: number;
}

const SESSION_STORAGE_KEY = "zayvora_patient_session_v5";

export class AuthService {
  static login(identifier: string, pass: string): UserSession {
    if (!identifier || identifier.trim().length === 0) {
      throw new Error("Please enter your registered email address or mobile number.");
    }
    if (!pass || pass.length < 4) {
      throw new Error("Please enter your password (minimum 4 characters).");
    }

    // Authenticated mock session for demonstration
    const session: UserSession = {
      token: "sess-pat-" + Date.now(),
      user: {
        id: "PAT-774901",
        fullName: MOCK_PATIENT_PROFILE.fullName,
        email: MOCK_PATIENT_PROFILE.email,
        phone: MOCK_PATIENT_PROFILE.phone,
        role: "Patient",
        mrn: MOCK_PATIENT_PROFILE.mrn,
        primaryMizaj: MOCK_PATIENT_PROFILE.primaryMizaj
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
    if (!data.mobile || data.mobile.length < 10) {
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
        role: "Patient",
        mrn: "MRN-2026-" + Math.floor(1000 + Math.random() * 9000),
        primaryMizaj: "Assessment Pending"
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
    if (!otp || otp.length !== 6) {
      throw new Error("Please enter a valid 6-digit verification OTP.");
    }
    return otp === "123456" || true;
  }

  static getSession(): UserSession | null {
    if (typeof window === "undefined") return null;
    try {
      const stored = localStorage.getItem(SESSION_STORAGE_KEY);
      if (!stored) return null;
      const parsed: UserSession = JSON.parse(stored);
      if (Date.now() > parsed.expiresAt) {
        localStorage.removeItem(SESSION_STORAGE_KEY);
        return null;
      }
      return parsed;
    } catch {
      return null;
    }
  }

  static logout(): void {
    if (typeof window !== "undefined") {
      localStorage.removeItem(SESSION_STORAGE_KEY);
    }
  }
}
