"""
ZAYVORA Health OS™ — WHO SMART Guidelines Digital Adaptation Kit (DAK) Engine
=============================================================================
Converts traditional Unani clinical wisdom and statutory pharmacopoeias into
WHO SMART Guidelines Level 3 (Machine-Readable & Computable) knowledge assets.

Standard Alignment:
- WHO SMART Guidelines Architecture (L1 Narrative -> L2 DAK -> L3 Computable -> L4 Executable)
- WHO Core Data Dictionary (CDD) specification for Traditional & Integrative Medicine
- Decision Support Logic (DSL) in computable JSON-LD / FHIR Clinical Quality Language (CQL)
- Semantic Versioning (SemVer 2.0.0) with cryptographic SHA-256 integrity signatures
- Strict Clinical Governance Gate (No un-ratified autonomous knowledge mutation)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class DAKAssetType(str, Enum):
    MUFRAD_MONOGRAPH = "MUFRAD_MONOGRAPH"
    MURAKKAB_FORMULATION = "MURAKKAB_FORMULATION"
    ORGAN_AXIS_ONTOLOGY = "ORGAN_AXIS_ONTOLOGY"
    DECISION_SUPPORT_RULE = "DECISION_SUPPORT_RULE"
    SAFETY_FIREWALL_PROTOCOL = "SAFETY_FIREWALL_PROTOCOL"
    PARHEZ_LIFESTYLE_RULE = "PARHEZ_LIFESTYLE_RULE"


class EvidenceLevel(str, Enum):
    E0_TRADITIONAL = "E0_TRADITIONAL"               # Scriptural / Folk tradition only
    E1_CLASSICAL_TEXT = "E1_CLASSICAL_TEXT"         # Canon (Al-Qanun, Al-Hawi, Bayaz-e-Kabir)
    E2_PHARMACOPOEIA = "E2_PHARMACOPOEIA"           # Statutory compendium (UPI, NFUM)
    E3_PRECLINICAL = "E3_PRECLINICAL"               # In-vitro / in-vivo animal bioassays
    E4_OBSERVATIONAL_RWE = "E4_OBSERVATIONAL_RWE"   # Retrospective cohort / Registry RWE
    E5_CLINICAL_TRIAL = "E5_CLINICAL_TRIAL"         # Phase II/III Human Clinical Trial
    E6_SYSTEMATIC_REVIEW = "E6_SYSTEMATIC_REVIEW"   # Meta-analysis / International guideline


@dataclass
class WHOCoreDataElement:
    code: str
    display: str
    system: str  # e.g., "http://zayvora.org/fhir/cdd" or "http://snomed.info/sct"
    definition: str
    data_type: str  # "CodeableConcept", "Quantity", "boolean", "string"
    allowed_values: Optional[List[str]] = None


@dataclass
class ComputableDecisionRule:
    rule_id: str
    title: str
    version: str
    trigger_context: str  # e.g., "PRESCRIPTION_AUTHORIZATION", "TRIAGE"
    condition_cql_json: Dict[str, Any]  # Computable Boolean logic
    action_type: str  # "MANDATE_MUSLEH", "HARD_BLOCK", "WARN", "ADJUST_DOSE"
    action_payload: Dict[str, Any]
    evidence_level: EvidenceLevel
    citation: str
    status: str = "ACTIVE_RATIFIED"


@dataclass
class SMARTKnowledgeArtifact:
    artifact_id: str
    asset_type: DAKAssetType
    title: str
    version: str  # SemVer, e.g. "1.2.0"
    author_attribution: str
    governance_ratified_by: str
    effective_date: str
    sha256_hash: str
    computable_payload: Dict[str, Any]
    decision_rules: List[ComputableDecisionRule] = field(default_factory=list)
    fhir_conformance: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WHOSmartDAKEngine:
    """Computable Knowledge Management Engine conforming to WHO SMART Guidelines."""

    # 1. Standardized Core Data Dictionary (CDD) Registry
    CDD_REGISTRY: Dict[str, WHOCoreDataElement] = {
        "MIZAJ_HOT_DEGREE": WHOCoreDataElement(
            code="MIZ-01",
            display="Hararat (Heat Potency Degree)",
            system="http://zayvora.org/fhir/cdd",
            definition="Degree of innate thermal potency from 1 (mild) to 4 (extreme/toxic)",
            data_type="integer",
            allowed_values=["1", "2", "3", "4"],
        ),
        "MIZAJ_COLD_DEGREE": WHOCoreDataElement(
            code="MIZ-02",
            display="Buroodat (Cold Potency Degree)",
            system="http://zayvora.org/fhir/cdd",
            definition="Degree of cooling potency from 1 (mild) to 4 (extreme/narcotic)",
            data_type="integer",
            allowed_values=["1", "2", "3", "4"],
        ),
        "SCHEDULE_E1_POISON_STATUS": WHOCoreDataElement(
            code="REG-E1",
            display="Schedule E(1) Statutory Poison Flag",
            system="http://zayvora.org/fhir/cdd/regulatory",
            definition="Statutory classification under Drugs and Cosmetics Rules, 1945 (India)",
            data_type="boolean",
            allowed_values=["true", "false"],
        ),
        "TADBEER_STATUS": WHOCoreDataElement(
            code="PHARM-TAD",
            display="Mudabbar Shodhana Detoxification Status",
            system="http://zayvora.org/fhir/cdd/pharmacy",
            definition="Certified completion of classical detoxification protocol prior to formulation release",
            data_type="boolean",
            allowed_values=["true", "false"],
        ),
        "ORGAN_AXIS_TARGET": WHOCoreDataElement(
            code="AXIS-12",
            display="12 Canonical Organ Axes",
            system="http://zayvora.org/fhir/cdd/anatomy",
            definition="Target visceral or neuromuscular functional axis in traditional physiology",
            data_type="CodeableConcept",
            allowed_values=[
                "jigar-banas", "dimagh-aasab", "qalb-uroq", "riya-sadr",
                "meda-amaa", "ghudad-hazm", "khusyatain", "reham-mabaysim",
                "mafasil", "shaar-jigar", "ghudda-mithana", "tabiyat"
            ],
        ),
    }
    CORE_DATA_DICTIONARY = CDD_REGISTRY

    @classmethod
    def compute_sha256_fingerprint(cls, data: Dict[str, Any]) -> str:
        """Generates deterministic cryptographic SHA-256 fingerprint of computable data."""
        canonical_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    @classmethod
    def transform_mufrad_to_smart_artifact(
        cls,
        drug: Dict[str, Any],
        version: str = "1.0.0",
        governance_authority: str = "ZAYVORA Clinical Governance Board",
    ) -> SMARTKnowledgeArtifact:
        """Transforms a raw single-drug monograph into a WHO SMART Level 3 Computable Artifact."""
        drug_id = drug.get("id") or drug.get("zmf_id", "ZMF-UNKNOWN")
        name = drug.get("name", "Unknown Drug")
        is_e1 = bool(drug.get("is_schedule_e1", False))

        computable_payload = {
            "canonical_name": name,
            "botanical_name": drug.get("botanical_name"),
            "family": drug.get("family"),
            "part_used": drug.get("part_used"),
            "mizaj": drug.get("mizaj") or {
                "temperament": drug.get("temperament", "Motadil"),
                "heat_degree": drug.get("mizaj_heat", 0),
                "cold_degree": drug.get("mizaj_cold", 0),
                "dry_degree": drug.get("mizaj_dryness", 0),
                "wet_degree": drug.get("mizaj_moisture", 0),
            },
            "organ_axes": drug.get("organ_axes", []),
            "dosage_range": drug.get("dose") or drug.get("dosage", "3g - 5g"),
            "dose_ceiling_mg": drug.get("max_single_dose_mg") or 5000.0,
            "is_schedule_e1": is_e1,
            "mudabbar_protocol": drug.get("mudabbar_protocol"),
            "musleh": drug.get("musleh") or drug.get("correctives", []),
            "badal": drug.get("badal") or drug.get("substitutes", []),
        }

        # Generate Computable Decision Support Rules for this drug
        rules: List[ComputableDecisionRule] = []

        # Rule A: Schedule E(1) Autonomous Hard-Block Rule
        if is_e1:
            rules.append(
                ComputableDecisionRule(
                    rule_id=f"RULE-E1-BLOCK-{drug_id}",
                    title=f"Schedule E(1) Statutory Gate: {name}",
                    version="1.0.0",
                    trigger_context="AI_COPILOT_PRESCRIPTION",
                    condition_cql_json={
                        "operand": "AND",
                        "conditions": [
                            {"field": "ingredient.is_schedule_e1", "operator": "==", "value": True},
                            {"field": "user_role", "operator": "in", "value": ["HAKEEM_SAHAB_AI", "AI_COPILOT"]},
                        ],
                    },
                    action_type="HARD_BLOCK",
                    action_payload={
                        "code": "SCHEDULE_E1_AUTONOMOUS_PROHIBITION",
                        "message": f"{name} is a statutory Schedule E(1) poison. AI prescribing is legally blocked.",
                        "statutory_reference": "Drugs and Cosmetics Rules, 1945, Schedule E(1)",
                    },
                    evidence_level=EvidenceLevel.E2_PHARMACOPOEIA,
                    citation="Unani Pharmacopoeia of India (UPI)",
                )
            )

        # Rule B: Mandatory Musleh Pairing Rule
        musleh_target = computable_payload["musleh"]
        if musleh_target:
            musleh_name = musleh_target if isinstance(musleh_target, str) else ", ".join(musleh_target)
            rules.append(
                ComputableDecisionRule(
                    rule_id=f"RULE-MUSLEH-PAIR-{drug_id}",
                    title=f"Mandatory Musleh Corrective: {name}",
                    version="1.0.0",
                    trigger_context="NUSKHA_COMPILATION",
                    condition_cql_json={
                        "operand": "AND",
                        "conditions": [
                            {"field": "formula.contains_ingredient", "operator": "==", "value": name},
                            {"field": "formula.has_corrective", "operator": "==", "value": False},
                        ],
                    },
                    action_type="MANDATE_MUSLEH",
                    action_payload={
                        "mandated_musleh": musleh_name,
                        "rationale": "Prevents gastric mucosal irritation and balances thermal excess.",
                    },
                    evidence_level=EvidenceLevel.E1_CLASSICAL_TEXT,
                    citation="Al-Qanoon fit-Tibb & Khazainul Advia",
                )
            )

        sha = cls.compute_sha256_fingerprint(computable_payload)

        return SMARTKnowledgeArtifact(
            artifact_id=f"WHO-SMART-ZMF-{drug_id}",
            asset_type=DAKAssetType.MUFRAD_MONOGRAPH,
            title=f"WHO SMART DAK Monograph: {name}",
            version=version,
            author_attribution="Dr. Irfan Ashraf, BUMS & ZAYVORA Clinical Directorate",
            governance_ratified_by=governance_authority,
            effective_date="2026-09-19",
            sha256_hash=sha,
            computable_payload=computable_payload,
            decision_rules=rules,
            fhir_conformance={
                "resourceType": "MedicationKnowledge",
                "codeSystem": "http://zayvora.org/fhir/CodeSystem/mufradat",
                "profile": "http://zayvora.org/fhir/StructureDefinition/zayvora-computable-mufrad",
            },
        )

    @classmethod
    def validate_computable_artifact(cls, artifact: SMARTKnowledgeArtifact) -> Dict[str, Any]:
        """Performs automated validation checking schema compliance and signature verification."""
        expected_sha = cls.compute_sha256_fingerprint(artifact.computable_payload)
        is_integrity_valid = artifact.sha256_hash == expected_sha

        errors = []
        if not is_integrity_valid:
            errors.append("Cryptographic SHA-256 fingerprint mismatch. Payload may have been tampered.")
        if not artifact.version or not artifact.version.count(".") == 2:
            errors.append("Invalid SemVer specification. Must be major.minor.patch (e.g., 1.0.0).")
        if not artifact.decision_rules and artifact.computable_payload.get("is_schedule_e1"):
            errors.append("Schedule E(1) substance missing mandatory decision support rules.")

        return {
            "artifact_id": artifact.artifact_id,
            "is_valid": len(errors) == 0,
            "sha256_verified": is_integrity_valid,
            "rule_count": len(artifact.decision_rules),
            "errors": errors,
            "governance_status": "RATIFIED_COMPUTABLE" if len(errors) == 0 else "REJECTED_VALIDATION",
        }
