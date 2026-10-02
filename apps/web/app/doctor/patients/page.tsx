"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";

const FALLBACK_PATIENTS = [
  { id:"P-001", name:"Arjun Mehta",    age:34, gender:"M", mizaj:"Damawi",   lastVisit:"2026-09-10", conditions:["Hypertension","Anxiety"] },
  { id:"P-002", name:"Fatima Zahra",   age:52, gender:"F", mizaj:"Balghami", lastVisit:"2026-09-08", conditions:["Obesity","Hypothyroid"] },
  { id:"P-003", name:"Rahul Singh",    age:28, gender:"M", mizaj:"Safrawi",  lastVisit:"2026-09-12", conditions:["IBS","Skin Allergy"] },
  { id:"P-004", name:"Anita Sharma",   age:61, gender:"F", mizaj:"Sawdawi",  lastVisit:"2026-09-01", conditions:["Arthritis","Insomnia"] },
  { id:"P-005", name:"Mohammed Iqbal", age:45, gender:"M", mizaj:"Damawi",   lastVisit:"2026-09-14", conditions:["Diabetes T2","Fatigue"] },
  { id:"P-006", name:"Priya Nair",     age:39, gender:"F", mizaj:"Safrawi",  lastVisit:"2026-08-28", conditions:["PCOS","Migraine"] },
];

export default function DoctorPatientsPage() {
  const [patientsList, setPatientsList] = useState(FALLBACK_PATIENTS);
  const [isLiveDb, setIsLiveDb] = useState(false);
  const [q, setQ] = useState("");

  useEffect(() => {
    fetch('/api/v1/patients')
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && data.patients && Array.isArray(data.patients) && data.patients.length > 0) {
          const liveMapped = data.patients.map((p: any) => ({
            id: p.mrn || p.id,
            name: `${p.first_name || ''} ${p.last_name || ''}`.trim() || 'Patient',
            age: p.age || 40,
            gender: (p.gender || 'M').charAt(0).toUpperCase(),
            mizaj: p.mizaj_dominant ? p.mizaj_dominant.split(' ')[0] : 'Damawi',
            lastVisit: p.created_at ? p.created_at.split(' ')[0] : '2026-09-18',
            conditions: p.allergies_json && p.allergies_json !== '[]' ? ['Allergy Logged'] : ['Integrative Evaluation']
          }));
          setPatientsList(liveMapped);
          setIsLiveDb(true);
        }
      })
      .catch(() => {});
  }, []);

  const filtered = patientsList.filter(p =>
    p.name.toLowerCase().includes(q.toLowerCase()) ||
    p.id.toLowerCase().includes(q.toLowerCase())
  );
  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">My Patients</h1>
              {isLiveDb ? (
                <span className="text-[10px] px-2 py-0.5 rounded-full font-bold bg-emerald-950 text-emerald-400 border border-emerald-500/40">● LIVE DB CONNECTED</span>
              ) : (
                <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-slate-800 text-slate-400">STANDBY CACHE</span>
              )}
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">{patientsList.length} active patients</p>
          </div>
          <button className="zv-btn-primary text-sm px-4 py-2">+ Register Patient</button>
        </div>
        <div className="flex gap-3">
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search by name or ID…"
            className="zv-input max-w-sm" />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(p => (
            <Link key={p.id} href={`/doctor/${p.id}`}
              className="zv-card p-4 hover:border-[var(--primary)] transition-all group block">
              <div className="flex items-start justify-between mb-3">
                <div className="w-10 h-10 rounded-full bg-[var(--primary-light)] flex items-center justify-center text-sm font-bold text-[#2DD4BF]">
                  {p.name.charAt(0)}
                </div>
                <span className="text-[10px] font-mono text-[var(--text-muted)]">{p.id}</span>
              </div>
              <h3 className="font-semibold text-[var(--text-primary)] text-sm group-hover:text-[#2DD4BF] transition">{p.name}</h3>
              <p className="text-xs text-[var(--text-muted)] mt-0.5">{p.age}y · {p.gender} · {p.mizaj}</p>
              <div className="flex flex-wrap gap-1 mt-2">
                {p.conditions.map(c => (
                  <span key={c} className="text-[10px] px-1.5 py-0.5 rounded bg-[var(--bg-elevated)] text-[var(--text-muted)]">{c}</span>
                ))}
              </div>
              <p className="text-[10px] text-[var(--text-muted)] mt-3">Last visit: {p.lastVisit}</p>
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
