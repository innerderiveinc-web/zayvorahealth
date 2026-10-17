"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

export default function PatientSettingsPage() {
  const [phone, setPhone] = useState("+91-9876543210");
  const [email, setEmail] = useState("hamza.farooqi@example.com");
  const [abhaId, setAbhaId] = useState("91-8271-9920-1490");
  const [smsNotifs, setSmsNotifs] = useState(true);
  const [whatsappNotifs, setWhatsappNotifs] = useState(true);

  const handleSave = () => {
    alert("Profile settings and ABHA preferences saved successfully!");
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">⚙️ Patient Profile & Security Settings</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            Manage your personal credentials, contact details, and national ABHA health ID linkage
          </p>
        </div>

        <div className="bg-[var(--card)] p-6 rounded-2xl border border-[var(--border)] space-y-5">
          <h3 className="font-bold text-white text-base">Personal & Contact Information</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-[var(--text-muted)] font-semibold">Registered Full Name</label>
              <input type="text" value="Hamza Farooqi" disabled className="w-full bg-slate-900 border border-[var(--border)] rounded-xl px-4 py-2.5 text-slate-400 cursor-not-allowed" />
            </div>
            <div className="space-y-1.5">
              <label className="text-[var(--text-muted)] font-semibold">Medical Record Number (MRN)</label>
              <input type="text" value="MRN-2026-0814" disabled className="w-full bg-slate-900 border border-[var(--border)] rounded-xl px-4 py-2.5 text-slate-400 font-mono cursor-not-allowed" />
            </div>
            <div className="space-y-1.5">
              <label className="text-[var(--text-muted)] font-semibold">Primary Phone Number</label>
              <input type="text" value={phone} onChange={e => setPhone(e.target.value)} className="w-full bg-slate-800 border border-[var(--border)] rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div className="space-y-1.5">
              <label className="text-[var(--text-muted)] font-semibold">Email Address</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-slate-800 border border-[var(--border)] rounded-xl px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            </div>
            <div className="space-y-1.5 md:col-span-2">
              <label className="text-[var(--text-muted)] font-semibold">Ayushman Bharat Health Account (ABHA ID)</label>
              <input type="text" value={abhaId} onChange={e => setAbhaId(e.target.value)} className="w-full bg-slate-800 border border-[var(--border)] rounded-xl px-4 py-2.5 text-emerald-400 font-mono focus:outline-none focus:ring-2 focus:ring-emerald-500" />
            </div>
          </div>

          <div className="pt-4 border-t border-[var(--border)] space-y-3">
            <h4 className="font-bold text-white text-sm">Communication Channels</h4>
            <div className="flex items-center justify-between text-xs py-2">
              <span className="text-slate-300">Receive SMS Prescription & Token Alerts</span>
              <input type="checkbox" checked={smsNotifs} onChange={e => setSmsNotifs(e.target.checked)} className="w-4 h-4 accent-emerald-500" />
            </div>
            <div className="flex items-center justify-between text-xs py-2">
              <span className="text-slate-300">Receive WhatsApp Audio Posology & Diet Plans (via QSURA)</span>
              <input type="checkbox" checked={whatsappNotifs} onChange={e => setWhatsappNotifs(e.target.checked)} className="w-4 h-4 accent-emerald-500" />
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              onClick={handleSave}
              className="px-6 py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-bold text-xs rounded-xl shadow transition"
            >
              Save Preferences
            </button>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
