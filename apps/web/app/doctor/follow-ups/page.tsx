"use client";
import React from "react";
import { AppShell } from "@/components/AppShell";

const FOLLOWUPS = [
  { patient:"Arjun Mehta",    due:"2026-09-21", reason:"Nuskha response check",   priority:"routine" },
  { patient:"Fatima Zahra",   due:"2026-09-18", reason:"Thyroid re-evaluation",   priority:"urgent" },
  { patient:"Mohammed Iqbal", due:"2026-09-22", reason:"HbA1c follow-up",         priority:"routine" },
  { patient:"Priya Nair",     due:"2026-09-20", reason:"PCOS Nuskha compliance",  priority:"routine" },
];

export default function FollowUpsPage() {
  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">Follow-ups</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">{FOLLOWUPS.length} follow-ups scheduled</p>
        </div>
        <div className="space-y-3">
          {FOLLOWUPS.map((f,i) => (
            <div key={i} className="zv-card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-sm text-[var(--text-primary)]">{f.patient}</div>
                <div className="text-xs text-[var(--text-muted)] mt-0.5">{f.reason}</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-[var(--text-muted)]">Due: {f.due}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${f.priority==="urgent"?"zv-badge-rose":"zv-badge-emerald"}`}>
                  {f.priority}
                </span>
                <button className="zv-btn-primary text-xs px-3 py-1.5">Schedule</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
