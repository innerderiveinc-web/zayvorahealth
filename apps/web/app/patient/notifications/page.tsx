"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

interface NotificationItem {
  id: string;
  type: "Medication" | "Appointment" | "Lab Alert" | "Clinical Guidance";
  title: string;
  desc: string;
  date: string;
  read: boolean;
}

const NOTIFICATIONS: NotificationItem[] = [
  { id: "1", type: "Medication", title: "Dose Reminder: Majun Suranjan", desc: "Please take 5g of Majun Suranjan with warm fennel infusion after dinner.", date: "Today, 8:00 PM", read: false },
  { id: "2", type: "Appointment", title: "Follow-up Consultation Confirmed", desc: "Your appointment with Hakeem Dr. Irfan Ashraf is scheduled for September 24, 2026 at 10:30 AM in Room 204.", date: "Yesterday", read: false },
  { id: "3", type: "Lab Alert", title: "Diagnostic Results Ready", desc: "Your Fasting Blood Glucose and ESR inflammatory markers have been verified and attached to your patient file.", date: "3 days ago", read: true },
  { id: "4", type: "Clinical Guidance", title: "Tanqiya Phase Diet Instructions", desc: "Remember to adhere to warm, light broths and avoid chilled items during Stage 1.", date: "5 days ago", read: true }
];

export default function PatientNotificationsPage() {
  const [items, setItems] = useState<NotificationItem[]>(NOTIFICATIONS);

  const markAllRead = () => {
    setItems(items.map(i => ({ ...i, read: true })));
  };

  return (
    <AppShell activeRole="patient">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">🔔 Notification Center</h1>
            <p className="text-sm text-[var(--text-muted)] mt-1">
              Medication reminders, appointment confirmations, and clinical alerts
            </p>
          </div>
          <button 
            onClick={markAllRead}
            className="px-4 py-2 border border-[var(--border)] text-[var(--text-muted)] hover:text-white rounded-xl text-xs font-semibold transition"
          >
            Mark All as Read
          </button>
        </div>

        <div className="space-y-3">
          {items.map(n => (
            <div key={n.id} className={`p-5 rounded-2xl border transition flex items-start justify-between gap-4 ${
              n.read ? "bg-[var(--card)] border-[var(--border)] opacity-70" : "bg-[var(--card)] border-emerald-500/40 shadow-sm"
            }`}>
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-emerald-400 uppercase">{n.type}</span>
                  {!n.read && <span className="w-2 h-2 rounded-full bg-emerald-400"></span>}
                </div>
                <h3 className="font-bold text-white text-sm">{n.title}</h3>
                <p className="text-xs text-[var(--text-muted)] leading-relaxed">{n.desc}</p>
                <span className="text-[10px] text-[var(--text-muted)] font-mono block pt-1">{n.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
