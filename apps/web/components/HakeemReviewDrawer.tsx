"use client";

import React, { useState, useEffect, useCallback } from "react";
import { hakeemApi, type HakeemConsultOut } from "@/lib/hakeemApi";
import type { PatientRecord } from "@/lib/clinicalApi";

interface HakeemReviewDrawerProps {
  token: string;
  patient: PatientRecord;
  isOpen: boolean;
  onClose: () => void;
  onConvertToNuskha?: (consultation: HakeemConsultOut) => void;
}

const SECTION_ORDER = [
  "CLINICAL SUMMARY",
  "WHAT IS KNOWN",
  "UNANI PERSPECTIVE",
  "BIOMEDICAL PERSPECTIVE",
  "DIFFERENTIAL CONSIDERATIONS",
  "RED FLAGS",
  "MISSING INFORMATION",
  "EVIDENCE",
  "SAFETY",
  "POSSIBLE CARE OPTIONS",
  "MONITORING",
  "UNCERTAINTY",
  "CLINICIAN REVIEW REQUIRED",
];

export function HakeemReviewDrawer({
  token,
  patient,
  isOpen,
  onClose,
  onConvertToNuskha,
}: HakeemReviewDrawerProps) {
  const [chiefComplaint, setChiefComplaint] = useState("");
  const [organAxis, setOrganAxis] = useState("mida");
  const [isConsulting, setIsConsulting] = useState(false);
  const [consultError, setConsultError] = useState<string | null>(null);

  const [consultations, setConsultations] = useState<HakeemConsultOut[]>([]);
  const [selectedConsultation, setSelectedConsultation] = useState<HakeemConsultOut | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  const [isMarkingReviewed, setIsMarkingReviewed] = useState(false);

  // Fetch consultation history
  const loadHistory = useCallback(async () => {
    if (!patient?.id) return;
    try {
      setIsLoadingHistory(true);
      const res = await hakeemApi.listConsultationsForPatient(token, patient.id);
      setConsultations(res);
      if (res.length > 0 && !selectedConsultation) {
        setSelectedConsultation(res[0]);
      }
    } catch {
      // ignore
    } finally {
      setIsLoadingHistory(false);
    }
  }, [patient?.id, token, selectedConsultation]);

  useEffect(() => {
    if (isOpen && patient?.id) {
      loadHistory();
    }
  }, [isOpen, patient?.id, loadHistory]);

  if (!isOpen) return null;

  const handleStartConsultation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chiefComplaint.trim()) return;

    try {
      setIsConsulting(true);
      setConsultError(null);
      const consult = await hakeemApi.consult(token, {
        patient_id: patient.id,
        chief_complaint: chiefComplaint,
        organ_axis: organAxis,
      });
      setSelectedConsultation(consult);
      setConsultations((prev) => [consult, ...prev]);
      setChiefComplaint("");
    } catch (err: unknown) {
      setConsultError(err instanceof Error ? err.message : "Consultation request failed");
    } finally {
      setIsConsulting(false);
    }
  };

  const handleMarkReviewed = async () => {
    if (!selectedConsultation) return;
    try {
      setIsMarkingReviewed(true);
      const updated = await hakeemApi.markReviewed(token, selectedConsultation.id);
      setSelectedConsultation(updated);
      setConsultations((prev) =>
        prev.map((c) => (c.id === updated.id ? updated : c))
      );
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to mark reviewed");
    } finally {
      setIsMarkingReviewed(false);
    }
  };

  const getSectionStyle = (sectionKey: string) => {
    switch (sectionKey) {
      case "RED FLAGS":
        return "border-red-600/70 bg-red-950/30 text-red-200";
      case "SAFETY":
        return "border-amber-600/70 bg-amber-950/30 text-amber-200";
      case "UNCERTAINTY":
        return "border-purple-600/70 bg-purple-950/20 text-purple-200";
      case "MISSING INFORMATION":
        return "border-blue-600/70 bg-blue-950/20 text-blue-200";
      case "CLINICIAN REVIEW REQUIRED":
        return "border-[#c9a24b] bg-[#1a1811] text-[#e3c884]";
      default:
        return "border-[#24302a] bg-[#171d17] text-[#ece8dd]";
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden flex justify-end bg-black/60 backdrop-blur-xs">
      <div className="w-full max-w-2xl bg-[#121712] border-l border-[#24302a] h-full flex flex-col shadow-2xl">
        {/* Header */}
        <div className="p-5 border-b border-[#24302a] flex items-center justify-between bg-[#0b0f0d]">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs px-2 py-0.5 rounded font-mono bg-emerald-950 text-emerald-300 border border-emerald-700">
                AI CLINICAL CO-PILOT
              </span>
              <h2 className="text-base font-serif font-bold text-[#e3c884]">
                Hakeem Sahab™
              </h2>
            </div>
            <p className="text-xs text-[#8a9490] mt-1">
              Patient: {patient.first_name} {patient.last_name} · MRN: {patient.mrn}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-[#8a9490] hover:text-white rounded-md cursor-pointer text-lg font-bold"
          >
            ✕
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-5 space-y-6">
          {/* New Consultation Prompt */}
          <div className="zv-panel p-4 border border-[#2ea87f]/30">
            <h4 className="text-xs font-semibold uppercase text-[#2ea87f] mb-2 font-mono">
              Request AI Integrative Consultation
            </h4>
            <form onSubmit={handleStartConsultation} className="space-y-3">
              <div>
                <label className="zv-label">Chief Complaint &amp; Clinical Context</label>
                <textarea
                  value={chiefComplaint}
                  onChange={(e) => setChiefComplaint(e.target.value)}
                  placeholder="Describe patient's symptoms, duration, aggravating factors, pulse (Nabz), and tongue (Lisan) observations..."
                  className="zv-input text-xs h-20"
                  required
                />
              </div>
              <div className="flex items-center justify-between gap-3">
                <div className="flex-1">
                  <label className="zv-label">Suspected Organ Axis</label>
                  <select
                    value={organAxis}
                    onChange={(e) => setOrganAxis(e.target.value)}
                    className="zv-input text-xs"
                  >
                    <option value="mida">Mida (Gastric / GI)</option>
                    <option value="kabid">Kabid (Hepato-Biliary)</option>
                    <option value="qalb">Qalb (Cardiovascular)</option>
                    <option value="dimagh">Dimagh / Asab (Neurological)</option>
                    <option value="kulyah">Kulyah (Renal / Urinary)</option>
                    <option value="riya">Riya (Pulmonary / Respiratory)</option>
                  </select>
                </div>
                <div className="pt-4">
                  <button
                    type="submit"
                    disabled={isConsulting || !chiefComplaint.trim()}
                    className="zv-btn-primary text-xs cursor-pointer disabled:opacity-50"
                  >
                    {isConsulting ? "Analyzing Evidence..." : "✨ Run Consultation"}
                  </button>
                </div>
              </div>
            </form>
            {consultError && (
              <p className="text-xs text-red-400 mt-2 bg-red-950/40 p-2 rounded border border-red-800">
                {consultError}
              </p>
            )}
          </div>

          {/* Past Consultations Selector */}
          {consultations.length > 0 && (
            <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
              <span className="text-[#8a9490] font-mono shrink-0">Consultations ({consultations.length}):</span>
              {consultations.map((c) => {
                const active = selectedConsultation?.id === c.id;
                const dt = new Date(c.created_at).toLocaleDateString(undefined, {
                  month: "short",
                  day: "numeric",
                });
                return (
                  <button
                    key={c.id}
                    onClick={() => setSelectedConsultation(c)}
                    className={`px-2.5 py-1 rounded text-xs font-mono shrink-0 cursor-pointer border ${
                      active
                        ? "bg-[#c9a24b] text-[#06120c] font-bold border-[#e3c884]"
                        : "bg-[#171d17] text-[#8a9490] border-[#24302a] hover:border-[#8a9490]"
                    }`}
                  >
                    {dt}: {c.chief_complaint.slice(0, 18)}...
                  </button>
                );
              })}
            </div>
          )}

          {/* Selected Consultation View */}
          {selectedConsultation ? (
            <div className="space-y-4">
              {/* Consultation Metadata & Actions */}
              <div className="flex flex-wrap items-center justify-between gap-3 p-3 rounded bg-[#0b0f0d] border border-[#24302a]">
                <div className="text-xs">
                  <div className="text-[#8a9490]">
                    Axis: <strong className="text-white uppercase font-mono">{selectedConsultation.organ_axis}</strong> ·
                    Recorded: {new Date(selectedConsultation.created_at).toLocaleString()}
                  </div>
                  <div className="mt-1">
                    Status:{" "}
                    {selectedConsultation.reviewed_by_clinician ? (
                      <span className="text-emerald-400 font-semibold font-mono">
                        ✓ Reviewed by Clinician
                      </span>
                    ) : (
                      <span className="text-amber-400 font-semibold font-mono">
                        ⚠️ Pending Clinician Review
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {!selectedConsultation.reviewed_by_clinician && (
                    <button
                      onClick={handleMarkReviewed}
                      disabled={isMarkingReviewed}
                      className="px-3 py-1 rounded text-xs font-semibold bg-[#1f6f54] hover:bg-[#2ea87f] text-[#06120c] cursor-pointer"
                    >
                      {isMarkingReviewed ? "Updating..." : "Mark Reviewed"}
                    </button>
                  )}
                  {onConvertToNuskha && (
                    <button
                      onClick={() => onConvertToNuskha(selectedConsultation)}
                      className="px-3 py-1 rounded text-xs font-semibold bg-[#c9a24b] hover:bg-[#e3c884] text-[#06120c] cursor-pointer"
                    >
                      Draft Nuskha →
                    </button>
                  )}
                </div>
              </div>

              {/* Candidate Mufradat Chips */}
              {selectedConsultation.candidate_mufradat &&
                selectedConsultation.candidate_mufradat.length > 0 && (
                  <div className="p-3 rounded bg-[#171d17] border border-[#24302a]">
                    <span className="text-[11px] font-mono uppercase text-[#8a9490] block mb-1.5">
                      Identified Candidate Mufradat:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedConsultation.candidate_mufradat.map((m, idx) => {
                        const name = (m.name as string) || (m.canonical_name as string) || "Mufrad";
                        return (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded text-xs font-medium bg-[#121712] text-[#2ea87f] border border-[#1f6f54]/50"
                          >
                            {name}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                )}

              {/* 13 Structured Sections */}
              <div className="space-y-3">
                {SECTION_ORDER.map((secName) => {
                  const content =
                    selectedConsultation.parsed_sections?.[secName] ||
                    (selectedConsultation.raw_response?.includes(secName)
                      ? "Present in unstructured report."
                      : null);

                  if (!content) return null;

                  return (
                    <div
                      key={secName}
                      className={`p-3.5 rounded-lg border text-xs leading-relaxed ${getSectionStyle(
                        secName
                      )}`}
                    >
                      <h5 className="font-mono text-[11px] uppercase font-bold tracking-wider mb-1 opacity-90">
                        {secName}
                      </h5>
                      <div className="whitespace-pre-line text-xs font-normal">
                        {content}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : isLoadingHistory ? (
            <div className="text-center py-10 text-xs text-[#8a9490]">
              Loading previous consultations...
            </div>
          ) : (
            <div className="text-center py-12 text-xs text-[#8a9490] zv-panel">
              No clinical consultation selected. Submit a chief complaint above to begin.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
