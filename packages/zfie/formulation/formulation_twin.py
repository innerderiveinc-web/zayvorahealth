"""
ZFIE Computational Formulation Twin
Defines the first-class ComputationalFormulationTwin entity representing classical,
chemical, biological, and clinical states of a polyherbal formulation.
Separates Formula from Batch.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from packages.zfie.core.enums import QualityStatus, SafetyVerdict


@dataclass
class FormulaIngredient:
    mufrad_id: str
    botanical_name: str
    vernacular_name: str
    ratio: float                            # e.g., 0.40 (40%)
    part_used: str                          # e.g., "Corm", "Fruit", "Rhizome"
    processing_method: str = "Taqteer / Raw"  # Mudabbar or raw
    measured_compounds: List[str] = field(default_factory=list)


@dataclass
class BatchManufacturingTwin:
    batch_id: str
    formulation_id: str
    formula_version: str
    lot_number: str
    manufacture_date: str
    expiry_date: str
    quality_status: QualityStatus = QualityStatus.CERTIFIED
    coas: List[str] = field(default_factory=list)
    hplc_fingerprint_id: Optional[str] = None
    moisture_content_pct: float = 4.2
    heavy_metals_pass: bool = True
    microbial_load_pass: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["quality_status"] = self.quality_status.value
        return d


@dataclass
class ComputationalFormulationTwin:
    canonical_id: str                       # e.g., ZAY-FORM-0001
    name: str                               # e.g., Majoon Suranjan Advanced
    traditional_name: str                   # e.g., معجون سورنجان
    formula_version: str                    # e.g., v1.1
    classical_source: str                   # e.g., Bayaz-e-Kabeer, Vol II, p. 114
    therapeutic_target: str                 # e.g., Waja-ul-Mafasil / Gout / Inflammatory Arthritis
    ingredients: List[FormulaIngredient] = field(default_factory=list)
    preparation_method: str = "Traditional Majoon Confection with Asal (Honey) Excipient Base"
    hash_signature: str = ""
    created_at: float = field(default_factory=time.time)
    parent_version: Optional[str] = None
    change_rationale: Optional[str] = None
    version_history: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        if not self.hash_signature:
            self.hash_signature = self.compute_hash()

    def compute_hash(self) -> str:
        rep = {
            "id": self.canonical_id,
            "version": self.formula_version,
            "ingredients": [
                {"id": i.mufrad_id, "ratio": i.ratio, "prep": i.processing_method}
                for i in sorted(self.ingredients, key=lambda x: x.mufrad_id)
            ]
        }
        raw = json.dumps(rep, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FormulationTwinRegistry:
    """In-memory authoritative registry for Formulation Twins and Batches."""
    _TWINS: Dict[str, ComputationalFormulationTwin] = {}
    _BATCHES: Dict[str, List[BatchManufacturingTwin]] = {}

    @classmethod
    def register_twin(cls, twin: ComputationalFormulationTwin) -> ComputationalFormulationTwin:
        cls._TWINS[twin.canonical_id] = twin
        return twin

    @classmethod
    def get_twin(cls, canonical_id: str) -> Optional[ComputationalFormulationTwin]:
        return cls._TWINS.get(canonical_id)

    @classmethod
    def register_batch(cls, batch: BatchManufacturingTwin) -> BatchManufacturingTwin:
        if batch.formulation_id not in cls._BATCHES:
            cls._BATCHES[batch.formulation_id] = []
        cls._BATCHES[batch.formulation_id].append(batch)
        return batch

    @classmethod
    def list_batches(cls, formulation_id: str) -> List[BatchManufacturingTwin]:
        return cls._BATCHES.get(formulation_id, [])

    @classmethod
    def create_new_version(
        cls,
        base_id: str,
        new_version_tag: str,
        modified_proportions: Dict[str, float],
        change_rationale: str
    ) -> ComputationalFormulationTwin:
        """Modifying ratios or ingredients triggers a new formula version with an audited lineage."""
        parent = cls.get_twin(base_id)
        if not parent:
            raise ValueError(f"Base formulation {base_id} not found.")

        new_ingredients = []
        for ing in parent.ingredients:
            ratio = modified_proportions.get(ing.mufrad_id, ing.ratio)
            new_ingredients.append(
                FormulaIngredient(
                    mufrad_id=ing.mufrad_id,
                    botanical_name=ing.botanical_name,
                    vernacular_name=ing.vernacular_name,
                    ratio=ratio,
                    part_used=ing.part_used,
                    processing_method=ing.processing_method,
                    measured_compounds=ing.measured_compounds
                )
            )

        new_twin = ComputationalFormulationTwin(
            canonical_id=base_id,
            name=parent.name,
            traditional_name=parent.traditional_name,
            formula_version=new_version_tag,
            classical_source=parent.classical_source,
            therapeutic_target=parent.therapeutic_target,
            ingredients=new_ingredients,
            preparation_method=parent.preparation_method,
            parent_version=parent.formula_version,
            change_rationale=change_rationale,
            version_history=parent.version_history + [{
                "version": parent.formula_version,
                "timestamp": parent.created_at,
                "hash": parent.hash_signature
            }]
        )
        cls.register_twin(new_twin)
        return new_twin


# Seed Canonical Formulation: Majoon Suranjan Advanced
_SEED_TWIN = ComputationalFormulationTwin(
    canonical_id="ZAY-FORM-0001",
    name="Majoon Suranjan Advanced",
    traditional_name="معجون سورنجان ایڈوانسڈ",
    formula_version="v1.1",
    classical_source="Qarabadin-e-Azam / Bayaz-e-Kabeer Vol 2",
    therapeutic_target="Waja-ul-Mafasil / Gout / Inflammatory Joint Pathology",
    ingredients=[
        FormulaIngredient("ZAY-MUF-0001", "Colchicum autumnale", "Suranjan Shirin", 0.45, "Corm", "Mudabbar / Purified", ["Colchicine", "Demecolcine"]),
        FormulaIngredient("ZAY-MUF-0002", "Piper nigrum", "Filfil Siyah", 0.25, "Dried Fruit", "Micronized", ["Piperine", "Chavicine"]),
        FormulaIngredient("ZAY-MUF-0003", "Commiphora mukul", "Muqil", 0.30, "Purified Gum Resin", "Shodhit in Triphala Decoction", ["Guggulsterone E", "Guggulsterone Z"])
    ]
)
FormulationTwinRegistry.register_twin(_SEED_TWIN)

# Seed 2 distinct batches demonstrating formula vs batch separation
FormulationTwinRegistry.register_batch(
    BatchManufacturingTwin(
        batch_id="ZAY-BATCH-2026-001",
        formulation_id="ZAY-FORM-0001",
        formula_version="v1.1",
        lot_number="MS-2026-08A",
        manufacture_date="2026-08-01",
        expiry_date="2028-07-31",
        quality_status=QualityStatus.CERTIFIED,
        coas=["COA-MS-001.pdf"],
        hplc_fingerprint_id="HPLC-MS-2026-08A-PEAKS"
    )
)
FormulationTwinRegistry.register_batch(
    BatchManufacturingTwin(
        batch_id="ZAY-BATCH-2026-002",
        formulation_id="ZAY-FORM-0001",
        formula_version="v1.1",
        lot_number="MS-2026-09B",
        manufacture_date="2026-09-10",
        expiry_date="2028-09-09",
        quality_status=QualityStatus.CERTIFIED,
        coas=["COA-MS-002.pdf"],
        hplc_fingerprint_id="HPLC-MS-2026-09B-PEAKS"
    )
)
