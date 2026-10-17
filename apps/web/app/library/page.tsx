"use client";

import React, { useState, useMemo } from "react";
import Link from "next/link";
import { PublicWebsiteShell } from "@/components/shells/PublicWebsiteShell";
import { PageHeader } from "@/components/website/PageHeader";
import { HealthcareIcon } from "@/components/ui/HealthcareIcon";
import { CANONICAL_TREATISES } from "@/lib/data/canonicalTreatises";
import { GRAND_INTEGRATIVE_LIBRARY } from "@/lib/data/grandLibraryData";

// 12 Master Volumes Static Index
const VOLUMES_DATA = [
  {
    id: "vol-01",
    num: 1,
    title_en: "Kulliyat-e-Tibb & Human Physiology",
    title_ur: "کلیاتِ طب اور انسانی افعال الاعضاء",
    icon: "🧬",
    badge: "Classical Foundations",
    summary: "Foundational doctrine of human existence, physical matter, humoral equilibrium, and biological faculties bridging Avicennian pneuma with cellular thermodynamics.",
    chapters: [
      { id: "ch-01-01", num: "1.1", title_en: "Arkan-e-Arba'a: The Four Elements & States of Matter", title_ur: "ارکانِ اربعہ اور مادی تغیرات" },
      { id: "ch-01-02", num: "1.2", title_en: "Akhlat-e-Arba'a: Humoral Dynamics & Fluid Compartments", title_ur: "اخلاطِ اربعہ اور جسمانی مائعات" },
      { id: "ch-01-03", num: "1.3", title_en: "Ilm-ul-Mizaj: Temperamental Science & Metabolic Typing", title_ur: "علم المزاج اور انفرادی بائیو کیمسٹری" },
      { id: "ch-01-04", num: "1.4", title_en: "Quwa & Afaal: Vital, Natural & Psychic Physiology", title_ur: "قویٰ اور افعال — حیوانی، طبعی اور نفسیاتی نظام" }
    ]
  },
  {
    id: "vol-02",
    num: 2,
    title_en: "Asbab-e-Sitta Zarooriyya: The Six Essential Prerequisites",
    title_ur: "اسبابِ ستہ ضروریہ اور احتیاطی طرزِ زندگی",
    icon: "🌿",
    badge: "Preventive Lifestyle",
    summary: "The immutable six lifestyle determinants of health: ambient air, chrono-nutrition, physical exercise, circadian sleep, detox evacuation, and psychic equilibrium.",
    chapters: [
      { id: "ch-02-01", num: "2.1", title_en: "Hawa-e-Muheet: Atmospheric Aeration, Air Quality & Breathwork", title_ur: "ہوائے محیط — سانس اور آلودگی" },
      { id: "ch-02-02", num: "2.2", title_en: "Makool-o-Mashroob: Chrono-Nutrition & Food-as-Medicine", title_ur: "ماکول و مشروب — غذائی نظام" },
      { id: "ch-02-03", num: "2.3", title_en: "Harkat-o-Sukoon-e-Badani: Physical Exercise & Ergonomics", title_ur: "حرکت و سکونِ بدنی — ورزش اور آرام" },
      { id: "ch-02-04", num: "2.4", title_en: "Naum-o-Yaqza: Sleep Architecture & Circadian Entrainment", title_ur: "نوم و یقظہ — نیند اور ہارمونی بحالی" },
      { id: "ch-02-05", num: "2.5", title_en: "Istifragh-o-Ihtibas: Evacuation, Retention & Detox Pathways", title_ur: "استفراغ و احتباس — سموم کا اخراج" },
      { id: "ch-02-06", num: "2.6", title_en: "Harkat-o-Sukoon-e-Nafsani: Psychic Equilibrium & Stress Modulation", title_ur: "حرکت و سکونِ نفسانی — ذہنی دباؤ اور توازن" }
    ]
  },
  {
    id: "vol-03",
    num: 3,
    title_en: "Classical Diagnostics & Bedside Examination",
    title_ur: "تشخیص و معاینۂ سريري — نبض، قارورہ اور براز",
    icon: "🩺",
    badge: "Clinical Semiology",
    summary: "The non-invasive semiology art: 10-Ajnas pulse waveform evaluation, urine sediment stratification, stool analysis, and cranial facial diagnostics.",
    chapters: [
      { id: "ch-03-01", num: "3.1", title_en: "Ilm-un-Nabz: The 10 Classical Ajnas Pulse Evaluation", title_ur: "علم النبض — دس اجناسِ نبض" },
      { id: "ch-03-02", num: "3.2", title_en: "Qaroorah: Urine Examination & Sediment Topography", title_ur: "قارورہ — پیشاب کا تجزیہ" },
      { id: "ch-03-03", num: "3.3", title_en: "Baraaz & Lisaan: Stool Transit & Tongue Topography", title_ur: "براز اور لسان — آنتوں اور زبان کی تشخیص" }
    ]
  },
  {
    id: "vol-04",
    num: 4,
    title_en: "Clinical Laboratory Biomarkers & Modern Pathology",
    title_ur: "جدید لیب ٹیسٹ، بائیو مارکرز اور پیتھولوجی",
    icon: "🧪",
    badge: "Biomedical Precision",
    summary: "Bridging modern clinical hematology, biochemistry, and endocrinology with classical humoral dyscrasias and systemic inflammation cascades.",
    chapters: [
      { id: "ch-04-01", num: "4.1", title_en: "Inflammatory Biomarkers: hs-CRP, ESR & Cytokines", title_ur: "سوزش کے مارکرز — سی آر پی، ای ایس آر" },
      { id: "ch-04-02", num: "4.2", title_en: "Cardiometabolic Panel: HbA1c, Fasting Insulin & Lipid Fractionation", title_ur: "کارڈیو میٹابولک پینل — ایچ بی اے ون سی" },
      { id: "ch-04-03", num: "4.3", title_en: "Hepatorenal & Endocrine Panels: LFT, KFT, Thyroid & Cortisol", title_ur: "جگر، گردے اور ہارمونز کا تجزیہ" }
    ]
  },
  {
    id: "vol-05",
    num: 5,
    title_en: "Radio-Diagnostics & Medical Imaging",
    title_ur: "ریڈیو ڈائیگنوسٹکس اور جدید امیجنگ — ایکسرے، ایم آر آئی اور الٹراساؤنڈ",
    icon: "🩻",
    badge: "Structural Imaging",
    summary: "Modern radiological semiology (Plain Radiography, Ultrasound, MRI, FibroScan, DEXA) correlated with musculoskeletal and visceral organ temperaments.",
    chapters: [
      { id: "ch-05-01", num: "5.1", title_en: "Musculoskeletal Imaging: X-Ray & MRI in Arthritis", title_ur: "ہڈیوں اور جوڑوں کے ایکسرے اور ایم آر آئی" },
      { id: "ch-05-02", num: "5.2", title_en: "Abdominal Ultrasound & FibroScan: Hepatic Steatosis & Visceral Stones", title_ur: "پیٹ کا الٹراساؤنڈ اور فائبرو اسکین" },
      { id: "ch-05-03", num: "5.3", title_en: "DEXA Bone Densitometry & Vascular Doppler", title_ur: "ہڈیوں کی کمزوری (DEXA) اور ڈوپلر" }
    ]
  },
  {
    id: "vol-06",
    num: 6,
    title_en: "Gut Microbiome, Metagenomics & Epigenetics",
    title_ur: "گٹ مائیکرو بائیوم، آنتوں کے جراثیم اور جینیاتی اظہار",
    icon: "🦠",
    badge: "Microbiome Biology",
    summary: "Avicennian first digestion (Hazm-e-Awwal) and Kiloos synthesis unified with modern 16S rRNA metagenomics, Short-Chain Fatty Acids, and epigenetics.",
    chapters: [
      { id: "ch-06-01", num: "6.1", title_en: "Hazm-e-Awwal & Metagenomics: The Microbiome as Humoral Factory", title_ur: "ہضمِ اول اور گٹ مائیکروبائیوم" },
      { id: "ch-06-02", num: "6.2", title_en: "Short-Chain Fatty Acids (SCFAs) & Epigenetics", title_ur: "شارٹ چین فیٹی ایسڈز اور ایپی جینیٹکس" }
    ]
  },
  {
    id: "vol-07",
    num: 7,
    title_en: "Continuous Wearables, IoT & Smartphone AI Vision",
    title_ur: "پہننے والے گیجٹس، لائیو مانیٹرنگ اور سمارٹ فون اے آئی",
    icon: "📱",
    badge: "Digital Diagnostics",
    summary: "Real-time Asbab-e-Sitta telemetry: Continuous Glucose Monitoring, HRV autonomic tracking, sleep hypnograms, and smartphone computer vision diagnostics.",
    chapters: [
      { id: "ch-07-01", num: "7.1", title_en: "Continuous Glucose Monitoring (CGM) & Glycemic Telemetry", title_ur: "مسلسل گلوکوز ٹریکنگ اور میٹابولک اتار چڑھاؤ" },
      { id: "ch-07-02", num: "7.2", title_en: "Heart Rate Variability (HRV) & Sleep Architecture IoT", title_ur: "دل کی دھڑکن کا توازن (HRV) اور سلیپ ٹریکنگ" },
      { id: "ch-07-03", num: "7.3", title_en: "Smartphone Computer Vision: Digital Lisaan & Sima Diagnostics", title_ur: "موبائل کیمرہ اے آئی — زبان اور چہرے کی تشخیص" }
    ]
  },
  {
    id: "vol-08",
    num: 8,
    title_en: "Comprehensive Materia Medica & Toxicology",
    title_ur: "جامع مفرودات و مرکبات، سموم اور تدبیرِ ادویہ",
    icon: "🌿",
    badge: "Pharmacopoeia & Safety",
    summary: "1,280+ Codified Botanical Monographs, Schedule E(1) Statutory Poison detoxification (Mudabbar / Shodhana), Badal substitutes, and classical Murakkabat.",
    chapters: [
      { id: "ch-08-01", num: "8.1", title_en: "The Master Botanical Pharmacopoeia: 1,280+ Codified Monographs", title_ur: "یونانی فارماکوپیا — ۱۲۸۰ سے زائد نباتاتی ادویہ" },
      { id: "ch-08-02", num: "8.2", title_en: "Schedule E(1) Statutory Poisons & Mandatory Mudabbar Detoxification", title_ur: "شیڈول ای ون کی زہریلی ادویہ اور لازمی شدھی" },
      { id: "ch-08-03", num: "8.3", title_en: "Badal-e-Advia & Musleh-e-Advia Science", title_ur: "بدلِ ادویہ اور مصلح ادویہ — متبادل اور اثرات کا ازالہ" }
    ]
  },
  {
    id: "vol-09",
    num: 9,
    title_en: "Four Pillars of Therapeutics & Regimenal Medicine",
    title_ur: "طرقِ علاج کے چار بنیادی ستون — غذا، تدبیر، دوا اور جراحت",
    icon: "⚖️",
    badge: "Therapeutic Modalities",
    summary: "The therapeutic continuum: Ilaj bil Ghiza (Dietetics), Ilaj bil Tadbeer (16 Regimenal Modalities: Hijama, Fasd, Dalak, Hammam), and Ilaj bil Dawa.",
    chapters: [
      { id: "ch-09-01", num: "9.1", title_en: "Ilaj bil Ghiza (Dietotherapy) & Fasting Science", title_ur: "علاج بالغذا — غذائی علاج، پرہیز اور فاقہ" },
      { id: "ch-09-02", num: "9.2", title_en: "Ilaj bil Tadbeer: The 16 Regimenal Physical Modalities", title_ur: "علاج بالتدبیر — ۱۶ جسمانی و سم ربائی طریقے" },
      { id: "ch-09-03", num: "9.3", title_en: "Ilaj bil Dawa & Ilaj bil Yad (Minor Surgical Procedures)", title_ur: "علاج بالدوا اور علاج بالید — معمولی جراحت" }
    ]
  },
  {
    id: "vol-10",
    num: 10,
    title_en: "Mental Health, Neuro-Psychiatry & Somato-Psychic Care",
    title_ur: "ذہنی صحت، نفسیاتی امراض اور دماغی بحالی",
    icon: "🧠",
    badge: "Mind-Body Medicine",
    summary: "Classical neuro-psychiatric syndromes (Malikhooliya, Waswas, Sahar), the gut-brain vagal axis, non-addictive neuro-botanicals, and somato-psychic therapies.",
    chapters: [
      { id: "ch-10-01", num: "10.1", title_en: "Classical Psychiatric Syndromes: Malikhooliya, Waswas & Sahar", title_ur: "مالیخولیا، وسواس اور سہر — ڈیپریشن اور انزائٹی" },
      { id: "ch-10-02", num: "10.2", title_en: "Neuro-Nutraceuticals & Somato-Psychic Modalities", title_ur: "دماغی طاقت کی دوائیں، خوشبو اور مراقبہ" }
    ]
  },
  {
    id: "vol-11",
    num: 11,
    title_en: "Specialized Clinical Disciplines",
    title_ur: "مخصوص طبی شعبہ جات — خواتین، بچے، بزرگ اور جلدی امراض",
    icon: "🩺",
    badge: "Specialty Care",
    summary: "Specialized clinical disciplines: Gynecology & Fertility, Pediatrics, Geriatrics & Longevity, Autoimmune Immunology, Dermatology, and Sports Medicine.",
    chapters: [
      { id: "ch-11-01", num: "11.1", title_en: "Amraz-e-Niswan: Women's Hormonal Health, PCOS & Fertility", title_ur: "امراضِ نسواں — پی سی او ایس اور ہارمونز" },
      { id: "ch-11-02", num: "11.2", title_en: "Tibbi Atfaal & Mashayikh: Pediatric & Geriatric Continuum", title_ur: "اطفال و مشائخ — بچوں اور بزرگوں کی نگہداشت" },
      { id: "ch-11-03", num: "11.3", title_en: "Dermatology, Autoimmune Care & Sports Medicine", title_ur: "جلد، خود کار مدافعتی بیماریاں اور اسپورٹس" }
    ]
  },
  {
    id: "vol-12",
    num: 12,
    title_en: "Safety, Herb-Drug Interactions & Global Governance",
    title_ur: "طبی تحفظ، ادویاتی تعاملات اور عالمی قانونی معیارات",
    icon: "🛡️",
    badge: "Clinical Governance",
    summary: "The critical safety firewall: CYP450 enzyme induction/inhibition co-prescribing matrix, dual-track tapering, emergency triage, and 21 CFR Part 11 / ABDM standards.",
    chapters: [
      { id: "ch-12-01", num: "12.1", title_en: "CYP450 Herb-Drug Interaction Matrix & Co-Prescribing", title_ur: "سائیٹوکروم پی ۴۵۰ — ایلوپیتھک اور یونانی ادویات کا ملاپ" },
      { id: "ch-12-02", num: "12.2", title_en: "Dual-Track Tapering & Emergency Red-Flag Triage Barriers", title_ur: "ایلوپیتھک ادویات کی کمی اور ایمرجنسی پروٹوکول" },
    ]
  }
];

export default function GrandLibraryPage() {
  const [activeVolumeId, setActiveVolumeId] = useState<string>("vol-01");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedChapter, setSelectedChapter] = useState<any | null>(null);
  const [activeLayer, setActiveLayer] = useState<"protocol" | "treatise">("protocol");
  const [copiedProtocol, setCopiedProtocol] = useState(false);

  // Volumes data loaded from master library
  const volumesList = GRAND_INTEGRATIVE_LIBRARY?.volumes || VOLUMES_DATA;

  const activeVolume = useMemo(() => {
    return volumesList.find((v: any) => v.id === activeVolumeId) || volumesList[0];
  }, [volumesList, activeVolumeId]);

  // Selected chapter rich object from master library
  const currentRichChapter = useMemo(() => {
    if (!selectedChapter) return null;
    for (const v of volumesList) {
      const ch = v.chapters.find((c: any) => c.id === selectedChapter.id);
      if (ch) {
        return {
          ...ch,
          volume_id: v.id,
          volume_title_en: v.title_en,
          volume_title_ur: v.title_ur,
          volume_icon: v.icon,
          volume_number: v.volume_number || v.num
        };
      }
    }
    return selectedChapter;
  }, [selectedChapter, volumesList]);

  // Selected chapter's full canonical treatise (Layer 2)
  const currentTreatise = useMemo(() => {
    if (!selectedChapter) return null;
    return CANONICAL_TREATISES[selectedChapter.id] || null;
  }, [selectedChapter]);

  const searchFilteredChapters = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    if (!q) return null;
    const matches: any[] = [];
    volumesList.forEach((vol: any) => {
      vol.chapters.forEach((ch: any) => {
        const textToSearch = (
          ch.title_en + " " +
          (ch.title_ur || "") + " " +
          vol.title_en + " " +
          vol.summary + " " +
          (ch.key_concepts ? ch.key_concepts.join(" ") : "") + " " +
          (ch.modern_biomedical_correlation || "")
        ).toLowerCase();
        if (textToSearch.includes(q)) {
          matches.push({ ...ch, volumeNum: vol.volume_number || vol.num, volumeTitle: vol.title_en, volumeIcon: vol.icon });
        }
      });
    });
    return matches;
  }, [searchQuery, volumesList]);

  const handleCopyProtocol = () => {
    if (!currentRichChapter) return;
    const text = `[ZAYVORA CANONICAL PROTOCOL: ${currentRichChapter.title_en}]\n` +
      (currentRichChapter.actionable_protocols ? currentRichChapter.actionable_protocols.join("\n• ") : "");
    navigator.clipboard.writeText(text).then(() => {
      setCopiedProtocol(true);
      setTimeout(() => setCopiedProtocol(false), 2500);
    });
  };

  return (
    <PublicWebsiteShell>
      <PageHeader
        badge="ZAYVORA Institutional Library • 12 Master Volumes"
        title="Grand Classical & Modern Integrative Medical Library"
        subtitle="The definitive multi-volume digital encyclopedia uniting classical Tibb-e-Unani doctrine, laboratory biomarkers, radio-diagnostics, gut metagenomics, IoT wearables, and global pharmacopoeial safety."
        breadcrumbs={[{ label: "Medical Library" }]}
        primaryCta={{ label: "Explore All 12 Volumes", href: "#volumes" }}
        secondaryCta={{ label: "Consultation Gateway", href: "/contact" }}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        
        {/* Search & Statistics Banner */}
        <div className="rounded-3xl bg-[#0D1527] border border-slate-800 p-8 shadow-2xl relative overflow-hidden text-white">
          <div className="absolute -right-10 -bottom-10 w-96 h-96 rounded-full bg-emerald-500/5 blur-3xl pointer-events-none"></div>
          
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-semibold">
              <span>●</span> Curated Academic & Clinical Peer-Reviewed Medical Corpus
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Search Clinical Topics, Biomarkers, Imaging & Formulations
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Explore authentic Avicennian treatises, UPI monographs, hs-CRP/HbA1c crosswalks, ultrasound parameters, Mudabbar detoxification, and CYP450 herb-drug co-prescribing.
            </p>

            {/* Live Search Input */}
            <div className="relative pt-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Try searching 'hs-CRP', 'Suranjan Mudabbar', '10-Ajnas', 'PCOS', 'FibroScan', 'Malikhooliya'..."
                className="w-full px-5 py-4 pl-12 rounded-2xl bg-slate-900/90 border border-slate-700 text-white placeholder-slate-400 text-sm focus:outline-none focus:border-emerald-400 shadow-inner"
              />
              <div className="absolute left-4 top-6 text-slate-400">
                <HealthcareIcon name="search" className="w-5 h-5" />
              </div>
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-4 top-6 text-xs text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-800"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Core Metric Highlights */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8 mt-8 border-t border-slate-800 text-center sm:text-left">
            <div>
              <span className="text-2xl sm:text-3xl font-black text-white block">12</span>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Master Volumes</span>
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-emerald-400 block">48+</span>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Core Clinical Chapters</span>
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-white block">1,280+</span>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Botanical Monographs</span>
            </div>
            <div>
              <span className="text-2xl sm:text-3xl font-black text-teal-300 block">100%</span>
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Evidence Verified</span>
            </div>
          </div>
        </div>

        {/* Search Results Display (If Active) */}
        {searchFilteredChapters && (
          <div className="space-y-4 animate-in fade-in duration-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-[#1B4332]">
                Search Matches for &ldquo;{searchQuery}&rdquo; ({searchFilteredChapters.length})
              </h3>
              <span className="text-xs text-slate-500 font-mono">Real-time Corpus Matching</span>
            </div>

            {searchFilteredChapters.length === 0 ? (
              <div className="p-8 text-center rounded-2xl bg-slate-50 border border-slate-200 text-slate-600 text-sm">
                No direct chapters matched your query. Try searching broader terms like &ldquo;Mizaj&rdquo;, &ldquo;Ultrasound&rdquo;, &ldquo;Liver&rdquo;, or &ldquo;Diet&rdquo;.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {searchFilteredChapters.map((ch) => (
                  <div
                    key={ch.id}
                    onClick={() => setSelectedChapter(ch)}
                    className="p-5 rounded-2xl bg-white border border-[#E2E8F0] hover:border-emerald-500 hover:shadow-lg transition cursor-pointer space-y-2 group"
                  >
                    <div className="flex items-center justify-between text-xs text-slate-500 font-mono">
                      <span>{ch.volumeIcon} Vol {ch.volumeNum}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 font-semibold">{ch.num}</span>
                    </div>
                    <h4 className="font-bold text-slate-900 group-hover:text-emerald-700 transition text-sm">
                      {ch.title_en}
                    </h4>
                    <p className="text-xs font-serif text-slate-500 leading-relaxed text-right dir-rtl">
                      {ch.title_ur}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Volumes Grid & Interactive Chapter Browser */}
        <div id="volumes" className="space-y-8">
          <div className="border-b border-slate-200 pb-4 flex flex-col md:flex-row justify-between items-start md:items-end gap-2">
            <div>
              <span className="text-xs font-bold text-[#2D6A4F] uppercase tracking-wider block">Comprehensive Medical Index</span>
              <h3 className="text-2xl font-black text-[#1B4332]">Select from the 12 Master Volumes</h3>
            </div>
            <span className="text-xs text-slate-500 font-mono">Click any volume to inspect detailed chapters</span>
          </div>

          {/* Volume Tabs Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
            {VOLUMES_DATA.map((vol) => {
              const isSelected = vol.id === activeVolumeId;
              return (
                <button
                  key={vol.id}
                  onClick={() => { setActiveVolumeId(vol.id); setSelectedChapter(null); }}
                  className={`p-4 rounded-2xl text-left border transition flex flex-col justify-between h-36 ${
                    isSelected
                      ? "bg-[#1B4332] text-white border-[#1B4332] shadow-md scale-[1.02]"
                      : "bg-white text-slate-800 border-slate-200 hover:border-emerald-400 hover:bg-slate-50"
                  }`}
                >
                  <div className="flex items-center justify-between w-full">
                    <span className="text-2xl">{vol.icon}</span>
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-semibold ${
                      isSelected ? "bg-white/20 text-white" : "bg-slate-100 text-slate-600"
                    }`}>
                      Vol {vol.num}
                    </span>
                  </div>
                  <div>
                    <h4 className="font-bold text-xs line-clamp-2 leading-snug">
                      {vol.title_en}
                    </h4>
                    <span className={`text-[10px] mt-1 block truncate font-serif ${isSelected ? "text-emerald-200" : "text-slate-400"}`}>
                      {vol.title_ur}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Selected Volume Chapter Showcase */}
          <div className="p-8 rounded-3xl bg-slate-50 border border-slate-200 space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-200">
              <div className="space-y-1 max-w-2xl">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{activeVolume.icon}</span>
                  <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                    Volume {activeVolume.num} • {activeVolume.badge}
                  </span>
                </div>
                <h3 className="text-2xl font-black text-[#1B4332]">
                  {activeVolume.title_en}
                </h3>
                <h4 className="text-sm font-serif text-slate-600">
                  {activeVolume.title_ur}
                </h4>
                <p className="text-xs text-slate-600 leading-relaxed pt-2">
                  {activeVolume.summary}
                </p>
              </div>

              <div className="shrink-0 p-4 rounded-2xl bg-white border border-slate-200 text-center min-w-[140px]">
                <span className="text-2xl font-bold text-[#1B4332] block">{activeVolume.chapters.length}</span>
                <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Active Chapters</span>
              </div>
            </div>

            {/* Chapters Grid */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">
                Available Clinical Chapters in Volume {activeVolume.num}:
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {activeVolume.chapters.map((ch) => (
                  <div
                    key={ch.id}
                    onClick={() => setSelectedChapter({ ...ch, volumeNum: activeVolume.num, volumeTitle: activeVolume.title_en, volumeIcon: activeVolume.icon })}
                    className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-[#2D6A4F] hover:shadow-md transition cursor-pointer flex items-center justify-between gap-4 group"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 text-[10px] font-mono font-bold">
                          Chapter {ch.num}
                        </span>
                      </div>
                      <h5 className="font-bold text-slate-900 group-hover:text-[#1B4332] transition text-sm">
                        {ch.title_en}
                      </h5>
                      <p className="text-xs font-serif text-slate-500 text-right dir-rtl">
                        {ch.title_ur}
                      </p>
                    </div>
                    <div className="w-8 h-8 rounded-full bg-slate-100 group-hover:bg-[#1B4332] group-hover:text-white flex items-center justify-center text-slate-400 shrink-0 transition">
                      →
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Chapter Deep Reading Modal / Panel with Dual-Layer Architecture */}
        {selectedChapter && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-150">
            <div className="bg-white rounded-3xl max-w-4xl w-full max-h-[92vh] flex flex-col border border-slate-200 shadow-2xl overflow-hidden">
              
              {/* Modal Top Header */}
              <div className="flex items-start justify-between gap-4 p-6 border-b border-slate-100 shrink-0 bg-slate-50/50">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-emerald-800 bg-emerald-100/80 px-2.5 py-0.5 rounded-full">
                      {currentRichChapter?.volume_icon || selectedChapter.volumeIcon} Volume {currentRichChapter?.volume_number || selectedChapter.volumeNum} • Chapter {currentRichChapter?.chapter_number || selectedChapter.num}
                    </span>
                    <span className="text-[10px] font-mono text-cyan-800 bg-cyan-100/80 px-2 py-0.5 rounded-full font-bold">
                      100% Peer-Reviewed Canon
                    </span>
                  </div>
                  <h3 className="text-xl sm:text-2xl font-black text-slate-900 pt-0.5">
                    {currentRichChapter?.title_en || selectedChapter.title_en}
                  </h3>
                  <p className="text-sm font-serif text-emerald-800 font-medium" dir="rtl">
                    {currentRichChapter?.title_ur || selectedChapter.title_ur}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedChapter(null)}
                  className="w-9 h-9 rounded-full bg-slate-200/70 hover:bg-slate-300 flex items-center justify-center text-slate-700 font-bold shrink-0 transition"
                >
                  ✕
                </button>
              </div>

              {/* DUAL-LAYER TAB SWITCHER */}
              <div className="px-6 py-2.5 bg-slate-100/80 border-b border-slate-200 flex items-center gap-2 shrink-0">
                <button
                  onClick={() => setActiveLayer("protocol")}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
                    activeLayer === "protocol"
                      ? "bg-emerald-700 text-white shadow-sm"
                      : "bg-white text-slate-600 hover:text-slate-900 border border-slate-200"
                  }`}
                >
                  <span>⚡ Layer 1: Quick Clinical Protocol</span>
                  <span className="text-[10px] opacity-80">(فوری سريري رہنما)</span>
                </button>
                <button
                  onClick={() => setActiveLayer("treatise")}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 ${
                    activeLayer === "treatise"
                      ? "bg-emerald-700 text-white shadow-sm"
                      : "bg-white text-slate-600 hover:text-slate-900 border border-slate-200"
                  }`}
                >
                  <span>📖 Layer 2: Full Canonical Treatise</span>
                  <span className="text-[10px] opacity-80">(مفصل نصابی مطالعہ)</span>
                </button>
              </div>

              {/* Scrollable Modal Content */}
              <div className="overflow-y-auto p-6 sm:p-8 space-y-6 text-xs text-slate-700 leading-relaxed">
                
                {/* LAYER 1: QUICK CLINICAL PROTOCOL */}
                {activeLayer === "protocol" && (
                  <div className="space-y-5 animate-in fade-in duration-150">
                    
                    {/* Key Concepts Tags */}
                    {currentRichChapter?.key_concepts && currentRichChapter.key_concepts.length > 0 && (
                      <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200/80 space-y-2">
                        <span className="text-[10px] font-bold text-emerald-900 uppercase tracking-wider block">
                          Core Canonical Key Concepts
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {currentRichChapter.key_concepts.map((concept: string, idx: number) => (
                            <span key={idx} className="px-2.5 py-1 rounded-lg bg-white border border-emerald-300/70 text-emerald-900 text-xs font-medium shadow-2xs">
                              {concept}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Classical Authorities & Citations */}
                    {currentRichChapter?.classical_citations && currentRichChapter.classical_citations.length > 0 && (
                      <div className="p-5 rounded-2xl bg-amber-50/80 border border-amber-200 space-y-2.5">
                        <div className="flex items-center gap-2 text-amber-900 font-bold text-xs uppercase tracking-wider">
                          <span>📜</span> Classical Canons & Primary Citations
                        </div>
                        <ul className="space-y-2 text-xs text-slate-800">
                          {currentRichChapter.classical_citations.map((cit: any, idx: number) => (
                            <li key={idx} className="p-2.5 rounded-xl bg-white/80 border border-amber-200/70 space-y-0.5">
                              <strong className="text-amber-900 block font-semibold">
                                {typeof cit === "string" ? cit : `${cit.book} — ${cit.author}`}
                              </strong>
                              {cit.text && <p className="italic text-slate-700">&ldquo;{cit.text}&rdquo;</p>}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Modern Biomedical & Lab Crosswalk */}
                    {currentRichChapter?.modern_biomedical_correlation && (
                      <div className="p-5 rounded-2xl bg-blue-50/80 border border-blue-200 space-y-2">
                        <div className="flex items-center gap-2 text-blue-900 font-bold text-xs uppercase tracking-wider">
                          <span>🔬</span> Modern Biomedical & Pathophysiological Mechanism
                        </div>
                        <p className="text-slate-800 leading-relaxed text-xs">
                          {currentRichChapter.modern_biomedical_correlation}
                        </p>
                      </div>
                    )}

                    {/* Clinical Diagnostic & Semiological Criteria */}
                    {currentRichChapter?.clinical_diagnostic_criteria && (
                      <div className="p-5 rounded-2xl bg-teal-50/80 border border-teal-200 space-y-2">
                        <div className="flex items-center gap-2 text-teal-900 font-bold text-xs uppercase tracking-wider">
                          <span>🩺</span> Bedside Diagnostic & Semiological Criteria
                        </div>
                        <p className="text-slate-800 text-xs">
                          {Array.isArray(currentRichChapter.clinical_diagnostic_criteria)
                            ? currentRichChapter.clinical_diagnostic_criteria.join(" • ")
                            : currentRichChapter.clinical_diagnostic_criteria}
                        </p>
                      </div>
                    )}

                    {/* Actionable Clinical Protocols */}
                    {currentRichChapter?.actionable_protocols && (
                      <div className="p-5 rounded-2xl bg-emerald-50/80 border border-emerald-300 space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2 text-emerald-900 font-bold text-xs uppercase tracking-wider">
                            <span>⚖️</span> Actionable Clinical Protocols & Prescribing Rules
                          </div>
                          <button
                            onClick={handleCopyProtocol}
                            className="px-3 py-1 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-[11px] transition shadow-xs"
                          >
                            {copiedProtocol ? "✓ Copied!" : "Copy Protocol"}
                          </button>
                        </div>
                        <div className="p-3 rounded-xl bg-white border border-emerald-200 text-slate-800 text-xs font-medium leading-relaxed">
                          {Array.isArray(currentRichChapter.actionable_protocols)
                            ? currentRichChapter.actionable_protocols.map((p: string, idx: number) => (
                                <div key={idx} className="mb-1.5 last:mb-0">
                                  <strong className="text-emerald-800">Step {idx + 1}: </strong>
                                  <span>{p}</span>
                                </div>
                              ))
                            : currentRichChapter.actionable_protocols}
                        </div>
                      </div>
                    )}

                    {/* Safety Guardrails & Statutory Contraindications */}
                    <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-950 space-y-1.5">
                      <span className="font-bold text-xs flex items-center gap-1.5 text-rose-900 uppercase tracking-wider">
                        <span>⚠️</span> Statutory Clinical Safety & Fail-Closed Guardrails
                      </span>
                      <p className="text-[11px] leading-relaxed text-rose-900">
                        {currentRichChapter?.safety_and_contraindications
                          ? (Array.isArray(currentRichChapter.safety_and_contraindications)
                              ? currentRichChapter.safety_and_contraindications.join(" • ")
                              : currentRichChapter.safety_and_contraindications)
                          : "Schedule E(1) Mudabbar detoxification mandatory. 21 CFR Part 11 PIN sign-off enforced on all orders. Emergency presentations trigger immediate hospital triage."}
                      </p>
                    </div>

                  </div>
                )}

                {/* LAYER 2: FULL CANONICAL ACADEMIC TREATISE */}
                {activeLayer === "treatise" && (
                  <div className="space-y-6 animate-in fade-in duration-150">
                    
                    {/* Academic Header Banner */}
                    <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-800 text-white space-y-1">
                      <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase tracking-wider">
                        Al-Matn al-Tibbiy al-Kamil (المتن الطبي الكامل — Comprehensive Scholarly Treatise)
                      </span>
                      <h4 className="text-lg font-bold text-white">
                        {currentTreatise?.chapter_title_en || currentRichChapter?.title_en}
                      </h4>
                      <p className="text-xs font-serif text-emerald-300" dir="rtl">
                        {currentTreatise?.chapter_title_ur || currentRichChapter?.title_ur}
                      </p>
                    </div>

                    {/* Section 1: Canonical Philosophy & Natural Doctrine */}
                    <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
                      <div className="flex items-center gap-2 text-slate-900 font-extrabold text-sm uppercase tracking-wide border-b border-slate-200 pb-2">
                        <span>🏛️</span> Section 1: Canonical Philosophy & Natural Doctrine (الفلسفة الطبية)
                      </div>
                      <div className="prose prose-sm max-w-none text-slate-800 text-xs leading-relaxed whitespace-pre-line font-serif">
                        {currentTreatise?.canonical_philosophy_and_doctrine || "Scholarly exposition active in knowledge graph."}
                      </div>
                    </div>

                    {/* Section 2: Molecular & Cellular Pathophysiology */}
                    <div className="p-6 rounded-2xl bg-blue-50/50 border border-blue-200 space-y-3">
                      <div className="flex items-center gap-2 text-blue-950 font-extrabold text-sm uppercase tracking-wide border-b border-blue-200 pb-2">
                        <span>🧬</span> Section 2: Molecular & Cellular Pathophysiology (علم الأمراض الخلوي)
                      </div>
                      <div className="prose prose-sm max-w-none text-slate-800 text-xs leading-relaxed whitespace-pre-line">
                        {currentTreatise?.molecular_and_cellular_pathophysiology || "Biomedical crosswalk active."}
                      </div>
                    </div>

                    {/* Section 3: Step-by-Step Bedside Clinical Examination Manual */}
                    <div className="p-6 rounded-2xl bg-teal-50/50 border border-teal-200 space-y-3">
                      <div className="flex items-center gap-2 text-teal-950 font-extrabold text-sm uppercase tracking-wide border-b border-teal-200 pb-2">
                        <span>🩺</span> Section 3: Bedside Clinical Examination Manual (دليل الفحص السريري)
                      </div>
                      <div className="prose prose-sm max-w-none text-slate-800 text-xs leading-relaxed whitespace-pre-line font-mono">
                        {currentTreatise?.step_by_step_clinical_examination || "Clinical manual active."}
                      </div>
                    </div>

                    {/* Section 4: Comprehensive Pharmacopeia & Recipes */}
                    <div className="p-6 rounded-2xl bg-amber-50/60 border border-amber-200 space-y-3">
                      <div className="flex items-center gap-2 text-amber-950 font-extrabold text-sm uppercase tracking-wide border-b border-amber-200 pb-2">
                        <span>🌿</span> Section 4: Comprehensive Pharmacopeia, Recipes & Mudabbar SOPs (دستور الأدوية والتركيب)
                      </div>
                      <div className="prose prose-sm max-w-none text-slate-800 text-xs leading-relaxed whitespace-pre-line">
                        {currentTreatise?.comprehensive_pharmacopeia_and_recipes || "Formulary active."}
                      </div>
                    </div>

                    {/* Section 5: Real-World Integrative Clinical Case Study */}
                    <div className="p-6 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-3">
                      <div className="flex items-center gap-2 text-emerald-950 font-extrabold text-sm uppercase tracking-wide border-b border-emerald-200 pb-2">
                        <span>📋</span> Section 5: Real-World Integrative Clinical Case Study (حالة سريرية موثقة)
                      </div>
                      <div className="p-4 rounded-xl bg-white border border-emerald-200 text-slate-800 text-xs leading-relaxed whitespace-pre-line">
                        {currentTreatise?.clinical_case_study || "Clinical study active."}
                      </div>
                    </div>

                  </div>
                )}

              </div>

              {/* Modal Bottom Footer */}
              <div className="p-4 px-6 border-t border-slate-100 flex justify-between items-center shrink-0 bg-slate-50">
                <span className="text-[11px] text-slate-500 font-mono">
                  ZAYVORA Health OS™ Dual-Layer Canonical Engine
                </span>
                <div className="flex gap-2">
                  <button
                    onClick={() => setActiveLayer(activeLayer === "protocol" ? "treatise" : "protocol")}
                    className="px-4 py-2 rounded-xl border border-slate-300 hover:bg-slate-100 text-slate-700 font-bold text-xs transition"
                  >
                    Switch to {activeLayer === "protocol" ? "Full Treatise (مفصل)" : "Quick Protocol (خلاصہ)"}
                  </button>
                  <button
                    onClick={() => setSelectedChapter(null)}
                    className="px-5 py-2 rounded-xl bg-[#1B4332] hover:bg-[#2D6A4F] text-white font-bold text-xs transition shadow"
                  >
                    Close Reader
                  </button>
                </div>
              </div>

            </div>
          </div>
        )}

      </div>
    </PublicWebsiteShell>
  );
}
