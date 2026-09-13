"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { CLINICAL_FACULTY } from "@/lib/cms/doctorsData";
import { CANONICAL_PRODUCTS } from "@/lib/cms/productsData";
import { CLINICAL_PROGRAMS } from "@/lib/cms/programsData";

type AdminSection =
  | "overview"
  | "clinics"
  | "doctors"
  | "staff"
  | "patients"
  | "appointments"
  | "billing"
  | "inventory"
  | "products"
  | "programs"
  | "reports"
  | "communications"
  | "knowledge"
  | "analytics"
  | "permissions"
  | "audit"
  | "settings";

export default function AdminWorkspacePage() {
  const [activeTab, setActiveTab] = useState<AdminSection>("overview");
  const [actionNotice, setActionNotice] = useState<string | null>(null);

  // Trigger quick action feedback
  const triggerAction = (name: string) => {
    setActionNotice(`Executing Admin Operation: ${name}`);
    setTimeout(() => setActionNotice(null), 3500);
  };

  // Mock Merkle Blocks for 21 CFR Part 11
  const merkleLogs = [
    {
      blockNumber: 44102,
      timestamp: "2026-09-13T10:30:00Z",
      leafHash: "731f5cf53472e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495",
      eventType: "PRESCRIPTION_LOCKED",
      signer: "Prof. (Dr.) Mansoor Alam (CCIM-U-1988-0412)",
      status: "ANCHORED",
    },
    {
      blockNumber: 44101,
      timestamp: "2026-09-13T10:15:22Z",
      leafHash: "8f4b29c91a03e147b2c9d01248a0f9b3e217c49b01538a7c29b0134f59c14820",
      eventType: "CLINICAL_SOAP_ANCHORED",
      signer: "Prof. (Dr.) Mansoor Alam (CCIM-U-1988-0412)",
      status: "ANCHORED",
    },
    {
      blockNumber: 44100,
      timestamp: "2026-09-13T09:50:11Z",
      leafHash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      eventType: "MUDABBAR_CERTIFICATE_VERIFIED",
      signer: "Pharmacist Zainab Ali (PB-PHARM-2015-8812)",
      status: "ANCHORED",
    },
  ];

  // Facilities
  const facilities = [
    { id: "FAC-HQ-01", name: "Jamia Hamdard AUTC - Main Hospital", code: "JH-AUTC", activeDoctors: 12, activeBeds: 45, status: "Operational" },
    { id: "FAC-HQ-02", name: "National Institute of Integrative Medicine (NIIM)", code: "NIIM-DELHI", activeDoctors: 6, activeBeds: 20, status: "Operational" },
    { id: "FAC-HQ-03", name: "ZAYVORA Regional Matab & Regimenal Centre", code: "ZYV-HYD", activeDoctors: 4, activeBeds: 12, status: "Operational" }
  ];

  // Staff Directory
  const staffMembers = [
    { id: "STF-101", name: "Irfan Ashraf", role: "Super Administrator", email: "admin@zayvora.health", facility: "Central HQ", status: "Active" },
    { id: "STF-102", name: "Zainab Ali", role: "Chief Pharmacist", email: "zainab.pharm@zayvora.health", facility: "Central Dispensary", status: "Active" },
    { id: "STF-103", name: "Tariq Ansari", role: "Receptionist / OPD Coordinator", email: "reception.opd@zayvora.health", facility: "Jamia Hamdard AUTC", status: "Active" },
    { id: "STF-104", name: "Sameena Khan", role: "Clinical Care Coordinator (Nurse)", email: "sameena.nurse@zayvora.health", facility: "Jamia Hamdard AUTC", status: "Active" },
  ];

  const navItems: Array<{ id: AdminSection; label: string; icon: string }> = [
    { id: "overview", label: "System Overview", icon: "📊" },
    { id: "clinics", label: "Clinics & Facilities", icon: "🏥" },
    { id: "doctors", label: "Clinicians & Faculty", icon: "🩺" },
    { id: "staff", label: "Staff & Users", icon: "👥" },
    { id: "patients", label: "Patient Directory (MPI)", icon: "👤" },
    { id: "appointments", label: "Appointment Operations", icon: "📅" },
    { id: "billing", label: "Revenue & Billing", icon: "💳" },
    { id: "inventory", label: "Dispensary Inventory", icon: "📦" },
    { id: "products", label: "Botanical Products", icon: "🌿" },
    { id: "programs", label: "Health Programs", icon: "📑" },
    { id: "reports", label: "Diagnostic Lab Reports", icon: "🧪" },
    { id: "communications", label: "QSURA Notification Gate", icon: "💬" },
    { id: "knowledge", label: "ZKB Pharmacopoeia", icon: "📚" },
    { id: "analytics", label: "Clinical & RWE Analytics", icon: "📈" },
    { id: "permissions", label: "RBAC Matrix", icon: "🛡️" },
    { id: "audit", label: "21 CFR Part 11 Audit", icon: "🔒" },
    { id: "settings", label: "System Settings", icon: "⚙️" },
  ];

  return (
    <AppShell activeRole="admin">
      <div className="space-y-6 max-w-7xl mx-auto pb-12 text-slate-100">
        
        {/* Top Admin Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-[#0C1524] via-[#101C30] to-[#152540] border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">🛡️</span>
              <span className="text-[11px] font-bold text-teal-400 uppercase tracking-widest bg-teal-950/80 px-3 py-1 rounded-full border border-teal-800/80">
                Enterprise SaaS Administration
              </span>
              <span className="text-xs text-slate-400 font-mono">• Multi-Tenant Healthcare OS</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mt-1">
              Hospital Operations & Governance Console
            </h1>
            <p className="text-xs text-slate-400">
              Complete administrative control over clinic tenancies, clinicians, patient registries, billing, inventory, and 21 CFR Part 11 audit trails.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <span className="px-3 py-1.5 rounded-xl bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-xs font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>All 6 Services Operational</span>
            </span>
          </div>
        </div>

        {/* Action Notice Toast */}
        {actionNotice && (
          <div className="p-4 rounded-2xl bg-teal-950/80 border border-teal-500/60 text-teal-200 text-xs flex items-center justify-between shadow-lg animate-fade-in">
            <div className="flex items-center gap-3">
              <span className="text-base font-bold">⚡</span>
              <span>{actionNotice}</span>
            </div>
            <button onClick={() => setActionNotice(null)} className="text-teal-400 hover:text-white">✕</button>
          </div>
        )}

        {/* 8 Admin KPI Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard label="Total Patients" value="1,248" subtext="+12.4% MoM • 100% ABDM Linked" variant="teal" icon="👥" />
          <StatCard label="New Patients (Week)" value="38" subtext="Verified registrations" variant="blue" icon="👤" />
          <StatCard label="Appointments Today" value="28" subtext="8 Completed • 4 Active" variant="emerald" icon="📅" />
          <StatCard label="Active Doctors" value="18" subtext="Board-Certified Tabeebs" variant="teal" icon="🩺" />
          <StatCard label="Today's Revenue" value="₹38,450" subtext="OPD & Dispensary settled" variant="amber" icon="💳" />
          <StatCard label="Pending Payments" value="₹3,200" subtext="4 Invoices in review" variant="blue" icon="⏳" />
          <StatCard label="Inventory Alerts" value="2 Items" subtext="Near reorder threshold" variant="amber" icon="📦" />
          <StatCard label="System Alerts" value="0 Critical" subtext="Merkle root validated" variant="emerald" icon="🔒" />
        </div>

        {/* 9 Admin Quick Actions */}
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Administrative Operations & Governance Actions
          </span>
          <div className="flex flex-wrap gap-2">
            {[
              { label: "+ Add Staff Member", action: "Add Staff Member" },
              { label: "Manage Roles & Permissions", action: "Manage Roles & Permissions" },
              { label: "Configure Appointment Slots", action: "Configure Appointment Slots" },
              { label: "Manage Clinic Facilities", action: "Manage Clinic Facilities" },
              { label: "Manage Health Programs", action: "Manage Health Programs" },
              { label: "Manage Botanical Products", action: "Manage Botanical Products" },
              { label: "Manage Website Content", action: "Manage Website Content" },
              { label: "View 21 CFR Audit Logs", action: "View 21 CFR Audit Logs" },
              { label: "Configure Notification Gateways", action: "Configure Notification Gateways" },
            ].map(item => (
              <button
                key={item.label}
                onClick={() => triggerAction(item.action)}
                className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-teal-950 hover:text-teal-300 hover:border-teal-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {/* 17 Navigable Modules Bar */}
        <div className="border-b border-slate-800 overflow-x-auto no-scrollbar flex gap-1 pb-1">
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex items-center gap-2 px-3 py-2 text-xs font-semibold whitespace-nowrap rounded-xl transition ${
                activeTab === item.id
                  ? "bg-teal-950/80 text-teal-300 border border-teal-600/50 shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-slate-800/40"
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>

        {/* ========================================================= */}
        {/* MODULE 1: SYSTEM OVERVIEW                                 */}
        {/* ========================================================= */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in text-xs">
            <div className="lg:col-span-2 space-y-4">
              <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 shadow-md">
                <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                  <h3 className="text-sm font-bold text-white">Registered Multi-Center Hospital Network</h3>
                  <span className="text-teal-400 font-semibold">3 Active Facilities</span>
                </div>
                <div className="space-y-3">
                  {facilities.map(f => (
                    <div key={f.id} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
                      <div>
                        <div className="font-bold text-white">{f.name}</div>
                        <div className="text-slate-400 text-[11px]">{f.code} • {f.activeDoctors} Attending Doctors • {f.activeBeds} Inpatient Beds</div>
                      </div>
                      <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                        {f.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Cryptographic Ledger Summary */}
              <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-3 shadow-md">
                <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                  <h3 className="text-sm font-bold text-white">21 CFR Part 11 Merkle Cryptographic Anchor</h3>
                  <StatusBadge status="Anchored" variant="verified" />
                </div>
                <p className="text-slate-400 leading-relaxed text-[11px]">
                  All clinical diagnoses, prescription locks, and Mudabbar batch verifications are hashed and chained in an immutable SHA-256 Merkle root to prevent retroactive tampering.
                </p>
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-[11px] text-teal-300 truncate">
                  Latest Merkle Root: a8b3d6e99b9bc060fb3591c27a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b
                </div>
              </div>
            </div>

            {/* Right Column: Platform Telemetry */}
            <div className="space-y-4">
              <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-3 shadow-md">
                <h3 className="text-sm font-bold text-white">Microservices Health</h3>
                <div className="space-y-2">
                  {[
                    { name: "Clinical Service (FHIR R4)", status: "Healthy • 1.2ms" },
                    { name: "Therapeutic Engine (Mudabbar Gate)", status: "Healthy • 0.8ms" },
                    { name: "Identity & RBAC Service", status: "Healthy • 1.1ms" },
                    { name: "Hakeem Sahab AI Copilot", status: "Healthy • 12.4ms" },
                    { name: "Hardware & IoT Gateway", status: "Healthy • 100Hz Active" },
                    { name: "QSURA Notification Broker", status: "Healthy • 0 Queue" },
                  ].map((s, idx) => (
                    <div key={idx} className="p-2.5 bg-slate-900 rounded-xl border border-slate-800 flex justify-between items-center text-[11px]">
                      <span className="text-slate-300 font-medium">{s.name}</span>
                      <span className="text-emerald-400 font-mono font-bold">✓ {s.status}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 2: CLINICS & FACILITIES                            */}
        {/* ========================================================= */}
        {activeTab === "clinics" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">Clinical Facilities & Multi-Tenant Partitioning</h3>
                <p className="text-slate-400 text-[11px]">Manage hospital physical addresses, bed counts, and clinical consultation suites.</p>
              </div>
              <button onClick={() => triggerAction("Add Facility")} className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold">
                + Add Facility
              </button>
            </div>

            <div className="space-y-3">
              {facilities.map(f => (
                <div key={f.id} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h4 className="font-bold text-white text-sm">{f.name}</h4>
                    <p className="text-slate-400 text-[11px]">Facility ID: {f.id} • Code: {f.code}</p>
                    <span className="text-teal-400 text-[11px]">{f.activeDoctors} Practicing Specialists • {f.activeBeds} Inpatient Beds</span>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => triggerAction(`Configure ${f.name}`)} className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700">
                      Configure Rooms
                    </button>
                    <button onClick={() => triggerAction(`View Schedule ${f.name}`)} className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700">
                      Doctor Schedule
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 3: DOCTORS & FACULTY                               */}
        {/* ========================================================= */}
        {activeTab === "doctors" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">Board-Certified Clinical Faculty Directory</h3>
                <p className="text-slate-400 text-[11px]">Verified registrations under Central Council of Indian Medicine (CCIM) / NCISM.</p>
              </div>
              <button onClick={() => triggerAction("Onboard Clinician")} className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold">
                + Onboard New Clinician
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {CLINICAL_FACULTY.map(doc => (
                <div key={doc.id} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-bold text-white text-sm">{doc.name}</h4>
                      <p className="text-teal-400 text-[11px]">{doc.title}</p>
                      <span className="text-slate-400 text-[10px] font-mono">{doc.registration}</span>
                    </div>
                    <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                      Verified
                    </span>
                  </div>
                  <p className="text-slate-300 text-[11px]">{doc.degrees} • {doc.experienceYears}+ years experience</p>
                  <p className="text-slate-400 text-[11px]">OPD Hours: {doc.opdSchedule}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 4: STAFF & USERS                                   */}
        {/* ========================================================= */}
        {activeTab === "staff" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">Administrative & Clinical Support Staff</h3>
                <p className="text-slate-400 text-[11px]">Role assignment, credentialing, and multi-facility access controls.</p>
              </div>
              <button onClick={() => triggerAction("Invite Staff Member")} className="px-4 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold">
                + Add Staff Member
              </button>
            </div>

            <div className="space-y-3">
              {staffMembers.map(staff => (
                <div key={staff.id} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <div className="font-bold text-white">{staff.name}</div>
                    <div className="text-slate-400 text-[11px]">{staff.role} • {staff.email}</div>
                    <span className="text-teal-400 text-[10px]">{staff.facility}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                      {staff.status}
                    </span>
                    <button onClick={() => triggerAction(`Edit Permissions for ${staff.name}`)} className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] border border-slate-700">
                      Edit Roles
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 5: MASTER PATIENT INDEX (MPI)                      */}
        {/* ========================================================= */}
        {activeTab === "patients" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Master Patient Index (MPI) & ABHA Registry</h3>
                <p className="text-slate-400 text-[11px]">1,248 enrolled patients with ABDM health record linkages.</p>
              </div>
            </div>

            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <div className="font-bold text-white">Hamza Farooqi</div>
                <div className="text-slate-400 text-[11px]">MRN-2026-0814 • ABHA: 91-1234-5678-9012 • Balghami (Cold & Moist)</div>
                <span className="text-teal-300 text-[11px]">Condition: Waja-ul-Mafasil Barid Balghami • Stage 2 Tanqiya</span>
              </div>
              <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                Active Care Plan
              </span>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 6: APPOINTMENT OPERATIONS                          */}
        {/* ========================================================= */}
        {activeTab === "appointments" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">OPD Slot Configuration & Doctor Rosters</h3>
                <p className="text-slate-400 text-[11px]">Manage clinic working hours, holiday schedules, and teleconsultation bandwidth.</p>
              </div>
              <button onClick={() => triggerAction("Add Slot Configuration")} className="px-3 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold">
                Configure Slots
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800">
                <h4 className="font-bold text-white">OPD Shift Hours</h4>
                <p className="text-slate-400 text-[11px] mt-1">Morning OPD: 09:00 AM – 01:00 PM • Afternoon OPD: 02:30 PM – 05:30 PM</p>
              </div>
              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800">
                <h4 className="font-bold text-white">Teleconsultation HD Rooms</h4>
                <p className="text-slate-400 text-[11px] mt-1">4 encrypted WebRTC channels allocated with automatic call recording for 21 CFR compliance.</p>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 7: REVENUE & BILLING                               */}
        {/* ========================================================= */}
        {activeTab === "billing" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Hospital Financial Reconciliation</h3>
                <p className="text-slate-400 text-[11px]">Real-time OPD fees, herbal dispensary sales, and GST compliance.</p>
              </div>
              <span className="text-emerald-400 font-mono font-bold text-sm">Today: ₹38,450.00</span>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <div className="font-bold text-white">Daily Summary (Sep 13, 2026)</div>
                <div className="text-slate-400 text-[11px]">28 OPD Consultations (₹22,400) + 16 Dispensary Orders (₹16,050)</div>
              </div>
              <button onClick={() => triggerAction("Export GST Tally Report")} className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-teal-300 font-semibold border border-slate-700">
                Export GST Sheet 📥
              </button>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 8: DISPENSARY INVENTORY                            */}
        {/* ========================================================= */}
        {activeTab === "inventory" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Dispensary Stock & Cold-Chain Telemetry</h3>
                <p className="text-slate-400 text-[11px]">FEFO tracking, Mudabbar detoxification certificates, and temperature logs.</p>
              </div>
              <span className="text-teal-400 font-mono text-[11px]">Cold-Chain Chamber: 19.4°C • Stable</span>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">Majun Suranjan (Mudabbar)</span>
                <span className="text-amber-400 font-bold">29 Units Left (Reorder Warning)</span>
              </div>
              <div className="text-slate-400 text-[11px]">Batch MS-2026-LOT4 • Expiry: 2027-08-30 • Schedule E(1) Mudabbar Verified</div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 9: BOTANICAL PRODUCTS                              */}
        {/* ========================================================= */}
        {activeTab === "products" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3 flex justify-between items-center">
              <div>
                <h3 className="text-sm font-bold text-white">Canonical Formulations Catalog (10 Products)</h3>
                <p className="text-slate-400 text-[11px]">Categorized into Clinic Unani, Retail Unani, AYUSH, and FSSAI supplements.</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {CANONICAL_PRODUCTS.slice(0, 6).map(p => (
                <div key={p.id} className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <div className="font-bold text-white">{p.brandName}</div>
                    <div className="text-teal-400 text-[10px]">{p.category}</div>
                  </div>
                  <span className="font-mono text-white font-semibold">₹{p.price}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 10: HEALTH PROGRAMS                                */}
        {/* ========================================================= */}
        {activeTab === "programs" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Clinical Programs & Afaal Cascades</h3>
              <p className="text-slate-400 text-[11px]">6 specialized integrative chronic care pathways.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {CLINICAL_PROGRAMS.map(prog => (
                <div key={prog.id} className="p-3 bg-slate-900/80 rounded-xl border border-slate-800 space-y-1">
                  <h4 className="font-bold text-white">{prog.title}</h4>
                  <p className="text-teal-400 text-[10px]">{prog.duration} • {prog.category}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 11: DIAGNOSTIC LAB REPORTS                         */}
        {/* ========================================================= */}
        {activeTab === "reports" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Diagnostic Laboratory Integration</h3>
              <p className="text-slate-400 text-[11px]">Biochemistry, inflammatory panels (hs-CRP, ESR), and radiological imaging.</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <span className="font-bold text-white">Bilateral Knee Digital Radiography (AP/Lateral)</span>
                <p className="text-slate-400 text-[11px]">Hamza Farooqi (MRN-2026-0814) • Verified by Dr. Lal PathLabs</p>
              </div>
              <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                Normal Alignment
              </span>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 12: COMMUNICATIONS                                 */}
        {/* ========================================================= */}
        {activeTab === "communications" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">QSURA Multi-Channel Notification Broker</h3>
              <p className="text-slate-400 text-[11px]">Automated SMS, WhatsApp appointment confirmations, and voice posology dispatches.</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <span className="font-bold text-white">WhatsApp Clinical Dispatch Gateway</span>
                <p className="text-slate-400 text-[11px]">99.4% Delivery Success Rate • 1,420 notifications dispatched this month</p>
              </div>
              <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                Connected
              </span>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 13: KNOWLEDGE BASE                                 */}
        {/* ========================================================= */}
        {activeTab === "knowledge" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">ZAYVORA Knowledge Base (ZKB) Pharmacopoeia</h3>
              <p className="text-slate-400 text-[11px]">1,280+ codified monographs from Unani Pharmacopoeia of India (UPI) & NFUM.</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <span className="font-bold text-white">UPI Standardized Monograph: Colchicum luteum Baker (Suranjan Talkh)</span>
                <p className="text-slate-400 text-[11px]">Volume I, Page 84 • Schedule E(1) Mudabbar Detoxification Gate Active</p>
              </div>
              <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2.5 py-1 rounded-full text-[10px] font-bold">
                Approved
              </span>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 14: ANALYTICS & RWE                                */}
        {/* ========================================================= */}
        {activeTab === "analytics" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Real-World Evidence (RWE) Observational Registry</h3>
              <p className="text-slate-400 text-[11px]">Longitudinal PROMs data tracking WOMAC pain scores and glycemic reversal curves.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1">
                <span className="text-slate-400">Mean VAS Pain Score Reduction</span>
                <div className="text-2xl font-bold text-white font-mono">-68.75%</div>
                <span className="text-emerald-400 text-[11px]">Across 340 Knee Osteoarthritis patients</span>
              </div>
              <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1">
                <span className="text-slate-400">Multi-Center Clinical Concordance</span>
                <div className="text-2xl font-bold text-white font-mono">94.2%</div>
                <span className="text-teal-400 text-[11px]">Validated across 3 university teaching hospitals</span>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 15: RBAC PERMISSIONS MATRIX                        */}
        {/* ========================================================= */}
        {activeTab === "permissions" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Role-Based Access Control (RBAC) Hierarchy</h3>
              <p className="text-slate-400 text-[11px]">Strict data isolation ensuring patients only access their own records.</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center border-b border-slate-800 pb-2 font-semibold text-slate-300">
                <span>Role Name</span>
                <span>Permissions Tier</span>
              </div>
              {[
                { r: "Super Admin", p: "Platform wide: manage facilities, users, Merkle logs" },
                { r: "Clinic Admin", p: "Tenant level: staff management, slot configuration, billing" },
                { r: "Doctor / Senior Tabeeb", p: "Clinical workspace, 21 CFR prescription lock, Hakeem copilot" },
                { r: "Receptionist", p: "OPD queue management, patient registration, check-in, fee collection" },
                { r: "Pharmacist", p: "Prescription verification, Schedule E(1) gate, FEFO inventory allocation" },
                { r: "Patient", p: "Personal Health Record (PHR), appointment booking, report upload" }
              ].map((item, idx) => (
                <div key={idx} className="flex justify-between items-center text-[11px] py-1">
                  <span className="font-bold text-teal-300">{item.r}</span>
                  <span className="text-slate-400">{item.p}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 16: 21 CFR PART 11 AUDIT TRAIL                     */}
        {/* ========================================================= */}
        {activeTab === "audit" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">Immutable Merkle Audit Log (21 CFR Part 11)</h3>
              <p className="text-slate-400 text-[11px]">Cryptographically verified records of all clinical encounters and prescription locks.</p>
            </div>
            <div className="space-y-3">
              {merkleLogs.map(log => (
                <div key={log.blockNumber} className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="font-mono text-teal-400 font-bold">Block #{log.blockNumber}</span>
                    <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px] font-bold">
                      {log.status}
                    </span>
                  </div>
                  <div className="font-semibold text-white">{log.eventType}</div>
                  <div className="text-slate-400 text-[11px]">Signer: {log.signer} • {log.timestamp}</div>
                  <div className="font-mono text-[10px] text-slate-500 truncate pt-1">Leaf Hash: {log.leafHash}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================= */}
        {/* MODULE 17: SYSTEM SETTINGS                                */}
        {/* ========================================================= */}
        {activeTab === "settings" && (
          <div className="bg-[#0F172A] border border-slate-800 rounded-3xl p-6 space-y-4 animate-fade-in text-xs">
            <div className="border-b border-slate-800 pb-3">
              <h3 className="text-sm font-bold text-white">System Settings & Compliance Configuration</h3>
              <p className="text-slate-400 text-[11px]">Ayushman Bharat (ABDM) sandbox, database backup drills, and encryption keys.</p>
            </div>
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">ABDM M3 Milestone Certification</span>
                <span className="text-emerald-400 font-semibold">Active & Certified</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">Daily Disaster Recovery (DR) Snapshot</span>
                <span className="text-emerald-400 font-semibold">Verified Today (RTO &lt; 1h)</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-bold text-white">AES-256 GCM Cryptographic Storage</span>
                <span className="text-emerald-400 font-semibold">Enforced on all PHI</span>
              </div>
            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
