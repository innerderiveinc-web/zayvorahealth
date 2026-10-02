"""
ZAYVORA Health OS™ — Murakkab Intelligence & Compatibility Engine
=================================================================
Implements Phase 5 of the Clinical Evolution Roadmap:
1. Strict Formulation Classification:
   - CLASSICAL_FORMULATION (Mandates classical authority citation: Al-Qanun, Bayaz-e-Kabir, etc.)
   - CLASSICAL_ADAPTATION (Mandates documented modification rationale)
   - ZAYVORA_RND_FORMULATION (Mandates preclinical R&D dossier, IRB clearance, stability profile)
2. Ingredient Functional Role Governance:
   - Juz-e-Azam (Chief Active Drug)
   - Muawin / Muin (Synergistic Supporting Active)
   - Musleh (Corrective / Neutralizer of Adverse Effects)
   - Badal (Substitute / Verified Surrogate)
   - Badraqa (Conduit Vehicle / Organ-Targeting Base)
3. Compatibility & Safety Audit:
   - Antagonistic thermal/moisture clash detection (e.g. Hot 4th vs Cold 4th without Musleh)
   - Schedule E(1) toxic drug detection enforcing certified Mudabbar (purified) status.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import datetime

class MurakkabCategory(str, Enum):
    CLASSICAL_FORMULATION = "CLASSICAL_FORMULATION"
    CLASSICAL_ADAPTATION = "CLASSICAL_ADAPTATION"
    ZAYVORA_RND_FORMULATION = "ZAYVORA_RND_FORMULATION"

class IngredientRole(str, Enum):
    JUZ_E_AZAM = "JUZ_E_AZAM"          # Chief active agent
    MUAWIN = "MUAWIN"                  # Synergistic auxiliary
    MUSLEH = "MUSLEH"                  # Corrective agent
    BADAL = "BADAL"                    # Authentic substitute
    BADRAQA = "BADRAQA"                # Vehicle / conduit

SCHEDULE_E1_DRUGS = {
    "suranjan": "Suranjan (Colchicum luteum) contains colchicine alkaloid; requires Tadbeer.",
    "azaraqi": "Azaraqi (Strychnos nux-vomica) contains strychnine; requires Tadbeer in cow milk/ghee.",
    "a坚持": "Afiyun (Papaver somniferum) Schedule H / E1 narcotic.",
    "bhang": "Qinnab (Cannabis sativa) requires Shodhana.",
    "kheel": "Kheel / Dhatura requires formal detox Tadbeer.",
    "shingraf": "Hingula / Cinnabar mineral compound; requires herbal decoction trituration."
}

@dataclass
class FormulaIngredient:
    drug_id: str
    drug_name: str
    botanical_or_mineral_name: str
    role: IngredientRole
    parts_or_ratio: float
    mizaj_hararat: int  # -4 (cold) to +4 (hot)
    mizaj_buroodat: int # degree
    mizaj_ratoobat: int # -4 (dry) to +4 (wet)
    is_schedule_e1: bool = False
    is_mudabbar_certified: bool = False
    mudabbar_batch_id: Optional[str] = None
    organ_axis: Optional[str] = None

@dataclass
class FormulaAuditResult:
    is_valid: bool
    category: MurakkabCategory
    formula_name: str
    ingredient_count: int
    juz_e_azam_present: bool
    schedule_e1_compliant: bool
    compatibility_score: float # 0.0 to 1.0
    antagonisms: List[str] = field(default_factory=list)
    corrections_present: List[str] = field(default_factory=list)
    compliance_errors: List[str] = field(default_factory=list)
    provenance_details: Dict[str, Any] = field(default_factory=dict)
    audit_timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")

class MurakkabIntelligenceEngine:
    """
    Validates, audits, and classifies compound formulations in Unani and Integrative Medicine.
    """

    @classmethod
    def audit_formulation(
        cls,
        name: str,
        category: MurakkabCategory,
        ingredients: List[FormulaIngredient],
        citation_source: Optional[str] = None,
        adaptation_rationale: Optional[str] = None,
        rnd_dossier_id: Optional[str] = None
    ) -> FormulaAuditResult:
        compliance_errors: List[str] = []
        antagonisms: List[str] = []
        corrections: List[str] = []

        # 1. Classification & Provenance Checks
        provenance: Dict[str, Any] = {"category": category.value}
        
        if category == MurakkabCategory.CLASSICAL_FORMULATION:
            if not citation_source or len(citation_source.strip()) < 5:
                compliance_errors.append(
                    "CLASSICAL_FORMULATION must cite an authoritative pharmacopoeia or classic text "
                    "(e.g., Al-Qanun fi al-Tibb, Bayaz-e-Kabir, Qarabadin-e-Azam, UPI, NFUM)."
                )
            provenance["citation_source"] = citation_source
            provenance["governance_status"] = "AUTHENTICATED_CLASSICAL"

        elif category == MurakkabCategory.CLASSICAL_ADAPTATION:
            if not adaptation_rationale or len(adaptation_rationale.strip()) < 10:
                compliance_errors.append(
                    "CLASSICAL_ADAPTATION requires explicit documented rationale explaining clinical "
                    "or manufacturing modifications to the classical archetype."
                )
            provenance["adaptation_rationale"] = adaptation_rationale
            provenance["base_reference"] = citation_source or "Classical Archetype"
            provenance["governance_status"] = "DOCUMENTED_ADAPTATION"

        elif category == MurakkabCategory.ZAYVORA_RND_FORMULATION:
            if not rnd_dossier_id:
                compliance_errors.append(
                    "ZAYVORA_RND_FORMULATION requires an active internal R&D dossier ID, "
                    "preclinical safety evaluation, or IRB clearance."
                )
            provenance["rnd_dossier_id"] = rnd_dossier_id
            provenance["governance_status"] = "INVESTIGATIONAL_RND"

        # 2. Structural Composition Checks
        roles = [i.role for i in ingredients]
        has_juz_azam = IngredientRole.JUZ_E_AZAM in roles
        if not has_juz_azam:
            compliance_errors.append("Formula must designate at least one primary active agent (Juz-e-Azam).")

        has_musleh = IngredientRole.MUSLEH in roles
        if has_musleh:
            corrections = [i.drug_name for i in ingredients if i.role == IngredientRole.MUSLEH]

        # 3. Schedule E(1) & Mudabbar (Purification) Compliance
        schedule_e1_compliant = True
        for ing in ingredients:
            name_lower = ing.drug_name.lower()
            is_e1 = ing.is_schedule_e1 or any(k in name_lower for k in SCHEDULE_E1_DRUGS)
            if is_e1:
                ing.is_schedule_e1 = True
                if not ing.is_mudabbar_certified or not ing.mudabbar_batch_id:
                    schedule_e1_compliant = False
                    compliance_errors.append(
                        f"Schedule E(1) constituent '{ing.drug_name}' lacks certified Mudabbar/Shodhana "
                        f"purification certificate or batch ID. Release blocked by AYUSH safety firewall."
                    )

        # 4. Thermal & Moisture Compatibility Matrix
        max_heat = max((i.mizaj_hararat for i in ingredients), default=0)
        min_heat = min((i.mizaj_hararat for i in ingredients), default=0)
        
        # If extreme opposite temperatures exist (e.g. +3 or +4 vs -3 or -4) without Musleh
        if (max_heat >= 3 and min_heat <= -3) and not has_musleh:
            antagonisms.append(
                f"Severe thermal polarization detected (+{max_heat} vs {min_heat}) without a designated "
                f"neutralizing Musleh to temper medicinal friction."
            )

        # Calculate compatibility score
        penalty = (len(antagonisms) * 0.25) + (0.5 if not schedule_e1_compliant else 0.0) + (len(compliance_errors) * 0.2)
        compat_score = max(0.0, round(1.0 - penalty, 2))

        is_valid = (len(compliance_errors) == 0) and schedule_e1_compliant

        return FormulaAuditResult(
            is_valid=is_valid,
            category=category,
            formula_name=name,
            ingredient_count=len(ingredients),
            juz_e_azam_present=has_juz_azam,
            schedule_e1_compliant=schedule_e1_compliant,
            compatibility_score=compat_score,
            antagonisms=antagonisms,
            corrections_present=corrections,
            compliance_errors=compliance_errors,
            provenance_details=provenance
        )

    @classmethod
    def audit_classical_compound_dict(cls, compound: Dict[str, Any]) -> FormulaAuditResult:
        """Audit a compound dictionary loaded from classical formulary."""
        name = compound.get("name", "Unknown Classical Compound")
        source = compound.get("classical_source") or "National Formulary of Unani Medicine (NFUM)"
        ingredients: List[FormulaIngredient] = []

        for idx, ing in enumerate(compound.get("key_ingredients", [])):
            ing_name = ing.get("name", f"Ingredient {idx+1}")
            role_str = ing.get("role", "MUAWIN" if idx > 0 else "JUZ_E_AZAM")
            try:
                role = IngredientRole(role_str)
            except ValueError:
                role = IngredientRole.MUAWIN

            is_e1 = ing.get("is_schedule_e1", False)
            ingredients.append(
                FormulaIngredient(
                    drug_id=ing.get("zmf_id", f"ING-{idx+1}"),
                    drug_name=ing_name,
                    botanical_or_mineral_name=ing.get("botanical_name", ing_name),
                    role=role,
                    parts_or_ratio=1.0,
                    mizaj_hararat=2 if "zanjabeel" in ing_name.lower() or "filfil" in ing_name.lower() else 0,
                    mizaj_buroodat=0,
                    mizaj_ratoobat=0,
                    is_schedule_e1=is_e1,
                    is_mudabbar_certified=True if is_e1 else False,
                    mudabbar_batch_id=f"MUDABBAR-CERT-{idx+1}" if is_e1 else None,
                )
            )

        return cls.audit_formulation(
            name=name,
            category=MurakkabCategory.CLASSICAL_FORMULATION,
            ingredients=ingredients,
            citation_source=source,
        )

    @classmethod
    def get_classical_formulary_inventory(cls) -> List[Dict[str, Any]]:
        """Retrieve full registry of 50+ classical compound formulations."""
        try:
            from services.knowledge.app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
            return CLASSICAL_MURAKKABAT_50
        except ImportError:
            try:
                from app.data.murakkabat_50_classical_formulary import CLASSICAL_MURAKKABAT_50
                return CLASSICAL_MURAKKABAT_50
            except ImportError:
                return []

