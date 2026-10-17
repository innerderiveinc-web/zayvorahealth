"use client";
import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

const SLOTS = [
  { time: "09:00", patient: "Arjun Mehta",    type: "Follow-up",        status: "confirmed" },
  { time: "09:30", patient: "Fatima Zahra",   type: "New Consultation", status: "confirmed" },
  { time: "10:00", patient: "—",              type: "Available",        status: "free" },
  { time: "10:30", patient: "Rahul Singh",    type: "Nuskha Review",    status: "confirmed" },
  { time: "11:00", patient: "Anita Sharma",   type: "Teleconsult",      status: "telehealth" },
  { time: "11:30", patient: "—",              type: "Available",        status: "free" },
  { time: "12:00", patient: "Lunch Break",    type: "Break",            status: "break" },
  { time: "14:00", patient: "Mohammed Iqbal", type: "New Consultation", status: "confirmed" },
  { time: "14:30", patient: "Priya Nair",     type: "Follow-up",        status: "pending" },
  { time: "15:00", patient: "—",              type: "Available",        status: "free" },
];

export default function DoctorCalendarPage() {
  const today = new Date().toLocaleDateString("en-IN", { weekday:"long", year:"numeric", month:"long", day:"numeric" });
  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">Calendar</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">{today}</p>
          </div>
          <button className="zv-btn-primary text-sm px-4 py-2">+ Block Slot</button>
        </div>
        <div className="zv-card divide-y divide-[var(--border-subtle)]">
          {SLOTS.map((slot) => (
            <div key={slot.time} className={`flex items-center gap-4 px-5 py-3 hover:bg-[var(--bg-elevated)] transition ${
              slot.status==="break" ? "opacity-50" : ""
            }`}>
              <span className="font-mono text-sm text-[var(--text-muted)] w-14 shrink-0">{slot.time}</span>
              <div className={`w-1 h-10 rounded-full shrink-0 ${
                slot.status==="free"?"bg-[var(--bg-elevated)]":
                slot.status==="confirmed"?"bg-[var(--primary)]":
                slot.status==="telehealth"?"bg-blue-500":
                slot.status==="pending"?"bg-amber-500":"bg-[var(--border-default)]"
              }`} />
              <div className="flex-1">
                <div className="font-medium text-sm text-[var(--text-primary)]">{slot.patient}</div>
                <div className="text-xs text-[var(--text-muted)]">{slot.type}</div>
              </div>
              {slot.status !== "free" && slot.status !== "break" && (
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  slot.status==="confirmed"?"zv-badge-emerald":
                  slot.status==="telehealth"?"zv-badge-blue":"zv-badge-amber"
                }`}>{slot.status}</span>
              )}
              {slot.status === "free" && (
                <button className="zv-btn-secondary text-xs px-2 py-1">Book</button>
              )}
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
