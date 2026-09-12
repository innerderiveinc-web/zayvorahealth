"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

interface QueuePatient {
  id: string;
  mrn: string;
  name: string;
  age: number;
  sex: string;
  arrival_time: string;
  acuity: "CRITICAL" | "URGENT" | "STANDARD" | "FOLLOWUP";
  chief_complaint: string;
  assigned_doctor: string;
  room: string;
  status: "WAITING" | "IN_CONSULTATION" | "LAB_PENDING" | "COMPLETED";
}

const INITIAL_QUEUE: QueuePatient[] = [
  {
    id: "Q-101",
    mrn: "MRN-DEL-8921",
    name: "Fatima Begum",
    age: 48,
    sex: "F",
    arrival_time: "09:15 AM",
    acuity: "URGENT",
    chief_complaint: "Acute exacerbation of Waja-ul-Mafasil with knee effusion",
    assigned_doctor: "Dr. Hakeem Tariq Ahmad",
    room: "OPD Room 3",
    status: "IN_CONSULTATION",
  },
  {
    id: "Q-102",
    mrn: "MRN-DEL-4410",
    name: "Mohammed Zeeshan",
    age: 36,
    sex: "M",
    arrival_time: "09:30 AM",
    acuity: "STANDARD",
    chief_complaint: "Epigastric distress, Su-e-Hazm, post-prandial fullness",
    assigned_doctor: "Dr. Asma Parveen",
    room: "OPD Room 1",
    status: "WAITING",
  },
  {
    id: "Q-103",
    mrn: "MRN-DEL-9932",
    name: "Aisha Siddiqui",
    age: 62,
    sex: "F",
    arrival_time: "09:45 AM",
    acuity: "FOLLOWUP",
    chief_complaint: "Routine 4-week follow-up for Ziabetes Shakari care plan",
    assigned_doctor: "Dr. Hakeem Tariq Ahmad",
    room: "OPD Room 3",
    status: "WAITING",
  },
  {
    id: "Q-104",
    mrn: "MRN-DEL-1029",
    name: "Khurram Shahzad",
    age: 54,
    sex: "M",
    arrival_time: "10:00 AM",
    acuity: "CRITICAL",
    chief_complaint: "Severe acute chest constriction with diaphoresis (Red Flag)",
    assigned_doctor: "Emergency Triage Officer",
    room: "Triage Bed A",
    status: "IN_CONSULTATION",
  },
];

export default function ClinicOperationsPage() {
  const [queue, setQueue] = useState<QueuePatient[]>(INITIAL_QUEUE);
  const [filterAcuity, setFilterAcuity] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedQueueItem, setSelectedQueueItem] = useState<QueuePatient | null>(INITIAL_QUEUE[0]);
  const [activeTab, setActiveTab] = useState<"queue" | "rooms" | "billing" | "staff">("queue");

  const filteredQueue = queue.filter((p) => {
    const matchesAcuity = filterAcuity === "ALL" || p.acuity === filterAcuity;
    const matchesSearch =
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.mrn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.chief_complaint.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesAcuity && matchesSearch;
  });

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Top Control Bar */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">Clinic & Hospital Operations Cockpit</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 font-semibold">
                Jamia Hamdard AUTC Medical Center
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Live patient triage, OPD consultation room assignments, queuing automation, and service billing.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                const newPatient: QueuePatient = {
                  id: `Q-${Date.now().toString().slice(-3)}`,
                  mrn: `MRN-DEL-${Math.floor(1000 + Math.random() * 9000)}`,
                  name: "Walk-in Patient",
                  age: 40,
                  sex: "M",
                  arrival_time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                  acuity: "STANDARD",
                  chief_complaint: "General consultation and vital sign check",
                  assigned_doctor: "Dr. Asma Parveen",
                  room: "OPD Room 2",
                  status: "WAITING",
                };
                setQueue([newPatient, ...queue]);
              }}
              className="zv-btn-primary text-xs font-semibold py-2 px-3.5 cursor-pointer shadow-sm"
            >
              + Check-In Walk-In Patient
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex flex-wrap gap-2 border-b border-[var(--border)] pb-2">
          <button
            onClick={() => setActiveTab("queue")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "queue"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            📋 Live Patient Queue & Triage ({filteredQueue.length})
          </button>
          <button
            onClick={() => setActiveTab("rooms")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "rooms"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            🚪 OPD Consultation Rooms (4 Active)
          </button>
          <button
            onClick={() => setActiveTab("billing")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "billing"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            💳 Billing & Invoices
          </button>
          <button
            onClick={() => setActiveTab("staff")}
            className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-colors ${
              activeTab === "staff"
                ? "bg-[var(--emerald)] text-white border-transparent"
                : "border-[var(--border)] text-[var(--muted)] hover:text-white"
            }`}
          >
            👥 Attending Staff & Shifts
          </button>
        </div>

        {/* TAB 1: Queue & Triage */}
        {activeTab === "queue" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Queue Table */}
            <div className="lg:col-span-2 space-y-4">
              <div className="flex flex-col sm:flex-row gap-3 justify-between items-center">
                <input
                  type="text"
                  placeholder="Search patient, MRN, complaint..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="zv-input text-xs max-w-sm"
                />
                <div className="flex items-center gap-2">
                  <label className="text-xs text-[var(--muted)]">Acuity:</label>
                  <select
                    value={filterAcuity}
                    onChange={(e) => setFilterAcuity(e.target.value)}
                    className="zv-input text-xs py-1.5 px-3"
                  >
                    <option value="ALL">All Acuity Levels</option>
                    <option value="CRITICAL">Critical (Red Flag)</option>
                    <option value="URGENT">Urgent</option>
                    <option value="STANDARD">Standard</option>
                    <option value="FOLLOWUP">Follow-up</option>
                  </select>
                </div>
              </div>

              <div className="zv-panel overflow-hidden">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[var(--elevated)] border-b border-[var(--border)] text-[var(--muted)] uppercase tracking-wider">
                    <tr>
                      <th className="p-3">Patient / MRN</th>
                      <th className="p-3">Acuity</th>
                      <th className="p-3">Arrival</th>
                      <th className="p-3">Doctor / Room</th>
                      <th className="p-3">Status</th>
                      <th className="p-3 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border)]">
                    {filteredQueue.map((item) => (
                      <tr
                        key={item.id}
                        onClick={() => setSelectedQueueItem(item)}
                        className={`hover:bg-[var(--elevated)] cursor-pointer transition-colors ${
                          selectedQueueItem?.id === item.id ? "bg-[var(--elevated)]" : ""
                        }`}
                      >
                        <td className="p-3 font-medium">
                          <div className="text-white font-semibold">{item.name}</div>
                          <div className="text-[11px] text-[var(--muted)] font-mono">{item.mrn} · {item.age}y {item.sex}</div>
                        </td>
                        <td className="p-3">
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                              item.acuity === "CRITICAL"
                                ? "bg-red-500/20 text-red-400 border border-red-500/40"
                                : item.acuity === "URGENT"
                                ? "bg-amber-500/20 text-amber-400 border border-amber-500/40"
                                : item.acuity === "FOLLOWUP"
                                ? "bg-blue-500/20 text-blue-400 border border-blue-500/40"
                                : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
                            }`}
                          >
                            {item.acuity}
                          </span>
                        </td>
                        <td className="p-3 text-[var(--muted)]">{item.arrival_time}</td>
                        <td className="p-3">
                          <div className="text-white">{item.assigned_doctor}</div>
                          <div className="text-[11px] text-[var(--gold-soft)]">{item.room}</div>
                        </td>
                        <td className="p-3">
                          <span className="text-[11px] text-white">
                            {item.status.replace("_", " ")}
                          </span>
                        </td>
                        <td className="p-3 text-right">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setQueue(
                                queue.map((q) =>
                                  q.id === item.id
                                    ? {
                                        ...q,
                                        status: q.status === "WAITING" ? "IN_CONSULTATION" : "COMPLETED",
                                      }
                                    : q
                                )
                              );
                            }}
                            className="text-[11px] px-2.5 py-1 rounded bg-[var(--elevated)] border border-[var(--border)] hover:bg-[var(--border)]"
                          >
                            {item.status === "WAITING" ? "Call In" : "Discharge"}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Selected Patient Triage Detail Panel */}
            <div className="zv-panel p-5 space-y-4">
              <div className="border-b border-[var(--border)] pb-3">
                <span className="text-[10px] uppercase tracking-wider text-[var(--muted)] block">Triage Inspector</span>
                <h3 className="text-base font-bold text-white">{selectedQueueItem?.name}</h3>
                <span className="text-xs font-mono text-[var(--gold-soft)]">{selectedQueueItem?.mrn}</span>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-[var(--muted)] block">Chief Complaint</span>
                  <p className="text-white font-medium mt-0.5">{selectedQueueItem?.chief_complaint}</p>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-2 border-t border-[var(--border)]">
                  <div>
                    <span className="text-[var(--muted)] block">Assigned Clinician</span>
                    <span className="text-white font-medium">{selectedQueueItem?.assigned_doctor}</span>
                  </div>
                  <div>
                    <span className="text-[var(--muted)] block">Location</span>
                    <span className="text-emerald-400 font-medium">{selectedQueueItem?.room}</span>
                  </div>
                </div>

                <div className="pt-2 border-t border-[var(--border)]">
                  <span className="text-[var(--muted)] block">Triage Action Protocol</span>
                  {selectedQueueItem?.acuity === "CRITICAL" ? (
                    <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 space-y-1 mt-1">
                      <span className="font-bold block">⚠️ STAT Emergency Protocol Activated</span>
                      <p className="text-[11px]">Immediate ECG, Continuous SpO2/NIBP telemetry, and Emergency Physician Notification.</p>
                    </div>
                  ) : (
                    <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)] text-[var(--text)] mt-1">
                      Standard OPD clinical assessment workflow. Ready for vital verification and doctor consultation.
                    </div>
                  )}
                </div>

                <div className="pt-4 flex flex-col gap-2">
                  <a
                    href="/doctor"
                    className="zv-btn-primary text-center text-xs font-semibold py-2 block"
                  >
                    Open Clinical Consultation
                  </a>
                </div>
              </div>
            </div>

          </div>
        )}

        {/* TAB 2: OPD Rooms */}
        {activeTab === "rooms" && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { room: "OPD Room 1", doctor: "Dr. Asma Parveen", spec: "General Unani Medicine", patient: "Mohammed Zeeshan", status: "Occupied" },
              { room: "OPD Room 2", doctor: "Dr. Khalid Mansoor", spec: "Ilaj bil-Tadbeer & Hijama", patient: "None (Sterilizing)", status: "Available" },
              { room: "OPD Room 3", doctor: "Dr. Hakeem Tariq Ahmad", spec: "Integrative Rheumatology", patient: "Fatima Begum", status: "Occupied" },
              { room: "Triage Bed A", doctor: "Emergency Triage Officer", spec: "Acute Stabilization", patient: "Khurram Shahzad", status: "Critical Care" },
            ].map((r) => (
              <div key={r.room} className="zv-panel p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-sm text-white">{r.room}</h4>
                  <span
                    className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                      r.status === "Occupied"
                        ? "bg-amber-500/20 text-amber-400"
                        : r.status === "Available"
                        ? "bg-emerald-500/20 text-emerald-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {r.status}
                  </span>
                </div>
                <div className="text-xs space-y-1">
                  <div className="text-[var(--muted)]">Doctor: <span className="text-white font-medium">{r.doctor}</span></div>
                  <div className="text-[var(--muted)]">Specialty: <span className="text-[var(--gold-soft)]">{r.spec}</span></div>
                  <div className="text-[var(--muted)]">Current Patient: <span className="text-white font-medium">{r.patient}</span></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB 3: Billing & Invoicing */}
        {activeTab === "billing" && (
          <div className="zv-panel p-5 space-y-4">
            <h3 className="font-bold text-sm">Outpatient Clinical Billing Ledger</h3>
            <table className="w-full text-left text-xs">
              <thead className="bg-[var(--elevated)] text-[var(--muted)] uppercase border-b border-[var(--border)]">
                <tr>
                  <th className="p-3">Invoice #</th>
                  <th className="p-3">Patient</th>
                  <th className="p-3">Services Rendered</th>
                  <th className="p-3">Amount</th>
                  <th className="p-3">Payment Status</th>
                  <th className="p-3">Receipt</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--border)]">
                {[
                  { inv: "INV-2026-0811", patient: "Fatima Begum", services: "Specialist Consultation + Mizaj Profiling", amount: "₹1,200", status: "PAID (UPI)" },
                  { inv: "INV-2026-0812", patient: "Mohammed Zeeshan", services: "OPD Consultation + Su-e-Mizaj Battery", amount: "₹850", status: "PAID (Card)" },
                  { inv: "INV-2026-0813", patient: "Khurram Shahzad", services: "Emergency Triage + Diagnostic ECG", amount: "₹2,500", status: "PENDING TPA" },
                ].map((b) => (
                  <tr key={b.inv} className="hover:bg-[var(--elevated)]">
                    <td className="p-3 font-mono text-[var(--gold-soft)]">{b.inv}</td>
                    <td className="p-3 font-medium text-white">{b.patient}</td>
                    <td className="p-3 text-[var(--muted)]">{b.services}</td>
                    <td className="p-3 font-bold text-white">{b.amount}</td>
                    <td className="p-3">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        b.status.includes("PAID") ? "bg-emerald-500/20 text-emerald-400" : "bg-amber-500/20 text-amber-400"
                      }`}>
                        {b.status}
                      </span>
                    </td>
                    <td className="p-3">
                      <button className="text-xs text-blue-400 hover:underline">Download PDF</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* TAB 4: Staff & Shifts */}
        {activeTab === "staff" && (
          <div className="zv-panel p-5 space-y-4">
            <h3 className="font-bold text-sm">Active Clinical Shifts & Credentials</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { name: "Dr. Hakeem Tariq Ahmad", role: "Senior Attending Tabeeb", reg: "CCIM/UNANI/2012/8821", shift: "Morning (08:00 - 14:00)", status: "Active" },
                { name: "Dr. Asma Parveen", role: "Resident Clinician", reg: "CCIM/UNANI/2019/4102", shift: "Morning (08:00 - 14:00)", status: "Active" },
                { name: "Dr. Khalid Mansoor", role: "Regimenal Specialist (Tadbeer)", reg: "CCIM/UNANI/2015/7719", shift: "Afternoon (12:00 - 18:00)", status: "On-Duty" },
              ].map((s) => (
                <div key={s.name} className="p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)] space-y-2 text-xs">
                  <div className="font-bold text-white text-sm">{s.name}</div>
                  <div className="text-[var(--gold-soft)] font-medium">{s.role}</div>
                  <div className="text-[var(--muted)]">Reg: <span className="font-mono">{s.reg}</span></div>
                  <div className="text-[var(--muted)]">Shift: {s.shift}</div>
                  <span className="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400">
                    {s.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
