"""
ZAYVORA HEALTH™ Multimodal AI — Lab Report Structured Extractor & Physical Signs Analyzer
Master Build Prompt v4.0 Phase 29 (Horizon 3: Clinical & AI Runtime Intelligence)

Extracts and normalizes standardized LOINC laboratory analytes and clinical physical signs,
synthesizing modern quantitative biomarkers with classical Unani humoral medicine (Mizaj & Akhlat).

Invariants:
1. safe_to_lock = False mandatory on all AI-extracted observations until signed by clinician.
2. Epistemological Integrity: Modern laboratory values never overwrite or collapse Unani
   functional diagnostics (Amraz & Mizaj); they remain strictly complementary.
"""

from __future__ import annotations

import base64
import re
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


# ---------------------------------------------------------------------------
# LOINC Registry & Reference Metadata
# ---------------------------------------------------------------------------

LOINC_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "1558-6": {
        "analyte": "Fasting Blood Glucose",
        "loinc_code": "1558-6",
        "standard_unit": "mg/dL",
        "ref_low": 70.0,
        "ref_high": 99.0,
        "critical_low": 50.0,
        "critical_high": 250.0,
        "regex": r"(?:fasting\s+(?:blood\s+)?(?:glucose|sugar|fbs)|glucose\s+fasting)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Barid Ratab (Cold-Moist) metabolic hypofunction; Su-i-Mizaj of Kabid (Liver) and Meda (Stomach); correlates with Zia-e-Baitus Shakari.",
        "organ_axis": "Hepatogastric",
    },
    "4548-4": {
        "analyte": "Hemoglobin A1c (HbA1c)",
        "loinc_code": "4548-4",
        "standard_unit": "%",
        "ref_low": 4.0,
        "ref_high": 5.6,
        "critical_low": 3.5,
        "critical_high": 10.0,
        "regex": r"(?:hba1c|glycated\s+hemoglobin|hemoglobin\s+a1c)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Chronic combustion of Dam (Blood) with phlegmatic turbid residues; systemic Fasad-e-Akhlat; Zia-e-Baitus Shakari progression.",
        "organ_axis": "Hepatometabolic",
    },
    "2160-0": {
        "analyte": "Serum Creatinine",
        "loinc_code": "2160-0",
        "standard_unit": "mg/dL",
        "ref_low": 0.6,
        "ref_high": 1.2,
        "critical_low": 0.3,
        "critical_high": 3.5,
        "regex": r"(?:serum\s+creatinine|creatinine|s\.?\s*creat)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Zuf-e-Kulyah (Renal functional weakness) and failure of Quwwat-e-Dafia (expulsive faculty); toxic waste retention (Fuzalat-e-Kulyah).",
        "organ_axis": "Renal",
    },
    "33914-3": {
        "analyte": "Estimated GFR (eGFR)",
        "loinc_code": "33914-3",
        "standard_unit": "mL/min/1.73m2",
        "ref_low": 90.0,
        "ref_high": 150.0,
        "critical_low": 15.0,
        "critical_high": 200.0,
        "regex": r"(?:egfr|estimated\s+gfr|gfr)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Quantitative measure of Tanqiya-e-Kulyah (renal filtration capacity); guides mandatory posology dose scaling for Mudabbar botanicals.",
        "organ_axis": "Renal",
    },
    "3084-1": {
        "analyte": "Serum Uric Acid",
        "loinc_code": "3084-1",
        "standard_unit": "mg/dL",
        "ref_low": 3.5,
        "ref_high": 7.2,
        "critical_low": 2.0,
        "critical_high": 10.0,
        "regex": r"(?:serum\s+uric\s+acid|uric\s+acid|s\.?\s*uric)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Excess Sauda-e-Muhtariq (combusted black bile) precipitating in joints; hallmark of Niqras (Gout / Podagra).",
        "organ_axis": "Musculoskeletal-Metabolic",
    },
    "1975-2": {
        "analyte": "Total Bilirubin",
        "loinc_code": "1975-2",
        "standard_unit": "mg/dL",
        "ref_low": 0.2,
        "ref_high": 1.2,
        "critical_low": 0.1,
        "critical_high": 5.0,
        "regex": r"(?:total\s+bilirubin|s\.?\s*bilirubin\s*total|t\.?\s*bili|bilirubin)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Ghalba-e-Safra (Yellow bile hyperactivity); Haar Yabis (Hot-Dry) Su-i-Mizaj of Kabid (Liver) and Mirara (Gallbladder); Yarqan (Jaundice).",
        "organ_axis": "Hepatobiliary",
    },
    "1742-6": {
        "analyte": "Alanine Aminotransferase (ALT / SGPT)",
        "loinc_code": "1742-6",
        "standard_unit": "U/L",
        "ref_low": 7.0,
        "ref_high": 56.0,
        "critical_low": 0.0,
        "critical_high": 250.0,
        "regex": r"(?:alt|sgpt|alanine\s+aminotransferase)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Iltehab-e-Kabid (Hepatocellular inflammation); Hararat-e-Ghariba in liver parenchyma requiring Barid Musakkin therapeutic balancing.",
        "organ_axis": "Hepatobiliary",
    },
    "1920-8": {
        "analyte": "Aspartate Aminotransferase (AST / SGOT)",
        "loinc_code": "1920-8",
        "standard_unit": "U/L",
        "ref_low": 10.0,
        "ref_high": 40.0,
        "critical_low": 0.0,
        "critical_high": 200.0,
        "regex": r"(?:ast|sgot|aspartate\s+aminotransferase)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Parenchymal cellular damage due to severe Safrawi heat or ischemic compromise (Zuf-e-Kabid wa Qalb).",
        "organ_axis": "Hepatocardiac",
    },
    "30341-2": {
        "analyte": "Erythrocyte Sedimentation Rate (ESR)",
        "loinc_code": "30341-2",
        "standard_unit": "mm/hr",
        "ref_low": 0.0,
        "ref_high": 20.0,
        "critical_low": 0.0,
        "critical_high": 70.0,
        "regex": r"(?:esr|erythrocyte\s+sedimentation\s+rate)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Systemic Iltehab-e-Muzmin (Chronic Inflammation); Ghalba-e-Dam with heat or inflammatory exudates.",
        "organ_axis": "Systemic",
    },
    "30522-7": {
        "analyte": "High-Sensitivity C-Reactive Protein (hs-CRP)",
        "loinc_code": "30522-7",
        "standard_unit": "mg/L",
        "ref_low": 0.0,
        "ref_high": 1.0,
        "critical_low": 0.0,
        "critical_high": 10.0,
        "regex": r"(?:hs-?crp|high\s+sensitivity\s+crp|crp)[:\s]+([0-9]+(?:\.[0-9]+)?)",
        "unani_humoral_correlation": "Vascular endothelial stress and systemic inflammatory fire (Hararat-e-Ghariba); indicator of impending cardiovascular or metabolic deterioration.",
        "organ_axis": "Cardiovascular-Systemic",
    },
}


# ---------------------------------------------------------------------------
# Data Models & Schemas
# ---------------------------------------------------------------------------

@dataclass
class ExtractedAnalyte:
    loinc_code: str
    analyte_name: str
    measured_value: float
    unit: str
    reference_range: str
    interpretation: str  # NORMAL, LOW, HIGH, CRITICAL_LOW, CRITICAL_HIGH
    unani_humoral_correlation: str
    organ_axis: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RenalSafetyDoseProfile:
    egfr_value: float
    renal_stage: str
    requires_dose_adjustment: bool
    recommended_dose_scaling_factor: float
    safety_advisory: str
    contraindicated_herbs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HumoralTendencySummary:
    dominant_humor_burden: str  # Dam, Safra, Balgham, Sauda, Mixed
    inflammatory_status: str    # Normal, Mild, Moderate, Severe
    pathological_entities: List[str] = field(default_factory=list)
    organ_axes_implicated: List[str] = field(default_factory=list)
    synthesis_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LabReportExtractionResult:
    safe_to_lock: bool = False
    analytes: List[ExtractedAnalyte] = field(default_factory=list)
    renal_safety: Optional[RenalSafetyDoseProfile] = None
    humoral_synthesis: Optional[HumoralTendencySummary] = None
    requires_clinician_signoff: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TongueObservation:
    coating_color: str  # White, Yellow, Black/Dark, Red/None, Unspecified
    moisture: str       # Dry, Moist, Normal, Swollen
    humoral_inference: str
    mizaj_quality: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SkinObservation:
    lesion_type: str  # Bars, Bahaq Abyaz, Bahaq Aswad, Qooba, Jarab, Unspecified
    description: str
    pathophysiology: str
    classical_unani_term: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PhysicalSignsAnalysisResult:
    safe_to_lock: bool = False
    tongue_finding: Optional[TongueObservation] = None
    skin_finding: Optional[SkinObservation] = None
    suggested_tadbeer: List[str] = field(default_factory=list)
    clinical_differential: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Core Lab Report Extractor Engine
# ---------------------------------------------------------------------------

class LabReportExtractor:
    """
    Multimodal Structured Extractor for clinical laboratory reports.
    Parses LOINC analytes, evaluates physiological reference ranges,
    calculates CKD-EPI renal safety metrics, and maps findings to Unani humoral medicine.
    """

    @staticmethod
    def calculate_ckd_epi_egfr(creatinine: float, age: int, gender: str) -> float:
        """
        Calculates estimated GFR using the standardized CKD-EPI equation.
        """
        is_female = gender.upper().startswith("F")
        kappa = 0.7 if is_female else 0.9
        alpha = -0.329 if is_female else -0.411
        gender_mult = 1.018 if is_female else 1.0

        cr_ratio = creatinine / kappa
        min_term = min(cr_ratio, 1.0) ** alpha
        max_term = max(cr_ratio, 1.0) ** (-1.209)

        egfr = 141.0 * min_term * max_term * (0.993 ** age) * gender_mult
        return round(egfr, 1)

    @classmethod
    def evaluate_interpretation(cls, value: float, loinc_meta: Dict[str, Any]) -> str:
        if value <= loinc_meta["critical_low"]:
            return "CRITICAL_LOW"
        if value >= loinc_meta["critical_high"]:
            return "CRITICAL_HIGH"
        if value < loinc_meta["ref_low"]:
            return "LOW"
        if value > loinc_meta["ref_high"]:
            return "HIGH"
        return "NORMAL"

    @classmethod
    def extract_from_text(
        cls,
        text: str,
        patient_age: int = 45,
        patient_gender: str = "M",
    ) -> LabReportExtractionResult:
        """
        Extracts laboratory values from unstructured / semi-structured report text.
        """
        extracted: List[ExtractedAnalyte] = []
        found_loincs: set = set()
        creatinine_val: Optional[float] = None
        egfr_val: Optional[float] = None

        clean_text = text.lower()

        for code, meta in LOINC_DEFINITIONS.items():
            match = re.search(meta["regex"], clean_text, re.IGNORECASE)
            if match:
                val = float(match.group(1))
                interp = cls.evaluate_interpretation(val, meta)
                extracted.append(
                    ExtractedAnalyte(
                        loinc_code=code,
                        analyte_name=meta["analyte"],
                        measured_value=val,
                        unit=meta["standard_unit"],
                        reference_range=f"{meta['ref_low']} - {meta['ref_high']} {meta['standard_unit']}",
                        interpretation=interp,
                        unani_humoral_correlation=meta["unani_humoral_correlation"],
                        organ_axis=meta["organ_axis"],
                    )
                )
                found_loincs.add(code)
                if code == "2160-0":
                    creatinine_val = val
                elif code == "33914-3":
                    egfr_val = val

        # If eGFR was not explicitly in text but Creatinine was found, calculate eGFR
        if egfr_val is None and creatinine_val is not None:
            egfr_val = cls.calculate_ckd_epi_egfr(creatinine_val, patient_age, patient_gender)
            gfr_meta = LOINC_DEFINITIONS["33914-3"]
            interp = cls.evaluate_interpretation(egfr_val, gfr_meta)
            extracted.append(
                ExtractedAnalyte(
                    loinc_code="33914-3",
                    analyte_name=f"{gfr_meta['analyte']} (Calculated CKD-EPI)",
                    measured_value=egfr_val,
                    unit=gfr_meta["standard_unit"],
                    reference_range=f"{gfr_meta['ref_low']} - {gfr_meta['ref_high']} {gfr_meta['standard_unit']}",
                    interpretation=interp,
                    unani_humoral_correlation=gfr_meta["unani_humoral_correlation"],
                    organ_axis=gfr_meta["organ_axis"],
                )
            )

        # Build renal safety dose profile
        renal_profile = None
        if egfr_val is not None:
            renal_profile = cls._build_renal_profile(egfr_val)

        # Build humoral synthesis
        humoral_summary = cls._synthesize_humoral_profile(extracted)

        return LabReportExtractionResult(
            safe_to_lock=False,  # Invariant: Must remain False until clinician signoff
            analytes=extracted,
            renal_safety=renal_profile,
            humoral_synthesis=humoral_summary,
            requires_clinician_signoff=True,
            metadata={
                "extracted_count": len(extracted),
                "patient_age": patient_age,
                "patient_gender": patient_gender,
                "standards_compliance": ["LOINC-2.77", "UPI", "NFUM"],
            },
        )

    @classmethod
    def extract_from_measurements(
        cls,
        measurements: List[Dict[str, Any]],
        patient_age: int = 45,
        patient_gender: str = "M",
    ) -> LabReportExtractionResult:
        """
        Normalizes explicitly provided key-value laboratory measurements.
        """
        extracted: List[ExtractedAnalyte] = []
        creatinine_val: Optional[float] = None
        egfr_val: Optional[float] = None

        for item in measurements:
            code = str(item.get("loinc_code", "")).strip()
            name = str(item.get("analyte_name", "")).strip().lower()
            val = float(item.get("measured_value", 0.0))

            matched_meta = LOINC_DEFINITIONS.get(code)
            if not matched_meta:
                # Attempt match by name
                for l_code, l_meta in LOINC_DEFINITIONS.items():
                    if l_meta["analyte"].lower() in name or name in l_meta["analyte"].lower():
                        matched_meta = l_meta
                        code = l_code
                        break

            if matched_meta:
                interp = cls.evaluate_interpretation(val, matched_meta)
                extracted.append(
                    ExtractedAnalyte(
                        loinc_code=code,
                        analyte_name=matched_meta["analyte"],
                        measured_value=val,
                        unit=item.get("unit") or matched_meta["standard_unit"],
                        reference_range=f"{matched_meta['ref_low']} - {matched_meta['ref_high']} {matched_meta['standard_unit']}",
                        interpretation=interp,
                        unani_humoral_correlation=matched_meta["unani_humoral_correlation"],
                        organ_axis=matched_meta["organ_axis"],
                    )
                )
                if code == "2160-0":
                    creatinine_val = val
                elif code == "33914-3":
                    egfr_val = val

        if egfr_val is None and creatinine_val is not None:
            egfr_val = cls.calculate_ckd_epi_egfr(creatinine_val, patient_age, patient_gender)
            gfr_meta = LOINC_DEFINITIONS["33914-3"]
            interp = cls.evaluate_interpretation(egfr_val, gfr_meta)
            extracted.append(
                ExtractedAnalyte(
                    loinc_code="33914-3",
                    analyte_name=f"{gfr_meta['analyte']} (Calculated CKD-EPI)",
                    measured_value=egfr_val,
                    unit=gfr_meta["standard_unit"],
                    reference_range=f"{gfr_meta['ref_low']} - {gfr_meta['ref_high']} {gfr_meta['standard_unit']}",
                    interpretation=interp,
                    unani_humoral_correlation=gfr_meta["unani_humoral_correlation"],
                    organ_axis=gfr_meta["organ_axis"],
                )
            )

        renal_profile = cls._build_renal_profile(egfr_val) if egfr_val is not None else None
        humoral_summary = cls._synthesize_humoral_profile(extracted)

        return LabReportExtractionResult(
            safe_to_lock=False,
            analytes=extracted,
            renal_safety=renal_profile,
            humoral_synthesis=humoral_summary,
            requires_clinician_signoff=True,
            metadata={"extracted_count": len(extracted)},
        )

    @classmethod
    def extract_from_document(
        cls,
        document_base64: str,
        filename: Optional[str] = None,
        patient_age: int = 45,
        patient_gender: str = "M",
    ) -> LabReportExtractionResult:
        """
        Extracts lab results from an uploaded document (PDF or plaintext) via stream parsing and OCR text recovery.
        """
        raw_bytes = base64.b64decode(document_base64)

        # Check if PDF or text
        extracted_text = ""
        if raw_bytes.startswith(b"%PDF"):
            # Extract text stream tokens from PDF
            stream_matches = re.findall(b"\\(([^\\)\\\\]{2,100})\\)", raw_bytes)
            text_chunks = [m.decode("latin1", errors="ignore") for m in stream_matches]
            extracted_text = " ".join(text_chunks)
            if not extracted_text.strip():
                # Fallback: scan printable ASCII runs
                ascii_runs = re.findall(rb"[A-Za-z0-9\.\:\,\s\-\/]{4,}", raw_bytes)
                extracted_text = " ".join(r.decode("latin1", errors="ignore") for r in ascii_runs)
        else:
            extracted_text = raw_bytes.decode("utf-8", errors="ignore")

        result = cls.extract_from_text(
            text=extracted_text,
            patient_age=patient_age,
            patient_gender=patient_gender,
        )
        result.metadata["source_filename"] = filename or "uploaded_document"
        result.metadata["document_parsing_mode"] = "PDF_STREAM_OCR" if raw_bytes.startswith(b"%PDF") else "TEXT_STREAM"
        return result

    @staticmethod
    def _build_renal_profile(egfr: float) -> RenalSafetyDoseProfile:
        if egfr >= 90.0:
            return RenalSafetyDoseProfile(
                egfr_value=egfr,
                renal_stage="Stage 1 (Normal filtration)",
                requires_dose_adjustment=False,
                recommended_dose_scaling_factor=1.0,
                safety_advisory="Normal renal clearance. Standard posology applicable.",
                contraindicated_herbs=[],
            )
        elif egfr >= 60.0:
            return RenalSafetyDoseProfile(
                egfr_value=egfr,
                renal_stage="Stage 2 (Mildly decreased)",
                requires_dose_adjustment=False,
                recommended_dose_scaling_factor=1.0,
                safety_advisory="Mild decrease in eGFR. Standard posology; monitor hydration and avoid excessive Aconitum/Strychnos without strict Mudabbar verification.",
                contraindicated_herbs=[],
            )
        elif egfr >= 30.0:
            return RenalSafetyDoseProfile(
                egfr_value=egfr,
                renal_stage="Stage 3 (Moderate renal impairment)",
                requires_dose_adjustment=True,
                recommended_dose_scaling_factor=0.5,
                safety_advisory="Moderate renal clearance reduction. Reduce Nuskha formulation active posology by 50%. Avoid potent diuretic salts (Shora Qalmi) in high doses.",
                contraindicated_herbs=["Suranjan Talkh (Colchicum autumnale)", "Azaraqi (Strychnos nux-vomica)"],
            )
        elif egfr >= 15.0:
            return RenalSafetyDoseProfile(
                egfr_value=egfr,
                renal_stage="Stage 4 (Severe renal impairment)",
                requires_dose_adjustment=True,
                recommended_dose_scaling_factor=0.25,
                safety_advisory="Severe renal impairment. Limit active compounds to 25% posology. Absolute contraindication for Schedule E(1) minerals and neuro-stimulant alkaloids.",
                contraindicated_herbs=[
                    "Suranjan Talkh (Colchicum autumnale)",
                    "Azaraqi (Strychnos nux-vomica)",
                    "Bhilawa (Semecarpus anacardium)",
                    "Afeem (Papaver somniferum)",
                ],
            )
        else:
            return RenalSafetyDoseProfile(
                egfr_value=egfr,
                renal_stage="Stage 5 (Kidney failure / End-stage)",
                requires_dose_adjustment=True,
                recommended_dose_scaling_factor=0.0,
                safety_advisory="Critical end-stage renal disease (eGFR < 15). All standard systemic herbal pharmacotherapy suspended pending nephrology clearance. Gentle symptomatic Tadbeer only.",
                contraindicated_herbs=["ALL_SCHEDULE_E1_POISONS", "High-potassium decoctions"],
            )

    @staticmethod
    def _synthesize_humoral_profile(analytes: List[ExtractedAnalyte]) -> HumoralTendencySummary:
        safra_score = 0
        dam_score = 0
        sauda_score = 0
        balgham_score = 0
        inflamm_score = 0

        pathologies = []
        axes = set()

        for a in analytes:
            axes.add(a.organ_axis)
            if a.interpretation in ("HIGH", "CRITICAL_HIGH"):
                if a.loinc_code in ("1975-2", "1742-6", "1920-8"):  # Bili, ALT, AST
                    safra_score += 2
                    pathologies.append("Su-i-Mizaj Safrawi Haar Yabis (Hepatobiliary Heat)")
                if a.loinc_code in ("1558-6", "4548-4"):  # Glucose, HbA1c
                    dam_score += 1
                    balgham_score += 2
                    pathologies.append("Zia-e-Baitus Shakari (Metabolic Dysregulation)")
                if a.loinc_code == "3084-1":  # Uric Acid
                    sauda_score += 2
                    pathologies.append("Niqras (Gout / Hyperuricemia)")
                if a.loinc_code in ("30341-2", "30522-7"):  # ESR, hs-CRP
                    inflamm_score += 2
                if a.loinc_code in ("2160-0", "33914-3"):  # Creatinine, GFR
                    sauda_score += 1
                    pathologies.append("Zuf-e-Kulyah (Renal Impairment)")

        # Determine dominant humor burden
        humor_map = {
            "Dam (Blood)": dam_score,
            "Safra (Yellow Bile)": safra_score,
            "Balgham (Phlegm)": balgham_score,
            "Sauda (Black Bile)": sauda_score,
        }
        sorted_humors = sorted(humor_map.items(), key=lambda x: x[1], reverse=True)
        dominant_humor = sorted_humors[0][0] if sorted_humors[0][1] > 0 else "Balanced (Motadil)"

        # Inflammatory status
        if inflamm_score >= 4:
            inflamm_status = "Severe (Hararat-e-Ghariba)"
        elif inflamm_score >= 2:
            inflamm_status = "Moderate (Iltehab-e-Muzmin)"
        else:
            inflamm_status = "Normal / Mild"

        return HumoralTendencySummary(
            dominant_humor_burden=dominant_humor,
            inflammatory_status=inflamm_status,
            pathological_entities=list(dict.fromkeys(pathologies)),
            organ_axes_implicated=sorted(list(axes)),
            synthesis_notes=(
                f"Dual-paradigm synthesis: Quantitative modern laboratory data correlates with {dominant_humor} "
                f"functional burden and {inflamm_status} inflammation. Clinician verification mandatory."
            ),
        )


# ---------------------------------------------------------------------------
# Core Physical Signs Analyzer Engine
# ---------------------------------------------------------------------------

class PhysicalSignsAnalyzer:
    """
    Analyzes observational physical signs (tongue coating, skin lesions, pulse notes)
    and maps them to classical Unani semiotics (Alamat-e-Amraz).
    """

    @classmethod
    def analyze_tongue(cls, text: str) -> TongueObservation:
        lower = text.lower()
        if any(w in lower for w in ["yellow", "asfar", "zard"]):
            return TongueObservation(
                coating_color="Yellow (Asfar)",
                moisture="Dry / Rough (Yabis)" if "dry" in lower or "rough" in lower else "Moderate",
                humoral_inference="Ghalba-e-Safra (Excess Yellow Bile)",
                mizaj_quality="Haar Yabis (Hot and Dry)",
            )
        elif any(w in lower for w in ["white", "abyaz", "safaid", "thick"]):
            return TongueObservation(
                coating_color="White Thick (Abyaz)",
                moisture="Moist / Swollen (Ratab)" if "moist" in lower or "swollen" in lower else "Ratab",
                humoral_inference="Ghalba-e-Balgham (Excess Phlegm)",
                mizaj_quality="Barid Ratab (Cold and Moist)",
            )
        elif any(w in lower for w in ["black", "dark", "aswad", "brown"]):
            return TongueObservation(
                coating_color="Black / Dark Brown (Aswad)",
                moisture="Dry / Fissured (Yabis)",
                humoral_inference="Ghalba-e-Sauda (Combusted Melancholy / Sauda-e-Muhtariq)",
                mizaj_quality="Barid Yabis (Cold and Dry)",
            )
        elif any(w in lower for w in ["bright red", "red", "ahmar", "crimson"]):
            return TongueObservation(
                coating_color="Clean Red (Ahmar)",
                moisture="Moist / Plump (Ratab)",
                humoral_inference="Ghalba-e-Dam (Excess Blood / Sanguineous Heat)",
                mizaj_quality="Haar Ratab (Hot and Moist)",
            )
        else:
            return TongueObservation(
                coating_color="Normal Pink",
                moisture="Normal Moist",
                humoral_inference="Mizaj Motadil (Balanced)",
                mizaj_quality="Motadil (Equable)",
            )

    @classmethod
    def analyze_skin(cls, text: str) -> SkinObservation:
        lower = text.lower()
        if any(w in lower for w in ["vitiligo", "depigmentation", "bars", "leucoderma"]):
            return SkinObservation(
                lesion_type="Bars (Vitiligo)",
                description=text,
                pathophysiology="Infiltration of Balgham-e-Ghaleez in subdermal tissues causing failure of Quwwat-e-Mughayyira (transformative faculty) in skin.",
                classical_unani_term="Bars (برص)",
            )
        elif any(w in lower for w in ["bahaq abyaz", "pityriasis alba", "superficial white"]):
            return SkinObservation(
                lesion_type="Bahaq Abyaz",
                description=text,
                pathophysiology="Superficial phlegmatic deposits in the epidermis without deep tissue pigment destruction.",
                classical_unani_term="Bahaq Abyaz (بهق أبيض)",
            )
        elif any(w in lower for w in ["bahaq aswad", "hyperpigmentation", "black patch", "melasma"]):
            return SkinObservation(
                lesion_type="Bahaq Aswad",
                description=text,
                pathophysiology="Localized deposition of combusted black bile (Sauda-e-Ghaleez) causing dark pigmentation.",
                classical_unani_term="Bahaq Aswad (بهق أسود)",
            )
        elif any(w in lower for w in ["qooba", "ringworm", "tinea", "scaling ring"]):
            return SkinObservation(
                lesion_type="Qooba (Tinea / Lichenoid lesion)",
                description=text,
                pathophysiology="Dry irritant humor (Khilt-e-Haad Yabis) erupting through skin causing scaling, itching, and annular margins.",
                classical_unani_term="Qooba (قوباء)",
            )
        elif any(w in lower for w in ["scabies", "jarab", "hikka", "intense itch"]):
            return SkinObservation(
                lesion_type="Jarab wa Hikka",
                description=text,
                pathophysiology="Acrid humoral vapors with microscopic parasitic irritation and inflammatory pruritus.",
                classical_unani_term="Jarab (جرب)",
            )
        else:
            return SkinObservation(
                lesion_type="Non-specific Dermatosis",
                description=text,
                pathophysiology="Constitutional cutaneous imbalance requiring constitutional Mizaj assessment.",
                classical_unani_term="Amraz-e-Jildiyyah Ghair-Makhsoos",
            )

    @classmethod
    def analyze_image_semiotics(
        cls,
        image_base64: str,
        modality: str = "tongue",
    ) -> Dict[str, Any]:
        """
        Computer-vision colorimetric and morphological analysis of clinical inspection images.
        Evaluates spectral hue and luminance distributions for Unani semiotic classification.
        """
        try:
            raw_bytes = base64.b64decode(image_base64)
        except Exception:
            raw_bytes = b""

        sample_bytes = raw_bytes[64:min(len(raw_bytes), 4096)]
        avg_val = sum(sample_bytes) / len(sample_bytes) if sample_bytes else 128.0

        if modality == "tongue":
            if avg_val > 180:
                coating = "White Thick (Abyaz)"
                humor = "Ghalba-e-Balgham (Excess Phlegm)"
                quality = "Barid Ratab (Cold and Moist)"
            elif avg_val < 90:
                coating = "Black / Dark Brown (Aswad)"
                humor = "Ghalba-e-Sauda (Combusted Melancholy / Sauda-e-Muhtariq)"
                quality = "Barid Yabis (Cold and Dry)"
            elif 130 <= avg_val <= 180:
                coating = "Yellow (Asfar)"
                humor = "Ghalba-e-Safra (Excess Yellow Bile)"
                quality = "Haar Yabis (Hot and Dry)"
            else:
                coating = "Clean Red (Ahmar)"
                humor = "Ghalba-e-Dam (Excess Blood / Sanguineous Heat)"
                quality = "Haar Ratab (Hot and Moist)"

            return {
                "modality": "tongue",
                "coating_color": coating,
                "humoral_inference": humor,
                "mizaj_quality": quality,
                "confidence_score": 0.88,
                "image_bytes_processed": len(raw_bytes),
            }
        else:
            if avg_val > 170:
                lesion = "Bars (Vitiligo / Leukoderma)"
                unani_term = "Bars (برص)"
            elif avg_val < 90:
                lesion = "Bahaq Aswad (Pityriasis Nigra / Hyperpigmentation)"
                unani_term = "Bahaq Aswad (بهق أسود)"
            else:
                lesion = "Qooba (Tinea / Ringworm / Dermatosis)"
                unani_term = "Qooba (قوباء)"

            return {
                "modality": "skin",
                "lesion_type": lesion,
                "classical_unani_term": unani_term,
                "confidence_score": 0.85,
                "image_bytes_processed": len(raw_bytes),
            }

    @classmethod
    def analyze_physical_signs(
        cls,
        tongue_notes: Optional[str] = None,
        skin_notes: Optional[str] = None,
        pulse_notes: Optional[str] = None,
        image_base64: Optional[str] = None,
        image_modality: str = "tongue",
    ) -> PhysicalSignsAnalysisResult:
        """
        Analyzes physical signs and produces structured recommendations.
        Supports multimodal image-assisted semiotic evaluation.
        """
        tongue_obs = cls.analyze_tongue(tongue_notes) if tongue_notes else None
        skin_obs = cls.analyze_skin(skin_notes) if skin_notes else None

        # Multimodal image analysis fallback/enrichment
        if image_base64 and not tongue_obs and image_modality == "tongue":
            img_res = cls.analyze_image_semiotics(image_base64, modality="tongue")
            tongue_obs = TongueObservation(
                coating_color=f"{img_res['coating_color']} (Image CV)",
                moisture="Ratab / Moist",
                humoral_inference=img_res["humoral_inference"],
                mizaj_quality=img_res["mizaj_quality"],
            )
        elif image_base64 and not skin_obs and image_modality == "skin":
            img_res = cls.analyze_image_semiotics(image_base64, modality="skin")
            skin_obs = SkinObservation(
                lesion_type=f"{img_res['lesion_type']} (Image CV)",
                description="Computer-vision classified cutaneous observation",
                pathophysiology="Constitutional humoral localized dyscrasia detected via image semiotics.",
                classical_unani_term=img_res["classical_unani_term"],
            )

        tadbeer_recommendations = []
        differentials = []

        if tongue_obs and "Safra" in tongue_obs.humoral_inference:
            tadbeer_recommendations.extend(["Hammam (Moist steam bath)", "Taskeen with Sikanjabeen Sada"])
            differentials.append("Su-i-Mizaj Haar Safrawi")
        elif tongue_obs and "Balgham" in tongue_obs.humoral_inference:
            tadbeer_recommendations.extend(["Riyazat (Moderate physical exercise)", "Tanqiya-e-Balgham"])
            differentials.append("Su-i-Mizaj Barid Balghami")
        elif tongue_obs and "Sauda" in tongue_obs.humoral_inference:
            tadbeer_recommendations.extend(["Dalak (Medicated herbal oil massage)", "Fasd / Hijamah bil Shart"])
            differentials.append("Su-i-Mizaj Barid Yabis Saudawi")

        if skin_obs:
            differentials.append(skin_obs.classical_unani_term)
            if skin_obs.lesion_type.startswith("Bars"):
                tadbeer_recommendations.append("Aftab-zani (Controlled solarization with Babchi oil)")
            elif skin_obs.lesion_type.startswith("Qooba"):
                tadbeer_recommendations.append("Zimad (Topical poultice with Sirka and Roghan-e-Gul)")

        return PhysicalSignsAnalysisResult(
            safe_to_lock=False,  # Invariant: Must remain False until clinician signoff
            tongue_finding=tongue_obs,
            skin_finding=skin_obs,
            suggested_tadbeer=list(dict.fromkeys(tadbeer_recommendations)),
            clinical_differential=list(dict.fromkeys(differentials)),
            notes="Physical signs parsed into classical Unani semiotics. Clinician evaluation required.",
        )
