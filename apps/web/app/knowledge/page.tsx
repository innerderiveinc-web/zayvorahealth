"use client";

import React, { useState } from "react";
import { PlatformHeader } from "@/components/PlatformHeader";

interface Monograph {
  id: string;
  unani_name: string;
  botanical_name: string;
  family: string;
  part_used: string;
  mizaj: string;
  daraja: string;
  afal: string[];
  indications: string[];
  musleh: string;
  badal: string;
  therapeutic_dose: string;
  is_schedule_e1: boolean;
  upi_volume: string;
}

const CANONICAL_MONOGRAPHS: Monograph[] = [
  {
    id: "MONO-001",
    unani_name: "Suranjan Shireen",
    botanical_name: "Colchicum autumnale L.",
    family: "Colchicaceae",
    part_used: "Corm (Dried)",
    mizaj: "Hot 2° / Dry 2°",
    daraja: "Daraja Dom (Grade II)",
    afal: ["Musakkin-e-Alam (Analgesic)", "Mahallil-e-Warm (Anti-inflammatory)", "Mudirr-e-Baul (Diuretic)"],
    indications: ["Waja-ul-Mafasil (Arthritis)", "Niqras (Gout)", "Irq-un-Nasa (Sciatica)"],
    musleh: "Kateera (Astragalus gummifer) & Roghan-e-Badam",
    badal: "Bozidan (Tanacetum umbelliferum)",
    therapeutic_dose: "1g to 3g",
    is_schedule_e1: false,
    upi_volume: "UPI Vol. I, Page 78",
  },
  {
    id: "MONO-002",
    unani_name: "Suranjan Talkh",
    botanical_name: "Colchicum luteum Baker",
    family: "Colchicaceae",
    part_used: "Corm (Toxic Crude)",
    mizaj: "Hot 3° / Dry 3°",
    daraja: "Daraja Som (Grade III Poisonous)",
    afal: ["Jali (Detergent)", "Musqat-e-Janeen (Abortifacient)", "Qawi Mahallil (Potent Resolvent)"],
    indications: ["Severe acute gouty arthritis", "External topical anti-inflammatory poultices"],
    musleh: "Shahad (Honey) & Roghan-e-Gul; requires Mudabbar boiling in Cow's Milk",
    badal: "Suranjan Shireen (at double dose)",
    therapeutic_dose: "250mg to 500mg (Mudabbar form only)",
    is_schedule_e1: true,
    upi_volume: "UPI Vol. I, Page 80; Schedule E(1) Reg. #14",
  },
  {
    id: "MONO-003",
    unani_name: "Zanjabeel",
    botanical_name: "Zingiber officinale Roscoe",
    family: "Zingiberaceae",
    part_used: "Rhizome",
    mizaj: "Hot 3° / Dry 2°",
    daraja: "Daraja Som / Dom",
    afal: ["Muqawwi-e-Meda (Stomachic)", "Hazim (Digestive)", "Kasir-e-Riyah (Carminative)"],
    indications: ["Su-e-Hazm (Dyspepsia)", "Qillat-e-Ishteha (Anorexia)", "Nafkh-e-Shikam (Flatulence)"],
    musleh: "Ghee & Roghan-e-Badam",
    badal: "Khulanjan (Alpinia galanga)",
    therapeutic_dose: "1g to 2g",
    is_schedule_e1: false,
    upi_volume: "UPI Vol. I, Page 92",
  },
  {
    id: "MONO-004",
    unani_name: "Asgandh",
    botanical_name: "Withania somnifera (L.) Dunal",
    family: "Solanaceae",
    part_used: "Root",
    mizaj: "Hot 2° / Dry 2°",
    daraja: "Daraja Dom",
    afal: ["Muqawwi-e-Aam (General Tonic)", "Muqawwi-e-Bah (Aphrodisiac)", "Musakkin-e-Asab (Nervine Sedative)"],
    indications: ["Zof-e-Asab (Neurasthenia)", "Waja-ul-Mafasil (Rheumatism)", "Insomnia"],
    musleh: "Kateera & Gond Kikar",
    badal: "Bahman Surkh & Musli Safed",
    therapeutic_dose: "3g to 5g",
    is_schedule_e1: false,
    upi_volume: "UPI Vol. I, Page 14",
  },
];

export default function KnowledgePage() {
  const [monographs, setMonographs] = useState<Monograph[]>(CANONICAL_MONOGRAPHS);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedMonograph, setSelectedMonograph] = useState<Monograph | null>(CANONICAL_MONOGRAPHS[0]);
  const [filterScheduleE1, setFilterScheduleE1] = useState(false);

  const filteredMonographs = monographs.filter((m) => {
    const matchesSearch =
      m.unani_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.botanical_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.indications.some((ind) => ind.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesE1 = !filterScheduleE1 || m.is_schedule_e1;
    return matchesSearch && matchesE1;
  });

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)] text-[var(--text)]">
      <PlatformHeader />

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-6 space-y-6">
        
        {/* Knowledge Header */}
        <div className="zv-panel p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold">ZAYVORA Knowledge Platform & Pharmacopoeia (ZKB)</h1>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 font-semibold">
                UPI & NFUM Standardized
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-0.5">
              Canonical Unani pharmacopeia monographs, botanical identities, temperament scoring (Mizaj & Daraja), and Musleh/Badal registers.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">Indexed Monographs:</span>
            <span className="font-bold text-white">412 Plants & Minerals</span>
            <span className="text-[var(--border)]">|</span>
            <span className="text-purple-400 font-medium">Neo4j Evidence Graph</span>
          </div>
        </div>

        {/* Layout Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Monographs List */}
          <div className="space-y-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Search herb, botanical name, disease..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="zv-input text-xs"
              />
            </div>

            <div className="flex items-center gap-2 text-xs">
              <label className="flex items-center gap-1.5 cursor-pointer text-[var(--muted)] hover:text-white">
                <input
                  type="checkbox"
                  checked={filterScheduleE1}
                  onChange={(e) => setFilterScheduleE1(e.target.checked)}
                  className="rounded accent-red-500"
                />
                <span>Show Schedule E(1) Poisons Only</span>
              </label>
            </div>

            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
              {filteredMonographs.map((m) => (
                <div
                  key={m.id}
                  onClick={() => setSelectedMonograph(m)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    selectedMonograph?.id === m.id
                      ? "bg-[var(--elevated)] border-emerald-500/60 shadow-xs"
                      : "bg-[var(--panel)] border-[var(--border)] hover:bg-[var(--elevated)]"
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <h4 className="font-bold text-sm text-white">{m.unani_name}</h4>
                    {m.is_schedule_e1 && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/40">
                        SCHED E(1)
                      </span>
                    )}
                  </div>
                  <p className="text-[11px] text-[var(--gold-soft)] italic">{m.botanical_name}</p>
                  <div className="flex items-center justify-between text-[11px] text-[var(--muted)] mt-2">
                    <span>{m.mizaj}</span>
                    <span className="text-emerald-400 font-medium">{m.daraja}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Monograph Detail Dossier */}
          <div className="lg:col-span-2 zv-panel p-6 space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-2xl font-bold text-white">{selectedMonograph?.unani_name}</h2>
                  {selectedMonograph?.is_schedule_e1 && (
                    <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/40">
                      Schedule E(1) Poison
                    </span>
                  )}
                </div>
                <p className="text-sm text-[var(--gold-soft)] italic mt-0.5">
                  {selectedMonograph?.botanical_name} ({selectedMonograph?.family})
                </p>
              </div>

              <div className="text-right text-xs">
                <span className="text-[var(--muted)] block">Statutory Source:</span>
                <span className="font-mono text-white font-medium">{selectedMonograph?.upi_volume}</span>
              </div>
            </div>

            {/* Core Classification Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                <span className="text-[var(--muted)] block">Part Used</span>
                <span className="text-white font-semibold">{selectedMonograph?.part_used}</span>
              </div>
              <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                <span className="text-[var(--muted)] block">Mizaj (Temperament)</span>
                <span className="text-white font-semibold">{selectedMonograph?.mizaj}</span>
              </div>
              <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                <span className="text-[var(--muted)] block">Daraja (Potency)</span>
                <span className="text-emerald-400 font-semibold">{selectedMonograph?.daraja}</span>
              </div>
              <div className="p-3 rounded-lg bg-[var(--elevated)] border border-[var(--border)]">
                <span className="text-[var(--muted)] block">Therapeutic Dose</span>
                <span className="text-[var(--gold-soft)] font-semibold">{selectedMonograph?.therapeutic_dose}</span>
              </div>
            </div>

            {/* Actions & Indications */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="space-y-2 p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                <h4 className="font-bold text-white">Af'al (Pharmacological Actions)</h4>
                <ul className="space-y-1 text-[var(--muted)] list-disc list-inside">
                  {selectedMonograph?.afal.map((a, i) => (
                    <li key={i} className="text-[var(--text)]">{a}</li>
                  ))}
                </ul>
              </div>

              <div className="space-y-2 p-4 rounded-xl bg-[var(--elevated)] border border-[var(--border)]">
                <h4 className="font-bold text-white">Mahall-e-Istemal (Indications)</h4>
                <ul className="space-y-1 text-[var(--muted)] list-disc list-inside">
                  {selectedMonograph?.indications.map((ind, i) => (
                    <li key={i} className="text-[var(--text)]">{ind}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Musleh (Corrective) & Badal (Substitute) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-2 border-t border-[var(--border)]">
              <div>
                <span className="text-[var(--gold-soft)] font-bold block">Musleh (Corrective Vehicle)</span>
                <p className="text-[var(--muted)] mt-1">{selectedMonograph?.musleh}</p>
              </div>
              <div>
                <span className="text-blue-400 font-bold block">Badal (Therapeutic Substitute)</span>
                <p className="text-[var(--muted)] mt-1">{selectedMonograph?.badal}</p>
              </div>
            </div>

          </div>

        </div>

      </main>
    </div>
  );
}
