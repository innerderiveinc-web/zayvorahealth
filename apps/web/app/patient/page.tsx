"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

export default function PatientPortalPage() {
  const [activeTab, setActiveTab] = useState<
    "overview" | "prescriptions" | "lifestyle" | "appointments" | "vitals" | "reports"
  >("overview");

  const [audioLang, setAudioLang] = useState<"urdu" | "hindi" | "english">("urdu");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  // Asbab Sittah Tracker states
  const [asbabScores, setAsbabScores] = useState({
    air: 4, // Clean air / Deep breathing
    diet: 3, // Warm foods / Parhez compliance
    movement: 3, // Gentle walking
    sleep: 4, // 7-8 hours restful sleep
    retention: 4, // Healthy digestion & evacuation
    mental: 5, // Calm, low stress
  });

  const handlePlayPosologyAudio = () => {
    setIsPlayingAudio(true);
    setTimeout(() => {
      setIsPlayingAudio(false);
    }, 4000);
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-5 max-w-6xl mx-auto">
        
        {/* Welcome Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 zv-card p-5 bg-gradient-to-r from-[#0F172A] to-[#1E293B]">
          <div>
            <span className="text-[11px] font-semibold text-[#2DD4BF] uppercase tracking-wider block">Patient Health Portal</span>
            <h1 className="text-xl font-bold text-white tracking-tight mt-0.5">Welcome back, Hamza Farooqi</h1>
            <p className="text-xs text-[#94A3B8] mt-1">
              MRN: <span className="font-mono text-white">MRN-2026-0814</span> • ABHA: <span className="font-mono text-white">91-1234-5678-9012</span> • Primary Mizaj: <span className="text-[#2DD4BF] font-semibold">Balghami</span>
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="zv-badge-emerald px-3 py-1.5 rounded-lg text-xs font-semibold">
              ✓ Active Care Plan
            </span>
          </div>
        </div>

        {/* Executive Health Overview Widgets */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Next Appointment" value="Sep 15" subtext="10:30 AM • OPD Room 3" variant="teal" icon="📅" />
          <StatCard label="Active Medications" value="2" subtext="Majun Suranjan & Roghan" variant="emerald" icon="💊" />
          <StatCard label="Lifestyle Score" value="78%" subtext="Asbab Sittah compliance" variant="blue" icon="🌿" />
          <StatCard label="Last Vitals" value="124/82" subtext="BP normal • Pulse 72" variant="teal" icon="❤️" />
        </div>

        {/* Portal Navigation Tabs */}
        <div className="border-b border-[#334155] flex gap-2">
          {[
            { id: "overview", label: "Health 360", icon: "👤" },
            { id: "prescriptions", label: "My Medicines & Dawa", icon: "💊" },
            { id: "lifestyle", label: "Lifestyle (Asbab Sittah)", icon: "🌿" },
            { id: "appointments", label: "Appointments", icon: "📅" },
            { id: "vitals", label: "Vitals & Progress", icon: "📊" },
            { id: "reports", label: "Lab Reports", icon: "📑" },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold border-b-2 transition ${
                  isActive
                    ? "border-[#0D9488] text-[#2DD4BF] bg-[#0D9488]/10 rounded-t-lg"
                    : "border-transparent text-[#94A3B8] hover:text-white"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* TAB 1: OVERVIEW */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Active Care Summary */}
            <div className="md:col-span-2 space-y-4">
              <div className="zv-card p-4 space-y-3">
                <div className="flex items-center justify-between border-b border-[#334155] pb-2">
                  <h3 className="text-sm font-bold text-white">Active Treatment & Care Plan</h3>
                  <StatusBadge status="Doctor Approved" variant="verified" />
                </div>
                <p className="text-xs text-[#F8FAFC]">
                  <strong>Condition:</strong> Waja-ul-Mafasil Barid Balghami (Knee Osteoarthritis / Joint Phlegmatic Dyscrasia)<br />
                  <strong>Supervising Doctor:</strong> Hakim Dr. Tariq Mansoor (CCIM-BUMS-2004-9841)
                </p>
                <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1.5 text-xs">
                  <span className="text-[11px] font-semibold text-[#2DD4BF] block">Clinical Advice & Tadbeer</span>
                  <p className="text-[#94A3B8]">
                    Apply warm Raughan-e-Balsan locally at bedtime. Avoid exposure to cold breezes and damp rooms. Follow daily morning joint mobility exercises.
                  </p>
                </div>
              </div>

              {/* Vernacular Audio Posology Widget */}
              <div className="zv-card p-4 space-y-3 border-[#0D9488]/40">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">🔊</span>
                    <div>
                      <h4 className="text-xs font-bold text-white">Voice Medication Instructions</h4>
                      <p className="text-[10px] text-[#94A3B8]">Listen to daily dosage advice in your preferred language</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {(["urdu", "hindi", "english"] as const).map((lang) => (
                      <button
                        key={lang}
                        onClick={() => setAudioLang(lang)}
                        className={`text-[11px] px-2 py-1 rounded font-semibold capitalize transition ${
                          audioLang === lang 
                            ? "bg-[#0D9488] text-white" 
                            : "bg-[#1E293B] text-[#94A3B8] hover:text-white"
                        }`}
                      >
                        {lang}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex items-center justify-between">
                  <div className="text-xs text-[#94A3B8]">
                    {audioLang === "urdu" && "Majun Suranjan subah wa sham 5 gram neem garam pani ke sath lein."}
                    {audioLang === "hindi" && "Majun Suranjan subah aur sham 5 gram gungune pani ke sath lein."}
                    {audioLang === "english" && "Take Majun Suranjan 5g twice daily with lukewarm water after meals."}
                  </div>
                  <button
                    onClick={handlePlayPosologyAudio}
                    disabled={isPlayingAudio}
                    className="zv-btn-primary text-xs px-3 py-1.5 bg-[#0D9488]"
                  >
                    {isPlayingAudio ? "▶️ Playing Audio..." : "🔊 Play Voice"}
                  </button>
                </div>
              </div>
            </div>

            {/* Right Column: Next Appointment Card */}
            <div className="space-y-4">
              <div className="zv-card p-4 space-y-3 border-[#0D9488]/40">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-white">Next Clinic Visit</h4>
                  <StatusBadge status="Confirmed" variant="verified" />
                </div>
                <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1 text-xs">
                  <span className="text-[10px] text-[#64748B] block uppercase">Scheduled Date & Time</span>
                  <span className="text-sm font-bold text-white">Sep 15, 2026 • 10:30 AM</span>
                  <p className="text-[11px] text-[#94A3B8]">Central Integrative Clinic • OPD Room 3</p>
                  <p className="text-[11px] text-[#2DD4BF] font-semibold">Queue Token: T-104</p>
                </div>
                <button className="zv-btn-secondary w-full text-xs py-1.5">
                  Reschedule Appointment
                </button>
              </div>

              {/* Emergency Contact */}
              <div className="zv-card p-4 space-y-2 text-xs">
                <span className="text-[10px] text-[#64748B] uppercase block">Emergency Care Desk</span>
                <p className="text-white font-medium">Clinic Hotline: +91-11-2605-9000</p>
                <p className="text-[11px] text-[#94A3B8]">Available 24/7 for urgent clinical support.</p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: PRESCRIPTIONS */}
        {activeTab === "prescriptions" && (
          <div className="zv-card p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-[#334155] pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">Active Prescription: RX-2026-0441</h3>
                <span className="text-[11px] text-[#94A3B8]">Prescribed by Hakim Dr. Tariq Mansoor on Sep 12, 2026</span>
              </div>
              <StatusBadge status="Dispensed & Active" variant="verified" />
            </div>

            <div className="space-y-3">
              <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center text-xs">
                <div>
                  <span className="font-bold text-white">1. Majun Suranjan (Mudabbar / Detoxified)</span>
                  <p className="text-[11px] text-[#94A3B8]">Dose: 5g twice daily after meals with lukewarm water • 14 days</p>
                  <span className="text-[10px] text-[#34D399]">✓ Mudabbar Batch Verified (MS-2026-LOT4)</span>
                </div>
                <span className="zv-badge-teal px-2 py-0.5 rounded text-[10px] font-semibold">Safoof / Majun</span>
              </div>

              <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center text-xs">
                <div>
                  <span className="font-bold text-white">2. Raughan-e-Balsan</span>
                  <p className="text-[11px] text-[#94A3B8]">Application: Local gentle massage over knee joint nocte • 14 days</p>
                </div>
                <span className="zv-badge-teal px-2 py-0.5 rounded text-[10px] font-semibold">Roghan</span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: ASBAB SITTAH LIFESTYLE TRACKER */}
        {activeTab === "lifestyle" && (
          <div className="zv-card p-5 space-y-5">
            <div>
              <h3 className="text-sm font-bold text-white">Asbab Sittah Zaruriyyah (6 Essential Lifestyle Determinants)</h3>
              <p className="text-xs text-[#94A3B8] mt-0.5">
                Classical Unani lifestyle tracking to restore your innate temperament (Mizaj-e-Asli)
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              {[
                { key: "air", name: "1. Hawa-e-Muheet (Ambient Air & Breathing)", desc: "Fresh morning air, avoiding damp cold winds", val: asbabScores.air },
                { key: "diet", name: "2. Makool wa Mashroob (Diet & Hydration)", desc: "Warm soups, avoiding phlegmatic foods", val: asbabScores.diet },
                { key: "movement", name: "3. Harkat wa Sukun Badani (Physical Activity)", desc: "20 min light joint mobilization walking", val: asbabScores.movement },
                { key: "sleep", name: "4. Nawm wa Yaqza (Sleep & Wakefulness)", desc: "7-8 hours restful nocturnal sleep", val: asbabScores.sleep },
                { key: "retention", name: "5. Ihtibas wa Istifragh (Digestion & Elimination)", desc: "Regular bowel habits and toxin evacuation", val: asbabScores.retention },
                { key: "mental", name: "6. Harkat wa Sukun Nafsani (Emotional Balance)", desc: "Stress management and calm mindset", val: asbabScores.mental },
              ].map((item) => (
                <div key={item.key} className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-white">{item.name}</span>
                    <span className="text-[#2DD4BF] font-bold font-mono">{item.val}/5</span>
                  </div>
                  <p className="text-[11px] text-[#94A3B8]">{item.desc}</p>
                  <div className="flex gap-1.5 pt-1">
                    {[1, 2, 3, 4, 5].map((num) => (
                      <button
                        key={num}
                        onClick={() => setAsbabScores({ ...asbabScores, [item.key]: num })}
                        className={`w-7 h-7 rounded text-xs font-semibold transition ${
                          item.val === num
                            ? "bg-[#0D9488] text-white"
                            : "bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]"
                        }`}
                      >
                        {num}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: APPOINTMENTS */}
        {activeTab === "appointments" && (
          <div className="zv-card p-5 space-y-3 text-xs">
            <h3 className="text-sm font-bold text-white">My Clinic Appointments</h3>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center">
              <div>
                <span className="font-bold text-white">Sep 15, 2026 at 10:30 AM</span>
                <p className="text-[#94A3B8]">In-Clinic Consultation • Hakim Dr. Tariq Mansoor</p>
              </div>
              <StatusBadge status="Confirmed" variant="verified" />
            </div>
          </div>
        )}

        {/* TAB 5: VITALS */}
        {activeTab === "vitals" && (
          <div className="zv-card p-5 space-y-3 text-xs">
            <h3 className="text-sm font-bold text-white">Recent Vital Trends</h3>
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                <span className="text-[10px] text-[#64748B] block">Blood Pressure</span>
                <span className="text-base font-bold text-white font-mono">124/82</span>
              </div>
              <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                <span className="text-[10px] text-[#64748B] block">Heart Rate</span>
                <span className="text-base font-bold text-white font-mono">72 bpm</span>
              </div>
              <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                <span className="text-[10px] text-[#64748B] block">Weight</span>
                <span className="text-base font-bold text-white font-mono">78 kg</span>
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: REPORTS */}
        {activeTab === "reports" && (
          <div className="zv-card p-5 space-y-3 text-xs">
            <h3 className="text-sm font-bold text-white">Diagnostic Reports & Imaging</h3>
            <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center">
              <div>
                <span className="font-bold text-white">X-Ray Knee Bilateral (AP/Lateral)</span>
                <p className="text-[#94A3B8]">Sep 02, 2026 • Verified by Radiologist</p>
              </div>
              <button className="zv-btn-secondary py-1 px-3">Download PDF</button>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
