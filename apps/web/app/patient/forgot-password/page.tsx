"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AuthService } from "@/lib/services/authService";

export default function ForgotPasswordPage() {
  const [identifier, setIdentifier] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier) {
      setErrorMessage("Please enter your registered mobile or email.");
      return;
    }
    setIsLoading(true);
    setErrorMessage(null);

    try {
      AuthService.requestPasswordReset(identifier);
      setTimeout(() => {
        setIsLoading(false);
        setSubmitted(true);
      }, 500);
    } catch (err: any) {
      setErrorMessage(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-slate-100 relative overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center relative z-10 space-y-3">
        <Link href="/website" className="inline-flex items-center gap-2.5 text-xl font-bold text-white tracking-wide">
          <span className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-400 flex items-center justify-center text-white text-lg">🌿</span>
          <span className="font-extrabold tracking-tight">ZAYVORA<span className="text-teal-400 font-light ml-1">HEALTH</span></span>
        </Link>
        <h2 className="text-2xl font-bold tracking-tight text-white">Reset Account Password</h2>
        <p className="text-xs text-slate-400">We will dispatch a secure 6-digit recovery OTP to your mobile or email</p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="bg-[#0F172A]/90 backdrop-blur-md py-8 px-6 sm:px-10 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
          {submitted ? (
            <div className="text-center space-y-4 text-xs">
              <div className="w-12 h-12 mx-auto rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-bold border border-emerald-500/40">
                ✓
              </div>
              <h3 className="text-base font-bold text-white">Recovery Link Sent</h3>
              <p className="text-slate-300">
                If an account exists for <strong className="text-teal-400">{identifier}</strong>, you will receive password reset instructions shortly.
              </p>
              <div className="pt-2">
                <Link
                  href="/patient/reset-password"
                  className="inline-block px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition text-xs"
                >
                  Enter Verification Code & Set New Password →
                </Link>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              {errorMessage && (
                <div className="p-3 rounded-xl bg-rose-950/70 border border-rose-800 text-rose-300 text-xs">
                  {errorMessage}
                </div>
              )}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Registered Email Address or Mobile
                </label>
                <input
                  type="text"
                  placeholder="patient@example.com or +91-9876543210"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 text-white font-bold transition shadow-lg shadow-teal-900/30 flex items-center justify-center"
              >
                {isLoading ? "Dispatching OTP..." : "Send Password Reset OTP"}
              </button>
            </form>
          )}

          <div className="pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
            <Link href="/patient/login" className="text-teal-400 font-medium hover:underline">
              ← Back to Patient Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
