"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";
import { useAuth } from "@/lib/hooks/useAuth";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface QueueAppointment {
  id: string;
  token_number: string;
  mrn: string;
  patient_name: string;
  doctor_name: string;
  department: string;
  opd_room: string;
  appointment_date: string;
  appointment_time: string;
  acuity: string;
  chief_complaint: string;
  status: string;
  fee_amount: number;
  payment_status: string;
}

export default function DoctorQueuePage() {
  const { isLoading: authLoading, isAuthorized } = useAuth({
    requiredRoles: ["DOCTOR", "HAKEEM", "NURSE", "NURSE_COORDINATOR"],
  });

  const [appointments, setAppointments] = useState<QueueAppointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<"all" | "waiting" | "in_consultation" | "urgent">("all");

  const fetchQueue = async () => {
    setLoading(true);
    setError(null);
    const session = AuthService.getSession();

    try {
      const res = await fetch(`${API}/api/v1/appointments`, {
        headers: {
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
        }
      });

      if (!res.ok) {
        throw new Error(`Failed to load queue (HTTP ${res.status})`);
      }

      const data = await res.json();
      if (data.ok && Array.isArray(data.appointments)) {
        setAppointments(data.appointments);
      } else {
        setAppointments([]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to queue service.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthorized) {
      fetchQueue();
    }
  }, [isAuthorized]);

  const filtered = appointments.filter((p) => {
    if (filter === "waiting") return p.status === "WAITING";
    if (filter === "in_consultation") return p.status === "IN_CONSULTATION";
    if (filter === "urgent") return p.acuity?.toUpperCase() === "URGENT";
    return true;
  });

  const waitingCount = appointments.filter((p) => p.status === "WAITING").length;

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--bg-base)]">
        <div className="text-center space-y-3">
          <div className="text-3xl animate-spin">⏳</div>
          <p className="text-sm text-[var(--text-muted)]">Verifying credentials…</p>
        </div>
      </div>
    );
  }

  if (!isAuthorized) return null;

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-6xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">Clinical OPD Queue</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Live Reception Stream
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              {appointments.length} patients registered today · {waitingCount} currently waiting
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchQueue}
              className="zv-btn-secondary text-xs px-3 py-1.5 flex items-center gap-1.5"
              title="Refresh queue"
            >
              <span>🔄</span>
              <span>Refresh</span>
            </button>
            <div className="flex bg-[var(--bg-elevated)] rounded-lg p-1 border border-[var(--border-default)]">
              {(["all", "waiting", "in_consultation", "urgent"] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-3 py-1 rounded-md text-xs font-medium transition ${
                    filter === f
                      ? "bg-[var(--primary)] text-white font-semibold"
                      : "text-[var(--text-muted)] hover:text-white"
                  }`}
                >
                  {f === "all" ? "All" : f === "waiting" ? "Waiting" : f === "in_consultation" ? "In Consult" : "⚠ Urgent"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span>⚠</span>
              <span>{error}</span>
            </div>
            <button onClick={fetchQueue} className="zv-btn-secondary text-[11px] px-3 py-1 font-semibold">
              Retry
            </button>
          </div>
        )}

        <div className="zv-card overflow-hidden">
          {loading ? (
            <div className="p-8 text-center space-y-3">
              <div className="animate-spin text-2xl">⏳</div>
              <p className="text-xs text-[var(--text-muted)]">Loading clinical queue...</p>
            </div>
          ) : filtered.length === 0 ? (
            <div className="p-12 text-center space-y-3">
              <div className="text-3xl">☕</div>
              <h3 className="font-semibold text-base text-[var(--text-primary)]">No Patients in this View</h3>
              <p className="text-xs text-[var(--text-muted)] max-w-sm mx-auto">
                There are currently no patients matching the selected filter criteria.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-[var(--border-default)] bg-[var(--bg-elevated)]">
                  <tr className="text-left text-[var(--text-muted)] text-xs font-semibold">
                    <th className="px-4 py-3">Token</th>
                    <th className="px-4 py-3">Patient & MRN</th>
                    <th className="px-4 py-3">Schedule</th>
                    <th className="px-4 py-3">Chief Complaint</th>
                    <th className="px-4 py-3">Acuity</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--border-subtle)]">
                  {filtered.map((p) => (
                    <tr key={p.id} className="hover:bg-[var(--bg-elevated)] transition">
                      <td className="px-4 py-3 font-mono text-xs font-bold text-emerald-400">
                        {p.token_number}
                      </td>
                      <td className="px-4 py-3">
                        <div className="font-semibold text-sm text-[var(--text-primary)]">{p.patient_name}</div>
                        <div className="text-[11px] font-mono text-[var(--text-muted)]">{p.mrn}</div>
                      </td>
                      <td className="px-4 py-3 text-xs text-[var(--text-muted)]">
                        <div>{p.appointment_time}</div>
                        <div className="text-[10px] text-[var(--text-secondary)]">{p.department}</div>
                      </td>
                      <td className="px-4 py-3 text-xs text-[var(--text-primary)] max-w-xs truncate">
                        {p.chief_complaint || "Routine consultation"}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                            p.acuity?.toUpperCase() === "URGENT"
                              ? "bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse"
                              : "bg-gray-500/10 text-[var(--text-muted)]"
                          }`}
                        >
                          {p.acuity || "Standard"}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
                            p.status === "IN_CONSULTATION"
                              ? "zv-badge-emerald"
                              : p.status === "COMPLETED"
                              ? "bg-blue-500/10 text-blue-400 border border-blue-500/30"
                              : "zv-badge-amber"
                          }`}
                        >
                          {p.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Link
                          href={`/doctor?patientId=${p.mrn}`}
                          className="zv-btn-primary text-xs px-3.5 py-1.5 font-semibold inline-block"
                        >
                          Start Consultation →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
