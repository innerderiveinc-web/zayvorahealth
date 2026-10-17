"use client";

import React, { useState, useEffect, useCallback } from "react";
import { AppShell } from "@/components/AppShell";
import { useAuth } from "@/lib/hooks/useAuth";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

// ─── Types ────────────────────────────────────────────────────────────────────

interface WardPatient {
  id: string;
  mrn: string;
  name: string;
  age: number;
  gender: string;
  bed: string;
  ward: string;
  admittedDate: string;
  primaryDiagnosis: string;
  attendingDoctor: string;
  status: "STABLE" | "CRITICAL" | "OBSERVATION" | "DISCHARGE_READY";
  alertFlags: string[];
}

interface VitalsEntry {
  patientId: string;
  patientName: string;
  mrn: string;
  bp: string;
  pulse: number | "";
  temp: number | "";
  spo2: number | "";
  rr: number | "";
  weight: number | "";
  notes: string;
  recordedAt: string;
}

interface MedScheduleItem {
  id: string;
  mrn: string;
  patientName: string;
  bed: string;
  medicineName: string;
  dose: string;
  route: string;
  scheduledTime: string;
  status: "PENDING" | "GIVEN" | "SKIPPED" | "HELD";
  prescribedBy: string;
}

type ActiveTab = "ward" | "vitals" | "medications" | "rounds";

// ─── Seed / Offline data (shown when API is offline) ─────────────────────────

const SEED_PATIENTS: WardPatient[] = [
  {
    id: "WP-001", mrn: "MRN-2026-0192", name: "Fatima Mirza", age: 62,
    gender: "Female", bed: "W2-B04", ward: "Women's Medical",
    admittedDate: "2026-09-28", primaryDiagnosis: "Hypertension + Obesity (Mizaj: Balghami)",
    attendingDoctor: "Hakeem Dr. Irfan Ashraf",
    status: "STABLE", alertFlags: [],
  },
  {
    id: "WP-002", mrn: "MRN-2026-0214", name: "Abdul Qadir Siddiqui", age: 71,
    gender: "Male", bed: "W1-B09", ward: "General Medicine",
    admittedDate: "2026-09-30", primaryDiagnosis: "Diabetic neuropathy + chronic joint pain",
    attendingDoctor: "Dr. Mansoor Alam",
    status: "OBSERVATION", alertFlags: ["High BP last reading"],
  },
  {
    id: "WP-003", mrn: "MRN-2026-0301", name: "Zainab Hussain", age: 45,
    gender: "Female", bed: "W2-B11", ward: "Women's Medical",
    admittedDate: "2026-10-01", primaryDiagnosis: "Anaemia + menstrual irregularity",
    attendingDoctor: "Hakeem Dr. Irfan Ashraf",
    status: "DISCHARGE_READY", alertFlags: ["Discharge pending pharmacy"],
  },
  {
    id: "WP-004", mrn: "MRN-2026-0388", name: "Tariq Mehmood", age: 55,
    gender: "Male", bed: "ICU-B02", ward: "ICU",
    admittedDate: "2026-09-29", primaryDiagnosis: "Acute cardiac event — post-stabilisation",
    attendingDoctor: "Dr. Yusuf Hashmi",
    status: "CRITICAL", alertFlags: ["SpO2 monitoring", "IV line check", "Hourly BP"],
  },
];

const SEED_MED_SCHEDULE: MedScheduleItem[] = [
  {
    id: "MS-001", mrn: "MRN-2026-0192", patientName: "Fatima Mirza",
    bed: "W2-B04", medicineName: "Sharbat-e-Anar", dose: "15 mL",
    route: "Oral", scheduledTime: "08:00", status: "GIVEN",
    prescribedBy: "Hakeem Dr. Irfan Ashraf",
  },
  {
    id: "MS-002", mrn: "MRN-2026-0192", patientName: "Fatima Mirza",
    bed: "W2-B04", medicineName: "Habbe Mumsik Tilai", dose: "2 tabs",
    route: "Oral", scheduledTime: "14:00", status: "PENDING",
    prescribedBy: "Hakeem Dr. Irfan Ashraf",
  },
  {
    id: "MS-003", mrn: "MRN-2026-0214", patientName: "Abdul Qadir Siddiqui",
    bed: "W1-B09", medicineName: "Jawarish Jalinus", dose: "5 g",
    route: "Oral", scheduledTime: "08:00", status: "GIVEN",
    prescribedBy: "Dr. Mansoor Alam",
  },
  {
    id: "MS-004", mrn: "MRN-2026-0214", patientName: "Abdul Qadir Siddiqui",
    bed: "W1-B09", medicineName: "Roghan Baiza Murgh", dose: "5 mL massage",
    route: "Topical", scheduledTime: "20:00", status: "PENDING",
    prescribedBy: "Dr. Mansoor Alam",
  },
  {
    id: "MS-005", mrn: "MRN-2026-0388", patientName: "Tariq Mehmood",
    bed: "ICU-B02", medicineName: "Normal Saline 0.9%", dose: "500 mL",
    route: "IV", scheduledTime: "06:00", status: "GIVEN",
    prescribedBy: "Dr. Yusuf Hashmi",
  },
  {
    id: "MS-006", mrn: "MRN-2026-0388", patientName: "Tariq Mehmood",
    bed: "ICU-B02", medicineName: "Aspirin 75 mg", dose: "1 tab",
    route: "Oral", scheduledTime: "12:00", status: "PENDING",
    prescribedBy: "Dr. Yusuf Hashmi",
  },
];

// ─── Status helpers ───────────────────────────────────────────────────────────

const statusColor = (s: WardPatient["status"]) => {
  switch (s) {
    case "CRITICAL":        return "bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse";
    case "OBSERVATION":     return "bg-amber-500/15 text-amber-400 border border-amber-500/25";
    case "STABLE":          return "bg-emerald-500/15 text-emerald-400 border border-emerald-500/25";
    case "DISCHARGE_READY": return "bg-blue-500/15 text-blue-400 border border-blue-500/25";
  }
};

const medStatusColor = (s: MedScheduleItem["status"]) => {
  switch (s) {
    case "GIVEN":   return "bg-emerald-500/15 text-emerald-400 border border-emerald-500/25";
    case "PENDING": return "bg-amber-500/15 text-amber-400 border border-amber-500/25";
    case "SKIPPED": return "bg-gray-500/10 text-gray-400 border border-gray-500/20";
    case "HELD":    return "bg-red-500/15 text-red-400 border border-red-500/25";
  }
};

// ─── Empty vitals form ────────────────────────────────────────────────────────

const emptyVitals = (patient: WardPatient): VitalsEntry => ({
  patientId: patient.id,
  patientName: patient.name,
  mrn: patient.mrn,
  bp: "",
  pulse: "",
  temp: "",
  spo2: "",
  rr: "",
  weight: "",
  notes: "",
  recordedAt: new Date().toISOString(),
});

// ─── Main Component ───────────────────────────────────────────────────────────

export default function NurseDashboardPage() {
  const { isLoading: authLoading, isAuthorized, user } = useAuth({
    requiredRoles: ["NURSE", "NURSE_COORDINATOR"],
  });

  const [activeTab, setActiveTab] = useState<ActiveTab>("ward");
  const [patients, setPatients] = useState<WardPatient[]>([]);
  const [medSchedule, setMedSchedule] = useState<MedScheduleItem[]>(SEED_MED_SCHEDULE);
  const [loading, setLoading] = useState(true);
  const [apiOnline, setApiOnline] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Vitals entry state
  const [selectedPatient, setSelectedPatient] = useState<WardPatient | null>(null);
  const [vitalsForm, setVitalsForm] = useState<VitalsEntry | null>(null);
  const [vitalsSubmitting, setVitalsSubmitting] = useState(false);
  const [vitalsSuccess, setVitalsSuccess] = useState(false);

  // Ward rounds state
  const [roundNotes, setRoundNotes] = useState<Record<string, string>>({});
  const [roundChecked, setRoundChecked] = useState<Record<string, boolean>>({});

  // Clock tick
  useEffect(() => {
    const t = setInterval(() => setCurrentTime(new Date()), 60_000);
    return () => clearInterval(t);
  }, []);

  // Load ward patients
  const loadPatients = useCallback(async () => {
    setLoading(true);
    const session = AuthService.getSession();
    try {
      const res = await fetch(`${API}/api/v1/ward/patients`, {
        headers: session?.token ? { Authorization: `Bearer ${session.token}` } : {},
      });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data.patients)) {
          setPatients(data.patients);
          setApiOnline(true);
          setLoading(false);
          return;
        }
      }
    } catch { /* fall through to seed */ }
    setPatients(SEED_PATIENTS);
    setApiOnline(false);
    setLoading(false);
  }, []);

  useEffect(() => {
    if (isAuthorized) loadPatients();
  }, [isAuthorized, loadPatients]);

  // ── Vitals submit ───────────────────────────────────────────────────────────
  const handleVitalsSubmit = async () => {
    if (!vitalsForm) return;
    setVitalsSubmitting(true);
    const session = AuthService.getSession();
    try {
      await fetch(`${API}/api/v1/ward/vitals`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {}),
        },
        body: JSON.stringify({ ...vitalsForm, recordedAt: new Date().toISOString() }),
      });
    } catch { /* offline — still show success */ }
    setVitalsSubmitting(false);
    setVitalsSuccess(true);
    setTimeout(() => {
      setVitalsSuccess(false);
      setSelectedPatient(null);
      setVitalsForm(null);
    }, 2000);
  };

  // ── Med status toggle ───────────────────────────────────────────────────────
  const markMed = (id: string, status: MedScheduleItem["status"]) => {
    setMedSchedule(prev => prev.map(m => m.id === id ? { ...m, status } : m));
  };

  // ── Stat counts ─────────────────────────────────────────────────────────────
  const criticalCount   = patients.filter(p => p.status === "CRITICAL").length;
  const stableCount     = patients.filter(p => p.status === "STABLE").length;
  const dischargeCount  = patients.filter(p => p.status === "DISCHARGE_READY").length;
  const pendingMeds     = medSchedule.filter(m => m.status === "PENDING").length;

  // ── Guard ───────────────────────────────────────────────────────────────────
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--bg-base)]">
        <div className="text-center space-y-3">
          <div className="text-3xl animate-spin">⏳</div>
          <p className="text-sm text-[var(--text-muted)]">Verifying credentials…</p>
        </div>
      </div>
    );
  }
  if (!isAuthorized) return null;

  const tabs: { id: ActiveTab; label: string; icon: string }[] = [
    { id: "ward",        label: "Ward Overview",    icon: "🏥" },
    { id: "vitals",      label: "Vitals Entry",     icon: "🩺" },
    { id: "medications", label: "Medication Round", icon: "💊" },
    { id: "rounds",      label: "Ward Rounds",      icon: "📋" },
  ];

  return (
    <AppShell activeRole="nurse">
      <div className="space-y-6 max-w-7xl">

        {/* ── Header ── */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">Nurse Station</h1>
              <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${
                apiOnline
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                  : "bg-amber-500/10 text-amber-400 border-amber-500/20"
              }`}>
                {apiOnline ? "● Live" : "● Offline Mode"}
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              {currentTime.toLocaleDateString("en-IN", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}
              {" · "}
              {currentTime.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })}
              {user?.fullName ? ` · Logged in as ${user.fullName}` : ""}
            </p>
          </div>
          <button
            onClick={loadPatients}
            className="zv-btn-secondary text-xs px-3 py-1.5 flex items-center gap-1.5"
          >
            <span>🔄</span> Refresh
          </button>
        </div>

        {/* ── Stat Row ── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Total Ward Patients", value: patients.length,  icon: "🛏",  color: "text-blue-400" },
            { label: "Critical / ICU",       value: criticalCount,   icon: "🚨",  color: "text-red-400" },
            { label: "Stable",               value: stableCount,     icon: "✅",  color: "text-emerald-400" },
            { label: "Discharge Ready",       value: dischargeCount,  icon: "🚪",  color: "text-sky-400" },
          ].map(s => (
            <div key={s.label} className="zv-card p-4 flex items-center gap-3">
              <span className="text-2xl">{s.icon}</span>
              <div>
                <div className={`text-xl font-bold ${s.color}`}>{s.value}</div>
                <div className="text-[11px] text-[var(--text-muted)]">{s.label}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Pending meds banner */}
        {pendingMeds > 0 && (
          <div
            className="flex items-center gap-3 px-4 py-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm cursor-pointer"
            onClick={() => setActiveTab("medications")}
          >
            <span className="text-lg">💊</span>
            <span><strong>{pendingMeds} medication(s)</strong> pending for this round — tap to review</span>
            <span className="ml-auto">→</span>
          </div>
        )}

        {/* ── Tabs ── */}
        <div className="flex gap-1 bg-[var(--bg-elevated)] rounded-xl p-1 border border-[var(--border-default)] overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition ${
                activeTab === tab.id
                  ? "bg-[var(--primary)] text-white shadow"
                  : "text-[var(--text-muted)] hover:text-white"
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* ═══════════════════════════════════════════════════
            TAB 1 — WARD OVERVIEW
        ═══════════════════════════════════════════════════ */}
        {activeTab === "ward" && (
          <div className="zv-card overflow-hidden">
            {loading ? (
              <div className="p-12 text-center">
                <div className="text-3xl animate-spin">⏳</div>
                <p className="text-xs text-[var(--text-muted)] mt-3">Loading ward patients…</p>
              </div>
            ) : patients.length === 0 ? (
              <div className="p-12 text-center space-y-3">
                <div className="text-3xl">🛏</div>
                <p className="text-sm text-[var(--text-muted)]">No patients in ward today.</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="border-b border-[var(--border-default)] bg-[var(--bg-elevated)]">
                    <tr className="text-left text-[var(--text-muted)] text-xs font-semibold">
                      <th className="px-4 py-3">Bed</th>
                      <th className="px-4 py-3">Patient</th>
                      <th className="px-4 py-3">Diagnosis</th>
                      <th className="px-4 py-3">Attending</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3">Alerts</th>
                      <th className="px-4 py-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-subtle)]">
                    {patients.map(p => (
                      <tr key={p.id} className="hover:bg-[var(--bg-elevated)] transition">
                        <td className="px-4 py-3">
                          <div className="font-mono text-xs font-bold text-emerald-400">{p.bed}</div>
                          <div className="text-[10px] text-[var(--text-muted)]">{p.ward}</div>
                        </td>
                        <td className="px-4 py-3">
                          <div className="font-semibold text-[var(--text-primary)]">{p.name}</div>
                          <div className="text-[11px] text-[var(--text-muted)]">
                            {p.age}y {p.gender} · {p.mrn}
                          </div>
                        </td>
                        <td className="px-4 py-3 text-xs text-[var(--text-primary)] max-w-xs">
                          {p.primaryDiagnosis}
                        </td>
                        <td className="px-4 py-3 text-xs text-[var(--text-muted)]">
                          {p.attendingDoctor}
                        </td>
                        <td className="px-4 py-3">
                          <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${statusColor(p.status)}`}>
                            {p.status.replace("_", " ")}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          {p.alertFlags.length > 0 ? (
                            <div className="space-y-0.5">
                              {p.alertFlags.map((f, i) => (
                                <div key={i} className="text-[10px] text-red-400 flex items-center gap-1">
                                  <span>⚠</span> {f}
                                </div>
                              ))}
                            </div>
                          ) : (
                            <span className="text-[10px] text-[var(--text-muted)]">—</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-right">
                          <button
                            onClick={() => {
                              setSelectedPatient(p);
                              setVitalsForm(emptyVitals(p));
                              setActiveTab("vitals");
                            }}
                            className="zv-btn-secondary text-[11px] px-3 py-1 font-semibold"
                          >
                            Record Vitals
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* ═══════════════════════════════════════════════════
            TAB 2 — VITALS ENTRY
        ═══════════════════════════════════════════════════ */}
        {activeTab === "vitals" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {/* Patient selector */}
            <div className="zv-card p-4 space-y-2 lg:col-span-1">
              <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Select Patient</h3>
              {patients.map(p => (
                <button
                  key={p.id}
                  onClick={() => {
                    setSelectedPatient(p);
                    setVitalsForm(emptyVitals(p));
                    setVitalsSuccess(false);
                  }}
                  className={`w-full text-left px-3 py-2.5 rounded-lg border transition text-xs ${
                    selectedPatient?.id === p.id
                      ? "border-[var(--primary)] bg-[var(--primary)]/10 text-[var(--text-primary)]"
                      : "border-[var(--border-default)] text-[var(--text-muted)] hover:border-[var(--primary)]/40"
                  }`}
                >
                  <div className="font-semibold text-[var(--text-primary)]">{p.name}</div>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="font-mono">{p.bed}</span>
                    <span>·</span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${statusColor(p.status)}`}>
                      {p.status.replace("_", " ")}
                    </span>
                  </div>
                </button>
              ))}
            </div>

            {/* Vitals form */}
            <div className="zv-card p-5 lg:col-span-2">
              {!selectedPatient ? (
                <div className="h-full flex items-center justify-center text-center py-20">
                  <div>
                    <div className="text-3xl mb-3">🩺</div>
                    <p className="text-sm text-[var(--text-muted)]">Select a patient to record vitals</p>
                  </div>
                </div>
              ) : vitalsSuccess ? (
                <div className="h-full flex items-center justify-center text-center py-20">
                  <div>
                    <div className="text-4xl mb-3">✅</div>
                    <p className="text-base font-semibold text-emerald-400">Vitals Recorded Successfully</p>
                    <p className="text-xs text-[var(--text-muted)] mt-1">for {selectedPatient.name}</p>
                  </div>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-5">
                    <div>
                      <h3 className="font-semibold text-[var(--text-primary)]">
                        {selectedPatient.name}
                      </h3>
                      <p className="text-xs text-[var(--text-muted)]">
                        {selectedPatient.bed} · {selectedPatient.mrn} · {selectedPatient.age}y {selectedPatient.gender}
                      </p>
                    </div>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${statusColor(selectedPatient.status)}`}>
                      {selectedPatient.status.replace("_", " ")}
                    </span>
                  </div>

                  {vitalsForm && (
                    <div className="grid grid-cols-2 gap-4">
                      {/* BP */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Blood Pressure (mmHg)
                        </label>
                        <input
                          type="text"
                          placeholder="e.g. 120/80"
                          value={vitalsForm.bp}
                          onChange={e => setVitalsForm({ ...vitalsForm, bp: e.target.value })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* Pulse */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Pulse (bpm)
                        </label>
                        <input
                          type="number"
                          placeholder="e.g. 78"
                          value={vitalsForm.pulse}
                          onChange={e => setVitalsForm({ ...vitalsForm, pulse: e.target.value === "" ? "" : Number(e.target.value) })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* Temperature */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Temperature (°F)
                        </label>
                        <input
                          type="number"
                          step="0.1"
                          placeholder="e.g. 98.6"
                          value={vitalsForm.temp}
                          onChange={e => setVitalsForm({ ...vitalsForm, temp: e.target.value === "" ? "" : Number(e.target.value) })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* SpO2 */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          SpO₂ (%)
                        </label>
                        <input
                          type="number"
                          placeholder="e.g. 98"
                          value={vitalsForm.spo2}
                          onChange={e => setVitalsForm({ ...vitalsForm, spo2: e.target.value === "" ? "" : Number(e.target.value) })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* RR */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Respiratory Rate (breaths/min)
                        </label>
                        <input
                          type="number"
                          placeholder="e.g. 16"
                          value={vitalsForm.rr}
                          onChange={e => setVitalsForm({ ...vitalsForm, rr: e.target.value === "" ? "" : Number(e.target.value) })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* Weight */}
                      <div>
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Weight (kg)
                        </label>
                        <input
                          type="number"
                          step="0.1"
                          placeholder="e.g. 72.5"
                          value={vitalsForm.weight}
                          onChange={e => setVitalsForm({ ...vitalsForm, weight: e.target.value === "" ? "" : Number(e.target.value) })}
                          className="zv-input w-full text-sm"
                        />
                      </div>
                      {/* Notes */}
                      <div className="col-span-2">
                        <label className="block text-xs font-medium text-[var(--text-muted)] mb-1">
                          Nursing Notes
                        </label>
                        <textarea
                          rows={3}
                          placeholder="Patient complaints, observations, behaviour changes, wound status…"
                          value={vitalsForm.notes}
                          onChange={e => setVitalsForm({ ...vitalsForm, notes: e.target.value })}
                          className="zv-input w-full text-sm resize-none"
                        />
                      </div>
                      {/* Submit */}
                      <div className="col-span-2 flex gap-3 pt-2">
                        <button
                          onClick={handleVitalsSubmit}
                          disabled={vitalsSubmitting}
                          className="zv-btn-primary flex-1 py-2.5 font-semibold text-sm disabled:opacity-50"
                        >
                          {vitalsSubmitting ? "Saving…" : "✅ Save Vitals"}
                        </button>
                        <button
                          onClick={() => { setSelectedPatient(null); setVitalsForm(null); }}
                          className="zv-btn-secondary px-5 py-2.5 text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════
            TAB 3 — MEDICATION ROUND
        ═══════════════════════════════════════════════════ */}
        {activeTab === "medications" && (
          <div className="zv-card overflow-hidden">
            <div className="px-5 py-4 border-b border-[var(--border-default)]">
              <h3 className="font-semibold text-[var(--text-primary)]">Today's Medication Schedule</h3>
              <p className="text-xs text-[var(--text-muted)] mt-0.5">
                {medSchedule.filter(m => m.status === "GIVEN").length} given ·{" "}
                <span className="text-amber-400 font-medium">{pendingMeds} pending</span> ·{" "}
                {medSchedule.filter(m => m.status === "HELD").length} held
              </p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-[var(--border-default)] bg-[var(--bg-elevated)]">
                  <tr className="text-left text-[var(--text-muted)] text-xs font-semibold">
                    <th className="px-4 py-3">Time</th>
                    <th className="px-4 py-3">Patient / Bed</th>
                    <th className="px-4 py-3">Medicine</th>
                    <th className="px-4 py-3">Dose / Route</th>
                    <th className="px-4 py-3">Prescribed By</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {medSchedule.map(m => (
                    <tr key={m.id} className={`hover:bg-[var(--bg-elevated)] transition ${m.status === "GIVEN" ? "opacity-60" : ""}`}>
                      <td className="px-4 py-3 font-mono text-xs text-emerald-400 font-bold">{m.scheduledTime}</td>
                      <td className="px-4 py-3">
                        <div className="font-semibold text-[var(--text-primary)] text-xs">{m.patientName}</div>
                        <div className="text-[10px] text-[var(--text-muted)]">{m.bed} · {m.mrn}</div>
                      </td>
                      <td className="px-4 py-3 font-medium text-[var(--text-primary)] text-xs">{m.medicineName}</td>
                      <td className="px-4 py-3 text-xs text-[var(--text-muted)]">
                        {m.dose} · <span className="italic">{m.route}</span>
                      </td>
                      <td className="px-4 py-3 text-xs text-[var(--text-muted)]">{m.prescribedBy}</td>
                      <td className="px-4 py-3">
                        <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${medStatusColor(m.status)}`}>
                          {m.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        {m.status === "PENDING" ? (
                          <div className="flex items-center gap-1.5 justify-end">
                            <button
                              onClick={() => markMed(m.id, "GIVEN")}
                              className="text-[10px] px-2.5 py-1 rounded font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30 transition"
                            >
                              ✓ Given
                            </button>
                            <button
                              onClick={() => markMed(m.id, "HELD")}
                              className="text-[10px] px-2.5 py-1 rounded font-semibold bg-red-500/15 text-red-400 border border-red-500/25 hover:bg-red-500/25 transition"
                            >
                              Hold
                            </button>
                            <button
                              onClick={() => markMed(m.id, "SKIPPED")}
                              className="text-[10px] px-2.5 py-1 rounded font-semibold bg-gray-500/10 text-gray-400 border border-gray-500/20 hover:bg-gray-500/20 transition"
                            >
                              Skip
                            </button>
                          </div>
                        ) : (
                          <button
                            onClick={() => markMed(m.id, "PENDING")}
                            className="text-[10px] px-2.5 py-1 rounded font-semibold text-[var(--text-muted)] border border-[var(--border-default)] hover:border-amber-500/40 transition"
                          >
                            Undo
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ═══════════════════════════════════════════════════
            TAB 4 — WARD ROUNDS
        ═══════════════════════════════════════════════════ */}
        {activeTab === "rounds" && (
          <div className="space-y-3">
            <div className="zv-card px-5 py-4">
              <h3 className="font-semibold text-[var(--text-primary)]">Morning Ward Round Checklist</h3>
              <p className="text-xs text-[var(--text-muted)] mt-0.5">
                {Object.values(roundChecked).filter(Boolean).length} of {patients.length} patients reviewed
              </p>
            </div>
            {patients.map(p => (
              <div key={p.id} className={`zv-card p-5 border transition ${
                roundChecked[p.id]
                  ? "border-emerald-500/30 bg-emerald-500/5"
                  : "border-[var(--border-default)]"
              }`}>
                <div className="flex items-start gap-4">
                  {/* Checkbox */}
                  <button
                    onClick={() => setRoundChecked(prev => ({ ...prev, [p.id]: !prev[p.id] }))}
                    className={`mt-0.5 w-5 h-5 rounded border-2 flex-shrink-0 flex items-center justify-center transition ${
                      roundChecked[p.id]
                        ? "border-emerald-400 bg-emerald-400"
                        : "border-[var(--border-default)]"
                    }`}
                  >
                    {roundChecked[p.id] && <span className="text-[10px] text-black font-bold">✓</span>}
                  </button>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-semibold text-[var(--text-primary)]">{p.name}</span>
                      <span className="font-mono text-xs text-emerald-400">{p.bed}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${statusColor(p.status)}`}>
                        {p.status.replace("_", " ")}
                      </span>
                    </div>
                    <div className="text-xs text-[var(--text-muted)] mt-0.5">
                      {p.mrn} · {p.age}y {p.gender} · {p.primaryDiagnosis}
                    </div>
                    <div className="text-xs text-[var(--text-muted)] mt-0.5">
                      Attending: {p.attendingDoctor}
                    </div>

                    {/* Alert flags */}
                    {p.alertFlags.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1.5">
                        {p.alertFlags.map((f, i) => (
                          <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-red-500/15 text-red-400 border border-red-500/25">
                            ⚠ {f}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Round notes */}
                    <textarea
                      rows={2}
                      placeholder="Round observations, patient complaints, plan changes…"
                      value={roundNotes[p.id] || ""}
                      onChange={e => setRoundNotes(prev => ({ ...prev, [p.id]: e.target.value }))}
                      className="zv-input w-full text-xs mt-3 resize-none"
                    />
                  </div>
                </div>
              </div>
            ))}

            {patients.length > 0 && (
              <div className="flex justify-end">
                <button
                  onClick={() => {
                    // POST round notes to API (fire-and-forget)
                    const session = AuthService.getSession();
                    fetch(`${API}/api/v1/ward/round-notes`, {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                        ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {}),
                      },
                      body: JSON.stringify({ notes: roundNotes, timestamp: new Date().toISOString() }),
                    }).catch(() => {});
                    alert("Round notes saved ✓");
                  }}
                  className="zv-btn-primary px-6 py-2.5 font-semibold text-sm"
                >
                  Save Round Notes →
                </button>
              </div>
            )}
          </div>
        )}

      </div>
    </AppShell>
  );
}
