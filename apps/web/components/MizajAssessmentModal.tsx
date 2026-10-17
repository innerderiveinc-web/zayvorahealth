"use client";

import React, { useState } from "react";
import { clinicalApi, type MizajAssessmentRecord } from "@/lib/clinicalApi";

interface MizajAssessmentModalProps {
  token: string;
  patientId: string;
  patientName: string;
  isOpen: boolean;
  onClose: () => void;
  onSaved?: (assessment: MizajAssessmentRecord) => void;
}

const AJNAS_QUESTIONS = [
  {
    key: "malmas",
    title: "1. Malmas (Tactile / Skin Texture & Temperature)",
    options: [
      { id: "hot_moist", label: "Warm & Soft/Moist (Har Ratab)", humor: "Damwi" },
      { id: "hot_dry", label: "Hot & Rough/Dry (Har Yabis)", humor: "Safrawi" },
      { id: "cold_moist", label: "Cool & Flabby/Moist (Barid Ratab)", humor: "Balghami" },
      { id: "cold_dry", label: "Cold & Rough/Dry (Barid Yabis)", humor: "Saudawi" },
    ],
  },
  {
    key: "lahm_shahm",
    title: "2. Lahm wa Shahm (Musculature & Body Build)",
    options: [
      { id: "muscular_moderate", label: "Muscular, robust frame, moderate fat", humor: "Damwi" },
      { id: "lean_sinewy", label: "Lean, sinewy, prominent tendons, low fat", humor: "Safrawi" },
      { id: "heavy_adipose", label: "Heavy adipose tissue, flabby, broad", humor: "Balghami" },
      { id: "emaciated_bony", label: "Skinny, bony, prominent joints, dry", humor: "Saudawi" },
    ],
  },
  {
    key: "ashar",
    title: "3. Ash'ar (Hair Growth & Characteristics)",
    options: [
      { id: "thick_dark", label: "Thick, dark/black, fast growing, wavy", humor: "Damwi" },
      { id: "rapid_thin", label: "Thin, brownish/reddish tint, early balding", humor: "Safrawi" },
      { id: "slow_light", label: "Fine, slow growing, light/blonde, early greying", humor: "Balghami" },
      { id: "dry_curly", label: "Dry, coarse, brittle, tightly curly", humor: "Saudawi" },
    ],
  },
  {
    key: "laun",
    title: "4. Laun (Complexion)",
    options: [
      { id: "ruddy_red", label: "Ruddy, reddish, radiant, flushed", humor: "Damwi" },
      { id: "yellowish_sallow", label: "Pale yellowish, sallow, bilious hue", humor: "Safrawi" },
      { id: "chalky_pale", label: "Chalky white, pale, pasty", humor: "Balghami" },
      { id: "dark_leaden", label: "Dark, brownish, leaden, dull", humor: "Saudawi" },
    ],
  },
  {
    key: "hayat_aza",
    title: "5. Hay'at-ul-A'za (Organ Morphology & Chest Breadth)",
    options: [
      { id: "broad_strong", label: "Broad chest, strong limbs, visible prominent veins", humor: "Damwi" },
      { id: "narrow_sinewy", label: "Medium frame, prominent sinews and joints", humor: "Safrawi" },
      { id: "broad_padded", label: "Broad chest with thick soft padding, deep veins", humor: "Balghami" },
      { id: "narrow_sunken", label: "Narrow chest, sunken eyes, prominent clavicles", humor: "Saudawi" },
    ],
  },
  {
    key: "kayfiyyat_infial",
    title: "6. Kayfiyyat-ul-Infial (Emotional Reactivity & Mood)",
    options: [
      { id: "cheerful_courageous", label: "Cheerful, optimistic, courageous, sociable", humor: "Damwi" },
      { id: "quick_irritable", label: "Quick to anger, impatient, sharp, bold", humor: "Safrawi" },
      { id: "calm_sluggish", label: "Calm, placid, slow to anger, unhurried", humor: "Balghami" },
      { id: "anxious_brooding", label: "Anxious, introspective, meticulous, prone to worry", humor: "Saudawi" },
    ],
  },
  {
    key: "naum_yaqzah",
    title: "7. Naum wa Yaqzah (Sleep Pattern)",
    options: [
      { id: "moderate_sound", label: "Sound, restful, moderate (6–8 hours)", humor: "Damwi" },
      { id: "short_fitful", label: "Short, light, easily disturbed sleep", humor: "Safrawi" },
      { id: "excessive_deep", label: "Excessive, heavy, difficult to awaken (> 9 hours)", humor: "Balghami" },
      { id: "insomnia_fragmented", label: "Insomnia, fragmented sleep, early waking", humor: "Saudawi" },
    ],
  },
  {
    key: "harkat_sukoon",
    title: "8. Harkat wa Sukoon (Motor Velocity & Agility)",
    options: [
      { id: "robust_active", label: "Robust, steady pace, good physical stamina", humor: "Damwi" },
      { id: "brisk_restless", label: "Brisk, rapid, energetic, restless movements", humor: "Safrawi" },
      { id: "slow_lethargic", label: "Slow, deliberate, tires easily, prefers rest", humor: "Balghami" },
      { id: "hesitant_variable", label: "Cautious, hesitant, variable bursts of energy", humor: "Saudawi" },
    ],
  },
  {
    key: "fuzalaat",
    title: "9. Fuzalaat (Excreta & Perspiration)",
    options: [
      { id: "copious_normal", label: "Moderate sweat, normal urine and regular stool", humor: "Damwi" },
      { id: "pungent_dark", label: "Pungent warm sweat, dark yellow urine, dry stool", humor: "Safrawi" },
      { id: "cold_pale", label: "Cold clammy sweat, pale clear urine, soft/loose stool", humor: "Balghami" },
      { id: "scanty_dry", label: "Scanty sweat, cloudy or light urine, constipated stool", humor: "Saudawi" },
    ],
  },
  {
    key: "afal_aza",
    title: "10. Af'al-ul-A'za (Digestion & Pulse / Nabz)",
    options: [
      { id: "strong_full", label: "Strong appetite, fast digestion, full pulse (Mumtali)", humor: "Damwi" },
      { id: "ravenous_quick", label: "Ravenous hunger, intense thirst, rapid pulse (Sari)", humor: "Safrawi" },
      { id: "sluggish_slow", label: "Sluggish appetite, low thirst, slow deep pulse (Batee)", humor: "Balghami" },
      { id: "variable_hard", label: "Variable appetite, flatulence, hard narrow pulse (Salb)", humor: "Saudawi" },
    ],
  },
];

export function MizajAssessmentModal({
  token,
  patientId,
  patientName,
  isOpen,
  onClose,
  onSaved,
}: MizajAssessmentModalProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({
    malmas: "hot_moist",
    lahm_shahm: "muscular_moderate",
    ashar: "thick_dark",
    laun: "ruddy_red",
    hayat_aza: "broad_strong",
    kayfiyyat_infial: "cheerful_courageous",
    naum_yaqzah: "moderate_sound",
    harkat_sukoon: "robust_active",
    fuzalaat: "copious_normal",
    afal_aza: "strong_full",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState<MizajAssessmentRecord | null>(null);

  if (!isOpen) return null;

  const handleOptionChange = (key: string, optionId: string) => {
    setAnswers((prev) => ({ ...prev, [key]: optionId }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      const res = await clinicalApi.createMizajAssessment(token, patientId, answers);
      setAssessmentResult(res);
      if (onSaved) onSaved(res);
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to record Mizaj assessment");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
      <div className="zv-panel p-6 max-w-3xl w-full my-8 space-y-5 border border-[#c9a24b]/70 bg-[#121712] max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-[#24302a]">
          <div>
            <h3 className="text-base font-serif font-bold text-[#e3c884]">
              Ajnas-e-Ashara: 10-Determinant Mizaj Assessment
            </h3>
            <p className="text-xs text-[#8a9490]">
              Patient: {patientName} · Quantitative Constitutional Evaluation
            </p>
          </div>
          <button onClick={onClose} className="text-[#8a9490] hover:text-white text-lg font-bold cursor-pointer">
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto pr-1 space-y-5">
          {assessmentResult ? (
            <div className="space-y-4 p-4 rounded-lg bg-[#0b0f0d] border border-[#2ea87f]/60">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-mono uppercase text-[#8a9490]">Diagnostic Outcome:</span>
                  <h4 className="text-lg font-bold text-[#2ea87f]">
                    Primary Mizaj: {assessmentResult.primary_temperament}
                  </h4>
                  <p className="text-xs text-[#ece8dd]">
                    Secondary: <strong className="text-[#c9a24b]">{assessmentResult.secondary_temperament}</strong> · Status: {assessmentResult.su_e_mizaj}
                  </p>
                </div>
                <span className="px-3 py-1 rounded text-xs font-mono bg-[#171d17] border border-[#2ea87f] text-[#2ea87f]">
                  Degree {assessmentResult.dyscrasia_degree} Dyscrasia
                </span>
              </div>

              {/* Humor Vector Breakdown */}
              <div className="space-y-1.5 pt-2">
                <span className="text-[11px] font-mono uppercase text-[#8a9490]">
                  Quantitative Humoral Distribution (Akhlat Balance):
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                  {Object.entries(assessmentResult.distribution_percentages).map(([humor, pct]) => (
                    <div key={humor} className="p-2.5 rounded bg-[#121712] border border-[#24302a] text-center">
                      <div className="text-[11px] font-semibold text-[#8a9490]">{humor}</div>
                      <div className="text-sm font-bold text-[#e3c884] font-mono">{pct}%</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-3 flex justify-end">
                <button
                  type="button"
                  onClick={onClose}
                  className="zv-btn-primary text-xs cursor-pointer"
                >
                  Done &amp; Close
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              {AJNAS_QUESTIONS.map((q) => (
                <div key={q.key} className="p-3.5 rounded-lg bg-[#171d17] border border-[#24302a] space-y-2">
                  <h5 className="text-xs font-semibold text-[#ece8dd]">{q.title}</h5>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    {q.options.map((opt) => {
                      const selected = answers[q.key] === opt.id;
                      return (
                        <label
                          key={opt.id}
                          onClick={() => handleOptionChange(q.key, opt.id)}
                          className={`p-2.5 rounded border cursor-pointer flex items-start justify-between transition ${
                            selected
                              ? "bg-[#1f6f54]/30 border-[#2ea87f] text-white"
                              : "bg-[#121712] border-[#24302a] text-[#8a9490] hover:border-[#8a9490]"
                          }`}
                        >
                          <span className="text-[11px] font-medium leading-snug">{opt.label}</span>
                          <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-[#0b0f0d] text-[#c9a24b] ml-2 shrink-0">
                            {opt.humor}
                          </span>
                        </label>
                      );
                    })}
                  </div>
                </div>
              ))}

              <div className="flex justify-end gap-3 pt-3 border-t border-[#24302a]">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 rounded text-xs text-[#8a9490] hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="zv-btn-primary text-xs cursor-pointer disabled:opacity-50"
                >
                  {isSubmitting ? "Calculating Balance..." : "Evaluate & Record Mizaj"}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
