/**
 * ZAYVORA Health OS™ — useAuth Hook
 * Centralised client-side auth guard for all role-based panel pages.
 *
 * Usage:
 *   const { session, user, role, isLoading, logout } = useAuth({ requiredRoles: ["DOCTOR", "HAKEEM"] });
 *
 * - Reads session from lib/auth (localStorage + cookie).
 * - Falls back to legacy AuthService session so no existing sessions break.
 * - Redirects to /login if no valid session is found.
 * - Redirects to role dashboard if user accesses wrong panel.
 */

"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter, usePathname } from "next/navigation";
import {
  loadSession,
  clearSession,
  getRoleDashboard,
  getPrimaryRole,
  ZayvoraSession,
  ZayvoraRole,
} from "@/lib/auth";

export interface UseAuthOptions {
  /** If provided, user must have one of these roles or be redirected to their dashboard */
  requiredRoles?: ZayvoraRole[];
  /** Override redirect target when unauthenticated (default: /login) */
  loginPath?: string;
}

export interface UseAuthReturn {
  session: ZayvoraSession | null;
  user: ZayvoraSession["user"] | null;
  role: ZayvoraRole | null;
  isLoading: boolean;
  isAuthorized: boolean;
  logout: () => void;
}

export function useAuth(options: UseAuthOptions = {}): UseAuthReturn {
  const { requiredRoles, loginPath = "/login" } = options;
  const router = useRouter();
  const pathname = usePathname();

  const [session, setSession] = useState<ZayvoraSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = useCallback(() => {
    clearSession();
    router.push("/login");
  }, [router]);

  useEffect(() => {
    const s = loadSession();

    if (!s) {
      // No session — redirect to login preserving intended destination
      const redirect = encodeURIComponent(pathname || "/");
      router.replace(`${loginPath}?redirect=${redirect}`);
      setIsLoading(false);
      return;
    }

    const role = getPrimaryRole(s);

    // Role guard: if requiredRoles specified, check membership (SUPER_ADMIN has universal master access)
    if (requiredRoles && requiredRoles.length > 0) {
      const allowed = role === "SUPER_ADMIN" || requiredRoles.includes(role);
      if (!allowed) {
        // Send user to their correct dashboard instead
        router.replace(getRoleDashboard(role));
        setIsLoading(false);
        return;
      }
    }

    setSession(s);
    setIsLoading(false);
  }, [pathname, loginPath, requiredRoles, router]);

  const role = session ? getPrimaryRole(session) : null;
  const isAuthorized =
    !!session &&
    (!requiredRoles ||
      requiredRoles.length === 0 ||
      (role !== null && (role === "SUPER_ADMIN" || requiredRoles.includes(role))));

  return {
    session,
    user: session?.user ?? null,
    role,
    isLoading,
    isAuthorized,
    logout,
  };
}
