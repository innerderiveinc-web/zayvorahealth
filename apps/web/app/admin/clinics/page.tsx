"use client";
import React from "react";
import { AppShell } from "@/components/AppShell";

const CLINICS = [
  { name:"ZAYVORA Matab™ — Central Care Centre", city:"New Delhi", doctors:5, status:"Active",   patients:180 },
  { name:"ZAYVORA Matab™ — Bhopal",           city:"Bhopal",     doctors:2, status:"Active",   patients:64 },
  { name:"ZAYVORA Matab™ — Hyderabad",        city:"Hyderabad",  doctors:1, status:"Pending",  patients:0 },
];

export default function AdminClinicsPage() {
  return (
    <AppShell activeRole="admin">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🏥 Clinics</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">ZAYVORA Matab™ clinic network</p>
          </div>
          <button className="zv-btn-primary text-sm px-4 py-2">+ Add Clinic</button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {CLINICS.map(c => (
            <div key={c.name} className="zv-card p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-2xl">🏥</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${c.status==="Active"?"zv-badge-emerald":"zv-badge-amber"}`}>{c.status}</span>
              </div>
              <h3 className="font-semibold text-sm text-[var(--text-primary)]">{c.name}</h3>
              <p className="text-xs text-[var(--text-muted)]">{c.city}</p>
              <div className="flex gap-4 text-xs text-[var(--text-muted)]">
                <span>👨‍⚕️ {c.doctors} doctors</span>
                <span>🧑 {c.patients} patients</span>
              </div>
              <button className="zv-btn-secondary text-xs px-3 py-1.5 w-full">Manage</button>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
