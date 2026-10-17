"use client";

import React, { useState } from "react";
import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { MASTER_PROTOCOLS, MasterProtocol } from "@/lib/data";

const CATEGORIES = [
  "ALL",
  "METABOLIC",
  "CARDIO",
  "NEURO",
  "RESPIRATORY",
  "JOINTS",
  "MALE",
  "FEMALE",
  "GENERAL",
];

export default function ProtocolsLibraryPage() {
  const [selectedCategory, setSelectedCategory] = useState("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [activeProto, setActiveProto] = useState<MasterProtocol>(MASTER_PROTOCOLS[0]);
  const [notice, setNotice] = useState<string | null>(null);

  const filtered = MASTER_PROTOCOLS.filter((p) => {
    const matchCat =
      selectedCategory === "ALL" ||
      p.category.toUpperCase() === selectedCategory.toUpperCase();
    const q = searchQuery.toLowerCase();
    const matchSearch =
      p.id.toLowerCase().includes(q) ||
      p.name.toLowerCase().includes(q) ||
      p.indication.toLowerCase().includes(q) ||
      p.primary_axis.toLowerCase().includes(q) ||
      p.protocol_kit_name.toLowerCase().includes(q);
    return matchCat && matchSearch;
  });

  const handleImportToEncounter = (proto: MasterProtocol) => {
    setNotice(`Protocol ${proto.id} (${proto.name}) with Kit ${proto.protocol_kit_id} imported into active clinical encounter.`);
    setTimeout(() => setNotice(null), 4000);
  };

  const handleOrderKit = (proto: MasterProtocol) => {
    setNotice(`Kit ${proto.protocol_kit_id} (${proto.protocol_kit_name}) added to prescription order.`);
    setTimeout(() => setNotice(null), 4000);
  };

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[var(--border)] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">📑</span>
              <h1 className="text-xl font-bold text-white tracking-tight">
                ZAYVORA Master Clinical Protocols (P-01 to P-21)
              </h1>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
                21 Canonical Protocols
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] mt-1">
              Standardized Unani-Modern integrative protocols: 3-Phase Clinical Continuum, 12 Canonical Organ Axes, Lab Monitoring & Protocol Kits (K-01 to K-21).
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <Link
              href="/doctor/organ-axis"
              className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-teal-300 font-semibold border border-[var(--border)] transition"
            >
              🔬 Organ-Axis Console →
            </Link>
            <Link
              href="/doctor/mizaj"
              className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-emerald-300 font-semibold border border-[var(--border)] transition"
            >
              ⚖️ Z-MAI Mizaj →
            </Link>
          </div>
        </div>

        {notice && (
          <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-between shadow-md animate-fadeIn">
            <span className="flex items-center gap-2">
              <span>✓</span>
              <span>{notice}</span>
            </span>
            <button
              onClick={() => setNotice(null)}
              className="text-slate-400 hover:text-white font-bold ml-4"
            >
              ✕
            </button>
          </div>
        )}

        {/* Filter & Search Bar */}
        <div className="flex flex-col md:flex-row gap-3 items-center justify-between">
          <div className="flex items-center gap-1.5 p-1 bg-[var(--panel)] border border-[var(--border)] rounded-2xl text-xs overflow-x-auto w-full md:w-auto">
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1.5 rounded-xl font-medium whitespace-nowrap transition ${
                  selectedCategory === cat
                    ? "bg-teal-600 text-white font-semibold shadow-xs"
                    : "text-[var(--muted)] hover:text-white"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <div className="w-full md:w-80">
            <input
              type="text"
              placeholder="Search by ID (e.g. P-01), name, organ axis..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[var(--panel)] border border-[var(--border)] rounded-xl px-3.5 py-2 text-xs text-white placeholder-[var(--muted)] focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {/* Master-Detail Protocol Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Protocols List Directory (5 cols) */}
          <div className="lg:col-span-5 space-y-3">
            <div className="flex items-center justify-between px-1">
              <span className="text-[11px] font-bold text-[var(--muted)] uppercase tracking-wider">
                Protocols Directory ({filtered.length} of {MASTER_PROTOCOLS.length})
              </span>
              <span className="text-[10px] text-teal-400 font-mono">
                P-01 - P-21
              </span>
            </div>

            <div className="space-y-2.5 max-h-[780px] overflow-y-auto pr-1">
              {filtered.map((proto) => {
                const isSelected = proto.id === activeProto.id;
                return (
                  <div
                    key={proto.id}
                    onClick={() => setActiveProto(proto)}
                    className={`p-3.5 rounded-2xl border cursor-pointer transition space-y-2 ${
                      isSelected
                        ? "bg-teal-950/25 border-teal-500 shadow-md ring-1 ring-teal-500/40"
                        : "bg-[var(--panel)] border-[var(--border)] hover:bg-[var(--elevated)] hover:border-slate-700"
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded-md bg-teal-900/50 border border-teal-600/40 text-teal-300 font-mono text-xs font-bold">
                          {proto.id}
                        </span>
                        <span className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] font-semibold text-slate-300 uppercase">
                          {proto.category}
                        </span>
                      </div>
                      <span className="px-2 py-0.5 rounded bg-emerald-950/40 border border-emerald-700/30 text-emerald-400 text-[10px] font-mono font-bold">
                        {proto.protocol_kit_id}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white leading-tight">
                      {proto.name}
                    </h3>

                    <p className="text-[11px] text-[var(--muted)] line-clamp-2 leading-relaxed">
                      {proto.indication}
                    </p>

                    <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1.5 border-t border-[var(--border)]">
                      <span className="flex items-center gap-1">
                        <span className="text-teal-400 font-medium">Axis:</span> {proto.primary_axis}
                      </span>
                      <span className="text-slate-300 font-mono">
                        {proto.kit_price_range}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Active Protocol Comprehensive Inspector (7 cols) */}
          <div className="lg:col-span-7 space-y-4">
            <div className="p-5 sm:p-6 rounded-3xl bg-[var(--panel)] border border-[var(--border)] space-y-5 shadow-xl">
              {/* Header */}
              <div className="flex flex-col sm:flex-row justify-between items-start gap-3 border-b border-[var(--border)] pb-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-md bg-teal-500/20 text-teal-300 font-mono text-xs font-bold border border-teal-500/30">
                      {activeProto.id}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-xs font-bold text-slate-300 uppercase">
                      {activeProto.category}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs font-mono font-bold">
                      Kit {activeProto.protocol_kit_id}
                    </span>
                  </div>
                  <h2 className="text-lg font-bold text-white tracking-tight mt-1">
                    {activeProto.name}
                  </h2>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-300">
                    <span>
                      <strong className="text-teal-400">Primary Axis:</strong> {activeProto.primary_axis}
                    </span>
                    {activeProto.secondary_axis && (
                      <span>
                        <strong className="text-cyan-400">Secondary Axis:</strong> {activeProto.secondary_axis}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 self-stretch sm:self-auto">
                  <button
                    onClick={() => handleImportToEncounter(activeProto)}
                    className="flex-1 sm:flex-initial px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-xs shadow-sm transition flex items-center justify-center gap-1.5"
                  >
                    <span>📥 Consult</span>
                  </button>
                  <button
                    onClick={() => handleOrderKit(activeProto)}
                    className="flex-1 sm:flex-initial px-3.5 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white font-bold text-xs shadow-sm transition flex items-center justify-center gap-1.5"
                  >
                    <span>📦 Order Kit</span>
                  </button>
                </div>
              </div>

              {/* Indication */}
              <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] text-xs space-y-1">
                <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">
                  Diagnostic Criteria & Clinical Indication
                </span>
                <p className="text-slate-200 leading-relaxed">
                  {activeProto.indication}
                </p>
              </div>

              {/* Protocol Kit Card */}
              <div className="p-4 rounded-2xl bg-gradient-to-br from-teal-950/30 via-slate-900/40 to-emerald-950/30 border border-teal-700/40 space-y-2.5">
                <div className="flex justify-between items-center">
                  <div>
                    <span className="text-[10px] text-teal-400 font-bold uppercase tracking-wider block">
                      Recommended Protocol Kit
                    </span>
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <span>{activeProto.protocol_kit_name}</span>
                      <span className="text-xs font-mono text-emerald-400 font-semibold">({activeProto.protocol_kit_id})</span>
                    </h4>
                  </div>
                  <span className="text-xs font-mono font-bold text-emerald-300 bg-emerald-950/60 border border-emerald-600/30 px-2.5 py-1 rounded-lg">
                    {activeProto.kit_price_range}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs pt-1">
                  <div className="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[10px] text-emerald-400 font-bold block">Core Stack</span>
                    <span className="text-slate-200 font-medium">
                      {activeProto.product_stack.core.join(", ") || "Standard"}
                    </span>
                  </div>
                  <div className="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[10px] text-teal-400 font-bold block">Support Stack</span>
                    <span className="text-slate-200 font-medium">
                      {activeProto.product_stack.support.join(", ") || "None"}
                    </span>
                  </div>
                  <div className="p-2 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[10px] text-cyan-400 font-bold block">Modulator</span>
                    <span className="text-slate-200 font-medium">
                      {activeProto.product_stack.modulator.join(", ") || "None"}
                    </span>
                  </div>
                </div>
              </div>

              {/* 3-Phase Continuum */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <span>⚡</span> 3-Phase Clinical Continuum
                </h4>

                <div className="space-y-3">
                  {/* Phase 1 */}
                  <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-teal-500/20 text-teal-300 font-mono text-[11px] font-bold">
                          Phase 1: {activeProto.phase1.title}
                        </span>
                      </div>
                      <span className="text-[10px] font-mono font-bold text-slate-300">
                        {activeProto.phase1.duration_days} Days
                      </span>
                    </div>

                    <div className="space-y-1.5 text-xs">
                      <span className="text-[10px] text-teal-400 font-bold uppercase tracking-wider block">
                        Prescribed Formulations:
                      </span>
                      {activeProto.phase1.products.map((prd, i) => (
                        <div key={i} className="p-2 rounded-xl bg-[var(--panel)] border border-slate-800 text-[11px] space-y-0.5">
                          <div className="flex justify-between font-bold text-slate-200">
                            <span>{prd.name}</span>
                            <span className="text-teal-300 font-mono">{prd.dose} ({prd.timing})</span>
                          </div>
                          {prd.rationale && (
                            <p className="text-[10px] text-slate-400 italic">{prd.rationale}</p>
                          )}
                        </div>
                      ))}
                    </div>

                    {activeProto.phase1.diet && (
                      <div className="p-2 rounded-xl bg-amber-950/20 border border-amber-800/30 text-[11px] text-amber-200">
                        <strong>Diet (Parhez):</strong> {activeProto.phase1.diet}
                      </div>
                    )}
                  </div>

                  {/* Phase 2 */}
                  <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[11px] font-bold">
                          Phase 2: {activeProto.phase2.title}
                        </span>
                      </div>
                      <span className="text-[10px] font-mono font-bold text-slate-300">
                        {activeProto.phase2.duration_days} Days
                      </span>
                    </div>

                    <div className="space-y-1.5 text-xs">
                      <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider block">
                        Prescribed Formulations:
                      </span>
                      {activeProto.phase2.products.map((prd, i) => (
                        <div key={i} className="p-2 rounded-xl bg-[var(--panel)] border border-slate-800 text-[11px] space-y-0.5">
                          <div className="flex justify-between font-bold text-slate-200">
                            <span>{prd.name}</span>
                            <span className="text-emerald-300 font-mono">{prd.dose} ({prd.timing})</span>
                          </div>
                          {prd.rationale && (
                            <p className="text-[10px] text-slate-400 italic">{prd.rationale}</p>
                          )}
                        </div>
                      ))}
                    </div>

                    {activeProto.phase2.monitoring && (
                      <div className="p-2 rounded-xl bg-cyan-950/20 border border-cyan-800/30 text-[11px] text-cyan-200">
                        <strong>Monitoring:</strong> {activeProto.phase2.monitoring}
                      </div>
                    )}
                    {activeProto.phase2.exercise && (
                      <div className="p-2 rounded-xl bg-slate-900/60 border border-slate-800 text-[11px] text-slate-300">
                        <strong>Exercise / Physical:</strong> {activeProto.phase2.exercise}
                      </div>
                    )}
                  </div>

                  {/* Phase 3 */}
                  <div className="p-3.5 rounded-2xl bg-[var(--background)] border border-[var(--border)] space-y-2">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono text-[11px] font-bold">
                          Phase 3: {activeProto.phase3.title}
                        </span>
                      </div>
                      <span className="text-[10px] font-mono font-bold text-slate-300">
                        {String(activeProto.phase3.duration_days)}
                      </span>
                    </div>

                    <div className="space-y-1.5 text-xs">
                      <span className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider block">
                        Prescribed Formulations:
                      </span>
                      {activeProto.phase3.products.map((prd, i) => (
                        <div key={i} className="p-2 rounded-xl bg-[var(--panel)] border border-slate-800 text-[11px] space-y-0.5">
                          <div className="flex justify-between font-bold text-slate-200">
                            <span>{prd.name}</span>
                            <span className="text-cyan-300 font-mono">{prd.dose} ({prd.timing})</span>
                          </div>
                          {prd.rationale && (
                            <p className="text-[10px] text-slate-400 italic">{prd.rationale}</p>
                          )}
                        </div>
                      ))}
                    </div>

                    {activeProto.phase3.monitoring && (
                      <div className="p-2 rounded-xl bg-slate-900/60 border border-slate-800 text-[11px] text-slate-300">
                        <strong>Ongoing Monitoring:</strong> {activeProto.phase3.monitoring}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Lab Monitoring Checklist */}
              {activeProto.lab_monitoring && activeProto.lab_monitoring.length > 0 && (
                <div className="p-3.5 rounded-2xl bg-cyan-950/15 border border-cyan-800/30 text-xs space-y-2">
                  <span className="text-[11px] font-bold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5">
                    <span>🔬</span> Mandatory Clinical Lab Monitoring
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                    {activeProto.lab_monitoring.map((lab, i) => (
                      <div key={i} className="flex items-center gap-1.5 text-[11px] text-slate-200">
                        <span className="text-cyan-400">▪</span>
                        <span>{lab}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Clinical Warnings & Red Flags */}
              {activeProto.clinical_warnings && activeProto.clinical_warnings.length > 0 && (
                <div className="p-3.5 rounded-2xl bg-rose-950/20 border border-rose-800/30 text-xs space-y-1.5">
                  <span className="text-[11px] font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1">
                    ⚠️ Statutory Safety & Clinical Warnings
                  </span>
                  <ul className="list-disc list-inside text-rose-200 space-y-1 text-[11px]">
                    {activeProto.clinical_warnings.map((w, i) => (
                      <li key={i}>{w}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Action Links */}
              <div className="pt-2 border-t border-[var(--border)] flex flex-wrap gap-2 text-xs">
                <Link
                  href="/doctor/nuskha"
                  className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-teal-300 font-semibold border border-[var(--border)] transition"
                >
                  📝 Open in Nuskha Builder →
                </Link>
                <Link
                  href="/doctor/organ-axis"
                  className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-slate-300 font-semibold border border-[var(--border)] transition"
                >
                  🔬 View Organ-Axis Mapping →
                </Link>
                <Link
                  href="/doctor/mizaj"
                  className="px-3 py-1.5 rounded-xl bg-[var(--elevated)] hover:bg-[var(--border)] text-emerald-300 font-semibold border border-[var(--border)] transition"
                >
                  ⚖️ Z-MAI Mizaj Calculator →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
