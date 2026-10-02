"""
ZAYVORA Health OS™ — Global Clinical Knowledge Localization Engine (Phase 26)
=============================================================================
Provides cross-jurisdictional regulatory compliance, pharmacopoeial mapping,
and legal labeling generation for Unani & botanical therapeutics across 5 key authorities:

1. India (AYUSH / D&C Act 1940 & Rules 1945, First Schedule Pharmacopoeias, Schedule E1)
2. United States (FDA Botanical Drug Guidance FDA-2015-D-2479, DSHEA 1994, 21 CFR 111)
3. European Union (EMA HMPC, THMPD 2004/24/EC, Directive 2001/83/EC Article 10a WEU)
4. GCC & Middle East (SFDA CAM Regulations, Gulf Health Council Herbal Registration)
5. Global / WHO (WHO Traditional Medicine Strategy 2025-2034, ICD-11 TM Module)
"""

from __future__ import annotations

import enum
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


class RegulatoryJurisdiction(str, enum.Enum):
    IN_AYUSH = "IN_AYUSH"          # Ministry of AYUSH, Drugs & Cosmetics Act 1940
    US_FDA = "US_FDA"              # US FDA CDER Botanical Review Team / DSHEA
    EU_EMA = "EU_EMA"              # EMA Committee on Herbal Medicinal Products (HMPC)
    GCC_SFDA = "GCC_SFDA"          # Saudi FDA & Gulf Health Council CAM Division
    WHO_GLOBAL = "WHO_GLOBAL"      # WHO Traditional, Complementary & Integrative Medicine


class RegulatoryCategory(str, enum.Enum):
    APPROVED_BOTANICAL_DRUG = "APPROVED_BOTANICAL_DRUG"
    TRADITIONAL_HERBAL_MEDICINE = "TRADITIONAL_HERBAL_MEDICINE"   # EMA THMPD / AYUSH Classical
    DIETARY_SUPPLEMENT = "DIETARY_SUPPLEMENT"                     # US DSHEA / GCC Health Product
    PRESCRIPTION_ONLY_SCHEDULE_E1 = "PRESCRIPTION_ONLY_SCHEDULE_E1"
    RESTRICTED_MAX_DAILY_DOSE = "RESTRICTED_MAX_DAILY_DOSE"
    PROHIBITED_UNAPPROVED = "PROHIBITED_UNAPPROVED"


@dataclass
class JurisdictionMonographRule:
    jurisdiction: RegulatoryJurisdiction
    category: RegulatoryCategory
    legal_status_summary: str
    max_daily_dose_mg: Optional[float]
    requires_prescription: bool
    is_prohibited: bool
    mandatory_label_warning: str
    statutory_citations: List[str]


@dataclass
class LocalizedDrugCrosswalk:
    drug_id: str
    classical_name_urdu: str
    transliterated_name: str
    botanical_name: str
    family: str
    jurisdiction_rules: Dict[RegulatoryJurisdiction, JurisdictionMonographRule]


@dataclass
class PrescriptionLocalizationAudit:
    target_jurisdiction: RegulatoryJurisdiction
    is_fully_compliant: bool
    eligible_product_class: str
    prohibited_items: List[str]
    restricted_dose_items: List[str]
    mandatory_label_statements: List[str]
    package_insert_advisories: List[str]
    regulatory_citations: List[str]
    audit_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GlobalLocalizationEngine:
    """
    Cross-jurisdictional clinical regulatory and pharmacopoeial crosswalk engine.
    Ensures safe, legally defensible international deployment of Unani therapeutics.
    """

    # Comprehensive Curated Monograph Crosswalk for Classical Botanicals
    CROSSWALK_REGISTRY: Dict[str, LocalizedDrugCrosswalk] = {
        "ASGANDH": LocalizedDrugCrosswalk(
            drug_id="MM-ASG-001",
            classical_name_urdu="اسگندھ",
            transliterated_name="Asgandh",
            botanical_name="Withania somnifera (L.) Dunal",
            family="Solanaceae",
            jurisdiction_rules={
                RegulatoryJurisdiction.IN_AYUSH: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.IN_AYUSH,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="Official in Unani Pharmacopoeia of India (UPI Vol I). Non-Schedule E1.",
                    max_daily_dose_mg=6000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Ayurvedic/Unani medicine. Store in a cool dry place.",
                    statutory_citations=["UPI Part I, Vol I, p. 19", "D&C Rules 1945 First Schedule"],
                ),
                RegulatoryJurisdiction.US_FDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.US_FDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="Admissible as Dietary Supplement under DSHEA 1994. Eligible for Botanical IND.",
                    max_daily_dose_mg=1500.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning=(
                        "These statements have not been evaluated by the Food and Drug Administration. "
                        "This product is not intended to diagnose, treat, cure, or prevent any disease."
                    ),
                    statutory_citations=["FDA Botanical Guidance Docket FDA-2015-D-2479", "DSHEA Section 403(r)(6)"],
                ),
                RegulatoryJurisdiction.EU_EMA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.EU_EMA,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="EMA HMPC Community Herbal Monograph (Traditional Use for stress and exhaustion).",
                    max_daily_dose_mg=1000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="The use in children and adolescents under 18 years of age is not recommended.",
                    statutory_citations=["Directive 2004/24/EC (THMPD)", "EMA/HMPC/582379/2020"],
                ),
                RegulatoryJurisdiction.GCC_SFDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.GCC_SFDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="SFDA Listed Herbal & Health Product. Requires standardized withanolide assay.",
                    max_daily_dose_mg=1200.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Do not exceed the recommended daily dose. Consult healthcare practitioner if pregnant.",
                    statutory_citations=["SFDA Guidelines for Herbal Products 2022", "GDR-CAM Registration Manual"],
                ),
                RegulatoryJurisdiction.WHO_GLOBAL: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.WHO_GLOBAL,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="WHO Monographs on Selected Medicinal Plants Vol 4. Adaptogenic/Muqawwi.",
                    max_daily_dose_mg=3000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Follow recognized traditional pharmacopoeial posology.",
                    statutory_citations=["WHO Monographs Vol 4, Radix Withaniae", "WHO Traditional Medicine Strategy 2025-2034"],
                ),
            },
        ),
        "SURANJAN_TALKH": LocalizedDrugCrosswalk(
            drug_id="MM-SUR-002",
            classical_name_urdu="سورنجان تلخ",
            transliterated_name="Suranjan Talkh",
            botanical_name="Colchicum luteum Baker",
            family="Colchicaceae",
            jurisdiction_rules={
                RegulatoryJurisdiction.IN_AYUSH: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.IN_AYUSH,
                    category=RegulatoryCategory.PRESCRIPTION_ONLY_SCHEDULE_E1,
                    legal_status_summary="Statutory Schedule E(1) Poison. Mandatory Mudabbar purification (Tadbir).",
                    max_daily_dose_mg=250.0,
                    requires_prescription=True,
                    is_prohibited=False,
                    mandatory_label_warning="CAUTION: SCHEDULE E(1) POISON. To be taken strictly under medical supervision.",
                    statutory_citations=["D&C Rules 1945, Schedule E(1) Item 17", "UPI Part I, Vol II"],
                ),
                RegulatoryJurisdiction.US_FDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.US_FDA,
                    category=RegulatoryCategory.PROHIBITED_UNAPPROVED,
                    legal_status_summary="Prohibited in Dietary Supplements due to colchicine alkaloid toxicity. Prescription NDA/IND only.",
                    max_daily_dose_mg=0.0,
                    requires_prescription=True,
                    is_prohibited=True,
                    mandatory_label_warning="PROHIBITED in OTC supplements. Prescription only active pharmaceutical ingredient.",
                    statutory_citations=["21 CFR 314 (New Drug Approval)", "FDA Colchicine Safety Alert"],
                ),
                RegulatoryJurisdiction.EU_EMA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.EU_EMA,
                    category=RegulatoryCategory.PROHIBITED_UNAPPROVED,
                    legal_status_summary="Not eligible for THMPD simplified registration due to narrow therapeutic index of colchicine.",
                    max_daily_dose_mg=0.0,
                    requires_prescription=True,
                    is_prohibited=True,
                    mandatory_label_warning="Prescription only medicinal product under Directive 2001/83/EC.",
                    statutory_citations=["Directive 2001/83/EC Article 70", "EMA HMPC Safety Position on Colchicum"],
                ),
                RegulatoryJurisdiction.GCC_SFDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.GCC_SFDA,
                    category=RegulatoryCategory.PRESCRIPTION_ONLY_SCHEDULE_E1,
                    legal_status_summary="SFDA Toxic Botanical Schedule. Dispensing restricted to licensed specialist CAM hospitals.",
                    max_daily_dose_mg=200.0,
                    requires_prescription=True,
                    is_prohibited=False,
                    mandatory_label_warning="PRESCRIPTION ONLY. High toxicity potential. Strict medical monitoring required.",
                    statutory_citations=["SFDA Restricted Botanicals List 2021"],
                ),
                RegulatoryJurisdiction.WHO_GLOBAL: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.WHO_GLOBAL,
                    category=RegulatoryCategory.RESTRICTED_MAX_DAILY_DOSE,
                    legal_status_summary="High-potency alkaloidal drug. Documented anti-inflammatory with rigorous detox.",
                    max_daily_dose_mg=250.0,
                    requires_prescription=True,
                    is_prohibited=False,
                    mandatory_label_warning="Strict toxicological posology limits apply.",
                    statutory_citations=["WHO Quality Control Methods for Herbal Materials"],
                ),
            },
        ),
        "ZANJABEEL": LocalizedDrugCrosswalk(
            drug_id="MM-ZAN-003",
            classical_name_urdu="زنجبیل",
            transliterated_name="Zanjabeel",
            botanical_name="Zingiber officinale Roscoe",
            family="Zingiberaceae",
            jurisdiction_rules={
                RegulatoryJurisdiction.IN_AYUSH: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.IN_AYUSH,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="Official in UPI Vol I. Classic Kasir-e-Riyah & Hazim stimulant.",
                    max_daily_dose_mg=3000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Store protected from moisture.",
                    statutory_citations=["UPI Part I, Vol I"],
                ),
                RegulatoryJurisdiction.US_FDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.US_FDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="FDA GRAS (Generally Recognized As Safe) 21 CFR 182.20 & Dietary Supplement.",
                    max_daily_dose_mg=4000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="These statements have not been evaluated by the FDA.",
                    statutory_citations=["21 CFR 182.20 GRAS", "DSHEA 1994"],
                ),
                RegulatoryJurisdiction.EU_EMA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.EU_EMA,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="EMA HMPC Monograph (Well-Established Use for motion sickness; Traditional use for digestive discomfort).",
                    max_daily_dose_mg=2000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Do not use in children under 6 years of age for motion sickness without medical advice.",
                    statutory_citations=["EMA/HMPC/749154/2010"],
                ),
                RegulatoryJurisdiction.GCC_SFDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.GCC_SFDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="SFDA Listed Approved Botanical for digestive and circulatory support.",
                    max_daily_dose_mg=3000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Consult physician if taking anti-coagulants.",
                    statutory_citations=["SFDA OTC Herbal List"],
                ),
                RegulatoryJurisdiction.WHO_GLOBAL: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.WHO_GLOBAL,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="WHO Monographs on Selected Medicinal Plants Vol 1 (Rhizoma Zingiberis).",
                    max_daily_dose_mg=4000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Antiemetic and carminative.",
                    statutory_citations=["WHO Monographs Vol 1, Rhizoma Zingiberis"],
                ),
            },
        ),
        "USTUKHUDDUS": LocalizedDrugCrosswalk(
            drug_id="MM-UST-004",
            classical_name_urdu="استخودوس",
            transliterated_name="Ustukhuddus",
            botanical_name="Lavandula stoechas L.",
            family="Lamiaceae",
            jurisdiction_rules={
                RegulatoryJurisdiction.IN_AYUSH: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.IN_AYUSH,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="Official in UPI Vol II. Premier Jarub-e-Dimagh (Brain cleanser/nervine).",
                    max_daily_dose_mg=7000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Store protected from light.",
                    statutory_citations=["UPI Part I, Vol II"],
                ),
                RegulatoryJurisdiction.US_FDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.US_FDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="Dietary supplement botanical for relaxation and calm.",
                    max_daily_dose_mg=2000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="These statements have not been evaluated by the FDA.",
                    statutory_citations=["DSHEA 1994"],
                ),
                RegulatoryJurisdiction.EU_EMA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.EU_EMA,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="EMA HMPC Monograph on Lavandula (traditional use for mental stress and sleep).",
                    max_daily_dose_mg=1500.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="If symptoms persist longer than 2 weeks, consult a physician.",
                    statutory_citations=["EMA/HMPC/143181/2010"],
                ),
                RegulatoryJurisdiction.GCC_SFDA: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.GCC_SFDA,
                    category=RegulatoryCategory.DIETARY_SUPPLEMENT,
                    legal_status_summary="Approved herbal health ingredient for neuro-cognitive support.",
                    max_daily_dose_mg=2500.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Not intended for pregnancy without physician consult.",
                    statutory_citations=["SFDA CAM Guidelines"],
                ),
                RegulatoryJurisdiction.WHO_GLOBAL: JurisdictionMonographRule(
                    jurisdiction=RegulatoryJurisdiction.WHO_GLOBAL,
                    category=RegulatoryCategory.TRADITIONAL_HERBAL_MEDICINE,
                    legal_status_summary="WHO Traditional Medicine benchmark botanical for cephalic disorders.",
                    max_daily_dose_mg=5000.0,
                    requires_prescription=False,
                    is_prohibited=False,
                    mandatory_label_warning="Follow official Unani pharmacopoeia administration.",
                    statutory_citations=["WHO TM Benchmarks"],
                ),
            },
        ),
    }

    @classmethod
    def get_crosswalk(cls, drug_canonical_key: str) -> Optional[LocalizedDrugCrosswalk]:
        """Looks up cross-jurisdictional monograph by canonical drug key."""
        key = drug_canonical_key.strip().upper().replace(" ", "_")
        return cls.CROSSWALK_REGISTRY.get(key)

    @classmethod
    def audit_prescription_for_jurisdiction(
        cls,
        drug_items: List[Dict[str, Any]],
        target_jurisdiction: RegulatoryJurisdiction,
    ) -> PrescriptionLocalizationAudit:
        """
        Audits a multi-ingredient prescription against statutory rules of the destination jurisdiction.
        Checks admissibility, dosage caps, prescription requirements, and compiles legal packaging text.
        """
        prohibited: List[str] = []
        restricted: List[str] = []
        mandatory_warnings: set[str] = set()
        citations: set[str] = set()
        has_prescription_requirement = False

        for item in drug_items:
            raw_name = item.get("drug_name", "")
            norm_key = raw_name.upper().replace(" ", "_")
            dose_mg = float(item.get("daily_dose_mg", 0.0))

            # Match against crosswalk registry
            matched_entry: Optional[LocalizedDrugCrosswalk] = None
            for k, entry in cls.CROSSWALK_REGISTRY.items():
                if k in norm_key or norm_key in k or entry.transliterated_name.upper() in norm_key:
                    matched_entry = entry
                    break

            if matched_entry and target_jurisdiction in matched_entry.jurisdiction_rules:
                rule = matched_entry.jurisdiction_rules[target_jurisdiction]

                if rule.is_prohibited:
                    prohibited.append(f"{matched_entry.transliterated_name} ({matched_entry.botanical_name}) - Prohibited in {target_jurisdiction.value}")

                if rule.max_daily_dose_mg is not None and dose_mg > rule.max_daily_dose_mg:
                    restricted.append(
                        f"{matched_entry.transliterated_name}: Dose {dose_mg}mg exceeds statutory maximum {rule.max_daily_dose_mg}mg/day"
                    )

                if rule.requires_prescription:
                    has_prescription_requirement = True

                mandatory_warnings.add(rule.mandatory_label_warning)
                citations.update(rule.statutory_citations)
            else:
                # Uncatalogued botanical default check
                if target_jurisdiction == RegulatoryJurisdiction.US_FDA:
                    mandatory_warnings.add(
                        "These statements have not been evaluated by the FDA. Not intended to diagnose, treat, cure, or prevent any disease."
                    )
                elif target_jurisdiction == RegulatoryJurisdiction.IN_AYUSH:
                    mandatory_warnings.add("Ayurvedic/Unani medicine. To be taken under medical guidance.")

        is_compliant = len(prohibited) == 0 and len(restricted) == 0

        # Determine product classification
        if has_prescription_requirement:
            product_class = "PRESCRIPTION_ONLY_HERBAL_MEDICINE"
        elif target_jurisdiction == RegulatoryJurisdiction.US_FDA:
            product_class = "DIETARY_SUPPLEMENT"
        elif target_jurisdiction == RegulatoryJurisdiction.EU_EMA:
            product_class = "TRADITIONAL_HERBAL_MEDICINAL_PRODUCT_(THMP)"
        elif target_jurisdiction == RegulatoryJurisdiction.IN_AYUSH:
            product_class = "AYUSH_CLASSICAL_UNANI_MEDICINE"
        else:
            product_class = "CAM_HEALTH_PRODUCT"

        package_inserts = [
            f"Authorized Product Class: {product_class}",
            f"Target Regulatory Jurisdiction: {target_jurisdiction.value}",
            "Batch traceability to source pharmacopoeia authenticated by ZAYVORA Health OS™.",
        ]
        if has_prescription_requirement:
            package_inserts.append("RESTRICTION: Medical prescription by registered practitioner required prior to dispensing.")

        return PrescriptionLocalizationAudit(
            target_jurisdiction=target_jurisdiction,
            is_fully_compliant=is_compliant,
            eligible_product_class=product_class,
            prohibited_items=prohibited,
            restricted_dose_items=restricted,
            mandatory_label_statements=sorted(list(mandatory_warnings)),
            package_insert_advisories=package_inserts,
            regulatory_citations=sorted(list(citations)),
        )
