"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

type AlertPriority = "Critical" | "High" | "Normal" | "Info";
type AlertCategory = "clinical" | "interaction" | "labs" | "appointments" | "system";

interface AlertItem {
  id: string;
  title: string;
  description: string;
  category: AlertCategory;
  priority: AlertPriority;
  timestamp: string;
  patientName?: string;
  mrn?: string;
  actionUrl?: string;
  actionLabel?: string;
  acknowledged: boolean;
}

const INITIAL_ALERTS: AlertItem[] = [
  {
    id: "alt-01",
    title: "Schedule E(1) Mudabbar Certificate Required",
    description: "Prescription RX-2026-0441 contains Suranjan Talkh (Colchicum luteum). 21 CFR Part 11 dispensing lock active until detoxification signature is uploaded.",
    category: "interaction",
    priority: "Critical",
    timestamp: "12 mins ago",
    patientName: "Hamza Farooqi",
    mrn: "MRN-2026-0814",
    actionUrl: "/doctor/nuskha",
    actionLabel: "Verify Mudabbar Signature",
    acknowledged: false,
  },
  {
    id: "alt-02",
    title: "Critical Lab Abnormality: Serum Uric Acid > 9.2 mg/dL",
    description: "Automated HL7/FHIR ingest detected elevated uric acid in bilateral knee arthralgia patient. Immediate Stage 1 Tanqiya intervention recommended.",
    category: "labs",
    priority: "Critical",
    timestamp: "28 mins ago",
    patientName: "Hamza Farooqi",
    mrn: "MRN-2026-0814",
    actionUrl: "/doctor/reports",
    actionLabel: "Review Diagnostic Panel",
    acknowledged: false,
  },
  {
    id: "alt-03",
    title: "Drug-Herb Interaction Alert: Glycemic Potentiation",
    description: "Concomitant Metformin 500mg with high-dose Jamun seed powder (Syzygium cumini) poses mild hypoglycemia risk. Monitor fasting glucose.",
    category: "clinical",
    priority: "High",
    timestamp: "1 hour ago",
    patientName: "Bilal Ahmad",
    mrn: "MRN-2026-0744",
    actionUrl: "/doctor/patients",
    actionLabel: "Adjust Regimen",
    acknowledged: false,
  },
  {
    id: "alt-04",
    title: "OPD Check-In Waiting > 20 Mins",
    description: "Token T-104 Hamza Farooqi arrived at 10:15 AM. Assigned to Consultation Desk Room 3.",
    category: "appointments",
    priority: "Normal",
    timestamp: "35 mins ago",
    patientName: "Hamza Farooqi",
    mrn: "MRN-2026-0814",
    actionUrl: "/doctor",
    actionLabel: "Start Consultation",
    acknowledged: true,
  },
  {
    id: "alt-05",
    title: "Dispensary FEFO Batch Reallocation",
    description: "Batch B2-SURANJAN nearing 90-day expiry threshold. Automatically promoted to primary dispensing queue under AYUSH-GMP rules.",
    category: "system",
    priority: "Info",
    timestamp: "2 hours ago",
    actionUrl: "/pharmacy/inventory",
    actionLabel: "Inspect Stock",
    acknowledged: false,
  },
  {
    id: "alt-06",
    title: "Telemedicine Video Appointment in 15 Minutes",
    description: "Ayesha Siddiqui has joined the virtual WebRTC waiting room for PCOS follow-up review.",
    category: "appointments",
    priority: "High",
    timestamp: "Just now",
    patientName: "Ayesha Siddiqui",
    mrn: "MRN-2026-0921",
    actionUrl: "/telemedicine",
    actionLabel: "Join Tele-Room",
    acknowledged: false,
  },
];

export default function NotificationsCenterPage() {
  const [alerts, setAlerts] = useState<AlertItem[]>(INITIAL_ALERTS);
  const [selectedCategory, setSelectedCategory] = useState<"all" | AlertCategory>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [notice, setNotice] = useState<string | null>(null);

  const handleAcknowledge = (id: string) => {
    setAlerts((prev) =>
      prev.map((a) => (a.id === id ? { ...a, acknowledged: true } : a))
    );
    setNotice("Alert acknowledged and recorded in clinical log.");
    setTimeout(() => setNotice(null), 2500);
  };

  const handleDismiss = (id: string) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
    setNotice("Notification dismissed.");
    setTimeout(() => setNotice(null), 2500);
  };

  const handleMarkAllRead = () => {
    setAlerts((prev) => prev.map((a) => ({ ...a, acknowledged: true })));
    setNotice("All notifications marked as acknowledged.");
    setTimeout(() => setNotice(null), 2500);
  };

  const filteredAlerts = alerts.filter((a) => {
    const matchesCategory = selectedCategory === "all" || a.category === selectedCategory;
    const matchesSearch =
      a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      a.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (a.patientName && a.patientName.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const unreadCount = alerts.filter((a) => !a.acknowledged).length;

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-6xl mx-auto">
        
        {/* Header Title */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>🔔</span> Clinical Alerts & Notifications Hub
              {unreadCount > 0 && (
                <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-bold border border-rose-500/30">
                  {unreadCount} Actionable
                </span>
              )}
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              Real-time surveillance: Schedule E(1) safety triggers, abnormal diagnostic thresholds, and patient queues.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={handleMarkAllRead}
              className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] border border-[var(--border)] text-[var(--muted)] hover:text-white font-medium transition"
            >
              ✓ Mark All Acknowledged
            </button>
            <Link
              href="/settings"
              className="px-3 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition"
            >
              ⚙️ Alert Rules
            </Link>
          </div>
        </div>

        {/* Action Notice */}
        {notice && (
          <div className="p-3 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between animate-fadeIn">
            <span>✓ {notice}</span>
            <button onClick={() => setNotice(null)} className="text-slate-400 hover:text-white">✕</button>
          </div>
        )}

        {/* Filter Controls & Search */}
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto p-1 bg-[var(--panel)] border border-[var(--border)] rounded-2xl text-xs">
            {(
              [
                { id: "all", label: "All Alerts", icon: "📋" },
                { id: "interaction", label: "Drug Interactions", icon: "⚠️" },
                { id: "labs", label: "Lab Abnormalities", icon: "🧪" },
                { id: "clinical", label: "Clinical Triggers", icon: "🩺" },
                { id: "appointments", label: "Appointments", icon: "📅" },
                { id: "system", label: "System Health", icon: "⚙️" },
              ] as const
            ).map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedCategory(tab.id)}
                className={`px-3 py-1.5 rounded-xl font-medium whitespace-nowrap transition flex items-center gap-1.5 ${
                  selectedCategory === tab.id
                    ? "bg-teal-600 text-white font-semibold shadow-xs"
                    : "text-[var(--muted)] hover:text-white hover:bg-[var(--elevated)]"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          <div className="w-full sm:w-64">
            <input
              type="text"
              placeholder="Search alert title or MRN..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[var(--panel)] border border-[var(--border)] rounded-xl px-3 py-1.5 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {/* Alerts Stream List */}
        <div className="space-y-3">
          {filteredAlerts.length === 0 ? (
            <div className="p-12 text-center rounded-3xl bg-[var(--panel)] border border-[var(--border)] text-xs space-y-2">
              <span className="text-3xl">🎉</span>
              <p className="font-bold text-white">No active alerts in this category</p>
              <p className="text-[var(--muted)]">All clinical criteria and safety barriers are operating within normal parameters.</p>
            </div>
          ) : (
            filteredAlerts.map((alt) => {
              const isCrit = alt.priority === "Critical";
              const isHigh = alt.priority === "High";
              return (
                <div
                  key={alt.id}
                  className={`p-4 rounded-2xl border transition flex flex-col md:flex-row items-start md:items-center justify-between gap-4 ${
                    alt.acknowledged
                      ? "bg-[var(--panel)]/50 border-[var(--border)] opacity-75"
                      : isCrit
                      ? "bg-rose-950/20 border-rose-800/40 shadow-sm"
                      : isHigh
                      ? "bg-amber-950/20 border-amber-800/40"
                      : "bg-[var(--panel)] border-[var(--border)]"
                  }`}
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          isCrit
                            ? "bg-rose-500/20 text-rose-300 border-rose-500/30"
                            : isHigh
                            ? "bg-amber-500/20 text-amber-300 border-amber-500/30"
                            : alt.priority === "Normal"
                            ? "bg-blue-500/20 text-blue-300 border-blue-500/30"
                            : "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"
                        }`}
                      >
                        {alt.priority}
                      </span>
                      <span className="text-xs font-bold text-white">{alt.title}</span>
                      <span className="text-[10px] text-[var(--muted)]">• {alt.timestamp}</span>
                      {alt.acknowledged && (
                        <span className="text-[10px] text-emerald-400 font-medium">✓ Acknowledged</span>
                      )}
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
                      {alt.description}
                    </p>

                    {alt.patientName && (
                      <div className="flex items-center gap-2 pt-1 text-[11px]">
                        <span className="text-[var(--muted)]">Patient:</span>
                        <span className="font-semibold text-white">{alt.patientName}</span>
                        {alt.mrn && (
                          <span className="font-mono text-[10px] text-teal-300 bg-slate-900 px-1.5 py-0.2 rounded border border-slate-700">
                            {alt.mrn}
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 shrink-0 self-end md:self-center text-xs">
                    {alt.actionUrl && (
                      <Link
                        href={alt.actionUrl}
                        className="px-3.5 py-1.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold transition flex items-center gap-1"
                      >
                        <span>{alt.actionLabel || "Inspect Record"}</span>
                        <span>→</span>
                      </Link>
                    )}

                    {!alt.acknowledged && (
                      <button
                        onClick={() => handleAcknowledge(alt.id)}
                        className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] border border-[var(--border)] text-slate-300 hover:text-white font-medium transition"
                      >
                        Acknowledge
                      </button>
                    )}

                    <button
                      onClick={() => handleDismiss(alt.id)}
                      className="p-1.5 rounded-xl hover:bg-rose-500/10 text-slate-400 hover:text-rose-400 transition"
                      title="Dismiss notification"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              );
            })
          )}
        </div>

      </div>
    </AppShell>
  );
}
