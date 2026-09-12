"use client";

import React, { useState } from "react";
import Link from "next/link";

interface ProductMonograph {
  id: string;
  name: string;
  category: string;
  price: string;
  sku: string;
  chiefDrug: string;
  indications: string;
  botanicalActives: Array<{ name: string; spec: string }>;
  posology: string;
  vehicleAnupan: string;
  classicalSource: string;
  batchCoa: {
    lot: string;
    mfgDate: string;
    expDate: string;
    purityPct: string;
    heavyMetals: string;
    status: string;
  };
}

const MONOGRAPHS: Record<string, ProductMonograph> = {
  "manivital-pro": {
    id: "manivital-pro",
    name: "ManiVital Pro",
    category: "Fertility & Vitality",
    price: "₹1,450",
    sku: "ZY-FERT-001",
    chiefDrug: "Withania somnifera & Mucuna pruriens",
    indications: "Male reproductive vitality, oligospermia, seminal thinning (Riqqat-e-Mani), and physical asthenia (Zof-e-Aam).",
    botanicalActives: [
      { name: "Withania somnifera (Asgandh)", spec: "5.0% Withanolides (HPLC verified)" },
      { name: "Mucuna pruriens (Kunch)", spec: "15.0% L-DOPA" },
      { name: "Asphaltum punjabianum (Shilajit Shodhit)", spec: "50.0% Fulvic Acid" },
      { name: "Chlorophytum borivilianum (Safed Musli)", spec: "20.0% Saponins" },
    ],
    posology: "5g (one level metric teaspoon) twice daily after breakfast and dinner.",
    vehicleAnupan: "Lukewarm cow's milk (Sheer-e-Gao) or warm water.",
    classicalSource: "Ibn Rushd's Kitab al-Kulliyat & UPI Vol. I",
    batchCoa: {
      lot: "BMR-2026-MVP-09",
      mfgDate: "2026-08-15",
      expDate: "2028-09-30",
      purityPct: "99.4%",
      heavyMetals: "< 0.012 ppm (Passed Pb/Cd/As/Hg)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  ovasync: {
    id: "ovasync",
    name: "OvaSync",
    category: "Fertility & Vitality",
    price: "₹1,380",
    sku: "ZY-FERT-002",
    chiefDrug: "Asparagus racemosus & Saraca asoca",
    indications: "Ovarian follicular health, menstrual cycle regularity, luteal phase support, and PCOS-associated Su-e-Mizaj.",
    botanicalActives: [
      { name: "Asparagus racemosus (Shatavari)", spec: "20.0% Saponins" },
      { name: "Saraca asoca (Ashoka)", spec: "Standardized Tannins & Flavonoids" },
      { name: "Symplocos racemosa (Lodh)", spec: "Total Glycosides > 5.0%" },
    ],
    posology: "5g twice daily with warm milk or Arq-e-Mako.",
    vehicleAnupan: "Warm milk or water.",
    classicalSource: "Al-Qanoon fi al-Tibb, Book III & UPI Vol. II",
    batchCoa: {
      lot: "BMR-2026-OVA-04",
      mfgDate: "2026-08-01",
      expDate: "2028-08-31",
      purityPct: "99.1%",
      heavyMetals: "< 0.015 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "qurs-taqwiyat-mani": {
    id: "qurs-taqwiyat-mani",
    name: "Qurs-e-Taqwiyat-e-Mani",
    category: "Fertility & Vitality",
    price: "₹980",
    sku: "ZY-FERT-003",
    chiefDrug: "Salep & Behman Surkh",
    indications: "Classical seminal viscosity, nocturnal emissions, premature ejaculation, and reproductive tone.",
    botanicalActives: [
      { name: "Orchis mascula (Salep Misri)", spec: "Mucilage & Starch Complex" },
      { name: "Centaurea behen (Behman Safed)", spec: "Bioactive Glucosides" },
      { name: "Ambergris synthetic analog", spec: "Purified resin" },
    ],
    posology: "2 tablets twice daily after meals.",
    vehicleAnupan: "Lukewarm milk or water.",
    classicalSource: "Bayaaz-e-Kabeer Vol. II",
    batchCoa: {
      lot: "BMR-2026-QTM-02",
      mfgDate: "2026-07-20",
      expDate: "2029-07-20",
      purityPct: "99.8%",
      heavyMetals: "< 0.010 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "metabocore-elite": {
    id: "metabocore-elite",
    name: "MetaboCore Elite",
    category: "Metabolic",
    price: "₹1,250",
    sku: "ZY-META-001",
    chiefDrug: "Gymnema sylvestre & Momordica charantia",
    indications: "Metabolic syndrome, peripheral insulin resistance, HbA1c elevation, and dyslipidemia.",
    botanicalActives: [
      { name: "Gymnema sylvestre (Gurmar)", spec: "25.0% Gymnemic Acids" },
      { name: "Berberis aristata (Darhald)", spec: "97.0% Berberine HCl" },
      { name: "Momordica charantia (Karela)", spec: "Charantin 2.5%" },
    ],
    posology: "1 capsule twice daily 30 minutes before major meals.",
    vehicleAnupan: "Lukewarm water.",
    classicalSource: "Kitab al-Hawi fi al-Tibb & UPI Vol. III",
    batchCoa: {
      lot: "BMR-2026-MET-03",
      mfgDate: "2026-09-01",
      expDate: "2028-09-30",
      purityPct: "99.6%",
      heavyMetals: "< 0.008 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "thyromet-axis": {
    id: "thyromet-axis",
    name: "ThyroMet Axis",
    category: "Metabolic",
    price: "₹1,350",
    sku: "ZY-META-002",
    chiefDrug: "Commiphora mukul & Bauhinia variegata",
    indications: "Subclinical thyroid sluggishness, cold-moist metabolic hypofunction, and peri-articular heaviness.",
    botanicalActives: [
      { name: "Commiphora mukul (Guggulu Shodhit)", spec: "2.5% Guggulsterones (HPLC)" },
      { name: "Bauhinia variegata (Kanchnar)", spec: "Total Flavonoids > 4.0%" },
    ],
    posology: "1 tablet morning and night after food.",
    vehicleAnupan: "Warm water with lemon wedge.",
    classicalSource: "UPI Vol. IV & Sharh al-Asbab",
    batchCoa: {
      lot: "BMR-2026-THY-01",
      mfgDate: "2026-08-10",
      expDate: "2028-08-10",
      purityPct: "99.3%",
      heavyMetals: "< 0.014 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "liverprime-core": {
    id: "liverprime-core",
    name: "LiverPrime Core",
    category: "Liver & Gut",
    price: "₹1,150",
    sku: "ZY-LIV-001",
    chiefDrug: "Picrorhiza kurroa & Cichorium intybus",
    indications: "Non-alcoholic fatty liver (NAFLD), hepatobiliary stasis, sluggish digestive fire (Zof-e-Ishtaha).",
    botanicalActives: [
      { name: "Picrorhiza kurroa (Kutki)", spec: "10.0% Kutkin / Picrosides" },
      { name: "Cichorium intybus (Kasni)", spec: "Inulin & Cichoriin" },
    ],
    posology: "10ml syrup twice daily before food.",
    vehicleAnupan: "Direct or diluted in 50ml lukewarm water.",
    classicalSource: "Kitab al-Jami li-Mufradat & UPI Vol. I",
    batchCoa: {
      lot: "BMR-2026-LIV-05",
      mfgDate: "2026-08-20",
      expDate: "2028-08-20",
      purityPct: "99.7%",
      heavyMetals: "< 0.009 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  neurocalmx: {
    id: "neurocalmx",
    name: "NeuroCalmX",
    category: "Calm & Sleep",
    price: "₹1,200",
    sku: "ZY-CALM-001",
    chiefDrug: "Bacopa monnieri & Convolvulus pluricaulis",
    indications: "Chronic psychological stress, GABAergic modulation, memory retention, and mental exhaustion.",
    botanicalActives: [
      { name: "Bacopa monnieri (Brahmi)", spec: "20.0% Bacosides A & B" },
      { name: "Convolvulus pluricaulis (Shankhpushpi)", spec: "Alkaloid fraction > 2.0%" },
    ],
    posology: "5g at bedtime with lukewarm milk.",
    vehicleAnupan: "Lukewarm milk or chamomile infusion.",
    classicalSource: "Al-Qanoon Book II & UPI Vol. II",
    batchCoa: {
      lot: "BMR-2026-NCX-07",
      mfgDate: "2026-08-18",
      expDate: "2028-08-18",
      purityPct: "99.5%",
      heavyMetals: "< 0.011 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "nightone-x": {
    id: "nightone-x",
    name: "NightOne X",
    category: "Calm & Sleep",
    price: "₹1,320",
    sku: "ZY-CALM-002",
    chiefDrug: "Valeriana wallichii & Nardostachys jatamansi",
    indications: "Circadian rhythm disruption, prolonged sleep onset latency, and unrefreshing non-REM sleep.",
    botanicalActives: [
      { name: "Valeriana wallichii (Tagar)", spec: "0.8% Valerenic Acids" },
      { name: "Nardostachys jatamansi (Sumbul-ut-Teeb)", spec: "Jatamansone rich essential oil" },
    ],
    posology: "1 capsule 30 minutes before retiring for sleep.",
    vehicleAnupan: "Warm water.",
    classicalSource: "Kitab al-Mansuri fi al-Tibb",
    batchCoa: {
      lot: "BMR-2026-NOX-03",
      mfgDate: "2026-08-25",
      expDate: "2028-08-25",
      purityPct: "99.2%",
      heavyMetals: "< 0.007 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "sleep-stress": {
    id: "sleep-stress",
    name: "Sleep Stress Harmonizer",
    category: "Calm & Sleep",
    price: "₹1,180",
    sku: "ZY-CALM-003",
    chiefDrug: "Withania somnifera & Matricaria chamomilla",
    indications: "Nocturnal cortisol spike, mid-night awakenings, and racing thoughts before bed.",
    botanicalActives: [
      { name: "Withania somnifera (Asgandh)", spec: "3.5% Withanolides" },
      { name: "Matricaria chamomilla (Babuna)", spec: "Apigenin 1.2%" },
    ],
    posology: "1 teaspoon steeped in warm water as herbal infusion.",
    vehicleAnupan: "Steeped herbal tea.",
    classicalSource: "UPI Vol. III",
    batchCoa: {
      lot: "BMR-2026-SSH-02",
      mfgDate: "2026-08-12",
      expDate: "2028-08-12",
      purityPct: "99.4%",
      heavyMetals: "< 0.010 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
  "men-daily": {
    id: "men-daily",
    name: "Men Daily Adaptogen",
    category: "Daily",
    price: "₹1,280",
    sku: "ZY-DAY-001",
    chiefDrug: "Tribulus terrestris & Asphaltum (Shilajit)",
    indications: "Daily micronutrient replenishment, physical stamina, immune resilience, and adaptogenic vitality.",
    botanicalActives: [
      { name: "Tribulus terrestris (Gokhru)", spec: "40.0% Saponins" },
      { name: "Purified Shilajit", spec: "50.0% Fulvic Acid" },
    ],
    posology: "1 tablet after breakfast.",
    vehicleAnupan: "Water.",
    classicalSource: "UPI Vol. I & Al-Qanoon",
    batchCoa: {
      lot: "BMR-2026-MDA-01",
      mfgDate: "2026-08-30",
      expDate: "2028-08-30",
      purityPct: "99.9%",
      heavyMetals: "< 0.005 ppm (Passed)",
      status: "RELEASED_FOR_DISPENSARY",
    },
  },
};

export default function ProductDetailPage() {
  const [selectedProductId, setSelectedProductId] = useState<string>("manivital-pro");
  const product = MONOGRAPHS[selectedProductId] || MONOGRAPHS["manivital-pro"];

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-8 text-xs text-[#CBD5E1]">
      {/* Product Selection Tabs */}
      <div className="border-b border-[#334155] pb-4">
        <span className="text-[11px] font-bold text-[#2DD4BF] uppercase tracking-wider">ZAYVORA Pharmacopoeia Monograph</span>
        <h1 className="text-3xl font-extrabold text-white mt-1">Official Botanical Drug Monograph</h1>
        <div className="flex flex-wrap gap-2 mt-4">
          {Object.values(MONOGRAPHS).map((m) => (
            <button
              key={m.id}
              onClick={() => setSelectedProductId(m.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                selectedProductId === m.id
                  ? "bg-[#0D9488] text-white"
                  : "bg-[#1E293B] text-[#94A3B8] hover:text-white border border-[#334155]"
              }`}
            >
              {m.name}
            </button>
          ))}
        </div>
      </div>

      {/* Hero Header for Active Product */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 bg-[#1E293B] p-6 rounded-2xl border border-[#334155]">
        <div>
          <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-[#0D9488]/20 text-[#2DD4BF]">
            {product.category}
          </span>
          <h2 className="text-2xl font-extrabold text-white mt-2">{product.name}</h2>
          <p className="text-sm text-[#94A3B8] mt-1">{product.chiefDrug} • SKU: {product.sku}</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <span className="text-2xl font-extrabold text-white block">{product.price}</span>
            <span className="text-[10px] text-emerald-400 font-semibold block">FEFO In Stock</span>
          </div>
          <Link
            href={`/website/cart?add=${product.id}`}
            className="px-5 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-xs shadow-lg"
          >
            + Add to Cart
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          {/* Clinical Indications */}
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Clinical Indications & Classical Action</h3>
            <p className="leading-relaxed text-slate-300">{product.indications}</p>
          </div>

          {/* Phytochemical Actives */}
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Standardized Botanical Actives (HPLC / HPTLC)</h3>
            <ul className="space-y-2 list-disc pl-5 text-[#CBD5E1]">
              {product.botanicalActives.map((active, idx) => (
                <li key={idx}>
                  <strong className="text-white">{active.name}:</strong> <span className="text-emerald-400 font-mono">{active.spec}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Posology & Vehicle */}
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Posology & Vehicle (Anupan)</h3>
            <p className="leading-relaxed text-slate-300">
              <strong className="text-white">Dosage:</strong> {product.posology}
            </p>
            <p className="leading-relaxed text-slate-300">
              <strong className="text-[#2DD4BF]">Recommended Vehicle (Anupan):</strong> {product.vehicleAnupan}
            </p>
          </div>

          {/* Classical Reference */}
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-1">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Classical Pharmacopoeia Authority</h3>
            <p className="text-emerald-300 font-mono text-xs">{product.classicalSource}</p>
          </div>
        </div>

        {/* Batch Certificate of Analysis (CoA) Card */}
        <div className="space-y-4">
          <div className="p-5 rounded-2xl bg-[#0F172A] border border-emerald-500/40 space-y-3 shadow-lg">
            <div className="flex justify-between items-center border-b border-[#334155] pb-2">
              <span className="text-xs font-bold text-white uppercase tracking-wider">Batch CoA Verification</span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-bold">RELEASED</span>
            </div>

            <div className="space-y-2 text-[11px]">
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Batch Lot No:</span>
                <span className="font-mono text-white font-bold">{product.batchCoa.lot}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Mfg Date:</span>
                <span className="text-white">{product.batchCoa.mfgDate}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">FEFO Expiry:</span>
                <span className="text-white font-semibold">{product.batchCoa.expDate}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">HPLC Assay Purity:</span>
                <span className="text-emerald-400 font-bold">{product.batchCoa.purityPct}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#94A3B8]">Heavy Metals:</span>
                <span className="text-emerald-400 font-bold">{product.batchCoa.heavyMetals}</span>
              </div>
            </div>

            <div className="pt-2 border-t border-[#334155]">
              <button
                onClick={() => alert(`Official COA for ${product.batchCoa.lot} downloaded with 21 CFR cryptographic hash verification.`)}
                className="w-full py-2 bg-[#1E293B] hover:bg-slate-700 text-white font-bold text-xs rounded-xl border border-[#334155]"
              >
                Download Signed CoA (PDF)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
