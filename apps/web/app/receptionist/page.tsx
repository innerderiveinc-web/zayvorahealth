"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { AppointmentStatus, PaymentStatus } from "@/lib/shared/statusEnums";

interface ReceptionQueueItem {
  id: string;
  tokenNumber: string;
  mrn: string;
  patientName: string;
  age: number;
  gender: string;
  phone: string;
  arrivalTime: string;
  acuity: "URGENT" | "STANDARD" | "FOLLOWUP";
  chiefComplaint: string;
  assignedDoctor: string;
  opdRoom: string;
  status: AppointmentStatus;
  feeAmount: number;
  paymentStatus: PaymentStatus;
}

const INITIAL_QUEUE: ReceptionQueueItem[] = [
  {
    id: "Q-104",
    tokenNumber: "T-104",
    mrn: "MRN-2026-0814",
    patientName: "Hamza Farooqi",
    age: 44,
    gender: "Male",
    phone: "+91 98110 44219",
    arrivalTime: "10:15 AM",
    acuity: "STANDARD",
    chiefComplaint: "Bilateral knee stiffness, joint ache in cold weather",
    assignedDoctor: "Prof. (Dr.) Mansoor Alam",
    opdRoom: "OPD Room 3",
    status: "IN_CONSULTATION",
    feeAmount: 800,
    paymentStatus: "PAID",
  },
  {
    id: "Q-105",
    tokenNumber: "T-105",
    mrn: "MRN-2026-0815",
    patientName: "Ayesha Siddiqui",
    age: 58,
    gender: "Female",
    phone: "+91 98221 55301",
    arrivalTime: "10:28 AM",
    acuity: "URGENT",
    chiefComplaint: "Acute Su-e-Hazm with post-prandial heartburn",
    assignedDoctor: "Dr. Aisha Siddiqui",
    opdRoom: "OPD Room 2",
    status: "WAITING",
    feeAmount: 800,
    paymentStatus: "PAID",
  },
  {
    id: "Q-106",
    tokenNumber: "T-106",
    mrn: "MRN-2026-0816",
    patientName: "Mohammed Zeeshan",
    age: 36,
    gender: "Male",
    phone: "+91 98334 77190",
    arrivalTime: "10:40 AM",
    acuity: "FOLLOWUP",
    chiefComplaint: "Post-Tadbeer evaluation for lumbar muscle spasm",
    assignedDoctor: "Dr. Tariq Zafar",
    opdRoom: "OPD Room 1",
    status: "WAITING",
    feeAmount: 500,
    paymentStatus: "PAID",
  },
  {
    id: "Q-107",
    tokenNumber: "T-107",
    mrn: "MRN-2026-0817",
    patientName: "Fatima Bi",
    age: 51,
    gender: "Female",
    phone: "+91 98445 88203",
    arrivalTime: "10:55 AM",
    acuity: "STANDARD",
    chiefComplaint: "Metabolic follow-up (Ziabetus Shakari) & HbA1c review",
    assignedDoctor: "Prof. (Dr.) Mansoor Alam",
    opdRoom: "OPD Room 3",
    status: "WAITING",
    feeAmount: 800,
    paymentStatus: "PENDING",
  },
  {
    id: "Q-103",
    tokenNumber: "T-103",
    mrn: "MRN-2026-0813",
    patientName: "Rukhsana Begum",
    age: 62,
    gender: "Female",
    phone: "+91 98112 33419",
    arrivalTime: "09:30 AM",
    acuity: "STANDARD",
    chiefComplaint: "Cervical stiffness (Waja-ul-Unuq)",
    assignedDoctor: "Dr. Shagufta Parveen",
    opdRoom: "OPD Room 4",
    status: "COMPLETED",
    feeAmount: 800,
    paymentStatus: "PAID",
  }
];

interface DoctorRoster {
  id: string;
  name: string;
  specialty: string;
  room: string;
  status: "ACTIVE" | "BUSY" | "ON_BREAK";
  currentPatient: string;
  nextSlot: string;
}

const DOCTOR_ROSTER: DoctorRoster[] = [
  {
    id: "DOC-1001",
    name: "Prof. (Dr.) Mansoor Alam",
    specialty: "Ilmul Advia & Chronic Joint Dyscrasia",
    room: "OPD Room 3",
    status: "BUSY",
    currentPatient: "Hamza Farooqi (T-104)",
    nextSlot: "11:00 AM",
  },
  {
    id: "DOC-1002",
    name: "Dr. Aisha Siddiqui",
    specialty: "Tahaffuzi wa Samaji Tibb (Preventive Medicine)",
    room: "OPD Room 2",
    status: "ACTIVE",
    currentPatient: "Calling Next: Ayesha Siddiqui (T-105)",
    nextSlot: "10:45 AM",
  },
  {
    id: "DOC-1003",
    name: "Dr. Tariq Zafar",
    specialty: "Ilaj-bit-Tadbeer & Musculoskeletal Therapy",
    room: "OPD Room 1",
    status: "ACTIVE",
    currentPatient: "Calling Next: Mohammed Zeeshan (T-106)",
    nextSlot: "11:15 AM",
  },
  {
    id: "DOC-1004",
    name: "Dr. Shagufta Parveen",
    specialty: "Niswan wa Qabalat (Women's Health)",
    room: "OPD Room 4",
    status: "ON_BREAK",
    currentPatient: "Returning at 11:15 AM",
    nextSlot: "11:30 AM",
  },
];

export default function ReceptionistDashboardPage() {
  const [activeTab, setActiveTab] = useState<"queue" | "register" | "roster" | "billing" | "followup">("queue");
  const [queue, setQueue] = useState<ReceptionQueueItem[]>(INITIAL_QUEUE);
  const [filterAcuity, setFilterAcuity] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  
  // Registration Form State
  const [showRegModal, setShowRegModal] = useState(false);
  const [newPatient, setNewPatient] = useState({
    fullName: "",
    mobile: "",
    age: 35,
    gender: "Male",
    doctor: "Prof. (Dr.) Mansoor Alam",
    chiefComplaint: "",
    acuity: "STANDARD" as "STANDARD" | "URGENT" | "FOLLOWUP",
    feeAmount: 800
  });

  // Patient Call Notification
  const [callNotice, setCallNotice] = useState<string | null>(null);

  // Status Handler
  const handleUpdateStatus = (id: string, newStatus: AppointmentStatus) => {
    setQueue(prev => prev.map(item => item.id === id ? { ...item, status: newStatus } : item));
  };

  // Payment Handler
  const handleMarkPaid = (id: string) => {
    const item = queue.find(q => q.id === id);
    setQueue(prev => prev.map(item => item.id === id ? { ...item, paymentStatus: "PAID" } : item));
    if (item) {
      try {
        fetch("http://localhost:8000/api/v1/billing/invoices", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            mrn: item.mrn,
            patientName: item.patientName,
            amount: item.feeAmount,
            department: "Integrative Unani OPD",
            paymentMethod: "UPI"
          })
        }).catch(() => {});
      } catch (e) {}
    }
  };

  // Call Patient Trigger
  const handleCallPatient = (item: ReceptionQueueItem) => {
    setCallNotice(`📢 Calling Token ${item.tokenNumber}: ${item.patientName} to ${item.opdRoom} (${item.assignedDoctor})`);
    setTimeout(() => setCallNotice(null), 5000);
  };

  // Register New Patient Submit
  const handleRegisterSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPatient.fullName.trim() || !newPatient.mobile.trim()) return;

    const nextTokenNum = 100 + queue.length + 1;
    const tokenStr = `T-${nextTokenNum}`;
    const mrnStr = `MRN-2026-${Math.floor(1000 + Math.random() * 9000)}`;

    const roomMap: Record<string, string> = {
      "Prof. (Dr.) Mansoor Alam": "OPD Room 3",
      "Dr. Aisha Siddiqui": "OPD Room 2",
      "Dr. Tariq Zafar": "OPD Room 1",
      "Dr. Shagufta Parveen": "OPD Room 4"
    };

    const newItem: ReceptionQueueItem = {
      id: `Q-${nextTokenNum}`,
      tokenNumber: tokenStr,
      mrn: mrnStr,
      patientName: newPatient.fullName,
      age: Number(newPatient.age),
      gender: newPatient.gender,
      phone: newPatient.mobile,
      arrivalTime: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      acuity: newPatient.acuity,
      chiefComplaint: newPatient.chiefComplaint || "General consultation",
      assignedDoctor: newPatient.doctor,
      opdRoom: roomMap[newPatient.doctor] || "OPD Room 1",
      status: "WAITING",
      feeAmount: newPatient.feeAmount,
      paymentStatus: "PAID"
    };

    // Synchronize walk-in patient with live database API
    try {
      fetch("http://localhost:8000/api/v1/patients", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firstName: newPatient.fullName.split(" ")[0] || "Walk-in",
          lastName: newPatient.fullName.split(" ").slice(1).join(" ") || "Patient",
          phone: newPatient.mobile,
          gender: newPatient.gender
        })
      }).catch(() => {});

      fetch("http://localhost:8000/api/v1/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patientName: newPatient.fullName,
          mrn: mrnStr,
          doctorName: newPatient.doctor,
          chiefComplaint: newPatient.chiefComplaint || "General consultation",
          fee: newPatient.feeAmount
        })
      }).catch(() => {});
    } catch (e) {}

    setQueue([newItem, ...queue]);
    setShowRegModal(false);
    setNewPatient({
      fullName: "",
      mobile: "",
      age: 35,
      gender: "Male",
      doctor: "Prof. (Dr.) Mansoor Alam",
      chiefComplaint: "",
      acuity: "STANDARD",
      feeAmount: 800
    });
    setCallNotice(`✓ Patient Registered: ${newItem.patientName} (${tokenStr}) added to live queue.`);
    setTimeout(() => setCallNotice(null), 4000);
  };

  // Filtered Queue
  const filteredQueue = queue.filter(item => {
    const matchesAcuity = filterAcuity === "ALL" || item.acuity === filterAcuity;
    const matchesSearch = searchQuery === "" ||
      item.patientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.mrn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.tokenNumber.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesAcuity && matchesSearch;
  });

  const waitingCount = queue.filter(q => q.status === "WAITING").length;
  const inConsultCount = queue.filter(q => q.status === "IN_CONSULTATION").length;
  const completedCount = queue.filter(q => q.status === "COMPLETED").length;
  const totalRevenue = queue.filter(q => q.paymentStatus === "PAID").reduce((sum, q) => sum + q.feeAmount, 0);

  return (
    <AppShell activeRole="clinic">
      <div className="space-y-6 max-w-7xl mx-auto pb-12 text-slate-100">
        
        {/* Reception Header & Broadcast Notice */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">🏥</span>
              <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Central OPD Reception Desk
              </span>
              <span className="text-xs text-slate-400 font-mono">• Jamia Hamdard AUTC Main Hospital</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Patient Queue & Reception Workspace
            </h1>
            <p className="text-xs text-slate-400">
              Real-time OPD check-in, token triage, doctor room allocation, fee collection, and follow-up scheduling.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => setShowRegModal(true)}
              className="px-5 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold transition shadow-lg shadow-teal-900/30 flex items-center gap-2"
            >
              <span>+</span> Register New Patient (Token)
            </button>
          </div>
        </div>

        {/* Live Audio Call Alert */}
        {callNotice && (
          <div className="p-4 rounded-2xl bg-teal-950/80 border border-teal-500/60 text-teal-200 text-xs flex items-center justify-between shadow-lg animate-fade-in">
            <div className="flex items-center gap-3">
              <span className="text-lg animate-pulse">🔊</span>
              <span className="font-semibold">{callNotice}</span>
            </div>
            <button onClick={() => setCallNotice(null)} className="text-teal-400 hover:text-white">✕</button>
          </div>
        )}

        {/* Executive KPI Summary */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard label="Waiting in Lobby" value={`${waitingCount} Patients`} subtext="Average wait: 14 mins" variant="teal" icon="⏳" />
          <StatCard label="In Consultation" value={`${inConsultCount} Active`} subtext="Across 4 OPD Rooms" variant="emerald" icon="🩺" />
          <StatCard label="Completed Today" value={`${completedCount} Visits`} subtext="Since 09:00 AM" variant="blue" icon="✓" />
          <StatCard label="OPD Fees Collected" value={`₹${totalRevenue.toLocaleString()}`} subtext="100% Reconciled" variant="amber" icon="💳" />
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-slate-800 flex gap-2">
          {[
            { id: "queue", label: "Live Queue & Triage", icon: "👥" },
            { id: "roster", label: "Doctor Availability Roster", icon: "🩺" },
            { id: "billing", label: "Fee Collection & Receipts", icon: "💳" },
            { id: "followup", label: "Follow-up Scheduling", icon: "🔄" },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-xl transition ${
                activeTab === tab.id
                  ? "bg-teal-950/80 text-teal-300 border border-teal-600/50 shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-slate-800/40"
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* TAB 1: LIVE QUEUE & TRIAGE */}
        {activeTab === "queue" && (
          <div className="space-y-4 animate-fade-in text-xs">
            
            {/* Search & Filter Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-900/80 p-4 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 flex-1 max-w-md">
                <span className="text-slate-500">🔍</span>
                <input
                  type="text"
                  placeholder="Search by Patient Name, MRN, or Token (e.g. T-104)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-transparent text-xs text-white placeholder-slate-500 focus:outline-none"
                />
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[11px] text-slate-400">Acuity Filter:</span>
                {["ALL", "URGENT", "STANDARD", "FOLLOWUP"].map(acuity => (
                  <button
                    key={acuity}
                    onClick={() => setFilterAcuity(acuity)}
                    className={`px-3 py-1 rounded-lg text-[11px] font-semibold transition ${
                      filterAcuity === acuity
                        ? "bg-teal-600 text-white"
                        : "bg-slate-800 text-slate-400 hover:text-white"
                    }`}
                  >
                    {acuity}
                  </button>
                ))}
              </div>
            </div>

            {/* Queue Table */}
            <div className="bg-[#0F172A] border border-slate-800 rounded-3xl overflow-hidden shadow-lg">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-900/90 border-b border-slate-800 text-slate-400 font-semibold text-[11px]">
                      <th className="p-4">Token</th>
                      <th className="p-4">Patient & MRN</th>
                      <th className="p-4">Arrival / Acuity</th>
                      <th className="p-4">Chief Complaint</th>
                      <th className="p-4">Doctor & Room</th>
                      <th className="p-4">Status</th>
                      <th className="p-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-200">
                    {filteredQueue.map(item => (
                      <tr key={item.id} className="hover:bg-slate-800/30 transition">
                        <td className="p-4">
                          <span className="font-mono text-sm font-extrabold text-teal-400 bg-teal-950/60 px-2.5 py-1 rounded-lg border border-teal-800/60">
                            {item.tokenNumber}
                          </span>
                        </td>
                        <td className="p-4">
                          <div className="font-bold text-white text-xs">{item.patientName}</div>
                          <div className="text-[11px] text-slate-400 font-mono">{item.mrn} • {item.gender}, {item.age} yrs</div>
                        </td>
                        <td className="p-4">
                          <div className="text-slate-300 font-medium">{item.arrivalTime}</div>
                          <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.acuity === "URGENT"
                              ? "bg-rose-950 text-rose-300 border border-rose-800"
                              : item.acuity === "FOLLOWUP"
                              ? "bg-blue-950 text-blue-300 border border-blue-800"
                              : "bg-slate-800 text-slate-400"
                          }`}>
                            {item.acuity}
                          </span>
                        </td>
                        <td className="p-4 max-w-xs text-slate-300 truncate" title={item.chiefComplaint}>
                          {item.chiefComplaint}
                        </td>
                        <td className="p-4">
                          <div className="font-medium text-white">{item.assignedDoctor}</div>
                          <span className="text-[11px] text-teal-400">{item.opdRoom}</span>
                        </td>
                        <td className="p-4">
                          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                            item.status === "IN_CONSULTATION"
                              ? "bg-amber-950 text-amber-300 border border-amber-800 animate-pulse"
                              : item.status === "WAITING"
                              ? "bg-teal-950 text-teal-300 border border-teal-800"
                              : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                          }`}>
                            {item.status.replace("_", " ")}
                          </span>
                        </td>
                        <td className="p-4 text-right space-x-1.5 whitespace-nowrap">
                          {item.status === "WAITING" && (
                            <>
                              <button
                                onClick={() => handleCallPatient(item)}
                                className="px-2.5 py-1 rounded-lg bg-teal-600 hover:bg-teal-500 text-white font-semibold text-[11px]"
                                title="Call patient to room"
                              >
                                🔊 Call
                              </button>
                              <button
                                onClick={() => handleUpdateStatus(item.id, "IN_CONSULTATION")}
                                className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold text-[11px] border border-slate-700"
                              >
                                Start Consult
                              </button>
                            </>
                          )}
                          {item.status === "IN_CONSULTATION" && (
                            <button
                              onClick={() => handleUpdateStatus(item.id, "COMPLETED")}
                              className="px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-[11px]"
                            >
                              ✓ Check-Out
                            </button>
                          )}
                          {item.status === "COMPLETED" && (
                            <span className="text-slate-500 text-[11px] font-medium">Encounter Done</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: DOCTOR AVAILABILITY ROSTER */}
        {activeTab === "roster" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in text-xs">
            {DOCTOR_ROSTER.map(doc => (
              <div key={doc.id} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-white text-sm">{doc.name}</h3>
                    <p className="text-teal-400 text-[11px]">{doc.specialty}</p>
                    <span className="text-slate-400 font-mono text-[11px] block mt-0.5">{doc.room}</span>
                  </div>
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                    doc.status === "BUSY"
                      ? "bg-amber-950 text-amber-300 border border-amber-800"
                      : doc.status === "ACTIVE"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                      : "bg-slate-800 text-slate-400"
                  }`}>
                    {doc.status === "BUSY" ? "In Consultation" : doc.status === "ACTIVE" ? "Available" : "Break"}
                  </span>
                </div>

                <div className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-slate-300 space-y-1">
                  <div><strong>Current Status:</strong> {doc.currentPatient}</div>
                  <div><strong>Next Free Appointment Window:</strong> <span className="text-teal-300 font-semibold">{doc.nextSlot}</span></div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setNewPatient(prev => ({ ...prev, doctor: doc.name }));
                      setShowRegModal(true);
                    }}
                    className="flex-1 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-[11px] transition"
                  >
                    Assign Patient to {doc.room}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* TAB 3: FEE COLLECTION & RECEIPTS */}
        {activeTab === "billing" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">OPD Registration & Consultation Billing</h3>
                <p className="text-slate-400 text-[11px]">Instant receipt generation, UPI QR settlements, and cash reconciliation.</p>
              </div>
              <span className="text-emerald-400 font-mono font-bold text-sm">
                Total Today: ₹{totalRevenue.toLocaleString()}
              </span>
            </div>

            <div className="space-y-3">
              {queue.map(item => (
                <div key={item.id} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-teal-400 font-bold">{item.tokenNumber}</span>
                      <span className="text-slate-600">•</span>
                      <span className="font-bold text-white">{item.patientName} ({item.mrn})</span>
                    </div>
                    <p className="text-slate-400 text-[11px]">Assigned to {item.assignedDoctor} • {item.opdRoom}</p>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <span className="font-mono text-sm font-bold text-white">₹{item.feeAmount}</span>
                      <span className={`block text-[10px] font-bold ${
                        item.paymentStatus === "PAID" ? "text-emerald-400" : "text-amber-400"
                      }`}>
                        {item.paymentStatus}
                      </span>
                    </div>

                    {item.paymentStatus === "PENDING" ? (
                      <button
                        onClick={() => handleMarkPaid(item.id)}
                        className="px-3.5 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                      >
                        Collect ₹{item.feeAmount} (Cash / UPI)
                      </button>
                    ) : (
                      <button
                        onClick={() => alert(`Printing official OPD Receipt for ${item.patientName} (${item.tokenNumber})`)}
                        className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700"
                      >
                        Print Receipt 🖨️
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: FOLLOW-UP SCHEDULING */}
        {activeTab === "followup" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Patient Follow-up & Re-visit Booking</h3>
              <p className="text-slate-400 text-[11px]">Schedule Day +7 or Day +14 reviews directly at the checkout desk.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-3">
                <h4 className="font-bold text-teal-300">Quick 1-Click Re-visit Booker</h4>
                <div className="space-y-2">
                  <label className="block text-slate-400">Select Patient from Today's Queue</label>
                  <select className="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white">
                    {queue.map(q => (
                      <option key={q.id} value={q.id}>{q.tokenNumber}: {q.patientName} ({q.assignedDoctor})</option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  <button onClick={() => alert("Scheduled Day +7 Follow-up with WhatsApp alert!")} className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-center">
                    +7 Days (Sep 20)
                  </button>
                  <button onClick={() => alert("Scheduled Day +14 Follow-up with WhatsApp alert!")} className="p-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-center">
                    +14 Days (Sep 27)
                  </button>
                  <button onClick={() => alert("Scheduled Day +28 Follow-up with WhatsApp alert!")} className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-center">
                    +28 Days (Oct 11)
                  </button>
                </div>
              </div>

              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
                <h4 className="font-bold text-teal-300">Automatic Notification Dispatch</h4>
                <p className="text-slate-400 leading-relaxed text-[11px]">
                  When a follow-up is confirmed, ZAYVORA OS automatically dispatches:
                </p>
                <ul className="list-disc pl-5 space-y-1 text-slate-300 text-[11px]">
                  <li>WhatsApp Appointment Confirmation with Google Maps navigation pin</li>
                  <li>SMS reminder 24 hours prior to scheduled review slot</li>
                  <li>In-app alert in the patient's Personal Health Record (PHR) portal</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* MODAL: REGISTER NEW PATIENT */}
        {showRegModal && (
          <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-[#0F172A] border border-slate-700 rounded-3xl p-6 max-w-lg w-full space-y-4 shadow-2xl text-xs">
              <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-teal-400 text-base">📋</span>
                  <h3 className="text-sm font-bold text-white">OPD Patient Registration & Token Allocation</h3>
                </div>
                <button onClick={() => setShowRegModal(false)} className="text-slate-400 hover:text-white text-lg">✕</button>
              </div>

              <form onSubmit={handleRegisterSubmit} className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 mb-1">Full Legal Name *</label>
                    <input
                      type="text"
                      placeholder="e.g. Tariq Ansari"
                      value={newPatient.fullName}
                      onChange={(e) => setNewPatient({ ...newPatient, fullName: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-slate-300 mb-1">Mobile Number *</label>
                    <input
                      type="tel"
                      placeholder="+91-9876543210"
                      value={newPatient.mobile}
                      onChange={(e) => setNewPatient({ ...newPatient, mobile: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-teal-500"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 mb-1">Age</label>
                    <input
                      type="number"
                      value={newPatient.age}
                      onChange={(e) => setNewPatient({ ...newPatient, age: Number(e.target.value) })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-slate-300 mb-1">Gender</label>
                    <select
                      value={newPatient.gender}
                      onChange={(e) => setNewPatient({ ...newPatient, gender: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                    >
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 mb-1">Assign Clinician & Room</label>
                  <select
                    value={newPatient.doctor}
                    onChange={(e) => setNewPatient({ ...newPatient, doctor: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                  >
                    <option value="Prof. (Dr.) Mansoor Alam">Prof. (Dr.) Mansoor Alam — OPD Room 3 (Joints & Metabolic)</option>
                    <option value="Dr. Aisha Siddiqui">Dr. Aisha Siddiqui — OPD Room 2 (Preventive & Lifestyle)</option>
                    <option value="Dr. Tariq Zafar">Dr. Tariq Zafar — OPD Room 1 (Tadbeer & Musculoskeletal)</option>
                    <option value="Dr. Shagufta Parveen">Dr. Shagufta Parveen — OPD Room 4 (Women's Health)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 mb-1">Chief Symptoms</label>
                  <input
                    type="text"
                    placeholder="e.g. Knee swelling, morning joint stiffness..."
                    value={newPatient.chiefComplaint}
                    onChange={(e) => setNewPatient({ ...newPatient, chiefComplaint: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 mb-1">Triage Acuity</label>
                    <select
                      value={newPatient.acuity}
                      onChange={(e) => setNewPatient({ ...newPatient, acuity: e.target.value as any })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                    >
                      <option value="STANDARD">Standard OPD</option>
                      <option value="URGENT">Urgent (Priority Triage)</option>
                      <option value="FOLLOWUP">Routine Follow-up</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-300 mb-1">OPD Registration Fee</label>
                    <input
                      type="number"
                      value={newPatient.feeAmount}
                      onChange={(e) => setNewPatient({ ...newPatient, feeAmount: Number(e.target.value) })}
                      className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white"
                    />
                  </div>
                </div>

                <div className="flex gap-2 pt-3 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setShowRegModal(false)}
                    className="flex-1 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold hover:bg-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold"
                  >
                    Confirm & Issue Token
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
