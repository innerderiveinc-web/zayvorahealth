from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class ScheduleE1SubstanceOut(BaseModel):
    id: str
    canonical_name: str
    urdu_name: str
    botanical_name: str
    family: str
    part_used: str
    synonyms: list[str]
    mizaj: dict[str, Any]
    toxic_alkaloids: list[str]
    poison_class: str
    mandatory_mudabbar: bool
    mudabbar_protocol: str
    musleh: str
    badal: str
    max_single_dose_mg: float
    max_daily_dose_mg: float
    therapeutic_window: str
    antidote: str
    statutory_warning: str


class CompoundIngredient(BaseModel):
    name: str
    is_schedule_e1: bool = False


class CompoundFormulationOut(BaseModel):
    id: str
    name: str
    urdu_name: str
    category: str
    classical_indication: str
    key_ingredients: list[CompoundIngredient]
    dose: str
    schedule_e1_warning: bool
    precautions: str


class PharmacopoeiaMonographOut(BaseModel):
    id: str
    name: str
    botanical_name: str
    part_used: str
    synonyms: list[str]
    afal: list[str]
    mizaj: dict[str, Any]
    organ_axes: list[str]
    traditional_uses: str
    contraindications: str
    musleh: str
    badal: str
    dose: str
    is_schedule_e1: bool
    modern_pharmacology: str
