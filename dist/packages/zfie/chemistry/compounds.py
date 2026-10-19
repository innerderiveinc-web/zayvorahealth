"""
ZFIE Chemistry Domain: Canonical Phytochemical Compounds
Stores normalized 2D/3D chemical structures, molecular properties, and SMILES.
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CanonicalCompound:
    canonical_id: str                   # e.g., ZAY-CMP-0001
    common_name: str                    # e.g., Colchicine
    iupac_name: str
    molecular_formula: str              # C22H25NO6
    molecular_weight: float             # 399.44
    smiles: str
    inchikey: str
    pubchem_cid: int
    log_p: float
    polar_surface_area: float
    h_bond_donors: int
    h_bond_acceptors: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


_COMPOUNDS = {
    "ZAY-CMP-0001": CanonicalCompound(
        canonical_id="ZAY-CMP-0001",
        common_name="Colchicine",
        iupac_name="N-[(7S)-1,2,3,10-tetramethoxy-9-oxo-5,6,7,9-tetrahydrobenzo[a]heptalen-7-yl]acetamide",
        molecular_formula="C22H25NO6",
        molecular_weight=399.44,
        smiles="CC(=O)N[C@@H]1CCC2=CC(=C(C(=C2C3=CC=C(C(=O)C=C13)OC)OC)OC)OC",
        inchikey="IAKHMKGGTNLKSZ-INIZCTEOSA-N",
        pubchem_cid=6167,
        log_p=1.3,
        polar_surface_area=83.0,
        h_bond_donors=1,
        h_bond_acceptors=6
    ),
    "ZAY-CMP-0002": CanonicalCompound(
        canonical_id="ZAY-CMP-0002",
        common_name="Piperine",
        iupac_name="(2E,4E)-5-(1,3-benzodioxol-5-yl)-1-piperidin-1-ylpenta-2,4-dien-1-one",
        molecular_formula="C17H19NO3",
        molecular_weight=285.34,
        smiles="C1CCN(CC1)C(=O)/C=C/C=C/C2=CC3=C(C=C2)OCO3",
        inchikey="MXXWOMGUGJBKIW-YPCIICBESA-N",
        pubchem_cid=638024,
        log_p=2.8,
        polar_surface_area=38.8,
        h_bond_donors=0,
        h_bond_acceptors=3
    ),
    "ZAY-CMP-0003": CanonicalCompound(
        canonical_id="ZAY-CMP-0003",
        common_name="Guggulsterone E",
        iupac_name="(17E)-pregna-4,17-diene-3,16-dione",
        molecular_formula="C21H28O2",
        molecular_weight=312.45,
        smiles="CC1=CC(=O)CC2C1(CCC3C2CCC4(C3CC(=O)C4=C/C)C)C",
        inchikey="BQZCSORZCVQCSN-YMMAPLKPSA-N",
        pubchem_cid=6450098,
        log_p=3.5,
        polar_surface_area=34.1,
        h_bond_donors=0,
        h_bond_acceptors=2
    ),
    "ZAY-CMP-0004": CanonicalCompound(
        canonical_id="ZAY-CMP-0004",
        common_name="Withaferin A",
        iupac_name="4-hydroxy-5,6-epoxy-1-oxo-ergost-2-en-26-oic acid",
        molecular_formula="C28H38O6",
        molecular_weight=470.6,
        smiles="CC1=C(C(=O)OC1C(C)C2CCC3C2(CCC4C3C5C(O5)C(C=CC4=O)O)C)CO",
        inchikey="SIHQGZNVNWVOBS-VLVYOFINSA-N",
        pubchem_cid=265237,
        log_p=2.2,
        polar_surface_area=96.2,
        h_bond_donors=2,
        h_bond_acceptors=6
    )
}


class CompoundRegistry:
    @classmethod
    def get(cls, cid: str) -> Optional[CanonicalCompound]:
        return _COMPOUNDS.get(cid)

    @classmethod
    def list_all(cls) -> List[CanonicalCompound]:
        return list(_COMPOUNDS.values())
