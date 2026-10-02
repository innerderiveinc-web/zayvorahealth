"""
Therapeutic Core domain models (ZAYVORA Clinical Architecture Specification v4.0 §14-19 Ilaj
bil-Dawa/Nuskha Nawisi/Nuskha Compiler, §15 Ilaj bil-Tadbeer, §16 Ilaj
bil-Ghiza).

Clinical Authority Guardrail (§2, §19): a NuskhaDraft is created with
status='draft' and a Safety Firewall verdict computed and stored at
creation time. It can NEVER be created directly as 'approved' — moving to
'approved' is a separate, permission-gated action
(POST /nuskha-drafts/{id}/approve), and if the stored safety verdict is
DO_NOT_RECOMMEND or REFER, that approval is blocked unless the approver
also holds safety_firewall.override and supplies a logged justification.
See routers/nuskha.py for the enforcement; this module only defines the
shape.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, JSON, String, Text, Boolean, Integer, Float, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def _now() -> datetime:
    return datetime.now(timezone.utc)


class NuskhaDraft(Base):
    __tablename__ = "nuskha_drafts"
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'approved', 'rejected')",
            name="chk_nuskha_draft_status",
        ),
        CheckConstraint(
            "(status != 'approved') OR (status = 'approved' AND reviewed_by_user_id IS NOT NULL)",
            name="chk_nuskha_approved_reviewer",
        ),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    # Nuskha Nawisi sequence fields (§18) — captured in the order clinical
    # reasoning actually happens, not just as a flat ingredient list.
    mizaj_context: Mapped[dict] = mapped_column(JSON, default=dict)  # patient's current Mizaj snapshot
    asbab: Mapped[str] = mapped_column(Text, default="")  # causes
    tashkhis: Mapped[str] = mapped_column(Text, default="")  # diagnosis/assessment
    organ_axis_context: Mapped[list] = mapped_column(JSON, default=list)  # axis codes involved
    usool_e_ilaj: Mapped[str] = mapped_column(Text, default="")  # treatment principle
    therapeutic_objective: Mapped[str] = mapped_column(Text, default="")
    ingredients: Mapped[list] = mapped_column(JSON, default=list)  # [{name, mufrad_id, afal, miqdaar, musleh, badal}]
    dosage_form: Mapped[str] = mapped_column(String(100), default="")
    dose: Mapped[str] = mapped_column(String(200), default="")
    timing: Mapped[str] = mapped_column(String(200), default="")
    duration: Mapped[str] = mapped_column(String(200), default="")
    parhez: Mapped[str] = mapped_column(Text, default="")  # dietary restrictions during treatment

    # Safety Firewall result — computed once at creation, never silently
    # recomputed/overwritten afterward (a changed ingredient list requires
    # a new draft, preserving the audit trail of what was actually checked).
    safety_verdict: Mapped[str] = mapped_column(String(30), nullable=False)
    safety_reasons: Mapped[list] = mapped_column(JSON, default=list)

    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft | approved | rejected
    reviewed_by_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    clinician_registration_number: Mapped[str] = mapped_column(String(100), default="")
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str] = mapped_column(Text, default="")
    safety_override_justification: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class TadbeerPlan(Base):
    """Ilaj bil-Tadbeer (§15) — a structured non-pharmacological
    intervention record, never reduced to a free-text lifestyle
    paragraph."""

    __tablename__ = "tadbeer_plans"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(40), nullable=False)  # regimen|rest|physical_activity|massage|bathing|other
    indication: Mapped[str] = mapped_column(Text, default="")
    method: Mapped[str] = mapped_column(Text, default="")
    frequency: Mapped[str] = mapped_column(String(100), default="")
    duration: Mapped[str] = mapped_column(String(100), default="")
    contraindications: Mapped[str] = mapped_column(Text, default="")
    practitioner_requirements: Mapped[str] = mapped_column(Text, default="")
    safety_verdict: Mapped[str] = mapped_column(String(30), default="SAFE_TO_CONSIDER")
    safety_reasons: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active | completed | discontinued
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class GhizaPlan(Base):
    """Ilaj bil-Ghiza (§16) — a structured dietary intervention, not
    generic advice."""

    __tablename__ = "ghiza_plans"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    dietary_goals: Mapped[str] = mapped_column(Text, default="")
    meal_structure: Mapped[str] = mapped_column(Text, default="")
    foods_recommended: Mapped[list] = mapped_column(JSON, default=list)
    foods_to_limit: Mapped[list] = mapped_column(JSON, default=list)
    hydration_guidance: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class UnifiedCarePlan(Base):
    """Unified Multi-Horizon Care Plan Engine.
    
    Synthesizes the core Unani triad:
    1. Ilaj bil-Dawa (Medicinal Formulations / Nuskha)
    2. Ilaj bil-Tadbeer (Regimenal Therapies / Evacuation & Retention)
    3. Ilaj bil-Ghiza (Dietetics / Temperament-aligned Nutrition)
    4. Asbab Sittah Daruriyyah (Six Essential Pre-requisites of Health)
    
    Clinical Authority Guardrail:
    safe_to_lock remains False and status remains 'draft' until an authorized
    registered clinician explicitly reviews, verifies posology and safety,
    and signs the care plan with their statutory registration number.
    """

    __tablename__ = "unified_care_plans"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    encounter_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    created_by_user_id: Mapped[str] = mapped_column(String(64), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    horizon: Mapped[str] = mapped_column(String(30), default="stabilization")  # acute | stabilization | maintenance
    duration_days: Mapped[int] = mapped_column(Integer, default=30)

    # Core Clinical & Temperamental Context
    mizaj_context: Mapped[dict] = mapped_column(JSON, default=dict)
    usool_e_ilaj: Mapped[str] = mapped_column(Text, default="")
    primary_indication: Mapped[str] = mapped_column(String(255), default="")

    # The 3 Therapeutic Branches
    ilaj_bid_dawa: Mapped[list] = mapped_column(JSON, default=list)  # Nuskha items or approved draft IDs
    ilaj_bit_tadbeer: Mapped[list] = mapped_column(JSON, default=list)  # Tadbeer regimens prescribed
    ilaj_bil_ghiza: Mapped[dict] = mapped_column(JSON, default=dict)  # Recommended & restricted foods, meal schedule

    # Asbab Sittah Daruriyyah (6 Essential Pre-requisites of Health)
    asbab_sittah: Mapped[dict] = mapped_column(JSON, default=dict)

    # Review Milestones & Prognosis
    review_milestones: Mapped[list] = mapped_column(JSON, default=list)
    prognosis_notes: Mapped[str] = mapped_column(Text, default="")

    # Clinician Authority & Statutory Locking Guardrail
    safe_to_lock: Mapped[bool] = mapped_column(Boolean, default=False)
    signed_by_clinician_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    clinician_registration_number: Mapped[str] = mapped_column(String(100), default="")
    signed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft | active | completed | discontinued
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)


class InventoryBatch(Base):
    """ZAYVORA Pharmacy OS Inventory Batch Model (Phase 13).
    Tracks physical batches, FEFO expiry dates, and mandatory Mudabbar certificates.
    """
    __tablename__ = "inventory_batches"
    __table_args__ = (
        CheckConstraint(
            "(is_schedule_e1 = FALSE) OR (is_schedule_e1 = TRUE AND mudabbar_certified = TRUE AND mudabbar_certificate_number IS NOT NULL)",
            name="chk_schedule_e1_mudabbar",
        ),
    )

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    medication_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    formulation_type: Mapped[str] = mapped_column(String(50), default="murakkab")
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    manufacturer: Mapped[str] = mapped_column(String(255), default="ZAYVORA GMP Dispensary")
    manufacturing_date: Mapped[str] = mapped_column(String(50), nullable=False)
    expiry_date: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    initial_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    available_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), default="g")
    is_schedule_e1: Mapped[bool] = mapped_column(Boolean, default=False)
    mudabbar_certified: Mapped[bool] = mapped_column(Boolean, default=False)
    mudabbar_certificate_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    qc_release_status: Mapped[str] = mapped_column(String(30), default="released")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class DispenseRecord(Base):
    """ZAYVORA Pharmacy OS Dispense Audit Record (Phase 13).
    Links prescription fulfillment to specific batch, pharmacist, and Mudabbar verification.
    """
    __tablename__ = "dispense_records"

    id: Mapped[uuid.UUID] = _uuid_pk()
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    prescription_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    batch_number: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity_dispensed: Mapped[float] = mapped_column(Float, nullable=False)
    dispensed_by_pharmacist_id: Mapped[str] = mapped_column(String(64), nullable=False)
    pharmacist_license_number: Mapped[str] = mapped_column(String(100), nullable=False)
    patient_counseling_notes: Mapped[str] = mapped_column(Text, default="")
    mudabbar_verified_at_dispense: Mapped[bool] = mapped_column(Boolean, default=False)
    dispensed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


