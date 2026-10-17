"use client";

import React, { useState } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";

export default function OrganizationApplyPage() {
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [appRef, setAppRef] = useState("");

  const [formData, setFormData] = useState({
    institutionName: "",
    institutionType: "Specialty Unani Matab & OPD",
    clinicalEstablishmentNumber: "",
    chiefMedicalOfficer: "",
    ncismRegNumber: "",
    city: "",
    state: "Delhi",
    phone: "",
    email: "",
    opdRoomCount: 3,
    hasDispensary: true,
    hasTadbeerWing: true,
    abdmReadiness: "Milestone 1 (ABHA Creation Verified)",
    notes: ""
  });

  const update = (f: string, v: any) => {
    setFormData(prev => ({ ...prev, [f]: v }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      const ref = `ORG-APP-2026-${Math.floor(1000 + Math.random() * 9000)}`;
      setAppRef(ref);
      setSubmitted(true);
    }, 1000);
  };

  return (
    <PublicWebsiteShell>
      <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-950/70 border border-teal-800 text-teal-400 text-xs font-mono mb-3">
            <span>🏥 Institutional Partnership</span>
            <span>•</span>
            <span>NABH / ABDM Compatible</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Institutional Matab & Facility Onboarding
          </h1>
          <p className="mt-2 text-sm text-slate-400 max-w-xl mx-auto">
            Deploy ZAYVORA Health OS™ across your hospital, clinic, or specialized Unani wellness centre with centralized governance, FEFO dispensary, and ABDM interoperability.
          </p>
        </div>

        {submitted ? (
          <div className="bg-[#0D1527] border border-slate-800 rounded-3xl p-8 sm:p-12 text-center space-y-6 shadow-2xl">
            <div className="w-16 h-16 rounded-full bg-teal-900/50 border border-teal-600 text-teal-300 flex items-center justify-center text-3xl mx-auto">
              ✓
            </div>
            <h2 className="text-2xl font-bold text-white">Facility Application Submitted</h2>
            <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800 inline-block font-mono text-sm text-teal-400">
              Reference: {appRef}
            </div>
            <p className="text-sm text-slate-400 max-w-lg mx-auto leading-relaxed">
              Thank you for partnering with ZAYVORA. Our Enterprise Onboarding and Clinical Audit team will contact <span className="text-white font-medium">{formData.email}</span> within 24 hours to schedule the facility review and configure your dedicated institutional tenancy.
            </p>
            <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/login" className="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition">
                Go to Staff Portal Login →
              </Link>
              <Link href="/" className="px-6 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">
                Return to Homepage
              </Link>
            </div>
          </div>
        ) : (
          <div className="bg-[#0D1527] border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl">
            <form onSubmit={handleSubmit} className="space-y-5 text-xs">
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Healthcare Institution Legal Name *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Al-Hikmah Integrated Unani Hospital & Research Centre"
                  value={formData.institutionName}
                  onChange={e => update("institutionName", e.target.value)}
                  className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Facility Classification *
                  </label>
                  <select
                    value={formData.institutionType}
                    onChange={e => update("institutionType", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  >
                    <option value="Specialty Unani Matab & OPD">Specialty Unani Matab & OPD</option>
                    <option value="Integrated AYUSH Hospital (IPD/OPD)">Integrated AYUSH Hospital (IPD/OPD)</option>
                    <option value="Academic Teaching Hospital & Research Wing">Academic Teaching Hospital & Research Wing</option>
                    <option value="Regimenal Therapy (Tadbeer) Wellness Centre">Regimenal Therapy (Tadbeer) Wellness Centre</option>
                    <option value="Licensed Unani Pharmacy & Dispensary">Licensed Unani Pharmacy & Dispensary</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Clinical Establishment Act Reg. No.
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. CEA-DEL-2021-9984"
                    value={formData.clinicalEstablishmentNumber}
                    onChange={e => update("clinicalEstablishmentNumber", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Designated Medical Director / Chief Tabeeb *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Prof. (Dr.) Mansoor Alam"
                    value={formData.chiefMedicalOfficer}
                    onChange={e => update("chiefMedicalOfficer", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Chief Tabeeb NCISM Reg. No. *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. UP-UNANI-2012-08819"
                    value={formData.ncismRegNumber}
                    onChange={e => update("ncismRegNumber", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Institutional Email Address *
                  </label>
                  <input
                    type="email"
                    required
                    placeholder="contact@alhikmah.health"
                    value={formData.email}
                    onChange={e => update("email", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Contact Phone Number *
                  </label>
                  <input
                    type="tel"
                    required
                    placeholder="+91-11-23456789"
                    value={formData.phone}
                    onChange={e => update("phone", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">City *</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. New Delhi"
                    value={formData.city}
                    onChange={e => update("city", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">State / UT *</label>
                  <select
                    value={formData.state}
                    onChange={e => update("state", e.target.value)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  >
                    <option value="Delhi">Delhi</option>
                    <option value="Uttar Pradesh">Uttar Pradesh</option>
                    <option value="Telangana">Telangana</option>
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Bihar">Bihar</option>
                    <option value="Jammu & Kashmir">Jammu & Kashmir</option>
                    <option value="Other">Other State</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">Active OPD Rooms</label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    value={formData.opdRoomCount}
                    onChange={e => update("opdRoomCount", parseInt(e.target.value) || 1)}
                    className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                <span className="font-semibold text-slate-300 block mb-1">Facility Capabilities:</span>
                <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                  <input
                    type="checkbox"
                    checked={formData.hasDispensary}
                    onChange={e => update("hasDispensary", e.target.checked)}
                    className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                  />
                  <span>In-house Pharmacy / Dispensary (Requires FEFO Cold-Chain Tracking)</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer text-slate-300">
                  <input
                    type="checkbox"
                    checked={formData.hasTadbeerWing}
                    onChange={e => update("hasTadbeerWing", e.target.checked)}
                    className="rounded border-slate-700 text-teal-600 focus:ring-teal-500 h-4 w-4"
                  />
                  <span>Ilaj-bit-Tadbeer Clinical Wing (Hijama, Dal'k, Hammam, Fasd Chambers)</span>
                </label>
              </div>

              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Additional Clinical Requirements or Existing EMR Integration
                </label>
                <textarea
                  rows={3}
                  value={formData.notes}
                  onChange={e => update("notes", e.target.value)}
                  placeholder="Describe your current patient volume, hardware peripherals (e.g. pulse sensors), or migration timeline..."
                  className="w-full px-4 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-600 focus:outline-none focus:border-teal-500"
                />
              </div>

              <div className="p-3 rounded-xl bg-teal-950/40 border border-teal-800/60 text-[11px] text-slate-300">
                <span>🛡️ Enterprise Review Policy: Facility applications undergo statutory verification of clinical licenses and medical superintendent credentials prior to provisioning isolated multi-tenant instance.</span>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:brightness-110 text-white font-bold transition shadow-lg shadow-teal-900/40 flex items-center justify-center gap-2"
              >
                {submitting ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    <span>Submitting Facility Application...</span>
                  </>
                ) : (
                  <span>Submit Institutional Application →</span>
                )}
              </button>
            </form>

            <div className="pt-6 border-t border-slate-800 text-center text-xs text-slate-400">
              <span>Already an authorized facility? </span>
              <Link href="/login" className="text-teal-400 font-bold hover:underline">
                Sign In to ZAYVORA Health OS™
              </Link>
            </div>
          </div>
        )}
      </div>
    </PublicWebsiteShell>
  );
}
