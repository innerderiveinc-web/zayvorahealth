"use client";
import React from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

export default function PatientMizajPage() {
  const mizaj = { type:"Damawi (Sanguine)", score:{ damawi:68, safrawi:18, balghami:10, sawdawi:4 } };
  return (
    <AppShell activeRole="patient">
      <div className="space-y-6 max-w-2xl">
        <div>
          <h1 className="text-2xl font-bold text-[var(--text-primary)]">🌿 Mizaj Profile</h1>
          <p className="text-sm text-[var(--text-muted)] mt-1">Your Unani temperament · Ajnas-e-Ashrah validated</p>
        </div>
        <div className="zv-card p-6 space-y-5">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🌿</span>
            <div>
              <div className="font-bold text-lg text-[var(--text-primary)]">{mizaj.type}</div>
              <div className="text-xs text-[var(--text-muted)]">Assessed by ZAYVORA Knowledge Intelligence™</div>
            </div>
          </div>
          <div className="space-y-3">
            {Object.entries(mizaj.score).map(([k,v]) => (
              <div key={k}>
                <div className="flex justify-between text-xs text-[var(--text-muted)] mb-1">
                  <span className="capitalize">{k}</span><span>{v}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-[var(--bg-elevated)]">
                  <div className="h-2 rounded-full bg-[var(--primary)] transition-all" style={{width:`${v}%`}} />
                </div>
              </div>
            ))}
          </div>
          <Link href="/patient/book" className="zv-btn-primary text-sm px-4 py-2 inline-flex">
            Book Mizaj Consultation
          </Link>
        </div>
      </div>
    </AppShell>
  );
}
