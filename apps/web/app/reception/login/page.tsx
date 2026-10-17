"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { identityApi, ApiError } from "@/lib/identityApi";
import { saveSession } from "@/lib/session";

export default function ReceptionLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const session = await identityApi.login({
        email,
        password,
        organization_slug: "zayvora-central"
      });
      saveSession(session);
      router.push("/receptionist");
    } catch (err: any) {
      if (err instanceof ApiError) {
        setError(err.status === 429 ? "Too many attempts. Account locked. Please wait." : err.message || "Invalid receptionist credentials.");
      } else {
        setError(err.message || "Unable to reach identity server.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <PublicWebsiteShell>
      <div className="min-h-[80vh] flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-600 to-teal-600 flex items-center justify-center mx-auto text-xl shadow-lg mb-4 text-white">
              📋
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Reception & OPD Desk Login
            </h1>
            <p className="mt-2 text-xs text-slate-400">
              Walk-in Patient Check-in, Token Issuance & Consultation Queue
            </p>
          </div>

          <div className="rounded-3xl bg-[#0D1527] border border-slate-800 p-8 shadow-2xl space-y-6">
            {error && (
              <div className="p-3.5 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs flex items-center gap-2">
                <span>⚠️</span>
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Reception Staff Email / ID
                </label>
                <input
                  type="text"
                  required
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500"
                  placeholder="reception@zayvorahealth.com"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block text-xs font-semibold text-slate-300">
                    Password
                  </label>
                  <Link href="/patient/forgot-password" className="text-[11px] text-cyan-400 hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500"
                  placeholder="••••••••"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-cyan-600 to-teal-600 text-white font-bold text-sm shadow-md hover:brightness-110 transition disabled:opacity-50 mt-2"
              >
                {loading ? "Authenticating Staff..." : "Sign In to OPD Queue Desk →"}
              </button>
            </form>

            <div className="pt-6 border-t border-slate-800 space-y-2 text-center text-xs">
              <div className="flex items-center justify-center gap-3 pt-2 text-[11px] text-slate-500">
                <Link href="/login" className="hover:text-slate-300">Unified Staff Login</Link>
                <span>•</span>
                <Link href="/patient/login" className="hover:text-slate-300">Patient Portal</Link>
                <span>•</span>
                <Link href="/doctor/login" className="hover:text-slate-300">Clinician OPD</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
