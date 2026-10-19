"""
ZFIE Formulation Adapter: ZAYVORAFormulationAdapter
Translates existing clinical Nuskha / Prescription items into a canonical
ComputationalFormulationTwin representation.
Does NOT modify or mutate the original clinical Nuskha record.
"""

from typing import Any, Dict, List, Optional
from packages.zfie.formulation.formulation_twin import (
    ComputationalFormulationTwin,
    FormulaIngredient,
    FormulationTwinRegistry
)
from packages.zfie.identity.synonym_resolution import SynonymResolver


class ZAYVORAFormulationAdapter:
    """Read-only translation layer between Clinical Nuskha and ZFIE Computational Models."""

    @classmethod
    def nuskha_to_formulation_twin(cls, nuskha_data: Dict[str, Any]) -> ComputationalFormulationTwin:
        """
        Translates an existing Nuskha item (Mufradat list, quantities, preparation)
        into a canonical formulation twin without altering the database Nuskha record.
        """
        nuskha_id = nuskha_data.get("id") or nuskha_data.get("prescription_id", "NUSKHA-LOCAL")
        title = nuskha_data.get("name") or nuskha_data.get("title", "Clinical Master Compound")
        raw_items = nuskha_data.get("items") or nuskha_data.get("ingredients", [])

        ingredients: List[FormulaIngredient] = []
        total_qty = sum(float(i.get("quantity_g", 1.0)) for i in raw_items) or 1.0

        for item in raw_items:
            name = item.get("name") or item.get("herb_name", "Herbal Ingredient")
            qty = float(item.get("quantity_g", 1.0))
            ratio = round(qty / total_qty, 3)

            canonical_id = SynonymResolver.resolve_to_canonical_id(name) or f"ZAY-MUF-GEN-{abs(hash(name)) % 10000}"
            ingredients.append(
                FormulaIngredient(
                    mufrad_id=canonical_id,
                    botanical_name=item.get("botanical_name", name),
                    vernacular_name=name,
                    ratio=ratio,
                    part_used=item.get("part", "Dried Aerial Parts / Root"),
                    processing_method=item.get("prep", "Traditional Matab Preparation")
                )
            )

        # Check if an existing twin matches this canonical structure
        existing = FormulationTwinRegistry.get_twin("ZAY-FORM-0001")
        if existing and existing.name.lower() in title.lower():
            return existing

        temp_twin = ComputationalFormulationTwin(
            canonical_id=f"ZAY-TWIN-{nuskha_id}",
            name=title,
            traditional_name=nuskha_data.get("traditional_name", title),
            formula_version="v1.0-CLINICAL-SNAPSHOT",
            classical_source=nuskha_data.get("source", "Attending Physician Prescriptive Formula"),
            therapeutic_target=nuskha_data.get("indication", "Clinical Encounter Objective"),
            ingredients=ingredients,
            preparation_method=nuskha_data.get("instructions", "Traditional Decoction / Safoof")
        )
        return temp_twin
