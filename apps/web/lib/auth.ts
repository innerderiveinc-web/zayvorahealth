/**
 * ZAYVORA Health OS™ — Auth Utility
 * Role-based session management and route resolution.
 * All roles defined here match the backend ROLE_PERMISSIONS in live_api_server.py
 */

export type ZayvoraRole =
  | "SUPER_ADMIN"
  | "CLINIC_ADMIN"
  | "DOCTOR"
  | "HAKEEM"
  | "RECEPTIONIST"
  | "PHARMACIST"
  | "PATIENT"
  | "NURSE"
  | "NURSE_COORDINATOR"
  | "RESEARCHER"
  | "MANUFACTURING_HEAD"
  | "SUPPORT_STAFF";

export interface ZayvoraSession {
  access_token: string;
  refresh_token?: string;
  user: {
    id: string;
    email: string;
    fullName: string;
    role: ZayvoraRole;
    mrn?: string;
    facilityId: string;
    facilityName: string;
    permissions: string[];
  };
  roles: ZayvoraRole[];
  permissions: string[];
}

const SESSION_KEY = "zayvora_session_v2";

/** Map each role to its dedicated dashboard route */
export const ROLE_DASHBOARD_MAP: Record<ZayvoraRole, string> = {
  SUPER_ADMIN:        "/admin",
  CLINIC_ADMIN:       "/admin",
  DOCTOR:             "/doctor",
  HAKEEM:             "/doctor",
  RECEPTIONIST:       "/receptionist",
  PHARMACIST:         "/pharmacy",
  PATIENT:            "/patient",
  NURSE:              "/nurse",
  NURSE_COORDINATOR:  "/nurse",
  RESEARCHER:         "/research/workspace",
  MANUFACTURING_HEAD: "/manufacturing",
  SUPPORT_STAFF:      "/admin",
};

/** Resolve the correct dashboard URL for a given role */
export function getRoleDashboard(role: ZayvoraRole | string): string {
  const normalized = role.toUpperCase() as ZayvoraRole;
  return ROLE_DASHBOARD_MAP[normalized] ?? "/dashboard";
}

/** Save session to localStorage + set middleware-readable cookie */
export function saveSession(session: ZayvoraSession): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    // Legacy keys — backward compat with existing dashboard code
    localStorage.setItem("zayvora_token", session.access_token);
    localStorage.setItem("zayvora_user", JSON.stringify(session.user));

    // Cookie signal for Next.js middleware (server-side auth guard).
    // Format: "ROLE|token_first16chars" — NOT sensitive, just a gate signal.
    // Full JWT validation still happens on every API call.
    const role = session.user?.role || session.roles?.[0] || "PATIENT";
    const tokenSnippet = session.access_token.slice(0, 16);
    const cookieValue = `${role}|${tokenSnippet}`;
    const maxAge = 60 * 60 * 24; // 24 hours
    document.cookie = `zayvora_auth=${encodeURIComponent(cookieValue)}; path=/; max-age=${maxAge}; SameSite=Strict`;
  } catch {
    // Storage quota exceeded — not critical
  }
}

/** Load session from localStorage */
export function loadSession(): ZayvoraSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (raw) return JSON.parse(raw) as ZayvoraSession;

    // Fallback: try legacy keys
    const token = localStorage.getItem("zayvora_token");
    const user = localStorage.getItem("zayvora_user");
    if (token && user) {
      const parsedUser = JSON.parse(user);
      return {
        access_token: token,
        user: parsedUser,
        roles: [parsedUser.role],
        permissions: parsedUser.permissions || [],
      };
    }
    return null;
  } catch {
    return null;
  }
}

/** Clear session — used on logout */
export function clearSession(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(SESSION_KEY);
  localStorage.removeItem("zayvora_token");
  localStorage.removeItem("zayvora_user");
  // Clear the middleware auth cookie
  document.cookie = "zayvora_auth=; path=/; max-age=0; SameSite=Strict";
}

/** Get the primary role from session */
export function getPrimaryRole(session: ZayvoraSession): ZayvoraRole {
  return (session.user?.role || session.roles?.[0] || "PATIENT") as ZayvoraRole;
}

/** Check if user has a specific permission */
export function hasPermission(session: ZayvoraSession, permission: string): boolean {
  const perms = session.permissions || session.user?.permissions || [];
  return perms.includes("*") || perms.includes(permission);
}
