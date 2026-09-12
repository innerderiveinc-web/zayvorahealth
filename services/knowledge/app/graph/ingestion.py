"""
Knowledge Graph Ingestion Engine for ZAYVORA HEALTH.
Extracts authenticated monographs, poisons, compounds, and taxonomies
and constructs canonical node and edge structures for Neo4j and In-Memory graphs.
"""
from __future__ import annotations

from typing import Any

from app.core.pharmacopoeia import (
    NFUM_COMPOUND_REGISTRY,
    SCHEDULE_E1_POISONS,
    UPI_MUFRADAT_REGISTRY,
)
from app.core.taxonomy import MIZAJ_TEMPERAMENTS, ORGAN_AXES


def build_canonical_graph_nodes_and_edges() -> dict[str, Any]:
    """Generates normalized graph structures from classical repositories."""
    nodes = {
        "OrganAxis": [],
        "Mizaj": [],
        "PoisonClass": [],
        "MudabbarProtocol": [],
        "Mufrad": [],
        "Murakkab": [],
    }
    edges = []

    # 1. Organ Axes
    for ax in ORGAN_AXES:
        nodes["OrganAxis"].append({
            "code": ax["code"],
            "name": ax["name"],
            "translation": ax["translation"],
            "systemsCovered": ax.get("systems_covered", ax.get("translation", "")),
        })

    # 2. Mizaj Nodes
    humor_map = {
        "Damwi": ("Dam (Blood)", "Air (Hawa)"),
        "Safrawi": ("Safra (Yellow Bile)", "Fire (Naar)"),
        "Saudawi": ("Sauda (Black Bile)", "Earth (Arz)"),
        "Balghami": ("Balgham (Phlegm)", "Water (Maa)"),
    }
    for mz in MIZAJ_TEMPERAMENTS:
        temp = mz["temperament"]
        default_humor, default_element = humor_map.get(temp, ("", ""))
        nodes["Mizaj"].append({
            "temperament": temp,
            "quality": mz.get("quality", ""),
            "humor": mz.get("humor", default_humor),
            "element": mz.get("element", default_element),
            "translation": mz.get("translation", ""),
        })

    # 3. Schedule E(1) Poisons & Detox Protocols
    for key, p in SCHEDULE_E1_POISONS.items():
        poison_class_name = p["poison_class"]
        nodes["PoisonClass"].append({
            "name": poison_class_name,
            "toxicAlkaloids": p["toxic_alkaloids"],
            "antidote": p["antidote"],
        })
        protocol_name = f"Mudabbar Protocol for {p['canonical_name']}"
        nodes["MudabbarProtocol"].append({
            "name": protocol_name,
            "targetDrug": p["canonical_name"],
            "protocol": p["mudabbar_protocol"],
        })

    # 4. Mufradat Nodes & Relationships
    for m in UPI_MUFRADAT_REGISTRY:
        m_id = m["id"]
        nodes["Mufrad"].append({
            "id": m_id,
            "name": m["name"],
            "botanicalName": m["botanical_name"],
            "partUsed": m["part_used"],
            "synonyms": m["synonyms"],
            "afal": m["afal"],
            "traditionalUses": m["traditional_uses"],
            "contraindications": m["contraindications"],
            "musleh": m["musleh"],
            "badal": m["badal"],
            "dose": m["dose"],
            "isScheduleE1": m["is_schedule_e1"],
            "modernPharmacology": m["modern_pharmacology"],
        })

        # Relationship: HAS_MIZAJ
        mz = m.get("mizaj", {})
        if mz.get("temperament"):
            edges.append({
                "type": "HAS_MIZAJ",
                "from_label": "Mufrad",
                "from_id": m_id,
                "to_label": "Mizaj",
                "to_id": mz["temperament"],
                "props": {
                    "hc_degree": mz.get("hc_degree", 0),
                    "wd_degree": mz.get("wd_degree", 0),
                    "quality": mz.get("quality", ""),
                },
            })

        # Relationship: ACTS_ON
        for axis_code in m.get("organ_axes", []):
            edges.append({
                "type": "ACTS_ON",
                "from_label": "Mufrad",
                "from_id": m_id,
                "to_label": "OrganAxis",
                "to_id": axis_code,
                "props": {},
            })

        # Link to Schedule E(1) & Mudabbar
        if m["is_schedule_e1"]:
            for _, p in SCHEDULE_E1_POISONS.items():
                if p["canonical_name"].lower() in m["name"].lower() or m["name"].lower() in p["canonical_name"].lower():
                    edges.append({
                        "type": "SCHEDULE_E1_POISON",
                        "from_label": "Mufrad",
                        "from_id": m_id,
                        "to_label": "PoisonClass",
                        "to_id": p["poison_class"],
                        "props": {
                            "statutory_warning": p["statutory_warning"],
                            "max_single_dose_mg": p["max_single_dose_mg"],
                            "max_daily_dose_mg": p["max_daily_dose_mg"],
                        },
                    })
                    edges.append({
                        "type": "REQUIRES_DETOXIFICATION",
                        "from_label": "Mufrad",
                        "from_id": m_id,
                        "to_label": "MudabbarProtocol",
                        "to_id": f"Mudabbar Protocol for {p['canonical_name']}",
                        "props": {
                            "mandatory": True,
                        },
                    })

    # 5. Murakkabat (Compound Formulations)
    for c in NFUM_COMPOUND_REGISTRY:
        c_id = c["id"]
        nodes["Murakkab"].append({
            "id": c_id,
            "name": c["name"],
            "urduName": c.get("urdu_name", ""),
            "category": c["category"],
            "classicalIndication": c["classical_indication"],
            "dose": c["dose"],
            "scheduleE1Warning": c["schedule_e1_warning"],
            "precautions": c["precautions"],
            "canonicalReference": c.get("canonical_reference", ""),
            "modernizationTags": c.get("modernization_tags", {}),
        })

        # Link ingredients
        for ing in c.get("key_ingredients", []):
            ing_name = ing["name"]
            # Look up matching Mufrad
            matched_m = next((m for m in UPI_MUFRADAT_REGISTRY if m["name"].lower() in ing_name.lower()), None)
            if matched_m:
                edges.append({
                    "type": "CONTAINS_INGREDIENT",
                    "from_label": "Murakkab",
                    "from_id": c_id,
                    "to_label": "Mufrad",
                    "to_id": matched_m["id"],
                    "props": {
                        "ingredient_name": ing_name,
                        "is_schedule_e1": ing.get("is_schedule_e1", False),
                    },
                })

    return {"nodes": nodes, "edges": edges}
