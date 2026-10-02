"""
ZAYVORA Health OS™ — Phenotype & Response Intelligence Engine (Phase 19 & 20 Foundation)
========================================================================================
Implements:
1. Clinical Sub-Phenotype Stratification:
   Maps diagnosis + 10-Ajnas Mizaj + 12 Organ-Axes + Biomarkers into constitutional sub-phenotypes.
   Example:
     Waja-ul-Mafasil (Joint Pain/Arthritis) →
       - Balghami Ghaleez (Phlegmatic-Stagnant: cold, damp, swollen, morning stiffness)
       - Safrawi Haar (Bilious-Inflammatory: burning heat, redness, acute effusion)
       - Sawdawi Yabis (Melancholic-Desiccated: degenerative crepitus, chronic stiffness)
       - Damawi Imtila (Sanguine-Plethoric: throbbing vascular congestion, full pulse)

2. 5-Tier Canonical Response Intelligence Classification:
   - RESPONDER: ≥ 75% symptom improvement + positive biomarker delta + restored humoral equilibrium
   - PARTIAL_RESPONDER: 40% - 74% improvement
   - NON_RESPONDER: < 40% improvement despite acceptable adherence
   - INTOLERANT: Adverse drug reaction or constitutional humoral aggravation
   - ADHERENT_NON_RESPONDER: Adherence ≥ 80% with < 15% improvement
     → Crucial safety trigger: Flags failed first-line therapy to prevent toxic persistence,
       recommends second-line Badal-e-Advia switch and expert Hakeem case review.
"""

from __future__ import annotations

import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


class ResponseClassificationTier(str, Enum):
    RESPONDER = "RESPONDER"
    PARTIAL_RESPONDER = "PARTIAL_RESPONDER"
    NON_RESPONDER = "NON_RESPONDER"
    INTOLERANT = "INTOLERANT"
    ADHERENT_NON_RESPONDER = "ADHERENT_NON_RESPONDER"


@dataclass
class ClinicalPhenotypeProfile:
    condition_name: str
    primary_mizaj: str
    dominant_organ_axis: str
    phenotype_code: str
    phenotype_name: str
    temperament_qualities: Dict[str, str]
    pathological_humor: str
    suggested_line_of_treatment: str
    contraindicated_categories: List[str]
    biomarker_patterns: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResponseEvaluation:
    patient_id: str
    tier: ResponseClassificationTier
    vas_baseline: float
    vas_followup: float
    vas_improvement_pct: float
    adherence_pct: float
    adverse_events_count: int
    biomarker_improvement_score: float  # 0.0 to 1.0
    protocol_switch_recommended: bool
    clinical_recommendation: str
    evaluation_timestamp: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier.value
        return d


class PhenotypeAndResponseEngine:
    """
    Sub-phenotype stratification & 5-tier response classification engine.
    """

    PHENOTYPE_CATALOG = {
        "waja_ul_mafasil": {
            "balghami": ClinicalPhenotypeProfile(
                condition_name="Waja-ul-Mafasil",
                primary_mizaj="Balghami (Cold & Wet)",
                dominant_organ_axis="Musculoskeletal & Articular (Mafasil)",
                phenotype_code="PHENO-ARTH-BALGHAM",
                phenotype_name="Phlegmatic-Stagnant (Balghami Ghaleez)",
                temperament_qualities={"heat": "Barid (Cold)", "moisture": "Ratab (Wet)"},
                pathological_humor="Balgham Ghaleez (Viscous Phlegm)",
                suggested_line_of_treatment="Tanqia-e-Balgham (Munzij & Mushil), warm resolvent fomentation (Takmeed Haar), Majun Suranjan.",
                contraindicated_categories=["Cold/Damp hydrotherapy", "Excessive sedentary rest", "Heavy mucus-forming diet"],
                biomarker_patterns={"ESR": "Mildly elevated", "Synovial effusion": "High viscosity, cold effusion"}
            ),
            "safrawi": ClinicalPhenotypeProfile(
                condition_name="Waja-ul-Mafasil",
                primary_mizaj="Safrawi (Hot & Dry)",
                dominant_organ_axis="Musculoskeletal & Articular (Mafasil)",
                phenotype_code="PHENO-ARTH-SAFRA",
                phenotype_name="Bilious-Inflammatory (Safrawi Haar)",
                temperament_qualities={"heat": "Haar (Hot)", "moisture": "Yabis (Dry)"},
                pathological_humor="Safra Hadda (Acute Bilious Humor)",
                suggested_line_of_treatment="Tabreed (Cooling), Tadil-e-Safra, Zimad of Sandal & Gul-e-Surkh, Sharbat Bazoori.",
                contraindicated_categories=["Hot fomentations", "Pungent spicy herbs", "Vigorous friction"],
                biomarker_patterns={"CRP": "Markedly elevated", "Joint temperature": "Warm to hot on palpation"}
            ),
            "sawdawi": ClinicalPhenotypeProfile(
                condition_name="Waja-ul-Mafasil",
                primary_mizaj="Sawdawi (Cold & Dry)",
                dominant_organ_axis="Musculoskeletal & Articular (Mafasil)",
                phenotype_code="PHENO-ARTH-SAWDA",
                phenotype_name="Melancholic-Desiccated (Sawdawi Yabis)",
                temperament_qualities={"heat": "Barid (Cold)", "moisture": "Yabis (Dry)"},
                pathological_humor="Sawda Muhtariqa (Burnt/Oxidized Black Bile)",
                suggested_line_of_treatment="Tartib (Moistening & Hydration), Munzij-e-Sawda, Roghan Babuna massage, gentle Ilaj bil Ghiza.",
                contraindicated_categories=["Excessive astringents", "Desiccating dry heat", "Sour acidic foods"],
                biomarker_patterns={"Joint stiffness": "Severe morning & evening crepitus", "Bone density": "Osteopenic tendency"}
            ),
            "damawi": ClinicalPhenotypeProfile(
                condition_name="Waja-ul-Mafasil",
                primary_mizaj="Damawi (Hot & Wet)",
                dominant_organ_axis="Musculoskeletal & Articular (Mafasil)",
                phenotype_code="PHENO-ARTH-DAM",
                phenotype_name="Sanguine-Plethoric (Damawi Imtila)",
                temperament_qualities={"heat": "Haar (Hot)", "moisture": "Ratab (Wet)"},
                pathological_humor="Dam Imtila'i (Plethoric Congestive Blood)",
                suggested_line_of_treatment="Fasd (Venesection) or Hijama Bish-Shart, Tanqia-e-Dam, light cooling diet (Sikanjabin).",
                contraindicated_categories=["High red meat intake", "Heavy tonics", "Excessive heat exposure"],
                biomarker_patterns={"Pulse": "Full, bounding (Nabz Imtila)", "Facial complexion": "Ruddy/Erythematous"}
            )
        },
        "ziyabetus": {
            "haar": ClinicalPhenotypeProfile(
                condition_name="Ziyabetus (Diabetes Mellitus)",
                primary_mizaj="Haar Yabis (Hot & Dry)",
                dominant_organ_axis="Hepato-Renal & Metabolic (Kabid & Kulliyah)",
                phenotype_code="PHENO-DM-HAAR",
                phenotype_name="Ziyabetus Haar (Metabolic Burn / Intense Thirst)",
                temperament_qualities={"heat": "Haar (Hot)", "moisture": "Yabis (Dry)"},
                pathological_humor="Du'f al-Kulliyah bi-Sabab al-Hararah",
                suggested_line_of_treatment="Tabreed al-Kulliyah, Jamun seed kernel, Gurmar, Kushta Baiza-e-Murgh, Sikanjabin Bazoori.",
                contraindicated_categories=["Heating stimulatory tonics", "Excess salt & fried foods"],
                biomarker_patterns={"HbA1c": "Elevated", "Urine Specific Gravity": "High with glucose wasting"}
            ),
            "barid": ClinicalPhenotypeProfile(
                condition_name="Ziyabetus (Diabetes Mellitus)",
                primary_mizaj="Barid Ratab (Cold & Wet)",
                dominant_organ_axis="Hepato-Pancreatic & Renal (Kabid & Kulliyah)",
                phenotype_code="PHENO-DM-BARID",
                phenotype_name="Ziyabetus Barid (Sluggish Metabolism / Fluid retention)",
                temperament_qualities={"heat": "Barid (Cold)", "moisture": "Ratab (Wet)"},
                pathological_humor="Su-e-Mizaj Barid Kabidi wa Kulliyah",
                suggested_line_of_treatment="Taskheen-e-Mo'tadil (Gentle Warming), Dar Chini, Halela Siyah, Regimental Riyazat (Exercise).",
                contraindicated_categories=["Sedentary inertia", "Cold mucilaginous foods"],
                biomarker_patterns={"Fasting Insulin": "High with Insulin Resistance", "Lipids": "Hypertriglyceridemia"}
            )
        }
    }

    def classify_phenotype(
        self,
        condition: str,
        mizaj: str,
        dominant_axis: str = "General",
        biomarkers: Optional[Dict[str, Any]] = None
    ) -> ClinicalPhenotypeProfile:
        """
        Classifies patient into canonical clinical sub-phenotype based on condition and humoral state.
        """
        cond_key = condition.lower().replace("-", "_").replace(" ", "_")
        mizaj_lower = mizaj.lower()

        # Check matched condition in catalog
        catalog_entry = None
        for key in self.PHENOTYPE_CATALOG:
            if key in cond_key or cond_key in key:
                catalog_entry = self.PHENOTYPE_CATALOG[key]
                break

        if catalog_entry:
            if "balgham" in mizaj_lower or "phlegm" in mizaj_lower or "cold_wet" in mizaj_lower or "barid ratab" in mizaj_lower:
                if "balghami" in catalog_entry:
                    return catalog_entry["balghami"]
                elif "barid" in catalog_entry:
                    return catalog_entry["barid"]
            elif "safra" in mizaj_lower or "bilious" in mizaj_lower or "hot_dry" in mizaj_lower or "haar yabis" in mizaj_lower:
                if "safrawi" in catalog_entry:
                    return catalog_entry["safrawi"]
                elif "haar" in catalog_entry:
                    return catalog_entry["haar"]
            elif "sawda" in mizaj_lower or "melancholic" in mizaj_lower or "cold_dry" in mizaj_lower:
                if "sawdawi" in catalog_entry:
                    return catalog_entry["sawdawi"]
            elif "dam" in mizaj_lower or "sanguine" in mizaj_lower or "hot_wet" in mizaj_lower:
                if "damawi" in catalog_entry:
                    return catalog_entry["damawi"]

            # Fallback to first available phenotype in condition catalog
            first_key = next(iter(catalog_entry))
            return catalog_entry[first_key]

        # Generic Dynamic Classification for conditions not pre-cataloged
        humor = "Murakkab (Mixed)"
        if "balgham" in mizaj_lower:
            humor = "Balgham (Phlegm)"
        elif "safra" in mizaj_lower:
            humor = "Safra (Yellow Bile)"
        elif "sawda" in mizaj_lower:
            humor = "Sawda (Black Bile)"
        elif "dam" in mizaj_lower:
            humor = "Dam (Blood)"

        return ClinicalPhenotypeProfile(
            condition_name=condition,
            primary_mizaj=mizaj,
            dominant_organ_axis=dominant_axis,
            phenotype_code=f"PHENO-GEN-{condition[:4].upper()}-{humor[:3].upper()}",
            phenotype_name=f"{condition} ({humor}-dominant Constitutional Phenotype)",
            temperament_qualities={"mizaj_assessment": mizaj},
            pathological_humor=humor,
            suggested_line_of_treatment=f"Tadil-e-Mizaj targeting {humor} with organ-support for {dominant_axis}",
            contraindicated_categories=["Contradictory thermal medicines"],
            biomarker_patterns=biomarkers or {}
        )

    def evaluate_response(
        self,
        patient_id: str,
        vas_baseline: float,
        vas_followup: float,
        adherence_pct: float,
        adverse_events: Optional[List[Any]] = None,
        biomarker_deltas: Optional[List[Dict[str, Any]]] = None
    ) -> ResponseEvaluation:
        """
        Evaluates clinical response into 5 canonical tiers:
        RESPONDER, PARTIAL_RESPONDER, NON_RESPONDER, INTOLERANT, ADHERENT_NON_RESPONDER.
        """
        adverse_events = adverse_events or []
        biomarker_deltas = biomarker_deltas or []

        # Calculate VAS improvement percentage
        if vas_baseline <= 0:
            vas_improvement_pct = 0.0
        else:
            delta = vas_baseline - vas_followup
            vas_improvement_pct = round(max(0.0, (delta / vas_baseline) * 100.0), 2)

        # Biomarker improvement score (0.0 to 1.0)
        improved_count = 0
        total_markers = len(biomarker_deltas)
        if total_markers > 0:
            for b in biomarker_deltas:
                # If improvement flag is present or delta is favourable
                if b.get("is_improved", False) or b.get("percentage_change", 0) < 0:
                    improved_count += 1
            biomarker_score = round(improved_count / total_markers, 2)
        else:
            biomarker_score = 0.5  # Neutral default when no biomarkers logged

        # Tier Evaluation Logic
        has_severe_adverse = any(ae.get("severity") in ("SEVERE", "LIFE_THREATENING") for ae in adverse_events if isinstance(ae, dict))
        has_adverse = len(adverse_events) > 0

        tier: ResponseClassificationTier
        switch_recommended = False
        recommendation = ""

        if has_severe_adverse or (has_adverse and vas_improvement_pct < 20.0):
            tier = ResponseClassificationTier.INTOLERANT
            switch_recommended = True
            recommendation = "DISCONTINUE CURRENT PROTOCOL IMMEDIATELY: Intolerance / Adverse event detected. Switch to safe Badal-e-Advia substitute."
        elif adherence_pct >= 80.0 and vas_improvement_pct < 15.0:
            tier = ResponseClassificationTier.ADHERENT_NON_RESPONDER
            switch_recommended = True
            recommendation = "FLAG: ADHERENT NON-RESPONDER. Patient maintained ≥80% adherence with <15% symptom relief. Autonomous second-line review requested; trigger Badal-e-Advia & clinical panel review."
        elif vas_improvement_pct >= 75.0 and biomarker_score >= 0.5:
            tier = ResponseClassificationTier.RESPONDER
            switch_recommended = False
            recommendation = "EXCELLENT RESPONSE: Maintain current dosage or begin gradual taper to maintenance (Tafawut-e-Jar'at)."
        elif vas_improvement_pct >= 40.0:
            tier = ResponseClassificationTier.PARTIAL_RESPONDER
            switch_recommended = False
            recommendation = "PARTIAL RESPONSE: Continue protocol with lifestyle (Asbab-e-Sittah) optimization and follow-up in 14 days."
        else:
            tier = ResponseClassificationTier.NON_RESPONDER
            if adherence_pct < 60.0:
                recommendation = f"SUB-OPTIMAL ADHERENCE ({adherence_pct}%): Address posology compliance and patient education before changing prescription."
            else:
                recommendation = "NON-RESPONDER: Minimal symptom improvement. Re-assess 10-Ajnas Mizaj for sub-phenotype misclassification."

        return ResponseEvaluation(
            patient_id=patient_id,
            tier=tier,
            vas_baseline=vas_baseline,
            vas_followup=vas_followup,
            vas_improvement_pct=vas_improvement_pct,
            adherence_pct=adherence_pct,
            adverse_events_count=len(adverse_events),
            biomarker_improvement_score=biomarker_score,
            protocol_switch_recommended=switch_recommended,
            clinical_recommendation=recommendation
        )
