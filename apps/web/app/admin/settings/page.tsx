"use client";

import React, { useState } from "react";

export default function AdminSettingsPage() {
  const [settings, setSettings] = useState({
    mfaEnforced: true,
    sessionTimeoutMinutes: 60,
    twoPhaseClinicalLock: true,
    part11AuditTrail: true,
    stripeLiveMode: false,
    qsuraSmsAlerts: true,
    fhirInteroperability: true,
    neo4jKnowledgeSync: true,
  });

  const [saved, setSaved] = useState(false);

  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-800">Platform & Governance Settings</h2>
          <p className="text-xs text-gray-500">
            System-wide security policies, compliance locks, and external API configurations.
          </p>
        </div>
        {saved && (
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 animate-pulse">
            ✓ Settings Saved
          </span>
        )}
      </div>

      <form onSubmit={handleSave} className="space-y-6 text-sm">
        {/* Clinical Safety & Compliance */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2">
            <span>🛡️</span> Clinical Safety & 21 CFR Part 11 Invariants
          </h3>

          <div className="space-y-3">
            <label className="flex items-start justify-between cursor-pointer">
              <div>
                <span className="font-semibold text-gray-700 block">Enforce safe_to_lock=False on Clinical AI</span>
                <span className="text-xs text-gray-500 block">
                  Prescription locks require human clinician review. Automated prescribing is prohibited.
                </span>
              </div>
              <input
                type="checkbox"
                checked={settings.twoPhaseClinicalLock}
                disabled
                className="mt-1 h-4 w-4 text-[#2D6A4F] rounded border-gray-300"
              />
            </label>

            <label className="flex items-start justify-between cursor-pointer">
              <div>
                <span className="font-semibold text-gray-700 block">21 CFR Part 11 Cryptographic Audit Trail</span>
                <span className="text-xs text-gray-500 block">
                  Generate SHA-256 HMAC digest on all eBMR releases and electronic prescription locks.
                </span>
              </div>
              <input
                type="checkbox"
                checked={settings.part11AuditTrail}
                onChange={(e) => setSettings({ ...settings, part11AuditTrail: e.target.checked })}
                className="mt-1 h-4 w-4 text-[#2D6A4F] rounded border-gray-300"
              />
            </label>
          </div>
        </div>

        {/* Security & Authentication */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2">
            <span>🔐</span> Authentication & Session Security
          </h3>

          <div className="space-y-3">
            <label className="flex items-start justify-between cursor-pointer">
              <div>
                <span className="font-semibold text-gray-700 block">Enforce TOTP Multi-Factor Authentication (MFA)</span>
                <span className="text-xs text-gray-500 block">
                  Mandatory for clinical roles (Hakeem, Doctor, Pharmacist, Nurse, Admin).
                </span>
              </div>
              <input
                type="checkbox"
                checked={settings.mfaEnforced}
                onChange={(e) => setSettings({ ...settings, mfaEnforced: e.target.checked })}
                className="mt-1 h-4 w-4 text-[#2D6A4F] rounded border-gray-300"
              />
            </label>

            <div className="flex items-center justify-between">
              <div>
                <span className="font-semibold text-gray-700 block">Session Inactivity Timeout</span>
                <span className="text-xs text-gray-500 block">Automatic logout duration for healthcare workspaces.</span>
              </div>
              <select
                value={settings.sessionTimeoutMinutes}
                onChange={(e) => setSettings({ ...settings, sessionTimeoutMinutes: Number(e.target.value) })}
                className="px-3 py-1.5 border rounded-lg text-xs bg-gray-50 font-medium"
              >
                <option value={15}>15 minutes</option>
                <option value={30}>30 minutes</option>
                <option value={60}>60 minutes (Standard)</option>
                <option value={120}>120 minutes</option>
              </select>
            </div>
          </div>
        </div>

        {/* External Service Connectors */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm space-y-4">
          <h3 className="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2">
            <span>🔌</span> External Integrations & Connectors
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-3 border rounded-xl bg-gray-50 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-gray-800">Stripe Billing Engine</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">Active</span>
              </div>
              <p className="text-[11px] text-gray-500">Card processing, subscription renewals & webhook verification.</p>
            </div>

            <div className="p-3 border rounded-xl bg-gray-50 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-gray-800">SMART on FHIR R4 Client</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">Active</span>
              </div>
              <p className="text-[11px] text-gray-500">Electronic health record & diagnostic lab result sync.</p>
            </div>

            <div className="p-3 border rounded-xl bg-gray-50 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-gray-800">OpenFDA Drug Safety Feed</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">Active</span>
              </div>
              <p className="text-[11px] text-gray-500">Adverse event warnings & modern drug-herb interaction checks.</p>
            </div>

            <div className="p-3 border rounded-xl bg-gray-50 space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-gray-800">QSURA Gateway / Twilio</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-semibold">Active</span>
              </div>
              <p className="text-[11px] text-gray-500">SMS OTP verification and appointment dispatch alerts.</p>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-6 py-2.5 bg-[#2D6A4F] text-white rounded-xl text-sm font-bold hover:bg-[#1B4332] transition shadow-md"
          >
            Save All Platform Settings
          </button>
        </div>
      </form>
    </div>
  );
}
