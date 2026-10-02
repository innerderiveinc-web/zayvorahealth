"use client";
import React from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

const ENCOUNTERS = [
  { id:"E-001", date:"2026-09-14", patient:"Arjun Mehta",    type:"Follow-up",        mizaj:"Damawi",   status:"Signed",  rx:"Nuskha #47" },
  { id:"E-002", date:"2026-09-13", patient:"Fatima Zahra",   type:"New Consultation", mizaj:"Balghami", status:"Signed",  rx:"Nuskha #48" },
  { id:"E-003", date:"2026-09-12", patient:"Rahul Singh",    type:"Urgent",           mizaj:"Safrawi",  status:"Draft",   rx:"Pending" },
  { id:"E-004", date:"2026-09-10", patient:"Anita Sharma",   type:"Teleconsult",      mizaj:"Sawdawi",  status:"Signed",  rx:"Nuskha #45" },
  { id:"E-005", date:"2026-09-08", patient:"Mohammed Iqbal", type:"Follow-up",        mizaj:"Damawi",   status:"Signed",  rx:"Nuskha #44" },
];

export default function EncountersPage() {
  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">Encounters</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">Clinical encounters · eBMR ledger</p>
          </div>
          <Link href="/doctor/queue" className="zv-btn-primary text-sm px-4 py-2">+ New Encounter</Link>
        </div>
        <div className="zv-card overflow-hidden">
          <table className="w-full text-sm">
            <thead className="border-b border-[var(--border-default)]">
              <tr className="text-left text-[var(--text-muted)] text-xs">
                <th className="px-4 py-3">ID</th>
                <th className="px-4 py-3">Date</th>
                <th className="px-4 py-3">Patient</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Mizaj</th>
                <th className="px-4 py-3">Rx</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-subtle)]">
              {ENCOUNTERS.map(e => (
                <tr key={e.id} className="hover:bg-[var(--bg-elevated)] transition cursor-pointer">
                  <td className="px-4 py-3 font-mono text-xs text-[var(--text-muted)]">{e.id}</td>
                  <td className="px-4 py-3 text-xs text-[var(--text-muted)]">{e.date}</td>
                  <td className="px-4 py-3 font-medium text-[var(--text-primary)]">{e.patient}</td>
                  <td className="px-4 py-3 text-xs">{e.type}</td>
                  <td className="px-4 py-3">
                    <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--primary-light)] text-[#2DD4BF] border border-[rgba(13,148,136,0.3)]">{e.mizaj}</span>
                  </td>
                  <td className="px-4 py-3 text-xs font-mono text-[var(--text-muted)]">{e.rx}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${e.status==="Signed"?"zv-badge-emerald":"zv-badge-amber"}`}>{e.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </AppShell>
  );
}
