from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.auth_dependency import CurrentUser, require_permission
from app.core.pharmacopoeia import (
    get_compound_by_name,
    get_compound_formulations,
    get_mufrad_by_name,
    get_schedule_e1_poisons,
    get_upi_mufradat,
    match_schedule_e1_substance,
)
from app.schemas.pharmacopoeia import (
    CompoundFormulationOut,
    PharmacopoeiaMonographOut,
    ScheduleE1SubstanceOut,
)

router = APIRouter(prefix="/api/v1/pharmacopoeia", tags=["pharmacopoeia-core"])


@router.get("/schedule-e1", response_model=list[ScheduleE1SubstanceOut])
def list_schedule_e1_poisons(
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    """Retrieve statutory Schedule E(1) poisons list with mandatory Mudabbar protocols and dose ceilings."""
    poisons = get_schedule_e1_poisons()
    return list(poisons.values())


@router.get("/schedule-e1/{name}", response_model=ScheduleE1SubstanceOut)
def get_schedule_e1_substance(
    name: str,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    substance = match_schedule_e1_substance(name)
    if not substance:
        raise HTTPException(status_code=404, detail=f"Schedule E(1) substance '{name}' not found")
    return substance


@router.get("/monographs", response_model=list[PharmacopoeiaMonographOut])
def list_monographs(
    is_schedule_e1: bool | None = None,
    organ_axis: str | None = None,
    search: str | None = None,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    """List classical UPI monographs with filtering by schedule, organ-axis, and keyword search."""
    items = get_upi_mufradat()
    if is_schedule_e1 is not None:
        items = [i for i in items if i["is_schedule_e1"] == is_schedule_e1]
    if organ_axis:
        items = [i for i in items if organ_axis in i.get("organ_axes", [])]
    if search:
        s = search.lower()
        items = [
            i
            for i in items
            if s in i["name"].lower()
            or s in i["botanical_name"].lower()
            or any(s in syn.lower() for syn in i.get("synonyms", []))
        ]
    return items


@router.get("/monographs/{name}", response_model=PharmacopoeiaMonographOut)
def get_monograph(
    name: str,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    item = get_mufrad_by_name(name)
    if not item:
        raise HTTPException(status_code=404, detail=f"Monograph for '{name}' not found in UPI registry")
    return item


@router.get("/compounds", response_model=list[CompoundFormulationOut])
def list_compounds(
    category: str | None = None,
    schedule_e1_only: bool = False,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    """List NFUM classical compound formulations (Murakkabat) with safety cautions."""
    compounds = get_compound_formulations()
    if category:
        compounds = [c for c in compounds if category.lower() in c["category"].lower()]
    if schedule_e1_only:
        compounds = [c for c in compounds if c["schedule_e1_warning"]]
    return compounds


@router.get("/compounds/{name}", response_model=CompoundFormulationOut)
def get_compound(
    name: str,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    comp = get_compound_by_name(name)
    if not comp:
        raise HTTPException(status_code=404, detail=f"Compound formulation '{name}' not found in NFUM registry")
    return comp
