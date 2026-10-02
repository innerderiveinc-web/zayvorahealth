"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { saveSession, getRoleDashboard, type ZayvoraSession } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [organizationSlug, setOrganizationSlug] = useState("zayvora-central");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8088/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password: password }),
      });

      if (!response.ok) {
        const errBody = await response.json().catch(() => ({}));
        throw new Error(errBody.detail || errBody.message || "Invalid credentials.");
      }

      const data = await response.json();

      // Build normalised session object
      const session: ZayvoraSession = {
        access_token: data.access_token || data.token,
        refresh_token: data.refresh_token,
        user: data.user || {},
        roles: data.roles || [data.user?.role || "PATIENT"],
        permissions: data.permissions || data.user?.permissions || [],
      };

      // Persist session to localStorage
      saveSession(session);

      // Role-based redirect — each role goes to its dedicated panel
      const role = session.user?.role || session.roles?.[0] || "PATIENT";
      const destination = getRoleDashboard(role);
      router.push(destination);

    } catch (err: any) {
      setError(err.message || "Authentication service is unreachable. Please verify server connectivity.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PublicWebsiteShell>
      <div className="min-h-[80vh] flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          
          {/* Header Card */}
          <div className="text-center">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#0D9488] to-[#2D6A4F] flex items-center justify-center mx-auto text-xl shadow-lg mb-4">
              🏥
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Sign In to ZAYVORA Health OS™
            </h1>
            <p className="mt-2 text-xs text-[#94A3B8]">
              Secure unified gateway for Clinicians, Patients, Pharmacy, and Administrators.
            </p>
          </div>

          {/* Form Card */}
          <div className="rounded-3xl bg-[#0D1527] border border-[#1E293B] p-8 shadow-2xl space-y-6">
            {error && (
              <div className="p-3.5 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs flex items-center gap-2">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  placeholder="name@zayvorahealth"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block text-xs font-semibold text-[#CBD5E1]">
                    Password
                  </label>
                  <Link href="/forgot-password" className="text-[11px] text-[#5EEAD4] hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  placeholder="••••••••"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                  Facility / Organization
                </label>
                <input
                  type="text"
                  value={organizationSlug}
                  onChange={e => setOrganizationSlug(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-[#0D9488] to-[#2D6A4F] text-white font-bold text-sm shadow-md hover:brightness-110 transition disabled:opacity-50 mt-2"
              >
                {loading ? "Authenticating..." : "Sign In →"}
              </button>
            </form>

            {/* Enterprise Security & Onboarding Pathways */}
            <div className="pt-6 border-t border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[#94A3B8]">Patient Portal:</span>
                <Link href="/patient/login" className="text-[#5EEAD4] font-semibold hover:underline">
                  My ZAYVORA™ Access →
                </Link>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-[#94A3B8]">Practitioner Credentialing:</span>
                <Link href="/clinician/apply" className="text-[#5EEAD4] font-semibold hover:underline">
                  NCISM Application →
                </Link>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-[#94A3B8]">Matab / Facility Partner:</span>
                <Link href="/organization/apply" className="text-[#5EEAD4] font-semibold hover:underline">
                  Institutional Onboarding →
                </Link>
              </div>

              {/* Department Quick Access Deep-links */}
              <div className="pt-3 border-t border-[#1E293B]/60 text-center">
                <span className="text-[10px] text-[#64748B] uppercase tracking-wider block mb-2 font-mono">
                  Role Portals
                </span>
                <div className="flex flex-wrap items-center justify-center gap-2 text-[11px]">
                  <Link href="/doctor/login" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Clinician OPD
                  </Link>
                  <Link href="/nurse" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Nurse Station
                  </Link>
                  <Link href="/pharmacy/login" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Dispensary
                  </Link>
                  <Link href="/reception/login" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Reception Desk
                  </Link>
                  <Link href="/research/workspace" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Clinical Research
                  </Link>
                  <Link href="/manufacturing" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Manufacturing Lab
                  </Link>
                  <Link href="/admin/login" className="px-2.5 py-1 rounded-lg bg-[#0A0F1D] text-[#CBD5E1] hover:text-white hover:border-[#0D9488] border border-[#1E293B] transition">
                    Governance
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* New Patient Registration Prompt */}
          <p className="text-center text-xs text-[#94A3B8]">
            New patient seeking holistic care?{" "}
            <Link href="/patient/register" className="text-[#5EEAD4] font-semibold hover:underline">
              Create Patient Health Account
            </Link>
          </p>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
