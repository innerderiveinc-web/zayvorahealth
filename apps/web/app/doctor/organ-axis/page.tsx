"use client";

import React, { useState, useEffect } from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

interface OrganAxis {
  id: string;
  arabic_name: string;
  body_system: string;
  governing_power: string;
  key_diseases: string[];
  primary_products: string[];
  regulatory_track: string;
  description: string;
}

interface ScoreResult {
  primary_axis: string;
  primary_score: number;
  secondary_axis?: string;
  secondary_score?: number;
  clinical_strategy: string;
  recommendations: Array<{
    role: string;
    axis: string;
    score: number;
    products: string[];
    phase: string;
  }>;
}

const DEFAULT_AXES: OrganAxis[] = [
  {
    id: "Qalb-Uroq",
    arabic_name: "Qalb wa Urooq (Cardiovascular)",
    body_system: "Cardio-Vascular",
    governing_power: "Quwwat-e-Haiwaniyah (Vital Faculty)",
    key_diseases: ["Hypertension", "Ischaemic Heart Disease (IHD)", "Palpitations", "Arrhythmia"],
    primary_products: ["HyperCalm", "CardioGuard", "LipidClear"],
    regulatory_track: "AYUSH preferred",
    description: "Cardiovascular and vascular network governing circulation, blood pressure, and arterial elasticity."
  },
  {
    id: "Jigar-Banas",
    arabic_name: "Jigar wa Banqaras (Hepato-Pancreatic)",
    body_system: "Hepato-Metabolic",
    governing_power: "Quwwat-e-Tabi'iyah (Natural/Metabolic Faculty)",
    key_diseases: ["Diabetes Type 2", "NAFLD", "Fatty Liver", "Metabolic Syndrome", "Insulin Resistance"],
    primary_products: ["DiabEase", "HepaClear", "LipidClear", "MetaboBurn-M"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Hepatic and pancreatic metabolic axis regulating glucose homeostasis, glycogen storage, and intermediate metabolism."
  },
  {
    id: "Dimagh-Qalb",
    arabic_name: "Dimagh wa Qalb (Neuro-Cardiac)",
    body_system: "Neuro-Cardiac",
    governing_power: "Quwwat-e-Nafsaniyah wa Haiwaniyah",
    key_diseases: ["Anxiety", "Depression", "Insomnia", "Stress", "Burnout", "Cardioneurosis"],
    primary_products: ["MindBalance", "Sleep+Stress"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Central nervous system, HPA axis, and cardiac autonomic interface governing emotional and sleep regulation."
  },
  {
    id: "Riya-Sadr",
    arabic_name: "Riya wa Sadr (Pulmo-Respiratory)",
    body_system: "Pulmo-Respiratory",
    governing_power: "Quwwat-e-Tanaffusiyah (Respiratory Faculty)",
    key_diseases: ["Asthma", "COPD", "Chronic Bronchitis", "Allergic Rhinitis"],
    primary_products: ["LungEase", "Immunity"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Pulmonary parenchyma, tracheobronchial tree, and respiratory immune barrier."
  },
  {
    id: "Meda-Hazm",
    arabic_name: "Meda wa Hazm (Gastro-Intestinal)",
    body_system: "Gastro-Intestinal",
    governing_power: "Quwwat-e-Hazima (Digestive Faculty)",
    key_diseases: ["IBS", "GERD", "Gastritis", "Dysbiosis", "Chronic Constipation"],
    primary_products: ["GutEase-IBS", "HepaClear"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Gastric concoction, upper GI mucosal barrier, and enteric nervous system."
  },
  {
    id: "Mafasil-Azam",
    arabic_name: "Mafasil wa Azam (Musculo-Skeletal)",
    body_system: "Musculo-Skeletal",
    governing_power: "Quwwat-e-Muharrika (Locomotor Faculty)",
    key_diseases: ["Osteoarthritis", "Rheumatoid Arthritis", "Gout", "Cervical Spondylosis"],
    primary_products: ["JointFree", "Immunity"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Synovial joints, cartilage matrix, connective tissue, and locomotor integrity."
  },
  {
    id: "Khasya-Qazeeb",
    arabic_name: "Khasya wa Qazeeb (Andrological)",
    body_system: "Male Reproductive / Andrology",
    governing_power: "Quwwat-e-Tawalludiyah (Generative Faculty)",
    key_diseases: ["Erectile Dysfunction (ED)", "Oligospermia", "Low Testosterone", "Premature Ejaculation"],
    primary_products: ["VigorX-ED", "FertiMax-M", "SemenGuard", "Night-One X", "TestoVital Classic"],
    regulatory_track: "AYUSH Rx / FSSAI",
    description: "Testicular steroidogenesis, spermatogenic epithelium, and penile vascular perfusion."
  },
  {
    id: "Reham-Mubiz",
    arabic_name: "Reham wa Mabayiz (Gynecological)",
    body_system: "Female Reproductive / Gynaecology",
    governing_power: "Quwwat-e-Tawalludiyah (Generative Faculty)",
    key_diseases: ["PCOS / PCOD", "Female Infertility", "Leucorrhoea", "Dysmenorrhoea", "Menopause"],
    primary_products: ["CycloCare-PCOS", "FertiliWomen", "LeucoClear", "UterTone", "MenoPease"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Ovarian folliculogenesis, endometrial receptivity, and hypothalamic-pituitary-ovarian axis."
  },
  {
    id: "Kulya-Masana",
    arabic_name: "Kulya wa Masana (Reno-Urinary)",
    body_system: "Reno-Urinary",
    governing_power: "Quwwat-e-Dafia (Expulsive Faculty)",
    key_diseases: ["Kidney Stones (Nephrolithiasis)", "UTI", "BPH", "Dysuria"],
    primary_products: ["UroClear", "ProstaGuard"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Renal glomeruli, tubular filtration, ureterovesical transit, and prostate stroma."
  },
  {
    id: "Darqiya-Metabolic",
    arabic_name: "Ghudda-e-Darqiya (Thyroid & Endocrine)",
    body_system: "Thyroid & Endocrine",
    governing_power: "Quwwat-e-Tabi'iyah (Basal Metabolism)",
    key_diseases: ["Hypothyroidism", "Hashimoto's", "Subclinical Hypothyroid", "Metabolic Slowdown"],
    primary_products: ["ThyroMet-W", "LipidClear"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Thyroidal hormone synthesis, T4-to-T3 deiodination, and basal cellular thermogenesis."
  },
  {
    id: "Jild-Sha'r",
    arabic_name: "Jild wa Sha'r (Dermatological)",
    body_system: "Dermatological & Trichology",
    governing_power: "Quwwat-e-Ghazia & Dafia (Dermal Secretory)",
    key_diseases: ["Telogen Effluvium", "Androgenetic Alopecia", "Eczema", "Psoriasis", "Acne"],
    primary_products: ["HairRoot-X", "HepaClear"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Follicular dermal papilla, scalp microcirculation, and cutaneous barrier keratinization."
  },
  {
    id: "Mana'at-Kulli",
    arabic_name: "Mana'at-e-Kulliyah (Vital Defense)",
    body_system: "Immune System & Vital Defense",
    governing_power: "Tabiyat Mudabbira-e-Badan (Innate Vital Defense)",
    key_diseases: ["Frequent Viral Infections", "Post-viral Fatigue", "Immunosenescence", "Autoimmune Proneness"],
    primary_products: ["Immunity", "LungEase"],
    regulatory_track: "FSSAI/AYUSH",
    description: "Reticuloendothelial system, mucosal secretory IgA, and constitutional vital reserves."
  }
];

export default function OrganAxisPage() {
  const [axes, setAxes] = useState<OrganAxis[]>(DEFAULT_AXES);
  const [scores, setScores] = useState<Record<string, number>>({
    "Jigar-Banas": 4,
    "Meda-Hazm": 3,
    "Qalb-Uroq": 2
  });
  const [scoreResult, setScoreResult] = useState<ScoreResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchFilter, setSearchFilter] = useState("");

  useEffect(() => {
    fetch("/api/v1/clinical/axes")
      .then(res => res.json())
      .then(data => {
        if (data && data.ok && Array.isArray(data.axes) && data.axes.length > 0) {
          setAxes(data.axes);
        }
      })
      .catch(() => {
        // Default fallback
      });
  }, []);

  const handleScoreChange = (axisId: string, val: number) => {
    const updated = { ...scores, [axisId]: val };
    setScores(updated);
    calculateScoring(updated);
  };

  const calculateScoring = async (currentScores: Record<string, number>) => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/clinical/axes/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scores: currentScores })
      });
      const data = await res.json();
      if (data && data.ok && data.result) {
        setScoreResult(data.result);
      }
    } catch {
      // Local fallback calculation
      const sorted = Object.entries(currentScores).filter(([_, s]) => s > 0).sort((a, b) => b[1] - a[1]);
      const primary = sorted[0] ? sorted[0][0] : "";
      const primary_s = sorted[0] ? sorted[0][1] : 0;
      const secondary = sorted[1] && sorted[1][1] >= 3 ? sorted[1][0] : undefined;
      const secondary_s = sorted[1] && sorted[1][1] >= 3 ? sorted[1][1] : undefined;
      
      const recs = [];
      if (primary) {
        const axData = axes.find(a => a.id === primary);
        recs.push({
          role: "PRIMARY",
          axis: primary,
          score: primary_s,
          products: axData ? axData.primary_products : [],
          phase: "Phase 1 Reset / Foundation"
        });
      }
      if (secondary) {
        const axData = axes.find(a => a.id === secondary);
        recs.push({
          role: "SECONDARY",
          axis: secondary,
          score: secondary_s || 0,
          products: axData ? axData.primary_products : [],
          phase: "Phase 2 Target Addition"
        });
      }
      
      setScoreResult({
        primary_axis: primary,
        primary_score: primary_s,
        secondary_axis: secondary,
        secondary_score: secondary_s,
        clinical_strategy: "Treat Primary Axis first in Phase 1 (30 days); introduce Secondary Axis in Phase 2 (60-90 days); maintain both in Phase 3.",
        recommendations: recs
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    calculateScoring(scores);
  }, []);

  const filteredAxes = axes.filter(ax => 
    ax.id.toLowerCase().includes(searchFilter.toLowerCase()) ||
    ax.body_system.toLowerCase().includes(searchFilter.toLowerCase()) ||
    ax.key_diseases.some(d => d.toLowerCase().includes(searchFilter.toLowerCase()))
  );

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border)] pb-5">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-700 border border-emerald-500/20">
                Classical Unani & Modern Systems Biology
              </span>
              <span className="text-xs text-[var(--text-muted)]">12 Canonical Axes</span>
            </div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] mt-1 tracking-tight">
              Organ-Axis Diagnostic & Scoring Matrix
            </h1>
            <p className="text-sm text-[var(--text-muted)] mt-0.5">
              Quantify constitutional pathology on a 0–5 clinical severity scale to determine Phase 1 and Phase 2 protocol pathways.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <input
              type="text"
              placeholder="Search diseases or axes..."
              value={searchFilter}
              onChange={e => setSearchFilter(e.target.value)}
              className="text-xs px-3 py-2 rounded-lg border border-[var(--border)] bg-[var(--surface)] text-[var(--text-primary)] w-56 focus:outline-none focus:ring-1 focus:ring-emerald-600"
            />
            <Link
              href="/protocols"
              className="text-xs font-medium px-4 py-2 rounded-lg bg-emerald-700 text-white hover:bg-emerald-800 transition"
            >
              View 21 Protocols →
            </Link>
          </div>
        </div>

        {/* Clinical Stratification Summary Card */}
        {scoreResult && scoreResult.primary_axis && (
          <div className="bg-gradient-to-r from-emerald-950/40 via-teal-950/30 to-[var(--surface)] border border-emerald-500/30 rounded-xl p-5 shadow-sm">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div>
                <span className="text-xs font-semibold tracking-wider text-emerald-700 uppercase">
                  Current Axis Stratification
                </span>
                <div className="flex flex-wrap items-center gap-3 mt-1.5">
                  <div className="flex items-center gap-2 bg-emerald-900/40 border border-emerald-500/40 px-3 py-1 rounded-md">
                    <span className="text-xs text-emerald-700 font-bold uppercase">Primary (Phase 1):</span>
                    <span className="text-sm font-semibold text-white">
                      {scoreResult.primary_axis} (Score: {scoreResult.primary_score}/5)
                    </span>
                  </div>
                  {scoreResult.secondary_axis && (
                    <div className="flex items-center gap-2 bg-blue-900/30 border border-blue-500/30 px-3 py-1 rounded-md">
                      <span className="text-xs text-blue-700 font-bold uppercase">Secondary (Phase 2):</span>
                      <span className="text-sm font-semibold text-white">
                        {scoreResult.secondary_axis} (Score: {scoreResult.secondary_score}/5)
                      </span>
                    </div>
                  )}
                </div>
                <p className="text-xs text-[var(--text-muted)] mt-2">
                  <span className="font-semibold text-[var(--text-primary)]">Strategy:</span> {scoreResult.clinical_strategy}
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                {scoreResult.recommendations.map((rec, idx) => (
                  <div key={idx} className="bg-[var(--surface)] border border-[var(--border)] p-2.5 rounded-lg text-xs">
                    <div className="text-[10px] uppercase font-bold text-[var(--text-muted)]">{rec.phase}</div>
                    <div className="font-semibold text-emerald-700 mt-0.5">{rec.axis}</div>
                    <div className="text-[11px] text-[var(--text-muted)] mt-1">
                      Kits/Products: <span className="text-[var(--text-primary)] font-medium">{rec.products.slice(0, 3).join(", ")}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* 12 Axes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAxes.map(ax => {
            const currentScore = scores[ax.id] || 0;
            const isPrimary = scoreResult?.primary_axis === ax.id;
            const isSecondary = scoreResult?.secondary_axis === ax.id;

            return (
              <div
                key={ax.id}
                className={`zv-card p-5 space-y-3 transition border rounded-xl relative ${
                  isPrimary
                    ? "border-emerald-500 ring-1 ring-emerald-500/50 bg-emerald-950/10"
                    : isSecondary
                    ? "border-blue-500/50 ring-1 ring-blue-500/30 bg-blue-950/10"
                    : "border-[var(--border)] hover:border-[var(--border-strong)]"
                }`}
              >
                {/* Header with Arabic */}
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-mono text-[var(--text-muted)] uppercase tracking-wider">
                      {ax.body_system}
                    </span>
                    <h3 className="font-bold text-[var(--text-primary)] text-base mt-0.5">
                      {ax.id}
                    </h3>
                  </div>
                  <span className="text-sm font-arabic font-semibold px-2 py-0.5 rounded bg-[var(--surface-accent)] text-emerald-700 border border-emerald-500/20">
                    {ax.arabic_name}
                  </span>
                </div>

                {/* Faculty / Qiwa */}
                <div className="text-xs text-[var(--text-muted)]">
                  <span className="font-medium text-[var(--text-primary)]">Governing Power:</span> {ax.governing_power}
                </div>

                {/* Description */}
                <p className="text-xs text-[var(--text-muted)] line-clamp-2 leading-relaxed">
                  {ax.description}
                </p>

                {/* Diseases Tags */}
                <div className="space-y-1">
                  <div className="text-[10px] uppercase font-bold text-[var(--text-muted)] tracking-wider">Key Target Diseases</div>
                  <div className="flex flex-wrap gap-1">
                    {ax.key_diseases.slice(0, 3).map((d, i) => (
                      <span key={i} className="text-[10px] px-2 py-0.5 rounded-full bg-[var(--surface-accent)] text-[var(--text-secondary)] border border-[var(--border)]">
                        {d}
                      </span>
                    ))}
                    {ax.key_diseases.length > 3 && (
                      <span className="text-[10px] px-1.5 py-0.5 text-[var(--text-muted)]">+{ax.key_diseases.length - 3}</span>
                    )}
                  </div>
                </div>

                {/* Primary Products */}
                <div className="space-y-1">
                  <div className="text-[10px] uppercase font-bold text-[var(--text-muted)] tracking-wider">Assigned Formulations</div>
                  <div className="text-xs text-emerald-700 font-semibold">
                    {ax.primary_products.join(" · ")}
                  </div>
                </div>

                {/* 0-5 Severity Slider */}
                <div className="pt-2 border-t border-[var(--border)] space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-medium text-[var(--text-secondary)]">Clinical Severity:</span>
                    <span className={`font-bold px-2 py-0.5 rounded text-xs ${
                      currentScore >= 4 ? "bg-red-500/20 text-red-700" :
                      currentScore >= 3 ? "bg-amber-500/20 text-amber-700" :
                      currentScore >= 1 ? "bg-emerald-500/20 text-emerald-700" :
                      "bg-gray-500/10 text-gray-700"
                    }`}>
                      {currentScore === 0 ? "0 (Unaffected)" : `${currentScore} / 5`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="1"
                    value={currentScore}
                    onChange={e => handleScoreChange(ax.id, parseInt(e.target.value))}
                    className="w-full accent-emerald-600 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-[var(--text-muted)] px-0.5">
                    <span>0 None</span>
                    <span>1 Mild</span>
                    <span>2 Low</span>
                    <span>3 Mod</span>
                    <span>4 High</span>
                    <span>5 Critical</span>
                  </div>
                </div>

                {/* Status Badges */}
                <div className="flex items-center justify-between pt-1 text-[11px]">
                  <span className="text-[var(--text-muted)]">{ax.regulatory_track}</span>
                  {isPrimary && (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-700 border border-emerald-500/30">
                      ★ PRIMARY AXIS
                    </span>
                  )}
                  {isSecondary && (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-700 border border-blue-500/30">
                      ◆ SECONDARY AXIS
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AppShell>
  );
}
