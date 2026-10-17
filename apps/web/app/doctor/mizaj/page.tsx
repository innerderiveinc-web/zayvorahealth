"use client";

import React, { useState, useEffect } from "react";
import { AppShell } from "@/components/AppShell";
import Link from "next/link";

interface DomainQuestion {
  id: string;
  text: string;
  options: {
    damawi: string;
    safrawi: string;
    balghami: string;
    sawdawi: string;
  };
}

interface Domain {
  title: string;
  weight: number;
  questions: DomainQuestion[];
}

interface ZMAIResult {
  total_questions_scored: number;
  counts: Record<string, number>;
  percentages: Record<string, number>;
  dominant_mizaj: string;
  secondary_mizaj: string;
  mizaj_formula: string;
  dyscrasia?: string | null;
  clinical_guidance?: {
    primary_organ_axis_vulnerability?: string;
    dietary_thermal_direction?: string;
  };
}

const SAMPLE_DOMAINS: Record<string, Domain> = {
  morphology: {
    title: "Domain 1: Morphology & Somatotype",
    weight: 5,
    questions: [
      {
        id: "q1_build",
        text: "Body build and skeletal frame:",
        options: {
          damawi: "Muscular, broad, symmetrical, robust frame",
          safrawi: "Lean, sinewy, angular, prominent tendons",
          balghami: "Heavy, soft, adipose, rounded frame",
          sawdawi: "Thin, bony, delicate, narrow chest"
        }
      },
      {
        id: "q2_complexion",
        text: "Facial complexion and skin undertone:",
        options: {
          damawi: "Ruddy, pinkish-red, flushed, vibrant",
          safrawi: "Yellowish, sallow, warm olive, flushed in heat",
          balghami: "Pale, chalky white, cool, clear",
          sawdawi: "Dusky, dark, hyper-pigmented, dull, dry"
        }
      },
      {
        id: "q3_skin_feel",
        text: "Skin texture and tactile warmth:",
        options: {
          damawi: "Warm and moist, supple, well-perfused",
          safrawi: "Hot and dry, thin, prone to flushing",
          balghami: "Cool and moist, soft, smooth, damp",
          sawdawi: "Cold and dry, rough, coarse, scaling"
        }
      },
      {
        id: "q4_hair",
        text: "Hair thickness, color and density:",
        options: {
          damawi: "Thick, dark, lustrous, wavy, rapid growth",
          safrawi: "Fine, reddish or blonde-brown, early thinning/balding",
          balghami: "Thick, straight, oily, slow to grey",
          sawdawi: "Dry, coarse, frizzy, brittle, split ends"
        }
      },
      {
        id: "q5_joints",
        text: "Joints and skeletal structure:",
        options: {
          damawi: "Firm, well-covered with muscle, stable",
          safrawi: "Prominent, visible veins and tendons",
          balghami: "Large, fleshy, well-padded, lax ligaments",
          sawdawi: "Bony, crackling sounds on motion, prominent joints"
        }
      }
    ]
  },
  digestion: {
    title: "Domain 2: Digestion & Appetite (Hazm wa Ishtiha)",
    weight: 5,
    questions: [
      {
        id: "q6_appetite",
        text: "Natural appetite intensity:",
        options: {
          damawi: "Strong, regular, enjoys hearty meals",
          safrawi: "Voracious, intense, irritable if meals delayed",
          balghami: "Weak, slow to develop, skips meals easily",
          sawdawi: "Erratic, false hunger, variable appetite"
        }
      },
      {
        id: "q7_thirst",
        text: "Thirst sensation and water intake:",
        options: {
          damawi: "Normal to moderate, satisfied with cool water",
          safrawi: "Intense, frequent craving for ice-cold beverages",
          balghami: "Low thirst, rarely feels thirsty, dislikes cold water",
          sawdawi: "Dry mouth with minimal thirst desire"
        }
      },
      {
        id: "q8_digestion_speed",
        text: "Speed and ease of digestion:",
        options: {
          damawi: "Rapid, robust, comfortable digestion",
          safrawi: "Very rapid, hyperacidic, heartburn tendency",
          balghami: "Sluggish, takes hours, heavy post-meal fatigue",
          sawdawi: "Slow, gaseous, bloating, irregular fermentation"
        }
      },
      {
        id: "q9_cravings",
        text: "Preferred tastes and food cravings:",
        options: {
          damawi: "Cooling, refreshing, sour, citrus, salads",
          safrawi: "Cold, sweet, soothing milk/desserts, bitter foods",
          balghami: "Hot, pungent, spicy, ginger, black pepper",
          sawdawi: "Warm, rich, moist, sweet, comfort foods"
        }
      },
      {
        id: "q10_postmeal",
        text: "Physical sensation after a full meal:",
        options: {
          damawi: "Pleasantly energized and contented",
          safrawi: "Internal heat, epigastric acidity or burning",
          balghami: "Severe heaviness, brain fog, sleepiness",
          sawdawi: "Abdominal distension, gas, borborygmi, discomfort"
        }
      }
    ]
  },
  sleep: {
    title: "Domain 3: Sleep & Dream Patterns (Naum wa Ru'ya)",
    weight: 5,
    questions: [
      {
        id: "q11_sleep_depth",
        text: "Typical sleep duration and depth:",
        options: {
          damawi: "Moderate (7-8 hours), deep, highly restorative",
          safrawi: "Short (5-6 hours), light, easily awakened",
          balghami: "Excessive (>8-10 hours), very deep, hard to wake",
          sawdawi: "Fragmented (4-6 hours), tossing and turning, insomnia"
        }
      },
      {
        id: "q12_dream_themes",
        text: "Predominant dream imagery and themes:",
        options: {
          damawi: "Red colors, flowers, celebrations, joyful flying, blood",
          safrawi: "Fire, lightning, warfare, yellow hues, burning",
          balghami: "Water, swimming, rain, snow, white scenery, lakes",
          sawdawi: "Darkness, falling, being chased, anxiety, monsters, grief"
        }
      },
      {
        id: "q13_sleep_latency",
        text: "Ease of falling asleep at night:",
        options: {
          damawi: "Normal sleep onset within 15-20 minutes",
          safrawi: "Variable, restless before settling",
          balghami: "Falls asleep almost immediately upon lying down",
          sawdawi: "Prolonged sleep latency (>45 minutes), racing mind"
        }
      },
      {
        id: "q14_awakening",
        text: "Morning state upon awakening:",
        options: {
          damawi: "Refreshed, cheerful, ready for daily work",
          safrawi: "Alert immediately, dry throat, bitter mouth",
          balghami: "Lethargic, groggy, needs an hour to fully wake",
          sawdawi: "Fatigued, anxious about the day, unrefreshed"
        }
      },
      {
        id: "q15_daytime_naps",
        text: "Daytime sleepiness tendency:",
        options: {
          damawi: "Rare, occasional brief post-lunch power nap",
          safrawi: "None, high daytime adrenaline/arousal",
          balghami: "Strong habitual desire for prolonged afternoon nap",
          sawdawi: "Exhausted but unable to nap peacefully"
        }
      }
    ]
  },
  thermal: {
    title: "Domain 4: Thermal Response & Weather Adaptation",
    weight: 5,
    questions: [
      {
        id: "q16_cold_weather",
        text: "Response to cold environmental temperatures:",
        options: {
          damawi: "Comfortable in cold, enjoys crisp winter weather",
          safrawi: "Thrives in cold air, seeks cold rooms and shade",
          balghami: "Extremely uncomfortable, shivers, aches in cold",
          sawdawi: "Very sensitive to cold, joint stiffness, cold misery"
        }
      },
      {
        id: "q17_hot_weather",
        text: "Response to summer heat and humidity:",
        options: {
          damawi: "Dislikes oppressive humid heat, tolerates dry warmth",
          safrawi: "Suffers intensely in summer, prone to heat rashes/anger",
          balghami: "Loves hot sunny weather, feels energized in heat",
          sawdawi: "Prefers mild warmth, dislikes dry hot autumn winds"
        }
      },
      {
        id: "q18_sweating",
        text: "Perspiration quantity and odor:",
        options: {
          damawi: "Profuse, warm, neutral to sweetish odor",
          safrawi: "Abundant, hot, sharp or pungent odor",
          balghami: "Scanty, cool, clammy, odorless",
          sawdawi: "Minimal to dry, coarse skin with rarely any sweat"
        }
      },
      {
        id: "q19_worst_season",
        text: "Season with highest symptom exacerbation:",
        options: {
          damawi: "Spring (Rabi) - allergies, epistaxis, headaches",
          safrawi: "Summer (Saif) - irritability, acid reflux, skin eruptions",
          balghami: "Winter (Shita) - phlegm, lethargy, joint sluggishness",
          sawdawi: "Autumn (Kharif) - melancholy, dry skin, insomnia"
        }
      },
      {
        id: "q20_extremities",
        text: "Baseline temperature of hands and feet:",
        options: {
          damawi: "Consistently warm, pink, healthy circulation",
          safrawi: "Warm to hot, burning soles of feet at night",
          balghami: "Cold and damp, clammy palms",
          sawdawi: "Icy cold, dry, pale or bluish fingers in cold"
        }
      }
    ]
  },
  mental: {
    title: "Domain 5: Mental & Emotional Profile (Nafsiyat)",
    weight: 5,
    questions: [
      {
        id: "q21_temperament",
        text: "Dominant emotional predisposition:",
        options: {
          damawi: "Optimistic, cheerful, gregarious, generous",
          safrawi: "Intense, ambitious, competitive, quick-tempered",
          balghami: "Peaceful, placid, steady, slow to anger, forgiving",
          sawdawi: "Thoughtful, analytical, melancholic, perfectionist"
        }
      },
      {
        id: "q22_speech",
        text: "Natural speech cadence and voice tone:",
        options: {
          damawi: "Loud, resonant, fluent, animated, enthusiastic",
          safrawi: "Fast, decisive, sharp, articulate, commanding",
          balghami: "Soft, slow, measured, gentle, quiet",
          sawdawi: "Cautious, low volume, precise, detailed"
        }
      },
      {
        id: "q23_stress",
        text: "Response to acute psychological crisis or stress:",
        options: {
          damawi: "Faces it with confidence, can become overly dramatic",
          safrawi: "Confrontational, explosive outburst, then calms down",
          balghami: "Withdraws into quiet, avoids confrontation, patient",
          sawdawi: "Deep worry, chronic rumination, catastrophizing"
        }
      },
      {
        id: "q24_learning",
        text: "Learning style and memory retention:",
        options: {
          damawi: "Learns quickly, grasps the big picture, moderate recall",
          safrawi: "Sharp analytical intellect, fast grasp, selective memory",
          balghami: "Takes time to learn, but permanent lifelong retention",
          sawdawi: "Deep methodical study, retains details and grievances"
        }
      },
      {
        id: "q25_activity_tempo",
        text: "Pace of daily movement and execution:",
        options: {
          damawi: "Energetic, dynamic, fluid, social",
          safrawi: "Fast-paced, goal-driven, restless, hurried",
          balghami: "Steady, unhurried, prefers routine, calm",
          sawdawi: "Systematic, meticulous, cautious, stops to review"
        }
      }
    ]
  },
  elimination: {
    title: "Domain 6: Elimination & Secretions (Istifragh)",
    weight: 5,
    questions: [
      {
        id: "q26_bowels",
        text: "Typical bowel evacuation pattern:",
        options: {
          damawi: "Regular 1-2 times daily, well-formed, easy passage",
          safrawi: "Frequent (2-3 times), loose or soft, burning sensation",
          balghami: "Sluggish, pale, soft, occurs once daily or alternate days",
          sawdawi: "Dry, hard, pellet-like stools, chronic constipation"
        }
      },
      {
        id: "q27_urine",
        text: "Baseline urine color and urination sensation:",
        options: {
          damawi: "Straw-yellow, normal volume, painless",
          safrawi: "Dark amber or reddish-yellow, concentrated, warm feeling",
          balghami: "Pale, clear, copious, frequent volume",
          sawdawi: "Variable, cloudy or dusky, occasional sediment"
        }
      },
      {
        id: "q28_oral_state",
        text: "Morning oral taste and salivation:",
        options: {
          damawi: "Normal saliva, sweetish pleasant aftertaste",
          safrawi: "Dryness, bitter taste on the back of the tongue",
          balghami: "Excessive watery saliva, sweetish or tasteless mouth",
          sawdawi: "Dry mouth, sour or astringent taste on waking"
        }
      },
      {
        id: "q29_pulse",
        text: "Classical pulse characteristics (Nabz):",
        options: {
          damawi: "Full (Imtila), large, bounding, rhythmic",
          safrawi: "Rapid (Sari), tense, sharp stroke, frequent",
          balghami: "Slow (Bati), soft (Layyin), deep, compressible",
          sawdawi: "Small (Sagheer), wiry, hard, narrow caliber"
        }
      },
      {
        id: "q30_tongue",
        text: "Tongue body and coating appearance:",
        options: {
          damawi: "Clean pink body, moist, light thin clear coat",
          safrawi: "Red tip and edges, thin to moderate yellowish coat",
          balghami: "Pale, swollen with teeth marks, thick white slimy coat",
          sawdawi: "Dusky or bluish-purple, dry, thin brownish coat"
        }
      }
    ]
  }
};

const HUMOR_COLORS: Record<string, { badge: string; text: string; bar: string }> = {
  damawi: { badge: "bg-red-500/20 text-red-700 border-red-500/30", text: "text-red-700", bar: "bg-red-500" },
  safrawi: { badge: "bg-amber-500/20 text-amber-700 border-amber-500/30", text: "text-amber-700", bar: "bg-amber-500" },
  balghami: { badge: "bg-blue-500/20 text-blue-700 border-blue-500/30", text: "text-blue-700", bar: "bg-blue-500" },
  sawdawi: { badge: "bg-purple-500/20 text-purple-700 border-purple-500/30", text: "text-purple-700", bar: "bg-purple-500" },
};

export default function DoctorMizajPage() {
  const [activeTab, setActiveTab] = useState<"overview" | "zmai">("zmai");
  const [answers, setAnswers] = useState<Record<string, string>>({
    q1_build: "safrawi",
    q2_complexion: "safrawi",
    q3_skin_feel: "safrawi",
    q4_hair: "damawi",
    q5_joints: "safrawi"
  });
  const [result, setResult] = useState<ZMAIResult | null>(null);
  const [selectedDomain, setSelectedDomain] = useState<string>("morphology");

  const handleSelectAnswer = (qId: string, humor: string) => {
    const updated = { ...answers, [qId]: humor };
    setAnswers(updated);
    computeScore(updated);
  };

  const computeScore = async (currentAnswers: Record<string, string>) => {
    try {
      const res = await fetch("/api/v1/clinical/zmai/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responses: currentAnswers })
      });
      const data = await res.json();
      if (data && data.ok && data.assessment) {
        setResult(data.assessment);
        return;
      }
    } catch {
      // fallback
    }

    // Client-side calculation fallback
    const counts: Record<string, number> = { damawi: 0, safrawi: 0, balghami: 0, sawdawi: 0 };
    Object.values(currentAnswers).forEach(val => {
      if (counts[val] !== undefined) counts[val]++;
    });
    const total = Object.keys(currentAnswers).length || 1;
    const percentages: Record<string, number> = {
      damawi: Math.round((counts.damawi / total) * 100),
      safrawi: Math.round((counts.safrawi / total) * 100),
      balghami: Math.round((counts.balghami / total) * 100),
      sawdawi: Math.round((counts.sawdawi / total) * 100)
    };
    const sorted = Object.entries(percentages).sort((a, b) => b[1] - a[1]);
    const dominant = sorted[0][0];
    const secondary = sorted[1][0];

    setResult({
      total_questions_scored: total,
      counts,
      percentages,
      dominant_mizaj: dominant,
      secondary_mizaj: secondary,
      mizaj_formula: `${dominant.toUpperCase()}-${secondary.toUpperCase()}`,
      dyscrasia: percentages[dominant] >= 42 ? `Su-e-Mizaj ${dominant.toUpperCase()}` : null,
      clinical_guidance: {
        primary_organ_axis_vulnerability: dominant === "safrawi" ? "HEPATOBILIARY & GASTROINTESTINAL" : "CARDIOVASCULAR",
        dietary_thermal_direction: dominant === "safrawi" ? "Cooling & Demulcents (Tabreed & Tarseeb)" : "Ta'deel (Depurative)"
      }
    });
  };

  useEffect(() => {
    computeScore(answers);
  }, []);

  const domainsList = Object.entries(SAMPLE_DOMAINS);
  const currentDomainData = SAMPLE_DOMAINS[selectedDomain];

  return (
    <AppShell activeRole="doctor">
      <div className="space-y-6 max-w-7xl mx-auto pb-12">
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border)] pb-5">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-700 border border-emerald-500/20">
                Z-MAI 30-Point Validated Tool
              </span>
              <span className="text-xs text-[var(--text-muted)]">Canon of Medicine & Ajnas-e-Ashara</span>
            </div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] mt-1 tracking-tight">
              Clinical Mizaj Assessment & Dyscrasia Engine
            </h1>
            <p className="text-sm text-[var(--text-muted)] mt-0.5">
              Comprehensive 6-domain constitutional profiling to calibrate individual pharmacokinetics, organ-axis vulnerability, and Parhez.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("zmai")}
              className={`text-xs px-3.5 py-2 rounded-lg font-medium transition ${
                activeTab === "zmai"
                  ? "bg-emerald-700 text-white"
                  : "bg-[var(--surface-accent)] text-[var(--text-secondary)] border border-[var(--border)]"
              }`}
            >
              30-Point Z-MAI Assessment
            </button>
            <Link
              href="/doctor/organ-axis"
              className="text-xs px-3.5 py-2 rounded-lg font-medium bg-[var(--surface-accent)] text-[var(--text-secondary)] border border-[var(--border)] hover:border-emerald-500 transition"
            >
              Organ-Axis Matrix →
            </Link>
          </div>
        </div>

        {/* Real-time Assessment Summary Card */}
        {result && (
          <div className="bg-gradient-to-r from-emerald-950/40 via-teal-950/30 to-[var(--surface)] border border-emerald-500/30 rounded-xl p-5 shadow-sm">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Constitutional Verdict */}
              <div className="space-y-2 border-r border-[var(--border)] pr-4">
                <span className="text-xs font-semibold tracking-wider text-emerald-700 uppercase">
                  Constitutional Formula
                </span>
                <div className="text-2xl font-bold text-white capitalize">
                  {result.dominant_mizaj}-{result.secondary_mizaj}
                </div>
                <div className="flex items-center gap-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${HUMOR_COLORS[result.dominant_mizaj]?.badge || ""}`}>
                    Primary: {result.dominant_mizaj}
                  </span>
                  <span className="text-xs text-[var(--text-muted)]">
                    Scored: {result.total_questions_scored}/30
                  </span>
                </div>
                {result.dyscrasia && (
                  <div className="text-xs text-amber-700 font-semibold bg-amber-500/10 border border-amber-500/20 p-2 rounded mt-2">
                    ⚠ {result.dyscrasia}
                  </div>
                )}
              </div>

              {/* Humor Percentage Breakdown */}
              <div className="lg:col-span-2 space-y-2.5">
                <span className="text-xs font-semibold tracking-wider text-[var(--text-muted)] uppercase">
                  Humoral Equilibrium (%)
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {(["damawi", "safrawi", "balghami", "sawdawi"] as const).map(h => {
                    const pct = result.percentages[h] || 0;
                    return (
                      <div key={h} className="bg-[var(--surface)] border border-[var(--border)] p-3 rounded-lg">
                        <div className="flex justify-between items-center text-xs mb-1">
                          <span className="capitalize font-medium text-[var(--text-primary)]">{h}</span>
                          <span className="font-bold text-white">{pct}%</span>
                        </div>
                        <div className="w-full bg-[var(--surface-accent)] h-1.5 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${HUMOR_COLORS[h].bar}`}
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Clinical Direction */}
              <div className="space-y-2 text-xs">
                <span className="font-semibold text-emerald-700 uppercase tracking-wider">
                  Therapeutic Direction
                </span>
                <div className="text-[var(--text-muted)] leading-relaxed">
                  <span className="font-bold text-[var(--text-primary)]">Axis Vulnerability:</span>{" "}
                  {result.clinical_guidance?.primary_organ_axis_vulnerability || "Assessing..."}
                </div>
                <div className="text-[var(--text-muted)] leading-relaxed">
                  <span className="font-bold text-[var(--text-primary)]">Dietary Parhez:</span>{" "}
                  {result.clinical_guidance?.dietary_thermal_direction || "Assessing..."}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 6-Domain Question Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Domain Navigation Sidebar */}
          <div className="space-y-2">
            <span className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider px-2">
              Clinical Domains (6)
            </span>
            {domainsList.map(([dKey, dVal], idx) => {
              const qCount = dVal.questions.length;
              const answeredCount = dVal.questions.filter(q => !!answers[q.id]).length;
              const isSelected = selectedDomain === dKey;

              return (
                <button
                  key={dKey}
                  onClick={() => setSelectedDomain(dKey)}
                  className={`w-full text-left p-3 rounded-lg border text-xs transition flex items-center justify-between ${
                    isSelected
                      ? "bg-emerald-950/20 border-emerald-500 text-emerald-700 font-semibold"
                      : "bg-[var(--surface)] border-[var(--border)] text-[var(--text-secondary)] hover:border-[var(--border-strong)]"
                  }`}
                >
                  <div>
                    <div>{dVal.title}</div>
                    <div className="text-[10px] text-[var(--text-muted)] mt-0.5">
                      {answeredCount}/{qCount} answered
                    </div>
                  </div>
                  {answeredCount === qCount && (
                    <span className="text-emerald-700 font-bold">✓</span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Questions Panel for Selected Domain */}
          <div className="lg:col-span-3 space-y-4">
            <div className="flex items-center justify-between border-b border-[var(--border)] pb-2">
              <h2 className="text-lg font-bold text-[var(--text-primary)]">
                {currentDomainData?.title}
              </h2>
              <span className="text-xs text-[var(--text-muted)]">
                5 validated indicators
              </span>
            </div>

            <div className="space-y-4">
              {currentDomainData?.questions.map((q, qIndex) => {
                const selected = answers[q.id];

                return (
                  <div key={q.id} className="zv-card p-4 space-y-2.5 rounded-xl border border-[var(--border)]">
                    <div className="flex items-start justify-between gap-2">
                      <span className="font-semibold text-sm text-[var(--text-primary)]">
                        {qIndex + 1}. {q.text}
                      </span>
                      {selected && (
                        <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${HUMOR_COLORS[selected]?.badge || ""}`}>
                          {selected}
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {(["damawi", "safrawi", "balghami", "sawdawi"] as const).map(hKey => {
                        const optText = q.options[hKey];
                        const isChosen = selected === hKey;

                        return (
                          <button
                            key={hKey}
                            onClick={() => handleSelectAnswer(q.id, hKey)}
                            className={`text-left p-3 rounded-lg border text-xs transition ${
                              isChosen
                                ? "border-emerald-500 bg-emerald-950/30 text-white ring-1 ring-emerald-500/40"
                                : "border-[var(--border)] bg-[var(--surface-accent)] text-[var(--text-secondary)] hover:border-[var(--border-strong)]"
                            }`}
                          >
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-bold text-[11px] uppercase tracking-wider text-[var(--text-muted)]">
                                {hKey}
                              </span>
                              {isChosen && <span className="text-emerald-700">●</span>}
                            </div>
                            <div className="leading-relaxed">{optText}</div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
