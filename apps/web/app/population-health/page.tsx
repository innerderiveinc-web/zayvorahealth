"use client";

import React, { useState } from "react";
import { AppShell } from "@/components/AppShell";

type SeasonKey = "MAUSIM_E_BAHAR" | "MAUSIM_E_SAIF" | "MAUSIM_E_KHAZAN" | "MAUSIM_E_SHITA";

interface SeasonalProfile {
  name: string;
  urduName: string;
  months: string;
  thermal: string;
  humor: string;
  humorBadgeColor: string;
  pathology: string;
  highRiskAmraz: string[];
  asbabGuidance: { [key: string]: string };
  tadbeerPriorities: string[];
}

const SEASONAL_DATA: Record<SeasonKey, SeasonalProfile> = {
  MAUSIM_E_BAHAR: {
    name: "Spring",
    urduName: "Mausim-e-Bahar (Spring Season)",
    months: "February – April",
    thermal: "Haar-Ratab (Moderate Warmth & Moisture)",
    humor: "Dam (Blood) & Balgham Liquefaction",
    humorBadgeColor: "bg-rose-500/20 text-rose-300 border-rose-500/30",
    pathology: "Winter-accumulated thick phlegm liquefies (Tahleel-e-Akhlat), overflowing into vascular beds and triggering plethora (Imtila-e-Damawi).",
    highRiskAmraz: [
      "Waja-ul-Mafasil (Joint Inflammation Exacerbation)",
      "Nazla-o-Zukam (Allergic Rhinitis & Sinusitis)",
      "Ruaf (Epistaxis)",
      "Dumameel (Cutaneous Boils & Eruptions)"
    ],
    asbabGuidance: {
      "Hawa (Air)": "Mildly warming spring air; avoid sudden exposure to chilled dawn winds.",
      "Makul-o-Mashroob (Food & Drink)": "Taqlil-e-Ghiza (caloric reduction); restrict heavy meats, cold dairy, and viscous sweets.",
      "Harakat-o-Sukoon (Movement)": "Riyazat-e-Khafifa: Brisk morning walks before midday heat.",
      "Istifragh (Evacuation)": "Prime window for Tanqiya-e-Mawad (cleansing of morbid humors) via mild Munzij-Mushil regimens."
    },
    tadbeerPriorities: [
      "Fasd (Venesection) or Hijama (Wet Cupping) for sanguine plethora",
      "Drink lukewarm water boiled with Zanjabeel or Zeera",
      "Avoid daytime sleep (Naum-e-Nahar)",
      "Prophylactic Munzij-e-Balgham tea"
    ]
  },
  MAUSIM_E_SAIF: {
    name: "Summer",
    urduName: "Mausim-e-Saif (Summer Season)",
    months: "May – July",
    thermal: "Haar-Yabis (Intense Heat & Desiccation)",
    humor: "Safra (Yellow Bile)",
    humorBadgeColor: "bg-amber-500/20 text-amber-300 border-amber-500/30",
    pathology: "Extreme atmospheric solar radiation inflames bilious humors, exhausts innate moisture (Rutoobat-e-Ghariziyya) and triggers systemic dehydration.",
    highRiskAmraz: [
      "Huma-e-Safrawiyya (Bilious Heat Fevers)",
      "Ishaal (Summer Diarrheal Episodes)",
      "Su-e-Hazm Safrawi (Heartburn / Acid Gastritis)",
      "Suda-e-Haar (Heat Cephalea / Migraine)"
    ],
    asbabGuidance: {
      "Hawa (Air)": "Hot desiccating winds (Loo); remain in shaded, ventilated quarters.",
      "Makul-o-Mashroob (Food & Drink)": "Hydrating cooling diet: Sikanjabeen, Arq-e-Gulab, watermelon, pomegranate.",
      "Harakat-o-Sukoon (Movement)": "Avoid strenuous mid-day labor; exercise only at dawn or dusk.",
      "Istifragh (Evacuation)": "Strictly avoid drastic purgation; use gentle emollients (Turanjabeen, Shirkhisht)."
    },
    tadbeerPriorities: [
      "Sikanjabeen Sada and Sharbat Bazoori Motadil daily",
      "Lukewarm Hammam with rose water infusion",
      "Abstain from red chilies, mustard oil, and fried savories",
      "External application of Sandal and Arq-e-Gulab on forehead"
    ]
  },
  MAUSIM_E_KHAZAN: {
    name: "Autumn",
    urduName: "Mausim-e-Khazan (Autumn Season)",
    months: "August – October",
    thermal: "Barid-Yabis (Cold & Dryness)",
    humor: "Sawda (Black Bile)",
    humorBadgeColor: "bg-purple-500/20 text-purple-300 border-purple-500/30",
    pathology: "Sharp diurnal temperature swings and dry winds cause combustion residues of bile to precipitate into melancholic black bile (Ihtiraq-e-Akhlat).",
    highRiskAmraz: [
      "Malikhulia (Melancholic Anxiety & Depressive Stasis)",
      "Waja-ul-Warik (Sciatic Neuralgia)",
      "Bawaseer (Anorectal Stasis & Hemorrhoids)",
      "Qabz-e-Muzmin (Chronic Obstipation)"
    ],
    asbabGuidance: {
      "Hawa (Air)": "Diurnal volatility; dress in breathable thermal layers to shield against sudden evening chill.",
      "Makul-o-Mashroob (Food & Drink)": "Murattib (moistening) foods: Almond milk, mutton broth, spinach, dates.",
      "Harakat-o-Sukoon (Movement)": "Moderate rhythmic exercises to kindle internal innate heat.",
      "Istifragh (Evacuation)": "Evacuate burnt humors using Itrifal Ustukhuddus or Aftimoon."
    },
    tadbeerPriorities: [
      "Inshaaq (Nasal instillation of Roghan-e-Badam Shirin)",
      "Strictly avoid dry beef, brinjal (eggplant), and lentils",
      "Gentle oil massage (Dalk-e-Layeena) before sleep",
      "Uplifting social gatherings to dispel melancholia"
    ]
  },
  MAUSIM_E_SHITA: {
    name: "Winter",
    urduName: "Mausim-e-Shita (Winter Season)",
    months: "November – January",
    thermal: "Barid-Ratab (Cold & Moisture)",
    humor: "Balgham (Phlegm Accumulation)",
    humorBadgeColor: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
    pathology: "External cold closes dermal pores, concentrating innate heat inwardly (Hazm strengthens, but peripheral vascular stasis increases phlegmatic accumulation).",
    highRiskAmraz: [
      "Waja-ul-Mafasil-e-Barid (Cold-Aggravated Osteoarthritis)",
      "Zeeq-un-Nafas (Asthmatic Bronchoconstriction)",
      "Falij-o-Laqwa (Stroke & Facial Palsy Risk)",
      "Taqattur-ul-Baul (Urinary Incontinence in Elderly)"
    ],
    asbabGuidance: {
      "Hawa (Air)": "Pungent, cold, damp atmosphere; seek warmth and sun exposure.",
      "Makul-o-Mashroob (Food & Drink)": "Nutritious, warming diet: Harira, ginger tea, saffron broths, walnuts.",
      "Harakat-o-Sukoon (Movement)": "Vigorous indoor physical movement to enhance peripheral perfusion.",
      "Istifragh (Evacuation)": "Use warming expectorants (Joshina) and mild carminatives."
    },
    tadbeerPriorities: [
      "Nutool (warm herbal decoction irrigation) on aching joints",
      "Steam inhalation with Barg-e-Bansa and Qust Shirin",
      "Avoid raw salads, refrigerated dairy, and night curd",
      "Regular application of Roghan-e-Suranjan on joints"
    ]
  }
};

export default function PopulationHealthPage() {
  const [activeSeason, setActiveSeason] = useState<SeasonKey>("MAUSIM_E_BAHAR");
  const [activeSubTab, setActiveSubTab] = useState<"surveillance" | "epidemiology" | "adr-monitor" | "abdm-fhir">("surveillance");
  const [quarantineActive, setQuarantineActive] = useState(true);

  const currentSeasonData = SEASONAL_DATA[activeSeason];

  const HUMORAL_COHORT = [
    { name: "Balgham (Phlegmatic)", percentage: 38.5, count: 385, color: "bg-cyan-500", topAmraz: "Waja-ul-Mafasil", meanAge: 52.4, remissionRate: "89.1%" },
    { name: "Safra (Bilious)", percentage: 27.0, count: 270, color: "bg-amber-500", topAmraz: "Su-e-Hazm & Gastritis", meanAge: 36.8, remissionRate: "93.4%" },
    { name: "Dam (Sanguine)", percentage: 20.5, count: 205, color: "bg-rose-500", topAmraz: "Hypertension & Plethora", meanAge: 44.1, remissionRate: "91.8%" },
    { name: "Sawda (Melancholic)", percentage: 14.0, count: 140, color: "bg-purple-500", topAmraz: "Malikhulia & Chronic Pain", meanAge: 49.6, remissionRate: "84.2%" },
  ];

  return (
    <AppShell activeRole="admin">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-[var(--border)] pb-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              <span>🌍</span> Population Health & Seasonal Humoral Surveillance
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                Sequence 16 & 14
              </span>
            </h1>
            <p className="text-xs text-[var(--muted)] mt-1">
              Cohort temperament epidemiology, canonical Asbab-e-Sittah seasonal surveillance, multi-clinic pharmacovigilance, and ABDM FHIR R4 interoperability.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveSubTab("surveillance")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeSubTab === "surveillance" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              🍃 Seasonal Asbab-e-Sittah
            </button>
            <button
              onClick={() => setActiveSubTab("epidemiology")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeSubTab === "epidemiology" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              📊 Humoral Cohorts
            </button>
            <button
              onClick={() => setActiveSubTab("adr-monitor")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeSubTab === "adr-monitor" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              ⚠️ ADR Cluster Safety
            </button>
            <button
              onClick={() => setActiveSubTab("abdm-fhir")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeSubTab === "abdm-fhir" ? "bg-teal-600 text-white" : "bg-[var(--panel)] text-[var(--muted)] hover:text-white border border-[var(--border)]"}`}
            >
              🇮🇳 ABDM / FHIR R4
            </button>
          </div>
        </div>

        {/* SUBTAB 1: Seasonal Asbab-e-Sittah Surveillance */}
        {activeSubTab === "surveillance" && (
          <div className="space-y-6">
            
            {/* Season Selector Chips */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2">
              {(Object.keys(SEASONAL_DATA) as SeasonKey[]).map((key) => {
                const s = SEASONAL_DATA[key];
                const isActive = activeSeason === key;
                return (
                  <button
                    key={key}
                    onClick={() => setActiveSeason(key)}
                    className={`px-4 py-2 rounded-xl text-xs font-bold border transition flex items-center gap-2 whitespace-nowrap ${
                      isActive
                        ? "bg-teal-600/30 border-teal-500 text-white shadow-md"
                        : "bg-[var(--panel)] border-[var(--border)] text-[var(--muted)] hover:text-white"
                    }`}
                  >
                    <span>{key === "MAUSIM_E_BAHAR" ? "🌸" : key === "MAUSIM_E_SAIF" ? "☀️" : key === "MAUSIM_E_KHAZAN" ? "🍂" : "❄️"}</span>
                    <span>{s.name} ({s.months})</span>
                  </button>
                );
              })}
            </div>

            {/* Active Season Banner */}
            <div className="bg-[var(--panel)] p-6 rounded-2xl border border-[var(--border)] space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div>
                  <h2 className="text-xl font-bold text-white flex items-center gap-2">
                    {currentSeasonData.urduName}
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${currentSeasonData.humorBadgeColor}`}>
                      Dominant Humor: {currentSeasonData.humor}
                    </span>
                  </h2>
                  <div className="text-xs text-[var(--muted)] mt-1 flex items-center gap-3">
                    <span>🌡️ Thermal Dynamic: <strong className="text-white">{currentSeasonData.thermal}</strong></span>
                    <span>•</span>
                    <span>📅 Period: <strong className="text-white">{currentSeasonData.months}</strong></span>
                  </div>
                </div>

                <div className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  Active Surveillance Broadcast Live
                </div>
              </div>

              <div className="p-4 bg-[var(--background)] rounded-xl border border-[var(--border)] text-xs text-zinc-300 leading-relaxed">
                <strong className="text-white block mb-1">Pathophysiological Mechanism (Nafs-e-Amraz):</strong>
                {currentSeasonData.pathology}
              </div>

              {/* High Risk Amraz & Regimental Priorities */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div className="bg-[var(--background)] p-4 rounded-xl border border-[var(--border)] space-y-2">
                  <h3 className="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                    <span>⚠️</span> High-Risk Seasonal Amraz (Diseases)
                  </h3>
                  <ul className="space-y-1.5 text-xs text-zinc-300">
                    {currentSeasonData.highRiskAmraz.map((amraz, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <span className="text-teal-400">•</span> {amraz}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-[var(--background)] p-4 rounded-xl border border-[var(--border)] space-y-2">
                  <h3 className="text-xs font-bold text-teal-400 flex items-center gap-1.5">
                    <span>🌿</span> Priority Tadbeer & Parhez Directives
                  </h3>
                  <ul className="space-y-1.5 text-xs text-zinc-300">
                    {currentSeasonData.tadbeerPriorities.map((tadbeer, i) => (
                      <li key={i} className="flex items-center gap-2">
                        <span className="text-teal-400">✓</span> {tadbeer}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* 6 Essential Factors Grid */}
              <div className="pt-2">
                <h3 className="text-xs font-bold text-white mb-2">Canonical Asbab-e-Sittah Zarooriyyah Guidance:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  {Object.entries(currentSeasonData.asbabGuidance).map(([factor, guidance], i) => (
                    <div key={i} className="bg-[var(--background)] p-3 rounded-lg border border-[var(--border)] text-xs space-y-1">
                      <div className="font-bold text-teal-300 text-[11px]">{factor}</div>
                      <div className="text-[var(--muted)] text-[11px] leading-snug">{guidance}</div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </div>
        )}

        {/* SUBTAB 2: Cohort Humoral Epidemiology */}
        {activeSubTab === "epidemiology" && (
          <div className="space-y-6">
            <div className="text-sm font-semibold text-white flex justify-between items-center">
              <span>Cohort Humoral Stratification (1,000 Verified Patients across 4 Clinics)</span>
              <span className="text-xs text-[var(--muted)]">Continuous RWE Outcome Sync</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {HUMORAL_COHORT.map((c, i) => (
                <div key={i} className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-3 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-white">{c.name}</span>
                      <span className="text-lg font-extrabold text-white">{c.percentage}%</span>
                    </div>

                    <div className="w-full h-2 bg-[var(--background)] rounded-full overflow-hidden mt-2">
                      <div className={`h-full ${c.color}`} style={{ width: `${c.percentage}%` }}></div>
                    </div>

                    <div className="space-y-1.5 mt-4 text-xs">
                      <div className="flex justify-between text-[var(--muted)]">
                        <span>Cohort Count:</span>
                        <span className="text-white font-mono">{c.count} patients</span>
                      </div>
                      <div className="flex justify-between text-[var(--muted)]">
                        <span>Mean Age:</span>
                        <span className="text-white font-mono">{c.meanAge} yrs</span>
                      </div>
                      <div className="flex justify-between text-[var(--muted)]">
                        <span>Top Indication:</span>
                        <span className="text-teal-300 font-semibold">{c.topAmraz}</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-[var(--border)] flex justify-between items-center text-xs">
                    <span className="text-[var(--muted)]">Remission (Kamil):</span>
                    <span className="font-bold text-emerald-400 font-mono">{c.remissionRate}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-3">
              <h3 className="text-sm font-bold text-white">Dominant Epidemiological Dyscrasia Finding</h3>
              <p className="text-xs text-zinc-300 leading-relaxed">
                Multi-clinic aggregation identifies <strong className="text-cyan-400">Balgham-e-Ghaleez (Cold-Moist Phlegmatic Congestion)</strong> as the primary population-level pathology, accounting for 38.5% of overall outpatient presentations. This correlates directly with high clinical incidence of *Waja-ul-Mafasil* (Osteoarthritis) and metabolic dysregulation, validating the priority deployment of *Suranjan*, *Asgandh*, and *Munzij-e-Balgham* regimens.
              </p>
            </div>
          </div>
        )}

        {/* SUBTAB 3: Pharmacovigilance Cluster Early Warning */}
        {activeSubTab === "adr-monitor" && (
          <div className="space-y-6">
            <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div>
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <span>🚨</span> Multi-Clinic Pharmacovigilance Early Warning Radar
                  </h3>
                  <p className="text-xs text-[var(--muted)] mt-0.5">
                    Automated cluster detection flags batch lots exceeding adverse event thresholds across 2+ distinct clinic facilities.
                  </p>
                </div>
                {quarantineActive ? (
                  <span className="px-3 py-1 rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/40 text-xs font-bold flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping"></span>
                    CRITICAL_SAFETY_HOLD ACTIVE
                  </span>
                ) : (
                  <span className="px-3 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-bold">
                    QUARANTINE RESOLVED
                  </span>
                )}
              </div>

              {/* Seeded Incident Cluster */}
              <div className="p-4 bg-rose-950/20 border border-rose-500/40 rounded-xl space-y-3">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                  <div>
                    <h4 className="text-sm font-bold text-rose-300">Cluster #CLUST-04921: Suranjan Talkh (Colchicum luteum)</h4>
                    <div className="text-xs text-[var(--muted)]">Lot Batch: <strong className="text-white font-mono">B-SURT-2026-X1</strong> (Schedule E1 Poison)</div>
                  </div>
                  <div className="text-xs text-rose-400 font-mono font-bold">3 Reported Adverse Events</div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                  <div className="bg-[var(--background)] p-2.5 rounded-lg border border-[var(--border)]">
                    <span className="text-[var(--muted)] block text-[10px]">Reporting Nodes:</span>
                    <span className="text-white font-semibold">FAC-DEL-CENTRAL-01 (2), FAC-HYD-REGIONAL-02 (1)</span>
                  </div>
                  <div className="bg-[var(--background)] p-2.5 rounded-lg border border-[var(--border)]">
                    <span className="text-[var(--muted)] block text-[10px]">Dominant Symptoms:</span>
                    <span className="text-white font-semibold">Acute Epigastric Burning, GI Hyper-Motility</span>
                  </div>
                  <div className="bg-[var(--background)] p-2.5 rounded-lg border border-[var(--border)]">
                    <span className="text-[var(--muted)] block text-[10px]">DSMB / Governance Status:</span>
                    <span className="text-rose-400 font-semibold">Emergency Safety Review Convened</span>
                  </div>
                </div>

                <div className="flex justify-between items-center pt-2">
                  <span className="text-xs text-[var(--muted)]">Automated Statutory Action: Wholesale quarantine on batch B-SURT-2026-X1.</span>
                  <button
                    onClick={() => setQuarantineActive(!quarantineActive)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      quarantineActive
                        ? "bg-zinc-700 hover:bg-zinc-600 text-white"
                        : "bg-rose-600 hover:bg-rose-500 text-white"
                    }`}
                  >
                    {quarantineActive ? "Acknowledge & Maintain Hold" : "Re-trigger Safety Hold"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* SUBTAB 4: ABDM / FHIR R4 Bundle Inspector */}
        {activeSubTab === "abdm-fhir" && (
          <div className="space-y-6">
            <div className="bg-[var(--panel)] p-5 rounded-xl border border-[var(--border)] space-y-4">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                <div>
                  <h3 className="text-base font-bold text-white flex items-center gap-2">
                    <span>🇮🇳</span> ABDM HL7 FHIR R4 Clinical Document Exchange
                  </h3>
                  <p className="text-xs text-[var(--muted)] mt-0.5">
                    Conforms strictly to National Resource Centre for EHR Standards (NRCeS) OPConsultRecord and PrescriptionRecord profiles.
                  </p>
                </div>
                <span className="px-3 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xs font-mono font-bold">
                  ABDM Milestone 3 Compliant
                </span>
              </div>

              {/* Dual Coding Reference Table */}
              <div className="space-y-2">
                <div className="text-xs font-bold text-white">Authoritative Dual Coding Mapping:</div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead className="border-b border-[var(--border)] text-[var(--muted)]">
                      <tr>
                        <th className="pb-2">Classical Unani Pathology</th>
                        <th className="pb-2">Amraz Code</th>
                        <th className="pb-2">WHO ICD-11 Code</th>
                        <th className="pb-2">NAMASTE Code</th>
                        <th className="pb-2">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[var(--border)]">
                      <tr>
                        <td className="py-2 font-bold text-white">Waja-ul-Mafasil (Joint Inflammation)</td>
                        <td className="py-2 font-mono text-teal-400">UN-AMR-041</td>
                        <td className="py-2 font-mono text-cyan-400">FA00.Z (Osteoarthritis)</td>
                        <td className="py-2 font-mono text-zinc-300">NAM-UNA-JNT-001</td>
                        <td className="py-2"><span className="text-emerald-400 text-[10px] font-bold">CERTIFIED</span></td>
                      </tr>
                      <tr>
                        <td className="py-2 font-bold text-white">Irq-un-Nasa (Sciatica / Radiculopathy)</td>
                        <td className="py-2 font-mono text-teal-400">UN-AMR-042</td>
                        <td className="py-2 font-mono text-cyan-400">8B93.0 (Sciatica)</td>
                        <td className="py-2 font-mono text-zinc-300">NAM-UNA-NEU-014</td>
                        <td className="py-2"><span className="text-emerald-400 text-[10px] font-bold">CERTIFIED</span></td>
                      </tr>
                      <tr>
                        <td className="py-2 font-bold text-white">Ziabetus Shakari (Type 2 Diabetes)</td>
                        <td className="py-2 font-mono text-teal-400">UN-AMR-018</td>
                        <td className="py-2 font-mono text-cyan-400">5A11 (Type 2 Diabetes)</td>
                        <td className="py-2 font-mono text-zinc-300">NAM-UNA-MET-002</td>
                        <td className="py-2"><span className="text-emerald-400 text-[10px] font-bold">CERTIFIED</span></td>
                      </tr>
                      <tr>
                        <td className="py-2 font-bold text-white">Su-e-Hazm (Dyspepsia / Acid Gastritis)</td>
                        <td className="py-2 font-mono text-teal-400">UN-AMR-029</td>
                        <td className="py-2 font-mono text-cyan-400">MD90 (Dyspepsia)</td>
                        <td className="py-2 font-mono text-zinc-300">NAM-UNA-GST-005</td>
                        <td className="py-2"><span className="text-emerald-400 text-[10px] font-bold">CERTIFIED</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Encryption & Envelope Details */}
              <div className="p-4 bg-[var(--background)] rounded-xl border border-[var(--border)] space-y-2 text-xs">
                <div className="font-bold text-white flex justify-between">
                  <span>ABDM Milestone 3 Encryption Envelope:</span>
                  <span className="text-teal-400 font-mono">ECDH_AES_GCM_256</span>
                </div>
                <div className="text-[var(--muted)] text-[11px] font-mono">
                  SHA-256 Payload Integrity Checksum: <strong>9d98097aa5c9527663e264c8c7f991bb20f5c1d1824a73740e79ecf014b18c54</strong>
                </div>
                <div className="text-zinc-400 text-[11px]">
                  Encrypted bundle ready for patient-directed transfer into ABHA PHR app lockers with revocable digital consent artifact.
                </div>
              </div>

            </div>
          </div>
        )}

      </div>
    </AppShell>
  );
}
