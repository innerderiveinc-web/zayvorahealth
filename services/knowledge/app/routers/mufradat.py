from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.auth_dependency import CurrentUser, require_permission
from app.schemas.knowledge import AxisLink, MizajAssign, MufradCreate, MufradDetailOut, MufradOut

router = APIRouter(prefix="/api/v1/mufradat", tags=["pharmacopoeia"])


def _repo(request: Request):
    return request.app.state.graph_repository


@router.post("", response_model=MufradOut, status_code=201)
def create_mufrad(
    payload: MufradCreate,
    request: Request,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.write")),
):
    result = _repo(request).create_mufrad(organization_id=user.organization_id, data=payload.model_dump())
    return result


@router.get("/{mufrad_id}", response_model=MufradDetailOut)
def get_mufrad(
    mufrad_id: str,
    request: Request,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    result = _repo(request).get_mufrad(organization_id=user.organization_id, mufrad_id=mufrad_id)
    if not result:
        raise HTTPException(status_code=404, detail="Mufrad not found")
    return result


@router.get("", response_model=list[MufradOut])
def list_mufradat(
    request: Request,
    organ_axis: str | None = None,
    mizaj_temperament: str | None = None,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.read")),
):
    return _repo(request).list_mufradat(
        organization_id=user.organization_id, organ_axis=organ_axis, mizaj_temperament=mizaj_temperament
    )


@router.put("/{mufrad_id}/mizaj")
def set_mizaj(
    mufrad_id: str,
    payload: MizajAssign,
    request: Request,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.write")),
):
    try:
        return _repo(request).set_mufrad_mizaj(
            organization_id=user.organization_id,
            mufrad_id=mufrad_id,
            temperament=payload.temperament,
            hc_degree=payload.hc_degree,
            wd_degree=payload.wd_degree,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{mufrad_id}/organ-axes")
def link_axis(
    mufrad_id: str,
    payload: AxisLink,
    request: Request,
    user: CurrentUser = Depends(require_permission("pharmacopoeia.write")),
):
    try:
        return _repo(request).link_mufrad_to_axis(
            organization_id=user.organization_id, mufrad_id=mufrad_id, axis_code=payload.axis_code
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
