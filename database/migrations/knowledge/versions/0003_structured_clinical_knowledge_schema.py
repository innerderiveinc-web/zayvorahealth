"""Structured Clinical Knowledge, Formulation, Mizaj, Organ-Axis and Safety Schema

Revision ID: 0003_structured_clinical_knowledge
Revises: 0002_ocr_and_extraction
Create Date: 2026-09-14 00:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003_structured_clinical_knowledge"
down_revision: Union[str, None] = "0002_ocr_and_extraction"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. zkb_mufradat
    op.create_table(
        "zkb_mufradat",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name_latin", sa.String(length=255), nullable=False, index=True),
        sa.Column("canonical_name_urdu", sa.String(length=255), nullable=False),
        sa.Column("canonical_name_arabic", sa.String(length=255), nullable=False),
        sa.Column("canonical_name_english", sa.String(length=255), nullable=True),
        sa.Column("botanical_name", sa.String(length=255), nullable=False),
        sa.Column("upi_code", sa.String(length=64), unique=True, nullable=True),
        sa.Column("origin_category", sa.String(length=32), nullable=False, server_default="VEGETABLE"),
        sa.Column("plant_part_used", sa.String(length=128), nullable=True),
        sa.Column("mizaj_primary_quality", sa.String(length=32), nullable=False),
        sa.Column("mizaj_degree", sa.Integer(), nullable=False),
        sa.Column("mizaj_secondary_quality", sa.String(length=32), nullable=True),
        sa.Column("mizaj_secondary_degree", sa.Integer(), nullable=True),
        sa.Column("is_schedule_e1_poison", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mandatory_mudabbar", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mudabbar_protocol", sa.Text(), nullable=True),
        sa.Column("historical_dose", sa.String(length=128), nullable=True),
        sa.Column("approved_single_dose_max_grams", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column("approved_daily_dose_max_grams", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column("therapeutic_actions", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("badal_substitutes", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("musleh_correctives", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("pregnancy_status", sa.String(length=32), nullable=False, server_default="CAUTION"),
        sa.Column("lactation_status", sa.String(length=32), nullable=False, server_default="CAUTION"),
        sa.Column("pediatric_status", sa.String(length=32), nullable=False, server_default="CAUTION"),
        sa.Column("geriatric_status", sa.String(length=32), nullable=False, server_default="SAFE_WITH_MONITORING"),
        sa.Column("evidence_level", sa.String(length=8), nullable=False, server_default="E2"),
        sa.Column("current_lifecycle_state", sa.String(length=32), nullable=False, server_default="CLINICALLY_APPROVED"),
        sa.Column("safe_for_ai", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 2. zkb_murakkabat
    op.create_table(
        "zkb_murakkabat",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("canonical_name_urdu", sa.String(length=255), nullable=False),
        sa.Column("canonical_name_english", sa.String(length=255), nullable=False, index=True),
        sa.Column("dosage_form", sa.String(length=64), nullable=False),
        sa.Column("nfum_code", sa.String(length=64), nullable=True),
        sa.Column("primary_organ_axis", sa.String(length=64), nullable=False),
        sa.Column("therapeutic_objective", sa.Text(), nullable=False),
        sa.Column("overall_mizaj", sa.String(length=64), nullable=False),
        sa.Column("approved_single_dose_min_grams", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column("approved_single_dose_max_grams", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column("approved_daily_dose_max_grams", sa.Numeric(precision=6, scale=3), nullable=False),
        sa.Column("anupan_vehicle", sa.String(length=128), nullable=False),
        sa.Column("shelf_life_months", sa.Integer(), nullable=False, server_default="36"),
        sa.Column("manufacturing_protocol", sa.Text(), nullable=False),
        sa.Column("evidence_level", sa.String(length=8), nullable=False, server_default="E2"),
        sa.Column("current_lifecycle_state", sa.String(length=32), nullable=False, server_default="CLINICALLY_APPROVED"),
        sa.Column("safe_for_ai", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 3. zkb_murakkabat_ingredients
    op.create_table(
        "zkb_murakkabat_ingredients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("murakkab_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("zkb_murakkabat.id"), nullable=False, index=True),
        sa.Column("mufradat_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("zkb_mufradat.id"), nullable=False, index=True),
        sa.Column("quantity_ratio", sa.Numeric(precision=7, scale=4), nullable=False),
        sa.Column("processing_stage", sa.String(length=64), nullable=False, server_default="Fine Powder"),
        sa.Column("is_chief_active_ingredient", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("requires_mudabbar_proof", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    # 4. zkb_diseases
    op.create_table(
        "zkb_diseases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("unani_name_arabic", sa.String(length=255), nullable=False),
        sa.Column("unani_name_urdu", sa.String(length=255), nullable=False),
        sa.Column("transliterated_name", sa.String(length=255), nullable=False, index=True),
        sa.Column("icd11_code", sa.String(length=32), nullable=True),
        sa.Column("snomed_ct_id", sa.String(length=64), nullable=True),
        sa.Column("biomedical_mapping_type", sa.String(length=64), nullable=False, server_default="phenotypic_cluster"),
        sa.Column("primary_organ_axis", sa.String(length=64), nullable=False),
        sa.Column("pathology_mizaj_derangement", sa.String(length=64), nullable=False),
        sa.Column("predominant_maddah", sa.String(length=64), nullable=True),
        sa.Column("clinical_manifestations", sa.Text(), nullable=False),
        sa.Column("treatment_principles", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # 5. zkb_safety_rules
    op.create_table(
        "zkb_safety_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rule_code", sa.String(length=64), unique=True, nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("contraindication_cohort", sa.String(length=64), nullable=False),
        sa.Column("severity_level", sa.String(length=16), nullable=False),
        sa.Column("clinical_rationale", sa.Text(), nullable=False),
        sa.Column("regulatory_source", sa.String(length=128), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    # 6. zkb_drug_interactions
    op.create_table(
        "zkb_drug_interactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("mufradat_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("zkb_mufradat.id"), nullable=False, index=True),
        sa.Column("modern_drug_class", sa.String(length=128), nullable=False),
        sa.Column("interaction_mechanism", sa.String(length=255), nullable=False),
        sa.Column("clinical_effect", sa.Text(), nullable=False),
        sa.Column("risk_severity", sa.String(length=16), nullable=False),
        sa.Column("recommended_action", sa.String(length=64), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("zkb_drug_interactions")
    op.drop_table("zkb_safety_rules")
    op.drop_table("zkb_diseases")
    op.drop_table("zkb_murakkabat_ingredients")
    op.drop_table("zkb_murakkabat")
    op.drop_table("zkb_mufradat")
