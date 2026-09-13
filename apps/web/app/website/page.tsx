"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";

export default function PublicHomePage() {
  // Live hardware telemetry state
  const [pulseBpm, setPulseBpm] = useState(72);
  const [coldChainTemp, setColdChainTemp] = useState(19.4);
  const [bleDevices, setBleDevices] = useState(4);
  const [activeStageIndex, setActiveStageIndex] = useState(0);

  // Mini Mizaj assessment state
  const [mizajAnswers, setMizajAnswers] = useState({
    temp: "cold",
    moisture: "moist",
    physique: "broad",
    sleep: "deep"
  });

  // Canvas for Nabz 10-Ajnas pulse wave simulation
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let t = 0;

    const render = () => {
      t += 0.05;
      const width = canvas.width;
      const height = canvas.height;

      ctx.fillStyle = "#0F172A";
      ctx.fillRect(0, 0, width, height);

      // Draw grid
      ctx.strokeStyle = "rgba(51, 65, 85, 0.4)";
      ctx.lineWidth = 1;
      for (let x = 0; x < width; x += 30) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Draw arterial PPG waveform: systolic peak + dicrotic wave
      ctx.strokeStyle = "#2DD4BF";
      ctx.lineWidth = 2.5;
      ctx.beginPath();

      const midY = height / 2;
      for (let x = 0; x < width; x++) {
        const cycle = ((x - t * 40) % 120 + 120) % 120;
        let val = 0;
        if (cycle >= 0 && cycle < 30) {
          // Systolic upstroke & rapid fall
          val = Math.sin((cycle / 30) * Math.PI) * 32;
        } else if (cycle >= 30 && cycle < 60) {
          // Dicrotic notch and secondary wave
          val = Math.sin(((cycle - 30) / 30) * Math.PI) * 14;
        } else {
          // Diastolic decay
          val = Math.sin(((cycle - 60) / 60) * Math.PI * 0.5) * 4;
        }
        const y = midY - val;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  // Telemetry fluctuation simulator
  useEffect(() => {
    const interval = setInterval(() => {
      setPulseBpm(Math.floor(70 + Math.random() * 5));
      setColdChainTemp(Number((19.2 + Math.random() * 0.4).toFixed(1)));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // 12-Stage Closed-Loop Clinical Continuum
  const clinicalStages = [
    {
      num: "01",
      name: "KNOW",
      title: "Codified Knowledge & Evidence Retrieval",
      latin: "ZKB Pharmacopoeia Integration",
      desc: "Instant multi-hop traversal of UPI and NFUM classical monographs, Badal (substitutes), Musleh (correctives), and pharmacological affinities.",
      action: "Queried 1,280+ canonical botanical monographs with verified HPLC fingerprints."
    },
    {
      num: "02",
      name: "ASSESS",
      title: "10-Ajnas Longitudinal Mizaj Evaluation",
      latin: "Al-Ajnas al-Ashrah",
      desc: "Rigorous objective quantification across the 10 classical pulse criteria (Miqdar, Kayfiyat-e-Qar', Zamanah, Qawam, Khalwa, Mala, etc.) and tongue chromametry.",
      action: "Evaluates hot/cold, moist/dry deviations against patient baseline."
    },
    {
      num: "03",
      name: "DIFFERENTIATE",
      title: "Biomedical & Humoral Dual Assessment",
      latin: "Tashkheesh-e-Murakkab",
      desc: "Harmonizes classical Su-e-Mizaj humoral dyscrasias with modern ICD-10 diagnostic classifications, metabolic panels, and immunological markers.",
      action: "Cross-references biochemical lab results with humoral disharmonies."
    },
    {
      num: "04",
      name: "VERIFY",
      title: "Spectral Lab & Acoustic Scribe Validation",
      latin: "Lisan & Nabz Hardware Verification",
      desc: "Multispectral tongue imaging at 415nm, 560nm, 660nm, and 850nm paired with 100 Hz arterial PPG waveform analysis to establish objective physical signs.",
      action: "Hardware-confirmed coating thickness, moisture, and arterial elasticity."
    },
    {
      num: "05",
      name: "PERSONALIZE",
      title: "ZAPE Vitality & Posology Adaptation",
      latin: "ZAYVORA Adaptive Posology Engine",
      desc: "Calculates individual drug absorption, hepatic clearance, age, seasonal temperament (Fasl), and circadian timing (Anupan vehicle selection).",
      action: "Generates patient-specific dosing vectors with required correctives (Musleh)."
    },
    {
      num: "06",
      name: "PLAN",
      title: "Tri-Modal Regimen Synthesis",
      latin: "Ilaj bil-Ghiza, Tadbeer, Dawa",
      desc: "Simultaneous formulation of dietary directives (Dietetics), non-pharmacological regimenal therapies (Hijama, Natool, Zimad), and tailored botanical compounds.",
      action: "Synthesizes multi-week Afaal treatment roadmap with dietary prohibitions."
    },
    {
      num: "07",
      name: "TREAT",
      title: "21 CFR Part 11 Clinician Digital Signature",
      latin: "Statutory Clinician Discretion Barrier",
      desc: "Mandatory non-delegable clinical review. Prescriptions remain cryptographically locked until a credentialed Senior Tabeeb signs with cryptographic token.",
      action: "Zero automated autonomous prescribing; safe_to_lock=False strictly enforced."
    },
    {
      num: "08",
      name: "MONITOR",
      title: "IoT Wearable Telemetry & Relapse Forecasting",
      latin: "Asbab-e-Sittah Sensor Stream",
      desc: "Continuous BLE telemetry tracking sleep architecture, heart rate variability, skin temperature, and activity to anticipate humoral relapse before symptoms emerge.",
      action: "Real-time relapse prediction score updated every 15 minutes."
    },
    {
      num: "09",
      name: "MEASURE",
      title: "Longitudinal PROMs & Clinical Trajectory",
      latin: "Patient-Reported Outcomes (VAS / WOMAC)",
      desc: "Systematic tracking of functional mobility, pain attenuation curves, inflammatory marker reduction, and Meezan-e-Sehat 0-100 scores over time.",
      action: "Validates symptomatic and systemic recovery across weekly milestones."
    },
    {
      num: "10",
      name: "LEARN",
      title: "Real-World Evidence (RWE) Aggregation",
      latin: "De-Identified Observational Registry",
      desc: "Secure aggregation of clinical response vectors into HIPAA/ABDM-compliant research cohorts for botanical efficacy benchmarking.",
      action: "1,240+ multi-center clinical subjects actively contributing RWE insights."
    },
    {
      num: "11",
      name: "VALIDATE",
      title: "Academic Multi-Center Concordance",
      latin: "DSMB & University Consortium Review",
      desc: "Formal concordance analysis between traditional Unani diagnostics and blinded clinical specialist evaluations across 3 university hospitals.",
      action: "Maintains 94.2% diagnostic concordance across enrolled clinical trials."
    },
    {
      num: "12",
      name: "IMPROVE",
      title: "Governance Board Quorum & Protocol Evolution",
      latin: "3/3 Senior Specialist Quorum",
      desc: "Continuous clinical protocol updates requiring unanimous signed approval from Chief Clinician, Pharmacognosist, and Medical Director.",
      action: "Auditable governance log with immutable cryptographic Merkle tree hashes."
    }
  ];

  // 6 Specialized Clinical Care Areas
  const careAreas = [
    {
      id: "metabolic",
      name: "Metabolic & Endocrine Disorders",
      desc: "Su-e-Mizaj Barid Balghami management, insulin sensitivity, lipid dyscrasia, and metabolic syndrome reversal.",
      icon: "⚡",
      regimen: "Munzij-Mushil Balgham + MetaboCore Elite + Low-Glycemic Warm Diet"
    },
    {
      id: "joints",
      name: "Musculoskeletal & Joint Care (Mafasil)",
      desc: "Osteoarthritis, rheumatoid arthralgia, synovial fluid restoration, and peri-articular exudate resolution.",
      icon: "🦴",
      regimen: "Habb-e-Suranjan Forte + Medicated Natool Irrigation + Zimad Poultice"
    },
    {
      id: "gut-liver",
      name: "Liver & Gastrointestinal Axis (Kabid-Mida)",
      desc: "Hepatobiliary stasis, non-alcoholic fatty liver, dyspeptic stasis, and gut microbiome humoral balance.",
      icon: "🌿",
      regimen: "LiverPrime Core + Majun Dabeed-ul-Ward + Arq-e-Badiyan Anupan"
    },
    {
      id: "fertility",
      name: "Reproductive Vitality & Fertility",
      desc: "Male spermatogenic renewal and female follicular equilibrium via classical Muqawwiyat and endocrine harmonizers.",
      icon: "👶",
      regimen: "ManiVital Pro / OvaSync + Asbab-e-Sittah Circadian Sleep Calibration"
    },
    {
      id: "neuro",
      name: "Neuro-Psychiatric & Sleep Disorders",
      desc: "Chronic stress adaptation, GABAergic modulation, vagal nerve restoration, and restorative non-REM sleep.",
      icon: "🧠",
      regimen: "NeuroCalmX + NightOne X + Roghan-e-Badaam Shireen Nasal Drops"
    },
    {
      id: "preventive",
      name: "Preventive Health & Hifz-e-Sehat",
      desc: "Codified adherence to the Six Essential Precepts (Asbab-e-Sittah الضرورية) for lifelong immunity and vitality.",
      icon: "🛡️",
      regimen: "Seasonal Fasl Detoxification + Qalb-e-Salim + Personalized Ghiza Plan"
    }
  ];

  // Complete 10 Botanical Formulations Portfolio
  const allProducts = [
    {
      id: "manivital-pro",
      name: "ManiVital Pro",
      category: "Fertility & Vitality",
      price: "₹1,450",
      desc: "Targeted spermatogenic renewal formulation with Withania somnifera and purified Mucuna pruriens.",
      monograph: "UPI Vol. 1, p. 112 | HPLC Withanolide A > 2.5%"
    },
    {
      id: "ovasync",
      name: "OvaSync",
      category: "Fertility & Vitality",
      price: "₹1,380",
      desc: "Ovarian reserve and hormonal rhythm balancer with standardized Asparagus racemosus saponins.",
      monograph: "NFUM Part II, p. 74 | Shatavarin IV > 1.8%"
    },
    {
      id: "metabocore-elite",
      name: "MetaboCore Elite",
      category: "Metabolic Care",
      price: "₹1,250",
      desc: "Potent metabolic regulator featuring Gymnema sylvestre gymnemic acids and Berberis aristata.",
      monograph: "UPI Vol. 3, p. 89 | Berberine HCl > 8.0%"
    },
    {
      id: "liverprime-core",
      name: "LiverPrime Core",
      category: "Hepatobiliary",
      price: "₹1,150",
      desc: "Hepatoprotective and bile-regulating compound backed by classical Unani pharmacopoeia.",
      monograph: "UPI Vol. 2, p. 45 | Kutkin Assay > 4.2%"
    },
    {
      id: "neurocalmx",
      name: "NeuroCalmX",
      category: "Neuro-Psychiatric",
      price: "₹1,200",
      desc: "Nootropic stress modulator and adaptogenic nerve tonic with Convolvulus pluricaulis.",
      monograph: "NFUM Part I, p. 188 | Shankhpushpine > 1.2%"
    },
    {
      id: "nightone-x",
      name: "NightOne X",
      category: "Neuro-Psychiatric",
      price: "₹1,320",
      desc: "Restorative deep sleep confection enriched with Valeriana wallichii and Nardostachys jatamansi.",
      monograph: "UPI Vol. 4, p. 62 | Valerenic Acid > 0.8%"
    },
    {
      id: "qalb-e-salim",
      name: "Qalb-e-Salim Cardio Tonic",
      category: "Cardiovascular",
      price: "₹1,490",
      desc: "Classical Terminalia arjuna and Salvia haematodes cardio-protective vascular tonic.",
      monograph: "Al-Qanoon fit-Tibb | Arjunic Acid > 1.5%"
    },
    {
      id: "habbe-suranjan-forte",
      name: "Habb-e-Suranjan Forte",
      category: "Joints & Mafasil",
      price: "₹980",
      desc: "Mudabbar Colchicum luteum with Kateera corrective for rapid relief of joint inflammation.",
      monograph: "UPI Vol. 1, p. 98 | Schedule E(1) Mudabbar Verified"
    },
    {
      id: "majun-dabeed",
      name: "Majun Dabeed-ul-Ward",
      category: "Hepatobiliary",
      price: "₹850",
      desc: "Classical compound for chronic liver enlargement, gastritis, and systemic humoral cleansing.",
      monograph: "NFUM Part I, p. 210 | Rosa damascena Essence"
    },
    {
      id: "itrifal-ustukhuddus",
      name: "Itrifal Ustukhuddus",
      category: "Neuro & Head Care",
      price: "₹720",
      desc: "Lavandula stoechas cerebral purifier for chronic migraine, sinusitis, and cold-matter clearance.",
      monograph: "NFUM Part III, p. 33 | Lavandula Stoechas > 5.0%"
    }
  ];

  // Calculate calculated Mizaj based on mini-quiz
  const calculateMizaj = () => {
    const { temp, moisture } = mizajAnswers;
    if (temp === "hot" && moisture === "moist") return { name: "Damawi (Sanguine)", trait: "Warm & Moist", affinity: "Qalb & Damm (Circulation)" };
    if (temp === "hot" && moisture === "dry") return { name: "Safrawi (Choleric)", trait: "Warm & Dry", affinity: "Kabid & Safra (Liver & Bile)" };
    if (temp === "cold" && moisture === "moist") return { name: "Balghami (Phlegmatic)", trait: "Cold & Moist", affinity: "Mida & Dimagh (Gut & Brain)" };
    return { name: "Sawdawi (Melancholic)", trait: "Cold & Dry", affinity: "Tihal & A'sab (Spleen & Nerves)" };
  };

  const calculatedMizaj = calculateMizaj();

  return (
    <div className="space-y-16 pb-20">
      
      {/* Top Banner / Breadcrumb */}
      <div className="bg-[#0A0F1D] border-b border-[#1E293B] py-2 px-6">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-2 text-xs text-[#94A3B8]">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span className="font-semibold text-emerald-400">ZAYVORA Health OS™ v5.0 Live Production Network</span>
            <span className="text-[#475569]">|</span>
            <span>21 CFR Part 11 Clinically Governed</span>
          </div>
          <div className="flex items-center gap-4 text-[11px]">
            <Link href="/" className="text-[#2DD4BF] hover:underline font-semibold">Open Executive Cockpit →</Link>
            <Link href="/patient" className="hover:text-white">Patient Portal</Link>
            <Link href="/doctor" className="hover:text-white">Doctor Workspace</Link>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-8 pb-16 border-b border-[#334155] bg-gradient-to-b from-[#0F172A] via-[#0D1526] to-[#0A0F1D]">
        <div className="max-w-7xl mx-auto px-6 text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#0D9488]/15 border border-[#0D9488]/30 text-[#2DD4BF] text-xs font-semibold shadow-inner">
            <span>Codified Greco-Arab Wisdom + Molecular Omics Intelligence</span>
          </div>
          
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
            Ancient Wisdom. Modern Science. <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#2DD4BF] via-[#14B8A6] to-emerald-400">Intelligent Healthcare.</span>
          </h1>

          <p className="text-base sm:text-lg text-[#94A3B8] max-w-3xl mx-auto leading-relaxed">
            ZAYVORA Health OS™ unites 1,000 years of codified Unani medicine (*Tibb-e-Unani*) with state-of-the-art clinical AI, longitudinal 10-Ajnas Mizaj profiling, organ-axis cross-talk, IoT diagnostic hardware, and 21 CFR Part 11 medical governance.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <Link href="/website/book" className="px-7 py-3.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-sm shadow-xl shadow-teal-900/30 transition transform hover:-translate-y-0.5">
              Book Doctor Consultation
            </Link>
            <Link href="/website/philosophy" className="px-7 py-3.5 rounded-xl border border-[#334155] bg-[#1E293B]/70 hover:bg-[#1E293B] text-white font-semibold text-sm transition">
              Explore Clinical Philosophy →
            </Link>
            <Link href="/website/herbals" className="px-7 py-3.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20 font-semibold text-sm transition">
              View Herbals Store
            </Link>
          </div>

          {/* Clinical Credentials Pills */}
          <div className="flex flex-wrap items-center justify-center gap-6 pt-6 text-xs text-[#94A3B8]">
            <span className="flex items-center gap-1.5"><span className="text-emerald-400">✓</span> AYUSH GMP Certified</span>
            <span className="flex items-center gap-1.5"><span className="text-emerald-400">✓</span> HPLC Active Fingerprinted</span>
            <span className="flex items-center gap-1.5"><span className="text-emerald-400">✓</span> Schedule E(1) Mudabbar Verified</span>
            <span className="flex items-center gap-1.5"><span className="text-emerald-400">✓</span> ABDM & FHIR R4 Ready</span>
          </div>
        </div>
      </section>

      {/* Live Diagnostic Hardware Telemetry Bar */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="p-6 rounded-3xl bg-[#0F172A] border border-[#334155] shadow-2xl space-y-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-[#1E293B] pb-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-xs font-bold text-[#2DD4BF] uppercase tracking-wider">Clinical Diagnostic Hardware Stream</span>
              </div>
              <h2 className="text-xl font-bold text-white mt-1">Live Sensor Mesh & DSP Telemetry</h2>
            </div>
            <div className="flex items-center gap-3 text-xs">
              <span className="px-3 py-1 rounded-lg bg-[#1E293B] text-emerald-400 font-mono font-bold border border-emerald-500/30">
                Mesh Sync: 100 Hz
              </span>
              <span className="px-3 py-1 rounded-lg bg-[#1E293B] text-[#94A3B8] font-mono">
                Latency: 12ms
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            {/* Real-time Arterial PPG Waveform Canvas */}
            <div className="lg:col-span-5 p-4 rounded-2xl bg-[#0A0F1D] border border-[#1E293B] space-y-3">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-white flex items-center gap-1.5">
                  <span className="text-teal-400">📊</span> Nabz 10-Ajnas Arterial PPG Wave
                </span>
                <span className="font-mono text-emerald-400 font-bold">{pulseBpm} BPM (Bat'ee)</span>
              </div>
              
              <canvas
                ref={canvasRef}
                width={380}
                height={120}
                className="w-full h-28 rounded-lg bg-[#0F172A] border border-[#1E293B]"
              />

              <div className="grid grid-cols-3 gap-2 text-[10px] text-[#94A3B8] font-mono">
                <div className="p-1.5 rounded bg-[#1E293B]/70">
                  <span className="block text-white font-bold">Kayfiyat</span>
                  <span>Layyin (Soft)</span>
                </div>
                <div className="p-1.5 rounded bg-[#1E293B]/70">
                  <span className="block text-white font-bold">Miqdar</span>
                  <span>Azeem (Large)</span>
                </div>
                <div className="p-1.5 rounded bg-[#1E293B]/70">
                  <span className="block text-white font-bold">Zamanah</span>
                  <span>Bat'ee (Slow)</span>
                </div>
              </div>
            </div>

            {/* 3 Satellite Hardware Sensors */}
            <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Lisan Multispectral Camera */}
              <div className="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xl">👅</span>
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-blue-500/20 text-blue-300 font-bold">SPECTRAL</span>
                </div>
                <h4 className="text-xs font-bold text-white">Lisan Tongue Analysis</h4>
                <div className="text-[11px] text-[#94A3B8] space-y-1">
                  <div className="flex justify-between"><span>Coating:</span> <strong className="text-white">Saburra (Whitish)</strong></div>
                  <div className="flex justify-between"><span>Moisture:</span> <strong className="text-emerald-400">Rutubat 68%</strong></div>
                  <div className="flex justify-between"><span>NIR Index:</span> <strong className="text-white">88.4%</strong></div>
                  <div className="flex justify-between"><span>Humoral:</span> <strong className="text-amber-400">Balghami</strong></div>
                </div>
              </div>

              {/* Dispensary Cold-Chain IoT */}
              <div className="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xl">❄️</span>
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-emerald-500/20 text-emerald-300 font-bold">COLD-CHAIN</span>
                </div>
                <h4 className="text-xs font-bold text-white">Dispensary IoT Storage</h4>
                <div className="text-[11px] text-[#94A3B8] space-y-1">
                  <div className="flex justify-between"><span>Chamber Temp:</span> <strong className="text-emerald-400">{coldChainTemp}°C</strong></div>
                  <div className="flex justify-between"><span>Target Range:</span> <strong className="text-white">15°C - 25°C</strong></div>
                  <div className="flex justify-between"><span>Humidity:</span> <strong className="text-white">42% RH</strong></div>
                  <div className="flex justify-between"><span>FEFO Gate:</span> <strong className="text-emerald-400">LOCKED SECURE</strong></div>
                </div>
              </div>

              {/* Wearables BLE Gateway */}
              <div className="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xl">📡</span>
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-purple-500/20 text-purple-300 font-bold">BLE MESH</span>
                </div>
                <h4 className="text-xs font-bold text-white">Wearables Gateway</h4>
                <div className="text-[11px] text-[#94A3B8] space-y-1">
                  <div className="flex justify-between"><span>Paired Nodes:</span> <strong className="text-purple-300">{bleDevices} Active</strong></div>
                  <div className="flex justify-between"><span>SpO2 Level:</span> <strong className="text-emerald-400">98% Normal</strong></div>
                  <div className="flex justify-between"><span>HRV Index:</span> <strong className="text-white">58 ms</strong></div>
                  <div className="flex justify-between"><span>Relapse Risk:</span> <strong className="text-emerald-400">0.04 (Minimal)</strong></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive 12-Stage Closed-Loop Clinical Continuum */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Clinical Protocol Framework</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">The 12-Stage Closed-Loop Clinical Continuum</h2>
          <p className="text-xs md:text-sm text-[#94A3B8] max-w-2xl mx-auto">
            Every patient encounter is anchored in codified classical evidence, verified through diagnostic hardware, adapted to individual vitality, and locked by licensed clinicians.
          </p>
        </div>

        {/* 12 Clickable Stage Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
          {clinicalStages.map((stage, idx) => {
            const isActive = idx === activeStageIndex;
            return (
              <button
                key={stage.name}
                onClick={() => setActiveStageIndex(idx)}
                className={`p-3.5 rounded-xl text-left border transition-all ${
                  isActive
                    ? "bg-[#0D9488]/20 border-[#2DD4BF] shadow-lg shadow-teal-900/20"
                    : "bg-[#1E293B] border-[#334155] hover:border-[#0D9488]/50"
                }`}
              >
                <div className="flex items-center justify-between text-[11px] font-mono font-bold">
                  <span className={isActive ? "text-[#2DD4BF]" : "text-[#64748B]"}>{stage.num}.</span>
                  <span className={isActive ? "text-white font-bold" : "text-[#94A3B8]"}>{stage.name}</span>
                </div>
                <p className="text-[11px] text-[#CBD5E1] mt-1.5 line-clamp-1 font-semibold">{stage.title}</p>
              </button>
            );
          })}
        </div>

        {/* Active Stage Detailed Deep-Dive Card */}
        <div className="p-6 md:p-8 rounded-3xl bg-gradient-to-r from-[#1E293B] via-[#0F172A] to-[#1E293B] border border-[#2DD4BF]/40 space-y-4 shadow-xl">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-[#334155] pb-4">
            <div>
              <span className="text-xs font-mono font-bold text-[#2DD4BF]">STAGE {clinicalStages[activeStageIndex].num} OF 12</span>
              <h3 className="text-xl md:text-2xl font-bold text-white mt-0.5">
                {clinicalStages[activeStageIndex].name}: {clinicalStages[activeStageIndex].title}
              </h3>
              <span className="text-xs text-emerald-400 font-serif italic">{clinicalStages[activeStageIndex].latin}</span>
            </div>
            <div className="px-4 py-1.5 rounded-full bg-[#0D9488]/20 border border-[#0D9488]/40 text-[#2DD4BF] text-xs font-semibold">
              Live Verified Standard
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-[#94A3B8] uppercase">Clinical Mechanism</h4>
              <p className="text-sm text-[#CBD5E1] leading-relaxed">
                {clinicalStages[activeStageIndex].desc}
              </p>
            </div>
            <div className="space-y-2 bg-[#0A0F1D] p-4 rounded-xl border border-[#334155]">
              <h4 className="text-xs font-bold text-[#2DD4BF] uppercase">Clinical Execution & Safety Output</h4>
              <p className="text-xs text-[#94A3B8] leading-relaxed font-mono">
                {clinicalStages[activeStageIndex].action}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4-Stage Afaal Treatment Cascade */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Humoral Healing Continuum</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">The ZAYVORA Afaal Treatment Cascade</h2>
          <p className="text-xs md:text-sm text-[#94A3B8] max-w-xl mx-auto">
            Unlike superficial pharmaceutical suppression, our clinical protocol restores innate vitality (*Tabi'at*) through four systematic phases:
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 hover:border-emerald-500/50 transition">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-emerald-400">STAGE 01</span>
              <span className="text-xs text-[#64748B]">Days 1 - 14</span>
            </div>
            <h3 className="text-lg font-bold text-white">Tanqiya</h3>
            <span className="text-xs text-[#2DD4BF] block font-semibold">Humoral Cleansing & Detoxification</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Targeted concoction and elimination of accumulated cold, phlegmatic, or bilious morbid matter (*Mawad-e-Fasida*) through concoctive Munzaj pharmacotherapy and gentle cupping (*Hijama*).
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 hover:border-blue-500/50 transition">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-blue-400">STAGE 02</span>
              <span className="text-xs text-[#64748B]">Days 15 - 30</span>
            </div>
            <h3 className="text-lg font-bold text-white">Tahleel</h3>
            <span className="text-xs text-blue-400 block font-semibold">Resolution of Inflammation</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Dissolution of deep-seated peri-articular exudates and microvascular stasis via medicated warm fomentations (*Natool*), poultices (*Zimad*), and classical resolvent botanicals.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 hover:border-purple-500/50 transition">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-purple-400">STAGE 03</span>
              <span className="text-xs text-[#64748B]">Days 31 - 60</span>
            </div>
            <h3 className="text-lg font-bold text-white">Taqwiyaat</h3>
            <span className="text-xs text-purple-400 block font-semibold">Organ & Tissue Restoration</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Targeted nourishment of compromised primary organs and neural pathways (*Muqawwiyat-e-A'za*) to rebuild functional stamina and prevent recurring pathological deposition.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 hover:border-amber-500/50 transition">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-amber-400">STAGE 04</span>
              <span className="text-xs text-[#64748B]">Lifelong</span>
            </div>
            <h3 className="text-lg font-bold text-white">Hifz</h3>
            <span className="text-xs text-amber-400 block font-semibold">Homeostasis & Preservation</span>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Sustained physiological equilibrium through personalized dietetics (*Ilaj bil-Ghiza*) and strict daily adherence to the Six Essential Lifestyle Precepts (*Asbab-e-Sittah*).
            </p>
          </div>
        </div>
      </section>

      {/* Interactive Mini Mizaj Self-Assessment */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="p-6 md:p-8 rounded-3xl bg-[#0F172A] border border-[#334155] space-y-6">
          <div className="text-center space-y-1">
            <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Individualized Health Architecture</span>
            <h2 className="text-2xl font-bold text-white">Discover Your Innate Humoral Mizaj</h2>
            <p className="text-xs text-[#94A3B8] max-w-lg mx-auto">
              Answer 4 preliminary constitutional questions to estimate your Greco-Arab temperament and primary organ affinities.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Question 1: Thermal Tendency */}
            <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
              <span className="text-[10px] font-bold text-teal-400 uppercase">1. Thermal Sensitivity</span>
              <p className="text-xs font-semibold text-white">How does your body react to climate?</p>
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, temp: "hot" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.temp === "hot" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  🔥 Feel Warm
                </button>
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, temp: "cold" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.temp === "cold" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  ❄️ Feel Cold
                </button>
              </div>
            </div>

            {/* Question 2: Moisture Tendency */}
            <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
              <span className="text-[10px] font-bold text-teal-400 uppercase">2. Skin & Moisture</span>
              <p className="text-xs font-semibold text-white">What is your natural skin quality?</p>
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, moisture: "moist" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.moisture === "moist" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  💧 Soft & Moist
                </button>
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, moisture: "dry" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.moisture === "dry" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  🍂 Rough & Dry
                </button>
              </div>
            </div>

            {/* Question 3: Body Frame */}
            <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
              <span className="text-[10px] font-bold text-teal-400 uppercase">3. Physique & Build</span>
              <p className="text-xs font-semibold text-white">What is your natural skeletal build?</p>
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, physique: "broad" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.physique === "broad" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  🛡️ Broad / Heavy
                </button>
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, physique: "slender" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.physique === "slender" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  ⚡ Lean / Slender
                </button>
              </div>
            </div>

            {/* Question 4: Sleep Tendency */}
            <div className="p-4 rounded-xl bg-[#1E293B] border border-[#334155] space-y-2">
              <span className="text-[10px] font-bold text-teal-400 uppercase">4. Sleep Architecture</span>
              <p className="text-xs font-semibold text-white">How do you typically sleep?</p>
              <div className="grid grid-cols-2 gap-2 pt-1">
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, sleep: "deep" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.sleep === "deep" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  😴 Deep & Heavy
                </button>
                <button
                  type="button"
                  onClick={() => setMizajAnswers({ ...mizajAnswers, sleep: "light" })}
                  className={`p-2 rounded-lg text-xs font-semibold border ${
                    mizajAnswers.sleep === "light" ? "bg-[#0D9488] text-white border-transparent" : "bg-[#0F172A] text-[#94A3B8] border-[#334155]"
                  }`}
                >
                  🌙 Light & Alert
                </button>
              </div>
            </div>
          </div>

          {/* Assessment Result Box */}
          <div className="p-5 rounded-2xl bg-[#1E293B] border border-[#2DD4BF]/40 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="space-y-1 text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start gap-2">
                <span className="text-xs text-[#94A3B8]">Preliminary Mizaj Estimate:</span>
                <span className="text-base font-bold text-white">{calculatedMizaj.name}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">{calculatedMizaj.trait}</span>
              </div>
              <p className="text-xs text-[#94A3B8]">
                Organ Affinity: <strong className="text-teal-300">{calculatedMizaj.affinity}</strong>. Complete formal diagnosis requires in-person Nabz (pulse) and Lisan spectral examination.
              </p>
            </div>
            <Link
              href="/website/book"
              className="px-6 py-2.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold whitespace-nowrap shadow-lg"
            >
              Book Full 10-Ajnas Clinical Exam →
            </Link>
          </div>
        </div>
      </section>

      {/* 6 Specialized Clinical Care Areas */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Comprehensive Care</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">Specialized Clinical Care Areas</h2>
          <p className="text-xs md:text-sm text-[#94A3B8] max-w-xl mx-auto">
            Rigorous integrative protocols targeting root humoral dyscrasias across major metabolic, musculoskeletal, and organ-axis disorders.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {careAreas.map((area) => (
            <div key={area.id} className="p-6 rounded-2xl bg-[#0F172A] border border-[#334155] hover:border-[#0D9488]/60 transition space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-3xl">{area.icon}</span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-[#1E293B] text-[#2DD4BF] font-mono font-bold">
                    PROTOCOL READY
                  </span>
                </div>
                <h3 className="text-base font-bold text-white">{area.name}</h3>
                <p className="text-xs text-[#94A3B8] leading-relaxed">{area.desc}</p>
                <div className="p-3 rounded-lg bg-[#1E293B] border border-[#334155]/60 text-[11px] text-teal-300">
                  <span className="block text-[10px] text-[#94A3B8] font-bold uppercase">Standard Regimen</span>
                  {area.regimen}
                </div>
              </div>
              <div className="pt-2 border-t border-[#1E293B] flex items-center justify-between">
                <Link href="/website/conditions" className="text-xs font-bold text-[#2DD4BF] hover:text-white">
                  Clinical Details →
                </Link>
                <Link href="/website/book" className="text-xs font-semibold text-[#94A3B8] hover:text-white">
                  Consult Specialist
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Complete 10 Botanical Formulations Portfolio */}
      <section className="max-w-7xl mx-auto px-6 space-y-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-[#334155] pb-4">
          <div>
            <span className="text-xs font-bold text-[#2DD4BF] tracking-wider uppercase">Codified Botanical Therapeutics</span>
            <h2 className="text-2xl md:text-3xl font-bold text-white">ZAYVORA Herbals Portfolio</h2>
            <p className="text-xs text-[#94A3B8] mt-1">
              GMP manufactured, HPLC verified, Schedule E(1) Mudabbar purified classical & proprietary compounds.
            </p>
          </div>
          <Link href="/website/herbals" className="px-4 py-2 rounded-xl border border-[#334155] text-xs font-bold text-[#2DD4BF] hover:text-white hover:bg-[#1E293B] transition">
            View All 10 Formulations Store →
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {allProducts.map((p) => (
            <div key={p.id} className="p-4 rounded-2xl bg-[#1E293B] border border-[#334155] space-y-3 flex flex-col justify-between hover:border-teal-500/50 transition">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] px-2 py-0.5 rounded font-mono font-semibold bg-[#0D9488]/20 text-[#2DD4BF]">
                    {p.category}
                  </span>
                  <span className="text-sm font-bold text-white">{p.price}</span>
                </div>
                <h4 className="text-sm font-bold text-white leading-snug">{p.name}</h4>
                <p className="text-[11px] text-[#94A3B8] line-clamp-2 leading-relaxed">{p.desc}</p>
                <div className="text-[10px] font-mono text-[#64748B] pt-1">
                  {p.monograph}
                </div>
              </div>
              
              <div className="pt-3 border-t border-[#334155] flex items-center justify-between gap-2">
                <Link
                  href={`/website/product?id=${p.id}`}
                  className="text-[11px] font-semibold text-[#94A3B8] hover:text-white"
                >
                  Monograph
                </Link>
                <Link
                  href={`/website/cart?add=${p.id}`}
                  className="px-3 py-1.5 rounded-lg bg-[#0D9488] hover:bg-[#14B8A6] text-white text-xs font-bold transition shadow"
                >
                  + Add to Cart
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Statutory Safety & 21 CFR Part 11 Banner */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="p-6 rounded-2xl bg-[#0F172A] border border-amber-500/30 space-y-3">
          <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
            <span>🛡️</span>
            <span>Non-Delegable Clinician Discretion Barrier (21 CFR Part 11)</span>
          </div>
          <p className="text-xs text-[#94A3B8] leading-relaxed">
            ZAYVORA Health OS strictly enforces that AI assistants and algorithmic engines function strictly as assistive decision support. Prescriptions remain in non-dispensable draft status (<code className="text-amber-300">safe_to_lock = False</code>) until a licensed Senior Tabeeb completes independent clinical review and applies a 21 CFR Part 11 cryptographic digital signature.
          </p>
        </div>
      </section>

      {/* Appointment Booking Call-To-Action */}
      <section className="max-w-7xl mx-auto px-6">
        <div className="p-8 md:p-12 rounded-3xl bg-gradient-to-r from-[#0D9488]/25 via-[#1E293B] to-[#0F172A] border border-[#0D9488]/40 flex flex-col md:flex-row justify-between items-center gap-6 shadow-2xl">
          <div className="space-y-2">
            <h3 className="text-2xl md:text-3xl font-bold text-white">Experience Modern Evidence-Based Unani Care</h3>
            <p className="text-xs md:text-sm text-[#94A3B8] max-w-xl">
              Consult with senior licensed practitioners, receive objective 10-Ajnas Mizaj profiling, and benefit from organ-axis therapeutic formulations and supervised Ilaj bil-Tadbeer regimens.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link href="/website/book" className="px-8 py-3.5 rounded-xl bg-[#0D9488] hover:bg-[#14B8A6] text-white font-bold text-sm shadow-xl whitespace-nowrap transition text-center">
              Schedule Appointment Now
            </Link>
            <Link href="/website/cart" className="px-6 py-3.5 rounded-xl border border-[#334155] hover:bg-[#1E293B] text-white font-semibold text-sm transition text-center">
              View Cart / Checkout
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
}
