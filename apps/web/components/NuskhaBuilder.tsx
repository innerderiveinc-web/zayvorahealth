"use client";

import React, { useState, useEffect } from "react";
import {
  therapeuticApi,
  type NuskhaCompileResponse,
  type NuskhaDraftOut,
  type NuskhaIngredientInput,
} from "@/lib/therapeuticApi";
import { knowledgeApi, type MufradMonograph } from "@/lib/knowledgeApi";
import type { PatientRecord } from "@/lib/clinicalApi";

interface NuskhaBuilderProps {
  token: string;
  patient: PatientRecord;
  encounterId?: string;
  onDraftCreated?: (draft: NuskhaDraftOut) => void;
}

const COMMON_DOSAGE_FORMS = [
  "Safoof (Powder)",
  "Majun (Electuary)",
  "Hab (Pills)",
  "Joshanda (Decoction)",
  "Itrifal",
  "Qurs (Tablets)",
  "Sharbat (Syrup)",
  "Khamira",
  "Laooq (Linctus)",
  "Roghan (Oil)",
];

const ORGAN_AXES_OPTIONS = [
  { id: "kabid", label: "Kabid (Hepatic)" },
  { id: "mida", label: "Mida (Gastric / GI)" },
  { id: "qalb", label: "Qalb (Cardiovascular)" },
  { id: "dimagh", label: "Dimagh (Cerebral / Neuro)" },
  { id: "asab", label: "Asab (Nervous system)" },
  { id: "kulyah", label: "Kulyah (Renal / Urinary)" },
  { id: "riya", label: "Riya (Respiratory / Pulmonary)" },
];

export function NuskhaBuilder({
  token,
  patient,
  encounterId = "00000000-0000-0000-0000-000000000000",
  onDraftCreated,
}: NuskhaBuilderProps) {
  const [therapeuticObjective, setTherapeuticObjective] = useState("Muqawwi-e-Mida wa Hazim");
  const [selectedAxes, setSelectedAxes] = useState<string[]>(["mida"]);
  const [dosageForm, setDosageForm] = useState("Safoof (Powder)");
  const [dose, setDose] = useState("5g twice daily");
  const [timing, setTiming] = useState("After meals with warm water");
  const [duration, setDuration] = useState("14 days");
  const [parhez, setParhez] = useState("Avoid cold, oily, and heavy foods");

  // Ingredients state
  const [ingredients, setIngredients] = useState<NuskhaIngredientInput[]>([
    {
      name: "Zanjabeel",
      dose_mg: 1000,
      afal: "Hazim, Muqawwi-e-Mida",
      musleh: "Shahad (Honey)",
      badal: "Filfil Siyah",
      is_mudabbar: false,
    },
    {
      name: "Badiyan",
      dose_mg: 1500,
      afal: "Kasir-e-Riyah, Mudirr-e-Bawl",
      musleh: "Dhania",
      badal: "Aniseed",
      is_mudabbar: false,
    },
  ]);

  // UPI search & autocomplete
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<MufradMonograph[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // Compiler state
  const [isCompiling, setIsCompiling] = useState(false);
  const [compileResult, setCompileResult] = useState<NuskhaCompileResponse | null>(null);
  const [compileError, setCompileError] = useState<string | null>(null);

  // Save draft state
  const [isSaving, setIsSaving] = useState(false);
  const [latestDraft, setLatestDraft] = useState<NuskhaDraftOut | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);

  // Clinician override / approval modal
  const [showOverrideModal, setShowOverrideModal] = useState(false);
  const [overrideJustification, setOverrideJustification] = useState("");
  const [isApproving, setIsApproving] = useState(false);

  // Search UPI
  useEffect(() => {
    if (!searchTerm.trim() || searchTerm.length < 2) {
      setSearchResults([]);
      return;
    }
    const timer = setTimeout(async () => {
      try {
        setIsSearching(true);
        const res = await knowledgeApi.listMonographs(token, searchTerm);
        setSearchResults(res || []);
      } catch {
        setSearchResults([]);
      } finally {
        setIsSearching(false);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [searchTerm, token]);

  // Compute patient age
  const patientAge = React.useMemo(() => {
    if (!patient.date_of_birth) return 30;
    const dob = new Date(patient.date_of_birth);
    const diffMs = Date.now() - dob.getTime();
    const ageDt = new Date(diffMs);
    return Math.abs(ageDt.getUTCFullYear() - 1970);
  }, [patient.date_of_birth]);

  const handleAddIngredient = (mono?: MufradMonograph) => {
    if (mono) {
      setIngredients((prev) => [
        ...prev,
        {
          name: mono.name,
          mufrad_id: mono.id,
          dose_mg: 1000,
          afal: (mono.afal || []).join(", "),
          musleh: mono.musleh || "",
          badal: mono.badal || "",
          is_mudabbar: mono.is_schedule_e1 ? true : false,
          mizaj_temperament: mono.mizaj?.temperament || "Mutadil",
          mizaj_degree_hc: mono.mizaj?.hc_degree || 0,
          mizaj_degree_wd: mono.mizaj?.wd_degree || 0,
        },
      ]);
      setSearchTerm("");
      setSearchResults([]);
    } else {
      setIngredients((prev) => [
        ...prev,
        {
          name: "",
          dose_mg: 500,
          afal: "",
          musleh: "",
          badal: "",
          is_mudabbar: false,
        },
      ]);
    }
  };

  const handleUpdateIngredient = (index: number, field: keyof NuskhaIngredientInput, value: unknown) => {
    setIngredients((prev) => {
      const copy = [...prev];
      copy[index] = { ...copy[index], [field]: value };
      return copy;
    });
  };

  const handleRemoveIngredient = (index: number) => {
    setIngredients((prev) => prev.filter((_, i) => i !== index));
  };

  const toggleAxis = (axisId: string) => {
    setSelectedAxes((prev) =>
      prev.includes(axisId) ? prev.filter((a) => a !== axisId) : [...prev, axisId]
    );
  };

  // Compile
  const handleCompile = async () => {
    try {
      setIsCompiling(true);
      setCompileError(null);
      const res = await therapeuticApi.compileNuskha(token, {
        target_organ_axes: selectedAxes,
        therapeutic_objective: therapeuticObjective,
        patient_safety_context: {
          age: patientAge,
          pregnancy_status: patient.pregnancy_status,
          comorbidities: patient.comorbidities,
        },
        ingredients,
      });
      setCompileResult(res);
    } catch (err: unknown) {
      setCompileError(err instanceof Error ? err.message : "Compilation failed");
    } finally {
      setIsCompiling(false);
    }
  };

  // Save Draft
  const handleSaveDraft = async () => {
    try {
      setIsSaving(true);
      setSaveError(null);
      const payload = {
        patient_id: patient.id,
        encounter_id: encounterId,
        mizaj_context: { general: "Mutadil" },
        asbab: "Su-e-Mizaj Mida",
        tashkhis: therapeuticObjective,
        organ_axis_context: selectedAxes,
        usool_e_ilaj: `Tanqiya and Taqwiyat of ${selectedAxes.join(", ")}`,
        therapeutic_objective: therapeuticObjective,
        ingredients,
        dosage_form: dosageForm,
        dose,
        timing,
        duration,
        parhez,
        patient_safety_context: {
          age: patientAge,
          pregnancy_status: patient.pregnancy_status,
          comorbidities: patient.comorbidities,
        },
      };
      const draft = await therapeuticApi.createNuskhaDraft(token, payload);
      setLatestDraft(draft);
      if (onDraftCreated) onDraftCreated(draft);
    } catch (err: unknown) {
      setSaveError(err instanceof Error ? err.message : "Failed to save draft");
    } finally {
      setIsSaving(false);
    }
  };

  // Clinician Sign-off / Approve
  const handleApprove = async () => {
    if (!latestDraft) return;
    try {
      setIsApproving(true);
      const updated = await therapeuticApi.approveDraft(
        token,
        latestDraft.id,
        overrideJustification
      );
      setLatestDraft(updated);
      setShowOverrideModal(false);
      setOverrideJustification("");
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Failed to approve draft");
    } finally {
      setIsApproving(false);
    }
  };

  const getVerdictBadge = (verdict: NuskhaDraftOut["safety_verdict"]) => {
    switch (verdict) {
      case "SAFE_TO_CONSIDER":
        return {
          label: "SAFE TO CONSIDER",
          bg: "bg-emerald-950/60",
          text: "text-emerald-400",
          border: "border-emerald-600",
        };
      case "CAUTION":
        return {
          label: "CAUTION ADVISABLE",
          bg: "bg-amber-950/60",
          text: "text-amber-400",
          border: "border-amber-600",
        };
      case "MODIFY":
        return {
          label: "MODIFICATION REQUIRED",
          bg: "bg-orange-950/60",
          text: "text-orange-400",
          border: "border-orange-600",
        };
      case "DO_NOT_RECOMMEND":
        return {
          label: "DO NOT RECOMMEND",
          bg: "bg-red-950/80",
          text: "text-red-400",
          border: "border-red-600",
        };
      case "REFER":
        return {
          label: "EMERGENCY REFERRAL",
          bg: "bg-red-900",
          text: "text-white",
          border: "border-red-500",
        };
      default:
        return {
          label: verdict,
          bg: "bg-stone-900",
          text: "text-stone-300",
          border: "border-stone-700",
        };
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Objectives */}
      <div className="zv-panel p-5">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4 pb-3 border-b border-[#24302a]">
          <div>
            <h3 className="text-base font-semibold text-[#e3c884] font-serif tracking-wide">
              Nuskha Nawisi Studio (Classical Formulation Engine)
            </h3>
            <p className="text-xs text-[#8a9490]">
              Patient: {patient.first_name} {patient.last_name} (MRN: {patient.mrn}, Age: {patientAge}, Status: {patient.pregnancy_status})
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCompile}
              disabled={isCompiling || ingredients.length === 0}
              className="px-3.5 py-1.5 rounded text-xs font-semibold bg-[#1f6f54] hover:bg-[#2ea87f] text-[#06120c] transition cursor-pointer disabled:opacity-50"
            >
              {isCompiling ? "Compiling..." : "⚡ Compile & Balance"}
            </button>
            <button
              onClick={handleSaveDraft}
              disabled={isSaving || ingredients.length === 0}
              className="px-3.5 py-1.5 rounded text-xs font-semibold bg-[#c9a24b] hover:bg-[#e3c884] text-[#06120c] transition cursor-pointer disabled:opacity-50"
            >
              {isSaving ? "Saving..." : "📝 Save Draft"}
            </button>
          </div>
        </div>

        {/* Objectives & Axis Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="zv-label">Therapeutic Objective (Tashkhis / Matloob)</label>
            <input
              type="text"
              value={therapeuticObjective}
              onChange={(e) => setTherapeuticObjective(e.target.value)}
              className="zv-input text-xs"
              placeholder="e.g. Muqawwi-e-Mida wa Hazim, Musakkin-e-Dard"
            />
          </div>
          <div>
            <label className="zv-label">Target Organ Axes</label>
            <div className="flex flex-wrap gap-1.5 mt-1">
              {ORGAN_AXES_OPTIONS.map((axis) => {
                const active = selectedAxes.includes(axis.id);
                return (
                  <button
                    key={axis.id}
                    type="button"
                    onClick={() => toggleAxis(axis.id)}
                    className={`px-2 py-1 rounded text-xs transition cursor-pointer border ${
                      active
                        ? "bg-[#1f6f54] text-white border-[#2ea87f]"
                        : "bg-[#171d17] text-[#8a9490] border-[#24302a] hover:border-[#8a9490]"
                    }`}
                  >
                    {axis.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* UPI Monographs Live Search & Add */}
      <div className="zv-panel p-4">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
          <span className="text-xs font-semibold text-[#ece8dd]">Add Ingredients from UPI Pharmacopoeia</span>
          <button
            type="button"
            onClick={() => handleAddIngredient()}
            className="text-xs text-[#c9a24b] hover:text-[#e3c884] font-medium cursor-pointer"
          >
            + Add Custom Ingredient
          </button>
        </div>
        <div className="relative">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search authentic UPI single drugs (e.g. Suranjan, Asgand, Filfil, Zanjabeel)..."
            className="zv-input text-xs"
          />
          {isSearching && (
            <span className="absolute right-3 top-2.5 text-xs text-[#8a9490]">Searching UPI...</span>
          )}
          {searchResults.length > 0 && (
            <div className="absolute left-0 right-0 top-full mt-1 bg-[#121712] border border-[#24302a] rounded-lg shadow-xl z-20 max-h-56 overflow-y-auto">
              {searchResults.map((mono) => (
                <div
                  key={mono.id}
                  onClick={() => handleAddIngredient(mono)}
                  className="p-2.5 hover:bg-[#171d17] cursor-pointer border-b border-[#24302a]/50 flex items-center justify-between"
                >
                  <div>
                    <span className="font-semibold text-xs text-[#ece8dd]">{mono.name}</span>
                    <span className="text-[11px] text-[#8a9490] ml-2 italic">({mono.botanical_name})</span>
                    {mono.is_schedule_e1 && (
                      <span className="ml-2 text-[10px] font-mono px-1.5 py-0.5 rounded bg-red-950/80 text-red-400 border border-red-800">
                        Schedule E(1) Statutory Poison
                      </span>
                    )}
                  </div>
                  <span className="text-[11px] text-[#c9a24b]">
                    {mono.mizaj?.temperament || "Mutadil"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Ingredients List Table */}
      <div className="zv-panel p-4">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-[#8a9490]">
            Formulation Composition ({ingredients.length} items)
          </h4>
        </div>

        {ingredients.length === 0 ? (
          <p className="text-xs text-[#8a9490] py-4 text-center">
            No ingredients added. Search above or click &ldquo;+ Add Custom Ingredient&rdquo;.
          </p>
        ) : (
          <div className="space-y-3">
            {ingredients.map((ing, idx) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-[#171d17] border border-[#24302a] space-y-2 text-xs"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2 flex-1">
                    <span className="text-xs font-mono text-[#8a9490] w-4">{idx + 1}.</span>
                    <input
                      type="text"
                      value={ing.name}
                      onChange={(e) => handleUpdateIngredient(idx, "name", e.target.value)}
                      placeholder="Ingredient Name"
                      className="zv-input text-xs font-medium max-w-xs"
                    />
                    <div className="flex items-center gap-1.5">
                      <input
                        type="number"
                        value={ing.dose_mg || 0}
                        onChange={(e) =>
                          handleUpdateIngredient(idx, "dose_mg", parseFloat(e.target.value) || 0)
                        }
                        className="zv-input text-xs w-24 text-right"
                      />
                      <span className="text-xs text-[#8a9490]">mg</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <label className="flex items-center gap-1.5 cursor-pointer text-xs">
                      <input
                        type="checkbox"
                        checked={ing.is_mudabbar || false}
                        onChange={(e) => handleUpdateIngredient(idx, "is_mudabbar", e.target.checked)}
                        className="rounded border-[#24302a] accent-[#2ea87f]"
                      />
                      <span className={ing.is_mudabbar ? "text-[#2ea87f] font-semibold" : "text-[#8a9490]"}>
                        Mudabbar (Detoxified)
                      </span>
                    </label>
                    <button
                      type="button"
                      onClick={() => handleRemoveIngredient(idx)}
                      className="text-red-400 hover:text-red-300 font-bold px-2 py-1 cursor-pointer"
                      title="Remove ingredient"
                    >
                      ✕
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-1 border-t border-[#24302a]/60">
                  <div>
                    <span className="text-[10px] text-[#8a9490]">Af&apos;al (Action):</span>
                    <input
                      type="text"
                      value={ing.afal || ""}
                      onChange={(e) => handleUpdateIngredient(idx, "afal", e.target.value)}
                      placeholder="e.g. Hazim, Muqawwi"
                      className="zv-input text-xs mt-0.5 py-1"
                    />
                  </div>
                  <div>
                    <span className="text-[10px] text-[#8a9490]">Musleh (Corrective):</span>
                    <input
                      type="text"
                      value={ing.musleh || ""}
                      onChange={(e) => handleUpdateIngredient(idx, "musleh", e.target.value)}
                      placeholder="e.g. Shahad, Katira"
                      className="zv-input text-xs mt-0.5 py-1"
                    />
                  </div>
                  <div>
                    <span className="text-[10px] text-[#8a9490]">Badal (Substitute):</span>
                    <input
                      type="text"
                      value={ing.badal || ""}
                      onChange={(e) => handleUpdateIngredient(idx, "badal", e.target.value)}
                      placeholder="e.g. Filfil Siyah"
                      className="zv-input text-xs mt-0.5 py-1"
                    />
                  </div>
                </div>

                {ing.is_mudabbar && (
                  <div className="pt-1">
                    <span className="text-[10px] text-[#2ea87f]">Mudabbar Protocol Specification:</span>
                    <input
                      type="text"
                      value={ing.mudabbar_process || ""}
                      onChange={(e) => handleUpdateIngredient(idx, "mudabbar_process", e.target.value)}
                      placeholder="e.g. Soaked in cow's milk for 7 days, skin peeled, sun dried"
                      className="zv-input text-xs mt-0.5 py-1"
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Regimen Administration Details */}
      <div className="zv-panel p-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div>
          <label className="zv-label">Dosage Form</label>
          <select
            value={dosageForm}
            onChange={(e) => setDosageForm(e.target.value)}
            className="zv-input text-xs cursor-pointer"
          >
            {COMMON_DOSAGE_FORMS.map((df) => (
              <option key={df} value={df} className="bg-[#121712]">
                {df}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="zv-label">Dose & Administration</label>
          <input
            type="text"
            value={dose}
            onChange={(e) => setDose(e.target.value)}
            className="zv-input text-xs"
            placeholder="e.g. 5g twice daily"
          />
        </div>
        <div>
          <label className="zv-label">Timing (Auqat)</label>
          <input
            type="text"
            value={timing}
            onChange={(e) => setTiming(e.target.value)}
            className="zv-input text-xs"
            placeholder="e.g. After meals"
          />
        </div>
        <div>
          <label className="zv-label">Duration</label>
          <input
            type="text"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            className="zv-input text-xs"
            placeholder="e.g. 14 days"
          />
        </div>
        <div className="sm:col-span-2 md:col-span-4">
          <label className="zv-label">Parhez (Dietary Restrictions / Contraindications)</label>
          <input
            type="text"
            value={parhez}
            onChange={(e) => setParhez(e.target.value)}
            className="zv-input text-xs"
            placeholder="e.g. Abstain from spicy, sour, fried foods and carbonated drinks"
          />
        </div>
      </div>

      {/* Compiler Output Panel */}
      {compileError && (
        <div className="p-3 rounded bg-red-950/40 border border-red-800 text-xs text-red-300">
          Compiler Error: {compileError}
        </div>
      )}

      {compileResult && (
        <div className="zv-panel p-5 border border-[#2ea87f]/40 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[#24302a]">
            <div>
              <span className="text-xs font-serif text-[#e3c884] font-semibold">
                Nuskha Compiler Analysis Verdict
              </span>
              <p className="text-xs text-[#8a9490]">
                Juz-e-Azam (Chief Principal):{" "}
                <strong className="text-emerald-400 font-mono">
                  {compileResult.juz_e_azam || "Not designated"}
                </strong>
              </p>
            </div>
            <span
              className={`text-xs px-2.5 py-1 rounded font-mono border ${
                compileResult.is_formulation_balanced
                  ? "bg-emerald-950/50 text-emerald-300 border-emerald-700"
                  : "bg-amber-950/50 text-amber-300 border-amber-700"
              }`}
            >
              {compileResult.is_formulation_balanced
                ? "✓ Formulation Balanced"
                : "⚠ Formulation Needs Balance"}
            </span>
          </div>

          {compileResult.missing_musleh_alerts.length > 0 && (
            <div className="p-3 rounded bg-amber-950/40 border border-amber-700/60 text-xs space-y-1">
              <span className="font-semibold text-amber-300">⚠ Classical Musleh Warnings:</span>
              <ul className="list-disc list-inside text-amber-200 space-y-0.5">
                {compileResult.missing_musleh_alerts.map((alert, i) => (
                  <li key={i}>{alert}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Compiled Ingredients Breakdown */}
          <div className="space-y-2">
            <h5 className="text-[11px] font-mono uppercase text-[#8a9490]">
              Ingredient Posology & Role Allocations
            </h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              {compileResult.compiled_ingredients.map((ci, i) => (
                <div key={i} className="p-2.5 rounded bg-[#171d17] border border-[#24302a]">
                  <div className="flex justify-between items-baseline mb-1">
                    <span className="font-semibold text-[#ece8dd]">{ci.name}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#121712] border border-[#24302a] text-[#c9a24b]">
                      {ci.classical_role}
                    </span>
                  </div>
                  <div className="text-[11px] text-[#8a9490]">
                    Prescribed: {ci.prescribed_dose_mg}mg → Adjusted:{" "}
                    <span className="font-semibold text-emerald-400">
                      {ci.clinically_adjusted_dose_mg}mg
                    </span>
                  </div>
                  {ci.posology_adjustments && ci.posology_adjustments.length > 0 && (
                    <div className="text-[10px] text-amber-300/80 mt-1 italic">
                      Adjustments: {ci.posology_adjustments.join("; ")}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Latest Saved Draft & Safety Firewall Verdict */}
      {saveError && (
        <div className="p-3 rounded bg-red-950/40 border border-red-800 text-xs text-red-300">
          Save Error: {saveError}
        </div>
      )}

      {latestDraft && (
        <div className="zv-panel p-5 border border-[#c9a24b]/40 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#24302a]">
            <div>
              <span className="text-xs font-mono text-[#8a9490]">Draft ID: {latestDraft.id}</span>
              <h4 className="text-sm font-semibold text-[#e3c884]">
                Safety Firewall Verdict:{" "}
                <span
                  className={`text-xs px-2.5 py-1 rounded font-mono border ml-2 ${
                    getVerdictBadge(latestDraft.safety_verdict).bg
                  } ${getVerdictBadge(latestDraft.safety_verdict).text} ${
                    getVerdictBadge(latestDraft.safety_verdict).border
                  }`}
                >
                  {getVerdictBadge(latestDraft.safety_verdict).label}
                </span>
              </h4>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-mono uppercase text-[#8a9490]">
                Status: <strong className="text-emerald-400">{latestDraft.status}</strong>
              </span>
              {latestDraft.status === "draft" && (
                <button
                  onClick={() => setShowOverrideModal(true)}
                  className="px-3 py-1 rounded text-xs font-semibold bg-[#1f6f54] hover:bg-[#2ea87f] text-[#06120c] cursor-pointer"
                >
                  Clinician Sign-off
                </button>
              )}
            </div>
          </div>

          {latestDraft.safety_reasons && latestDraft.safety_reasons.length > 0 && (
            <div className="p-3 rounded bg-[#0b0f0d] border border-[#24302a] text-xs space-y-1">
              <span className="font-mono text-[#8a9490] text-[11px]">Safety Firewall Rationale:</span>
              <ul className="list-disc list-inside text-[#ece8dd] space-y-0.5">
                {latestDraft.safety_reasons.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          )}

          {latestDraft.safety_override_justification && (
            <div className="p-3 rounded bg-amber-950/30 border border-amber-800/40 text-xs">
              <span className="font-mono text-amber-400 font-semibold">Clinician Override Justification:</span>
              <p className="text-amber-200 mt-1 italic">{latestDraft.safety_override_justification}</p>
            </div>
          )}
        </div>
      )}

      {/* Clinician Approval & Safety Override Modal */}
      {showOverrideModal && latestDraft && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="zv-panel p-6 max-w-lg w-full space-y-4 border border-[#c9a24b]">
            <h3 className="text-base font-serif text-[#e3c884] font-semibold">
              Clinician Sign-off &amp; Prescription Authorization
            </h3>
            <p className="text-xs text-[#8a9490] leading-relaxed">
              In accordance with statutory safety guidelines and Unani clinical governance, the clinician must review all safety alerts before authorizing this formulation.
            </p>

            {(latestDraft.safety_verdict === "DO_NOT_RECOMMEND" ||
              latestDraft.safety_verdict === "REFER" ||
              latestDraft.safety_verdict === "MODIFY") && (
              <div className="p-3 rounded bg-red-950/40 border border-red-800 text-xs space-y-2">
                <span className="font-bold text-red-300">
                  ⚠️ Safety Override Required (Verdict: {latestDraft.safety_verdict})
                </span>
                <p className="text-red-200">
                  Please document your clinical justification for overriding the safety firewall, including patient consent and intended monitoring plan:
                </p>
                <textarea
                  value={overrideJustification}
                  onChange={(e) => setOverrideJustification(e.target.value)}
                  placeholder="Clinical rationale, detoxification verification, posology titration, and scheduled follow-up..."
                  className="zv-input text-xs h-24"
                  required
                />
              </div>
            )}

            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowOverrideModal(false)}
                className="px-4 py-2 rounded text-xs text-[#8a9490] hover:text-white cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleApprove}
                disabled={
                  isApproving ||
                  ((latestDraft.safety_verdict === "DO_NOT_RECOMMEND" ||
                    latestDraft.safety_verdict === "REFER") &&
                    !overrideJustification.trim())
                }
                className="zv-btn-primary text-xs cursor-pointer disabled:opacity-50"
              >
                {isApproving ? "Authorizing..." : "Authorize & Sign Prescription"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
