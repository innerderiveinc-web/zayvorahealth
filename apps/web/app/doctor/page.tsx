"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { NuskhaBuilder } from "@/components/NuskhaBuilder";
import { HakeemReviewDrawer } from "@/components/HakeemReviewDrawer";
import type { PatientRecord } from "@/lib/clinicalApi";

const DEFAULT_PATIENT: PatientRecord = {
  id: "PAT-774901",
  first_name: "Hamza",
  last_name: "Farooqi",
  date_of_birth: "1984-06-15",
  gender: "male",
  contact_phone: "+91-9876543210",
  contact_email: "hamza.farooqi@example.com",
  blood_group: "B+",
  mizaj_dominant: "Balghami (Cold & Moist)",
  allergies: ["Sonf (Foeniculum vulgare)"],
};

export default function DoctorWorkspacePage() {
  const [activeTab, setActiveTab] = useState<
    | "overview"
    | "history"
    | "examination"
    | "vitals"
    | "investigations"
    | "diagnosis"
    | "mizaj"
    | "axis"
    | "treatment"
    | "prescription"
    | "followup"
    | "timeline"
    | "documents"
  >("overview");

  const [aiDrawerOpen, setAiDrawerOpen] = useState(false);
  const [activePatient] = useState<PatientRecord>(DEFAULT_PATIENT);
  const [chiefComplaint, setChiefComplaint] = useState(
    "Bilateral knee pain and morning stiffness, aggravating in cold and damp weather. Relieved by warm fomentation."
  );
  const [examNotes, setExamNotes] = useState(
    "Nabz: Bat'ee (Slow), Layyin (Soft), Munkafish. Lisan: Rutubat-e-Ghaliba, whitish coating. Joints: Mild crepitus in bilateral patellofemoral joints, no acute erythema."
  );
  const [vitals, setVitals] = useState({
    bp: "124/82",
    pulse: "72",
    temp: "98.4",
    weight: "78",
    spo2: "98",
  });
  const [isLocked, setIsLocked] = useState(false);
  const [signatureHash, setSignatureHash] = useState<string | null>(null);

  const handleSignEncounter = () => {
    const mockHash = "731f5cf53472" + Math.random().toString(36).substring(2, 10);
    setSignatureHash(mockHash);
    setIsLocked(true);
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-5 max-w-7xl mx-auto">
        
        {/* ============================================================= */}
        {/* 1. 8-WIDGET DOCTOR OVERVIEW PANEL */}
        {/* ============================================================= */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-lg font-bold text-white tracking-tight">Clinical Consultation Cockpit</h1>
              <p className="text-xs text-[#94A3B8]">
                Hakim Dr. Tariq Mansoor • CCIM-BUMS-2004-9841 • OPD Room 3
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setAiDrawerOpen(true)}
                className="zv-btn-secondary text-xs border-[#0D9488]/40 text-[#2DD4BF] hover:bg-[#0D9488]/20"
              >
                🤖 Hakeem Sahab AI Copilot
              </button>
              {isLocked ? (
                <span className="zv-badge-emerald px-3 py-1 text-xs rounded-lg font-semibold flex items-center gap-1.5">
                  ✓ 21 CFR Part 11 Locked
                </span>
              ) : (
                <button
                  onClick={handleSignEncounter}
                  className="zv-btn-primary text-xs bg-[#0D9488] hover:bg-[#14B8A6]"
                >
                  🔒 Sign & Lock Encounter
                </button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2.5">
            <StatCard label="Today's Appts" value="14" subtext="3 Completed" variant="teal" icon="📅" />
            <StatCard label="Waiting Queue" value="3" subtext="Next: T-105" variant="amber" icon="⏳" />
            <StatCard label="Active Consult" value="T-104" subtext="Hamza Farooqi" variant="emerald" icon="🩺" />
            <StatCard label="Pending Notes" value="2" subtext="Draft state" variant="blue" icon="📝" />
            <StatCard label="Draft Rx" value="1" subtext="Awaiting lock" variant="rose" icon="💊" />
            <StatCard label="Follow-ups" value="4" subtext="Due this week" variant="purple" icon="🔄" />
            <StatCard label="Safety Alerts" value="1" subtext="Mudabbar Req." variant="amber" icon="⚠️" />
            <StatCard label="Recent Vitals" value="Normal" subtext="BP 124/82" variant="teal" icon="📊" />
          </div>
        </div>

        {/* ============================================================= */}
        {/* 2. MAIN CONSULTATION WORKSPACE (LEFT CONTEXT + CENTER TABS) */}
        {/* ============================================================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
          
          {/* LEFT CONTEXT PANEL (3 Columns) */}
          <div className="lg:col-span-3 space-y-4">
            {/* Active Patient Card */}
            <div className="zv-card p-4 space-y-3">
              <div className="flex items-center justify-between border-b border-[#334155] pb-2.5">
                <div className="flex items-center gap-2.5">
                  <div className="w-10 h-10 rounded-full bg-[#1E293B] border border-[#334155] flex items-center justify-center font-bold text-white text-sm">
                    HF
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">
                      {activePatient.first_name} {activePatient.last_name}
                    </h3>
                    <span className="text-[11px] text-[#94A3B8] font-mono">MRN-2026-0814</span>
                  </div>
                </div>
                <StatusBadge status="In Consult" variant="verified" pulse />
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-[#64748B] block text-[10px] uppercase">Age / Gender</span>
                  <span className="text-white font-medium">42y • Male</span>
                </div>
                <div>
                  <span className="text-[#64748B] block text-[10px] uppercase">Blood Group</span>
                  <span className="text-white font-medium">B+ Positive</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-[#0A0F1D] border border-[#334155] space-y-1">
                <span className="text-[10px] text-[#64748B] uppercase block">Primary Mizaj</span>
                <span className="text-xs font-semibold text-[#2DD4BF] flex items-center gap-1">
                  ❄️ {activePatient.mizaj_dominant}
                </span>
                <p className="text-[10px] text-[#94A3B8]">Organ Axis: Mafasil-Asab (Joint-Nerve)</p>
              </div>

              <div className="space-y-1">
                <span className="text-[10px] text-[#EF4444] font-semibold uppercase block">Allergies & Contraindications</span>
                <div className="flex flex-wrap gap-1">
                  {activePatient.allergies.map((allergy) => (
                    <span key={allergy} className="text-[11px] px-2 py-0.5 rounded bg-[#EF4444]/15 text-[#FB7185] border border-[#EF4444]/30">
                      ⚠️ {allergy}
                    </span>
                  ))}
                </div>
              </div>

              <div className="border-t border-[#334155] pt-2 space-y-1 text-xs text-[#94A3B8]">
                <div className="flex justify-between">
                  <span>Contact:</span>
                  <span className="text-white">{activePatient.contact_phone}</span>
                </div>
                <div className="flex justify-between">
                  <span>ABHA ID:</span>
                  <span className="text-white font-mono">91-1234-5678-9012</span>
                </div>
              </div>
            </div>

            {/* Quick Vitals Recorder */}
            <div className="zv-card p-4 space-y-3">
              <h4 className="text-xs font-semibold text-white uppercase tracking-wider">Clinical Vitals</h4>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <label className="text-[10px] text-[#64748B]">BP (mmHg)</label>
                  <input
                    type="text"
                    value={vitals.bp}
                    onChange={(e) => setVitals({ ...vitals, bp: e.target.value })}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">Pulse (bpm)</label>
                  <input
                    type="text"
                    value={vitals.pulse}
                    onChange={(e) => setVitals({ ...vitals, pulse: e.target.value })}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">Weight (kg)</label>
                  <input
                    type="text"
                    value={vitals.weight}
                    onChange={(e) => setVitals({ ...vitals, weight: e.target.value })}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-[#64748B]">SpO2 (%)</label>
                  <input
                    type="text"
                    value={vitals.spo2}
                    onChange={(e) => setVitals({ ...vitals, spo2: e.target.value })}
                    disabled={isLocked}
                    className="zv-input mt-0.5 font-mono text-xs"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* CENTER DOCUMENTATION SEQUENCE: 13 TABS (9 Columns) */}
          <div className="lg:col-span-9 zv-card flex flex-col min-h-[680px]">
            
            {/* 13-Tab Navigation Header */}
            <div className="border-b border-[#334155] bg-[#0F172A] rounded-t-xl px-2 pt-2 flex items-center gap-1 overflow-x-auto">
              {[
                { id: "overview", label: "1. Overview" },
                { id: "history", label: "2. History" },
                { id: "examination", label: "3. Examination" },
                { id: "vitals", label: "4. Vitals" },
                { id: "investigations", label: "5. Investigations" },
                { id: "diagnosis", label: "6. Diagnosis" },
                { id: "mizaj", label: "7. Mizaj" },
                { id: "axis", label: "8. Axis Mapping" },
                { id: "treatment", label: "9. Treatment Plan" },
                { id: "prescription", label: "10. Prescription" },
                { id: "followup", label: "11. Follow-up" },
                { id: "timeline", label: "12. Timeline" },
                { id: "documents", label: "13. Documents" },
              ].map((tab) => {
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`px-3 py-2 text-xs font-semibold whitespace-nowrap border-b-2 transition ${
                      isActive
                        ? "border-[#0D9488] text-[#2DD4BF] bg-[#0D9488]/10 rounded-t-md"
                        : "border-transparent text-[#94A3B8] hover:text-white hover:bg-[#1E293B]"
                    }`}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>

            {/* Tab Body Content */}
            <div className="p-5 flex-1 overflow-y-auto">
              {/* TAB 1: OVERVIEW */}
              {activeTab === "overview" && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-white">Consultation Overview & Chief Complaint</h3>
                    <StatusBadge status="Encounter In Progress" variant="verified" />
                  </div>
                  <div>
                    <label className="text-xs text-[#94A3B8] block mb-1">Chief Complaint (Shikayat-e-Awwal)</label>
                    <textarea
                      rows={3}
                      value={chiefComplaint}
                      onChange={(e) => setChiefComplaint(e.target.value)}
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <h4 className="text-xs font-semibold text-[#2DD4BF]">Integrated Diagnostic Assessment</h4>
                    <p className="text-xs text-[#F8FAFC]">
                      <strong>Unani Diagnosis:</strong> Waja-ul-Mafasil Barid Balghami (Knee Osteoarthritis / Joint Phlegmatic Dyscrasia)<br />
                      <strong>Biomedical Mapping:</strong> ICD-10 M17.9 (Bilateral Primary Knee Osteoarthritis)
                    </p>
                  </div>
                  {isLocked && signatureHash && (
                    <div className="p-3 bg-[#10B981]/10 border border-[#10B981]/30 rounded-lg text-xs space-y-1">
                      <div className="flex items-center gap-2 text-[#34D399] font-bold">
                        <span>✓ 21 CFR Part 11 Cryptographically Sealed</span>
                      </div>
                      <p className="text-[11px] text-[#94A3B8] font-mono">Signature Hash: {signatureHash}</p>
                      <p className="text-[10px] text-[#64748B]">Signer: Hakim Dr. Tariq Mansoor (CCIM-BUMS-2004-9841)</p>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: HISTORY */}
              {activeTab === "history" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Clinical History (Tarikh-e-Marz)</h3>
                  <div>
                    <label className="text-[#94A3B8] block mb-1">History of Present Illness (HPI)</label>
                    <textarea
                      rows={4}
                      defaultValue="Patient reports 14-month history of progressive bilateral knee stiffness and dull aching pain. Symptoms worsen during cold weather and early morning. Associated with mild pedal edema after prolonged standing."
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-[#94A3B8] block mb-1">Past Medical History</label>
                      <input type="text" defaultValue="Mild Dyspepsia (Su-e-Hazm), Hypertension (Controlled)" disabled={isLocked} className="zv-input text-xs" />
                    </div>
                    <div>
                      <label className="text-[#94A3B8] block mb-1">Family History</label>
                      <input type="text" defaultValue="Maternal history of joint arthralgia" disabled={isLocked} className="zv-input text-xs" />
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 3: EXAMINATION */}
              {activeTab === "examination" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Physical & Classical Unani Examination</h3>
                  <div>
                    <label className="text-[#94A3B8] block mb-1">Pulse (Nabz), Tongue (Lisan), & Musculoskeletal Signs</label>
                    <textarea
                      rows={4}
                      value={examNotes}
                      onChange={(e) => setExamNotes(e.target.value)}
                      disabled={isLocked}
                      className="zv-input text-xs"
                    />
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Nabz (Pulse)</span>
                      <span className="text-xs font-semibold text-white">Bat'ee, Layyin, Munkafish</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Lisan (Tongue)</span>
                      <span className="text-xs font-semibold text-white">Pale, moist, white coating</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] uppercase block">Baul & Baraz</span>
                      <span className="text-xs font-semibold text-white">Qarura: Abyad (Pale), normal clarity</span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: VITALS */}
              {activeTab === "vitals" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Longitudinal Vitals & Biometrics</h3>
                  <div className="grid grid-cols-4 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Blood Pressure</span>
                      <span className="text-sm font-bold text-white font-mono">124/82 mmHg</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Pulse Rate</span>
                      <span className="text-sm font-bold text-white font-mono">72 bpm</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Body Temperature</span>
                      <span className="text-sm font-bold text-white font-mono">98.4 °F</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">SpO2</span>
                      <span className="text-sm font-bold text-white font-mono">98% Room Air</span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 5: INVESTIGATIONS */}
              {activeTab === "investigations" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Diagnostic Investigations & Laboratory</h3>
                  <div className="zv-card p-3 space-y-2 border-[#334155]">
                    <div className="flex justify-between items-center text-xs font-semibold">
                      <span>X-Ray Bilateral Knees (AP/Lateral)</span>
                      <span className="text-[#2DD4BF]">Completed (2026-09-02)</span>
                    </div>
                    <p className="text-[11px] text-[#94A3B8]">
                      Findings: Moderate joint space narrowing of medial compartment with subchondral sclerosis. Kellgren-Lawrence Grade II.
                    </p>
                  </div>
                  <div className="zv-card p-3 space-y-2 border-[#334155]">
                    <div className="flex justify-between items-center text-xs font-semibold">
                      <span>Serum Uric Acid & ESR</span>
                      <span className="text-[#34D399]">Normal Limits</span>
                    </div>
                    <p className="text-[11px] text-[#94A3B8]">
                      Uric acid: 5.4 mg/dL (Normal). ESR: 18 mm/hr (Mildly elevated).
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 6: DIAGNOSIS */}
              {activeTab === "diagnosis" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Differential & Confirmed Clinical Diagnosis</h3>
                  <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#0D9488]/40 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-[#2DD4BF]">PRIMARY DIAGNOSIS: CONFIRMED</span>
                      <StatusBadge status="Evidence Grade A" variant="verified" />
                    </div>
                    <p className="text-sm text-white font-medium">
                      Waja-ul-Mafasil Barid Balghami (Phlegmatic Cold Knee Osteoarthritis)
                    </p>
                    <p className="text-xs text-[#94A3B8]">
                      ICD-10 Code: <strong>M17.9</strong> • SNOMED CT: <strong>399269003</strong>
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 7: MIZAJ ASSESSMENT */}
              {activeTab === "mizaj" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">10-Ajnas Quantitative Mizaj Engine</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Balgham (Phlegm)</span>
                      <span className="text-sm font-bold text-[#2DD4BF] font-mono">65% Dominant</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Dam (Blood)</span>
                      <span className="text-sm font-bold text-white font-mono">20% Secondary</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Safra (Yellow Bile)</span>
                      <span className="text-sm font-bold text-white font-mono">10% Low</span>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155]">
                      <span className="text-[10px] text-[#64748B] block">Sauda (Black Bile)</span>
                      <span className="text-sm font-bold text-white font-mono">5% Low</span>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 8: AXIS MAPPING */}
              {activeTab === "axis" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Organ-Axis Functional Cross-Talk</h3>
                  <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <h4 className="text-xs font-semibold text-[#2DD4BF]">Primary Axis: Mafasil-Asab (Joint-Nerve Axis)</h4>
                    <p className="text-xs text-[#94A3B8]">
                      Phlegmatic accumulation (Burudat wa Rutubat) in synovial bursae causing localized neurovascular slowing and mechanical friction.
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 9: TREATMENT PLAN */}
              {activeTab === "treatment" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Multi-Horizon Integrative Care Plan</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
                      <h4 className="text-xs font-semibold text-[#34D399]">Ilaj bit-Tadbeer (Regimenal Therapy)</h4>
                      <p className="text-[11px] text-[#94A3B8]">
                        1. Dalak Layyin (Gentle massage) with Raughan-e-Balsan nocte.<br />
                        2. Natool (Warm herbal irrigation) with decoction of Babuna twice weekly.
                      </p>
                    </div>
                    <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-1">
                      <h4 className="text-xs font-semibold text-[#2DD4BF]">Ilaj bil-Ghiza (Dietary Prescription)</h4>
                      <p className="text-[11px] text-[#94A3B8]">
                        Avoid cold and mucus-generating foods (yogurt, cucumber, iced beverages). Incorporate warm ginger, cinnamon, and sheep bone broth.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 10: PRESCRIPTION & NUSKHA BUILDER */}
              {activeTab === "prescription" && (
                <div className="space-y-4">
                  <NuskhaBuilder
                    token="SESSION_MOCK_TOKEN"
                    patient={activePatient}
                    encounterId="ENC-2026-0814"
                  />
                </div>
              )}

              {/* TAB 11: FOLLOW-UP */}
              {activeTab === "followup" && (
                <div className="space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Follow-up Consultation & Warning Red Flags</h3>
                  <div className="p-3 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2">
                    <span className="text-xs font-semibold text-white">Scheduled Review: Day +14 (2026-09-29)</span>
                    <p className="text-xs text-[#94A3B8]">
                      Evaluate VAS pain score reduction, knee flexion degrees, and check for any botanical gastric intolerance.
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 12: TIMELINE */}
              {activeTab === "timeline" && (
                <div className="space-y-3 text-xs">
                  <h3 className="text-sm font-bold text-white">Longitudinal Clinical Encounters</h3>
                  <div className="border-l-2 border-[#0D9488] pl-4 space-y-3">
                    <div>
                      <span className="text-[10px] text-[#64748B]">2026-09-12 (Today)</span>
                      <p className="text-xs font-semibold text-white">Integrative OPD Consultation • Hakim Dr. Tariq Mansoor</p>
                    </div>
                    <div>
                      <span className="text-[10px] text-[#64748B]">2026-09-02</span>
                      <p className="text-xs font-semibold text-white">Radiology: X-Ray Knee Bilateral • Dr. K. Saxena</p>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 13: DOCUMENTS */}
              {activeTab === "documents" && (
                <div className="space-y-3 text-xs">
                  <h3 className="text-sm font-bold text-white">Attached Clinical Documents & Reports</h3>
                  <div className="zv-card p-3 flex justify-between items-center border-[#334155]">
                    <div>
                      <span className="text-xs font-semibold text-white">X-Ray Knee Scan Report.pdf</span>
                      <span className="text-[10px] text-[#64748B] block">Uploaded 2026-09-02 • 1.4 MB</span>
                    </div>
                    <button className="zv-btn-secondary text-xs py-1 px-2.5">View PDF</button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* HAKEEM SAHAB AI REVIEW DRAWER */}
        <HakeemReviewDrawer
          token="SESSION_MOCK_TOKEN"
          patient={activePatient}
          isOpen={aiDrawerOpen}
          onClose={() => setAiDrawerOpen(false)}
        />
      </div>
    </AppShell>
  );
}
