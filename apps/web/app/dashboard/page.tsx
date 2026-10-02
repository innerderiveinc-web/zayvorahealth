"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { PlatformHeader } from "@/components/PlatformHeader";
import { PlatformFooter } from "@/components/PlatformFooter";
import { loadSession, clearSession } from "@/lib/session";
import type { TokenResponse } from "@/lib/identityApi";
import { useAuth } from "@/lib/hooks/useAuth";
import { getRoleDashboard } from "@/lib/auth";

type DashboardRole = "doctor" | "admin" | "patient" | "pharmacist" | "receptionist";

type DashboardModuleTab = 
  | "clinical"
  | "therapeutic"
  | "operations"
  | "all";

export default function EnterpriseHealthDashboard() {
  const router = useRouter();
  const { role, isLoading: authLoading } = useAuth();
  const [session, setSession] = useState<TokenResponse | null>(null);

  // Redirect to role-specific panel immediately after auth resolves
  useEffect(() => {
    if (!authLoading && role) {
      const target = getRoleDashboard(role);
      if (target !== '/dashboard') {
        router.replace(target);
      }
    }
  }, [authLoading, role, router]);

  // Active Role View
  const [activeRole, setActiveRole] = useState<DashboardRole>("doctor");

  // Sidebar display mode: 'expanded' | 'collapsed' | 'mobile'
  const [sidebarMode, setSidebarMode] = useState<"expanded" | "collapsed" | "mobile">("expanded");
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  // Active in-dashboard section tab (Focus Mode)
  const [activeTab, setActiveTab] = useState<DashboardModuleTab>("clinical");

  // Interactive state
  const [appointmentFilter, setAppointmentFilter] = useState("today");
  const [patientFilter, setPatientFilter] = useState("all");
  const [acknowledgedAlerts, setAcknowledgedAlerts] = useState<number[]>([]);
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState<string | null>(null);
  const [aiError, setAiError] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [quickActionNotice, setQuickActionNotice] = useState<string | null>(null);

  // Load session
  useEffect(() => {
    setSession(loadSession());
  }, []);

  function handleQuickAction(actionName: string) {
    setQuickActionNotice(`Triggered: ${actionName}`);
    setTimeout(() => setQuickActionNotice(null), 3000);
  }

  function acknowledgeAlert(id: number) {
    setAcknowledgedAlerts((prev) => [...prev, id]);
  }

  // Ask Hakeem AI
  async function handleAskAi(customPrompt?: string) {
    const q = customPrompt || aiQuery;
    if (!q.trim()) return;
    setAiLoading(true);
    setAiResponse(null);
    setAiError(null);
    try {
      const res = await fetch("/api/v1/hakeem/consult", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q, mode: "copilot" }),
      });
      if (res.ok) {
        const data = await res.json();
        setAiResponse(data.summary || (typeof data === "string" ? data : JSON.stringify(data, null, 2)));
      } else {
        setAiError(`CDS Service returned HTTP ${res.status}. Clinical Decision Support Copilot is currently offline or unreachable.`);
      }
    } catch {
      setAiError("Unable to establish secure connection with ZAYVORA Clinical Inference Engine. Offline/fail-closed mode active.");
    } finally {
      setAiLoading(false);
    }
  }

  // 18 Sidebar Main Menu items
  const sidebarItems = [
    { id: "dashboard", label: "Dashboard", icon: "📊", tab: "all" },
    { id: "reception", label: "Reception & Queue", icon: "🛎️", href: "/receptionist" },
    { id: "patients", label: "Patients", icon: "👥", href: "/doctor/patients" },
    { id: "appointments", label: "Appointments", icon: "📅", href: "/doctor/calendar" },
    { id: "clinical", label: "Clinical Workspace", icon: "🩺", href: "/doctor" },
    { id: "ai_cds", label: "Hakeem Sahab AI™ — Clinical Decision Support", icon: "🤖", href: "/doctor/hakeem-sahab" },
    { id: "protocols", label: "ZAYVORA Protocols", icon: "📑", href: "/protocols" },
    { id: "prescriptions", label: "Prescriptions", icon: "📝", href: "/doctor/nuskha" },
    { id: "pharmacy", label: "Medicines / Pharmacy", icon: "💊", href: "/pharmacy" },
    { id: "diagnostics", label: "Diagnostics / Reports", icon: "🧪", href: "/doctor/reports" },
    { id: "treatment_plans", label: "Treatment Plans", icon: "🌿", href: "/doctor/organ-axis" },
    { id: "followups", label: "Follow-ups", icon: "🔄", href: "/doctor/follow-ups" },
    { id: "telemedicine", label: "Telemedicine", icon: "📱", href: "/telemedicine" },
    { id: "billing", label: "Billing & Payments", icon: "💳", href: "/billing" },
    { id: "analytics", label: "Analytics", icon: "📈", href: "/analytics" },
    { id: "knowledge", label: "Knowledge Base", icon: "📚", href: "/knowledge" },
    { id: "messages", label: "Messages", icon: "💬", href: "/messages" },
    { id: "notifications", label: "Notifications", icon: "🔔", href: "/notifications" },
    { id: "settings", label: "Settings", icon: "⚙️", href: "/settings" },
  ];

  // 6 KPI Summary Cards Data
  const kpiData = [
    { label: "Total Patients", value: "1,248", change: "+12.4%", trend: "up", sub: "Registered EMR profiles", icon: "👥" },
    { label: "Today's Appointments", value: "28", change: "+4 vs avg", trend: "up", sub: "8 Completed • 4 In Consult", icon: "📅" },
    { label: "Pending Follow-ups", value: "14", change: "6 Urgent", trend: "down", sub: "Requires WhatsApp/Call", icon: "🔄" },
    { label: "Active Treatment Plans", value: "89", change: "+7 this wk", trend: "up", sub: "24 in Phase 1 (Tanqiya)", icon: "🌿" },
    { label: "Today's Revenue", value: "₹54,200", change: "+18.2%", trend: "up", sub: "OPD Fees & Dispensary", icon: "💳" },
    { label: "Critical Alerts", value: "2", change: "Requires Action", trend: "alert", sub: "1 Drug Interaction • 1 Lab", icon: "⚠️" },
  ];

  // Appointments Data
  const appointments = [
    { id: "APT-801", patient: "Hamza Farooqi", pid: "MRN-2026-0814", time: "10:30 AM", type: "In-Person", doctor: "Dr. Irfan", status: "In Consultation" },
    { id: "APT-802", patient: "Ayesha Siddiqui", pid: "MRN-2026-0921", time: "11:15 AM", type: "Online (WebRTC)", doctor: "Dr. Irfan", status: "Waiting" },
    { id: "APT-803", patient: "Bilal Ahmad", pid: "MRN-2026-0744", time: "12:00 PM", type: "In-Person", doctor: "Dr. Irfan", status: "Confirmed" },
    { id: "APT-804", patient: "Fatima Noor", pid: "MRN-2026-1032", time: "02:30 PM", type: "Online (WebRTC)", doctor: "Dr. Irfan", status: "Confirmed" },
    { id: "APT-805", patient: "Zubair Khan", pid: "MRN-2026-0612", time: "03:15 PM", type: "In-Person", doctor: "Dr. Irfan", status: "Completed" },
  ];

  // Patients Data
  const patientsList = [
    { id: "MRN-2026-0814", name: "Hamza Farooqi", ageGender: "44 / M", complaint: "Knee arthralgia & morning stiffness", lastConsult: "Today", protocol: "Mafasil Reversal (Tanqiya)", nextFollowup: "2026-09-26", status: "Active" },
    { id: "MRN-2026-0921", name: "Ayesha Siddiqui", ageGender: "36 / F", complaint: "PCOS, follicular delay, fatigue", lastConsult: "3 days ago", protocol: "OvaSync Hormonal Reset", nextFollowup: "2026-09-18", status: "Observation" },
    { id: "MRN-2026-0744", name: "Bilal Ahmad", ageGender: "52 / M", complaint: "Metabolic syndrome, fatty liver", lastConsult: "1 week ago", protocol: "MetaboCore & Hepatic Priming", nextFollowup: "2026-09-22", status: "Active" },
    { id: "MRN-2026-1032", name: "Fatima Noor", ageGender: "29 / F", complaint: "Chronic migraine & non-REM insomnia", lastConsult: "Yesterday", protocol: "NeuroCalmX & Nasal Natool", nextFollowup: "2026-09-25", status: "Active" }
  ];

  // 9 Functional Axes
  const axesData = [
    { name: "Liver Axis (Kabid)", score: 72, risk: "Needs Attention", trend: "improving", protocol: "LiverPrime + Majun Dabeed", action: "Continue Munzij-e-Balgham" },
    { name: "Gut Axis (Mida)", score: 58, risk: "Moderate", trend: "stable", protocol: "Warm Anupan Dietetics", action: "Review bowel motility" },
    { name: "Metabolic Axis", score: 81, risk: "High Priority", trend: "improving", protocol: "MetaboCore Elite", action: "Fasting insulin recheck in 7d" },
    { name: "Stress / Sleep Axis (Dimagh)", score: 43, risk: "Stable", trend: "optimal", protocol: "NightOne X Restorative", action: "Maintain circadian timing" },
    { name: "Hormonal Axis", score: 65, risk: "Moderate", trend: "stable", protocol: "OvaSync Botanical", action: "Mid-cycle ultrasound follow-up" },
    { name: "Musculoskeletal Axis (Mafasil)", score: 78, risk: "Needs Attention", trend: "improving", protocol: "Habb-e-Suranjan + Natool", action: "Stage 2 Tahleel starting in 5d" },
    { name: "Reproductive Axis", score: 70, risk: "Moderate", trend: "improving", protocol: "ManiVital Pro Formula", action: "Semen analysis review in 30d" },
    { name: "Respiratory Axis (Riya)", score: 35, risk: "Optimal", trend: "optimal", protocol: "Hifz-e-Sehat Clean Air", action: "No intervention needed" },
    { name: "Renal Axis (Kulyah)", score: 40, risk: "Optimal", trend: "optimal", protocol: "Hydration & Arqiyat", action: "Normal eGFR > 90" }
  ];

  // Follow-up reminders
  const followupsList = [
    { patient: "Hamza Farooqi", due: "Today", reason: "Tanqiya Day 9 tolerance check", channel: "WhatsApp" },
    { patient: "Ayesha Siddiqui", due: "Tomorrow", reason: "Hormonal fasting blood sugar review", channel: "Call" },
    { patient: "Tariq Mehmood", due: "Overdue (2d)", reason: "Knee flexion range of motion test", channel: "SMS" },
  ];

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      {/* Top Header */}
      <PlatformHeader />

      {/* Main Content Area with Collapsible Sidebar */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Sidebar Navigation */}
        <aside
          className={`bg-[var(--panel)] border-r border-[var(--border)] flex flex-col transition-all duration-200 shrink-0 ${
            sidebarMode === "expanded" ? "w-64" : "w-16"
          } hidden md:flex`}
        >
          {/* Sidebar Toggle & Mode Selector */}
          <div className="p-3 border-b border-[var(--border)] flex items-center justify-between">
            {sidebarMode === "expanded" && (
              <span className="text-[10px] font-bold text-[var(--muted)] uppercase tracking-wider">
                Clinical Menu
              </span>
            )}
            <button
              onClick={() => setSidebarMode(sidebarMode === "expanded" ? "collapsed" : "expanded")}
              className="p-1 rounded-lg hover:bg-[var(--elevated)] text-[var(--muted)] hover:text-white transition"
              title="Toggle sidebar mode"
            >
              {sidebarMode === "expanded" ? "◀" : "▶"}
            </button>
          </div>

          {/* 18 Main Menu Items */}
          <nav className="p-2 space-y-0.5 flex-1 overflow-y-auto">
            {sidebarItems.map((item) => {
              const isActive = activeTab === item.tab;
              if (item.href) {
                return (
                  <Link
                    key={item.id}
                    href={item.href}
                    className="flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-[var(--muted)] hover:bg-[var(--elevated)] hover:text-white transition"
                    title={item.label}
                  >
                    <span className="text-base shrink-0">{item.icon}</span>
                    {sidebarMode === "expanded" && <span className="truncate">{item.label}</span>}
                  </Link>
                );
              }
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.tab as DashboardModuleTab)}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium transition text-left ${
                    isActive
                      ? "bg-[#0D9488]/20 text-[#2DD4BF] border border-[#0D9488]/40 shadow-xs font-semibold"
                      : "text-[var(--muted)] hover:bg-[var(--elevated)] hover:text-white"
                  }`}
                  title={item.label}
                >
                  <span className="text-base shrink-0">{item.icon}</span>
                  {sidebarMode === "expanded" && <span className="truncate">{item.label}</span>}
                </button>
              );
            })}
          </nav>

          {/* Sidebar Bottom Links */}
          <div className="p-2 border-t border-[var(--border)] bg-[var(--background)] space-y-0.5 text-xs">
            <Link href="/website/faqs" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>❓</span> {sidebarMode === "expanded" && <span>Help Center</span>}
            </Link>
            <Link href="/knowledge" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>📖</span> {sidebarMode === "expanded" && <span>Documentation</span>}
            </Link>
            <Link href="/admin" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>🟢</span> {sidebarMode === "expanded" && <span>System Status</span>}
            </Link>
            <Link href="/website/contact" className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-[var(--muted)] hover:text-white">
              <span>📞</span> {sidebarMode === "expanded" && <span>Contact Support</span>}
            </Link>
            <button onClick={() => { clearSession(); router.push("/"); }} className="w-full text-left flex items-center gap-2.5 px-3 py-1.5 rounded-lg text-rose-400 hover:bg-rose-500/10 font-semibold">
              <span>🚪</span> {sidebarMode === "expanded" && <span>Logout</span>}
            </button>
          </div>
        </aside>

        {/* Dashboard Workspace */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 space-y-8 bg-[var(--background)]">
          
          {/* Quick Action Toast Notice */}
          {quickActionNotice && (
            <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold flex items-center justify-between shadow-lg">
              <span>✓ {quickActionNotice}</span>
              <button onClick={() => setQuickActionNotice(null)}>✕</button>
            </div>
          )}

          {/* SECTION 3: Dashboard Welcome & Clinic Context Section */}
          <section className="p-6 rounded-3xl bg-gradient-to-r from-[#1E293B] via-[var(--panel)] to-[#0F172A] border border-[var(--border)] shadow-xl space-y-5">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 border-b border-[var(--border)] pb-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xl">☀️</span>
                  <h1 className="text-xl sm:text-2xl font-bold text-white">
                    Good Morning, Dr. Irfan
                  </h1>
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-bold border border-emerald-500/30">
                    Clinic Open
                  </span>
                </div>
                <p className="text-xs sm:text-sm text-[var(--muted)]">
                  Here is your clinical and operational overview for today.
                </p>
              </div>

              {/* Clinic Operational Metrics */}
              <div className="flex flex-wrap items-center gap-3 text-xs">
                <div className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                  <span className="text-[10px] text-[var(--muted)] block">Current Date</span>
                  <strong className="text-white font-mono">Sunday, 13 Sep 2026</strong>
                </div>
                <div className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                  <span className="text-[10px] text-[var(--muted)] block">Clinic Timing</span>
                  <strong className="text-[#2DD4BF] font-mono">09:00 AM – 06:00 PM</strong>
                </div>
                <div className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                  <span className="text-[10px] text-[var(--muted)] block">Current Shift</span>
                  <strong className="text-amber-300 font-mono">Morning OPD (General)</strong>
                </div>
              </div>
            </div>

            {/* Quick Action Buttons */}
            <div>
              <span className="text-[10px] font-bold text-[var(--muted)] uppercase tracking-wider block mb-2">
                Quick Actions
              </span>
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() => handleQuickAction("Add New Patient")}
                  className="px-3.5 py-2 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition shadow-sm"
                >
                  + Add New Patient
                </button>
                <button
                  onClick={() => handleQuickAction("Create Prescription")}
                  className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)] transition"
                >
                  📝 Create Prescription
                </button>
                <button
                  onClick={() => handleQuickAction("Start Consultation")}
                  className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)] transition"
                >
                  🩺 Start Consultation
                </button>
                <button
                  onClick={() => handleQuickAction("Book Appointment")}
                  className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)] transition"
                >
                  📅 Book Appointment
                </button>
                <button
                  onClick={() => { setActiveTab("clinical_ai"); handleQuickAction("Open Clinical Decision Support"); }}
                  className="px-3.5 py-2 rounded-xl bg-teal-500/20 text-teal-300 hover:bg-teal-500/30 text-xs font-semibold border border-teal-500/40 transition"
                >
                  🤖 Clinical Decision Support
                </button>
                <button
                  onClick={() => handleQuickAction("Add Medicine")}
                  className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)] transition"
                >
                  💊 Add Medicine
                </button>
                <button
                  onClick={() => handleQuickAction("Generate Report")}
                  className="px-3.5 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)] transition"
                >
                  📑 Generate Report
                </button>
              </div>
            </div>
          </section>

          {/* Role-Based Dashboard View Switcher */}
          {/* FOCUSED CLINICAL MODE SELECTOR (PROGRESSIVE DISCLOSURE) */}
          <div className="bg-[var(--panel)] border border-[var(--border)] rounded-2xl p-2.5 flex flex-wrap items-center justify-between gap-3 shadow-md">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-bold text-[var(--muted)] uppercase tracking-wider px-1">
                Clinical Focus:
              </span>
              
              <button
                onClick={() => setActiveTab("clinical")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition ${
                  activeTab === "clinical"
                    ? "bg-[#0D9488] text-white shadow-sm"
                    : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
                }`}
              >
                <span>🩺</span>
                <span>Daily Clinical OPD</span>
                <span className="text-[9px] px-1.5 py-0.5 rounded bg-black/25 text-[#A7F3D0] uppercase font-mono">Active OPD</span>
              </button>

              <button
                onClick={() => setActiveTab("therapeutic")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition ${
                  activeTab === "therapeutic"
                    ? "bg-[#0D9488] text-white shadow-sm"
                    : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
                }`}
              >
                <span>🌿</span>
                <span>9-Organ Axis & Living Plans</span>
              </button>

              <button
                onClick={() => setActiveTab("operations")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition ${
                  activeTab === "operations"
                    ? "bg-[#0D9488] text-white shadow-sm"
                    : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
                }`}
              >
                <span>💊</span>
                <span>Dispensary & Practice Ops</span>
              </button>

              <button
                onClick={() => setActiveTab("all")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition ${
                  activeTab === "all"
                    ? "bg-[#0D9488] text-white shadow-sm"
                    : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
                }`}
              >
                <span>🌐</span>
                <span>All Overview</span>
              </button>
            </div>

            {/* Quick Persona Navigation */}
            <div className="flex items-center gap-1.5 text-xs border-t lg:border-t-0 lg:border-l border-[var(--border)] pt-2 lg:pt-0 lg:pl-3 w-full lg:w-auto">
              <span className="text-[10px] text-[var(--muted)] uppercase font-semibold">Portal:</span>
              <button onClick={() => router.push("/doctor")} className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] text-[11px] text-white hover:border-[#2DD4BF] border border-transparent font-medium">Doctor Cockpit</button>
              <button onClick={() => router.push("/patient")} className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] text-[11px] text-white hover:border-[#2DD4BF] border border-transparent font-medium">Patient 360</button>
              <button onClick={() => router.push("/pharmacy")} className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] text-[11px] text-white hover:border-[#2DD4BF] border border-transparent font-medium">FEFO Pharmacy</button>
              <button onClick={() => router.push("/receptionist")} className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] text-[11px] text-white hover:border-[#2DD4BF] border border-transparent font-medium">Reception</button>
            </div>
          </div>

          {/* SECTION 4: KPI Cards / Summary Cards (Always visible on first screen) */}
          <section className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {kpiData.map((kpi) => (
              <div
                key={kpi.label}
                className="p-4 rounded-2xl bg-[var(--panel)] border border-[var(--border)] hover:border-[#2DD4BF]/40 transition space-y-2 flex flex-col justify-between"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xl">{kpi.icon}</span>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded font-mono ${
                    kpi.trend === "up" ? "bg-emerald-500/20 text-emerald-400" :
                    kpi.trend === "alert" ? "bg-rose-500/20 text-rose-300 animate-pulse" :
                    "bg-amber-500/20 text-amber-300"
                  }`}>
                    {kpi.change}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-[var(--muted)] block">{kpi.label}</span>
                  <span className="text-2xl font-extrabold text-white">{kpi.value}</span>
                  <span className="text-[10px] text-[#64748B] block mt-0.5 truncate">{kpi.sub}</span>
                </div>
                <button
                  onClick={() => handleQuickAction(`Inspect ${kpi.label}`)}
                  className="text-[10px] text-teal-400 hover:text-white font-semibold flex items-center gap-1 pt-1 border-t border-[var(--border)]"
                >
                  View Details →
                </button>
              </div>
            ))}
          </section>

          {/* SECTION 7 & 17: Clinical Safety Alerts & Critical Notices */}
          <section className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1.5">
                <span>⚠️</span> Clinical Safety Interceptions & Alerts (2 Active)
              </span>
              <span className="text-[11px] text-[var(--muted)]">Mandatory Physician Review Required</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {!acknowledgedAlerts.includes(1) && (
                <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-xs space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold text-[10px]">
                      DRUG / HERB INTERACTION WARNING
                    </span>
                    <button
                      onClick={() => acknowledgeAlert(1)}
                      className="text-[10px] px-2 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 font-bold"
                    >
                      Acknowledge & Sign
                    </button>
                  </div>
                  <h4 className="font-bold text-white">Azaraqi (Mudabbar) + Concomitant Sedative Therapy</h4>
                  <p className="text-[11px] text-rose-200/80 leading-relaxed">
                    Patient Hamza Farooqi (MRN-2026-0814): Azaraqi must not be co-administered with high-dose CNS depressants without 6-hour spacing and Kateera Musleh corrective.
                  </p>
                </div>
              )}

              {!acknowledgedAlerts.includes(2) && (
                <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-xs space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold text-[10px]">
                      ABNORMAL DIAGNOSTIC VALUE
                    </span>
                    <button
                      onClick={() => acknowledgeAlert(2)}
                      className="text-[10px] px-2 py-1 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 font-bold"
                    >
                      Acknowledge
                    </button>
                  </div>
                  <h4 className="font-bold text-white">Elevated Serum Uric Acid (8.4 mg/dL)</h4>
                  <p className="text-[11px] text-amber-200/80 leading-relaxed">
                    Patient Bilal Ahmad (MRN-2026-0744): Uric acid elevated. Consider Suranjan Talkh Mudabbar titration and avoid Purine-heavy mutton broths.
                  </p>
                </div>
              )}
            </div>
          </section>

          {/* SECTION 5 & 8: Priority Split - Today's Appointments & Hakeem Sahab AI */}
          {(activeTab === "clinical" || activeTab === "all") && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Today's Appointments Widget (7 cols) */}
            <div className="lg:col-span-7 p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                <div>
                  <h3 className="text-base font-bold text-white">Today's Scheduled Consultations</h3>
                  <p className="text-xs text-[var(--muted)]">Live appointment triage and room check-in status</p>
                </div>
                
                {/* Appointment Filters */}
                <div className="flex flex-wrap items-center gap-1 bg-[var(--background)] p-1 rounded-xl border border-[var(--border)] text-[10px] font-bold">
                  {["today", "tomorrow", "online", "in-person"].map(f => (
                    <button
                      key={f}
                      onClick={() => setAppointmentFilter(f)}
                      className={`px-2.5 py-1 rounded-lg capitalize transition ${
                        appointmentFilter === f ? "bg-[var(--elevated)] text-[#2DD4BF]" : "text-[var(--muted)] hover:text-white"
                      }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
              </div>

              {/* Appointment Rows */}
              <div className="space-y-2.5">
                {appointments.map(apt => (
                  <div
                    key={apt.id}
                    className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] hover:border-[#2DD4BF]/40 transition flex flex-col sm:flex-row justify-between sm:items-center gap-3 text-xs"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-white text-sm">{apt.patient}</span>
                        <span className="font-mono text-[10px] text-[var(--muted)]">{apt.pid}</span>
                        <span className={`px-2 py-0.5 rounded-full text-[9px] font-bold ${
                          apt.status === "In Consultation" ? "bg-amber-500/20 text-amber-300" :
                          apt.status === "Waiting" ? "bg-blue-500/20 text-blue-300" :
                          apt.status === "Completed" ? "bg-emerald-500/20 text-emerald-400" :
                          "bg-slate-700 text-slate-300"
                        }`}>
                          {apt.status}
                        </span>
                      </div>
                      <div className="text-[11px] text-[var(--muted)] flex items-center gap-3">
                        <span>🕒 {apt.time}</span>
                        <span>•</span>
                        <span>{apt.type}</span>
                        <span>•</span>
                        <span>Dr. Irfan</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => router.push("/doctor")}
                        className="px-3 py-1.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition shadow"
                      >
                        Start Consult →
                      </button>
                      <button
                        onClick={() => handleQuickAction(`Reschedule ${apt.patient}`)}
                        className="px-2.5 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-[var(--muted)] text-xs font-medium border border-[var(--border)]"
                      >
                        Reschedule
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* SECTION 8: Hakeem Sahab — Clinical Decision Support Panel (5 cols) */}
            <div className="lg:col-span-5 p-6 rounded-3xl bg-gradient-to-b from-[#1E293B] to-[var(--panel)] border border-teal-500/40 space-y-4 shadow-xl">
              <div className="flex items-center justify-between border-b border-[var(--border)] pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">🤖</span>
                  <div>
                    <h3 className="text-base font-bold text-white">Hakeem Sahab AI™ Copilot</h3>
                    <span className="text-[10px] text-teal-300 font-mono">5-Layer Clinical Decision Support</span>
                  </div>
                </div>
                <span className="px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 text-[10px] font-bold">
                  Active
                </span>
              </div>

              {/* Quick AI Action Pills */}
              <div className="flex flex-wrap gap-1.5 text-[10px]">
                <button onClick={() => handleAskAi("Explore Barid Balghami Dyscrasia Guidelines")} className="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-[#2DD4BF] text-slate-300">
                  ⚡ Barid Balghami Guidelines
                </button>
                <button onClick={() => handleAskAi("Review Knee Arthralgia Symptoms")} className="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-[#2DD4BF] text-slate-300">
                  🦴 Review Symptoms
                </button>
                <button onClick={() => handleAskAi("Check Suranjan + Colchicum Interaction")} className="px-2.5 py-1 rounded-lg bg-[var(--background)] border border-[var(--border)] hover:border-[#2DD4BF] text-slate-300">
                  💊 Check Interactions
                </button>
              </div>

              {/* Query Input Box */}
              <div className="space-y-2">
                <div className="relative">
                  <input
                    value={aiQuery}
                    onChange={(e) => setAiQuery(e.target.value)}
                    placeholder="Ask clinical question or paste symptoms..."
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-white placeholder-slate-500 focus:outline-none focus:border-[#2DD4BF]"
                    onKeyDown={(e) => { if (e.key === "Enter") handleAskAi(); }}
                  />
                  <button
                    onClick={() => handleAskAi()}
                    disabled={aiLoading}
                    className="absolute right-1.5 top-1.5 px-3 py-1.5 rounded-lg bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition disabled:opacity-50"
                  >
                    {aiLoading ? "Thinking..." : "Ask"}
                  </button>
                </div>
              </div>

              {/* AI Response Display */}
              {aiResponse && (
                <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-teal-500/30 text-xs text-slate-200 font-mono whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
                  {aiResponse}
                </div>
              )}

              {/* AI Service Fail-Closed State */}
              {aiError && (
                <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-800/60 text-xs space-y-2.5">
                  <div className="flex items-center gap-2 text-rose-300 font-semibold">
                    <span className="text-base">⚠</span>
                    <span>Clinical Decision Support Currently Unavailable</span>
                  </div>
                  <p className="text-slate-300 text-[11px] leading-relaxed">
                    {aiError} In accordance with medical safety guardrails (<code className="text-rose-200">safe_to_lock = False</code>), clinical suggestions cannot be simulated offline.
                  </p>
                  <div className="flex items-center gap-2 pt-1">
                    <button
                      type="button"
                      onClick={() => handleAskAi()}
                      className="px-3 py-1 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-white text-[10px] font-bold border border-rose-700 transition"
                    >
                      Retry Connection
                    </button>
                    <a
                      href="/knowledge"
                      className="px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-semibold border border-slate-700 transition"
                    >
                      Consult Knowledge Base
                    </a>
                  </div>
                </div>
              )}

              {/* Mandatory AI Safety Disclaimer */}
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[10px] text-amber-300 leading-snug">
                <strong>Statutory Disclaimer:</strong> AI-generated information is for clinical decision support only. Final diagnosis and treatment decisions require qualified clinician approval (<code className="text-amber-200">safe_to_lock = False</code>).
              </div>
            </div>
          )}

          {/* SECTION 6 & 11: Patient Overview & Follow-up Reminders */}
          {(activeTab === "therapeutic" || activeTab === "operations" || activeTab === "all" || activeTab === "clinical") && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              {/* Patient Overview Widget (8 cols in all, 12 cols in therapeutic) */}
              {(activeTab === "therapeutic" || activeTab === "all") && (
                <div className={`p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4 ${
                  activeTab === "therapeutic" ? "lg:col-span-12" : "lg:col-span-8"
                }`}>
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-3">
                    <div>
                      <h3 className="text-base font-bold text-white">Patient Clinical Directory</h3>
                      <p className="text-xs text-[var(--muted)]">Active cohorts and EMR records</p>
                    </div>
                    <div className="flex flex-wrap items-center gap-1 bg-[var(--background)] p-1 rounded-xl border border-[var(--border)] text-[10px] font-bold">
                      {["all", "high-priority", "follow-up", "pending-reports"].map(f => (
                        <button
                          key={f}
                          onClick={() => setPatientFilter(f)}
                          className={`px-2 py-1 rounded-lg capitalize transition ${
                            patientFilter === f ? "bg-[var(--elevated)] text-[#2DD4BF]" : "text-[var(--muted)]"
                          }`}
                        >
                          {f.replace("-", " ")}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {patientsList.map(p => (
                      <div key={p.id} className="p-4 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-2 text-xs">
                        <div className="flex justify-between items-start">
                          <div>
                            <h4 className="font-bold text-white text-sm">{p.name}</h4>
                            <span className="text-[10px] text-[var(--muted)] font-mono">{p.id} • {p.ageGender}</span>
                          </div>
                          <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-bold">
                            {p.status}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-300">
                          <strong>Complaint:</strong> {p.complaint}
                        </div>
                        <div className="text-[10px] text-[var(--muted)] space-y-0.5">
                          <div>Protocol: <strong className="text-teal-300">{p.protocol}</strong></div>
                          <div>Next Follow-up: <strong className="text-white">{p.nextFollowup}</strong></div>
                        </div>
                        <div className="pt-2 border-t border-[var(--border)] flex justify-between items-center">
                          <button onClick={() => router.push("/doctor")} className="text-xs text-emerald-400 font-bold hover:underline">
                            Open EMR Dossier →
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* SECTION 11: Pending Follow-ups with QSURA */}
              {(activeTab === "operations" || activeTab === "clinical" || activeTab === "all") && (
                <div className={`p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4 ${
                  activeTab === "operations" || activeTab === "clinical" ? "lg:col-span-12" : "lg:col-span-4"
                }`}>
                  <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                    <div>
                      <h3 className="text-base font-bold text-white">Pending Patient Follow-ups</h3>
                      <span className="text-[10px] text-emerald-400 font-mono">QSURA Multi-Rail Active</span>
                    </div>
                    <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[10px]">
                      3 Actionable Today
                    </span>
                  </div>

                  <div className={`space-y-3 ${activeTab === "clinical" || activeTab === "operations" ? "grid grid-cols-1 md:grid-cols-3 gap-3 space-y-0" : ""}`}>
                    {followupsList.map((f, i) => (
                      <div key={i} className="p-3 rounded-2xl bg-[var(--background)] border border-[var(--border)] text-xs space-y-2">
                        <div className="flex justify-between items-center">
                          <strong className="text-white font-bold">{f.patient}</strong>
                          <span className="text-[10px] font-mono text-amber-300 font-bold">{f.due}</span>
                        </div>
                        <p className="text-[11px] text-[var(--muted)]">{f.reason}</p>
                        <div className="flex gap-1.5 pt-1">
                          <button
                            onClick={() => handleQuickAction(`Sent WhatsApp reminder to ${f.patient}`)}
                            className="flex-1 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[10px]"
                          >
                            💬 WhatsApp
                          </button>
                          <button
                            onClick={() => handleQuickAction(`Placed call to ${f.patient}`)}
                            className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-[10px]"
                          >
                            📞 Call
                          </button>
                          <button
                            onClick={() => handleQuickAction(`Sent SMS to ${f.patient}`)}
                            className="px-2.5 py-1 rounded-lg bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-[10px]"
                          >
                            ✉️ SMS
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </div>
          )}

          {/* SECTION 9: ZAYVORA Axis Mapping Section (9 Functional Axes) */}
          {(activeTab === "therapeutic" || activeTab === "all") && (
            <section className="p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-[var(--border)] pb-3">
                <div>
                  <span className="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Functional Biomarker Topology</span>
                  <h3 className="text-lg font-bold text-white mt-0.5">ZAYVORA 9-Axis Clinical Mapping</h3>
                </div>
                <span className="text-xs text-[var(--muted)] font-mono">Patient Baseline vs Current Humoral Deviation</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {axesData.map((axis) => (
                  <div key={axis.name} className="p-4 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-2.5">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-white text-xs">{axis.name}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full font-mono ${
                        axis.risk === "Optimal" ? "bg-emerald-500/20 text-emerald-400" :
                        axis.risk === "Stable" ? "bg-blue-500/20 text-blue-400" :
                        axis.risk === "Moderate" ? "bg-yellow-500/20 text-yellow-300" :
                        "bg-rose-500/20 text-rose-300"
                      }`}>
                        {axis.risk}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <div className="flex-1 bg-[var(--panel)] h-2 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            axis.score > 75 ? "bg-rose-500" : axis.score > 60 ? "bg-amber-400" : "bg-emerald-400"
                          }`}
                          style={{ width: `${axis.score}%` }}
                        />
                      </div>
                      <span className="text-xs font-bold font-mono text-white">{axis.score}/100</span>
                    </div>

                    <div className="text-[11px] text-[var(--muted)] space-y-0.5 pt-1 border-t border-[var(--border)]">
                      <div>Protocol: <strong className="text-teal-300">{axis.protocol}</strong></div>
                      <div>Action: <span className="text-white">{axis.action}</span></div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* SECTION 10 & 12: Active Treatment Plans & Pharmacy Dispensary */}
          {(activeTab === "therapeutic" || activeTab === "operations" || activeTab === "all") && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              {/* Active Treatment Plans (6 cols in all, 12 cols in therapeutic) */}
              {(activeTab === "therapeutic" || activeTab === "all") && (
                <div className={`p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4 ${
                  activeTab === "therapeutic" ? "lg:col-span-12" : "lg:col-span-6"
                }`}>
                  <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                    <h3 className="text-base font-bold text-white">Active Living Treatment Plans</h3>
                    <span className="text-xs text-[#2DD4BF] font-semibold">89 Active Cohorts</span>
                  </div>

                  <div className="p-4 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-3 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-white text-sm">Metabolic Reset 90</span>
                      <span className="text-emerald-400 font-mono font-bold">27% Complete</span>
                    </div>
                    <div className="text-[11px] text-[var(--muted)] space-y-1">
                      <div>Patient: <strong className="text-white">Hamza Farooqi (MRN-2026-0814)</strong></div>
                      <div>Current Phase: <strong className="text-teal-300">Phase 1: Liver Priming (Day 24 of 90)</strong></div>
                      <div>Next Milestone: <strong>Fasting Lipid & Glucose Panel in 7 days</strong></div>
                      <div>Adherence Status: <span className="text-emerald-400 font-semibold">High (94%)</span></div>
                    </div>
                    <div className="w-full bg-[var(--panel)] h-2 rounded-full overflow-hidden">
                      <div className="bg-emerald-400 h-full rounded-full" style={{ width: "27%" }} />
                    </div>
                  </div>
                </div>
              )}

              {/* SECTION 12: Pharmacy & Medicine Inventory (6 cols in all, 12 cols in operations) */}
              {(activeTab === "operations" || activeTab === "all") && (
                <div className={`p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4 ${
                  activeTab === "operations" ? "lg:col-span-12" : "lg:col-span-6"
                }`}>
                  <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                    <div>
                      <h3 className="text-base font-bold text-white">Dispensary & Medicine Safety</h3>
                      <span className="text-[10px] text-emerald-400 font-mono">Schedule E(1) Mudabbar Gated</span>
                    </div>
                    <Link href="/pharmacy" className="text-xs text-teal-300 hover:underline font-bold">
                      Open Pharmacy OS →
                    </Link>
                  </div>

                  <div className="space-y-2.5 text-xs">
                    <div className="p-3 rounded-xl bg-[var(--background)] border border-amber-500/30 flex justify-between items-center">
                      <div>
                        <span className="font-bold text-white block">Suranjan Talkh (Mudabbar)</span>
                        <span className="text-[10px] text-amber-300">Batch B2-2026 • Exp: 2027-08-30</span>
                      </div>
                      <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono font-bold text-[10px]">
                        29 Units (Low Stock)
                      </span>
                    </div>
                    <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex justify-between items-center">
                      <div>
                        <span className="font-bold text-white block">ManiVital Pro (Withania Extract)</span>
                        <span className="text-[10px] text-[var(--muted)]">Batch MVP-901 • HPLC Verified</span>
                      </div>
                      <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold text-[10px]">
                        142 Units Normal
                      </span>
                    </div>
                  </div>
                </div>
              )}

            </div>
          )}

          {/* SECTION 14 & 15: Revenue & Business/Clinical Analytics */}
          {(activeTab === "operations" || activeTab === "all") && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              {/* Revenue Overview (5 cols) */}
              <div className="lg:col-span-5 p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
                <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                  <h3 className="text-base font-bold text-white">Revenue & Invoicing</h3>
                  <span className="text-xs text-emerald-400 font-mono font-bold">₹54,200 Today</span>
                </div>
                
                <div className="space-y-2 text-xs">
                  <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex justify-between items-center">
                    <span className="text-[var(--muted)]">Monthly Cumulative Revenue</span>
                    <strong className="text-white font-mono">₹14,82,400</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex justify-between items-center">
                    <span className="text-[var(--muted)]">Pending Insurance / Claims</span>
                    <strong className="text-amber-300 font-mono">₹38,500</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-[var(--background)] border border-[var(--border)] flex justify-between items-center">
                    <span className="text-[var(--muted)]">Dispensary Product Sales</span>
                    <strong className="text-emerald-400 font-mono">₹32,400 (60%)</strong>
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <button onClick={() => handleQuickAction("Create Invoice")} className="flex-1 py-2 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition">
                    + Create Invoice
                  </button>
                  <button onClick={() => handleQuickAction("Download Financial Report")} className="px-3 py-2 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-white text-xs font-semibold border border-[var(--border)]">
                    Download CSV
                  </button>
                </div>
              </div>

              {/* Analytics Section (7 cols) */}
              <div className="lg:col-span-7 p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-4">
                <div className="flex justify-between items-center border-b border-[var(--border)] pb-3">
                  <h3 className="text-base font-bold text-white">Clinical & Operational Analytics</h3>
                  <span className="text-xs text-[var(--muted)]">Last 30 Days Trajectory</span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
                  <div className="p-3 bg-[var(--background)] rounded-xl border border-[var(--border)]">
                    <span className="text-[10px] text-[var(--muted)] block uppercase">Retention Rate</span>
                    <span className="text-lg font-bold text-emerald-400">91.4%</span>
                  </div>
                  <div className="p-3 bg-[var(--background)] rounded-xl border border-[var(--border)]">
                    <span className="text-[10px] text-[var(--muted)] block uppercase">Avg Consult</span>
                    <span className="text-lg font-bold text-blue-400">32 mins</span>
                  </div>
                  <div className="p-3 bg-[var(--background)] rounded-xl border border-[var(--border)]">
                    <span className="text-[10px] text-[var(--muted)] block uppercase">Pain Reduction</span>
                    <span className="text-lg font-bold text-teal-300">58.2%</span>
                  </div>
                  <div className="p-3 bg-[var(--background)] rounded-xl border border-[var(--border)]">
                    <span className="text-[10px] text-[var(--muted)] block uppercase">Adherence</span>
                    <span className="text-lg font-bold text-purple-400">88.7%</span>
                  </div>
                </div>

                <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-1.5 text-xs">
                  <span className="text-[10px] font-bold text-[var(--muted)] uppercase">RWE Cohort Concordance</span>
                  <p className="text-[11px] text-slate-300 leading-relaxed">
                    94.2% diagnostic concordance between 10-Ajnas pulse evaluation and blinded university rheumatologist evaluations across 3 clinical centers.
                  </p>
                </div>
              </div>

            </div>
          )}

          {/* SECTION 18 & 19: Knowledge Base & System Status Widgets */}
          {(activeTab === "operations" || activeTab === "all") && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              
              {/* Knowledge Base Widget (6 cols) */}
              <div className="lg:col-span-6 p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-3">
                <div className="flex justify-between items-center border-b border-[var(--border)] pb-2">
                  <h3 className="text-sm font-bold text-white">Canonical Knowledge Base (ZKB)</h3>
                  <Link href="/knowledge" className="text-xs text-teal-300 hover:underline">Explore ZKB →</Link>
                </div>
                <p className="text-xs text-[var(--muted)]">
                  Query 1,280+ classical monographs (UPI, NFUM, Al-Qanoon) with verified Badal (substitutes) and Musleh (correctives).
                </p>
                <div className="flex gap-2">
                  <input
                    placeholder="Lookup herb (e.g., Asgandh, Suranjan)..."
                    className="flex-1 px-3 py-1.5 rounded-xl bg-[var(--background)] border border-[var(--border)] text-xs text-white"
                  />
                  <button onClick={() => router.push("/knowledge")} className="px-3 py-1.5 rounded-xl bg-[#0D9488] text-white text-xs font-bold">
                    Lookup
                  </button>
                </div>
              </div>

              {/* System Status Widget (6 cols) */}
              <div className="lg:col-span-6 p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-3">
                <div className="flex justify-between items-center border-b border-[var(--border)] pb-2">
                  <h3 className="text-sm font-bold text-white">Platform System & Microservices Status</h3>
                  <span className="text-[10px] text-emerald-400 font-mono">ALL OPERATIONAL</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px] font-mono">
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>Clinical AI CDS:</span> <span className="text-emerald-400">Online</span>
                  </div>
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>Patient EMR:</span> <span className="text-emerald-400">Online</span>
                  </div>
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>QSURA Comms:</span> <span className="text-emerald-400">Online</span>
                  </div>
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>Dispensary:</span> <span className="text-emerald-400">Online</span>
                  </div>
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>Payments:</span> <span className="text-emerald-400">Online</span>
                  </div>
                  <div className="p-2 rounded-lg bg-[var(--background)] border border-[var(--border)] flex justify-between">
                    <span>DR Backup:</span> <span className="text-emerald-400">Synced (12m)</span>
                  </div>
                </div>
              </div>

            </div>
          )}

        </main>
      </div>

      {/* SECTION 21: Dashboard Footer */}
      <PlatformFooter />
    </div>
  );
}
