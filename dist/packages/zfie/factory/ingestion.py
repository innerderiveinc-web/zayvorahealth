"""
ZAYVORA Formulation Intelligence Engine™ (ZFIE)
Layer 1: Scientific Data Factory — ETL, Ingestion & Normalization
System: ZAYVORA Health OS™
Doctrine: Public/Licensed Source -> Parsing -> Resolution -> Normalization -> Extraction -> Review -> Authoritative Commit
"""

import hashlib
import time
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum


class IngestionSourceType(str, Enum):
    PUBLIC_REPOSITORY = "PUBLIC_REPOSITORY"  # PubChem, ChEMBL, UniProt, Reactome
    PHARMACOPOEIA = "PHARMACOPOEIA"          # UPI, NFUM, IP, WHO
    CLASSICAL_CANON = "CLASSICAL_CANON"      # Al-Qanun, Kamil al-Sina'a, Makhzan al-Adwiya
    LABORATORY_LIMS = "LABORATORY_LIMS"      # HPLC, LC-MS, NMR, Bioassay raw streams
    PEER_REVIEWED_LIT = "PEER_REVIEWED_LIT"  # PubMed, PMC, ScienceDirect


class ReviewStatus(str, Enum):
    STAGED = "STAGED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@dataclass
class LicenseMetadata:
    source_name: str
    license_type: str  # CC-BY-4.0, ODC-By, Proprietary, AYUSH Academic
    commercial_use_allowed: bool
    attribution_required: bool
    redistribution_allowed: bool
    source_uri: str
    terms_version: str = "v1.0"


@dataclass
class StagedScientificRecord:
    staging_id: str
    source_type: IngestionSourceType
    source_name: str
    source_version: str
    raw_payload: Dict[str, Any]
    normalized_entity: Dict[str, Any]
    evidence_claims: List[Dict[str, Any]]
    license_meta: LicenseMetadata
    checksum: str
    review_status: ReviewStatus = ReviewStatus.STAGED
    reviewer_notes: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["source_type"] = self.source_type.value
        d["review_status"] = self.review_status.value
        return d


class ScientificDataFactory:
    """Enterprise ETL & Ingestion Engine for scientific literature and chemistry databases."""

    _STAGING_LEDGER: Dict[str, StagedScientificRecord] = {}

    @classmethod
    def ingest_payload(
        cls,
        source_type: IngestionSourceType,
        source_name: str,
        source_version: str,
        payload: Dict[str, Any],
        license_meta: LicenseMetadata
    ) -> StagedScientificRecord:
        """
        Ingests a raw payload from an external source, normalizes it,
        extracts candidate claims, computes provenance hash, and stages it for scientific review.
        """
        staging_id = f"STG-{uuid.uuid4().hex[:8].upper()}"
        raw_repr = str(sorted(payload.items())).encode("utf-8")
        checksum = hashlib.sha256(raw_repr).hexdigest()

        # Normalization and entity resolution
        normalized = cls._normalize_payload(source_type, payload)

        # Evidence claims extraction
        extracted_claims = cls._extract_evidence_claims(source_type, normalized)

        record = StagedScientificRecord(
            staging_id=staging_id,
            source_type=source_type,
            source_name=source_name,
            source_version=source_version,
            raw_payload=payload,
            normalized_entity=normalized,
            evidence_claims=extracted_claims,
            license_meta=license_meta,
            checksum=checksum,
            review_status=ReviewStatus.STAGED
        )

        cls._STAGING_LEDGER[staging_id] = record
        return record

    @classmethod
    def _normalize_payload(cls, source_type: IngestionSourceType, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes entities across languages, chemical formats, and nomenclatures."""
        norm: Dict[str, Any] = {
            "canonical_name": payload.get("canonical_name") or payload.get("pref_name") or payload.get("name", "Unknown"),
            "identifiers": {},
            "properties": {}
        }

        # Chemistry normalization
        if "smiles" in payload or "canonical_smiles" in payload:
            norm["properties"]["smiles"] = (payload.get("canonical_smiles") or payload.get("smiles", "")).strip()
        if "inchikey" in payload:
            norm["identifiers"]["inchikey"] = payload["inchikey"].strip().upper()
        if "chembl_id" in payload:
            norm["identifiers"]["chembl_id"] = payload["chembl_id"].strip().upper()
        if "pubchem_cid" in payload:
            norm["identifiers"]["pubchem_cid"] = int(payload["pubchem_cid"])

        # Molecular target normalization
        if "uniprot_id" in payload:
            norm["identifiers"]["uniprot_id"] = payload["uniprot_id"].strip().upper()
        if "target_organism" in payload:
            norm["properties"]["organism"] = payload["target_organism"].strip()

        # Classical botanicals normalization
        if "latin_name" in payload:
            norm["properties"]["latin_name"] = payload["latin_name"].strip()
        if "unani_name" in payload:
            norm["properties"]["unani_name"] = payload["unani_name"].strip()

        return norm

    @classmethod
    def _extract_evidence_claims(cls, source_type: IngestionSourceType, normalized: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts candidate claims without silent promotion to fact."""
        claims = []
        if source_type in (IngestionSourceType.PHARMACOPOEIA, IngestionSourceType.CLASSICAL_CANON):
            claims.append({
                "statement": f"Classical therapeutic documentation for {normalized.get('canonical_name')}",
                "evidence_level": "E0",
                "evidence_status": "TRADITIONAL_CLAIM",
                "origin": "CURATED"
            })
        elif source_type == IngestionSourceType.PUBLIC_REPOSITORY:
            claims.append({
                "statement": f"Repository entity profile for {normalized.get('canonical_name')}",
                "evidence_level": "E2",
                "evidence_status": "COMPUTATIONALLY_PREDICTED",
                "origin": "CALCULATED"
            })
        return claims

    @classmethod
    def review_record(cls, staging_id: str, approved: bool, reviewer_id: str, notes: str = "") -> StagedScientificRecord:
        """Human/Scientific Review Board gate before entering ZKB or production ZFIE."""
        if staging_id not in cls._STAGING_LEDGER:
            raise KeyError(f"Staged record {staging_id} not found.")

        record = cls._STAGING_LEDGER[staging_id]
        record.review_status = ReviewStatus.APPROVED if approved else ReviewStatus.REJECTED
        record.reviewer_notes = f"Reviewed by {reviewer_id}: {notes}"
        return record

    @classmethod
    def list_staged(cls, status: Optional[ReviewStatus] = None) -> List[Dict[str, Any]]:
        if status:
            return [r.to_dict() for r in cls._STAGING_LEDGER.values() if r.review_status == status]
        return [r.to_dict() for r in cls._STAGING_LEDGER.values()]
