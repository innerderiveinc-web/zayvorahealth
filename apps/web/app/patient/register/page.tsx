"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AuthService } from "@/lib/services/authService";

export default function PatientRegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    mobile: "",
    age: 35,
    gender: "Male",
    consent: true
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsLoading(true);

    try {
      AuthService.register(formData);
      router.push("/patient");
    } catch (err: any) {
      setErrorMessage(err.message || "Registration failed. Please review your details.");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070D18] flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-slate-100 relative overflow-hidden">
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-teal-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="sm:mx-auto sm:w-full sm:max-w-lg text-center relative z-10 space-y-3">
        <Link href="/website" className="inline-flex items-center gap-2.5 text-xl font-bold text-white tracking-wide group">
          <span className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-600 to-emerald-400 flex items-center justify-center text-white text-lg shadow-lg shadow-teal-900/30 group-hover:scale-105 transition">
            🌿
          </span>
          <span className="font-extrabold tracking-tight">ZAYVORA<span className="text-teal-400 font-light ml-1">HEALTH</span></span>
        </Link>
        <h2 className="text-2xl font-bold tracking-tight text-white">
          Create Your Patient Health Account
        </h2>
        <p className="text-xs text-slate-400">
          Register to view clinical care plans, track your Unani medicines, and schedule consultations
        </p>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-lg relative z-10">
        <div className="bg-[#0F172A]/90 backdrop-blur-md py-8 px-6 sm:px-10 rounded-3xl border border-slate-800 shadow-2xl space-y-6">

          {errorMessage && (
            <div className="p-3 rounded-xl bg-rose-950/70 border border-rose-800 text-rose-300 text-xs flex items-center gap-2">
              <span>⚠</span>
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-300 mb-1">
                Full Legal Name <span className="text-rose-400">*</span>
              </label>
              <input
                type="text"
                placeholder="e.g. Hamza Farooqi"
                value={formData.fullName}
                onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                required
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Mobile Number <span className="text-rose-400">*</span>
                </label>
                <input
                  type="tel"
                  placeholder="+91-9876543210"
                  value={formData.mobile}
                  onChange={(e) => setFormData({ ...formData, mobile: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Email Address <span className="text-rose-400">*</span>
                </label>
                <input
                  type="email"
                  placeholder="patient@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block font-semibold text-slate-300 mb-1">Age</label>
                <input
                  type="number"
                  min="1"
                  max="120"
                  value={formData.age}
                  onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  required
                />
              </div>
              <div>
                <label className="block font-semibold text-slate-300 mb-1">Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="w-full px-3 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-800/60 flex items-start gap-2.5">
              <input
                type="checkbox"
                id="regConsent"
                checked={formData.consent}
                onChange={(e) => setFormData({ ...formData, consent: e.target.checked })}
                className="mt-0.5 rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                required
              />
              <label htmlFor="regConsent" className="text-slate-300 text-[11px] leading-relaxed cursor-pointer">
                I agree to the ZAYVORA Health Terms of Service, Privacy Policy, and consent to clinical data processing under Ayushman Bharat Digital Mission (ABDM) standards.
              </label>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 rounded-xl bg-teal-600 hover:bg-teal-500 disabled:bg-slate-800 disabled:text-slate-600 text-white font-bold transition shadow-lg shadow-teal-900/30 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span>Registering Profile...</span>
                </>
              ) : (
                <span>Complete Registration & Enter Portal →</span>
              )}
            </button>
          </form>

          <div className="pt-4 border-t border-slate-800 text-center text-xs text-slate-400">
            <span>Already registered with us? </span>
            <Link href="/patient/login" className="text-teal-400 font-bold hover:underline">
              Sign In to Your Account
            </Link>
          </div>
        </div>

        <div className="text-center mt-6">
          <Link href="/website" className="text-xs text-slate-500 hover:text-slate-300 transition">
            ← Return to ZAYVORA Public Website
          </Link>
        </div>
      </div>
    </div>
  );
}
