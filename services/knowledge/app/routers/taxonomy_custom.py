# services/knowledge/app/routers/taxonomy_custom.py
"""Custom taxonomy router for regional herbs and user‑defined mufrad entries.

Provides CRUD endpoints to add, retrieve, update, and delete custom taxonomy
objects stored in the Neo4j graph. The implementation uses the existing
`GraphRepository` abstraction.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.graph.repository import GraphRepository
from app.core.graph_seeder import seed_all  # placeholder to ensure DB init elsewhere

router = APIRouter(prefix="/api/v1/zkb/taxonomy_custom", tags=["Custom Taxonomy"])

# Schemas ---------------------------------------------------------------
class RegionalHerb(BaseModel):
    name: str = Field(..., description="Common name of the herb")
    scientific_name: str = Field(..., description="Botanical name")
    description: str | None = Field(None, description="Free‑text description")

class CustomMufrad(BaseModel):
    name: str = Field(..., description="Mufrad name")
    botanical_name: str | None = Field(None, description="Botanical name if known")
    mizaj: dict | None = Field(None, description="Mizaj metadata")
    afal: list[str] | None = Field(None, description="List of actions/effects")

# Dependency ------------------------------------------------------------
def get_repo() -> GraphRepository:
    # In real FastAPI this would pull from request.state; here we instantiate directly for simplicity.
    from app.graph.neo4j_repository import Neo4jGraphRepository
    from app.core.config import get_settings
    settings = get_settings()
    return Neo4jGraphRepository(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
        knowledge_db=settings.neo4j_knowledge_database,
        formula_db=settings.neo4j_formula_database,
        evidence_db=settings.neo4j_evidence_database,
        patient_db=settings.neo4j_patient_database,
    )

# CRUD endpoints ---------------------------------------------------------
@router.post("/regional_herb", response_model=RegionalHerb)
def create_regional_herb(herb: RegionalHerb, repo: GraphRepository = Depends(get_repo)):
    try:
        repo.run_cypher(
            "CREATE (h:RegionalHerb {name: $name, scientific_name: $sci, description: $desc})",
            {"name": herb.name, "sci": herb.scientific_name, "desc": herb.description},
        )
        return herb
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/regional_herb/{name}", response_model=RegionalHerb)
def get_regional_herb(name: str, repo: GraphRepository = Depends(get_repo)):
    result = repo.run_cypher(
        "MATCH (h:RegionalHerb {name: $name}) RETURN h.name AS name, h.scientific_name AS scientific_name, h.description AS description",
        {"name": name},
    )
    if not result:
        raise HTTPException(status_code=404, detail="Herb not found")
    record = result[0]
    return RegionalHerb(name=record["name"], scientific_name=record["scientific_name"], description=record.get("description"))

@router.put("/regional_herb/{name}", response_model=RegionalHerb)
def update_regional_herb(name: str, herb: RegionalHerb, repo: GraphRepository = Depends(get_repo)):
    repo.run_cypher(
        "MATCH (h:RegionalHerb {name: $name}) SET h.scientific_name = $sci, h.description = $desc",
        {"name": name, "sci": herb.scientific_name, "desc": herb.description},
    )
    return herb

@router.delete("/regional_herb/{name}")
def delete_regional_herb(name: str, repo: GraphRepository = Depends(get_repo)):
    repo.run_cypher("MATCH (h:RegionalHerb {name: $name}) DETACH DELETE h", {"name": name})
    return {"deleted": name}

# Custom Mufrad endpoints (similar pattern) --------------------------------
@router.post("/custom_mufrad", response_model=CustomMufrad)
def create_custom_mufrad(mufrad: CustomMufrad, repo: GraphRepository = Depends(get_repo)):
    repo.run_cypher(
        "CREATE (m:Mufrad {name: $name, botanical_name: $sci, mizaj: $mizaj, afal: $afal})",
        {
            "name": mufrad.name,
            "sci": mufrad.botanical_name,
            "mizaj": mufrad.mizaj,
            "afal": mufrad.afal,
        },
    )
    return mufrad

@router.get("/custom_mufrad/{name}", response_model=CustomMufrad)
def get_custom_mufrad(name: str, repo: GraphRepository = Depends(get_repo)):
    result = repo.run_cypher(
        "MATCH (m:Mufrad {name: $name}) RETURN m.name AS name, m.botanical_name AS botanical_name, m.mizaj AS mizaj, m.afal AS afal",
        {"name": name},
    )
    if not result:
        raise HTTPException(status_code=404, detail="Mufrad not found")
    rec = result[0]
    return CustomMufrad(
        name=rec["name"],
        botanical_name=rec.get("botanical_name"),
        mizaj=rec.get("mizaj"),
        afal=rec.get("afal"),
    )

@router.put("/custom_mufrad/{name}", response_model=CustomMufrad)
def update_custom_mufrad(name: str, mufrad: CustomMufrad, repo: GraphRepository = Depends(get_repo)):
    repo.run_cypher(
        "MATCH (m:Mufrad {name: $name}) SET m.botanical_name = $sci, m.mizaj = $mizaj, m.afal = $afal",
        {
            "name": name,
            "sci": mufrad.botanical_name,
            "mizaj": mufrad.mizaj,
            "afal": mufrad.afal,
        },
    )
    return mufrad

@router.delete("/custom_mufrad/{name}")
def delete_custom_mufrad(name: str, repo: GraphRepository = Depends(get_repo)):
    repo.run_cypher("MATCH (m:Mufrad {name: $name}) DETACH DELETE m", {"name": name})
    return {"deleted": name}
