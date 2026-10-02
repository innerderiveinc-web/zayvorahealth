"""
ZAYVORA Health OS™ — Z-MAI (Zayvora Mizaj Assessment Instrument)
================================================================
A 30-point, 6-domain validated clinical instrument for determining human
constitutional temperament (Mizaj) according to the Canon of Medicine
(Avicenna / Ibn Sina) and Unani medicine:
- Domain 1: Morphology & Somatotype (5 points)
- Domain 2: Digestion & Hazm (5 points)
- Domain 3: Sleep Architecture & Oneiric Patterns (5 points)
- Domain 4: Thermal Response & Weather Adaptation (5 points)
- Domain 5: Mental, Cognitive & Emotional Profile (5 points)
- Domain 6: Elimination & Secretions (5 points)
"""

from typing import Dict, Any, List, Tuple

DOMAINS: Dict[str, Dict[str, Any]] = {
    "morphology": {
        "title": "Morphology & Somatotype",
        "weight": 5,
        "questions": [
            {
                "id": "q1_build",
                "text": "Body build and skeletal frame:",
                "options": {
                    "damawi": "Muscular, broad, symmetrical, robust frame",
                    "safrawi": "Lean, sinewy, angular, prominent tendons",
                    "balghami": "Heavy, soft, adipose, rounded frame",
                    "sawdawi": "Thin, bony, delicate, narrow chest"
                }
            },
            {
                "id": "q2_complexion",
                "text": "Facial complexion and skin undertone:",
                "options": {
                    "damawi": "Ruddy, pinkish-red, flushed, vibrant",
                    "safrawi": "Yellowish, sallow, warm olive, flushed in heat",
                    "balghami": "Pale, chalky white, cool, clear",
                    "sawdawi": "Dusky, dark, hyper-pigmented, dull, dry"
                }
            },
            {
                "id": "q3_skin_feel",
                "text": "Skin texture and tactile warmth:",
                "options": {
                    "damawi": "Warm and moist, supple, well-perfused",
                    "safrawi": "Hot and dry, thin, prone to flushing",
                    "balghami": "Cool and moist, soft, smooth, damp",
                    "sawdawi": "Cold and dry, rough, coarse, scaling"
                }
            },
            {
                "id": "q4_hair",
                "text": "Hair thickness, color and density:",
                "options": {
                    "damawi": "Thick, dark, lustrous, wavy, rapid growth",
                    "safrawi": "Fine, reddish or blonde-brown, early thinning/balding",
                    "balghami": "Thick, straight, oily, slow to grey",
                    "sawdawi": "Dry, coarse, frizzy, brittle, split ends"
                }
            },
            {
                "id": "q5_joints",
                "text": "Joints and skeletal structure:",
                "options": {
                    "damawi": "Firm, well-covered with muscle, stable",
                    "safrawi": "Prominent, visible veins and tendons",
                    "balghami": "Large, fleshy, well-padded, lax ligaments",
                    "sawdawi": "Bony, crackling sounds on motion, prominent joints"
                }
            }
        ]
    },
    "digestion": {
        "title": "Digestion & Appetite (Hazm wa Ishtiha)",
        "weight": 5,
        "questions": [
            {
                "id": "q6_appetite",
                "text": "Natural appetite intensity:",
                "options": {
                    "damawi": "Strong, regular, enjoys hearty meals",
                    "safrawi": "Voracious, intense, irritable if meals delayed",
                    "balghami": "Weak, slow to develop, skips meals easily",
                    "sawdawi": "Erratic, false hunger, variable appetite"
                }
            },
            {
                "id": "q7_thirst",
                "text": "Thirst sensation and water intake:",
                "options": {
                    "damawi": "Normal to moderate, satisfied with cool water",
                    "safrawi": "Intense, frequent craving for ice-cold beverages",
                    "balghami": "Low thirst, rarely feels thirsty, dislikes cold water",
                    "sawdawi": "Dry mouth with minimal thirst desire"
                }
            },
            {
                "id": "q8_digestion_speed",
                "text": "Speed and ease of digestion:",
                "options": {
                    "damawi": "Rapid, robust, comfortable digestion",
                    "safrawi": "Very rapid, hyperacidic, heartburn tendency",
                    "balghami": "Sluggish, takes hours, heavy post-meal fatigue",
                    "sawdawi": "Slow, gaseous, bloating, irregular fermentation"
                }
            },
            {
                "id": "q9_cravings",
                "text": "Preferred tastes and food cravings:",
                "options": {
                    "damawi": "Cooling, refreshing, sour, citrus, salads",
                    "safrawi": "Cold, sweet, soothing milk/desserts, bitter foods",
                    "balghami": "Hot, pungent, spicy, ginger, black pepper",
                    "sawdawi": "Warm, rich, moist, sweet, comfort foods"
                }
            },
            {
                "id": "q10_postmeal",
                "text": "Physical sensation after a full meal:",
                "options": {
                    "damawi": "Pleasantly energized and contented",
                    "safrawi": "Internal heat, epigastric acidity or burning",
                    "balghami": "Severe heaviness, brain fog, sleepiness",
                    "sawdawi": "Abdominal distension, gas, borborygmi, discomfort"
                }
            }
        ]
    },
    "sleep": {
        "title": "Sleep Architecture & Oneiric Themes (Naum wa Ru'ya)",
        "weight": 5,
        "questions": [
            {
                "id": "q11_sleep_depth",
                "text": "Typical sleep duration and depth:",
                "options": {
                    "damawi": "Moderate (7-8 hours), deep, highly restorative",
                    "safrawi": "Short (5-6 hours), light, easily awakened",
                    "balghami": "Excessive (>8-10 hours), very deep, hard to wake",
                    "sawdawi": "Fragmented (4-6 hours), tossing and turning, insomnia"
                }
            },
            {
                "id": "q12_dream_themes",
                "text": "Predominant dream imagery and themes:",
                "options": {
                    "damawi": "Red colors, flowers, celebrations, joyful flying, blood",
                    "safrawi": "Fire, lightning, warfare, yellow hues, burning",
                    "balghami": "Water, swimming, rain, snow, white scenery, lakes",
                    "sawdawi": "Darkness, falling, being chased, anxiety, monsters, grief"
                }
            },
            {
                "id": "q13_sleep_latency",
                "text": "Ease of falling asleep at night:",
                "options": {
                    "damawi": "Normal sleep onset within 15-20 minutes",
                    "safrawi": "Variable, restless before settling",
                    "balghami": "Falls asleep almost immediately upon lying down",
                    "sawdawi": "Prolonged sleep latency (>45 minutes), racing mind"
                }
            },
            {
                "id": "q14_awakening",
                "text": "Morning state upon awakening:",
                "options": {
                    "damawi": "Refreshed, cheerful, ready for daily work",
                    "safrawi": "Alert immediately, dry throat, bitter mouth",
                    "balghami": "Lethargic, groggy, needs an hour to fully wake",
                    "sawdawi": "Fatigued, anxious about the day, unrefreshed"
                }
            },
            {
                "id": "q15_daytime_naps",
                "text": "Daytime sleepiness tendency:",
                "options": {
                    "damawi": "Rare, occasional brief post-lunch power nap",
                    "safrawi": "None, high daytime adrenaline/arousal",
                    "balghami": "Strong habitual desire for prolonged afternoon nap",
                    "sawdawi": "Exhausted but unable to nap peacefully"
                }
            }
        ]
    },
    "thermal": {
        "title": "Thermal Adaptation & Climatic Response",
        "weight": 5,
        "questions": [
            {
                "id": "q16_cold_weather",
                "text": "Response to cold environmental temperatures:",
                "options": {
                    "damawi": "Comfortable in cold, enjoys crisp winter weather",
                    "safrawi": "Thrives in cold air, seeks cold rooms and shade",
                    "balghami": "Extremely uncomfortable, shivers, aches in cold",
                    "sawdawi": "Very sensitive to cold, joint stiffness, cold misery"
                }
            },
            {
                "id": "q17_hot_weather",
                "text": "Response to summer heat and humidity:",
                "options": {
                    "damawi": "Dislikes oppressive humid heat, tolerates dry warmth",
                    "safrawi": "Suffers intensely in summer, prone to heat rashes/anger",
                    "balghami": "Loves hot sunny weather, feels energized in heat",
                    "sawdawi": "Prefers mild warmth, dislikes dry hot autumn winds"
                }
            },
            {
                "id": "q18_sweating",
                "text": "Perspiration quantity and odor:",
                "options": {
                    "damawi": "Profuse, warm, neutral to sweetish odor",
                    "safrawi": "Abundant, hot, sharp or pungent odor",
                    "balghami": "Scanty, cool, clammy, odorless",
                    "sawdawi": "Minimal to dry, coarse skin with rarely any sweat"
                }
            },
            {
                "id": "q19_worst_season",
                "text": "Season with highest symptom exacerbation:",
                "options": {
                    "damawi": "Spring (Rabi) - allergies, epistaxis, headaches",
                    "safrawi": "Summer (Saif) - irritability, acid reflux, skin eruptions",
                    "balghami": "Winter (Shita) - phlegm, lethargy, joint sluggishness",
                    "sawdawi": "Autumn (Kharif) - melancholy, dry skin, insomnia"
                }
            },
            {
                "id": "q20_extremities",
                "text": "Baseline temperature of hands and feet:",
                "options": {
                    "damawi": "Consistently warm, pink, healthy circulation",
                    "safrawi": "Warm to hot, burning soles of feet at night",
                    "balghami": "Cold and damp, clammy palms",
                    "sawdawi": "Icy cold, dry, pale or bluish fingers in cold"
                }
            }
        ]
    },
    "mental": {
        "title": "Mental, Cognitive & Emotional Profile (Nafsiyat)",
        "weight": 5,
        "questions": [
            {
                "id": "q21_temperament",
                "text": "Dominant emotional predisposition:",
                "options": {
                    "damawi": "Optimistic, cheerful, gregarious, generous",
                    "safrawi": "Intense, ambitious, competitive, quick-tempered",
                    "balghami": "Peaceful, placid, steady, slow to anger, forgiving",
                    "sawdawi": "Thoughtful, analytical, melancholic, perfectionist"
                }
            },
            {
                "id": "q22_speech",
                "text": "Natural speech cadence and voice tone:",
                "options": {
                    "damawi": "Loud, resonant, fluent, animated, enthusiastic",
                    "safrawi": "Fast, decisive, sharp, articulate, commanding",
                    "balghami": "Soft, slow, measured, gentle, quiet",
                    "sawdawi": "Cautious, low volume, precise, detailed"
                }
            },
            {
                "id": "q23_stress",
                "text": "Response to acute psychological crisis or stress:",
                "options": {
                    "damawi": "Faces it with confidence, can become overly dramatic",
                    "safrawi": "Confrontational, explosive outburst, then calms down",
                    "balghami": "Withdraws into quiet, avoids confrontation, patient",
                    "sawdawi": "Deep worry, chronic rumination, catastrophizing"
                }
            },
            {
                "id": "q24_learning",
                "text": "Learning style and memory retention:",
                "options": {
                    "damawi": "Learns quickly, grasps the big picture, moderate recall",
                    "safrawi": "Sharp analytical intellect, fast grasp, selective memory",
                    "balghami": "Takes time to learn, but permanent lifelong retention",
                    "sawdawi": "Deep methodical study, retains details and grievances"
                }
            },
            {
                "id": "q25_activity_tempo",
                "text": "Pace of daily movement and execution:",
                "options": {
                    "damawi": "Energetic, dynamic, fluid, social",
                    "safrawi": "Fast-paced, goal-driven, restless, hurried",
                    "balghami": "Steady, unhurried, prefers routine, calm",
                    "sawdawi": "Systematic, meticulous, cautious, stops to review"
                }
            }
        ]
    },
    "elimination": {
        "title": "Elimination & Biological Secretions (Istifragh)",
        "weight": 5,
        "questions": [
            {
                "id": "q26_bowels",
                "text": "Typical bowel evacuation pattern:",
                "options": {
                    "damawi": "Regular 1-2 times daily, well-formed, easy passage",
                    "safrawi": "Frequent (2-3 times), loose or soft, burning sensation",
                    "balghami": "Sluggish, pale, soft, occurs once daily or alternate days",
                    "sawdawi": "Dry, hard, pellet-like stools, chronic constipation"
                }
            },
            {
                "id": "q27_urine",
                "text": "Baseline urine color and urination sensation:",
                "options": {
                    "damawi": "Straw-yellow, normal volume, painless",
                    "safrawi": "Dark amber or reddish-yellow, concentrated, warm feeling",
                    "balghami": "Pale, clear, copious, frequent volume",
                    "sawdawi": "Variable, cloudy or dusky, occasional sediment"
                }
            },
            {
                "id": "q28_oral_state",
                "text": "Morning oral taste and salivation:",
                "options": {
                    "damawi": "Normal saliva, sweetish pleasant aftertaste",
                    "safrawi": "Dryness, bitter taste on the back of the tongue",
                    "balghami": "Excessive watery saliva, sweetish or tasteless mouth",
                    "sawdawi": "Dry mouth, sour or astringent taste on waking"
                }
            },
            {
                "id": "q29_pulse",
                "text": "Classical pulse characteristics (Nabz):",
                "options": {
                    "damawi": "Full (Imtila), large, bounding, rhythmic",
                    "safrawi": "Rapid (Sari), tense, sharp stroke, frequent",
                    "balghami": "Slow (Bati), soft (Layyin), deep, compressible",
                    "sawdawi": "Small (Sagheer), wiry, hard, narrow caliber"
                }
            },
            {
                "id": "q30_tongue",
                "text": "Tongue body and coating appearance:",
                "options": {
                    "damawi": "Clean pink body, moist, light thin clear coat",
                    "safrawi": "Red tip and edges, thin to moderate yellowish coat",
                    "balghami": "Pale, swollen with teeth marks, thick white slimy coat",
                    "sawdawi": "Dusky or bluish-purple, dry, thin brownish coat"
                }
            }
        ]
    }
}


def calculate_zmai_score(responses: Dict[str, str]) -> Dict[str, Any]:
    """
    Computes constitutional Mizaj score based on 30 answered questions.
    responses: dict mapping question_id (e.g. 'q1_build') to humor string:
               'damawi', 'safrawi', 'balghami', 'sawdawi'
    """
    counts = {"damawi": 0, "safrawi": 0, "balghami": 0, "sawdawi": 0}
    total_answered = 0
    
    for domain_name, domain_data in DOMAINS.items():
        for q in domain_data["questions"]:
            qid = q["id"]
            if qid in responses:
                choice = responses[qid].lower()
                if choice in counts:
                    counts[choice] += 1
                    total_answered += 1

    # Standardize to 30 points if fewer answered
    effective_total = total_answered if total_answered > 0 else 30
    
    percentages = {
        k: round((v / effective_total) * 100, 1) for k, v in counts.items()
    }
    
    # Sort humors by percentage
    sorted_humors = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    dominant_humor = sorted_humors[0][0]
    secondary_humor = sorted_humors[1][0]
    
    mizaj_formula = f"{dominant_humor.capitalize()}-{secondary_humor.capitalize()}"
    
    # Su-e-Mizaj (Dyscrasia) determination
    dyscrasia = None
    if percentages[dominant_humor] >= 42.0:
        dyscrasia_map = {
            "damawi": "Su-e-Mizaj Haar Ratb (Hot-Moist Dyscrasia / Sanguine Plethora)",
            "safrawi": "Su-e-Mizaj Haar Yabis (Hot-Dry Dyscrasia / Bilious Irritation)",
            "balghami": "Su-e-Mizaj Barid Ratb (Cold-Moist Dyscrasia / Phlegmatic Stagnation)",
            "sawdawi": "Su-e-Mizaj Barid Yabis (Cold-Dry Dyscrasia / Melancholic Contraction)"
        }
        dyscrasia = dyscrasia_map.get(dominant_humor)

    return {
        "total_questions_scored": total_answered,
        "counts": counts,
        "percentages": percentages,
        "dominant_mizaj": dominant_humor,
        "secondary_mizaj": secondary_humor,
        "mizaj_formula": mizaj_formula,
        "dyscrasia": dyscrasia,
        "clinical_guidance": {
            "primary_organ_axis_vulnerability": {
                "damawi": "CARDIOVASCULAR & CEREBROVASCULAR (hypertension, plethora)",
                "safrawi": "HEPATOBILIARY & GASTROINTESTINAL (inflammation, hyperacidity)",
                "balghami": "PULMONARY & METABOLIC (mucus, insulin resistance, edema)",
                "sawdawi": "NEUROPSYCHIATRIC & MUSCULOSKELETAL (spasm, insomnia, joint pain)"
            }.get(dominant_humor),
            "dietary_thermal_direction": {
                "damawi": "Ta'deel (Cooling & depurative, reduce red meat & sweets)",
                "safrawi": "Tabreed & Tarseeb (Cold & moist demulcents, avoid chilies)",
                "balghami": "Tas-kheen & Tajfeef (Warm & dry aromatics, avoid cold dairy)",
                "sawdawi": "Tas-kheen & Tarseeb (Warm & moist nourishing, avoid dry astringents)"
            }.get(dominant_humor)
        }
    }


def get_all_domains() -> Dict[str, Dict[str, Any]]:
    """Returns complete 30-question assessment structure."""
    return DOMAINS


# ============================================================================
# MIZAJ 2.0: 6-DOMAIN OPERATIONAL TEMPERAMENT MATRIX (PART ONE CHAPTER 9)
# ============================================================================
MIZAJ_2_DOMAINS = [
    "body_build_weight",
    "skin_complexion",
    "psychological_profile",
    "digestion_appetite",
    "sleep_quality",
    "tongue_pulse"
]


def calculate_mizaj_2_matrix(domain_scores: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
    """
    Calculates the Mizaj 2.0 Profile across the 6 clinical domains (Chapter 9):
      - Scored 0-3 for each humor: Balgham, Safra, Sauda, Dam.
      - Total possible per humor = 18 points.
      - Thresholds:
          >= 10: Significant Dominance (triggers primary protocol)
          7-9:   Moderate Tendency (secondary corrective trigger)
          < 7:   Minimal Presence
      - Automatically outputs the mandated dosage form based on dominant Mizaj.
    """
    humor_totals = {"balgham": 0, "safra": 0, "sauda": 0, "dam": 0}

    for dom, scores in domain_scores.items():
        for h in humor_totals.keys():
            val = int(scores.get(h, 0))
            # clamp 0-3
            val = max(0, min(3, val))
            humor_totals[h] += val

    # Sort humors by total score
    sorted_scores = sorted(humor_totals.items(), key=lambda x: x[1], reverse=True)
    primary_humor, primary_score = sorted_scores[0]
    secondary_humor, secondary_score = sorted_scores[1]

    # Clinical Categorization
    def categorize_score(s: int) -> str:
        if s >= 10:
            return "SIGNIFICANT_DOMINANCE"
        elif s >= 7:
            return "MODERATE_TENDENCY"
        return "MINIMAL_PRESENCE"

    classifications = {h: {"score": s, "category": categorize_score(s)} for h, s in humor_totals.items()}

    # Dosage form & Clinical adjustments (Section 9.4)
    if primary_humor == "balgham" and primary_score >= 10:
        recommended_form = "Safoof (Dry Powder Capsule / Churna)"
        contraindicated_form = "Majoon (Moist Electuary is strictly contraindicated for Balgham)"
        drug_strategy = "Mujaffif (drying) + Muharrik (stimulating) drugs (Guggul, Zeera Siyah, Methi)"
        diet_focus = "Strict avoidance of cold, moist foods (dairy, ice cream, excess fruit)"
        monitoring_interval = "Bi-monthly biomarker check"
    elif primary_humor == "safra" and primary_score >= 10:
        recommended_form = "Joshanda (Aqueous Decoction) or cooling powder with water"
        contraindicated_form = "Hot pungent warming electuaries"
        drug_strategy = "Muhallil (resolvent) + cooling agents (Tabasheer, Amla, Sandal Safaid)"
        diet_focus = "Avoidance of spicy, fried, acidic foods"
        monitoring_interval = "Monthly biomarker monitoring (CRP, ALT, ESR)"
    elif primary_humor == "sauda" and primary_score >= 10:
        recommended_form = "Arq (Aqueous Hydrosol) / Sharbat (Hydrating Demulcent Syrup)"
        contraindicated_form = "Dry astringent powders without moistening vehicle"
        drug_strategy = "Mufarrih (mood-elevating) + neuro-antioxidants (Jatamansi, Asgandh, Badam)"
        diet_focus = "Avoidance of stale, fermented, astringent foods"
        monitoring_interval = "Monthly biomarker monitoring (Cortisol, MDA)"
    else:
        recommended_form = "Mutadil Safoof or mild Majoon with warm water"
        contraindicated_form = "Extreme thermal preparations"
        drug_strategy = "Musaffi-e-Dam (blood purifying) + Mudirr (diuretic) (Punarnava, Unnab)"
        diet_focus = "Ta'deel (cooling and depurative balance, reduce heavy red meat)"
        monitoring_interval = "Quarterly check-in"

    return {
        "mizaj_scores": humor_totals,
        "max_possible_per_humor": 18,
        "primary_dominant_humor": primary_humor,
        "primary_score": primary_score,
        "primary_category": categorize_score(primary_score),
        "secondary_humor": secondary_humor,
        "secondary_score": secondary_score,
        "classifications": classifications,
        "clinical_adjustment_logic": {
            "recommended_dosage_form": recommended_form,
            "contraindicated_dosage_form": contraindicated_form,
            "pharmacological_strategy": drug_strategy,
            "parhez_focus": diet_focus,
            "monitoring_frequency": monitoring_interval
        }
    }
