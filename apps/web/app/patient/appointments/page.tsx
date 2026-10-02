"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface AppointmentItem {
  id: string;
  token_number: string;
  mrn: string;
  patient_name: string;
  doctor_name: string;
  department?: string;
  opd_room?: string;
  appointment_date: string;
  appointment_time: string;
  acuity: string;
  chief_complaint?: string;
  status: string;
  fee_amount?: number;
  payment_status?: string;
}

export default function PatientAppointmentsPage() {
  const [appointments, setAppointments] = useState<AppointmentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAppointments = async () => {
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
        throw new Error(`Failed to load appointments (HTTP ${res.status})`);
      }

      const data = await res.json();
      if (data.ok && Array.isArray(data.appointments)) {
        setAppointments(data.appointments);
      } else {
        setAppointments([]);
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to appointments service.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6 max-w-4xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-[var(--text-primary)]">📅 Appointments</h1>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Live EMR Schedule
              </span>
            </div>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Your registered consultations & OPD tokens
            </p>
          </div>
          <Link href="/patient/book" className="zv-btn-primary text-xs px-4 py-2.5 font-semibold text-center">
            + Book New Consultation
          </Link>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span>⚠</span>
              <span>{error}</span>
            </div>
            <button
              onClick={fetchAppointments}
              className="zv-btn-secondary text-[11px] px-3 py-1 font-semibold"
            >
              Retry
            </button>
          </div>
        )}

        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((n) => (
              <div key={n} className="zv-card p-4 animate-pulse space-y-2">
                <div className="h-4 bg-[var(--bg-elevated)] rounded w-1/3"></div>
                <div className="h-3 bg-[var(--bg-elevated)] rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : appointments.length === 0 ? (
          <div className="zv-card p-10 text-center space-y-3">
            <div className="text-3xl">🗓️</div>
            <h3 className="font-semibold text-base text-[var(--text-primary)]">No Scheduled Consultations</h3>
            <p className="text-xs text-[var(--text-muted)] max-w-sm mx-auto">
              You do not have any upcoming visits booked with ZAYVORA Matab™.
            </p>
            <Link href="/patient/book" className="zv-btn-primary inline-block text-xs px-4 py-2 font-semibold mt-2">
              Book First Consultation →
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {appointments.map((a) => (
              <div
                key={a.id}
                className="zv-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-[var(--primary)] transition"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2.5">
                    <span className="font-mono text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                      {a.token_number}
                    </span>
                    <span className="font-semibold text-sm text-[var(--text-primary)]">
                      {a.doctor_name}
                    </span>
                  </div>
                  <div className="text-xs text-[var(--text-muted)] flex flex-wrap items-center gap-x-3 gap-y-1">
                    <span>🗓️ {a.appointment_date} at {a.appointment_time}</span>
                    <span>•</span>
                    <span>🏥 {a.department || "Integrative Unani OPD"}</span>
                    {a.opd_room && (
                      <>
                        <span>•</span>
                        <span>{a.opd_room}</span>
                      </>
                    )}
                  </div>
                  {a.chief_complaint && (
                    <div className="text-[11px] text-[var(--text-secondary)] italic pt-0.5">
                      Complaint: &ldquo;{a.chief_complaint}&rdquo;
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <span
                    className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                      a.status === "COMPLETED"
                        ? "zv-badge-emerald"
                        : a.status === "IN_CONSULTATION"
                        ? "bg-blue-500/10 text-blue-400 border border-blue-500/30"
                        : "zv-badge-amber"
                    }`}
                  >
                    {a.status === "WAITING" ? "⏳ In Queue" : a.status}
                  </span>
                  <span className="text-xs font-mono text-[var(--text-muted)]">
                    {a.payment_status === "PAID" ? "✓ Paid" : "Pending Fee"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
