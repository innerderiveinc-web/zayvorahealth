"use client";

import React, { useState } from "react";
import Link from "next/link";

interface Stage {
  stage_number: number;
  stage_name: string;
  clinical_question: string;
  options: string[];
  correct_option_index: number;
  classical_citation: string;
  biomedical_rationale: string;
}

interface CaseStudy {
  id: string;
  case_code: string;
  title_en: string;
  title_ur: string;
  category: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  patient_name: string;
  age: number;
  gender: string;
  occupation: string;
  chief_complaint: string;
  vitals: Record<string, string>;
  baseline_labs: Record<string, string>;
  stages: Stage[];
}

const SIMULATOR_CASES: CaseStudy[] = [
  {
    id: "sim-case-01",
    case_code: "SIM-MET-01",
    title_en: "Type 2 Diabetes Mellitus with Barid-Balghami Su-e-Mizaj",
    title_ur: "ذیابیطس شکری نوع دوم — سوء مزاج بارد بلغمى اور میٹابولک انحطاط",
    category: "Metabolic & Endocrine",
    difficulty: "Intermediate",
    patient_name: "Zafar Iqbal",
    age: 52,
    gender: "Male",
    occupation: "Bank Auditor (Sedentary)",
    chief_complaint: "Polyuria, postprandial stupor, heavy lethargy, and bilateral lower extremity tingling for 6 months.",
    vitals: {
      "Blood Pressure": "138/88 mmHg",
      "Pulse (Nabz)": "62 bpm (Nabz-e-Batee, Layyin)",
      "Core Temp": "36.2 °C (Sub-basal)",
      "BMI": "29.4 kg/m²"
    },
    baseline_labs: {
      "Fasting Glucose": "174 mg/dL",
      "HbA1c": "8.6%",
      "Fasting Insulin": "22.4 microIU/mL (HOMA-IR: 9.6)",
      "Lipid Profile": "Triglycerides: 240 mg/dL, HDL: 36 mg/dL",
      "Urine Routine": "Glycosuria 2+, No albuminuria"
    },
    stages: [
      {
        stage_number: 1,
        stage_name: "Stage 1: Constitutional Mizaj & Humoral Diagnosis",
        clinical_question: "Based on the presentation (sub-basal temperature, postprandial lethargy, soft pulse, and severe insulin resistance), what is the primary Unani diagnostic assessment?",
        options: [
          "Su-e-Mizaj Har-Yabis with excessive combustion of Safra",
          "Su-e-Mizaj Barid-Ratab (Balghami) with deficient innate metabolic fire (Hararat-e-Ghariziyyah)",
          "Pure Damawi plethora with secondary vascular engorgement",
          "Su-e-Mizaj Saudawi caused by acute splenic inflammation"
        ],
        correct_option_index: 1,
        classical_citation: "Ibn Sina, Al-Qanoon fit-Tibb, Book 3, Fen 19: 'Ziabates occurs primarily when the retentive faculty of the kidneys and metabolic transformation of the liver are impaired by coldness (Barudat) leading to rapid transit without concoction.'",
        biomedical_rationale: "Excess cold-moist dyscrasia correlates with profound downregulation of mitochondrial AMPK phosphorylation and GLUT4 glucose transporter translocation, manifesting as severe cellular insulin resistance."
      },
      {
        stage_number: 2,
        stage_name: "Stage 2: Bedside Semiology (Pulse & Urine)",
        clinical_question: "Which specific 10-Ajnas pulse waveform and Qaroorah characteristics confirm this Barid-Balghami metabolic state?",
        options: [
          "Nabz-e-Saree, Azeem, Sulb with fiery concentrated amber urine",
          "Nabz-e-Batee, Saghir, Layyin (Slow, Small, Soft) with pale, voluminous, low-viscosity Qaroorah and white sediment",
          "Nabz-e-Ghazali (Dicrotic, Bounding) with smoky urine",
          "Nabz-e-Munqati with saffron foam"
        ],
        correct_option_index: 1,
        classical_citation: "Ali ibn al-Abbas al-Majusi, Kamil al-Sina'a al-Tibbiyya, Discourse 2: 'The pulse of Barudat and Balgham is uniformly Batee (slow), Layyin (soft), and Saghir (small).'",
        biomedical_rationale: "Soft and slow pulse reflects diminished sympathetic vascular tone, while pale copious urine denotes renal excretion of un-metabolized solutes without bile concoction."
      },
      {
        stage_number: 3,
        stage_name: "Stage 3: Phased Integrative Therapeutic Plan",
        clinical_question: "What is the most appropriate first-line therapeutic regimen for Phase 1 metabolic harmonization?",
        options: [
          "High-dose cold purgatives with iced tamarind sherbet",
          "Thermogenic posology: Jamun seed + Karela powder with Qurs-e-Ziabates and warm cinnamon infusion, accompanied by 16-hour intermittent fasting (Faqah)",
          "Heavy meat stews (Yakhni) and complete bed rest",
          "Immediate wet cupping (Hijama) over the splenic zone"
        ],
        correct_option_index: 1,
        classical_citation: "Hakim Kabiruddin, Bayaz-e-Kabir, Vol. II: 'Ziabates with cold phlegmatic signs mandates Muharrik-e-Hararat botanicals (Jamun, Karela, Darchini) to awaken innate digestive heat.'",
        biomedical_rationale: "Cinnamon and bitter charantin upregulate AMPK signaling and enhance peripheral insulin sensitivity, while intermittent fasting induces hepatic autophagy."
      },
      {
        stage_number: 4,
        stage_name: "Stage 4: Statutory Pharmacovigilance & Safety Barrier",
        clinical_question: "If introducing calcined Kushta or mineral adjuvants into this diabetic regimen, what clinical governance standard must be verified?",
        options: [
          "No verification needed if prescribed by a local traditional healer",
          "Mandatory 21 CFR Part 11 SHA-256 HMAC digital signature, heavy-metal safety screening, and renal function (eGFR) monitoring",
          "Immediate co-administration with high-dose corticosteroids",
          "Dispensing un-pulverized raw ingredients directly to the patient"
        ],
        correct_option_index: 1,
        classical_citation: "ZAYVORA Clinical Governance Framework, Rule 12-E: 'All calcined organo-metallic Kushtajat require verified Certificate of Analysis (COA) and clinician digital seal.'",
        biomedical_rationale: "Ensures complete bioavailability without nephrotoxic or heavy-metal residues, strictly protecting baseline renal filtration."
      }
    ]
  },
  {
    id: "sim-case-02",
    case_code: "SIM-RHEUM-02",
    title_en: "Rheumatoid Arthritis (Waja-ul-Mafasil) with Saudawi-Balghami Stagnation",
    title_ur: "وجع المفاصل بلغمی و سوداوی — سوزشِ مفاصل اور مدافعتی بگاڑ",
    category: "Musculoskeletal & Immunology",
    difficulty: "Advanced",
    patient_name: "Shabana Begum",
    age: 46,
    gender: "Female",
    occupation: "School Teacher",
    chief_complaint: "Severe bilateral symmetrical swelling and early morning stiffness (>90 min) in PIP and MCP joints for 8 months.",
    vitals: {
      "Blood Pressure": "126/80 mmHg",
      "Pulse (Nabz)": "78 bpm (Nabz-e-Sulb)",
      "Core Temp": "37.0 °C",
      "BMI": "24.1 kg/m²"
    },
    baseline_labs: {
      "RF Titre": "94 IU/mL (Strongly Positive)",
      "Anti-CCP": "128 U/mL (Strongly Positive)",
      "hs-CRP": "18.4 mg/L (Markedly Elevated)",
      "ESR": "54 mm/1st hr",
      "Serum Uric Acid": "5.2 mg/dL (Normal)"
    },
    stages: [
      {
        stage_number: 1,
        stage_name: "Stage 1: Humoral Etiology & Diagnostic Synthesis",
        clinical_question: "What is the classical Unani humoral classification of chronic autoimmune articular erosions with morning stiffness?",
        options: [
          "Waja-ul-Mafasil Balghami-Saudawi with accumulation of viscid morbid humors (Akhlat-e-Raddiyya) in joint cavities",
          "Acute Safrawi arthritis caused by excessive citrus consumption",
          "Isolated trauma-induced mechanical synoviopathy",
          "Spontaneous idiopathic neurosis"
        ],
        correct_option_index: 0,
        classical_citation: "Al-Razi, Kitab al-Hawi fit-Tibb, Vol. 11: 'When the joints receive cold, thick humors that the natural faculty fails to resolve, they stagnate and solidify into intractable pain and deformity.'",
        biomedical_rationale: "Corresponds to chronic immune-complex mediated synovial hyperplasia, pannus formation, and systemic pro-inflammatory cytokine elevation (TNF-alpha, IL-6, IL-1beta)."
      },
      {
        stage_number: 2,
        stage_name: "Stage 2: Bedside Tactile Diagnostics & Tongue Signs",
        clinical_question: "Which tactile joint finding and tongue sign are pathognomonic of Waja-ul-Mafasil with Saudawi-Balghami stagnation?",
        options: [
          "Scalding hot erythema with thin bright yellow tongue coat",
          "Boggy, non-pitting synovial swelling with periarticular coolness and a thick dull white-grey tongue coat with lateral dental indentations",
          "Dry scaly petechiae with normal clean pink tongue",
          "Flaccid muscle paresis with completely smooth red tongue"
        ],
        correct_option_index: 1,
        classical_citation: "Ibn Sina, Al-Qanoon fit-Tibb, Book 3, Fen 22: 'Cold phlegmatic joint swellings are soft, pale or dusky, lacking acute redness, worsening with cold contact.'",
        biomedical_rationale: "Boggy coolness reflects chronic proliferative synovitis with stagnant lymphatic drainage, while tongue indentations indicate systemic fluid retention and tissue hypoperfusion."
      },
      {
        stage_number: 3,
        stage_name: "Stage 3: Phased Prescribing & Compound Formulation",
        clinical_question: "What is the classical drug of choice in Unani pharmacopoeia for resolving joint pain and its mandatory Musleh (corrective)?",
        options: [
          "Afeem (Opium) alone in large doses without any corrector",
          "Suranjan Shireen (Colchicum autumnale) paired with Katira / Samagh-e-Arabi and Zanjabeel as Musleh",
          "Excessive ingestion of vinegar and cold curds",
          "Continuous dry cold compresses over affected joints"
        ],
        correct_option_index: 1,
        classical_citation: "Hakim Najmul Ghani, Khazain-ul-Advia, Vol. 3: 'Suranjan is the sovereign antidote for joints (Dawa-e-Mafasil); its corrector is Katira and Zanjabeel to prevent gastrointestinal griping and mucosal irritation.'",
        biomedical_rationale: "Suranjan provides bioactive colchicine, which inhibits tubulin polymerization, arrests neutrophil chemotaxis into the synovium, and suppresses the NLRP3 inflammasome."
      },
      {
        stage_number: 4,
        stage_name: "Stage 4: Schedule E(1) Statutory Mudabbar Gate",
        clinical_question: "Suranjan Talkh (Bitter Colchicum) is classified under Schedule E(1) as a statutory poison. What mandatory detoxification SOP is legally and clinically required before dispensing?",
        options: [
          "No SOP needed; raw roots can be powdered directly",
          "Mandatory Mudabbar process: Soaking and boiling in pure cow's milk (Sheer-e-Gao) for 12 hours followed by desiccation and shade-drying",
          "Washing with alcohol and immediate flame roasting",
          "Mixing with high-dose synthetic NSAIDs without declaration"
        ],
        correct_option_index: 1,
        classical_citation: "NFUM Part-II & Drugs and Cosmetics Rules 1945, Schedule E(1): 'Suranjan Talkh must undergo Shodhana/Tadbeer in cow's milk to eliminate lethal toxic alkaloids while preserving therapeutic colchicosides.'",
        biomedical_rationale: "Milk lipids and casein bind toxic colchicine degradants, mitigating cardiotoxicity and severe hemorrhagic gastroenteritis while maintaining anti-inflammatory efficacy."
      }
    ]
  }
];

export default function SimulatorPage() {
  const [selectedCase, setSelectedCase] = useState<CaseStudy | null>(null);
  const [userAnswers, setUserAnswers] = useState<Record<number, number>>({});
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const handleSelectOption = (stageNumber: number, optionIndex: number) => {
    if (isSubmitted) return;
    setUserAnswers((prev) => ({ ...prev, [stageNumber]: optionIndex }));
  };

  const handleStartCase = (cs: CaseStudy) => {
    setSelectedCase(cs);
    setUserAnswers({});
    setIsSubmitted(false);
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  const calculateScore = () => {
    if (!selectedCase) return { score: 0, percentage: 0 };
    let correct = 0;
    selectedCase.stages.forEach((st) => {
      if (userAnswers[st.stage_number] === st.correct_option_index) {
        correct++;
      }
    });
    return {
      score: correct,
      total: selectedCase.stages.length,
      percentage: Math.round((correct / selectedCase.stages.length) * 100)
    };
  };

  const scoreResult = isSubmitted ? calculateScore() : null;

  return (
    <div className="min-h-screen bg-[#FAFAF7] text-[#1A1A1A] font-sans pb-20">
      {/* Header Banner */}
      <header className="bg-[#1B4332] text-white py-12 px-6 shadow-md">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full text-xs font-semibold tracking-wide text-[#F4A261] mb-3">
                <span>🎓 CLINICAL TRAINING & COMPETENCY ACADEMY</span>
              </div>
              <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
                ZAYVORA Clinical Case Study Simulator™
              </h1>
              <p className="text-sm md:text-base text-gray-200 mt-2 max-w-2xl">
                Master classical semiology, temperamental dyscrasia diagnosis, and evidence-grounded therapeutic formulating through authenticated real-world clinical cases.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link
                href="/library"
                className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm font-medium transition"
              >
                📖 12-Volume Library
              </Link>
              <Link
                href="/doctor"
                className="px-4 py-2 bg-[#2D6A4F] hover:bg-[#24543E] text-white rounded-lg text-sm font-medium shadow transition"
              >
                🩺 Doctor Consultation Desk
              </Link>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 mt-8">
        {!selectedCase ? (
          <div>
            <div className="mb-6 flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-[#1B4332]">Select an Interactive Clinical Case</h2>
                <p className="text-xs text-gray-500">Each case challenge evaluates diagnostic semiology, posology, and statutory safety governance.</p>
              </div>
              <span className="text-xs bg-[#2D6A4F]/10 text-[#2D6A4F] font-bold px-3 py-1 rounded-full">
                {SIMULATOR_CASES.length} Active Challenges
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {SIMULATOR_CASES.map((cs) => (
                <div
                  key={cs.id}
                  className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span className="text-xs font-bold text-gray-500">{cs.case_code}</span>
                      <span
                        className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                          cs.difficulty === "Beginner"
                            ? "bg-green-100 text-green-800"
                            : cs.difficulty === "Intermediate"
                            ? "bg-blue-100 text-blue-800"
                            : "bg-amber-100 text-amber-800"
                        }`}
                      >
                        {cs.difficulty}
                      </span>
                    </div>

                    <h3 className="text-lg font-bold text-[#1B4332] mb-1">{cs.title_en}</h3>
                    <p className="text-sm font-serif text-[#2D6A4F] mb-3 text-right" dir="rtl">{cs.title_ur}</p>

                    <div className="bg-[#FAFAF7] rounded-xl p-3 text-xs text-gray-700 mb-4 border border-gray-100">
                      <p className="font-semibold text-gray-900 mb-1">
                        Patient: {cs.patient_name}, {cs.age}y ({cs.gender}) — {cs.occupation}
                      </p>
                      <p className="italic">"{cs.chief_complaint}"</p>
                    </div>

                    <div className="flex flex-wrap gap-2 text-xs text-gray-600 mb-4">
                      <span className="bg-gray-100 px-2.5 py-1 rounded-md">Category: {cs.category}</span>
                      <span className="bg-gray-100 px-2.5 py-1 rounded-md">{cs.stages.length} Diagnostic Stages</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleStartCase(cs)}
                    className="w-full py-2.5 bg-[#2D6A4F] hover:bg-[#1B4332] text-white font-semibold rounded-xl text-sm transition shadow-sm"
                  >
                    Start Clinical Challenge →
                  </button>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div>
            {/* Active Case Top Navigation */}
            <div className="flex items-center justify-between mb-6">
              <button
                onClick={() => setSelectedCase(null)}
                className="text-sm font-medium text-gray-600 hover:text-[#1B4332] flex items-center gap-1"
              >
                ← Back to Case Catalog
              </button>
              <div className="flex items-center gap-2">
                <span className="text-xs bg-gray-200 text-gray-800 px-2.5 py-1 rounded-md font-bold">
                  {selectedCase.case_code}
                </span>
                <span className="text-xs bg-[#2D6A4F]/10 text-[#2D6A4F] px-2.5 py-1 rounded-md font-bold">
                  {selectedCase.category}
                </span>
              </div>
            </div>

            {/* Patient Presentation Card */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm mb-8">
              <div className="flex flex-wrap justify-between items-start gap-4 mb-4 pb-4 border-b border-gray-100">
                <div>
                  <h2 className="text-2xl font-bold text-[#1B4332]">{selectedCase.title_en}</h2>
                  <p className="text-sm font-serif text-[#2D6A4F] mt-1" dir="rtl">{selectedCase.title_ur}</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-400 block">PATIENT FILE</span>
                  <span className="text-sm font-bold text-gray-800">
                    {selectedCase.patient_name} ({selectedCase.age}y / {selectedCase.gender})
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Chief Complaint</h4>
                  <p className="text-xs text-gray-800 bg-[#FAFAF7] p-3 rounded-xl border border-gray-100 leading-relaxed">
                    {selectedCase.chief_complaint}
                  </p>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Baseline Bedside Vitals</h4>
                  <div className="bg-[#FAFAF7] p-3 rounded-xl border border-gray-100 space-y-1.5">
                    {Object.entries(selectedCase.vitals).map(([k, v]) => (
                      <div key={k} className="flex justify-between text-xs">
                        <span className="text-gray-500">{k}:</span>
                        <span className="font-semibold text-gray-800">{v}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Clinical Laboratory Workup</h4>
                  <div className="bg-[#FAFAF7] p-3 rounded-xl border border-gray-100 space-y-1.5">
                    {Object.entries(selectedCase.baseline_labs).map(([k, v]) => (
                      <div key={k} className="flex justify-between text-xs">
                        <span className="text-gray-500">{k}:</span>
                        <span className="font-semibold text-gray-800 text-right">{v}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Simulation Stages */}
            <div className="space-y-6">
              {selectedCase.stages.map((st) => {
                const selectedOption = userAnswers[st.stage_number];
                const isCorrect = isSubmitted && selectedOption === st.correct_option_index;
                const isWrong = isSubmitted && selectedOption !== undefined && selectedOption !== st.correct_option_index;

                return (
                  <div
                    key={st.stage_number}
                    className={`bg-white rounded-2xl border p-6 shadow-sm transition ${
                      isSubmitted
                        ? isCorrect
                          ? "border-green-300 bg-green-50/20"
                          : "border-red-300 bg-red-50/20"
                        : "border-gray-200"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold text-[#2D6A4F] bg-[#2D6A4F]/10 px-3 py-1 rounded-full">
                        {st.stage_name}
                      </span>
                      {isSubmitted && (
                        <span
                          className={`text-xs font-bold px-3 py-1 rounded-full ${
                            isCorrect ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                          }`}
                        >
                          {isCorrect ? "✓ Correct Decision" : "✗ Clinical Error"}
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-gray-900 mb-4">{st.clinical_question}</h3>

                    <div className="space-y-2.5">
                      {st.options.map((opt, idx) => {
                        const isChosen = selectedOption === idx;
                        const isActualCorrect = isSubmitted && idx === st.correct_option_index;

                        let optionStyle = "border-gray-200 hover:border-[#2D6A4F] hover:bg-gray-50 text-gray-800";
                        if (isSubmitted) {
                          if (isActualCorrect) {
                            optionStyle = "border-green-500 bg-green-100/50 text-green-900 font-semibold";
                          } else if (isChosen && !isActualCorrect) {
                            optionStyle = "border-red-500 bg-red-100/50 text-red-900 line-through";
                          } else {
                            optionStyle = "border-gray-100 text-gray-400 opacity-60";
                          }
                        } else if (isChosen) {
                          optionStyle = "border-[#2D6A4F] bg-[#2D6A4F]/10 text-[#1B4332] font-semibold";
                        }

                        return (
                          <label
                            key={idx}
                            className={`flex items-start gap-3 p-3.5 rounded-xl border text-sm cursor-pointer transition ${optionStyle}`}
                          >
                            <input
                              type="radio"
                              name={`stage-${st.stage_number}`}
                              checked={isChosen}
                              disabled={isSubmitted}
                              onChange={() => handleSelectOption(st.stage_number, idx)}
                              className="mt-1 accent-[#2D6A4F]"
                            />
                            <span className="flex-1 leading-snug">{opt}</span>
                          </label>
                        );
                      })}
                    </div>

                    {/* Explanations shown after submission */}
                    {isSubmitted && (
                      <div className="mt-5 pt-4 border-t border-gray-100 space-y-3">
                        <div className="bg-[#FAFAF7] rounded-xl p-3 text-xs border border-gray-200">
                          <span className="font-bold text-[#1B4332] block mb-1">📖 Classical Authority & Citation:</span>
                          <p className="italic text-gray-700">{st.classical_citation}</p>
                        </div>
                        <div className="bg-blue-50/50 rounded-xl p-3 text-xs border border-blue-100">
                          <span className="font-bold text-blue-900 block mb-1">🧬 Molecular & Pathophysiological Correlation:</span>
                          <p className="text-blue-800">{st.biomedical_rationale}</p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* Submission / Score Footer */}
            <div className="mt-8 bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
              {!isSubmitted ? (
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div>
                    <span className="text-sm font-bold text-gray-800 block">
                      Progress: {Object.keys(userAnswers).length} of {selectedCase.stages.length} Decisions Selected
                    </span>
                    <span className="text-xs text-gray-500">
                      Submit when all decision stages are selected to receive your competency assessment.
                    </span>
                  </div>
                  <button
                    onClick={handleSubmit}
                    disabled={Object.keys(userAnswers).length < selectedCase.stages.length}
                    className={`px-8 py-3 rounded-xl font-bold text-sm shadow transition ${
                      Object.keys(userAnswers).length === selectedCase.stages.length
                        ? "bg-[#2D6A4F] hover:bg-[#1B4332] text-white"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed"
                    }`}
                  >
                    Submit Clinical Evaluation →
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-gray-100">
                    <div>
                      <h3 className="text-xl font-bold text-[#1B4332]">Evaluation Summary & Clinical Grading</h3>
                      <p className="text-xs text-gray-500">Peer-reviewed against 12-Volume Grand Library Standards</p>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <span className="text-xs text-gray-400 block">SCORE</span>
                        <span className="text-2xl font-black text-[#2D6A4F]">{scoreResult?.percentage}%</span>
                      </div>
                      <div className="h-10 w-px bg-gray-200" />
                      <div className="text-right">
                        <span className="text-xs text-gray-400 block">RESULT</span>
                        <span className="text-sm font-bold text-gray-800">
                          {scoreResult?.score} / {scoreResult?.total} Correct
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
                    <span
                      className={`text-sm font-bold px-4 py-2 rounded-xl ${
                        (scoreResult?.percentage || 0) >= 80
                          ? "bg-green-100 text-green-800"
                          : (scoreResult?.percentage || 0) >= 60
                          ? "bg-blue-100 text-blue-800"
                          : "bg-amber-100 text-amber-800"
                      }`}
                    >
                      Competency Rank:{" "}
                      {(scoreResult?.percentage || 0) >= 80
                        ? "Master Integrative Physician (Tabeeb-e-Haziq)"
                        : (scoreResult?.percentage || 0) >= 60
                        ? "Senior Clinical Resident (Tabeeb-e-Mahir)"
                        : "Junior Practitioner — Remedial Review Recommended"}
                    </span>

                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => handleStartCase(selectedCase)}
                        className="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-xl text-xs font-semibold transition"
                      >
                        🔄 Retake Challenge
                      </button>
                      <button
                        onClick={() => setSelectedCase(null)}
                        className="px-5 py-2 bg-[#2D6A4F] hover:bg-[#1B4332] text-white rounded-xl text-xs font-semibold transition shadow-sm"
                      >
                        Next Case Challenge →
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
