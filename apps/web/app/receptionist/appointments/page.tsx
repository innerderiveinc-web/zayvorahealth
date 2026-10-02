"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { StatusBadge } from "@/components/StatusBadge";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface AppointmentItem {
  id: string;
  patientName: string;
  doctorName: string;
  timeSlot: string;
  date: string;
  chiefComplaint: string;
  status: string;
  fee: number;
}

export default function ReceptionistAppointmentsPage() {
  const [appointments, setAppointments] = useState<AppointmentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadAppointments() {
      try {
        const session = AuthService.getSession();
        const headers: Record<string, string> = session?.token ? { Authorization: `Bearer ${session.token}` } : {};
        const res = await fetch(`${API}/api/v1/appointments`, { headers });
        if (res.ok) {
          const data = await res.json();
          const items = data.appointments || data.items || data || [];
          if (Array.isArray(items)) {
            setAppointments(items);
          }
        }
      } catch {
      } finally {
        setLoading(false);
      }
    }
    loadAppointments();
  }, []);

  const filtered = appointments.filter(a =>
    search === "" ||
    (a.patientName && a.patientName.toLowerCase().includes(search.toLowerCase())) ||
    (a.doctorName && a.doctorName.toLowerCase().includes(search.toLowerCase())) ||
    (a.chiefComplaint && a.chiefComplaint.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <AppShell activeRole="receptionist">
      <div className="space-y-6 max-w-7xl mx-auto text-xs text-slate-200">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[#334155] pb-4">
          <div>
            <h1 className="text-lg font-bold text-white">OPD Appointments Schedule &amp; Allocation</h1>
            <p className="text-xs text-slate-400">Manage pre-booked visits, doctor slot allocations, and conflict avoidance.</p>
          </div>
          <div className="flex items-center gap-2">
            <Link
              href="/receptionist"
              className="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold"
            >
              ← Back to Live Queue
            </Link>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search patient, doctor, or complaint..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 bg-[#0F172A] border border-[#334155] rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-teal-500"
          />
          <span className="text-slate-400 font-mono text-[11px] whitespace-nowrap">
            {filtered.length} Appointments Found
          </span>
        </div>

        <div className="zv-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#0A0F1D] text-slate-400 uppercase text-[10px] tracking-wider border-b border-[#334155]">
                <tr>
                  <th className="p-3">Time &amp; Date</th>
                  <th className="p-3">Patient Name</th>
                  <th className="p-3">Assigned Tabeeb</th>
                  <th className="p-3">Clinical Concern</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 text-right">Fee</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]">
                {loading ? (
                  <tr>
                    <td colSpan={6} className="p-6 text-center text-slate-400">
                      Loading scheduled appointments from gateway...
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="p-6 text-center text-slate-500">
                      No appointments matching query.
                    </td>
                  </tr>
                ) : (
                  filtered.map((apt, idx) => (
                    <tr key={apt.id || idx} className="hover:bg-[#1E293B]/50 transition">
                      <td className="p-3 font-mono text-teal-300">
                        {apt.timeSlot || "10:30 AM"} • {apt.date || "Today"}
                      </td>
                      <td className="p-3 font-bold text-white">
                        {apt.patientName || "Patient"}
                      </td>
                      <td className="p-3 text-slate-300">
                        {apt.doctorName || "Consulting Tabeeb"}
                      </td>
                      <td className="p-3 text-slate-400 max-w-xs truncate">
                        {apt.chiefComplaint || "Routine Consultation"}
                      </td>
                      <td className="p-3">
                        <StatusBadge status={apt.status || "CONFIRMED"} variant="verified" />
                      </td>
                      <td className="p-3 text-right font-mono text-emerald-400 font-bold">
                        ₹{apt.fee || 800}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
