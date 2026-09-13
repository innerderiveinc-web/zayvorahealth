"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AuthService } from "@/lib/services/authService";

export default function PatientLoginPage() {
  const router = useRouter();
  const [authMode, setAuthMode] = useState<"password" | "otp">("password");
  const [identifier, setIdentifier] = useState("hamza.farooqi@gmail.com");
  const [password, setPassword] = useState("••••••••");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier) {
      setErrorMessage("Please enter your registered mobile number or email address.");
      return;
    }
    setIsLoading(true);
    setErrorMessage(null);
    setTimeout(() => {
      setIsLoading(false);
      setOtpSent(true);
    }, 600);
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsLoading(true);

    try {
      if (authMode === "password") {
        AuthService.login(identifier, password || "password123");
      } else {
        if (!otp || otp.length < 4) {
          throw new Error("Please enter the 6-digit OTP sent to your phone/email.");
        }
        AuthService.login(identifier, "otp-verified");
      }
      router.push("/patient");
    } catch (err: any) {
      setErrorMessage(err.message || "Invalid credentials. Please verify and try again.");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-slate-100 relative overflow-hidden">
      {/* Subtle Background Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center relative z-10 space-y-3">
        <Link href="/website" className="inline-flex items-center gap-2.5 text-xl font-bold text-white tracking-wide group">
          <span className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-400 flex items-center justify-center text-white text-lg shadow-lg shadow-teal-900/30 group-hover:scale-105 transition">
            🌿
          </span>
          <span className="font-extrabold tracking-tight">ZAYVORA<span className="text-teal-400 font-light ml-1">HEALTH</span></span>
        </Link>
        <h2 className="text-2xl font-bold tracking-tight text-white">
          Patient Portal Login
        </h2>
        <p className="text-xs text-slate-400">
          Access your digital health record, active prescriptions, and care plan
        </p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="bg-[#0F172A]/90 backdrop-blur-md py-8 px-6 sm:px-10 rounded-3xl border border-slate-800 shadow-2xl space-y-6">
          
          {/* Auth Method Switcher */}
          <div className="grid grid-cols-2 gap-2 bg-slate-900/90 p-1.5 rounded-xl border border-slate-800 text-xs">
            <button
              type="button"
              onClick={() => { setAuthMode("password"); setErrorMessage(null); }}
              className={`py-2 rounded-lg font-semibold transition ${
                authMode === "password"
                  ? "bg-teal-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Password Login
            </button>
            <button
              type="button"
              onClick={() => { setAuthMode("otp"); setErrorMessage(null); }}
              className={`py-2 rounded-lg font-semibold transition ${
                authMode === "otp"
                  ? "bg-teal-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Instant OTP Login
            </button>
          </div>

          {errorMessage && (
            <div className="p-3 rounded-xl bg-rose-950/70 border border-rose-800 text-rose-300 text-xs flex items-center gap-2">
              <span>⚠</span>
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-300 mb-1">
                Email Address or Registered Mobile
              </label>
              <input
                type="text"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="name@example.com or +91-9876543210"
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                required
              />
            </div>

            {authMode === "password" ? (
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block font-semibold text-slate-300">
                    Password
                  </label>
                  <Link href="/patient/forgot-password" className="text-teal-400 hover:underline text-[11px]">
                    Forgot Password?
                  </Link>
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your account password"
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
            ) : (
              <div>
                {!otpSent ? (
                  <button
                    type="button"
                    onClick={handleSendOtp}
                    disabled={isLoading}
                    className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-400 font-semibold border border-slate-700 transition"
                  >
                    {isLoading ? "Sending OTP..." : "Request 6-Digit OTP via SMS/Email"}
                  </button>
                ) : (
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <label className="block font-semibold text-slate-300">
                        Enter 6-Digit OTP
                      </label>
                      <button
                        type="button"
                        onClick={handleSendOtp}
                        className="text-[11px] text-teal-400 hover:underline"
                      >
                        Resend Code
                      </button>
                    </div>
                    <input
                      type="text"
                      maxLength={6}
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                      placeholder="123456"
                      className="w-full text-center tracking-widest text-lg font-mono px-4 py-2 rounded-xl bg-slate-900 border border-teal-500 text-white focus:outline-none"
                      required
                    />
                    <p className="text-[10px] text-emerald-400 text-center">
                      Demo OTP: Enter any 6 digits (e.g. 123456)
                    </p>
                  </div>
                )}
              </div>
            )}

            <div className="flex items-center justify-between pt-1">
              <label className="flex items-center gap-2 cursor-pointer text-slate-400">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                />
                <span>Remember this device</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading || (authMode === "otp" && !otpSent)}
              className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 disabled:text-slate-600 text-white font-bold transition shadow-lg shadow-teal-900/30 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span>Verifying Session...</span>
                </>
              ) : (
                <span>Access Patient Portal →</span>
              )}
            </button>
          </form>

          {/* New Patient Registration Prompt */}
          <div className="pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
            <span>First time consulting at ZAYVORA? </span>
            <Link href="/patient/register" className="text-teal-400 font-bold hover:underline">
              Create Patient Account
            </Link>
          </div>

          {/* Compliance Badges */}
          <div className="flex items-center justify-center gap-4 text-[10px] text-slate-500 pt-2 border-t border-slate-800/60">
            <span>🔒 256-Bit SSL Encrypted</span>
            <span>•</span>
            <span>ABDM Ayushman Bharat Linked</span>
            <span>•</span>
            <span>HIPAA Compliant</span>
          </div>

        </div>

        {/* Back Link */}
        <div className="text-center mt-6">
          <Link href="/website" className="text-xs text-slate-500 hover:text-slate-300 transition">
            ← Return to ZAYVORA Public Website
          </Link>
        </div>
      </div>
    </div>
  );
}
