"use client";
import React from "react";
import { AppShell } from "@/components/AppShell";

const REPORTS = [
  { name:"Monthly Encounter Summary",     date:"Sep 2026", type:"Clinical",    status:"Ready" },
  { name:"Nuskha Effectiveness Report",   date:"Sep 2026", type:"Clinical",    status:"Ready" },
  { name:"Mizaj Distribution Analysis",   date:"Sep 2026", type:"Research",    status:"Processing" },
  { name:"Patient Outcome Tracker",       date:"Aug 2026", type:"Clinical",    status:"Ready" },
  { name:"Schedule E(1) Compliance Log",  date:"Sep 2026", type:"Compliance",  status:"Ready" },
];

export default function DoctorReportsPage() {
  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">Reports</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">Clinical, research, and compliance reports</p>
          </div>
          <button className="zv-btn-primary text-sm px-4 py-2">Generate Report</button>
        </div>
        <div className="space-y-3">
          {REPORTS.map((r,i) => (
            <div key={i} className="zv-card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-sm text-[var(--text-primary)]">{r.name}</div>
                <div className="text-xs text-[var(--text-muted)] mt-0.5">{r.date} · {r.type}</div>
              </div>
              <div className="flex items-center gap-3">
                <span className={`text-xs px-2 py-0.5 rounded-full ${r.status==="Ready"?"zv-badge-emerald":"zv-badge-amber"}`}>{r.status}</span>
                {r.status==="Ready" && <button className="zv-btn-secondary text-xs px-3 py-1.5">Download PDF</button>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
