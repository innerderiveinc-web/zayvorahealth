"""
ZAYVORA HEALTH OS™ — Computational Formulation Twin™ Data Models
Governed Scientific Intelligence Layer (Blueprint §13, §14, §15, §36, §37)

Provides authoritative Digital Twin abstractions:
- Formulation Definition & Semantic Versioning (ZAY-FORM-XXXX v1.0, v1.1)
- Physical Manufacturing Batch Twin (ZAY-BATCH-XXXX)
- Multi-Constituent Ratio & Mudabbar Processing Spec
- Quantitative HPLC/HPTLC Fingerprint Profile
- Network Target & Pathway Interconnection
- Clinical Caveat Invariants
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class ConstituentRole(str, Enum):
    JUZ_E_AZAM = "JUZ_E_AZAM"       # Chief active botanical (e.g. Suranjan in Majun Suranjan)
    MUAWIN = "MUAWIN"               # Adjuvant / Potentiator (e.g. Zanjabil)
    MUSLEH = "MUSLEH"               # Corrective / Antidote against adverse effects (e.g. Roghan-e-Badam, Filfil)
    BADRANJ = "BADRANJ"             # Vehicle / Base / Syrupy matrix (e.g. Asal / Honey Qiwam)


class QualityStatus(str, Enum):
    CERTIFIED = "CERTIFIED"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"
    TESTING = "TESTING"


@dataclass
class ConstituentSpec:
    substance_id: str                      # ZAY-MUF-XXXX
    unani_name: str                        # e.g., "Suranjan Shirin"
    botanical_name: str                    # e.g., "Colchicum luteum Baker"
    parts_by_weight: float                 # Quantitative proportion (e.g., 2.0 parts)
    percentage: float                      # Percentage of active herb blend
    role: ConstituentRole                  # Role in classical formulation architecture
    processing_method: str                 # e.g., "Mudabbar in Cow's Milk per UPI"
    is_schedule_e1: bool = False
    mudabbar_verified: bool = True
    key_marker_compounds: List[str] = field(default_factory=list) # ZAY-CMP-XXXX IDs


@dataclass
class ChemicalFingerprintMarker:
    compound_id: str                       # ZAY-CMP-XXXX
    compound_name: str                     # e.g., "Colchicine", "6-Gingerol"
    target_concentration_mg_g: float       # Nominal marker concentration in finished product
    tolerance_min_mg_g: float              # Lower specification limit (LSL)
    tolerance_max_mg_g: float              # Upper specification limit (USL)
    retention_time_min: float              # HPLC peak retention time in minutes
    analytical_method: str = "HPLC-DAD 245nm"


@dataclass
class BatchManufacturingTwin:
    batch_id: str                          # ZAY-BATCH-XXXX
    formulation_id: str                    # ZAY-FORM-XXXX
    formula_version: str                   # e.g., "v1.1"
    lot_number: str                        # Physical manufacturing lot (e.g. "MS-2026-LOT5")
    manufacturing_date: str                # ISO format
    expiry_date: str                       # ISO format
    manufacturer_facility_id: str          # e.g., "FAC-DELHI-01"
    assayed_markers: Dict[str, float]      # compound_id -> actual assayed mg/g
    microbial_limits_pass: bool = True     # TAMC < 10^5 CFU/g, TYMC < 10^3 CFU/g
    heavy_metals_pass: bool = True         # Pb < 10ppm, As < 3ppm, Cd < 0.3ppm, Hg < 1ppm per AYUSH
    aflatoxins_pass: bool = True           # Total aflatoxins (B1+B2+G1+G2) < 5 ppb
    moisture_content_pct: float = 8.5      # Loss on drying
    quality_status: QualityStatus = QualityStatus.CERTIFIED
    release_officer_id: str = "QC-SIGN-8821"
    tamper_proof_hash: str = ""

    def __post_init__(self):
        if not self.tamper_proof_hash:
            raw = f"{self.batch_id}:{self.formulation_id}:{self.lot_number}:{self.quality_status.value}:{self.manufacturing_date}"
            self.tamper_proof_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @property
    def batch_number(self) -> str:
        return self.lot_number

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FormulationDigitalTwin:
    formulation_id: str                    # ZAY-FORM-XXXX
    formula_version: str                   # e.g., "v1.0", "v1.1"
    canonical_name: str                    # Classical or Coined Name (e.g. "Majun Suranjan", "Glucovora Core")
    unani_category: str                    # Majun, Hab, Safoof, Itrifal, Sharbat, Kushta
    classical_indication: str              # e.g., "Waja-ul-Mafasil, Niqris (Gout), Irq-un-Nasa (Sciatica)"
    primary_mizaj_effect: str              # e.g., "Har 2°, Yabis 2° (Resolves cold phlegm in articular joints)"
    primary_organ_axis: str                # e.g., "mafasil", "kabid-mida", "dimagh-aasab"
    constituents: List[ConstituentSpec] = field(default_factory=list)
    fingerprint_markers: List[ChemicalFingerprintMarker] = field(default_factory=list)
    resolved_targets: List[str] = field(default_factory=list) # ZAY-TGT-XXXX IDs
    resolved_pathways: List[str] = field(default_factory=list) # ZAY-PW-XXXX IDs
    synergy_pairs: List[Dict[str, Any]] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)
    scientific_disclaimer: str = (
        "Computational Formulation Intelligence™ provides governed scientific hypotheses and "
        "decision support. It does NOT replace clinician clinical judgment. Zero autonomous prescribing."
    )
    tamper_proof_hash: str = ""

    @property
    def hash_signature(self) -> str:
        return self.tamper_proof_hash

    @property
    def canonical_id(self) -> str:
        return self.formulation_id

    @property
    def is_schedule_e1(self) -> bool:
        return any(c.is_schedule_e1 for c in self.constituents)

    def __post_init__(self):
        if not self.tamper_proof_hash:
            raw = f"{self.formulation_id}:{self.formula_version}:{self.canonical_name}:{self.primary_organ_axis}"
            self.tamper_proof_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["constituents"] = [
            {
                "substance_id": c.substance_id,
                "unani_name": c.unani_name,
                "botanical_name": c.botanical_name,
                "parts_by_weight": c.parts_by_weight,
                "percentage": c.percentage,
                "role": c.role.value if hasattr(c.role, "value") else str(c.role),
                "processing_method": c.processing_method,
                "is_schedule_e1": c.is_schedule_e1,
                "mudabbar_verified": c.mudabbar_verified,
                "key_marker_compounds": c.key_marker_compounds
            }
            for c in self.constituents
        ]
        return res


class FormulationTwinRegistry:
    """Authoritative singleton registry for Formulation Twins and Production Batches."""

    _twins: Dict[str, FormulationDigitalTwin] = {} # Key: "{formulation_id}:{version}" or formulation_id (latest)
    _batches: Dict[str, BatchManufacturingTwin] = {}

    @classmethod
    def initialize_seeds(cls) -> None:
        if cls._twins:
            return

        # 1. Pilot Domain 1: Majun Suranjan (Classical Waja-ul-Mafasil formulation)
        majun_suranjan = FormulationDigitalTwin(
            formulation_id="ZAY-FORM-0001",
            formula_version="v1.1",
            canonical_name="Majun Suranjan",
            unani_category="Majun",
            classical_indication="Waja-ul-Mafasil (Rheumatoid & Osteoarthritis), Niqris (Gout), Joint stiffness",
            primary_mizaj_effect="Har 2°, Yabis 2° (Mudammih Balgham & Musakkin-e-Alam)",
            primary_organ_axis="mafasil",
            constituents=[
                ConstituentSpec(
                    substance_id="ZAY-MUF-0001",
                    unani_name="Suranjan Shirin",
                    botanical_name="Colchicum luteum Baker",
                    parts_by_weight=2.0,
                    percentage=40.0,
                    role=ConstituentRole.JUZ_E_AZAM,
                    processing_method="Mudabbar via 24h Cow's Milk boiling per UPI standard",
                    is_schedule_e1=True,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0001", "ZAY-CMP-0002"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0002",
                    unani_name="Zanjabil",
                    botanical_name="Zingiber officinale Roscoe",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUAWIN,
                    processing_method="Sun-dried peeled rhizome ground to fine Safoof",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0003", "ZAY-CMP-0004"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0003",
                    unani_name="Asgandh Nagori",
                    botanical_name="Withania somnifera (L.) Dunal",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUSLEH,
                    processing_method="Fine root powder, dual extracted in warm Ghilaf",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0005"]
                )
            ],
            fingerprint_markers=[
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0001",
                    compound_name="Colchicine",
                    target_concentration_mg_g=0.25,
                    tolerance_min_mg_g=0.20,
                    tolerance_max_mg_g=0.30,
                    retention_time_min=8.42,
                    analytical_method="HPLC-DAD 245nm per AYUSH Monograph"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0003",
                    compound_name="6-Gingerol",
                    target_concentration_mg_g=1.45,
                    tolerance_min_mg_g=1.20,
                    tolerance_max_mg_g=1.75,
                    retention_time_min=14.12,
                    analytical_method="HPLC-DAD 280nm"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0005",
                    compound_name="Withaferin A",
                    target_concentration_mg_g=0.85,
                    tolerance_min_mg_g=0.70,
                    tolerance_max_mg_g=1.05,
                    retention_time_min=11.60,
                    analytical_method="HPLC-DAD 225nm"
                )
            ],
            resolved_targets=["ZAY-TGT-0001", "ZAY-TGT-0002", "ZAY-TGT-0003", "ZAY-TGT-0004", "ZAY-TGT-0005"],
            resolved_pathways=["ZAY-PW-0001", "ZAY-PW-0002", "ZAY-PW-0003", "ZAY-PW-0004"],
            synergy_pairs=[
                {
                    "compound_a": "Colchicine (Suranjan)",
                    "compound_b": "6-Gingerol (Zanjabil)",
                    "mechanism": "Zanjabil gingerols suppress gastric mucosal COX-1 ulceration induced by alkaloid load while synergistically downregulating joint synovial NF-kappaB and NLRP3 inflammasome.",
                    "synergy_type": "Toxicity-Mitigating Potentiation (Classical Musleh Principle)"
                },
                {
                    "compound_a": "Colchicine (Suranjan)",
                    "compound_b": "Withaferin A (Asgandh)",
                    "mechanism": "Dual suppression of macrophage migration and proteasomal degradation inhibiting systemic pro-inflammatory cytokines TNF-alpha and IL-1beta.",
                    "synergy_type": "Additive Anti-Inflammatory"
                }
            ],
            contraindications=[
                "Absolute: Pregnancy and active lactation (Schedule E1 alkaloid teratogenicity risk)",
                "Absolute: Severe renal failure (eGFR < 30 mL/min/1.73m²)",
                "Relative: Concurrent strong CYP3A4 inhibitors (Clarithromycin, Ketoconazole)"
            ]
        )

        cls.register_twin(majun_suranjan)

        # 2. Pilot Domain 2: Glucovora Core (Metabolic & Glycemic Regulation)
        glucovora = FormulationDigitalTwin(
            formulation_id="ZAY-FORM-0002",
            formula_version="v1.0",
            canonical_name="Glucovora Core",
            unani_category="Safoof / Micro-pellet",
            classical_indication="Ziabetus Shakari (Type 2 Diabetes Mellitus), Su-e-Mizaj Barid Kabidi",
            primary_mizaj_effect="Yabis 2°, Barid 1° (Tanqiya-e-Dam & Muqawwi-e-Banqras)",
            primary_organ_axis="kabid-mida",
            constituents=[
                ConstituentSpec(
                    substance_id="ZAY-MUF-0004",
                    unani_name="Gurmar Booti",
                    botanical_name="Gymnema sylvestre (Retz.) R.Br. ex Schult.",
                    parts_by_weight=3.0,
                    percentage=60.0,
                    role=ConstituentRole.JUZ_E_AZAM,
                    processing_method="Standardized water extract (25% Gymnemic acids)",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0006"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0002",
                    unani_name="Zanjabil",
                    botanical_name="Zingiber officinale Roscoe",
                    parts_by_weight=1.0,
                    percentage=20.0,
                    role=ConstituentRole.MUAWIN,
                    processing_method="Subcritical CO2 rhizome extract",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0003"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0005",
                    unani_name="Kasni",
                    botanical_name="Cichorium intybus L.",
                    parts_by_weight=1.0,
                    percentage=20.0,
                    role=ConstituentRole.MUSLEH,
                    processing_method="Seed decoction spray-dried powder",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0007"]
                )
            ],
            fingerprint_markers=[
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0006",
                    compound_name="Gymnemic Acid I",
                    target_concentration_mg_g=15.0,
                    tolerance_min_mg_g=12.5,
                    tolerance_max_mg_g=18.0,
                    retention_time_min=18.30,
                    analytical_method="HPLC-ELSD"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0007",
                    compound_name="Cichoric Acid",
                    target_concentration_mg_g=3.20,
                    tolerance_min_mg_g=2.70,
                    tolerance_max_mg_g=3.80,
                    retention_time_min=9.15,
                    analytical_method="HPLC-DAD 330nm"
                )
            ],
            resolved_targets=["ZAY-TGT-0007", "ZAY-TGT-0008", "ZAY-TGT-0009"],
            resolved_pathways=["ZAY-PW-0006", "ZAY-PW-0007", "ZAY-PW-0008"],
            synergy_pairs=[
                {
                    "compound_a": "Gymnemic Acid I (Gurmar)",
                    "compound_b": "Cichoric Acid (Kasni)",
                    "mechanism": "Dual insulin sensitizing and hepatic gluconeogenesis suppression preventing post-prandial glycemic excursions.",
                    "synergy_type": "Metabolic Dual-Axis Synergy"
                }
            ],
            contraindications=[
                "Hypoglycemia risk when combined with high-dose sulfonylureas without dose adjustment"
            ]
        )

        cls.register_twin(glucovora)

        # 3. Pilot Domain 3: LiverPrime Core (Hepato-Biliary & Detoxification)
        liverprime = FormulationDigitalTwin(
            formulation_id="ZAY-FORM-0003",
            formula_version="v1.0",
            canonical_name="LiverPrime Core",
            unani_category="Sharbat / Concentrated Decoction",
            classical_indication="Su-e-Mizaj Barid Kabidi, Hepatic congestion, Sluggish bile flow",
            primary_mizaj_effect="Barid 1°, Yabis 1° (Mufattih Sudad & Muqawwi-e-Kabid)",
            primary_organ_axis="kabid-mida",
            constituents=[
                ConstituentSpec(
                    substance_id="ZAY-MUF-0005",
                    unani_name="Kasni",
                    botanical_name="Cichorium intybus L.",
                    parts_by_weight=2.0,
                    percentage=40.0,
                    role=ConstituentRole.JUZ_E_AZAM,
                    processing_method="Aqueous seed & root decoction (Qiwam standard)",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0007"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0006",
                    unani_name="Revand Chini",
                    botanical_name="Rheum emodi Wall. ex Meisn.",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUAWIN,
                    processing_method="Hydro-ethanolic rhizome extract",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0008"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0007",
                    unani_name="Gaozaban",
                    botanical_name="Borago officinalis L.",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUSLEH,
                    processing_method="Gentle floral infusion",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0010"]
                )
            ],
            fingerprint_markers=[
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0007",
                    compound_name="Cichoric Acid",
                    target_concentration_mg_g=4.20,
                    tolerance_min_mg_g=3.50,
                    tolerance_max_mg_g=4.90,
                    retention_time_min=9.15,
                    analytical_method="HPLC-DAD 330nm"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0008",
                    compound_name="Rhein",
                    target_concentration_mg_g=1.80,
                    tolerance_min_mg_g=1.40,
                    tolerance_max_mg_g=2.20,
                    retention_time_min=16.80,
                    analytical_method="HPLC-DAD 254nm"
                )
            ],
            resolved_targets=["ZAY-TGT-0010", "ZAY-TGT-0011", "ZAY-TGT-0009"],
            resolved_pathways=["ZAY-PW-0009", "ZAY-PW-0010", "ZAY-PW-0008"],
            synergy_pairs=[
                {
                    "compound_a": "Cichoric Acid (Kasni)",
                    "compound_b": "Rhein (Revand Chini)",
                    "mechanism": "Cooperative activation of Nrf2-ARE antioxidant axis and bile salt export pump (BSEP) resolving hepatic steatosis.",
                    "synergy_type": "Hepatoprotective Dual-Pathway Synergy"
                }
            ],
            contraindications=[
                "Biliary tract obstruction / acute gallstone cholecystitis"
            ]
        )
        cls.register_twin(liverprime)

        # 4. Pilot Domain 4: Cardiovora Core (Cardio-Vascular & Endothelial Axis)
        cardiovora = FormulationDigitalTwin(
            formulation_id="ZAY-FORM-0004",
            formula_version="v1.0",
            canonical_name="Cardiovora Core",
            unani_category="Khamira / Micro-emulsion",
            classical_indication="Khafaqan (Palpitations), Dhaf-e-Qalb (Cardiovascular weakness), Hypertension support",
            primary_mizaj_effect="Motadil Har 1°, Yabis 1° (Muqawwi-e-Qalb & Mufarreh)",
            primary_organ_axis="qalb-urooq",
            constituents=[
                ConstituentSpec(
                    substance_id="ZAY-MUF-0008",
                    unani_name="Arjun Chhal",
                    botanical_name="Terminalia arjuna (Roxb. ex DC.) Wight & Arn.",
                    parts_by_weight=2.5,
                    percentage=50.0,
                    role=ConstituentRole.JUZ_E_AZAM,
                    processing_method="Standardized bark aqueous extract",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0009"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0009",
                    unani_name="Badranjboya",
                    botanical_name="Melissa officinalis L.",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUAWIN,
                    processing_method="Cold hydro-distillation",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0010"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0003",
                    unani_name="Asgandh Nagori",
                    botanical_name="Withania somnifera (L.) Dunal",
                    parts_by_weight=1.0,
                    percentage=20.0,
                    role=ConstituentRole.MUSLEH,
                    processing_method="Fine root powder in honey base",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0005"]
                )
            ],
            fingerprint_markers=[
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0009",
                    compound_name="Arjunic Acid",
                    target_concentration_mg_g=2.50,
                    tolerance_min_mg_g=2.00,
                    tolerance_max_mg_g=3.00,
                    retention_time_min=13.40,
                    analytical_method="HPLC-DAD 210nm"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0010",
                    compound_name="Rosmarinic Acid",
                    target_concentration_mg_g=3.00,
                    tolerance_min_mg_g=2.40,
                    tolerance_max_mg_g=3.60,
                    retention_time_min=10.25,
                    analytical_method="HPLC-DAD 330nm"
                )
            ],
            resolved_targets=["ZAY-TGT-0012", "ZAY-TGT-0013", "ZAY-TGT-0004"],
            resolved_pathways=["ZAY-PW-0011", "ZAY-PW-0012"],
            synergy_pairs=[
                {
                    "compound_a": "Arjunic Acid (Arjun)",
                    "compound_b": "Rosmarinic Acid (Badranjboya)",
                    "mechanism": "Stimulates endothelial nitric oxide synthase (eNOS) while quenching vascular superoxide, enhancing arterial compliance.",
                    "synergy_type": "Endothelial Dual-Action Synergy"
                }
            ],
            contraindications=[
                "Concurrent high-dose nitrates without blood pressure monitoring"
            ]
        )
        cls.register_twin(cardiovora)

        # 5. Pilot Domain 5: Neurovora Core (Neuro-Cognitive & Psychiatric Axis)
        neurovora = FormulationDigitalTwin(
            formulation_id="ZAY-FORM-0005",
            formula_version="v1.0",
            canonical_name="Neurovora Core",
            unani_category="Itrifal / Capsule",
            classical_indication="Nisyan (Cognitive decline), Malikhuliya (Anxiety/Depression), Sleep architecture disturbance",
            primary_mizaj_effect="Motadil Barid 1°, Yabis 1° (Muqawwi-e-Dimagh & Munaqqi-e-Asab)",
            primary_organ_axis="dimagh-aasab",
            constituents=[
                ConstituentSpec(
                    substance_id="ZAY-MUF-0010",
                    unani_name="Brahmi Booti",
                    botanical_name="Bacopa monnieri (L.) Wettst.",
                    parts_by_weight=2.5,
                    percentage=50.0,
                    role=ConstituentRole.JUZ_E_AZAM,
                    processing_method="Standardized extract (20% Bacosides)",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0011"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0011",
                    unani_name="Shankhpushpi",
                    botanical_name="Convolvulus pluricaulis Choisy",
                    parts_by_weight=1.5,
                    percentage=30.0,
                    role=ConstituentRole.MUAWIN,
                    processing_method="Whole plant fine powder",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0012"]
                ),
                ConstituentSpec(
                    substance_id="ZAY-MUF-0003",
                    unani_name="Asgandh Nagori",
                    botanical_name="Withania somnifera (L.) Dunal",
                    parts_by_weight=1.0,
                    percentage=20.0,
                    role=ConstituentRole.MUSLEH,
                    processing_method="Water extract (KSM-66 standard)",
                    is_schedule_e1=False,
                    mudabbar_verified=True,
                    key_marker_compounds=["ZAY-CMP-0005"]
                )
            ],
            fingerprint_markers=[
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0011",
                    compound_name="Bacoside A",
                    target_concentration_mg_g=12.00,
                    tolerance_min_mg_g=9.50,
                    tolerance_max_mg_g=14.50,
                    retention_time_min=15.80,
                    analytical_method="HPLC-ELSD"
                ),
                ChemicalFingerprintMarker(
                    compound_id="ZAY-CMP-0012",
                    compound_name="Luteolin-7-O-glucoside",
                    target_concentration_mg_g=1.50,
                    tolerance_min_mg_g=1.20,
                    tolerance_max_mg_g=1.80,
                    retention_time_min=7.90,
                    analytical_method="HPLC-DAD 350nm"
                )
            ],
            resolved_targets=["ZAY-TGT-0014", "ZAY-TGT-0015", "ZAY-TGT-0016"],
            resolved_pathways=["ZAY-PW-0013", "ZAY-PW-0014", "ZAY-PW-0004"],
            synergy_pairs=[
                {
                    "compound_a": "Bacoside A (Brahmi)",
                    "compound_b": "Luteolin-7-O-glucoside (Shankhpushpi)",
                    "mechanism": "Dual acetylcholinesterase inhibition and BDNF expression elevation supporting hippocampal synaptic plasticity.",
                    "synergy_type": "Neuro-Cognitive Potentiation"
                }
            ],
            contraindications=[
                "Caution with concurrent high-dose benzodiazepines or sedatives"
            ]
        )
        cls.register_twin(neurovora)

        # Seed Production Manufacturing Batches
        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-001",
            formulation_id="ZAY-FORM-0001",
            formula_version="v1.1",
            lot_number="MS-2026-LOT5",
            manufacturing_date="2026-08-10T08:00:00Z",
            expiry_date="2028-08-10T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0001": 0.248, # Target 0.25 (PASS)
                "ZAY-CMP-0003": 1.420, # Target 1.45 (PASS)
                "ZAY-CMP-0005": 0.840  # Target 0.85 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=7.9,
            quality_status=QualityStatus.CERTIFIED
        ))

        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-002",
            formulation_id="ZAY-FORM-0001",
            formula_version="v1.1",
            lot_number="MS-2026-LOT6",
            manufacturing_date="2026-09-01T08:00:00Z",
            expiry_date="2028-09-01T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0001": 0.252, # Target 0.25 (PASS)
                "ZAY-CMP-0003": 1.480, # Target 1.45 (PASS)
                "ZAY-CMP-0005": 0.865  # Target 0.85 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=8.1,
            quality_status=QualityStatus.CERTIFIED
        ))

        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-003",
            formulation_id="ZAY-FORM-0002",
            formula_version="v1.0",
            lot_number="GLU-2026-LOT1",
            manufacturing_date="2026-08-15T08:00:00Z",
            expiry_date="2028-08-15T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0006": 15.2,  # Target 15.0 (PASS)
                "ZAY-CMP-0007": 3.15   # Target 3.20 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=6.5,
            quality_status=QualityStatus.CERTIFIED
        ))

        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-004",
            formulation_id="ZAY-FORM-0003",
            formula_version="v1.0",
            lot_number="LP-2026-LOT1",
            manufacturing_date="2026-08-20T08:00:00Z",
            expiry_date="2028-08-20T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0007": 4.18,  # Target 4.20 (PASS)
                "ZAY-CMP-0008": 1.78   # Target 1.80 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=7.2,
            quality_status=QualityStatus.CERTIFIED
        ))

        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-005",
            formulation_id="ZAY-FORM-0004",
            formula_version="v1.0",
            lot_number="CARD-2026-LOT1",
            manufacturing_date="2026-08-25T08:00:00Z",
            expiry_date="2028-08-25T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0009": 2.48,  # Target 2.50 (PASS)
                "ZAY-CMP-0010": 2.96   # Target 3.00 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=5.8,
            quality_status=QualityStatus.CERTIFIED
        ))

        cls.register_batch(BatchManufacturingTwin(
            batch_id="ZAY-BATCH-2026-006",
            formulation_id="ZAY-FORM-0005",
            formula_version="v1.0",
            lot_number="NEURO-2026-LOT1",
            manufacturing_date="2026-09-02T08:00:00Z",
            expiry_date="2028-09-02T08:00:00Z",
            manufacturer_facility_id="FAC-DELHI-01",
            assayed_markers={
                "ZAY-CMP-0011": 11.85, # Target 12.00 (PASS)
                "ZAY-CMP-0012": 1.48   # Target 1.50 (PASS)
            },
            microbial_limits_pass=True,
            heavy_metals_pass=True,
            aflatoxins_pass=True,
            moisture_content_pct=6.1,
            quality_status=QualityStatus.CERTIFIED
        ))

    @classmethod
    def register_twin(cls, twin: FormulationDigitalTwin) -> FormulationDigitalTwin:
        cls._twins[f"{twin.formulation_id}:{twin.formula_version}"] = twin
        cls._twins[twin.formulation_id] = twin # Latest default
        cls._twins[twin.canonical_name.lower().strip()] = twin
        return twin

    @classmethod
    def register_batch(cls, batch: BatchManufacturingTwin) -> BatchManufacturingTwin:
        cls._batches[batch.batch_id] = batch
        cls._batches[batch.lot_number.upper().strip()] = batch
        return batch

    @classmethod
    def get_twin(cls, query: str, version: Optional[str] = None) -> Optional[FormulationDigitalTwin]:
        cls.initialize_seeds()
        q = query.strip()
        if version:
            twin = cls._twins.get(f"{q}:{version}")
            if twin:
                return twin
        twin = cls._twins.get(q)
        if not twin:
            twin = cls._twins.get(q.lower())
        return twin

    @classmethod
    def get_batch(cls, query: str) -> Optional[BatchManufacturingTwin]:
        cls.initialize_seeds()
        return cls._batches.get(query.strip()) or cls._batches.get(query.upper().strip())

    @classmethod
    def list_twins(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        seen = set()
        out = []
        for k, twin in cls._twins.items():
            if twin.formulation_id not in seen:
                seen.add(twin.formulation_id)
                out.append(twin.to_dict())
        return out

    @classmethod
    def list_batches_for_formulation(cls, formulation_id: str) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        seen = set()
        out = []
        for batch in cls._batches.values():
            if batch.formulation_id == formulation_id and batch.batch_id not in seen:
                seen.add(batch.batch_id)
                out.append(batch.to_dict())
        return out

    @classmethod
    def create_new_formula_version(
        cls,
        base_formulation_id: str,
        new_version_tag: str,
        modified_proportions: Dict[str, float],
        change_rationale: str = ""
    ) -> FormulationDigitalTwin:
        base = cls.get_twin(base_formulation_id)
        if not base:
            raise ValueError(f"Base formulation not found: {base_formulation_id}")
        
        new_constituents = []
        for c in base.constituents:
            new_pct = modified_proportions.get(c.substance_id, c.percentage)
            new_constituents.append(ConstituentSpec(
                substance_id=c.substance_id,
                unani_name=c.unani_name,
                botanical_name=c.botanical_name,
                parts_by_weight=new_pct / 10.0,
                percentage=new_pct,
                role=c.role,
                processing_method=c.processing_method,
                is_schedule_e1=c.is_schedule_e1,
                mudabbar_verified=c.mudabbar_verified,
                key_marker_compounds=list(c.key_marker_compounds)
            ))
        
        content = f"{base.formulation_id}:{new_version_tag}:{change_rationale}:{json.dumps(modified_proportions, sort_keys=True)}"
        new_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        new_twin = FormulationDigitalTwin(
            formulation_id=base.formulation_id,
            formula_version=new_version_tag,
            canonical_name=base.canonical_name,
            unani_category=base.unani_category,
            classical_indication=base.classical_indication,
            primary_mizaj_effect=base.primary_mizaj_effect,
            primary_organ_axis=base.primary_organ_axis,
            constituents=new_constituents,
            fingerprint_markers=base.fingerprint_markers,
            resolved_targets=list(base.resolved_targets),
            resolved_pathways=list(base.resolved_pathways),
            synergy_pairs=list(base.synergy_pairs),
            contraindications=list(base.contraindications),
            tamper_proof_hash=new_hash
        )
        cls.register_twin(new_twin)
        return new_twin


# Auto-initialize
FormulationTwinRegistry.initialize_seeds()
