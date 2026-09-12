"use client";

import React, { useState } from "react";
import type { TimelineEvent } from "@/lib/clinicalApi";

interface PatientTimelineProps {
  events: TimelineEvent[];
  loading?: boolean;
  error?: string | null;
}

export function PatientTimeline({ events, loading = false, error = null }: PatientTimelineProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (loading) {
    return (
      <div className="p-8 text-center" style={{ color: "var(--muted)" }}>
        <div className="inline-block animate-spin w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full mb-3" />
        <p className="text-sm">Loading longitudinal timeline...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-lg bg-red-950/30 border border-red-800/50 text-sm text-red-400">
        Failed to load patient timeline: {error}
      </div>
    );
  }

  if (!events || events.length === 0) {
    return (
      <div className="p-8 text-center zv-panel">
        <p className="text-sm font-medium" style={{ color: "var(--muted)" }}>
          No longitudinal events recorded for this patient yet.
        </p>
        <p className="text-xs mt-1" style={{ color: "var(--muted)" }}>
          Encounters, clinical notes, and prescriptions will appear here chronologically.
        </p>
      </div>
    );
  }

  const getEventBadge = (type: TimelineEvent["event_type"]) => {
    switch (type) {
      case "encounter":
        return {
          label: "Encounter",
          bg: "bg-emerald-950/40",
          text: "text-emerald-400",
          border: "border-emerald-700/50",
          dot: "bg-emerald-500",
        };
      case "clinical_note":
        return {
          label: "Clinical Note",
          bg: "bg-amber-950/40",
          text: "text-amber-300",
          border: "border-amber-700/50",
          dot: "bg-amber-400",
        };
      case "prescription":
        return {
          label: "Prescription",
          bg: "bg-cyan-950/40",
          text: "text-cyan-300",
          border: "border-cyan-700/50",
          dot: "bg-cyan-400",
        };
      case "appointment":
        return {
          label: "Appointment",
          bg: "bg-indigo-950/40",
          text: "text-indigo-300",
          border: "border-indigo-700/50",
          dot: "bg-indigo-400",
        };
      default:
        return {
          label: type,
          bg: "bg-stone-900",
          text: "text-stone-300",
          border: "border-stone-700",
          dot: "bg-stone-400",
        };
    }
  };

  return (
    <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-[#24302a]">
      {events.map((evt) => {
        const badge = getEventBadge(evt.event_type);
        const isExpanded = expandedId === evt.id;
        const dateStr = new Date(evt.timestamp).toLocaleString(undefined, {
          month: "short",
          day: "numeric",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });

        return (
          <div key={evt.id} className="relative group">
            {/* Timeline node dot */}
            <span
              className={`absolute -left-6 top-1.5 w-3 h-3 rounded-full border-2 border-[#0b0f0d] ${badge.dot} shadow-sm`}
            />

            <div className="zv-panel p-4 transition-all duration-150 hover:border-[#2ea87f]/40">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span
                    className={`text-[11px] font-mono uppercase px-2 py-0.5 rounded border ${badge.bg} ${badge.text} ${badge.border}`}
                  >
                    {badge.label}
                  </span>
                  <span className="text-xs text-[#8a9490]">{dateStr}</span>
                </div>
                {evt.details && Object.keys(evt.details).length > 0 && (
                  <button
                    onClick={() => setExpandedId(isExpanded ? null : evt.id)}
                    className="text-xs text-[#c9a24b] hover:text-[#e3c884] font-mono cursor-pointer"
                  >
                    {isExpanded ? "Hide Details ▲" : "View Details ▼"}
                  </button>
                )}
              </div>

              <div className="mt-2 text-sm text-[#ece8dd] font-medium leading-relaxed">
                {evt.summary}
              </div>

              {isExpanded && evt.details && (
                <div className="mt-3 pt-3 border-t border-[#24302a] text-xs">
                  <div className="font-mono text-[#8a9490] mb-1.5">Structured Event Data:</div>
                  <pre className="bg-[#0b0f0d] p-3 rounded border border-[#24302a] overflow-x-auto text-[#ece8dd] font-mono leading-relaxed">
                    {JSON.stringify(evt.details, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
