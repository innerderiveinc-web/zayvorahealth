"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AuthService } from "@/lib/services/authService";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier) {
      setErrorMessage("Please enter your registered email or mobile.");
      return;
    }
    if (!otp || otp.length < 4) {
      setErrorMessage("Please enter the 6-digit verification OTP.");
      return;
    }
    if (newPassword.length < 8) {
      setErrorMessage("New password must be at least 8 characters long.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setErrorMessage("Passwords do not match. Please re-enter.");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      await AuthService.resetPasswordAsync(identifier, otp, newPassword);
      setIsLoading(false);
      setSuccess(true);
      setTimeout(() => {
        router.push("/patient/login");
      }, 2000);
    } catch (err: any) {
      setErrorMessage(err.message || "Password reset verification failed.");
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
        <h2 className="text-2xl font-bold tracking-tight text-white">Set New Password</h2>
        <p className="text-xs text-slate-400">Enter the verification code and your new secure credentials</p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="bg-[#0F172A]/90 backdrop-blur-md py-8 px-6 sm:px-10 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
          {success ? (
            <div className="text-center space-y-3 text-xs">
              <div className="w-12 h-12 mx-auto rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl font-bold border border-emerald-500/40">
                ✓
              </div>
              <h3 className="text-base font-bold text-white">Password Updated Successfully</h3>
              <p className="text-slate-300">Redirecting to login in 2 seconds...</p>
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

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  6-Digit Recovery OTP
                </label>
                <input
                  type="text"
                  maxLength={6}
                  placeholder="123456"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  className="w-full text-center tracking-widest text-lg font-mono px-4 py-2 rounded-xl bg-slate-900 border border-teal-500 text-white focus:outline-none"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  New Password (min 8 characters)
                </label>
                <input
                  type="password"
                  placeholder="••••••••"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  required
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 text-white font-bold transition shadow-lg shadow-teal-900/30 flex items-center justify-center"
              >
                {isLoading ? "Verifying & Updating..." : "Update Password & Sign In →"}
              </button>
            </form>
          )}

          <div className="pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
            <Link href="/patient/login" className="text-teal-400 font-medium hover:underline">
              ← Return to Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
