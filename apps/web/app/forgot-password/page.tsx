"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8088/api/v1/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email })
      });
      if (!response.ok) {
        throw new Error("Failed to send reset link.");
      }
      setSubmitted(true);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PublicWebsiteShell>
      <div className="min-h-[75vh] flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Reset Your Password
            </h1>
            <p className="mt-2 text-xs text-[#94A3B8]">
              Enter your registered clinical or patient email address to receive secure reset instructions.
            </p>
          </div>

          <div className="rounded-3xl bg-[#0D1527] border border-[#1E293B] p-8 shadow-2xl space-y-6">
            {submitted ? (
              <div className="text-center space-y-4">
                <div className="w-12 h-12 rounded-full bg-[#0D9488]/20 border border-[#0D9488] flex items-center justify-center mx-auto text-xl text-[#5EEAD4]">
                  ✓
                </div>
                <h3 className="text-lg font-bold text-white">Reset Link Dispatched</h3>
                <p className="text-xs text-[#94A3B8] leading-relaxed">
                  If an account exists for <strong className="text-white">{email}</strong>, password reset instructions and a cryptographic verification token have been sent.
                </p>
                <div className="pt-4">
                  <Link
                    href="/login"
                    className="block w-full py-2.5 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-white text-xs font-semibold transition"
                  >
                    ← Return to Login
                  </Link>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <div className="p-3.5 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs flex items-center gap-2">
                    <span>⚠️</span>
                    <span>{error}</span>
                  </div>
                )}
                <div>
                  <label className="block text-xs font-semibold text-[#CBD5E1] mb-1">
                    Registered Email Address
                  </label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    placeholder="doctor@zayvorahealth"
                    className="w-full px-4 py-2.5 rounded-xl bg-[#0A0F1D] border border-[#334155] text-white text-sm focus:outline-none focus:border-[#0D9488]"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 rounded-xl bg-gradient-to-r from-[#0D9488] to-[#2D6A4F] text-white font-bold text-sm shadow-md hover:brightness-110 transition disabled:opacity-50 mt-2"
                >
                  {loading ? "Sending..." : "Send Reset Token →"}
                </button>

                <div className="text-center pt-2">
                  <Link href="/login" className="text-xs text-[#5EEAD4] hover:underline">
                    ← Back to Sign In
                  </Link>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </PublicWebsiteShell>
  );
}
