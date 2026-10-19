"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 4A: Manufacturing + QC Intelligence Engine
System: ZAYVORA Health OS™
Doctrine: Raw Material -> Lot -> Extraction Parameters -> Physical Batch -> Chemical Fingerprint -> QC Outlier Detection -> Release Gate
"""

import math
import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class BatchReleaseStatus(str, Enum):
    QUARANTINE = "QUARANTINE"
    QC_PASSED = "QC_PASSED"
    QC_REJECTED = "QC_REJECTED"
    RELEASED = "RELEASED"


@dataclass
class ChemicalPeak:
    retention_time_min: float
    compound_name: str
    peak_area: float
    relative_abundance_pct: float


@dataclass
class BatchManufacturingDossier:
    batch_id: str
    batch_number: str
    formulation_id: str
    formulation_version: str
    raw_material_lot_ids: List[str]
    supplier_name: str
    extraction_solvent: str
    extraction_temp_celsius: float
    extraction_duration_hours: float
    mfg_date: str
    exp_date: str
    chromatogram_peaks: List[ChemicalPeak]
    fingerprint_hash: str
    similarity_to_golden_standard: float
    outlier_flag: bool = False
    status: BatchReleaseStatus = BatchReleaseStatus.QUARANTINE
    qc_notes: str = ""
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class BatchQCIntelligenceEngine:
    """Evaluates physical batch quality, spectral similarity, and anomaly detection."""

    _DOSSIER_REGISTRY: Dict[str, BatchManufacturingDossier] = {}

    # Golden Reference Fingerprint for Majun Suranjan (v1.1)
    _GOLDEN_PEAKS = [
        {"compound": "Colchicine", "rt": 4.12, "abundance": 28.5},
        {"compound": "Piperine", "rt": 7.45, "abundance": 34.2},
        {"compound": "Guggulsterone_E", "rt": 11.20, "abundance": 18.0}
    ]

    @classmethod
    def register_and_evaluate_batch(
        cls,
        batch_id: str,
        batch_number: str,
        formulation_id: str,
        formulation_version: str,
        raw_material_lots: List[str],
        supplier_name: str,
        solvent: str,
        temp_c: float,
        duration_h: float,
        mfg_date: str,
        exp_date: str,
        measured_peaks: List[Dict[str, Any]]
    ) -> BatchManufacturingDossier:
        """Computes spectral cosine similarity to golden batch, flags outliers, and issues release verdict."""
        peaks = [
            ChemicalPeak(
                retention_time_min=p.get("rt", 0.0),
                compound_name=p.get("compound", "Unknown"),
                peak_area=p.get("area", 100.0),
                relative_abundance_pct=p.get("abundance", 10.0)
            )
            for p in measured_peaks
        ]

        # Calculate cosine similarity against golden peaks
        similarity = cls._compute_spectral_similarity(peaks)
        
        # Calculate quantitative yield potency vs golden standard
        total_golden = sum(p["abundance"] for p in cls._GOLDEN_PEAKS)
        total_measured = sum(p.relative_abundance_pct for p in peaks)
        potency_ratio = total_measured / max(0.001, total_golden)

        # Flag outlier if spectral pattern diverges OR total active marker yield is deficient (< 70% or > 130%)
        outlier = (similarity < 0.90) or (potency_ratio < 0.70) or (potency_ratio > 1.30)

        status = BatchReleaseStatus.QC_PASSED if not outlier else BatchReleaseStatus.QC_REJECTED
        qc_notes = (
            f"Spectral similarity index: {similarity:.4f} against Golden Standard. "
            f"Active potency yield: {potency_ratio*100:.1f}%. "
            + ("Within release specifications." if not outlier else "FLAGGED: Significant chromatographic peak deviation or potency deficit detected.")
        )

        dossier = BatchManufacturingDossier(
            batch_id=batch_id,
            batch_number=batch_number,
            formulation_id=formulation_id,
            formulation_version=formulation_version,
            raw_material_lot_ids=raw_material_lots,
            supplier_name=supplier_name,
            extraction_solvent=solvent,
            extraction_temp_celsius=temp_c,
            extraction_duration_hours=duration_h,
            mfg_date=mfg_date,
            exp_date=exp_date,
            chromatogram_peaks=peaks,
            fingerprint_hash=f"FPT-{abs(hash(str(measured_peaks))) % 1000000:06d}",
            similarity_to_golden_standard=round(similarity, 4),
            outlier_flag=outlier,
            status=status,
            qc_notes=qc_notes
        )

        cls._DOSSIER_REGISTRY[batch_id] = dossier
        return dossier

    @classmethod
    def _compute_spectral_similarity(cls, measured_peaks: List[ChemicalPeak]) -> float:
        """Vector cosine similarity across primary marker abundances."""
        if not measured_peaks:
            return 0.0

        ref_vec = [p["abundance"] for p in cls._GOLDEN_PEAKS]
        meas_map = {p.compound_name: p.relative_abundance_pct for p in measured_peaks}
        meas_vec = [meas_map.get(p["compound"], 0.0) for p in cls._GOLDEN_PEAKS]

        dot = sum(r * m for r, m in zip(ref_vec, meas_vec))
        norm_r = math.sqrt(sum(r * r for r in ref_vec))
        norm_m = math.sqrt(sum(m * m for m in meas_vec))

        if norm_r == 0 or norm_m == 0:
            return 0.0
        return dot / (norm_r * norm_m)

    @classmethod
    def get_batch_dossier(cls, batch_id: str) -> Optional[Dict[str, Any]]:
        dossier = cls._DOSSIER_REGISTRY.get(batch_id)
        return dossier.to_dict() if dossier else None
