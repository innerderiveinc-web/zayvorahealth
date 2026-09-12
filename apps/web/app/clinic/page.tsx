"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";

interface QueueItem {
  id: string;
  token: string;
  mrn: string;
  name: string;
  age: number;
  sex: string;
  arrivalTime: string;
  acuity: "URGENT" | "STANDARD" | "FOLLOWUP";
  chiefComplaint: string;
  doctor: string;
  room: string;
  status: "WAITING" | "IN_CONSULTATION" | "COMPLETED";
}

const INITIAL_QUEUE: QueueItem[] = [
  {
    id: "Q-104",
    token: "T-104",
    mrn: "MRN-2026-0814",
    name: "Hamza Farooqi",
    age: 42,
    sex: "M",
    arrivalTime: "10:15 AM",
    acuity: "STANDARD",
    chiefComplaint: "Bilateral knee stiffness, joint pain in cold weather",
    doctor: "Hakim Dr. Tariq Mansoor",
    room: "OPD Room 3",
    status: "IN_CONSULTATION",
  },
  {
    id: "Q-105",
    token: "T-105",
    mrn: "MRN-2026-0815",
    name: "Aisha Siddiqui",
    age: 58,
    sex: "F",
    arrivalTime: "10:30 AM",
    acuity: "URGENT",
    chiefComplaint: "Acute Su-e-Hazm with epigastric burning",
    doctor: "Hakim Dr. Tariq Mansoor",
    room: "OPD Room 3",
    status: "WAITING",
  },
  {
    id: "Q-106",
    token: "T-106",
    mrn: "MRN-2026-0816",
    name: "Mohammed Zeeshan",
    age: 36,
    sex: "M",
    arrivalTime: "10:45 AM",
    acuity: "FOLLOWUP",
    chiefComplaint: "Post-Tadbeer evaluation for lumbar spasm",
    doctor: "Dr. Asma Parveen",
    room: "OPD Room 1",
    status: "WAITING",
  },
];

interface DoctorRoster {
  id: string;
  name: string;
  specialty: string;
  room: string;
  status: "ACTIVE" | "BUSY" | "ON_BREAK";
  currentPatient: string;
}

const INITIAL_ROSTER: DoctorRoster[] = [
  {
    id: "DOC-1001",
    name: "Hakim Dr. Tariq Mansoor",
    specialty: "Unani Rheumatology & Musculoskeletal",
    room: "OPD Room 3",
    status: "BUSY",
    currentPatient: "Hamza Farooqi (T-104)",
  },
  {
    id: "DOC-1002",
    name: "Dr. Asma Parveen",
    specialty: "Ilaj-bit-Tadbeer & Regimenal Medicine",
    room: "OPD Room 1",
    status: "ACTIVE",
    currentPatient: "Ready for next patient",
  },
];

export default function ClinicWorkspacePage() {
  const [activeTab, setActiveTab] = useState<"queue" | "register" | "roster" | "billing">("queue");
  const [queue, setQueue] = useState<QueueItem[]>(INITIAL_QUEUE);
  const [roster] = useState<DoctorRoster[]>(INITIAL_ROSTER);

  // Walk-in Registration form state
  const [regName, setRegName] = useState("");
  const [regAge, setRegAge] = useState("");
  const [regSex, setRegSex] = useState("M");
  const [regPhone, setRegPhone] = useState("");
  const [regComplaint, setRegComplaint] = useState("");
  const [regDoctor, setRegDoctor] = useState("Hakim Dr. Tariq Mansoor");
  const [regSuccess, setRegSuccess] = useState<string | null>(null);

  const handleRegisterPatient = (e: React.FormEvent) => {
    e.preventDefault();
    if (!regName.trim() || !regPhone.trim()) return;

    const nextTokenNum = 104 + queue.length;
    const newItem: QueueItem = {
      id: `Q-${nextTokenNum}`,
      token: `T-${nextTokenNum}`,
      mrn: `MRN-2026-0${nextTokenNum}`,
      name: regName,
      age: parseInt(regAge, 10) || 30,
      sex: regSex,
      arrivalTime: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      acuity: "STANDARD",
      chiefComplaint: regComplaint || "General consultation",
      doctor: regDoctor,
      room: regDoctor.includes("Tariq") ? "OPD Room 3" : "OPD Room 1",
      status: "WAITING",
    };

    setQueue([...queue, newItem]);
    setRegSuccess(`Patient registered! Token issued: ${newItem.token} (Assigned to ${newItem.room})`);
    setRegName("");
    setRegAge("");
    setRegPhone("");
    setRegComplaint("");
    setTimeout(() => setRegSuccess(null), 5000);
  };

  const handleUpdateStatus = (id: string, newStatus: QueueItem["status"]) => {
    setQueue(queue.map((item) => (item.id === id ? { ...item, status: newStatus } : item)));
  };

  return (
    <AppShell activeRole="clinic">
      <div className="space-y-5 max-w-7xl mx-auto">
        
        {/* Workspace Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight">Clinic Reception & OPD Operations</h1>
            <p className="text-xs text-[#94A3B8]">
              Central Integrated Facility • Sana Khan (OPD Operations Lead)
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("register")}
              className="zv-btn-primary text-xs bg-[#0D9488]"
            >
              + Register Walk-In Patient
            </button>
          </div>
        </div>

        {/* Executive Clinic Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard label="Today's Intake" value="18" subtext="Checked in" variant="teal" icon="📋" />
          <StatCard label="Waiting Queue" value={queue.filter(q => q.status === "WAITING").length} subtext="In waiting lobby" variant="amber" icon="⏳" />
          <StatCard label="In Consult" value={queue.filter(q => q.status === "IN_CONSULTATION").length} subtext="Across 2 rooms" variant="emerald" icon="🩺" />
          <StatCard label="Revenue Collected" value="₹14,500" subtext="Cash & UPI" variant="teal" icon="💳" />
          <StatCard label="Pending Bills" value="2" subtext="Awaiting settlement" variant="rose" icon="⚠️" />
          <StatCard label="Dispensary Pickups" value="6" subtext="Ready at counter" variant="blue" icon="💊" />
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-[#334155] flex gap-2">
          {[
            { id: "queue", label: "Live OPD Queue", icon: "📋" },
            { id: "register", label: "Walk-In Intake Form", icon: "📝" },
            { id: "roster", label: "Doctor Availability & Rooms", icon: "🩺" },
            { id: "billing", label: "Billing & Cash Counter", icon: "💳" },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold border-b-2 transition ${
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

        {/* TAB 1: LIVE OPD QUEUE */}
        {activeTab === "queue" && (
          <div className="zv-card overflow-hidden">
            <div className="p-4 border-b border-[#334155] flex justify-between items-center bg-[#0F172A]">
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Live OPD Token Queue</h3>
              <span className="text-[11px] text-[#94A3B8]">Auto-updates in real time</span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#0A0F1D] text-[#94A3B8] border-b border-[#334155]">
                  <tr>
                    <th className="p-3">Token</th>
                    <th className="p-3">Patient Name / MRN</th>
                    <th className="p-3">Arrival</th>
                    <th className="p-3">Assigned Room & Doctor</th>
                    <th className="p-3">Acuity</th>
                    <th className="p-3">Status</th>
                    <th className="p-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#334155]">
                  {queue.map((item) => (
                    <tr key={item.id} className="hover:bg-[#1E293B]/50 transition">
                      <td className="p-3 font-mono font-bold text-[#2DD4BF]">{item.token}</td>
                      <td className="p-3">
                        <span className="font-semibold text-white block">{item.name}</span>
                        <span className="text-[11px] text-[#94A3B8] font-mono">{item.mrn} • {item.age}y / {item.sex}</span>
                      </td>
                      <td className="p-3 text-[#94A3B8] font-mono">{item.arrivalTime}</td>
                      <td className="p-3">
                        <span className="text-white font-medium block">{item.room}</span>
                        <span className="text-[11px] text-[#94A3B8]">{item.doctor}</span>
                      </td>
                      <td className="p-3">
                        <span className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                          item.acuity === "URGENT" ? "zv-badge-rose" : "zv-badge-blue"
                        }`}>
                          {item.acuity}
                        </span>
                      </td>
                      <td className="p-3">
                        <StatusBadge
                          status={item.status.replace("_", " ")}
                          variant={item.status === "IN_CONSULTATION" ? "verified" : item.status === "WAITING" ? "pending" : "neutral"}
                        />
                      </td>
                      <td className="p-3 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          {item.status === "WAITING" && (
                            <button
                              onClick={() => handleUpdateStatus(item.id, "IN_CONSULTATION")}
                              className="zv-btn-primary text-[11px] py-1 px-2.5 bg-[#0D9488]"
                            >
                              Call to Room
                            </button>
                          )}
                          {item.status === "IN_CONSULTATION" && (
                            <button
                              onClick={() => handleUpdateStatus(item.id, "COMPLETED")}
                              className="zv-btn-secondary text-[11px] py-1 px-2.5"
                            >
                              Mark Done
                            </button>
                          )}
                          {item.status === "COMPLETED" && (
                            <span className="text-[11px] text-[#34D399] font-medium">Completed</span>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* TAB 2: WALK-IN REGISTRATION FORM */}
        {activeTab === "register" && (
          <div className="zv-card p-5 max-w-2xl mx-auto space-y-4">
            <div>
              <h3 className="text-sm font-bold text-white">Walk-In Patient Registration & Token Issuance</h3>
              <p className="text-xs text-[#94A3B8] mt-0.5">Captures primary demographics and immediately inserts patient into live OPD queue</p>
            </div>

            {regSuccess && (
              <div className="p-3 bg-[#10B981]/15 border border-[#10B981]/30 rounded-lg text-xs text-[#34D399] font-semibold">
                ✓ {regSuccess}
              </div>
            )}

            <form onSubmit={handleRegisterPatient} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-[#94A3B8] block mb-1">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={regName}
                    onChange={(e) => setRegName(e.target.value)}
                    placeholder="e.g. Tariq Mehmood"
                    className="zv-input"
                  />
                </div>
                <div>
                  <label className="text-[#94A3B8] block mb-1">Contact Phone *</label>
                  <input
                    type="text"
                    required
                    value={regPhone}
                    onChange={(e) => setRegPhone(e.target.value)}
                    placeholder="+91-9876543210"
                    className="zv-input"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-[#94A3B8] block mb-1">Age</label>
                  <input
                    type="number"
                    value={regAge}
                    onChange={(e) => setRegAge(e.target.value)}
                    placeholder="35"
                    className="zv-input"
                  />
                </div>
                <div>
                  <label className="text-[#94A3B8] block mb-1">Gender</label>
                  <select
                    value={regSex}
                    onChange={(e) => setRegSex(e.target.value)}
                    className="zv-input bg-[#0F172A]"
                  >
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="text-[#94A3B8] block mb-1">Assigned Doctor</label>
                  <select
                    value={regDoctor}
                    onChange={(e) => setRegDoctor(e.target.value)}
                    className="zv-input bg-[#0F172A]"
                  >
                    <option value="Hakim Dr. Tariq Mansoor">Hakim Dr. Tariq Mansoor (Room 3)</option>
                    <option value="Dr. Asma Parveen">Dr. Asma Parveen (Room 1)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-[#94A3B8] block mb-1">Chief Complaint</label>
                <textarea
                  rows={2}
                  value={regComplaint}
                  onChange={(e) => setRegComplaint(e.target.value)}
                  placeholder="Primary symptoms or reason for visit"
                  className="zv-input"
                />
              </div>

              <button
                type="submit"
                className="zv-btn-primary w-full py-2 bg-[#0D9488] font-bold"
              >
                Register & Issue OPD Queue Token
              </button>
            </form>
          </div>
        )}

        {/* TAB 3: DOCTOR ROSTER */}
        {activeTab === "roster" && (
          <div className="zv-card p-5 space-y-4">
            <h3 className="text-sm font-bold text-white">Consulting Physicians & Room Allocation</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {roster.map((doc) => (
                <div key={doc.id} className="p-4 bg-[#0A0F1D] rounded-lg border border-[#334155] space-y-2 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-white text-sm">{doc.name}</span>
                    <StatusBadge
                      status={doc.status}
                      variant={doc.status === "ACTIVE" ? "verified" : "pending"}
                    />
                  </div>
                  <p className="text-[#2DD4BF] font-medium">{doc.specialty}</p>
                  <div className="flex justify-between text-[#94A3B8] pt-2 border-t border-[#334155]">
                    <span>Consultation Room: <strong className="text-white">{doc.room}</strong></span>
                    <span>Status: <strong className="text-white">{doc.currentPatient}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: BILLING */}
        {activeTab === "billing" && (
          <div className="zv-card p-5 space-y-4 text-xs">
            <h3 className="text-sm font-bold text-white">Cash Counter & Billing Settlement</h3>
            <div className="p-4 bg-[#0A0F1D] rounded-lg border border-[#334155] flex justify-between items-center">
              <div>
                <span className="font-bold text-white text-sm">Invoice #INV-2026-0441 • Hamza Farooqi</span>
                <p className="text-[#94A3B8]">Items: Integrative Consultation (₹800) + Majun Suranjan 100g (₹450)</p>
                <span className="text-xs font-mono font-bold text-[#2DD4BF]">Total Amount: ₹1,250</span>
              </div>
              <div className="flex items-center gap-2">
                <StatusBadge status="Settled (UPI)" variant="verified" />
                <button className="zv-btn-secondary py-1 px-3">Print Receipt</button>
              </div>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
