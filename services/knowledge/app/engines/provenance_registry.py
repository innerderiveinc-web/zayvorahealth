"""
ZAYVORA HEALTH OS™ — Provenance & License Registry
Governed Scientific Intelligence Layer (Blueprint §12, §43, §44)

Maintains an immutable record of external data sources, biological ontologies,
and analytical databases ensuring intellectual property compliance, open-source
licensing governance, and data traceability.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class LicenseType(str, Enum):
    CC_BY_SA_3_0 = "CC-BY-SA-3.0"
    CC_BY_4_0 = "CC-BY-4.0"
    CC0_PUBLIC_DOMAIN = "CC0-1.0"
    ODBL = "ODbL-1.0"
    GOVERNMENT_STATUTORY = "GOVERNMENT_STATUTORY_OPEN"
    ZAYVORA_PROPRIETARY = "ZAYVORA_PROPRIETARY"


@dataclass
class KnowledgeSourceRecord:
    source_id: str                         # e.g., "SRC-CHEMBL", "SRC-REACTOME", "SRC-UPI"
    source_name: str                       # e.g., "ChEMBL Bioactivity Database"
    organization: str                      # e.g., "European Bioinformatics Institute (EMBL-EBI)"
    website_url: str
    license_type: LicenseType
    commercial_use_allowed: bool
    mandatory_attribution: str
    version_or_release: str                # e.g., "Release 33", "UPI Vol I-VI (2016-2022)"
    last_synchronized_at: str              # ISO timestamp
    record_count: int
    data_domain: str                       # e.g., "Bioactivity & Target Binding", "Biological Pathways"
    sha256_integrity_hash: str = ""

    def __post_init__(self):
        if not self.sha256_integrity_hash:
            raw = f"{self.source_id}:{self.version_or_release}:{self.license_type.value}:{self.commercial_use_allowed}"
            self.sha256_integrity_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ProvenanceLicenseRegistry:
    """Authoritative repository for knowledge source provenance and licensing governance."""

    _registry: Dict[str, KnowledgeSourceRecord] = {}

    @classmethod
    def initialize_seeds(cls) -> None:
        if cls._registry:
            return

        # 1. ChEMBL
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-CHEMBL",
            source_name="ChEMBL Database",
            organization="European Bioinformatics Institute (EMBL-EBI)",
            website_url="https://www.ebi.ac.uk/chembl/",
            license_type=LicenseType.CC_BY_SA_3_0,
            commercial_use_allowed=True,
            mandatory_attribution="Data sourced from ChEMBL database (EMBL-EBI) under CC-BY-SA 3.0 license.",
            version_or_release="ChEMBL_33",
            last_synchronized_at="2026-08-01T00:00:00Z",
            record_count=2350000,
            data_domain="Bioactivity, Drug-Target Binding Affinities, IC50/Ki values"
        ))

        # 2. Reactome
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-REACTOME",
            source_name="Reactome Pathway Knowledgebase",
            organization="Reactome Consortium (NYU Langone, OICR, EBI)",
            website_url="https://reactome.org",
            license_type=LicenseType.CC0_PUBLIC_DOMAIN,
            commercial_use_allowed=True,
            mandatory_attribution="Reactome pathway definitions utilized under Creative Commons Public Domain (CC0 1.0).",
            version_or_release="Reactome Version 86",
            last_synchronized_at="2026-08-01T00:00:00Z",
            record_count=2640,
            data_domain="Human Biological Pathways and Molecular Reactions"
        ))

        # 3. Open Targets
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-OPEN-TARGETS",
            source_name="Open Targets Platform",
            organization="Open Targets Consortium (EMBL-EBI, Wellcome Sanger, Industry)",
            website_url="https://platform.opentargets.org",
            license_type=LicenseType.CC_BY_4_0,
            commercial_use_allowed=True,
            mandatory_attribution="Open Targets Platform target-disease associations under CC-BY 4.0 license.",
            version_or_release="Open Targets 24.06",
            last_synchronized_at="2026-08-01T00:00:00Z",
            record_count=65000,
            data_domain="Target Validation and Target-Disease Genetic Associations"
        ))

        # 4. PubChem
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-PUBCHEM",
            source_name="PubChem",
            organization="National Center for Biotechnology Information (NCBI / NLM)",
            website_url="https://pubchem.ncbi.nlm.nih.gov",
            license_type=LicenseType.CC0_PUBLIC_DOMAIN,
            commercial_use_allowed=True,
            mandatory_attribution="National Center for Biotechnology Information (NCBI) PubChem database (Public Domain).",
            version_or_release="PubChem Snapshot 2026",
            last_synchronized_at="2026-08-01T00:00:00Z",
            record_count=115000000,
            data_domain="Chemical Structures, SMILES, InChI, Physicochemical Properties"
        ))

        # 5. Unani Pharmacopoeia of India (UPI)
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-UPI",
            source_name="Unani Pharmacopoeia of India (UPI)",
            organization="Pharmacopoeia Commission for Indian Medicine & Homoeopathy (PCIM&H), Ministry of AYUSH, Govt of India",
            website_url="https://pcimh.gov.in",
            license_type=LicenseType.GOVERNMENT_STATUTORY,
            commercial_use_allowed=True,
            mandatory_attribution="Statutory Quality Standards & Identity Monograph per Unani Pharmacopoeia of India, Ministry of AYUSH, Govt of India.",
            version_or_release="UPI Volumes I to VI (Complete Formulations & Single Drugs)",
            last_synchronized_at="2026-06-01T00:00:00Z",
            record_count=298,
            data_domain="Official AYUSH Standard Specifications, Mudabbar Protocols, TLC/HPLC Fingerprints"
        ))

        # 6. ZAYVORA Quality Control Lab Records
        cls.register_source(KnowledgeSourceRecord(
            source_id="SRC-ZAYVORA-LAB",
            source_name="ZAYVORA Analytical QC & Fingerprinting Lab",
            organization="ZAYVORA Health OS Sciences Division",
            website_url="https://zayvora.internal/qc",
            license_type=LicenseType.ZAYVORA_PROPRIETARY,
            commercial_use_allowed=True,
            mandatory_attribution="Proprietary Analytical Certificate of Analysis (CoA) & Fingerprint Dossier © ZAYVORA Health OS.",
            version_or_release="ZAY-QC-2026.09",
            last_synchronized_at="2026-09-20T00:00:00Z",
            record_count=184,
            data_domain="Internal HPLC-DAD Assay Quantification, Dissolution Testing, and Batch Certificates"
        ))

    @classmethod
    def register_source(cls, source: KnowledgeSourceRecord) -> KnowledgeSourceRecord:
        cls._registry[source.source_id] = source
        return source

    @classmethod
    def get_source(cls, source_id: str) -> Optional[KnowledgeSourceRecord]:
        cls.initialize_seeds()
        return cls._registry.get(source_id)

    @classmethod
    def list_sources(cls) -> List[Dict[str, Any]]:
        cls.initialize_seeds()
        return [s.to_dict() for s in cls._registry.values()]


# Auto-seed
ProvenanceLicenseRegistry.initialize_seeds()
