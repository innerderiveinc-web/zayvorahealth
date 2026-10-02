"""
ZAYVORA HEALTH OS™ — LIMS Batch Certificate of Analysis (CoA) Ingestion Engine
Physical Wet-Lab & Quality Assurance Layer (Blueprint §18, §19, §20, §99)

Automates the ingestion, pharmacopoeial tolerance verification, heavy metals limit testing,
microbial contamination screening, and cryptographic batch seal issuance for
commercial herbal manufacturing lots and classical murakkabat batches.
"""

from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class BatchReleaseStatus(str, Enum):
    PASSED_RELEASED = "PASSED_RELEASED"
    QUARANTINE_HOLD = "QUARANTINE_HOLD"
    REJECTED_OUT_OF_SPEC = "REJECTED_OUT_OF_SPEC"


@dataclass
class PharmacopoeialLimits:
    lead_pb_ppm_max: float = 10.0      # AYUSH / WHO limit: 10 ppm
    cadmium_cd_ppm_max: float = 0.3    # AYUSH / WHO limit: 0.3 ppm
    arsenic_as_ppm_max: float = 3.0    # AYUSH / WHO limit: 3.0 ppm
    mercury_hg_ppm_max: float = 1.0    # AYUSH / WHO limit: 1.0 ppm
    total_aerobic_microbial_max_cfu_g: int = 100000 # 10^5 CFU/g
    total_yeast_mold_max_cfu_g: int = 1000          # 10^3 CFU/g
    e_coli_detected: bool = False                   # Must be Absent
    salmonella_detected: bool = False               # Must be Absent
    loss_on_drying_pct_max: float = 10.0            # Max 10% moisture


@dataclass
class CertificateOfAnalysisPayload:
    batch_number: str
    formulation_canonical_id: str      # e.g. "ZAY-FORM-0001"
    manufacturing_date: str            # YYYY-MM-DD
    expiry_date: str                   # YYYY-MM-DD
    testing_lab_name: str              # e.g. "AYUSH Central Drug Testing Laboratory"
    testing_lab_accreditation: str     # e.g. "NABL ISO/IEC 17025:2017"
    active_marker_name: str            # e.g. "Colchicine"
    active_marker_assay_pct: float     # e.g. 0.22%
    active_marker_min_pct: float       # Standard min
    active_marker_max_pct: float       # Standard max
    heavy_metals: Dict[str, float]     # {"pb": 1.2, "cd": 0.05, "as": 0.8, "hg": 0.1}
    microbial_load: Dict[str, Any]     # {"tamc": 1200, "tymc": 150, "e_coli": false, "salmonella": false}
    physical_chemistry: Dict[str, float] # {"lod_pct": 5.8, "total_ash_pct": 4.2}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BatchVerificationReport:
    batch_number: str
    formulation_canonical_id: str
    release_status: BatchReleaseStatus
    assay_status: str                  # "WITHIN_SPEC", "OUT_OF_SPEC"
    metals_status: str                 # "PASSED", "EXCEEDED_LIMIT"
    microbial_status: str              # "PASSED", "CONTAMINATED"
    discrepancies: List[str] = field(default_factory=list)
    cryptographic_release_seal: str = ""
    timestamp_utc: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LimsBatchIngestionEngine:
    """
    Authoritative ingestion and verification engine for incoming laboratory CoAs.
    Enforces statutory quality limits before allowing batch lot release to clinical dispensary.
    """

    def __init__(self, limits: Optional[PharmacopoeialLimits] = None):
        self.limits = limits or PharmacopoeialLimits()
        self._verified_batches_registry: Dict[str, BatchVerificationReport] = {}

    def verify_and_ingest_coa(self, coa: CertificateOfAnalysisPayload) -> BatchVerificationReport:
        discrepancies = []

        # 1. Active Marker Assay Verification
        assay_status = "WITHIN_SPEC"
        if not (coa.active_marker_min_pct <= coa.active_marker_assay_pct <= coa.active_marker_max_pct):
            assay_status = "OUT_OF_SPEC"
            discrepancies.append(
                f"Assay out of spec: {coa.active_marker_name} is {coa.active_marker_assay_pct}%, "
                f"required range [{coa.active_marker_min_pct} - {coa.active_marker_max_pct}]%"
            )

        # 2. Heavy Metals ICP-MS Verification
        metals_status = "PASSED"
        pb = coa.heavy_metals.get("pb", 0.0)
        cd = coa.heavy_metals.get("cd", 0.0)
        as_val = coa.heavy_metals.get("as", 0.0)
        hg = coa.heavy_metals.get("hg", 0.0)

        if pb > self.limits.lead_pb_ppm_max:
            metals_status = "EXCEEDED_LIMIT"
            discrepancies.append(f"Lead (Pb) exceeded: {pb} ppm > limit {self.limits.lead_pb_ppm_max} ppm")
        if cd > self.limits.cadmium_cd_ppm_max:
            metals_status = "EXCEEDED_LIMIT"
            discrepancies.append(f"Cadmium (Cd) exceeded: {cd} ppm > limit {self.limits.cadmium_cd_ppm_max} ppm")
        if as_val > self.limits.arsenic_as_ppm_max:
            metals_status = "EXCEEDED_LIMIT"
            discrepancies.append(f"Arsenic (As) exceeded: {as_val} ppm > limit {self.limits.arsenic_as_ppm_max} ppm")
        if hg > self.limits.mercury_hg_ppm_max:
            metals_status = "EXCEEDED_LIMIT"
            discrepancies.append(f"Mercury (Hg) exceeded: {hg} ppm > limit {self.limits.mercury_hg_ppm_max} ppm")

        # 3. Microbial Limits Screening
        microbial_status = "PASSED"
        tamc = coa.microbial_load.get("tamc", 0)
        tymc = coa.microbial_load.get("tymc", 0)
        e_coli = bool(coa.microbial_load.get("e_coli", False))
        salmonella = bool(coa.microbial_load.get("salmonella", False))

        if tamc > self.limits.total_aerobic_microbial_max_cfu_g:
            microbial_status = "CONTAMINATED"
            discrepancies.append(f"TAMC count exceeded: {tamc} CFU/g > limit {self.limits.total_aerobic_microbial_max_cfu_g}")
        if tymc > self.limits.total_yeast_mold_max_cfu_g:
            microbial_status = "CONTAMINATED"
            discrepancies.append(f"TYMC yeast/mold exceeded: {tymc} CFU/g > limit {self.limits.total_yeast_mold_max_cfu_g}")
        if e_coli:
            microbial_status = "CONTAMINATED"
            discrepancies.append("Pathogen Alert: E. coli detected in lot!")
        if salmonella:
            microbial_status = "CONTAMINATED"
            discrepancies.append("Pathogen Alert: Salmonella detected in lot!")

        # 4. Final Determination & Release Status
        if discrepancies:
            release_status = BatchReleaseStatus.REJECTED_OUT_OF_SPEC
            crypt_seal = f"QUARANTINE-{hashlib.sha256(coa.batch_number.encode()).hexdigest()[:16]}"
        else:
            release_status = BatchReleaseStatus.PASSED_RELEASED
            seal_raw = f"{coa.batch_number}:{coa.formulation_canonical_id}:{coa.active_marker_assay_pct}:{coa.testing_lab_name}"
            crypt_seal = f"ZAY-SEAL-{hashlib.sha256(seal_raw.encode()).hexdigest()[:24]}"

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        report = BatchVerificationReport(
            batch_number=coa.batch_number,
            formulation_canonical_id=coa.formulation_canonical_id,
            release_status=release_status,
            assay_status=assay_status,
            metals_status=metals_status,
            microbial_status=microbial_status,
            discrepancies=discrepancies,
            cryptographic_release_seal=crypt_seal,
            timestamp_utc=now_utc,
        )

        self._verified_batches_registry[coa.batch_number] = report
        return report

    def get_batch_verification(self, batch_number: str) -> Optional[Dict[str, Any]]:
        report = self._verified_batches_registry.get(batch_number)
        return report.to_dict() if report else None


# Global singleton instance
lims_batch_ingestion_engine = LimsBatchIngestionEngine()
