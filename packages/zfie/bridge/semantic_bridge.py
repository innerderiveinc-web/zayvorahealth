"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 3: Unani <-> Biomedical Semantic Bridge & Biological State Precision Engine
System: ZAYVORA Health OS™
Doctrine: Classical Concept -> Operational Definition -> Observable Features -> Clinical Phenotype -> Biomarker Association -> Evidence Status
Invariant: A biomarker can NEVER be treated as automatic proof of Mizaj without calibrated empirical evidence.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class SemanticEvidenceStatus(str, Enum):
    ESTABLISHED = "ESTABLISHED"              # High-replicate clinical study
    SUPPORTED = "SUPPORTED"                  # Correlated biomarker pilot / observation
    HYPOTHESIS = "HYPOTHESIS"                # Theoretical / mechanistic deduction
    UNKNOWN = "UNKNOWN"                      # Unsubstantiated / pending mapping


@dataclass
class ClassicalBiomedicalBridgeNode:
    concept_id: str
    classical_concept: str          # e.g., "Su-i-Mizaj Damawi" / "Khilt-e-Ghaliz"
    tradition_origin: str           # "Unani Tibb"
    operational_definition: str     # Functional physiological state definition
    observable_features: List[str]  # Physical clinical observations (pulse, complexion, temperature, tongue)
    clinical_phenotype: str         # ICD-10 / NAMASTE cross-reference
    biomarker_associations: List[Dict[str, Any]] # Laboratory markers (e.g. hs-CRP, ESR, Serum Uric Acid)
    evidence_status: SemanticEvidenceStatus
    epistemic_caution: str          # Explicit guard against reductionist confusion
    citations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["evidence_status"] = self.evidence_status.value
        return d


class UnaniBiomedicalBridgeRegistry:
    """Rigorous semantic translator mapping classical humoral pathology to contemporary molecular biology."""

    _REGISTRY: Dict[str, ClassicalBiomedicalBridgeNode] = {}

    @classmethod
    def register_bridge(cls, node: ClassicalBiomedicalBridgeNode) -> None:
        cls._REGISTRY[node.concept_id] = node

    @classmethod
    def get_bridge(cls, concept_id: str) -> Optional[ClassicalBiomedicalBridgeNode]:
        return cls._REGISTRY.get(concept_id)

    @classmethod
    def map_classical_concept(cls, term: str) -> Optional[Dict[str, Any]]:
        term_clean = term.strip().lower()
        for node in cls._REGISTRY.values():
            if term_clean in node.classical_concept.lower() or term_clean in node.concept_id.lower():
                return node.to_dict()
        return None

    @classmethod
    def list_mappings(cls) -> List[Dict[str, Any]]:
        return [node.to_dict() for node in cls._REGISTRY.values()]


# Pre-seed foundational canonical bridges (Metabolic + Liver + Gut Vertical)
UnaniBiomedicalBridgeRegistry.register_bridge(
    ClassicalBiomedicalBridgeNode(
        concept_id="SEM-BRG-001",
        classical_concept="Waja-ul-Mafasil Barid / Balgham-e-Fasid",
        tradition_origin="Unani Tibb",
        operational_definition="Accumulation of viscous, cold morbid humor in articular cartilage leading to synovial stasis, severe inflammatory flares, and crystal-induced macrophage migration.",
        observable_features=[
            "Tense, warm, erythematous swelling over joint",
            "Deep throbbing pain aggravated by nocturnal rest and cold weather",
            "Slow, full, undulating pulse (Nabz-e-Azeem / Mutawassit)",
            "Turbid or concentrated morning urine (Qaroorah Ghaliz)"
        ],
        clinical_phenotype="M10.0 Idiopathic Gout / Inflammatory Monoarthritis",
        biomarker_associations=[
            {"biomarker": "Serum Uric Acid", "observed_trend": "Elevated (> 7.0 mg/dL)", "specificity": "Moderate"},
            {"biomarker": "hs-CRP", "observed_trend": "Markedly Elevated (> 10 mg/L)", "specificity": "High for Acute Phase"},
            {"biomarker": "Synovial MSU Crystals", "observed_trend": "Pathognomonic Birefringence", "specificity": "Definitive"}
        ],
        evidence_status=SemanticEvidenceStatus.SUPPORTED,
        epistemic_caution="Elevated Serum Uric Acid indicates crystal deposition burden but does NOT alone prove universal Balghami dyscrasia; clinical pulse, urine, and humoral balance remain authoritative.",
        citations=[
            "Al-Qanun fi al-Tibb, Kitab al-Adwiya al-Mufrada, Vol 2",
            "Lancet Rheumatol 2021; Colchicine in Crystal Synovitis Pathophysiology"
        ]
    )
)

UnaniBiomedicalBridgeRegistry.register_bridge(
    ClassicalBiomedicalBridgeNode(
        concept_id="SEM-BRG-002",
        classical_concept="Su-i-Mizaj Har Yabis Kabidi (Hot-Dry Hepatic Dyscrasia)",
        tradition_origin="Unani Tibb",
        operational_definition="Accelerated oxidative metabolism and hepatic microvascular inflammation causing bile thickening, hyperthermia of the digestive tract, and impaired xenobiotic clearance.",
        observable_features=[
            "Sallow yellowish complexion and conjunctival subicterus",
            "Dryness of tongue with yellowish fur (Lisan Safrawi)",
            "Rapid, hard, bounding pulse (Nabz-e-Saree Sawl)",
            "Intense thirst and bitter taste in mouth"
        ],
        clinical_phenotype="K76.0 Fatty Liver with Metabolic Inflammation / Steatohepatitis",
        biomarker_associations=[
            {"biomarker": "Serum ALT / AST", "observed_trend": "Elevated (> 45 U/L)", "specificity": "Hepatocellular injury"},
            {"biomarker": "Gamma-GT", "observed_trend": "Elevated (> 60 U/L)", "specificity": "Biliary stasis & oxidative stress"},
            {"biomarker": "TNF-alpha / IL-6", "observed_trend": "Upregulated systemic cytokines", "specificity": "Low"}
        ],
        evidence_status=SemanticEvidenceStatus.SUPPORTED,
        epistemic_caution="Transaminase elevations reflect acute liver cell membrane leakage; Har Yabis Kabidi assessment requires integration of whole-body thermal regulation and digestive symptoms.",
        citations=[
            "Kamil al-Sina'a al-Tibbiyya (Ali ibn al-Abbas al-Majusi), Disc 7",
            "Hepatology 2023; Metabolic Dysfunction-Associated Steatohepatitis Mechanisms"
        ]
    )
)
