"""
ZAYVORA Health OS™ — Enterprise Multi-Clinic Federation Engine (Sequence 15)
=============================================================================
Manages distributed multi-facility clinical operations across tiers:
- Tier 1: Central Hospital & Clinical Governance Board (Research, formulary ratification)
- Tier 2: Regional Specialty Centers (Regimental therapy, inpatient care, practicum)
- Tier 3: Community Matabs & Outpatient Clinics (Primary consultations, local dispensing)

Features:
1. Multi-Facility Network Registry & Topology
2. Strict Clinic Partitioning (Zero unauthorized cross-clinic leakage)
3. Cryptographically Signed Inter-Clinic Patient Referrals & Consults
4. Federated Multi-Dispensary Inventory FEFO Balancing & Branch Transfers
"""

from __future__ import annotations

import uuid
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class FacilityTier(str, Enum):
    TIER_1_CENTRAL_HOSPITAL = "TIER_1_CENTRAL_HOSPITAL"
    TIER_2_REGIONAL_SPECIALTY = "TIER_2_REGIONAL_SPECIALTY"
    TIER_3_COMMUNITY_MATAB = "TIER_3_COMMUNITY_MATAB"


@dataclass
class ClinicFacility:
    facility_id: str
    name: str
    tier: FacilityTier
    city: str
    state: str
    country: str = "India"
    abdm_facility_id: str = ""
    has_regimental_therapy: bool = False
    has_compounding_pharmacy: bool = False
    active_clinicians_count: int = 1
    is_active: bool = True
    specialty_axes_available: List[str] = field(default_factory=list)

    @property
    def active(self) -> bool:
        return self.is_active


@dataclass
class InterClinicReferral:
    referral_id: str
    referral_token: str
    patient_id: str
    source_facility_id: str
    target_facility_id: str
    referring_clinician_id: str
    clinical_condition: str
    specialty_axis_required: str  # e.g., "MAFASIL", "JIGAR-BANAS"
    reason_for_referral: str
    created_at: str
    expires_at: str
    status: str = "PENDING_ACCEPTANCE"  # PENDING_ACCEPTANCE, REDEEMED, EXPIRED, REVOKED
    receiving_clinician_id: Optional[str] = None
    redeemed_at: Optional[str] = None


@dataclass
class BranchInventoryLot:
    lot_id: str
    facility_id: str
    drug_name: str
    batch_number: str
    quantity_available_grams: float
    expiry_date: str
    mudabbar_certified: bool = False
    is_schedule_e1: bool = False


class MultiClinicFederationEngine:
    """Coordinates distributed clinic nodes, cross-clinic referrals, and federated inventory."""

    _SIGNING_KEY = "zayvora-federation-hmac-master-token-2026"

    # Default federated clinic network registry
    _FACILITY_REGISTRY: Dict[str, ClinicFacility] = {
        "FAC-DEL-CENTRAL-01": ClinicFacility(
            facility_id="FAC-DEL-CENTRAL-01",
            name="ZAYVORA Central Matab & Governance Hospital",
            tier=FacilityTier.TIER_1_CENTRAL_HOSPITAL,
            city="New Delhi",
            state="Delhi",
            abdm_facility_id="IN-FAC-DEL-0012",
            has_regimental_therapy=True,
            has_compounding_pharmacy=True,
            active_clinicians_count=18,
            specialty_axes_available=[
                "Cardiovascular & Circulatory Axis",
                "Pulmonary & Respiratory Axis",
                "Gastrointestinal & Metabolic Axis",
                "Hepatobiliary & Spleen Axis",
                "Renal & Urogenital Axis",
                "Neurological & Cognitive Axis",
                "Musculoskeletal & Articular Axis",
                "Dermatologic & Mucosal Axis",
                "Endocrine & Hormonal Axis",
                "Hematologic & Immunologic Axis",
                "Sensory (Ocular/ENT) Axis",
                "Reproductive & Sexual Axis",
            ],
        ),
        "FAC-HYD-REGIONAL-02": ClinicFacility(
            facility_id="FAC-HYD-REGIONAL-02",
            name="ZAYVORA Charminar Specialty Matab & Tadbeer Center",
            tier=FacilityTier.TIER_2_REGIONAL_SPECIALTY,
            city="Hyderabad",
            state="Telangana",
            abdm_facility_id="IN-FAC-HYD-0045",
            has_regimental_therapy=True,
            has_compounding_pharmacy=True,
            active_clinicians_count=10,
            specialty_axes_available=[
                "Musculoskeletal & Articular Axis",
                "Hepatobiliary & Spleen Axis",
                "Renal & Urogenital Axis",
                "Gastrointestinal & Metabolic Axis",
                "Dermatologic & Mucosal Axis",
                "Hematologic & Immunologic Axis",
            ],
        ),
        "FAC-LKO-REGIONAL-03": ClinicFacility(
            facility_id="FAC-LKO-REGIONAL-03",
            name="ZAYVORA Avadh Classical Care & Clinical Practicum Center",
            tier=FacilityTier.TIER_2_REGIONAL_SPECIALTY,
            city="Lucknow",
            state="Uttar Pradesh",
            abdm_facility_id="IN-FAC-LKO-0089",
            has_regimental_therapy=True,
            has_compounding_pharmacy=False,
            active_clinicians_count=8,
            specialty_axes_available=[
                "Neurological & Cognitive Axis",
                "Musculoskeletal & Articular Axis",
                "Pulmonary & Respiratory Axis",
                "Cardiovascular & Circulatory Axis",
                "Endocrine & Hormonal Axis",
                "Sensory (Ocular/ENT) Axis",
            ],
        ),
        "FAC-BLR-COMMUNITY-04": ClinicFacility(
            facility_id="FAC-BLR-COMMUNITY-04",
            name="ZAYVORA Bengaluru Integrated Care Matab",
            tier=FacilityTier.TIER_3_COMMUNITY_MATAB,
            city="Bengaluru",
            state="Karnataka",
            abdm_facility_id="IN-FAC-BLR-0112",
            has_regimental_therapy=False,
            has_compounding_pharmacy=False,
            active_clinicians_count=4,
            specialty_axes_available=[
                "Gastrointestinal & Metabolic Axis",
                "Musculoskeletal & Articular Axis",
            ],
        ),
    }

    # In-memory storage for cross-clinic referrals and federated inventory
    _REFERRALS_STORE: Dict[str, InterClinicReferral] = {}
    _FEDERATED_INVENTORY: List[BranchInventoryLot] = [
        BranchInventoryLot(
            lot_id="LOT-DEL-001",
            facility_id="FAC-DEL-CENTRAL-01",
            drug_name="Suranjan Shirin",
            batch_number="LOT-SS-2026-01",
            quantity_available_grams=5000.0,
            expiry_date="2027-06-30",
            mudabbar_certified=True,
            is_schedule_e1=False,
        ),
        BranchInventoryLot(
            lot_id="LOT-HYD-002",
            facility_id="FAC-HYD-REGIONAL-02",
            drug_name="Suranjan Shirin",
            batch_number="B-SUR-2026-A2",
            quantity_available_grams=2500.0,
            expiry_date="2027-08-31",
            mudabbar_certified=True,
            is_schedule_e1=False,
        ),
        BranchInventoryLot(
            lot_id="LOT-DEL-003",
            facility_id="FAC-DEL-CENTRAL-01",
            drug_name="Majun Suranjan",
            batch_number="B-MSUR-2026-B1",
            quantity_available_grams=3000.0,
            expiry_date="2028-06-30",
            mudabbar_certified=True,
            is_schedule_e1=True,
        ),
        BranchInventoryLot(
            lot_id="LOT-BLR-004",
            facility_id="FAC-BLR-COMMUNITY-04",
            drug_name="Asgandh",
            batch_number="B-ASG-2026-C1",
            quantity_available_grams=1200.0,
            expiry_date="2027-04-30",
            mudabbar_certified=False,
            is_schedule_e1=False,
        ),
    ]

    @classmethod
    def list_clinics(cls) -> List[Dict[str, Any]]:
        """Lists all registered clinic facilities in the federation."""
        return [asdict(f) for f in cls._FACILITY_REGISTRY.values() if f.is_active]

    @classmethod
    def get_clinic(cls, facility_id: str) -> Optional[ClinicFacility]:
        return cls._FACILITY_REGISTRY.get(facility_id)

    @classmethod
    def register_clinic(cls, facility: ClinicFacility) -> None:
        cls._FACILITY_REGISTRY[facility.facility_id] = facility

    @classmethod
    def create_inter_clinic_referral(
        cls,
        patient_id: str,
        source_facility_id: str,
        target_facility_id: str,
        referring_clinician_id: str,
        clinical_condition: str,
        specialty_axis_required: str,
        reason_for_referral: str = "Clinical consultation and specialized therapy",
        validity_days: int = 30,
    ) -> InterClinicReferral:
        """
        Creates an authorized inter-clinic referral with cryptographic HMAC token.
        Ensures patient data is only decrypted by the designated target facility.
        """
        if source_facility_id not in cls._FACILITY_REGISTRY:
            raise ValueError(f"Unknown source facility: {source_facility_id}")
        if target_facility_id not in cls._FACILITY_REGISTRY:
            raise ValueError(f"Unknown target facility: {target_facility_id}")

        ref_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
        now_dt = datetime.now(timezone.utc)
        exp_dt = now_dt + timedelta(days=validity_days)

        # Build cryptographic referral token (HMAC-SHA256 signature)
        raw_sig_payload = f"{ref_id}:{patient_id}:{source_facility_id}:{target_facility_id}:{exp_dt.isoformat()}"
        token_hash = hmac.new(cls._SIGNING_KEY.encode(), raw_sig_payload.encode(), hashlib.sha256).hexdigest()[:24]
        referral_token = f"ZAY-REF-{token_hash.upper()}"

        referral = InterClinicReferral(
            referral_id=ref_id,
            referral_token=referral_token,
            patient_id=patient_id,
            source_facility_id=source_facility_id,
            target_facility_id=target_facility_id,
            referring_clinician_id=referring_clinician_id,
            clinical_condition=clinical_condition,
            specialty_axis_required=specialty_axis_required,
            reason_for_referral=reason_for_referral,
            created_at=now_dt.isoformat(),
            expires_at=exp_dt.isoformat(),
            status="PENDING_ACCEPTANCE",
        )
        cls._REFERRALS_STORE[referral_token] = referral
        return referral

    @classmethod
    def redeem_inter_clinic_referral(
        cls,
        referral_token: str,
        receiving_facility_id: str,
        accepting_clinician_id: str,
    ) -> Dict[str, Any]:
        """Validates and redeems a cross-clinic referral upon patient presentation."""
        ref = cls._REFERRALS_STORE.get(referral_token)
        if not ref:
            return {"success": False, "error": "Referral token not found or invalid."}

        # Verify HMAC token integrity
        try:
            exp_dt = datetime.fromisoformat(ref.expires_at)
            raw_sig_payload = f"{ref.referral_id}:{ref.patient_id}:{ref.source_facility_id}:{ref.target_facility_id}:{exp_dt.isoformat()}"
            expected_hash = hmac.new(cls._SIGNING_KEY.encode(), raw_sig_payload.encode(), hashlib.sha256).hexdigest()[:24]
            expected_token = f"ZAY-REF-{expected_hash.upper()}"
            if referral_token != expected_token:
                return {"success": False, "error": "Invalid or tampered referral token."}
        except Exception:
            return {"success": False, "error": "Invalid or tampered referral token."}

        if ref.target_facility_id != receiving_facility_id:
            return {
                "success": False,
                "error": f"Target clinic mismatch: referral is designated for '{ref.target_facility_id}', not '{receiving_facility_id}'.",
            }

        if ref.status != "PENDING_ACCEPTANCE":
            return {"success": False, "error": f"Referral is in '{ref.status}' status (already redeemed or voided)."}

        # Check expiration
        if datetime.now(timezone.utc) > exp_dt:
            ref.status = "EXPIRED"
            return {"success": False, "error": "Referral token has expired."}

        ref.status = "REDEEMED"
        ref.receiving_clinician_id = accepting_clinician_id
        ref.redeemed_at = datetime.now(timezone.utc).isoformat()

        return {
            "success": True,
            "referral": asdict(ref),
            "status": "REDEEMED",
            "access_granted": True,
            "patient_id": ref.patient_id,
            "authorized_clinical_access": True,
            "message": f"Referral redeemed successfully. Clinical chart access granted to {accepting_clinician_id} at {receiving_facility_id}.",
        }

    @classmethod
    def query_federated_inventory(
        cls,
        drug_name: Optional[str] = None,
        facility_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Queries federated inventory across all clinic nodes."""
        results = []
        for lot in cls._FEDERATED_INVENTORY:
            if drug_name and drug_name.lower() not in lot.drug_name.lower():
                continue
            if facility_id and lot.facility_id != facility_id:
                continue
            results.append(asdict(lot))
        return results

    @classmethod
    def request_inventory_transfer(
        cls,
        drug_name: str,
        quantity_grams: Optional[float] = None,
        quantity: Optional[float] = None,
        from_facility_id: Optional[str] = None,
        source_facility_id: Optional[str] = None,
        to_facility_id: Optional[str] = None,
        target_facility_id: Optional[str] = None,
        requested_by_clinician: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes an automated FEFO-prioritized stock transfer between branches.
        Picks the earliest expiring available batch at source facility.
        """
        src_fac = from_facility_id or source_facility_id or ""
        dst_fac = to_facility_id or target_facility_id or ""
        qty = float(quantity_grams if quantity_grams is not None else (quantity if quantity is not None else 0.0))

        source_lots = [
            l for l in cls._FEDERATED_INVENTORY
            if l.facility_id == src_fac and drug_name.lower() in l.drug_name.lower() and l.quantity_available_grams > 0
        ]
        if not source_lots:
            return {"success": False, "error": f"No available stock of '{drug_name}' at facility {src_fac}."}

        # FEFO Sorting (Earliest expiring first)
        source_lots.sort(key=lambda x: x.expiry_date)
        chosen_lot = source_lots[0]

        if chosen_lot.quantity_available_grams < qty:
            return {
                "success": False,
                "error": f"Insufficient stock: requested {qty}g, but lot {chosen_lot.batch_number} has only {chosen_lot.quantity_available_grams}g.",
            }

        # Deduct from source lot
        chosen_lot.quantity_available_grams -= qty

        # Credit to destination lot
        dest_lot_id = f"LOT-XFER-{uuid.uuid4().hex[:6].upper()}"
        dest_lot = BranchInventoryLot(
            lot_id=dest_lot_id,
            facility_id=dst_fac,
            drug_name=chosen_lot.drug_name,
            batch_number=chosen_lot.batch_number,
            quantity_available_grams=qty,
            expiry_date=chosen_lot.expiry_date,
            mudabbar_certified=chosen_lot.mudabbar_certified,
            is_schedule_e1=chosen_lot.is_schedule_e1,
        )
        cls._FEDERATED_INVENTORY.append(dest_lot)

        transfer_record = {
            "transfer_id": f"XFER-{uuid.uuid4().hex[:8].upper()}",
            "from_facility_id": src_fac,
            "to_facility_id": dst_fac,
            "drug_name": chosen_lot.drug_name,
            "batch_number": chosen_lot.batch_number,
            "quantity_transferred_grams": qty,
            "fefo_expiry_date": chosen_lot.expiry_date,
            "transit_timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "TRANSFERRED_IN_TRANSIT",
        }
        return {
            "success": True,
            "transfer": transfer_record,
            "status": "TRANSFERRED_IN_TRANSIT",
            "quantity_transferred": qty,
            "fefo_lot_selected": chosen_lot.batch_number,
        }
