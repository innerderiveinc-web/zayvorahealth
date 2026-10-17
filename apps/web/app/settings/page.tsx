"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

type SettingsTab = "profile" | "clinic" | "security" | "notifications" | "localization";

export default function SettingsWorkspacePage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>("profile");
  const [saveNotice, setSaveNotice] = useState<string | null>(null);

  // Form states
  const [doctorName, setDoctorName] = useState("Prof. (Dr.) Mansoor Alam");
  const [doctorReg, setDoctorReg] = useState("NCISM-BUMS-1988-0412");
  const [doctorEmail, setDoctorEmail] = useState("mansoor.alam@zayvorahealth.com");
  const [doctorPhone, setDoctorPhone] = useState("+91 98110 44219");
  const [specialty, setSpecialty] = useState("Senior Consulting Tabeeb (M.D. Ilmul Advia)");

  // Clinic states
  const [clinicName, setClinicName] = useState("ZAYVORA Matab™ — Central Care Centre");
  const [opdTiming, setOpdTiming] = useState("09:00 AM – 06:00 PM");
  const [standardFee, setStandardFee] = useState("800");
  const [followupFee, setFollowupFee] = useState("500");

  // Notification states
  const [smsAlerts, setSmsAlerts] = useState(true);
  const [whatsappAlerts, setWhatsappAlerts] = useState(true);
  const [drugAlerts, setDrugAlerts] = useState(true);
  const [labThresholdAlerts, setLabThresholdAlerts] = useState(true);

  // Security states
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(true);
  const [merkleAuditAnchoring, setMerkleAuditAnchoring] = useState(true);

  // Localization states
  const [primaryLanguage, setPrimaryLanguage] = useState<"EN" | "HI" | "UR">("EN");
  const [timezone, setTimezone] = useState("Asia/Kolkata (IST, UTC+05:30)");

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaveNotice("Settings preferences updated and cryptographically sealed.");
    setTimeout(() => setSaveNotice(null), 3500);
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-6xl mx-auto">
        
        {/* Header Title */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>⚙️</span> Account & Clinical Settings
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              Configure clinician credentials, facility parameters, security controls, and communication gateways.
            </p>
          </div>
          {saveNotice && (
            <span className="px-3 py-1 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold animate-pulse">
              ✓ {saveNotice}
            </span>
          )}
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap items-center gap-2 border-b border-[var(--border)] pb-2 text-xs font-semibold">
          <button
            onClick={() => setActiveTab("profile")}
            className={`px-3.5 py-2 rounded-xl transition ${
              activeTab === "profile"
                ? "bg-[#0D9488] text-white shadow-xs"
                : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
            }`}
          >
            👤 Clinician Profile
          </button>
          <button
            onClick={() => setActiveTab("clinic")}
            className={`px-3.5 py-2 rounded-xl transition ${
              activeTab === "clinic"
                ? "bg-[#0D9488] text-white shadow-xs"
                : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
            }`}
          >
            🏥 Facility & OPD Timing
          </button>
          <button
            onClick={() => setActiveTab("security")}
            className={`px-3.5 py-2 rounded-xl transition ${
              activeTab === "security"
                ? "bg-[#0D9488] text-white shadow-xs"
                : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
            }`}
          >
            🔒 Security & 21 CFR 11
          </button>
          <button
            onClick={() => setActiveTab("notifications")}
            className={`px-3.5 py-2 rounded-xl transition ${
              activeTab === "notifications"
                ? "bg-[#0D9488] text-white shadow-xs"
                : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
            }`}
          >
            🔔 Notifications & QSURA
          </button>
          <button
            onClick={() => setActiveTab("localization")}
            className={`px-3.5 py-2 rounded-xl transition ${
              activeTab === "localization"
                ? "bg-[#0D9488] text-white shadow-xs"
                : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
            }`}
          >
            🌐 Language & Locale
          </button>
        </div>

        {/* Form Container */}
        <form onSubmit={handleSave} className="space-y-6">
          
          {/* TAB 1: CLINICIAN PROFILE */}
          {activeTab === "profile" && (
            <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">Clinician Credentials & Signature</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Full Name & Honorific</label>
                  <input
                    type="text"
                    value={doctorName}
                    onChange={(e) => setDoctorName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Statutory Council Registration No.</label>
                  <input
                    type="text"
                    value={doctorReg}
                    onChange={(e) => setDoctorReg(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white font-mono focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Clinical Specialty & Qualification</label>
                  <input
                    type="text"
                    value={specialty}
                    onChange={(e) => setSpecialty(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Professional Email</label>
                  <input
                    type="email"
                    value={doctorEmail}
                    onChange={(e) => setDoctorEmail(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Contact Phone (WhatsApp Dispatch)</label>
                  <input
                    type="tel"
                    value={doctorPhone}
                    onChange={(e) => setDoctorPhone(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Prescription Sealing Certificate</label>
                  <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono text-[11px] flex items-center justify-between">
                    <span>✓ SHA-256 PKI Key Installed</span>
                    <span className="text-[10px] font-bold">Valid thru 2028</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: CLINIC SETTINGS */}
          {activeTab === "clinic" && (
            <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">Facility Roster & Fee Schedule</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Facility / Clinic Name</label>
                  <input
                    type="text"
                    value={clinicName}
                    onChange={(e) => setClinicName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">OPD Consultation Shift Hours</label>
                  <input
                    type="text"
                    value={opdTiming}
                    onChange={(e) => setOpdTiming(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Standard Initial OPD Fee (₹)</label>
                  <input
                    type="number"
                    value={standardFee}
                    onChange={(e) => setStandardFee(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white font-mono focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Follow-Up Review Fee (₹)</label>
                  <input
                    type="number"
                    value={followupFee}
                    onChange={(e) => setFollowupFee(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white font-mono focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: SECURITY & 21 CFR PART 11 */}
          {activeTab === "security" && (
            <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">Security, Encryption & Cryptographic Auditing</h2>
              
              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">Two-Factor Authentication (2FA)</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Mandate OTP confirmation for clinical login and digital prescription signing.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={twoFactorEnabled}
                    onChange={(e) => setTwoFactorEnabled(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">21 CFR Part 11 Merkle-Tree Ledger</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Cryptographically chain all SOAP note approvals, Mudabbar releases, and prescription alterations.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={merkleAuditAnchoring}
                    onChange={(e) => setMerkleAuditAnchoring(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>

                <div className="p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)] space-y-2">
                  <h3 className="font-bold text-white">Active Cryptographic Sessions</h3>
                  <div className="space-y-1.5 font-mono text-[11px] text-[var(--muted)]">
                    <div className="flex justify-between items-center py-1 border-b border-[var(--border)]">
                      <span className="text-white">MacBook Pro (Clinical Cockpit) • Chrome 128</span>
                      <span className="text-emerald-400 font-bold">Active Now</span>
                    </div>
                    <div className="flex justify-between items-center py-1">
                      <span className="text-white">iPad Air (OPD Ward Rounds) • Safari Mobile</span>
                      <span className="text-[var(--muted)]">Last active 2h ago</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: NOTIFICATIONS & QSURA */}
          {activeTab === "notifications" && (
            <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">QSURA Notification Dispatch Channels</h2>
              
              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">Critical Drug Interaction & Safety Alerts</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Immediate alert chime and banner interception on Schedule E(1) contraindications.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={drugAlerts}
                    onChange={(e) => setDrugAlerts(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">Abnormal Diagnostic Lab Value Warnings</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Automated prompt when patient serum uric acid, ESR, or fasting glucose exceeds safe range.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={labThresholdAlerts}
                    onChange={(e) => setLabThresholdAlerts(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">SMS Appointment & Prescription Dispatch</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Send instant SMS confirmation tokens and pharmacy pickup alerts to patients.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={smsAlerts}
                    onChange={(e) => setSmsAlerts(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between p-4 rounded-2xl bg-[var(--elevated)] border border-[var(--border)]">
                  <div>
                    <h3 className="font-bold text-white">WhatsApp Care Plan & Voice Posology Dispatch</h3>
                    <p className="text-[var(--muted)] text-[11px] mt-0.5">Transmit audio posology voice instructions and PDF summaries via WhatsApp Business API.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={whatsappAlerts}
                    onChange={(e) => setWhatsappAlerts(e.target.checked)}
                    className="w-4 h-4 accent-[#0D9488] cursor-pointer"
                  />
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: LOCALIZATION */}
          {activeTab === "localization" && (
            <div className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5">
              <h2 className="text-sm font-bold text-white uppercase tracking-wider">Language, Locale & Timezone Settings</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Default Platform Language</label>
                  <select
                    value={primaryLanguage}
                    onChange={(e) => setPrimaryLanguage(e.target.value as "EN" | "HI" | "UR")}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  >
                    <option value="EN">English (Clinical Nomenclature)</option>
                    <option value="HI">हिन्दी (Hindi)</option>
                    <option value="UR">Urdu (Roman Transliteration / Monograph Text)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[var(--muted)] font-medium">Facility Timezone</label>
                  <input
                    type="text"
                    value={timezone}
                    onChange={(e) => setTimezone(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-[var(--elevated)] border border-[var(--border)] text-white focus:outline-none focus:border-[#2DD4BF]"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Save Button Bar */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-[var(--border)]">
            <Link
              href="/dashboard"
              className="px-4 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold transition"
            >
              Cancel
            </Link>
            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition shadow-sm"
            >
              Save Changes
            </button>
          </div>
        </form>

      </div>
    </AppShell>
  );
}
