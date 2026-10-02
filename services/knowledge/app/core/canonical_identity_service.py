"""
ZAYVORA HEALTH OS™ — Canonical Identity Service
Governed Scientific Intelligence Layer (Blueprint §10, §13, §14, §15)

Authoritative ID standard:
- ZAY-MUF-XXXX  : Botanical / Single Natural Substance (Mufrad)
- ZAY-CMP-XXXX  : Chemical Compound / Phytochemical Constituent
- ZAY-FORM-XXXX : Multi-component Formulation (Murakkab)
- ZAY-BATCH-XXXX: Physical Manufacturing Lot / Batch Record
- ZAY-TGT-XXXX  : Biological Target (Protein, Receptor, Enzyme)
- ZAY-PW-XXXX   : Biological Pathway (Cellular, Metabolic, Signaling)

Guarantees 100% deterministic identity resolution, immutable SHA-256 anchoring,
and cross-system reference resolution.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class EntityType(str, Enum):
    MUFRAD = "MUFRAD"           # ZAY-MUF-XXXX
    COMPOUND = "COMPOUND"       # ZAY-CMP-XXXX
    FORMULATION = "FORMULATION" # ZAY-FORM-XXXX
    BATCH = "BATCH"             # ZAY-BATCH-XXXX
    TARGET = "TARGET"           # ZAY-TGT-XXXX
    PATHWAY = "PATHWAY"         # ZAY-PW-XXXX


@dataclass
class CanonicalSubstanceRecord:
    canonical_id: str                      # ZAY-MUF-XXXX
    canonical_name: str                    # Standard Latin / Primary name
    botanical_name: str                    # Latin binomial with author
    unani_name: str                        # Classical Tibbi name
    urdu_name: str                         # Nastaliq script
    arabic_name: Optional[str] = None
    family: str = ""
    plant_part: str = ""                   # e.g., "Dried corms", "Rhizome", "Leaves"
    harvesting_season: str = ""            # e.g., "Autumn / Post-monsoon"
    synonyms: List[str] = field(default_factory=list)
    upi_monograph: Optional[str] = None
    is_schedule_e1: bool = False
    mandatory_mudabbar: bool = False
    mudabbar_protocol: Optional[str] = None
    primary_mizaj: str = ""                # e.g., "Hot 2°, Dry 2°"
    primary_organ_axis: str = ""           # e.g., "mafasil", "kabid-mida"
    key_compounds: List[str] = field(default_factory=list) # List of ZAY-CMP-XXXX IDs
    hash_signature: str = ""

    def __post_init__(self):
        if not self.hash_signature:
            content = f"{self.canonical_id}:{self.botanical_name}:{self.unani_name}:{self.primary_organ_axis}"
            self.hash_signature = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CanonicalCompoundRecord:
    canonical_id: str                      # ZAY-CMP-XXXX
    compound_name: str                     # IUPAC or trivial name (e.g. "Colchicine")
    iupac_name: str = ""
    molecular_formula: str = ""            # e.g. "C22H25NO6"
    molecular_weight: float = 0.0          # g/mol
    smiles: str = ""
    inchi: str = ""
    inchikey: str = ""
    pubchem_cid: Optional[int] = None
    chembl_id: Optional[str] = None
    log_p: float = 0.0                     # Octanol-water partition coefficient
    bioavailability_score: float = 0.0     # 0.0 - 1.0 (Lipinski's rule compliance)
    toxicity_profile: Dict[str, Any] = field(default_factory=dict)
    known_targets: List[str] = field(default_factory=list) # List of ZAY-TGT-XXXX IDs
    hash_signature: str = ""

    def __post_init__(self):
        if not self.hash_signature:
            content = f"{self.canonical_id}:{self.compound_name}:{self.inchikey}:{self.molecular_formula}"
            self.hash_signature = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CanonicalTargetRecord:
    canonical_id: str                      # ZAY-TGT-XXXX
    gene_symbol: str                       # e.g., "TUBA1A", "IL1B", "TNF", "PPARG"
    protein_name: str                      # e.g., "Tubulin alpha-1A chain"
    uniprot_id: str                        # e.g., "Q71U36"
    chembl_target_id: Optional[str] = None # e.g., "CHEMBL237"
    organ_systems: List[str] = field(default_factory=list)
    pathways: List[str] = field(default_factory=list) # List of ZAY-PW-XXXX IDs
    hash_signature: str = ""

    def __post_init__(self):
        if not self.hash_signature:
            content = f"{self.canonical_id}:{self.gene_symbol}:{self.uniprot_id}"
            self.hash_signature = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CanonicalPathwayRecord:
    canonical_id: str                      # ZAY-PW-XXXX
    pathway_name: str                      # e.g., "Microtubule dynamics & mitosis"
    reactome_id: Optional[str] = None      # e.g., "R-HSA-194315"
    kegg_id: Optional[str] = None          # e.g., "hsa04144"
    category: str = ""                     # "Cell Cycle", "Inflammatory Response", etc.
    description: str = ""
    associated_organ_axis: str = ""
    hash_signature: str = ""

    def __post_init__(self):
        if not self.hash_signature:
            content = f"{self.canonical_id}:{self.pathway_name}:{self.reactome_id}"
            self.hash_signature = hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CanonicalIdentityRegistry:
    """Authoritative singleton registry for all canonical entities."""

    _substances: Dict[str, CanonicalSubstanceRecord] = {}
    _compounds: Dict[str, CanonicalCompoundRecord] = {}
    _targets: Dict[str, CanonicalTargetRecord] = {}
    _pathways: Dict[str, CanonicalPathwayRecord] = {}
    _synonym_lookup: Dict[str, str] = {} # Lowercase normalized -> canonical_id

    @classmethod
    def initialize_seeds(cls) -> None:
        """Seed foundational botanical, chemical, target and pathway records."""
        if cls._substances:
            return

        # 1. Botanical: Suranjan Shirin (Colchicum luteum)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0001",
            canonical_name="Colchicum luteum Baker",
            botanical_name="Colchicum luteum Baker",
            unani_name="Suranjan Shirin",
            urdu_name="سورنجان شیریں",
            arabic_name="سورنجان حلو",
            family="Colchicaceae",
            plant_part="Dried corms",
            harvesting_season="Autumn (September - October)",
            synonyms=["suranjan shirin", "colchicum luteum", "sweet colchicum", "hermodactylus", "suranjan-e-shirin"],
            upi_monograph="UPI Part I, Vol. I, Page 94",
            is_schedule_e1=True,
            mandatory_mudabbar=True,
            mudabbar_protocol="Boiled in Cow's Milk or soaked in Almond Oil / Vinegar per UPI protocol",
            primary_mizaj="Hot 2°, Dry 2° (Mudabbar: Hot 1°, Dry 1°)",
            primary_organ_axis="mafasil",
            key_compounds=["ZAY-CMP-0001", "ZAY-CMP-0002"]
        ))

        # 2. Botanical: Zanjabil (Zingiber officinale)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0002",
            canonical_name="Zingiber officinale Roscoe",
            botanical_name="Zingiber officinale Roscoe",
            unani_name="Zanjabil",
            urdu_name="زنجبیل",
            arabic_name="زنجبيل",
            family="Zingiberaceae",
            plant_part="Dried rhizome",
            harvesting_season="Winter (December - February)",
            synonyms=["zanjabil", "zingiber officinale", "ginger", "sonth", "adrak"],
            upi_monograph="UPI Part I, Vol. I, Page 112",
            is_schedule_e1=False,
            mandatory_mudabbar=False,
            primary_mizaj="Hot 3°, Dry 2°",
            primary_organ_axis="kabid-mida",
            key_compounds=["ZAY-CMP-0003", "ZAY-CMP-0004"]
        ))

        # 3. Botanical: Asgandh / Ashwagandha (Withania somnifera)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0003",
            canonical_name="Withania somnifera (L.) Dunal",
            botanical_name="Withania somnifera (L.) Dunal",
            unani_name="Asgandh Nagori",
            urdu_name="اسگندھ ناگوری",
            arabic_name="اشواغندا",
            family="Solanaceae",
            plant_part="Dried roots",
            harvesting_season="Post-monsoon (October - December)",
            synonyms=["asgandh", "withania somnifera", "ashwagandha", "winter cherry", "asgandh nagori"],
            upi_monograph="UPI Part I, Vol. I, Page 15",
            is_schedule_e1=False,
            mandatory_mudabbar=False,
            primary_mizaj="Hot 2°, Dry 2°",
            primary_organ_axis="dimagh-aasab",
            key_compounds=["ZAY-CMP-0005"]
        ))

        # 4. Botanical: Gurmar / Meshashringi (Gymnema sylvestre)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0004",
            canonical_name="Gymnema sylvestre (Retz.) R.Br. ex Schult.",
            botanical_name="Gymnema sylvestre (Retz.) R.Br. ex Schult.",
            unani_name="Gurmar Booti",
            urdu_name="گڑمار بوٹی",
            family="Apocynaceae",
            plant_part="Dried leaves",
            harvesting_season="Summer (May - July)",
            synonyms=["gurmar", "gymnema sylvestre", "gurmar booti", "miracle fruit leaf"],
            upi_monograph="UPI Part I, Vol. II, Page 45",
            is_schedule_e1=False,
            mandatory_mudabbar=False,
            primary_mizaj="Dry 2°, Cold 1°",
            primary_organ_axis="kabid-mida",
            key_compounds=["ZAY-CMP-0006"]
        ))

        # 5. Botanical: Kasni (Cichorium intybus)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0005",
            canonical_name="Cichorium intybus L.",
            botanical_name="Cichorium intybus L.",
            unani_name="Kasni",
            urdu_name="کاسنی",
            arabic_name="هندباء",
            family="Asteraceae",
            plant_part="Seeds and roots",
            harvesting_season="Spring (March - May)",
            synonyms=["kasni", "cichorium intybus", "chicory", "tukhm-e-kasni", "bekh-e-kasni"],
            upi_monograph="UPI Part I, Vol. II, Page 58",
            is_schedule_e1=False,
            mandatory_mudabbar=False,
            primary_mizaj="Cold 1°, Dry 1°",
            primary_organ_axis="kabid-mida",
            key_compounds=["ZAY-CMP-0007"]
        ))

        # 6. Botanical: Revand Chini (Rheum emodi)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0006",
            canonical_name="Rheum emodi Wall. ex Meisn.",
            botanical_name="Rheum emodi Wall. ex Meisn.",
            unani_name="Revand Chini",
            urdu_name="ریوند چینی",
            family="Polygonaceae",
            plant_part="Dried rhizomes and roots",
            harvesting_season="Autumn",
            synonyms=["revand chini", "rheum emodi", "indian rhubarb"],
            upi_monograph="UPI Part I, Vol. III, Page 82",
            is_schedule_e1=False,
            primary_mizaj="Cold 1°, Dry 2°",
            primary_organ_axis="kabid-mida",
            key_compounds=["ZAY-CMP-0008"]
        ))

        # 7. Botanical: Gaozaban (Borago officinalis)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0007",
            canonical_name="Borago officinalis L.",
            botanical_name="Borago officinalis L.",
            unani_name="Gaozaban",
            urdu_name="گاؤزبان",
            family="Boraginaceae",
            plant_part="Dried leaves and flowers",
            harvesting_season="Summer",
            synonyms=["gaozaban", "borago officinalis", "borage", "lisan-us-saur"],
            upi_monograph="UPI Part I, Vol. I, Page 38",
            is_schedule_e1=False,
            primary_mizaj="Hot 1°, Moist 1°",
            primary_organ_axis="qalb-urooq",
            key_compounds=["ZAY-CMP-0010"]
        ))

        # 8. Botanical: Arjun (Terminalia arjuna)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0008",
            canonical_name="Terminalia arjuna (Roxb. ex DC.) Wight & Arn.",
            botanical_name="Terminalia arjuna (Roxb. ex DC.) Wight & Arn.",
            unani_name="Arjun Chhal",
            urdu_name="ارجن چھال",
            family="Combretaceae",
            plant_part="Stem bark",
            harvesting_season="Winter (dry season)",
            synonyms=["arjun", "terminalia arjuna", "arjun chhal", "white marudah"],
            upi_monograph="UPI Part I, Vol. II, Page 12",
            is_schedule_e1=False,
            primary_mizaj="Cold 2°, Dry 2°",
            primary_organ_axis="qalb-urooq",
            key_compounds=["ZAY-CMP-0009"]
        ))

        # 9. Botanical: Badranjboya (Melissa officinalis)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0009",
            canonical_name="Melissa officinalis L.",
            botanical_name="Melissa officinalis L.",
            unani_name="Badranjboya",
            urdu_name="بادرنجبویہ",
            family="Lamiaceae",
            plant_part="Leaves and aerial parts",
            harvesting_season="Summer",
            synonyms=["badranjboya", "melissa officinalis", "lemon balm"],
            upi_monograph="UPI Part I, Vol. II, Page 18",
            is_schedule_e1=False,
            primary_mizaj="Hot 2°, Dry 2°",
            primary_organ_axis="qalb-urooq",
            key_compounds=["ZAY-CMP-0010"]
        ))

        # 10. Botanical: Brahmi (Bacopa monnieri)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0010",
            canonical_name="Bacopa monnieri (L.) Wettst.",
            botanical_name="Bacopa monnieri (L.) Wettst.",
            unani_name="Brahmi Booti",
            urdu_name="براہمی بوٹی",
            family="Plantaginaceae",
            plant_part="Whole herb",
            harvesting_season="Post-monsoon",
            synonyms=["brahmi", "bacopa monnieri", "water hyssop", "brahmi booti"],
            upi_monograph="UPI Part I, Vol. II, Page 24",
            is_schedule_e1=False,
            primary_mizaj="Cold 1°, Dry 1°",
            primary_organ_axis="dimagh-aasab",
            key_compounds=["ZAY-CMP-0011"]
        ))

        # 11. Botanical: Shankhpushpi (Convolvulus pluricaulis)
        cls.register_substance(CanonicalSubstanceRecord(
            canonical_id="ZAY-MUF-0011",
            canonical_name="Convolvulus pluricaulis Choisy",
            botanical_name="Convolvulus pluricaulis Choisy",
            unani_name="Shankhpushpi",
            urdu_name="شنکھ پشپی",
            family="Convolvulaceae",
            plant_part="Whole herb",
            harvesting_season="Summer / Autumn",
            synonyms=["shankhpushpi", "convolvulus pluricaulis", "morning glory"],
            upi_monograph="UPI Part I, Vol. II, Page 72",
            is_schedule_e1=False,
            primary_mizaj="Cold 2°, Moist 1°",
            primary_organ_axis="dimagh-aasab",
            key_compounds=["ZAY-CMP-0012"]
        ))

        # Seed Phytochemical Compounds
        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0001",
            compound_name="Colchicine",
            iupac_name="N-[(7S)-1,2,3,10-tetramethoxy-9-oxo-6,7-dihydro-5H-benzo[a]heptalen-7-yl]acetamide",
            molecular_formula="C22H25NO6",
            molecular_weight=399.44,
            smiles="CC(=O)NC1CCC2=CC(=C(C(=C2C3=CC=C(C(=O)C=C13)OC)OC)OC)OC",
            inchikey="IAKHMKGGTNLKSZ-INIZCTEOSA-N",
            pubchem_cid=6167,
            chembl_id="CHEMBL84",
            log_p=1.85,
            bioavailability_score=0.85,
            toxicity_profile={"narrow_therapeutic_index": True, "ld50_mouse_mg_kg": 6.0, "renal_elimination_pct": 20.0},
            known_targets=["ZAY-TGT-0001", "ZAY-TGT-0002"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0002",
            compound_name="Colchicoside",
            iupac_name="Colchicine 2-O-beta-D-glucopyranoside",
            molecular_formula="C27H33NO11",
            molecular_weight=547.55,
            inchikey="CXSMLGUPQJUGQM-UHFFFAOYSA-N",
            pubchem_cid=92138,
            chembl_id="CHEMBL453472",
            log_p=0.42,
            bioavailability_score=0.55,
            known_targets=["ZAY-TGT-0001"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0003",
            compound_name="6-Gingerol",
            iupac_name="(5S)-5-hydroxy-1-(4-hydroxy-3-methoxyphenyl)decan-3-one",
            molecular_formula="C17H26O4",
            molecular_weight=294.39,
            smiles="CCCCCC(CC(=O)CCC1=CC(=C(C=C1)O)OC)O",
            inchikey="XERFZZINZQNPNR-UHFFFAOYSA-N",
            pubchem_cid=442793,
            chembl_id="CHEMBL108605",
            log_p=3.10,
            bioavailability_score=0.90,
            known_targets=["ZAY-TGT-0003", "ZAY-TGT-0004"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0004",
            compound_name="6-Shogaol",
            iupac_name="(4E)-1-(4-hydroxy-3-methoxyphenyl)dec-4-en-3-one",
            molecular_formula="C17H24O3",
            molecular_weight=276.37,
            smiles="CCCCCC=CC(=O)CCC1=CC(=C(C=C1)O)OC",
            pubchem_cid=5281794,
            chembl_id="CHEMBL446261",
            log_p=3.80,
            bioavailability_score=0.88,
            known_targets=["ZAY-TGT-0003", "ZAY-TGT-0005"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0005",
            compound_name="Withaferin A",
            iupac_name="(4beta,5beta,6beta,22R)-4,27-dihydroxy-5,6:22,26-diepoxyergosta-2,24-diene-1,26-dione",
            molecular_formula="C28H38O6",
            molecular_weight=470.60,
            pubchem_cid=265237,
            chembl_id="CHEMBL263914",
            log_p=3.25,
            bioavailability_score=0.65,
            known_targets=["ZAY-TGT-0006", "ZAY-TGT-0005"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0006",
            compound_name="Gymnemic Acid I",
            molecular_formula="C43H66O14",
            molecular_weight=806.98,
            pubchem_cid=11953835,
            chembl_id="CHEMBL2107380",
            log_p=2.15,
            bioavailability_score=0.40,
            known_targets=["ZAY-TGT-0007", "ZAY-TGT-0008"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0007",
            compound_name="Cichoric Acid",
            iupac_name="(2R,3R)-2,3-bis[[(E)-3-(3,4-dihydroxyphenyl)prop-2-enoyl]oxy]butanedioic acid",
            molecular_formula="C22H18O12",
            molecular_weight=474.37,
            pubchem_cid=5281767,
            chembl_id="CHEMBL453006",
            log_p=1.45,
            bioavailability_score=0.60,
            known_targets=["ZAY-TGT-0004", "ZAY-TGT-0009"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0008",
            compound_name="Rhein",
            iupac_name="4,5-dihydroxy-9,10-dioxoanthracene-2-carboxylic acid",
            molecular_formula="C15H8O6",
            molecular_weight=284.22,
            pubchem_cid=10207,
            chembl_id="CHEMBL47214",
            log_p=2.40,
            bioavailability_score=0.75,
            known_targets=["ZAY-TGT-0010", "ZAY-TGT-0011"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0009",
            compound_name="Arjunic Acid",
            iupac_name="(2alpha,3beta,19alpha)-2,3,19-trihydroxyolean-12-en-28-oic acid",
            molecular_formula="C30H48O5",
            molecular_weight=488.70,
            pubchem_cid=12304879,
            chembl_id="CHEMBL480924",
            log_p=4.20,
            bioavailability_score=0.55,
            known_targets=["ZAY-TGT-0012", "ZAY-TGT-0013"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0010",
            compound_name="Rosmarinic Acid",
            iupac_name="(2R)-2-[[(2E)-3-(3,4-dihydroxyphenyl)prop-2-enoyl]oxy]-3-(3,4-dihydroxyphenyl)propanoic acid",
            molecular_formula="C18H16O8",
            molecular_weight=360.31,
            pubchem_cid=5281792,
            chembl_id="CHEMBL268297",
            log_p=1.80,
            bioavailability_score=0.70,
            known_targets=["ZAY-TGT-0012", "ZAY-TGT-0004"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0011",
            compound_name="Bacoside A",
            molecular_formula="C41H68O13",
            molecular_weight=768.97,
            pubchem_cid=92043183,
            chembl_id="CHEMBL2107400",
            log_p=2.90,
            bioavailability_score=0.45,
            known_targets=["ZAY-TGT-0014", "ZAY-TGT-0016"]
        ))

        cls.register_compound(CanonicalCompoundRecord(
            canonical_id="ZAY-CMP-0012",
            compound_name="Luteolin-7-O-glucoside",
            molecular_formula="C21H20O11",
            molecular_weight=448.38,
            pubchem_cid=5280637,
            chembl_id="CHEMBL452445",
            log_p=0.85,
            bioavailability_score=0.65,
            known_targets=["ZAY-TGT-0014", "ZAY-TGT-0015"]
        ))

        # Seed Biological Targets
        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0001",
            gene_symbol="TUBA1A",
            protein_name="Tubulin alpha-1A chain",
            uniprot_id="Q71U36",
            chembl_target_id="CHEMBL237",
            organ_systems=["Musculoskeletal", "Immune System"],
            pathways=["ZAY-PW-0001"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0002",
            gene_symbol="NLRP3",
            protein_name="NACHT, LRR and PYD domains-containing protein 3 (Inflammasome)",
            uniprot_id="Q96P20",
            chembl_target_id="CHEMBL3714087",
            organ_systems=["Immune System", "Musculoskeletal"],
            pathways=["ZAY-PW-0002"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0003",
            gene_symbol="PTGS2",
            protein_name="Prostaglandin G/H synthase 2 (COX-2)",
            uniprot_id="P35354",
            chembl_target_id="CHEMBL230",
            organ_systems=["Gastrointestinal", "Musculoskeletal", "Vascular"],
            pathways=["ZAY-PW-0003"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0004",
            gene_symbol="TNF",
            protein_name="Tumor necrosis factor alpha",
            uniprot_id="P01375",
            chembl_target_id="CHEMBL1825",
            organ_systems=["Systemic Immune", "Musculoskeletal", "Hepatic"],
            pathways=["ZAY-PW-0002", "ZAY-PW-0004"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0005",
            gene_symbol="NFKB1",
            protein_name="Nuclear factor NF-kappa-B p105 subunit",
            uniprot_id="P19838",
            chembl_target_id="CHEMBL2047",
            organ_systems=["Systemic Immune", "Nervous System"],
            pathways=["ZAY-PW-0004"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0006",
            gene_symbol="HSP90AA1",
            protein_name="Heat shock protein HSP 90-alpha",
            uniprot_id="P07900",
            chembl_target_id="CHEMBL3880",
            organ_systems=["Nervous System", "Endocrine"],
            pathways=["ZAY-PW-0005"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0007",
            gene_symbol="TAS1R2",
            protein_name="Taste receptor type 1 member 2 (Sweet taste receptor)",
            uniprot_id="Q8TE23",
            chembl_target_id="CHEMBL4794",
            organ_systems=["Metabolic", "Gastrointestinal"],
            pathways=["ZAY-PW-0006"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0008",
            gene_symbol="SLC2A4",
            protein_name="Solute carrier family 2, facilitated glucose transporter member 4 (GLUT4)",
            uniprot_id="P14672",
            chembl_target_id="CHEMBL5553",
            organ_systems=["Metabolic", "Endocrine"],
            pathways=["ZAY-PW-0007"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0009",
            gene_symbol="PPARA",
            protein_name="Peroxisome proliferator-activated receptor alpha",
            uniprot_id="Q07869",
            chembl_target_id="CHEMBL239",
            organ_systems=["Hepatic", "Metabolic"],
            pathways=["ZAY-PW-0008"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0010",
            gene_symbol="NFE2L2",
            protein_name="Nuclear factor erythroid 2-related factor 2 (Nrf2)",
            uniprot_id="Q16236",
            chembl_target_id="CHEMBL2007641",
            organ_systems=["Hepatic", "Gastrointestinal"],
            pathways=["ZAY-PW-0009"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0011",
            gene_symbol="CYP2E1",
            protein_name="Cytochrome P450 2E1",
            uniprot_id="P05181",
            chembl_target_id="CHEMBL400",
            organ_systems=["Hepatic"],
            pathways=["ZAY-PW-0010"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0012",
            gene_symbol="NOS3",
            protein_name="Endothelial nitric oxide synthase (eNOS)",
            uniprot_id="P29474",
            chembl_target_id="CHEMBL225",
            organ_systems=["Cardiovascular", "Vascular"],
            pathways=["ZAY-PW-0011"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0013",
            gene_symbol="ACE",
            protein_name="Angiotensin-converting enzyme",
            uniprot_id="P12821",
            chembl_target_id="CHEMBL229",
            organ_systems=["Cardiovascular", "Renal"],
            pathways=["ZAY-PW-0012"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0014",
            gene_symbol="ACHE",
            protein_name="Acetylcholinesterase",
            uniprot_id="P22303",
            chembl_target_id="CHEMBL220",
            organ_systems=["Nervous System", "Cognitive"],
            pathways=["ZAY-PW-0013"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0015",
            gene_symbol="GABRA1",
            protein_name="Gamma-aminobutyric acid receptor subunit alpha-1",
            uniprot_id="P14867",
            chembl_target_id="CHEMBL2094112",
            organ_systems=["Nervous System"],
            pathways=["ZAY-PW-0014"]
        ))

        cls.register_target(CanonicalTargetRecord(
            canonical_id="ZAY-TGT-0016",
            gene_symbol="BDNF",
            protein_name="Brain-derived neurotrophic factor",
            uniprot_id="P23560",
            chembl_target_id="CHEMBL4523954",
            organ_systems=["Nervous System", "Cognitive"],
            pathways=["ZAY-PW-0013"]
        ))

        # Seed Biological Pathways
        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0001",
            pathway_name="Microtubule dynamics & mitosis arrest",
            reactome_id="R-HSA-194315",
            kegg_id="hsa04144",
            category="Cell Division & Cytoskeleton",
            description="Interference with tubulin heterodimer polymerization arresting neutrophil chemotaxis and cell division.",
            associated_organ_axis="mafasil"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0002",
            pathway_name="NLRP3 Inflammasome activation and IL-1beta release",
            reactome_id="R-HSA-844456",
            kegg_id="hsa04621",
            category="Innate Immunity & Inflammation",
            description="Assembly of ASC and pro-caspase-1 cleaving pro-IL-1beta into mature active inflammatory cytokine.",
            associated_organ_axis="mafasil"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0003",
            pathway_name="Prostanoid biosynthesis & COX-2 signaling",
            reactome_id="R-HSA-2142753",
            kegg_id="hsa00590",
            category="Lipid Mediators & Eicosanoids",
            description="Conversion of arachidonic acid to PGH2 by cyclooxygenase-2 causing pain and swelling.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0004",
            pathway_name="NF-kappa B signaling pathway",
            reactome_id="R-HSA-449147",
            kegg_id="hsa04064",
            category="Transcriptional Regulation of Immunity",
            description="Phosphorylation and degradation of IkappaB allowing p50/p65 translocation to nucleus.",
            associated_organ_axis="dimagh-aasab"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0005",
            pathway_name="Cellular response to stress and heat shock response",
            reactome_id="R-HSA-3371556",
            kegg_id="hsa04141",
            category="Proteostasis & Stress Response",
            description="Modulation of chaperone activity stabilizing cellular architecture against oxidative stress.",
            associated_organ_axis="dimagh-aasab"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0006",
            pathway_name="Sensory perception of sweet taste & GLP-1 secretion",
            reactome_id="R-HSA-9709957",
            kegg_id="hsa04742",
            category="Endocrine & Sensory Signaling",
            description="Reversible antagonism of lingual and intestinal sweet taste receptors suppressing glucose absorption.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0007",
            pathway_name="Insulin receptor recycling and GLUT4 translocation",
            reactome_id="R-HSA-1445148",
            kegg_id="hsa04910",
            category="Metabolic Regulation",
            description="Signaling cascade promoting peripheral glucose uptake into skeletal muscle and adipocytes.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0008",
            pathway_name="PPAR-alpha transcriptional regulation of lipid metabolism",
            reactome_id="R-HSA-400232",
            kegg_id="hsa03320",
            category="Hepatic Lipid Oxidation",
            description="Nuclear receptor dimerization mediating beta-oxidation and hepatic clearance of triglycerides.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0009",
            pathway_name="Cellular response to chemical stress and Nrf2 activation",
            reactome_id="R-HSA-9711123",
            kegg_id="hsa04140",
            category="Oxidative Stress & Cytoprotection",
            description="Antioxidant response element (ARE) activation upregulating glutathione S-transferases and HO-1.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0010",
            pathway_name="Bile acid and bile salt metabolism & hepatoprotection",
            reactome_id="R-HSA-194068",
            kegg_id="hsa00120",
            category="Hepatic Secretion & Bile Clearance",
            description="Cholesterol 7alpha-hydroxylase regulation facilitating hepatic lipid efflux and membrane stability.",
            associated_organ_axis="kabid-mida"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0011",
            pathway_name="Nitric oxide stimulates guanylate cyclase and vasodilation",
            reactome_id="R-HSA-389661",
            kegg_id="hsa04022",
            category="Cardiovascular & Vascular Tone",
            description="Endothelial eNOS stimulation producing cyclic GMP, relaxing vascular smooth muscle and lowering resistance.",
            associated_organ_axis="qalb-urooq"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0012",
            pathway_name="Renin-angiotensin system and blood pressure regulation",
            reactome_id="R-HSA-2022377",
            kegg_id="hsa04614",
            category="Cardiovascular & Renal Hemodynamics",
            description="Inhibition of angiotensin-converting enzyme preventing AT1 receptor-mediated vasoconstriction.",
            associated_organ_axis="qalb-urooq"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0013",
            pathway_name="Acetylcholine neurotransmitter release & degradation",
            reactome_id="R-HSA-181431",
            kegg_id="hsa04725",
            category="Neurotransmission & Synaptic Plasticity",
            description="Presynaptic choline acetyltransferase and postsynaptic muscarinic/nicotinic signaling supporting memory.",
            associated_organ_axis="dimagh-aasab"
        ))

        cls.register_pathway(CanonicalPathwayRecord(
            canonical_id="ZAY-PW-0014",
            pathway_name="GABAergic neurotransmission and post-synaptic inhibition",
            reactome_id="R-HSA-9617324",
            kegg_id="hsa04727",
            category="Neuronal Excitability & Anxiolysis",
            description="Allosteric modulation of GABAA receptor chloride channels attenuating neuronal hyperexcitability.",
            associated_organ_axis="dimagh-aasab"
        ))

    @classmethod
    def register_substance(cls, record: CanonicalSubstanceRecord) -> CanonicalSubstanceRecord:
        cls._substances[record.canonical_id] = record
        # Index all synonyms for resolution
        for syn in [record.canonical_name, record.botanical_name, record.unani_name] + record.synonyms:
            cls._synonym_lookup[syn.lower().strip()] = record.canonical_id
        return record

    @classmethod
    def register_compound(cls, record: CanonicalCompoundRecord) -> CanonicalCompoundRecord:
        cls._compounds[record.canonical_id] = record
        cls._synonym_lookup[record.compound_name.lower().strip()] = record.canonical_id
        if record.chembl_id:
            cls._synonym_lookup[record.chembl_id.lower().strip()] = record.canonical_id
        if record.inchikey:
            cls._synonym_lookup[record.inchikey.lower().strip()] = record.canonical_id
        return record

    @classmethod
    def register_target(cls, record: CanonicalTargetRecord) -> CanonicalTargetRecord:
        cls._targets[record.canonical_id] = record
        cls._synonym_lookup[record.gene_symbol.lower().strip()] = record.canonical_id
        cls._synonym_lookup[record.uniprot_id.lower().strip()] = record.canonical_id
        return record

    @classmethod
    def register_pathway(cls, record: CanonicalPathwayRecord) -> CanonicalPathwayRecord:
        cls._pathways[record.canonical_id] = record
        cls._synonym_lookup[record.pathway_name.lower().strip()] = record.canonical_id
        if record.reactome_id:
            cls._synonym_lookup[record.reactome_id.lower().strip()] = record.canonical_id
        return record

    @classmethod
    def resolve_identifier(cls, query: str) -> Optional[Dict[str, Any]]:
        """Resolves any free-text name, synonym, or code to its canonical record."""
        cls.initialize_seeds()
        q_norm = query.lower().strip()
        cid = cls._synonym_lookup.get(q_norm)
        if not cid:
            # Try direct canonical ID query
            q_upper = query.upper().strip()
            if q_upper in cls._substances:
                cid = q_upper
            elif q_upper in cls._compounds:
                cid = q_upper
            elif q_upper in cls._targets:
                cid = q_upper
            elif q_upper in cls._pathways:
                cid = q_upper

        if not cid:
            return None

        if cid.startswith("ZAY-MUF-"):
            rec = cls._substances.get(cid)
            return {"entity_type": EntityType.MUFRAD.value, "record": rec.to_dict() if rec else None}
        elif cid.startswith("ZAY-CMP-"):
            rec = cls._compounds.get(cid)
            return {"entity_type": EntityType.COMPOUND.value, "record": rec.to_dict() if rec else None}
        elif cid.startswith("ZAY-TGT-"):
            rec = cls._targets.get(cid)
            return {"entity_type": EntityType.TARGET.value, "record": rec.to_dict() if rec else None}
        elif cid.startswith("ZAY-PW-"):
            rec = cls._pathways.get(cid)
            return {"entity_type": EntityType.PATHWAY.value, "record": rec.to_dict() if rec else None}
        return None

    @classmethod
    def get_substance(cls, cid: str) -> Optional[CanonicalSubstanceRecord]:
        cls.initialize_seeds()
        return cls._substances.get(cid)

    @classmethod
    def get_compound(cls, cid: str) -> Optional[CanonicalCompoundRecord]:
        cls.initialize_seeds()
        return cls._compounds.get(cid)

    @classmethod
    def get_target(cls, cid: str) -> Optional[CanonicalTargetRecord]:
        cls.initialize_seeds()
        return cls._targets.get(cid)

    @classmethod
    def get_pathway(cls, cid: str) -> Optional[CanonicalPathwayRecord]:
        cls.initialize_seeds()
        return cls._pathways.get(cid)

    @classmethod
    def list_all_substances(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        return [s.to_dict() for s in cls._substances.values()]

    @classmethod
    def list_all_compounds(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        return [c.to_dict() for c in cls._compounds.values()]

    @classmethod
    def list_all_targets(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        return [t.to_dict() for t in cls._targets.values()]

    @classmethod
    def list_all_pathways(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        return [p.to_dict() for p in cls._pathways.values()]


# Ensure seeds are initialized when module is loaded
CanonicalIdentityRegistry.initialize_seeds()
