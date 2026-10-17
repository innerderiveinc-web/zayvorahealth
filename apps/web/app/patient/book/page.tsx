"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { AuthService } from "@/lib/services/authService";

const API = process.env.NEXT_PUBLIC_GATEWAY_URL || "http://localhost:8000";

interface DoctorOption {
  name: string;
  specialty: string;
  facilityId: string;
  facilityName: string;
  slots: string[];
}

const DOCTORS: DoctorOption[] = [
  {
    name: "Dr. Irfan Ashraf",
    specialty: "Integrative Unani OPD · Mizaj Diagnostics",
    facilityId: "FAC-HQ-01",
    facilityName: "zayvora clinic and hospital",
    slots: ["09:00 AM", "10:00 AM", "11:30 AM", "02:30 PM", "04:00 PM"]
  },
  {
    name: "Dr. Malik",
    specialty: "Clinical Tabeeb · Tadbeer & Herbal Posology",
    facilityId: "FAC-BRANCH-02",
    facilityName: "zayvora hospital",
    slots: ["09:30 AM", "11:00 AM", "01:00 PM", "03:30 PM"]
  }
];

export default function PatientBookPage() {
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1);
  const [selectedDoctor, setSelectedDoctor] = useState<DoctorOption>(DOCTORS[0]);
  const [date, setDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const [slot, setSlot] = useState<string>("");
  const [mode, setMode] = useState<"In-Person" | "Teleconsult">("In-Person");
  const [chiefComplaint, setChiefComplaint] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [confirmedBooking, setConfirmedBooking] = useState<{
    id: string;
    tokenNumber: string;
    doctorName: string;
    date: string;
    time: string;
    facility: string;
  } | null>(null);

  const handleBookingConfirm = async () => {
    setLoading(true);
    setError(null);

    const session = AuthService.getSession();
    const patientName = session?.user?.fullName || "Ahmad Khan";
    const mrn = session?.user?.mrn || "MRN-2026-0001";

    const payload = {
      patientName,
      mrn,
      doctorName: selectedDoctor.name,
      date,
      timeSlot: slot,
      chiefComplaint: chiefComplaint || (mode === "Teleconsult" ? "Teleconsultation Intake" : "General Unani OPD Consultation"),
      acuity: "STANDARD",
      fee: mode === "Teleconsult" ? 600.0 : 800.0,
      facilityId: selectedDoctor.facilityId
    };

    try {
      const res = await fetch(`${API}/api/v1/appointments`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(session?.token ? { Authorization: `Bearer ${session.token}` } : {})
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || errData.message || "Failed to book appointment.");
      }

      const data = await res.json();
      const apt = data.appointment || {};

      setConfirmedBooking({
        id: apt.id || "APT-" + Date.now(),
        tokenNumber: apt.tokenNumber || "T-101",
        doctorName: selectedDoctor.name,
        date: apt.appointmentDate || date,
        time: apt.appointmentTime || slot,
        facility: selectedDoctor.facilityName
      });
      setStep(4);
    } catch (err: any) {
      setError(err.message || "Network error. Please ensure the ZAYVORA backend service is active.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell activeRole="patient">
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🗓️ Book Consultation</h1>
            <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Live Matab Desk
            </span>
          </div>
          <p className="text-sm text-[var(--text-muted)] mt-1">
            ZAYVORA Matab™ — Clinician-led Unani care & holistic posology
          </p>
        </div>

        {/* Wizard Progress Bar */}
        {step < 4 && (
          <div className="flex gap-2 text-xs mb-4">
            {[
              { num: 1, label: "Choose Doctor" },
              { num: 2, label: "Select Slot" },
              { num: 3, label: "Confirm" }
            ].map((s) => (
              <div
                key={s.num}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full font-medium transition ${
                  step >= s.num
                    ? "bg-[var(--primary)] text-white shadow-sm"
                    : "bg-[var(--bg-elevated)] text-[var(--text-muted)]"
                }`}
              >
                <span className="w-4 h-4 rounded-full bg-black/20 flex items-center justify-center text-[10px] font-bold">
                  {s.num}
                </span>
                <span>{s.label}</span>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center justify-between">
            <span>⚠ {error}</span>
            <button
              onClick={() => setError(null)}
              className="text-red-400 hover:text-white font-bold ml-3"
            >
              ✕
            </button>
          </div>
        )}

        {/* Step 1: Doctor Selection */}
        {step === 1 && (
          <div className="space-y-3">
            <h2 className="text-sm font-semibold text-[var(--text-primary)]">Available Unani Physicians</h2>
            {DOCTORS.map((d) => (
              <div
                key={d.name}
                onClick={() => {
                  setSelectedDoctor(d);
                  setStep(2);
                }}
                className={`zv-card p-4 cursor-pointer hover:border-[var(--primary)] transition flex items-center justify-between ${
                  selectedDoctor.name === d.name ? "border-[var(--primary)] bg-[var(--primary-light)]" : ""
                }`}
              >
                <div>
                  <div className="font-semibold text-base text-[var(--text-primary)]">{d.name}</div>
                  <div className="text-xs text-[#2DD4BF] font-medium mt-0.5">{d.specialty}</div>
                  <div className="text-xs text-[var(--text-muted)] mt-1 flex items-center gap-1.5">
                    <span>🏥</span>
                    <span>{d.facilityName}</span>
                  </div>
                </div>
                <button className="zv-btn-secondary text-xs px-3.5 py-1.5 shrink-0">
                  Select Slots →
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Step 2: Date & Slot Selection */}
        {step === 2 && (
          <div className="space-y-5 zv-card p-5">
            <div>
              <h2 className="font-semibold text-base text-[var(--text-primary)]">
                Schedule with {selectedDoctor.name}
              </h2>
              <p className="text-xs text-[var(--text-muted)] mt-0.5">{selectedDoctor.facilityName}</p>
            </div>

            {/* Mode Selector */}
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1.5">Consultation Mode</label>
              <div className="flex gap-2">
                {(["In-Person", "Teleconsult"] as const).map((m) => (
                  <button
                    key={m}
                    onClick={() => setMode(m)}
                    className={`text-xs px-4 py-2 rounded-lg border font-medium transition ${
                      mode === m
                        ? "bg-[var(--primary)] text-white border-transparent"
                        : "border-[var(--border-default)] text-[var(--text-muted)] hover:text-white"
                    }`}
                  >
                    {m === "In-Person" ? "🏥 In-Person OPD" : "📱 Video Teleconsult"}
                  </button>
                ))}
              </div>
            </div>

            {/* Date Input */}
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1.5">Appointment Date</label>
              <input
                type="date"
                value={date}
                min={new Date().toISOString().split("T")[0]}
                onChange={(e) => setDate(e.target.value)}
                className="zv-input w-full max-w-xs text-sm"
              />
            </div>

            {/* Slot Grid */}
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1.5">Available Slots</label>
              <div className="flex gap-2.5 flex-wrap">
                {selectedDoctor.slots.map((s) => (
                  <button
                    key={s}
                    onClick={() => setSlot(s)}
                    className={`text-xs px-3.5 py-2 rounded-lg border font-mono font-medium transition ${
                      slot === s
                        ? "bg-[var(--primary)] text-white border-transparent"
                        : "border-[var(--border-default)] text-[var(--text-muted)] hover:border-[var(--primary)] hover:text-white"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            {/* Chief Complaint */}
            <div>
              <label className="text-xs font-semibold text-[var(--text-muted)] block mb-1.5">Chief Complaint / Symptoms (Optional)</label>
              <textarea
                rows={2}
                value={chiefComplaint}
                onChange={(e) => setChiefComplaint(e.target.value)}
                placeholder="e.g., Recurring migraine, gastric distress, chronic fatigue..."
                className="zv-input w-full text-xs"
              />
            </div>

            <div className="flex justify-between items-center pt-2 border-t border-[var(--border-default)]">
              <button onClick={() => setStep(1)} className="zv-btn-secondary text-xs px-4 py-2">
                ← Back
              </button>
              <button
                disabled={!slot}
                onClick={() => setStep(3)}
                className={`zv-btn-primary text-xs px-5 py-2 ${!slot ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                Proceed to Confirm →
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Confirmation Summary & Submission */}
        {step === 3 && (
          <div className="zv-card p-6 space-y-5">
            <h2 className="font-semibold text-lg text-[var(--text-primary)]">Review & Confirm Booking</h2>

            <div className="bg-[var(--bg-elevated)] p-4 rounded-xl space-y-2.5 text-xs">
              <div className="flex justify-between">
                <span className="text-[var(--text-muted)]">Physician:</span>
                <span className="font-semibold text-[var(--text-primary)]">{selectedDoctor.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--text-muted)]">Facility:</span>
                <span className="text-[var(--text-primary)]">{selectedDoctor.facilityName}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--text-muted)]">Date & Slot:</span>
                <span className="font-mono text-emerald-400 font-bold">{date} at {slot}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[var(--text-muted)]">Mode:</span>
                <span className="text-[var(--text-primary)]">{mode}</span>
              </div>
              {chiefComplaint && (
                <div className="flex justify-between border-t border-[var(--border-subtle)] pt-2">
                  <span className="text-[var(--text-muted)]">Complaint:</span>
                  <span className="text-[var(--text-primary)] max-w-xs text-right truncate">{chiefComplaint}</span>
                </div>
              )}
              <div className="flex justify-between border-t border-[var(--border-subtle)] pt-2 text-sm font-semibold">
                <span className="text-[var(--text-primary)]">Consultation Fee:</span>
                <span className="text-[#2DD4BF]">₹{mode === "Teleconsult" ? 600 : 800}</span>
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                disabled={loading}
                onClick={handleBookingConfirm}
                className="zv-btn-primary flex-1 py-2.5 text-sm font-semibold flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <span className="animate-spin text-base">⏳</span>
                    <span>Confirming Appointment...</span>
                  </>
                ) : (
                  <span>Confirm & Issue Token ✓</span>
                )}
              </button>
              <button
                disabled={loading}
                onClick={() => setStep(2)}
                className="zv-btn-secondary px-4 py-2.5 text-xs font-semibold"
              >
                ← Back
              </button>
            </div>
          </div>
        )}

        {/* Step 4: Live Success State */}
        {step === 4 && confirmedBooking && (
          <div className="zv-card p-6 space-y-6 border-emerald-500/40 bg-emerald-950/10">
            <div className="text-center space-y-2">
              <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-2xl mx-auto border border-emerald-500/30">
                ✓
              </div>
              <h2 className="text-xl font-bold text-[var(--text-primary)]">Appointment Confirmed!</h2>
              <p className="text-xs text-[var(--text-muted)]">
                Your consultation token has been generated and queued into the OPD system.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs text-[var(--text-muted)]">OPD Queue Token</span>
                <span className="font-mono text-xl font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-lg border border-emerald-500/20">
                  {confirmedBooking.tokenNumber}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[var(--text-muted)]">Booking Reference</span>
                <span className="font-mono text-[var(--text-primary)]">{confirmedBooking.id}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[var(--text-muted)]">Physician</span>
                <span className="text-[var(--text-primary)] font-medium">{confirmedBooking.doctorName}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[var(--text-muted)]">Schedule</span>
                <span className="font-mono text-[var(--text-primary)]">{confirmedBooking.date} at {confirmedBooking.time}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[var(--text-muted)]">Facility</span>
                <span className="text-[var(--text-primary)]">{confirmedBooking.facility}</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-2">
              <Link
                href="/patient/appointments"
                className="zv-btn-primary flex-1 py-2.5 text-center text-xs font-semibold"
              >
                View in My Appointments →
              </Link>
              <button
                onClick={() => {
                  setConfirmedBooking(null);
                  setStep(1);
                  setSlot("");
                }}
                className="zv-btn-secondary px-4 py-2.5 text-xs font-semibold"
              >
                Book Another
              </button>
            </div>
          </div>
        )}
      </div>
    </AppShell>
  );
}
